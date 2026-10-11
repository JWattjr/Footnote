class FootnoteRecheck(gl.Contract):
    notes: Address
    attempts: TreeMap[str, str]
    counter: u256
    operations: TreeMap[str, str]

    def __init__(self, notes: str):
        self.notes = Address(notes)
        self.counter = u256(0)

    @gl.public.write
    def recheck(self, note_id: str, extra_sources_json: str) -> str:
        note = json.loads(gl.get_contract_at(self.notes).view().get_note(note_id))
        require(note['status'] == 'active', 'note is awaiting finality')
        config = json.loads(gl.get_contract_at(self.notes).view().get_config())
        extra = json.loads(extra_sources_json)
        require(type(extra) is list and len(extra) <= 8, 'invalid added sources')
        urls = sources_checked(note['sources'] + extra, config['hosts'])
        key = note_id + ':' + str(note['version'])
        previous = json.loads(self.attempts[key]) if key in self.attempts else {'uncertain': 0, 'sources': urls, 'pending': False}
        require(not previous['pending'], 'recheck pending for this version')
        # After two inconclusive attempts, unchanged input URLs are rejected before consensus.
        # New allowlisted sources permit an evidence-change probe; content-only changes require
        # a distinct correction URL, since detecting changed content itself needs a web fetch.
        require(previous['uncertain'] < 2 or urls != previous['sources'], 'two UNCERTAIN rechecks; add changed evidence URL')
        prior = note['history'][-1]['decision']
        decision = judgment(note['post_uri'], urls, note['fingerprint'], prior['IS_ALLEGATION_ABOUT_PERSON'] == 'yes')
        changed = compared(decision) != compared({**prior, 'citations': decision['citations'] if prior['IS_ALLEGATION_ABOUT_PERSON'] == 'yes' else prior['citations']})
        evidence_changed = decision['source_digests'] != prior['source_digests'] or urls != note['sources']
        # An unchanged label with new canonical evidence still creates an auditable version.
        outcome = 'UPDATED' if decision['post_available'] and (changed or evidence_changed) else 'UNCERTAIN'
        if not decision['post_available']:
            outcome = 'POST_UNAVAILABLE'
        self.counter = u256(int(self.counter) + 1)
        operation = 'recheck-' + str(self.counter)
        previous.update(sources=urls, pending=True)
        self.attempts[key] = packed(previous)
        self.operations[operation] = packed({'note_id': note_id, 'version': note['version'], 'outcome': outcome,
                                            'decision': stored(decision), 'sources': urls, 'status': 'pending_finality'})
        gl.get_contract_at(gl.message.contract_address).emit(on='finalized').finalize_recheck(operation)
        return operation

    @gl.public.write
    def finalize_recheck(self, operation: str) -> None:
        require(gl.message.sender_address == gl.message.contract_address, 'self callback only')
        record = json.loads(self.operations[operation])
        if record['status'] != 'pending_finality':
            return
        record['status'] = 'finalized'
        key = record['note_id'] + ':' + str(record['version'])
        attempts = json.loads(self.attempts[key])
        attempts['pending'] = False
        if record['outcome'] == 'UNCERTAIN':
            attempts['uncertain'] += 1
        self.attempts[key] = packed(attempts)
        self.operations[operation] = packed(record)
        if record['outcome'] in ('UPDATED', 'POST_UNAVAILABLE'):
            decision = {**record['decision'], 'sources': record['sources']}
            gl.get_contract_at(self.notes).emit(on='finalized').apply_update(
                record['note_id'], record['version'], packed(decision), 'RECHECK', operation)

    @gl.public.view
    def get_operation(self, operation: str) -> str:
        require(operation in self.operations, 'operation not found')
        return self.operations[operation]
