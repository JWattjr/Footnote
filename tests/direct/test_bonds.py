import base64
import json
from types import SimpleNamespace
import pytest
from conftest import to_hex
from test_notes import Remote, module, warp, NOTES, APPEALS, GEN

PARENT = '0x' + 'aa' * 32
CHILD = '0x' + 'bb' * 32

@pytest.fixture
def escrow(direct_vm, direct_deploy, direct_owner, direct_alice, direct_bob, monkeypatch):
    vm = direct_vm; vm._chain_id = 61999; warp(vm, 2000000000); vm.sender = direct_owner
    c = direct_deploy('contracts/bonds.py', NOTES); c.wire(APPEALS)
    writer, appellant = to_hex(direct_alice).lower(), to_hex(direct_bob).lower()
    writes, sends, receipts = [], [], {}
    appeal = {'id': 'water:1', 'note_id': 'water', 'appellant': appellant, 'deposit': str(2 * GEN),
              'writer': writer, 'status': 'finalized', 'outcome': 'OVERTURNED'}
    note = {'status': 'active', 'history': [{'reason': 'APPEAL', 'operation': 'water:1'}]}
    reads = {'get_appeal': lambda *args: json.dumps(appeal), 'get_note': lambda *args: json.dumps(note), 'has_open_appeal': False}
    import genlayer.gl as sdk
    monkeypatch.setattr(sdk, 'get_contract_at', lambda addr: Remote(reads, writes))
    m = module('bonds')
    class Target:
        def __init__(self, address): self.address = str(address).lower()
        def emit_transfer(self, **kwargs): sends.append({'to': self.address, 'value': int(kwargs['value'])})
    monkeypatch.setattr(m, 'Recipient', Target)
    monkeypatch.setattr(sdk.nondet.web, 'post', lambda url, **kwargs: SimpleNamespace(status=200,
        body=json.dumps({'result': receipts.get(json.loads(kwargs['body'])['params'][0])}).encode()))
    r = SimpleNamespace(vm=vm, c=c, m=m, alice=direct_alice, bob=direct_bob, writer=writer, appellant=appellant,
                        writes=writes, sends=sends, receipts=receipts, appeal=appeal, note=note)
    vm.sender = direct_alice; vm.value = 2 * GEN; c.stake('water'); vm.value = 0
    vm.sender = vm._contract_address; c.finalize_stake('water'); vm.deal(vm._contract_address, 2 * GEN)
    return r

def finalize(r, method, *args):
    r.vm.sender = r.vm._contract_address; getattr(r.c, method)(*args)

def deposit(r):
    r.vm.sender = bytes.fromhex(APPEALS[2:]); r.vm.value = 2 * GEN
    r.c.hold_deposit('water:1', 'water', r.appellant, 2 * GEN); r.vm.value = 0
    finalize(r, 'finalize_hold', 'water:1'); r.vm.deal(r.vm._contract_address, 4 * GEN)

def evidence(r, claim_id, wallet, credited, attempt=1, parent=PARENT, child=CHILD):
    from genlayer.py import calldata
    contract = to_hex(r.vm._contract_address).lower()
    amount = json.loads(r.c.get_claim(claim_id))['amount']
    r.receipts[parent] = {'hash': parent, 'status': 'FINALIZED', 'result': 6, 'from_address': wallet, 'to_address': contract,
        'consensus_data': {'leader_receipt': [{'execution_result': 'SUCCESS'}]}, 'triggered_transactions': [child],
        'data': {'calldata': base64.b64encode(calldata.encode({'method': 'withdraw', 'args': [claim_id, attempt]})).decode()}}
    r.receipts[child] = {'hash': child, 'status': 'FINALIZED', 'from_address': contract, 'to_address': wallet,
        'value': amount, 'type': 0, 'consensus_data': None, 'triggered_on': 'finalized', 'value_credited': credited}

@pytest.mark.parametrize('outcome', ['OVERTURNED', 'UPHELD', 'UNCERTAIN'])
def test_appeal_settlement_exact_allocations(escrow, outcome):
    r = escrow; r.appeal['outcome'] = outcome; deposit(r)
    r.vm.sender = r.bob; r.c.settle_appeal('water:1')
    with r.vm.expect_revert('self callback'): r.c.finalize_settlement('water:1')
    finalize(r, 'finalize_settlement', 'water:1')
    dep = json.loads(r.c.get_claim('deposit:water:1'))
    assert dep['recipient'] == (r.writer if outcome == 'UPHELD' else r.appellant) and dep['amount'] == str(2 * GEN)
    if outcome == 'OVERTURNED':
        bond = json.loads(r.c.get_claim('bond:water'))
        assert bond['recipient'] == r.appellant and bond['amount'] == str(2 * GEN)
        assert json.loads(r.c.get_reputation(r.writer))['overturned'] == 1
    assert r.sends == []
    with r.vm.expect_revert('already settled'): r.c.settle_appeal('water:1')

