"""Record completed verified recovery without changing the historical v3 proof."""
import json
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

manifest = Path('public/deployment.json')
p = json.loads(manifest.read_text(encoding='utf-8'))
path = 'docs/legacy/v1/cleanup/journal.json'
recovery = json.loads(Path(path).read_text(encoding='utf-8'))
activity_path = 'docs/legacy/v1/cleanup/wallet-activity-before-recovery.json'
activity = json.loads(Path(activity_path).read_text(encoding='utf-8'))
preflight = json.loads(Path('docs/legacy/v1/cleanup/preflight.json').read_text(encoding='utf-8'))
historical = deepcopy(p['additionalProofs'])
wallet = historical['walletA']
assert recovery['complete'] is True and not recovery.get('failure')
ids = ['climate-record', 'open-question', 'climate-quota-2', 'climate-quota-3']
credits = 0
for note_id in ids:
    claim = recovery['states']['bond:'+note_id]
    assert claim['status'] == 'paid' and claim['recipient'] == wallet
    assert int(claim['amount']) == 2*10**18
    assert claim['transfer_hash'] in recovery['transactions'].values()
    credits += int(claim['amount'])
assert credits == 8*10**18
assert int(recovery['balances']['end']['bonds']) == 0
assert int(recovery['balances']['start']['bonds']) == credits
assert int(recovery['balances']['end']['wallet'])-int(recovery['balances']['start']['wallet']) == credits
outflow = sum(int(row['value']) for row in activity['rows'])
assert str(outflow) == activity['netOutflowWei']
assert int(historical['balances']['finish']['walletA'])-outflow == int(recovery['balances']['start']['wallet'])
p.setdefault('legacyCleanup', [])
if path not in p['legacyCleanup']:
    p['legacyCleanup'].append(path)
p.setdefault('historicalEscrowAccounting', deepcopy(p['accounting']))
p['postProofAccounting'] = {
    'checkedAt': datetime.now(timezone.utc).isoformat(),
    'historicalFinish': historical['balances']['finish'],
    'externalActivity': {'path': activity_path, 'netOutflowWei': str(outflow), 'before': preflight['checkedAt']},
    'recoveries': [path], 'verifiedRecoveryCreditsWei': str(credits),
    'current': {'walletA': recovery['balances']['end']['wallet'],
                'walletB': historical['balances']['finish']['walletB'],
                'bonds': historical['balances']['finish']['bonds']},
}
p['accounting']['walletBalance'] = recovery['balances']['end']['wallet']
assert p['additionalProofs'] == historical
manifest.write_text(json.dumps(p, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
readme = Path('README.md')
text = readme.read_text(encoding='utf-8')
text = text.replace('The previous immutable deployment and its held writer bonds remain separately archived in `docs/legacy/v1`; the app now targets generation 3.', 'The previous immutable deployment is archived in `docs/legacy/v1`; all four original writer bonds were released after their real deadlines and eight GEN were recovered through verified native credits. Its Bonds escrow is zero. The app targets generation 3.')
readme.write_text(text, encoding='utf-8')
security = Path('docs/SECURITY_NOTES.md')
text = security.read_text(encoding='utf-8')
text = text.replace('Its original eight simulated GEN of writer bonds remain in the old Bonds contract under the original 72-hour deadlines on 14 October; redeployment does not migrate those funds.', 'Its original four writer bonds were released after the actual 72-hour deadlines on 14 October, with eight simulated GEN returned through finalized, verified native credits. The legacy Bonds balance is zero; redeployment did not migrate the funds.')
text = text.replace('Its existing bonds still have their ordinary mature-release path if no appeal is open; see the archived exact addresses and state in `docs/legacy/v1/deployment.json`.', 'Finalized preflight confirmed no open appeals before the normal release path was used. Exact addresses, every recovery receipt, paid claims and balance deltas are archived in `docs/legacy/v1/cleanup/journal.json`. The v3 historical proof balances remain unchanged; seven later credited outflows outside Footnote (0.019 GEN) and these eight GEN of refunds are reconciled separately by the network verifier.')
security.write_text(text, encoding='utf-8')
print('Recorded four verified v1 refunds; preserved the complete historical v3 proof.')
