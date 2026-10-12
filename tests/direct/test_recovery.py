import json
import pytest
from conftest import to_hex
from test_notes import warp, NOTES, RECHECK, APPEALS, BONDS, GEN, setup, mocks, create, Remote
from test_flows import flow, finalize as appeal_finalize
from test_bonds import escrow, deposit, finalize, release, evidence, PARENT, CHILD

def open_appeal(r):
    op = r.c.contest('water', 1, '[]')
    appeal_finalize(r, 'finalize_deposit', op)
    return op

def test_open_appeal_recheck_guard_before_fetch(flow, monkeypatch):
    r = flow
    if r.name != 'recheck': pytest.skip('Recheck-only scenario')
    r.reads['has_open_appeal'] = True
    import genlayer.gl as sdk
    monkeypatch.setattr(sdk.nondet.web, 'get', lambda *a: pytest.fail('open appeal fetched'))
    with r.vm.expect_revert('[EXPECTED] note has an open appeal; recheck after it is decided'):
        r.c.recheck('water', '[]')

def test_notes_rechecks_cannot_race_an_open_appeal(setup, monkeypatch):
    r = setup; mocks(r); note = create(r)
    import genlayer.gl as sdk
    reads = {'has_open_appeal': True}
    monkeypatch.setattr(sdk, 'get_contract_at', lambda a: Remote(reads, r.writes))
    update = {**note['history'][0]['decision'], 'sources': note['sources']}
    r.vm.sender = bytes.fromhex(RECHECK[2:])
    with r.vm.expect_revert('note has an open appeal'): r.c.apply_update('water', 1, json.dumps(update), 'RECHECK', 'recheck-1')
    reads['has_open_appeal'] = False
    r.c.apply_update('water', 1, json.dumps(update), 'RECHECK', 'recheck-1')
    reads['has_open_appeal'] = True
    r.vm.sender = r.alice; r.c.resume_note('water')
    assert r.writes[-1][0] == 'finalize_note'
    r.vm.sender = r.vm._contract_address; r.c.finalize_note('water', 2)
    actual = json.loads(r.c.get_note('water'))
    assert actual['version'] == 1 and actual['status'] == 'active' and len(actual['history']) == 1

@pytest.mark.parametrize('condition', ['version', 'timeout'])
def test_cancel_stale_closes_once_and_rejects_replays(flow, condition, monkeypatch):
    r = flow
    if r.name != 'appeals': pytest.skip('Appeals-only scenario')
    op = open_appeal(r)
    with r.vm.expect_revert('version matches'): r.c.cancel_stale(op)
    if condition == 'version': r.n['version'] = 2
    else:
        warp(r.vm, r.n['deadline'] + 24*3600 - 1)
        with r.vm.expect_revert('version matches'): r.c.cancel_stale(op)
        warp(r.vm, r.n['deadline'] + 24*3600)
    r.c.cancel_stale(op)
    assert r.c.has_open_appeal('water')
    with r.vm.expect_revert('self callback'): r.c.finalize_cancel(op)
    appeal_finalize(r, 'finalize_cancel', op)
    assert json.loads(r.c.get_appeal(op))['cancel_reason'] == ('STALE_VERSION' if condition == 'version' else 'JUDGING_TIMEOUT')
    with r.vm.expect_revert('already applied'): appeal_finalize(r, 'finalize_cancel', op)
    r.reads['get_deposit'] = json.dumps({'status': 'settled'})
    r.vm.sender = bytes.fromhex(BONDS[2:]); r.c.mark_settled(op); r.vm.sender = r.alice
    assert json.loads(r.c.get_appeal(op))['status'] == 'CANCELLED'
    assert not r.c.has_open_appeal('water')
    with r.vm.expect_revert('already cancelled'): r.c.cancel_stale(op)
    with r.vm.expect_revert('already decided'): r.c.judge(op)
    r.vm.sender = bytes.fromhex(BONDS[2:])
    with r.vm.expect_revert('already closed'): r.c.mark_settled(op)

def test_cancel_recovers_missing_activation(flow):
    r = flow
    if r.name != 'appeals': pytest.skip('Appeals-only scenario')
    op = open_appeal(r); r.reads['has_deposit'] = False; r.n['version'] = 2
    r.c.cancel_stale(op); appeal_finalize(r, 'finalize_cancel', op)
    assert r.writes[-1][0] == 'activate_deposit'
    r.c.resume_appeal(op)
    assert r.writes[-1][0] == 'activate_deposit'
    r.reads['has_deposit'] = True; r.reads['get_deposit'] = json.dumps({'status': 'pending_finality'})
    r.c.resume_appeal(op)
    assert r.writes[-1][0] == 'resume_deposit'

