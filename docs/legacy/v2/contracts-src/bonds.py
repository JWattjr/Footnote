import base64
from genlayer.py import calldata

RECEIPT_RPC = 'https://studio.genlayer.com/api'

def receipt_hash(value):
    require(type(value) is str and len(value) == 66 and value.startswith('0x')
            and all(c in '0123456789abcdefABCDEF' for c in value[2:]), 'invalid receipt hash')
    return value.lower()

def protocol_receipt(tx_hash):
    response = gl.nondet.web.post(RECEIPT_RPC,
        body=packed({'jsonrpc': '2.0', 'id': 1, 'method': 'eth_getTransactionByHash', 'params': [tx_hash]}).encode(),
        headers={'Content-Type': 'application/json'})
    require(response.status == 200, 'protocol receipt unavailable; keep claim pending')
    payload = json.loads(response.body.decode('utf-8'))
    require('error' not in payload and type(payload.get('result')) is dict, 'protocol receipt unavailable; keep claim pending')
    tx = payload['result']
    require(receipt_hash(tx.get('hash')) == tx_hash, 'receipt hash mismatch')
    return tx

def transfer_decision(parent, child, contract, participant, claim_id, attempt, amount):
    require(parent.get('status') == 'FINALIZED', 'withdraw transaction not finalized')
    require(str(parent.get('from_address', '')).lower() == participant and str(parent.get('to_address', '')).lower() == contract,
            'withdraw sender or contract mismatch')
    leader = (parent.get('consensus_data') or {}).get('leader_receipt', [])
    require(parent.get('result') == 6 and len(leader) > 0 and leader[0].get('execution_result') == 'SUCCESS', 'withdraw execution failed')
    encoded = parent.get('data', {}).get('calldata')
    require(type(encoded) is str, 'withdraw calldata missing')
    call = calldata.decode(base64.b64decode(encoded, validate=True))
    require(call == {'method': 'withdraw', 'args': [claim_id, attempt]}, 'withdraw claim or attempt mismatch')
    children = parent.get('triggered_transactions')
    require(type(children) is list and len(children) == 1 and receipt_hash(children[0]) == receipt_hash(child.get('hash')), 'transfer parent mismatch')
    require(str(child.get('from_address', '')).lower() == contract and str(child.get('to_address', '')).lower() == participant
            and str(child.get('value')) == str(amount), 'transfer recipient or amount mismatch')
    require(child.get('type') == 0 and child.get('consensus_data') is None and child.get('triggered_on') == 'finalized', 'not a finalized native transfer')
    require(child.get('status') == 'FINALIZED', 'native transfer pending')
    require(type(child.get('value_credited')) is bool, 'native credit unknown; keep pending')
    return 'paid' if child['value_credited'] else 'failed'

@gl.evm.contract_interface
class Recipient:
    class View:
        pass
    class Write:
        pass