def release(r):
    r.vm.sender = r.alice; warp(r.vm, 2000000000 + 72 * 3600)
    r.c.release('water'); finalize(r, 'finalize_release', 'water')

def test_withdraw_only_after_window_and_verified_credit(escrow):
    r = escrow; r.vm.sender = r.alice
    with r.vm.expect_revert('window'): r.c.release('water')
    release(r)
    assert json.loads(r.c.get_reputation(r.writer)) == {'upheld': 1, 'overturned': 0}
    r.vm.sender = r.alice; r.c.withdraw('bond:water', 1)
    assert json.loads(r.c.get_claim('bond:water'))['status'] == 'pending'
    with r.vm.expect_revert('pending or paid'): r.c.withdraw('bond:water', 2)
    evidence(r, 'bond:water', r.writer, True)
    # Ledger delivery is independent of reservation.
    r.vm.deal(r.vm._contract_address, 0)
    assert r.c.verify_claim('bond:water', PARENT) == 'paid_pending_finality'
    with r.vm.expect_revert('self callback'): r.c.finalize_claim('bond:water', 1)
    finalize(r, 'finalize_claim', 'bond:water', 1)
    assert json.loads(r.c.get_totals()) == {'received': str(2 * GEN), 'paid': str(2 * GEN)}
    assert len(r.sends) == 1
    r.vm.sender = r.alice
    with r.vm.expect_revert('pending or paid'): r.c.withdraw('bond:water', 2)

def test_failed_credit_retry_only_after_confirmed_failure(escrow):
    r = escrow; release(r); r.vm.sender = r.alice; r.c.withdraw('bond:water', 1)
    evidence(r, 'bond:water', r.writer, False)
    assert r.c.verify_claim('bond:water', PARENT) == 'failed_pending_finality'
    with r.vm.expect_revert('pending or paid'): r.c.withdraw('bond:water', 2)
    finalize(r, 'finalize_claim', 'bond:water', 1)
    r.vm.sender = r.alice
    with r.vm.expect_revert('next withdrawal'): r.c.withdraw('bond:water', 1)
    r.c.withdraw('bond:water', 2)
    finalize(r, 'finalize_claim', 'bond:water', 1)
    assert json.loads(r.c.get_claim('bond:water'))['status'] == 'pending'
    r.vm.sender = r.alice
    with r.vm.expect_revert('attempt mismatch'): r.c.verify_claim('bond:water', PARENT)
    p2, c2 = '0x' + 'cc' * 32, '0x' + 'dd' * 32
    evidence(r, 'bond:water', r.writer, True, 2, p2, c2)
    r.c.verify_claim('bond:water', p2); finalize(r, 'finalize_claim', 'bond:water', 2)
    assert len(r.sends) == 2 and json.loads(r.c.get_totals())['paid'] == str(2 * GEN)

@pytest.mark.parametrize('change', ['recipient', 'amount', 'credit_unknown', 'unfinalized', 'unrelated_parent'])
def test_forged_receipts_do_not_unlock_claim(escrow, change):
    r = escrow; release(r); r.vm.sender = r.alice; r.c.withdraw('bond:water', 1)
    evidence(r, 'bond:water', r.writer, True)
    child = r.receipts[CHILD]
    if change == 'recipient': child['to_address'] = r.appellant
    if change == 'amount': child['value'] = '1'
    if change == 'credit_unknown': del child['value_credited']
    if change == 'unfinalized': child['status'] = 'ACCEPTED'
    if change == 'unrelated_parent': r.receipts[PARENT]['from_address'] = r.appellant
    with r.vm.expect_revert(): r.c.verify_claim('bond:water', PARENT)
    assert json.loads(r.c.get_claim('bond:water'))['status'] == 'pending'

def test_nonallowed_callers_and_unfinalized_overturn_rejected(escrow):
    r = escrow; r.vm.sender = r.alice; r.vm.value = 2 * GEN
    with r.vm.expect_revert('only Appeals'): r.c.hold_deposit('water:1', 'water', r.appellant, 2 * GEN)
    r.vm.value = 0; deposit(r); r.note['status'] = 'pending_finality'; r.vm.sender = r.alice
    with r.vm.expect_revert('label update'): r.c.settle_appeal('water:1')
