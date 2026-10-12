import json
from types import SimpleNamespace
import pytest
from conftest import to_hex
from test_notes import Remote, module, warp, NOTES, RECHECK, APPEALS, BONDS, URI, URL, QUOTE, TEXT, GEN

def decision(label='SUPPORTED'):
    import hashlib
    return {'evidence_label': label, 'tone_label': 'NOT_RAGE_BAIT', 'IS_ALLEGATION_ABOUT_PERSON': 'no',
            'citations': [{'url': URL, 'quote': QUOTE}] if label != 'UNSUPPORTED' else [],
            'source_digests': {URL: hashlib.sha256(QUOTE.encode()).hexdigest()}, 'post_available': True,
            'fingerprint': hashlib.sha256(TEXT.encode()).hexdigest()}

def note(writer):
    return {'id': 'water', 'writer': writer, 'post_uri': URI, 'fingerprint': decision()['fingerprint'], 'sources': [URL],
            'deadline': 2000000000 + 72 * 3600, 'status': 'active', 'version': 1,
            'history': [{'version': 1, 'reason': 'CREATED', 'operation': '', 'at': 2000000000, 'decision': decision()}]}

@pytest.fixture(params=['recheck', 'appeals'])
def flow(request, direct_vm, direct_deploy, direct_owner, direct_alice, monkeypatch):
    vm = direct_vm; vm._chain_id = 61999; warp(vm, 2000000000); vm.sender = direct_owner
    name, seconds = request.param if isinstance(request.param, tuple) else (request.param, 72*3600)
    args = [NOTES] if name == 'recheck' else [NOTES, BONDS, seconds, 300 if seconds == 300 else 24*3600]
    c = direct_deploy('contracts/' + name + '.py', *args)
    n = note(to_hex(direct_alice).lower()); writes = []
    n['deadline'] = 2000000000+seconds
    reads = {'get_note': lambda *args: json.dumps(n), 'get_config': json.dumps({'hosts': ['en.wikipedia.org', 'www.bbc.com'], 'appeals': APPEALS, 'appeal_window_seconds': seconds}),
             'get_deposit': json.dumps({'status': 'held'}), 'has_deposit': True, 'has_open_appeal': False,
             'get_funding': lambda *args: json.dumps({'status': 'funded', 'appellant': to_hex(direct_alice).lower(), 'amount': str(2*GEN)})}
    import genlayer.gl as sdk
    monkeypatch.setattr(sdk, 'get_contract_at', lambda address: Remote(reads, writes))
    vm.sender = direct_alice
    return SimpleNamespace(name=name, c=c, vm=vm, n=n, reads=reads, writes=writes, m=module(name), alice=direct_alice)

def mock(r, label='SUPPORTED', outcome='UPHELD', source=QUOTE):
    r.vm.clear_mocks()
    r.vm.mock_web('.*public.api.bsky.app.*', {'status': 200, 'body': json.dumps({'posts': [{'uri': URI, 'record': {'text': TEXT}}]})})
    r.vm.mock_web('.*en.wikipedia.org.*', {'status': 200, 'body': source})
    r.vm.mock_llm('FOOTNOTE_JUDGMENT.*', json.dumps({**decision(label), 'PUBLIC_REPORT_EXPLICIT': 'no'}))
    r.vm.mock_llm('FOOTNOTE_APPEAL.*', json.dumps({'outcome': outcome}))

def finalize(r, method, *args):
    r.vm.sender = r.vm._contract_address; getattr(r.c, method)(*args); r.vm.sender = r.alice

def test_recheck_updates_as_a_new_version_or_appeal_finalizes(flow):
    r = flow
    mock(r, 'CONTRADICTED', 'OVERTURNED')
    if r.name == 'recheck':
        op = r.c.recheck('water', '[]')
        assert not any(w[0] == 'apply_update' for w in r.writes)
        finalize(r, 'finalize_recheck', op)
        assert json.loads(r.c.get_operation(op))['outcome'] == 'UPDATED'
    else:
        op = r.c.contest('water', 1, '[]')
        finalize(r, 'finalize_deposit', op)
        assert r.c.judge(op) == 'OVERTURNED'
        assert not any(w[0] == 'apply_update' for w in r.writes)
        finalize(r, 'finalize_appeal', op)
    write = next(w for w in r.writes if w[0] == 'apply_update')
    assert write[1][1] == 1 and json.loads(write[1][2])['evidence_label'] == 'CONTRADICTED'