class FootnoteBonds(gl.Contract):
    appeal_window_seconds: u256
    release_delay_seconds: u256
    fundings: TreeMap[str, str]
    owner: Address
    notes: Address
    appeals: Address
    wired: bool
    bonds: TreeMap[str, str]
    deposits: TreeMap[str, str]
    claims: TreeMap[str, str]
    reputation: TreeMap[str, str]
    total_received: u256
    total_paid: u256

    def __init__(self, notes: str, appeal_window_seconds: int = DEFAULT_APPEAL_WINDOW, release_delay_seconds: int = DEFAULT_APPEAL_WINDOW):
        self.appeal_window_seconds = u256(checked_window(appeal_window_seconds, "appeal window"))
        self.release_delay_seconds = u256(checked_window(release_delay_seconds, "bond release delay"))
        require(release_delay_seconds >= appeal_window_seconds, "bond release delay must cover appeal window")
        require(int(gl.message.chain_id) == 61999, 'StudioNet only')
        self.owner, self.notes = gl.message.sender_address, Address(notes)
        self.wired = False
        self.total_received, self.total_paid = u256(0), u256(0)

    @gl.public.write
    def wire(self, appeals: str) -> None:
        require(gl.message.sender_address == self.owner and not self.wired, 'one-time deployer wiring only')
        self.appeals, self.wired = Address(appeals), True

    @gl.public.write.payable
    def stake(self, note_id: str) -> None:
        require(self.wired, 'deployment is not wired')
        require(re.fullmatch(r'[a-z0-9-]{1,64}', note_id) is not None and note_id not in self.bonds, 'bond ID invalid or used')
        require(2 * GEN <= int(gl.message.value) <= 20 * GEN, 'bond 2–20 simulated GEN')
        record = {'note_id': note_id, 'writer': str(gl.message.sender_address).lower(), 'amount': str(gl.message.value),
                  'created_at': now(), 'deadline': now() + int(self.appeal_window_seconds), 'release_at': now() + int(self.release_delay_seconds), 'status': 'pending_finality'}
        self.bonds[note_id] = packed(record)
        self.total_received = u256(int(self.total_received) + int(gl.message.value))
        gl.get_contract_at(gl.message.contract_address).emit(on='finalized').finalize_stake(note_id)

    @gl.public.write
    def finalize_stake(self, note_id: str) -> None:
        require(gl.message.sender_address == gl.message.contract_address, 'self callback only')
        record = json.loads(self.bonds[note_id])
        if record['status'] == 'pending_finality':
            record['status'] = 'locked'
            self.bonds[note_id] = packed(record)

    @gl.public.write.payable
    def fund_appeal(self, note_id: str, version: int) -> str:
        require(self.wired, 'deployment is not wired')
        note = json.loads(gl.get_contract_at(self.notes).view().get_note(note_id))
        require(note['status'] == 'active' and note['version'] == version and now() < note['deadline'], 'appeal version unavailable or window closed')
        amount = int(gl.message.value)
        require(amount >= 2 * GEN, 'deposit at least 2 simulated GEN')
        appellant = str(gl.message.sender_address).lower()
        funding_id = note_id + ':' + str(version) + ':' + appellant
        require(funding_id not in self.fundings, 'funding ID already used')
        self.fundings[funding_id] = packed({'id': funding_id, 'note_id': note_id, 'version': version,
            'appellant': appellant, 'amount': str(amount), 'status': 'pending_finality'})
        self.total_received = u256(int(self.total_received) + amount)
        gl.get_contract_at(gl.message.contract_address).emit(on='finalized').finalize_funding(funding_id)
        return funding_id

    @gl.public.write
    def finalize_funding(self, funding_id: str) -> None:
        require(gl.message.sender_address == gl.message.contract_address, 'self callback only')
        funding = json.loads(self.fundings[funding_id])
        if funding['status'] == 'pending_finality':
            funding['status'] = 'funded'
            self.fundings[funding_id] = packed(funding)

    @gl.public.write
    def activate_deposit(self, appeal_id: str) -> None:
        require(self.wired and gl.message.sender_address == self.appeals, 'only Appeals activates deposits')
        if appeal_id in self.deposits:
            return
        appeal = json.loads(gl.get_contract_at(self.appeals).view().get_appeal(appeal_id))
        require(appeal['status'] in ('open', 'cancelled_pending_settlement'), 'appeal is not open or cancelling')
        funding = json.loads(self.fundings[appeal['funding_id']])
        require(funding['note_id'] == appeal['note_id']
                and funding['appellant'] == appeal['appellant'] and funding['amount'] == appeal['deposit'], 'appeal funding binding mismatch')
        if funding['status'] == 'refunded':
            require(appeal['status'] == 'cancelled_pending_settlement', 'funding was refunded; cancel after deadline plus grace')
            claim_id = 'funding:' + appeal['funding_id']
            require(claim_id in self.claims, 'funding refund must be allocated')
            claim = json.loads(self.claims[claim_id])
            require(claim['recipient'] == funding['appellant'] and claim['amount'] == funding['amount'], 'funding refund binding mismatch')
            self.deposits[appeal_id] = packed({'note_id': appeal['note_id'], 'appellant': appeal['appellant'],
                'amount': funding['amount'], 'status': 'settled', 'refund_claim': claim_id})
            gl.get_contract_at(self.appeals).emit(on='finalized').mark_settled(appeal_id)
            return
        require(funding['status'] == 'funded', 'resume funding finality before activating deposit')
        funding['status'] = 'consumed'
        self.fundings[appeal['funding_id']] = packed(funding)
        self.deposits[appeal_id] = packed({'note_id': appeal['note_id'], 'appellant': appeal['appellant'],
            'amount': funding['amount'], 'status': 'pending_finality'})
        gl.get_contract_at(gl.message.contract_address).emit(on='finalized').finalize_hold(appeal_id)

    @gl.public.write
    def finalize_hold(self, appeal_id: str) -> None:
        require(gl.message.sender_address == gl.message.contract_address, 'self callback only')
        record = json.loads(self.deposits[appeal_id])
        if record['status'] == 'pending_finality':
            record['status'] = 'held'
            self.deposits[appeal_id] = packed(record)

    @gl.public.write
    def refund_unopened(self, funding_id: str) -> None:
        require(funding_id in self.fundings, 'funding not found')
        funding = json.loads(self.fundings[funding_id])
        require(funding['status'] == 'funded', 'funding already consumed, refunded or pending')
        appeal_id = funding['note_id'] + ':' + str(funding['version'])
        remote = gl.get_contract_at(self.appeals).view()
        if remote.has_appeal(appeal_id):
            appeal = json.loads(remote.get_appeal(appeal_id))
            require(appeal['funding_id'] != funding_id, 'funding belongs to an appeal; cancel stale or settle it')
        funding['status'] = 'refund_pending_finality'
        self.fundings[funding_id] = packed(funding)
        gl.get_contract_at(gl.message.contract_address).emit(on='finalized').finalize_refund(funding_id)

    @gl.public.write
    def finalize_refund(self, funding_id: str) -> None:
        require(gl.message.sender_address == gl.message.contract_address, 'self callback only')
        funding = json.loads(self.fundings[funding_id])
        require(funding['status'] == 'refund_pending_finality', 'funding refund callback already applied')
        self._allocate('funding:' + funding_id, funding['appellant'], int(funding['amount']))
        funding['status'] = 'refunded'
        self.fundings[funding_id] = packed(funding)

    def _allocate(self, claim_id, recipient, amount):
        require(claim_id not in self.claims, 'claim already allocated')
        self.claims[claim_id] = packed({'id': claim_id, 'recipient': recipient, 'amount': str(amount), 'attempt': 0, 'status': 'available'})

    def _reputation(self, writer, outcome):
        stats = json.loads(self.reputation[writer]) if writer in self.reputation else {'upheld': 0, 'overturned': 0}
        stats[outcome] += 1
        self.reputation[writer] = packed(stats)

    @gl.public.write
    def settle_appeal(self, appeal_id: str) -> None:
        require(appeal_id in self.deposits, 'deposit not found')
        deposit = json.loads(self.deposits[appeal_id])
        require(deposit['status'] == 'held', 'deposit already settled or pending')
        appeal = json.loads(gl.get_contract_at(self.appeals).view().get_appeal(appeal_id))
        require(appeal['status'] in ('finalized', 'cancelled_pending_settlement'), 'appeal result not finalized')
        bond = json.loads(self.bonds[deposit['note_id']])
        if appeal['outcome'] == 'OVERTURNED':
            note = json.loads(gl.get_contract_at(self.notes).view().get_note(deposit['note_id']))
            require(note['status'] == 'active' and any(v['reason'] == 'APPEAL' and v['operation'] == appeal_id for v in note['history']),
                    'appeal label update must be finalized before settlement')
            require(bond['status'] == 'locked', 'writer bond already settled')
        deposit['status'] = 'settlement_pending_finality'
        self.deposits[appeal_id] = packed(deposit)
        gl.get_contract_at(gl.message.contract_address).emit(on='finalized').finalize_settlement(appeal_id)

    @gl.public.write
    def finalize_settlement(self, appeal_id: str) -> None:
        require(gl.message.sender_address == gl.message.contract_address, 'self callback only')
        deposit = json.loads(self.deposits[appeal_id])
        require(deposit['status'] == 'settlement_pending_finality', 'settlement callback already applied')
        appeal = json.loads(gl.get_contract_at(self.appeals).view().get_appeal(appeal_id))
        bond = json.loads(self.bonds[deposit['note_id']])
        if appeal['outcome'] == 'OVERTURNED':
            require(bond['status'] == 'locked', 'writer bond already settled')
            self._allocate('bond:' + deposit['note_id'], deposit['appellant'], int(bond['amount']))
            bond['status'] = 'overturned'
            self.bonds[deposit['note_id']] = packed(bond)
            self._reputation(bond['writer'], 'overturned')
            gl.get_contract_at(self.notes).emit(on='finalized').close_note(deposit['note_id'])
        recipient = bond['writer'] if appeal['outcome'] == 'UPHELD' else deposit['appellant']
        self._allocate('deposit:' + appeal_id, recipient, int(deposit['amount']))
        deposit['status'] = 'settled'
        self.deposits[appeal_id] = packed(deposit)
        gl.get_contract_at(self.appeals).emit(on='finalized').mark_settled(appeal_id)

    @gl.public.write
    def release(self, note_id: str) -> None:
        require(note_id in self.bonds, 'bond not found')
        bond = json.loads(self.bonds[note_id])
        require(bond['status'] == 'locked' and now() >= bond['release_at'], 'bond locked until appeal window closes')
        require(not gl.get_contract_at(self.appeals).view().has_open_appeal(note_id), 'resolve outstanding appeal first')
        bond['status'] = 'release_pending_finality'
        self.bonds[note_id] = packed(bond)
        gl.get_contract_at(gl.message.contract_address).emit(on='finalized').finalize_release(note_id)

    @gl.public.write
    def finalize_release(self, note_id: str) -> None:
        require(gl.message.sender_address == gl.message.contract_address, 'self callback only')
        bond = json.loads(self.bonds[note_id])
        if bond['status'] != 'release_pending_finality':
            return
        self._allocate('bond:' + note_id, bond['writer'], int(bond['amount']))
        bond['status'] = 'survived'
        self.bonds[note_id] = packed(bond)
        self._reputation(bond['writer'], 'upheld')
        # A reserved bond whose note creation failed can still be recovered.
        gl.get_contract_at(self.notes).emit(on='finalized').close_note(note_id)

    @gl.public.write
    def withdraw(self, claim_id: str, attempt: int) -> None:
        require(claim_id in self.claims, 'no allocated claim')
        claim = json.loads(self.claims[claim_id])
        require(claim['recipient'] == str(gl.message.sender_address).lower(), 'claim belongs to another wallet')
        require(claim['status'] in ('available', 'failed'), 'claim already pending or paid')
        require(attempt == claim['attempt'] + 1, 'use next withdrawal attempt')
        amount = int(claim['amount'])
        require(int(self.balance) >= amount, 'contract balance insufficient')
        if claim['status'] == 'failed':
            require(int(self.balance) >= int(self.total_received) - int(self.total_paid), 'wait for failed credit refund and other verifications')
        claim.update(attempt=attempt, status='pending', claim_hash='', transfer_hash='')
        self.claims[claim_id] = packed(claim)
        Recipient(gl.message.sender_address).emit_transfer(value=u256(amount))

    @gl.public.write
    def verify_claim(self, claim_id: str, parent_hash: str) -> str:
        require(claim_id in self.claims, 'claim not found')
        claim = json.loads(self.claims[claim_id])
        require(claim['status'] == 'pending', 'no pending withdrawal')
        parent_hash = receipt_hash(parent_hash)
        contract = str(gl.message.contract_address).lower()
        def observe():
            parent = protocol_receipt(parent_hash)
            children = parent.get('triggered_transactions')
            require(type(children) is list and len(children) == 1, 'native child not available')
            child_hash = receipt_hash(children[0])
            child = protocol_receipt(child_hash)
            outcome = transfer_decision(parent, child, contract, claim['recipient'], claim_id, claim['attempt'], int(claim['amount']))
            return {'outcome': outcome, 'transfer_hash': child_hash}
        def validator(leader):
            return isinstance(leader, gl.vm.Return) and observe() == leader.calldata
        evidence = gl.vm.run_nondet_unsafe(observe, validator)
        claim.update(status=evidence['outcome'] + '_pending_finality', claim_hash=parent_hash, transfer_hash=evidence['transfer_hash'])
        self.claims[claim_id] = packed(claim)
        gl.get_contract_at(gl.message.contract_address).emit(on='finalized').finalize_claim(claim_id, claim['attempt'])
        return claim['status']

    @gl.public.write
    def finalize_claim(self, claim_id: str, attempt: int) -> None:
        require(gl.message.sender_address == gl.message.contract_address, 'self callback only')
        claim = json.loads(self.claims[claim_id])
        if claim['attempt'] != attempt:
            return
        if claim['status'] == 'paid_pending_finality':
            claim['status'] = 'paid'
            self.total_paid = u256(int(self.total_paid) + int(claim['amount']))
        elif claim['status'] == 'failed_pending_finality':
            claim['status'] = 'failed'
        self.claims[claim_id] = packed(claim)

    @gl.public.view
    def get_bond(self, note_id: str) -> str:
        require(note_id in self.bonds, 'bond not found')
        return self.bonds[note_id]

    @gl.public.view
    def get_deposit(self, appeal_id: str) -> str:
        require(appeal_id in self.deposits, 'deposit not found')
        return self.deposits[appeal_id]

    @gl.public.view
    def has_deposit(self, appeal_id: str) -> bool:
        return appeal_id in self.deposits

    @gl.public.view
    def get_claim(self, claim_id: str) -> str:
        require(claim_id in self.claims, 'claim not found')
        return self.claims[claim_id]

    @gl.public.view
    def get_reputation(self, writer: str) -> str:
        writer = str(Address(writer)).lower()
        return self.reputation[writer] if writer in self.reputation else packed({'upheld': 0, 'overturned': 0})

    @gl.public.view
    def get_totals(self) -> str:
        return packed({'received': str(self.total_received), 'paid': str(self.total_paid)})


    @gl.public.write
    def resume_deposit(self, appeal_id: str) -> None:
        require(appeal_id in self.deposits, 'deposit not found; resume appeal activation')
        deposit = json.loads(self.deposits[appeal_id])
        if deposit['status'] == 'pending_finality':
            gl.get_contract_at(gl.message.contract_address).emit(on='finalized').finalize_hold(appeal_id)
        elif deposit['status'] == 'settlement_pending_finality':
            gl.get_contract_at(gl.message.contract_address).emit(on='finalized').finalize_settlement(appeal_id)
        elif deposit['status'] == 'settled':
            appeal = json.loads(gl.get_contract_at(self.appeals).view().get_appeal(appeal_id))
            if appeal['status'] not in ('settled', 'CANCELLED'):
                gl.get_contract_at(self.appeals).emit(on='finalized').mark_settled(appeal_id)
        else:
            gl.get_contract_at(gl.message.contract_address).emit(on='finalized').settle_appeal(appeal_id)

    @gl.public.write
    def resume_bond(self, note_id: str) -> None:
        require(note_id in self.bonds, 'bond not found')
        bond = json.loads(self.bonds[note_id])
        if bond['status'] == 'pending_finality':
            gl.get_contract_at(gl.message.contract_address).emit(on='finalized').finalize_stake(note_id)
        elif bond['status'] == 'release_pending_finality':
            gl.get_contract_at(gl.message.contract_address).emit(on='finalized').finalize_release(note_id)
        elif bond['status'] in ('survived', 'overturned'):
            gl.get_contract_at(self.notes).emit(on='finalized').close_note(note_id)
        else:
            require(False, 'bond locked; wait for release time and resolve any appeal')

    @gl.public.write
    def resume_funding(self, funding_id: str) -> None:
        funding = json.loads(self.fundings[funding_id])
        require(funding['status'] in ('pending_finality', 'refund_pending_finality'), 'funding is not awaiting a callback')
        if funding['status'] == 'pending_finality':
            gl.get_contract_at(gl.message.contract_address).emit(on='finalized').finalize_funding(funding_id)
        else:
            gl.get_contract_at(gl.message.contract_address).emit(on='finalized').finalize_refund(funding_id)

    @gl.public.write
    def resume_claim(self, claim_id: str) -> None:
        claim = json.loads(self.claims[claim_id])
        require(claim['status'] in ('paid_pending_finality', 'failed_pending_finality'), 'verify pending credit first or claim already finalized')
        gl.get_contract_at(gl.message.contract_address).emit(on='finalized').finalize_claim(claim_id, claim['attempt'])

    @gl.public.view
    def get_funding(self, funding_id: str) -> str:
        require(funding_id in self.fundings, 'fund deposit directly in Bonds first')
        return self.fundings[funding_id]

    @gl.public.view
    def get_config(self) -> str:
        return packed({'appeal_window_seconds': int(self.appeal_window_seconds), 'release_delay_seconds': int(self.release_delay_seconds)})
