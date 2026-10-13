"""Exercise each public judging path and its independent validator callback."""
import json
from types import SimpleNamespace
import pytest
from conftest import to_hex
from test_notes import Remote, module, warp, NOTES, RECHECK, APPEALS, BONDS, URI, URL, TEXT
from test_flows import note


@pytest.fixture(params=['notes', 'recheck', 'appeals'])
def judging(request, direct_vm, direct_deploy, direct_owner, direct_alice, monkeypatch):
    vm = direct_vm
    vm._chain_id = 61999
    warp(vm, 2000000000)
    vm.sender = direct_owner
    name = request.param
    args = [json.dumps(['en.wikipedia.org'])] if name == 'notes' else [NOTES] if name == 'recheck' else [NOTES, BONDS]
    c = direct_deploy('contracts/' + name + '.py', *args)
    if name == 'notes':
        c.wire(RECHECK, APPEALS, BONDS)
    reads = {'get_note': json.dumps(note(to_hex(direct_alice).lower())),
             'get_config': json.dumps({'hosts': ['en.wikipedia.org'], 'appeals': APPEALS}),
             'get_bond': json.dumps({'writer': to_hex(direct_alice).lower(), 'status': 'locked', 'deadline': 2000259200}),
             'has_open_appeal': False, 'has_deposit': True,
             'get_deposit': json.dumps({'status': 'held'}),
             'get_funding': json.dumps({'status': 'funded', 'appellant': to_hex(direct_alice).lower(), 'amount': str(2*10**18)})}
    import genlayer.gl as sdk
    monkeypatch.setattr(sdk, 'get_contract_at', lambda address: Remote(reads, []))
    vm.sender = direct_alice
    return SimpleNamespace(vm=vm, c=c, m=module(name), name=name, alice=direct_alice)


def observe(r, page, quote):
    r.vm.clear_mocks()
    r.vm.mock_web('.*public.api.bsky.app.*', {'status': 200, 'body': json.dumps({'posts': [{'uri': URI, 'record': {'text': TEXT}}]})})
    r.vm.mock_web('.*en.wikipedia.org.*', {'status': 200, 'body': page})
    r.vm.mock_llm('FOOTNOTE_JUDGMENT.*', json.dumps({'evidence_label': 'SUPPORTED', 'tone_label': 'NOT_RAGE_BAIT',
        'IS_ALLEGATION_ABOUT_PERSON': 'no', 'PUBLIC_REPORT_EXPLICIT': 'no', 'citations': [{'url': URL, 'quote': quote}]}))
    r.vm.mock_llm('FOOTNOTE_APPEAL.*', json.dumps({'outcome': 'UPHELD'}))


@pytest.mark.parametrize('case', ['different_valid_quotes', 'missing_leader_quote', 'curly_quotes', 'dashes',
                                   'whitespace', 'edge_punctuation', 'changed_word', 'changed_case'])
def test_validator_consensus_and_grounding(judging, monkeypatch, case):
    r = judging
    first = 'Water freezes at zero degrees Celsius.'
    second = 'Ice forms at zero degrees Celsius.'
    page = first + ' ' + second
    leader_quote, own_quote, own_page, expected = first, second, page, True
    if case == 'missing_leader_quote':
        own_page, expected = second, False
    elif case == 'curly_quotes':
        leader_quote = 'Scientists say “water freezes” at zero degrees.'
        page = own_page = 'Scientists say "water freezes" at zero degrees. ' + second
    elif case == 'dashes':
        leader_quote = 'Water freezes—at zero degrees–and forms ice.'
        page = own_page = 'Water freezes-at zero degrees-and forms ice. ' + second
    elif case == 'whitespace':
        leader_quote = 'Water\u00a0 freezes\n at\t zero degrees Celsius.'
    elif case == 'edge_punctuation':
        leader_quote = '“Water freezes at zero degrees Celsius.”'
    elif case in ('changed_word', 'changed_case'):
        # Leader sees its quote, but the independently fetched validator page differs.
        own_page = page.replace('Water', 'water' if case == 'changed_case' else 'Mercury')
        expected = False
    observe(r, page, leader_quote)
    import genlayer.gl as sdk
    calls = []
    def run(leader, validator):
        result = leader()
        if isinstance(result, dict):
            assert result['citations'][0]['quote'] == leader_quote
            observe(r, own_page, own_quote)
            assert validator(sdk.vm.Return(result)) is expected
            calls.append(result)
        else:
            assert validator(sdk.vm.Return(result)) is True
        return result
    monkeypatch.setattr(sdk.vm, 'run_nondet_unsafe', run)
    if r.name == 'notes':
        r.c.create_note('water', URI, json.dumps([URL]))
        r.vm.sender = r.vm._contract_address
        r.c.finalize_note('water', 1)
        saved = json.loads(r.c.get_note('water'))['history'][0]['decision']
        assert saved['citations'][0]['quote'] == leader_quote
    elif r.name == 'recheck':
        op = r.c.recheck('water', '[]')
        assert json.loads(r.c.get_operation(op))['decision']['citations'][0]['quote'] == leader_quote
    else:
        appeal = r.c.contest('water', 1, '[]')
        r.vm.sender = r.vm._contract_address
        r.c.finalize_deposit(appeal)
        r.vm.sender = r.alice
        assert r.c.judge(appeal) == 'UPHELD'
        assert json.loads(r.c.get_appeal(appeal))['decision']['citations'][0]['quote'] == leader_quote
    assert len(calls) == 1


def test_url_set_comparison_still_requires_the_same_sources(judging):
    r = judging
    base = {'evidence_label': 'SUPPORTED', 'tone_label': 'NOT_RAGE_BAIT', 'IS_ALLEGATION_ABOUT_PERSON': 'no',
            'citations': [{'url': URL, 'quote': 'Water freezes at zero degrees.'}]}
    duplicate = {**base, 'citations': [{'url': URL, 'quote': 'A different valid sentence.'}, *base['citations']]}
    different = {**base, 'citations': [{'url': 'https://en.wikipedia.org/wiki/Ice', 'quote': 'Water freezes at zero degrees.'}]}
    assert r.m.compared(base) == r.m.compared(duplicate)
    assert r.m.compared(base) != r.m.compared(different)