def test_cancel_exact_recipient_balances_and_writer_release(escrow):
    r = escrow; r.appeal.update(status='cancelled_pending_settlement', outcome='CANCELLED')
    deposit(r); r.vm.sender = r.bob; r.c.settle_appeal('water:1'); finalize(r, 'finalize_settlement', 'water:1')
    with r.vm.expect_revert('already applied'): finalize(r, 'finalize_settlement', 'water:1')
    r.reads['has_open_appeal'] = True; r.vm.sender = r.alice; warp(r.vm, r.note['deadline'])
    with r.vm.expect_revert('outstanding appeal'): r.c.release('water')
    r.reads['has_open_appeal'] = False; release(r)
    r.vm.deal(r.bob, 0); r.vm.deal(r.alice, 0)
    for index, (claim, recipient, wallet) in enumerate([('deposit:water:1', r.bob, r.appellant), ('bond:water', r.alice, r.writer)]):
        r.vm.sender = recipient; r.c.withdraw(claim, 1)
        parent = '0x' + ('aa' if index == 0 else 'cc')*32
        child = '0x' + ('bb' if index == 0 else 'dd')*32
        evidence(r, claim, wallet, True, parent=parent, child=child)
        # Direct VM mocks emitted native delivery; model the independently verified ledger credit.
        delivery = r.sends[-1]
        assert delivery['to'] == wallet
        r.vm.deal(recipient, r.vm._balances.get(recipient, 0) + delivery['value'])
        r.vm.deal(r.vm._contract_address, r.vm._balances[r.vm._contract_address] - delivery['value'])
        r.c.verify_claim(claim, parent); finalize(r, 'finalize_claim', claim, 1)
        r.vm.sender = recipient
        with r.vm.expect_revert('pending or paid'): r.c.withdraw(claim, 2)
    assert r.vm._balances[r.bob] == 2*GEN and r.vm._balances[r.alice] == 2*GEN
    assert r.vm._balances[r.vm._contract_address] == 0
    assert json.loads(r.c.get_totals()) == {'received': str(4*GEN), 'paid': str(4*GEN)}
    assert len(r.sends) == 2

def test_unopened_funding_refund_and_callback_recovery(escrow):
    r = escrow; r.vm.sender = r.bob; r.vm.value = 2*GEN
    funding = r.c.fund_appeal('water', 1); r.vm.value = 0
    r.c.resume_funding(funding); assert r.writes[-1][0] == 'finalize_funding'
    finalize(r, 'finalize_funding', funding); r.vm.sender = r.bob
    r.c.refund_unopened(funding); r.c.resume_funding(funding)
    assert r.writes[-1][0] == 'finalize_refund'
    finalize(r, 'finalize_refund', funding)
    claim = json.loads(r.c.get_claim('funding:'+funding))
    assert claim['recipient'] == r.appellant and claim['amount'] == str(2*GEN)
    with r.vm.expect_revert('already applied'): finalize(r, 'finalize_refund', funding)
    with r.vm.expect_revert('already consumed'): r.c.refund_unopened(funding)

def test_reserved_funding_cannot_be_refunded(escrow):
    r = escrow; r.vm.sender = r.bob; r.vm.value = 2*GEN
    funding = r.c.fund_appeal('water', 1); r.vm.value = 0; finalize(r, 'finalize_funding', funding)
    r.reads['has_appeal'] = True; r.vm.sender = r.bob
    with r.vm.expect_revert('belongs to an appeal'): r.c.refund_unopened(funding)

def test_refunded_funding_opening_race_cancels_without_second_refund(escrow):
    r = escrow; r.vm.sender = r.bob; r.vm.value = 2*GEN
    funding = r.c.fund_appeal('water', 1); r.vm.value = 0; finalize(r, 'finalize_funding', funding)
    r.vm.sender = r.bob; r.c.refund_unopened(funding); finalize(r, 'finalize_refund', funding)
    r.appeal.update(status='open', outcome='')
    r.vm.sender = bytes.fromhex(APPEALS[2:])
    with r.vm.expect_revert('funding was refunded'): r.c.activate_deposit('water:1')
    r.appeal.update(status='cancelled_pending_settlement', outcome='CANCELLED')
    r.c.activate_deposit('water:1')
    record = json.loads(r.c.get_deposit('water:1'))
    assert record['status'] == 'settled' and record['refund_claim'] == 'funding:'+funding
    assert r.writes[-1][0] == 'mark_settled'
    with r.vm.expect_revert('claim not found'): r.c.get_claim('deposit:water:1')
    assert json.loads(r.c.get_claim('funding:'+funding))['amount'] == str(2*GEN)

def test_cancellation_can_activate_previously_missing_deposit(escrow):
    r = escrow; r.vm.sender = r.bob; r.vm.value = 2*GEN
    funding = r.c.fund_appeal('water', 1); r.vm.value = 0; finalize(r, 'finalize_funding', funding)
    r.appeal.update(status='cancelled_pending_settlement', outcome='CANCELLED')
    r.vm.sender = bytes.fromhex(APPEALS[2:]); r.c.activate_deposit('water:1')
    finalize(r, 'finalize_hold', 'water:1'); r.vm.sender = r.bob
    r.c.settle_appeal('water:1'); finalize(r, 'finalize_settlement', 'water:1')
    assert json.loads(r.c.get_claim('deposit:water:1'))['recipient'] == r.appellant