def test_two_uncertain_rechecks_then_pre_fetch_rejection(flow, monkeypatch):
    r = flow
    if r.name != 'recheck': pytest.skip('Recheck-only scenario')
    mock(r)
    for _ in range(2):
        op = r.c.recheck('water', '[]'); finalize(r, 'finalize_recheck', op)
        assert json.loads(r.c.get_operation(op))['outcome'] == 'UNCERTAIN'
    import genlayer.gl as sdk
    monkeypatch.setattr(sdk.nondet.web, 'get', lambda *args: pytest.fail('third recheck fetched'))
    with r.vm.expect_revert('two UNCERTAIN'): r.c.recheck('water', '[]')

@pytest.mark.parametrize('outcome', ['UPHELD', 'UNCERTAIN'])
def test_appeal_outcomes_duplicate_and_late(flow, outcome):
    r = flow
    if r.name != 'appeals': pytest.skip('Appeals-only scenario')
    mock(r, outcome=outcome)
    op = r.c.contest('water', 1, '[]')
    with r.vm.expect_revert('one appeal'): r.c.contest('water', 1, '[]')
    r.vm.value = 0; finalize(r, 'finalize_deposit', op)
    assert r.c.judge(op) == outcome
    with r.vm.expect_revert('self callback'): r.c.finalize_appeal(op)
    finalize(r, 'finalize_appeal', op)
    assert not any(w[0] == 'apply_update' for w in r.writes)
    r.n['version'] = 2
    warp(r.vm, r.n['deadline'])
    with r.vm.expect_revert('appeal window'): r.c.contest('water', 2, '[]')

def test_host_and_callback_rejections_pre_fetch(flow, monkeypatch):
    r = flow
    import genlayer.gl as sdk
    monkeypatch.setattr(sdk.nondet.web, 'get', lambda *args: pytest.fail('host check fetched'))
    if r.name == 'recheck':
        with r.vm.expect_revert('source host'): r.c.recheck('water', '["https://evil.test/a"]')
        with r.vm.expect_revert('self callback'): r.c.finalize_recheck('x')
    else:
        good = r.reads['get_funding']
        r.reads['get_funding'] = json.dumps({'status': 'funded', 'appellant': to_hex(r.alice).lower(), 'amount': str(GEN)})
        with r.vm.expect_revert('deposit'): r.c.contest('water', 1, '[]')
        r.reads['get_funding'] = good
        with r.vm.expect_revert('source host'): r.c.contest('water', 1, '["https://evil.test/a"]')
        with r.vm.expect_revert('self callback'): r.c.finalize_deposit('x')
        with r.vm.expect_revert('only Bonds'): r.c.mark_settled('x')

def test_changed_source_replay_is_actual_recheck_emission(flow):
    r = flow
    if r.name != 'recheck': pytest.skip('Recheck-only scenario')
    import hashlib
    from pathlib import Path
    claim = 'The fictional archive opens on Monday.'
    correction = 'Correction: the fictional archive is closed on Monday.'
    r.n['fingerprint'] = hashlib.sha256(claim.encode()).hexdigest()
    prior = r.n['history'][0]['decision']
    prior.update(fingerprint=r.n['fingerprint'], citations=[{'url': URL, 'quote': claim}],
                 source_digests={URL: hashlib.sha256(claim.encode()).hexdigest()})
    r.vm.clear_mocks()
    r.vm.mock_web('.*public.api.bsky.app.*', {'status': 200, 'body': json.dumps({'posts': [{'uri': URI, 'record': {'text': claim}}]})})
    r.vm.mock_web('.*en.wikipedia.org.*', {'status': 200, 'body': correction})
    r.vm.mock_llm('FOOTNOTE_JUDGMENT.*', json.dumps({'evidence_label':'CONTRADICTED','tone_label':'NOT_RAGE_BAIT',
        'IS_ALLEGATION_ABOUT_PERSON':'no','citations':[{'url':URL,'quote':correction}]}))
    op = r.c.recheck('water', '[]'); finalize(r, 'finalize_recheck', op)
    write = next(w for w in r.writes if w[0] == 'apply_update')
    result = json.loads(write[1][2])
    assert result['source_digests'][URL] != prior['source_digests'][URL]
    assert result['evidence_label'] == 'CONTRADICTED'
    path = Path('public/recheck-test.json')
    path.write_text(json.dumps({'scope':'test-only; direct VM, mocked source and post, stubbed cross-contract calls',
        'claim':claim,'sourceUrl':URL,'sourceUrlIsMocked':True,'before':prior,'after':result,
        'operation':json.loads(r.c.get_operation(op)),'emittedMethod':write[0],'expectedVersion':write[1][1]},indent=2),encoding='utf-8')
