class FootnoteNotes(gl.Contract):
    appeal_window_seconds: u256
    owner: Address
    recheck: Address
    appeals: Address
    bonds: Address
    wired: bool
    hosts: DynArray[str]
    notes: TreeMap[str, str]
    ids: DynArray[str]
    open_counts: TreeMap[str, u256]
    post_counts: TreeMap[str, u256]
    pending: TreeMap[str, str]

    def __init__(self, hosts_json: str, appeal_window_seconds: int = DEFAULT_APPEAL_WINDOW):
        self.appeal_window_seconds = u256(checked_window(appeal_window_seconds, "appeal window"))
        require(int(gl.message.chain_id) == 61999, 'StudioNet only')
        self.owner = gl.message.sender_address
        hosts = json.loads(hosts_json)
        require(type(hosts) is list and 0 < len(hosts) <= 64, 'fixed host allowlist required')
        for host in sorted(set(hosts)):
            require(type(host) is str and re.fullmatch(r'[a-z0-9.-]+', host) is not None, 'invalid host')
            self.hosts.append(host)
        self.wired = False

    @gl.public.write
    def wire(self, recheck: str, appeals: str, bonds: str) -> None:
        require(gl.message.sender_address == self.owner and not self.wired, 'one-time deployer wiring only')
        addresses = [Address(recheck), Address(appeals), Address(bonds)]
        require(len(set(str(a) for a in addresses + [gl.message.contract_address])) == 4, 'distinct contract addresses required')
        self.recheck, self.appeals, self.bonds = addresses
        self.wired = True

    def _get(self, note_id):
        require(note_id in self.notes, 'note not found')
        return json.loads(self.notes[note_id])

    def _save(self, note_id, record):
        self.notes[note_id] = packed(record)

    @gl.public.write
    def create_note(self, note_id: str, post_uri: str, sources_json: str) -> None:
        require(self.wired, 'deployment is not wired')
        require(re.fullmatch(r'[a-z0-9-]{1,64}', note_id) is not None, 'invalid note ID')
        require(note_id not in self.notes, 'note ID already used')
        writer = str(gl.message.sender_address).lower()
        count = int(self.open_counts[writer]) if writer in self.open_counts else 0
        require(count < 20, '20 open notes per address quota')
        uri_checked(post_uri)
        key = writer + '|' + post_uri
        post_count = int(self.post_counts[key]) if key in self.post_counts else 0
        require(post_count < 3, 'three notes per post per address quota')
        # No global note cap: bounded inputs and per-address quotas prevent a shared bottleneck.
        urls = sources_checked(json.loads(sources_json), list(self.hosts))
        bond = json.loads(gl.get_contract_at(self.bonds).view().get_bond(note_id))
        require(bond['writer'] == writer and bond['status'] == 'locked' and now() < bond['deadline'],
                'finalized writer bond required')
        decision = judgment(post_uri, urls)
        require(decision['post_available'], 'post unavailable at creation')
        record = {'id': note_id, 'writer': writer, 'post_uri': post_uri, 'fingerprint': decision['fingerprint'],
                  'sources': urls, 'created_at': now(), 'deadline': bond['deadline'], 'status': 'pending_finality',
                  'version': 1, 'history': [], 'open': True}
        self._save(note_id, record)
        self.ids.append(note_id)
        self.pending[note_id] = packed({'version': 1, 'decision': {**stored(decision), 'sources': urls}, 'reason': 'CREATED', 'operation': ''})
        self.open_counts[writer] = u256(count + 1)
        self.post_counts[key] = u256(post_count + 1)
        gl.get_contract_at(gl.message.contract_address).emit(on='finalized').finalize_note(note_id, 1)

    @gl.public.write
    def apply_update(self, note_id: str, expected_version: int, decision_json: str, reason: str, operation: str) -> None:
        require(self.wired and gl.message.sender_address in (self.recheck, self.appeals), 'only Recheck or Appeals may update labels')
        require((gl.message.sender_address == self.recheck and reason == 'RECHECK') or
                (gl.message.sender_address == self.appeals and reason == 'APPEAL'), 'caller reason mismatch')
        if reason == 'RECHECK':
            require(not gl.get_contract_at(self.appeals).view().has_open_appeal(note_id), 'note has an open appeal; recheck after it is decided')
        record = self._get(note_id)
        require(record['status'] == 'active' and record['version'] == expected_version and note_id not in self.pending,
                'note version changed or update pending')
        decision = json.loads(decision_json)
        require(decision['evidence_label'] in EVIDENCE and decision['tone_label'] in TONES
                and decision['IS_ALLEGATION_ABOUT_PERSON'] in ('yes', 'no'), 'invalid decision')
        prior = record['history'][-1]['decision']
        allegation = prior['IS_ALLEGATION_ABOUT_PERSON'] == 'yes' or decision['IS_ALLEGATION_ABOUT_PERSON'] == 'yes'
        if allegation:
            decision['IS_ALLEGATION_ABOUT_PERSON'] = 'yes'
            if decision['evidence_label'] not in ('SUPPORTED', 'UNSUPPORTED'):
                decision['evidence_label'] = 'UNSUPPORTED'
            # Prevent authorized callers accidentally persisting person names in quotes.
            decision = stored(decision) if any('quote' in c for c in decision.get('citations', [])) else decision
        urls = sources_checked(decision['sources'], list(self.hosts))
        require(decision['fingerprint'] == record['fingerprint'], 'immutable post fingerprint')
        require(decision['evidence_label'] == 'UNSUPPORTED' or len(decision.get('citations', [])) > 0,
                'grounded citation required')
        for citation in decision.get('citations', []):
            require(citation['url'] in urls, 'citation must use supplied source')
        # Copy only known fields, never arbitrary model/caller text.
        clean = {k: decision[k] for k in ('evidence_label', 'tone_label', 'IS_ALLEGATION_ABOUT_PERSON',
                 'citations', 'source_digests', 'post_available', 'fingerprint')}
        clean['sources'] = urls
        self.pending[note_id] = packed({'version': expected_version + 1, 'decision': clean,
                                      'reason': reason, 'operation': operation})
        record['status'] = 'pending_finality'
        self._save(note_id, record)
        gl.get_contract_at(gl.message.contract_address).emit(on='finalized').finalize_note(note_id, expected_version + 1)

    @gl.public.write
    def finalize_note(self, note_id: str, version: int) -> None:
        require(gl.message.sender_address == gl.message.contract_address, 'self callback only')
        if note_id not in self.pending:
            return
        update = json.loads(self.pending[note_id])
        if update['version'] != version:
            return
        record = self._get(note_id)
        if update['reason'] == 'RECHECK' and gl.get_contract_at(self.appeals).view().has_open_appeal(note_id):
            # An appeal opened after staging: discard the staged recheck, preserve its appealed version.
            record['status'] = 'active'
            self._save(note_id, record)
            del self.pending[note_id]
            return
        record['history'].append({**update, 'at': now()})
        record['version'], record['status'] = version, 'active'
        record['sources'] = update['decision'].get('sources', record['sources'])
        self._save(note_id, record)
        del self.pending[note_id]

    @gl.public.write
    def resume_note(self, note_id: str) -> None:
        require(note_id in self.pending, 'note has no pending callback')
        update = json.loads(self.pending[note_id])
        gl.get_contract_at(gl.message.contract_address).emit(on='finalized').finalize_note(note_id, update['version'])

    @gl.public.write
    def close_note(self, note_id: str) -> None:
        require(gl.message.sender_address == self.bonds, 'only Bonds closes open quota')
        if note_id not in self.notes:
            return
        record = self._get(note_id)
        if record['open']:
            record['open'] = False
            self.open_counts[record['writer']] = u256(int(self.open_counts[record['writer']]) - 1)
            self._save(note_id, record)

    @gl.public.view
    def get_note(self, note_id: str) -> str:
        return packed(self._get(note_id))

    @gl.public.view
    def list_notes(self, offset: int, limit: int) -> list[str]:
        require(offset >= 0 and 1 <= limit <= 50, 'page limit 1–50')
        return list(self.ids)[offset:offset + limit]

    @gl.public.view
    def get_config(self) -> str:
        return packed({'appeal_window_seconds': int(self.appeal_window_seconds), 'wired': self.wired, 'hosts': list(self.hosts), 'recheck': str(self.recheck),
                       'appeals': str(self.appeals), 'bonds': str(self.bonds)})

    @gl.public.view
    def get_quota(self, writer: str, post_uri: str) -> str:
        writer = str(Address(writer)).lower()
        key = writer + '|' + post_uri
        return packed({'open': int(self.open_counts[writer]) if writer in self.open_counts else 0,
                       'per_post': int(self.post_counts[key]) if key in self.post_counts else 0})