@pytest.mark.parametrize('flow', [('appeals', 300)], indirect=True)
def test_minimum_appeal_and_cancel_grace_use_real_contract_boundary(flow):
    r = flow; op = open_appeal(r)
    assert json.loads(r.c.get_appeal(op))['deadline'] == 2000000300
    warp(r.vm, 2000000599)
    with r.vm.expect_revert('version matches'): r.c.cancel_stale(op)
    warp(r.vm, 2000000600); r.c.cancel_stale(op)
    assert json.loads(r.c.get_appeal(op))['status'] == 'cancel_pending_finality'

@pytest.mark.parametrize('escrow', [300], indirect=True)
def test_minimum_bond_release_delay(escrow):
    r = escrow; r.vm.sender = r.alice; warp(r.vm, 2000000299)
    with r.vm.expect_revert('window'): r.c.release('water')
    warp(r.vm, 2000000300); r.c.release('water')
    finalize(r, 'finalize_release', 'water')
    assert json.loads(r.c.get_claim('bond:water'))['recipient'] == r.writer

def test_stalled_settlement_and_close_can_resume(escrow):
    r = escrow; r.appeal['outcome'] = 'CANCELLED'; deposit(r)
    r.vm.sender = r.bob; r.c.settle_appeal('water:1'); r.c.resume_deposit('water:1')
    assert r.writes[-1][0] == 'finalize_settlement'
    finalize(r, 'finalize_settlement', 'water:1'); r.vm.sender = r.bob
    r.c.resume_deposit('water:1'); assert r.writes[-1][0] == 'mark_settled'
    r.appeal['status'] = 'CANCELLED'; count = len(r.writes); r.c.resume_deposit('water:1')
    assert len(r.writes) == count

def test_stalled_release_and_verified_credit_callbacks_can_resume(escrow):
    r = escrow; r.vm.sender = r.alice; warp(r.vm, r.note['deadline'])
    r.c.release('water'); r.c.resume_bond('water'); assert r.writes[-1][0] == 'finalize_release'
    finalize(r, 'finalize_release', 'water'); r.vm.sender = r.alice
    r.c.resume_bond('water'); assert r.writes[-1][0] == 'close_note'
    r.c.withdraw('bond:water', 1); evidence(r, 'bond:water', r.writer, True)
    r.c.verify_claim('bond:water', PARENT); r.c.resume_claim('bond:water')
    assert r.writes[-1][0] == 'finalize_claim'
    finalize(r, 'finalize_claim', 'bond:water', 1); finalize(r, 'finalize_claim', 'bond:water', 1)
    assert json.loads(r.c.get_totals())['paid'] == str(2*GEN)

@pytest.mark.parametrize('contract', ['notes', 'bonds', 'appeals'])
@pytest.mark.parametrize('seconds', [None, 300, 30*86400, 299, 30*86400+1])
def test_timing_constructor_bounds(contract, seconds, direct_vm, direct_deploy, direct_owner):
    vm = direct_vm; vm._chain_id = 61999; vm.sender = direct_owner; warp(vm, 2000000000)
    args = {'notes': ['["en.wikipedia.org"]'], 'bonds': [NOTES], 'appeals': [NOTES, BONDS]}[contract]
    if seconds is not None: args += [seconds] if contract == 'notes' else [seconds, seconds]
    if seconds is not None and (seconds < 300 or seconds > 30*86400):
        with vm.expect_revert('between 5 minutes and 30 days'): direct_deploy('contracts/'+contract+'.py', *args)
    else:
        c = direct_deploy('contracts/'+contract+'.py', *args)
        config = json.loads(c.get_config())
        assert config['appeal_window_seconds'] == (72*3600 if seconds is None else seconds)
        if contract == 'appeals': assert config['cancel_grace_seconds'] == (24*3600 if seconds is None else seconds)
        if contract == 'bonds': assert config['release_delay_seconds'] == (72*3600 if seconds is None else seconds)

@pytest.mark.parametrize('contract,args', [('appeals',[NOTES,BONDS,300,299]), ('appeals',[NOTES,BONDS,300,30*86400+1]), ('bonds',[NOTES,300,299]), ('bonds',[NOTES,300,30*86400+1]), ('bonds',[NOTES,900,300])])
def test_independent_grace_and_release_bounds(contract, args, direct_vm, direct_deploy, direct_owner):
    direct_vm._chain_id = 61999; direct_vm.sender = direct_owner
    with direct_vm.expect_revert(): direct_deploy('contracts/'+contract+'.py', *args)
