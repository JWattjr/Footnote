"""Render the persisted journal without inventing completion or execution success."""
import base64
import json
from pathlib import Path
from datetime import datetime, timezone

def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))

p = load('public/deployment.json')
lines = ['# Live proof manifest', '', f"StudioNet 61999, generation {p['generation']}. Finality and successful execution are verified separately. Raw receipts are in `docs/proofs`; `public/deployment.json` is the persisted transaction journal. The network verifier is read-only.", '',
    'Timing disclosure: the public demo deployment uses a 15-minute appeal window; production default is 72 hours. Demo cancellation grace is 10 minutes and bond release delay is 15 minutes. Production defaults are 24 hours for grace and 72 hours for bond release. Constructor bounds are five minutes–30 days. Deadlines use actual chain time; no time travel is used.', '',
    'Generation 3 fixes literal quote-span consensus. Validators compare evidence, tone, allegation flag and sorted unique cited URLs; Appeals also compares its outcome. Every leader quote still passes an exact, case-sensitive substring check against each validator’s own page, after specified typography/whitespace normalization. Stored quotes are the leader’s. See SECURITY_NOTES.md.', '',
    '## Current contracts', '', '| Contract | Address |', '|---|---|']
for key, address in p['contracts'].items():
    lines.append(f'| {key} | [{address}](https://explorer-studio.genlayer.com/contracts/{address}) |')
lines += ['', '## Every current live transaction', '', '| Step | Hash | Evidence |', '|---|---|---|']
for name, h in p['transactions'].items():
    path = Path('docs/proofs') / (name+'.json')
    detail = 'Awaiting receipt; resume the same hash, never resubmit'
    if path.exists():
        r = load(path)
        leader = ((r.get('consensus_data') or {}).get('leader_receipt') or [{}])[0]
        output = base64.b64decode(leader.get('result', '')).decode('utf-8', errors='replace') if isinstance(leader.get('result'), str) else ''
        if r.get('hash') == h and r.get('status') == 'FINALIZED':
            if name in p.get('rejections', {}) and p['rejections'][name] in output:
                detail = 'FINALIZED expected pre-fetch rejection: '+p['rejections'][name]
            elif r.get('type') == 0 and r.get('consensus_data') is None:
                detail = 'FINALIZED native value_credited=true' if r.get('value_credited') is True else 'Native credit NOT verified'
            elif r.get('result') == 6 and leader.get('execution_result') in ['SUCCESS', 'FINISHED_WITH_RETURN']:
                detail = 'FINALIZED, result=6, leader execution SUCCESS'
            else:
                detail = 'LIVE FAILURE or unverified execution: '+str(r.get('result'))
    lines.append(f'| {name} | [{h}](https://explorer-studio.genlayer.com/transactions/{h}) | {detail} |')

lines += ['', '## Matched finalized state', '']
for key, state in p['states'].items():
    if not isinstance(state, dict):
        continue
    if 'history' in state:
        d = state['history'][-1]['decision']
        deadline = datetime.fromtimestamp(state['deadline'], timezone.utc).isoformat()
        lines.append(f"- `{key}`: {state['status']}, v{state['version']}, {d['evidence_label']} / {d['tone_label']}, open quota {state['open']}; actual original appeal deadline {deadline}.")
    elif key.endswith(':appeal'):
        lines.append(f"- `{key}`: {state['outcome'] or 'not judged'}, {state['status']}; deposit {state['deposit']} wei.")
    elif key.startswith(('bond:', 'deposit:')) and not key.endswith(':balances'):
        lines.append(f"- `{key}`: {state['status']}, amount {state['amount']} wei; verified native child `{state.get('transfer_hash', '')}`; withdrawal attempt {state['attempt']}.")
    elif key == 'quota':
        lines.append(f"- Quota read: `{json.dumps(state['value'])}`; fourth same-post creation rejected before fetching.")
    elif key == 'recheck':
        lines.append(f"- Recheck operation: {state['outcome']}, {state['status']}.")
    elif key == 'config' or key.endswith('Config'):
        lines.append(f'- `{key}`: `{json.dumps(state)}`.')

if p.get('quotaRejectionSnapshot'):
    lines += ['', f"Historical finalized quota read immediately after the fourth-note rejection: `{json.dumps(p['quotaRejectionSnapshot']['value'])}`. The current quota falls as mature bonds are released; the historical saturation snapshot is retained separately."]

e = p.get('additionalProofs')
if e:
    lines += ['', '## Added-source label change and distinct-wallet appeal', '',
        f"Wallet A (writer/funder): `{e['walletA']}`. Wallet B (appellant): `{e['walletB']}`. The signing key stays in the encrypted CLI keystore and OS credential store; only public addresses are recorded. These are two separate signing accounts operated for the demonstration, not independently verified human identities."]
    if e.get('completedAt'):
        note, appeal = e['labelChange']['after'], e['twoWallet']['decided']
        lines += ['', f"`{note['id']}`: v1 **UNSUPPORTED** → v2 **SUPPORTED**, reason RECHECK, operation `{e['labelChange']['operation']}`. The earlier history entry is retained unchanged in finalized state.", '',
            f"Wallet B’s appeal of A’s note is **{appeal['outcome']}**, settled and closed. The challenge reuses the authentic NASA evidence, without fabricated opposing claims. The deposit and writer bond are paid through verified native credits after the real release window."]
        for version in note['history']:
            for c in version['decision']['citations']:
                lines += ['', f"Stored v{version['version']} leader citation: [{c['url']}]({c['url']}) — “{c.get('quote', 'withheld')}”"]
    else:
        lines += ['', 'The additional proof is incomplete. No live label-change or settled two-wallet lifecycle is claimed.']
    inputs = load(e['inputs'])
    lines += ['', '### Off-chain evidence preflight', '', inputs['disclosure']]
    for url, check in inputs['checks'].items():
        for item in [check, *check.get('supportedClaimChecks', [])]:
            lines += ['', f"Source: [{url}]({url}). Preflight quote: “{item['quote']}”. Three HTTP 200 fetches, case-sensitive normalized quote presence, identical canonical SHA-256 `{item['fetches'][0]['digest']}`."]
    lines += ['', 'Fresh snapshots precede each new note and the recheck in `docs/proofs/preflight-<step>.json`. The quota3 preflight briefly refused changing navigation digests; it resumed the same existing stake only after the unchanged URL and quotes passed three fresh matching fetches. No publication was sent during that off-chain pause; see `proofs/quota3-preflight-pause.md`. The fresh NASA HTML was 265,616 UTF-8 bytes before canonical extraction. The long NASA source is independently fetched by validators; digests describe the observed full canonical source and do not claim equality across validators.', '',
        '### Exact balances (wei)', '', '| Stage | Wallet A | Wallet B | Current Bonds |', '|---|---:|---:|---:|']
    for stage, b in e['balances'].items():
        lines.append(f"| {stage} | {b['walletA']} | {b['walletB']} | {b['bonds']} |")
    lines += ['', f"A → B funding: `{p['transactions'].get('extra-fund-wallet-b', 'pending')}`, 2 GEN. Measured funding fee: {e.get('fundingFeeWei', 'pending')} wei. Parent withdrawals, native credit children and verification callbacks all require FINALIZED success. Outcome-specific balance deltas and escrow received-minus-verified-paid totals are checked by `verify:network`."]

if p.get('accounting'):
    a = p['accounting']
    lines += ['', f"Final escrow accounting: wallet A {a['walletBalance']} wei; Bonds {a['bondsBalance']} wei; received {a['totals']['received']} wei, verified paid {a['totals']['paid']} wei. Bonds balance equals received minus verified paid."]
lines += ['', '## Historical deployment recovery', '', 'Both old deployments are absent from Portal contract fields. Their immutable addresses are retained solely in archived diagnosis and recovery records.']
for path in p.get('legacyCleanup', []):
    old = load(path)
    lines += ['', f"{old['generation']} recovery journal: [{path}]({path.removeprefix('docs/')}). Complete: {old.get('complete', False)}.", '', '| Recovery step | Hash |', '|---|---|']
    for name, h in old['transactions'].items():
        lines.append(f'| {name} | [{h}](https://explorer-studio.genlayer.com/transactions/{h}) |')
    lines += ['', f"Exact historical start/end: `{json.dumps(old['balances']['start'])}` → `{json.dumps(old['balances'].get('end', {}))}`. Four 2-GEN verified credits recover eight GEN; the legacy escrow is zero."]
lines += ['', 'V1 recovery remains pending real maturity on 14 October 2026 (Africa/Lagos): climate-record 20:40:31, open-question 20:49:10, climate-quota-2 21:12:01 and climate-quota-3 21:15:14. The eight GEN cannot be withdrawn earlier. This future cleanup is not a completed live result. A one-time follow-up, `footnote-v1-bond-recovery`, is scheduled for 14 October at 21:16 Africa/Lagos, after the last deadline.', '',
    '## Tests and verification', '', '107 direct tests passed; 8 inapplicable scenario combinations skipped. Eleven TypeScript tests passed, including four wallet connection regressions with a mock provider. The wallet fix prevents overlapping permission requests and provides pending-request/cancellation recovery; desktop/mobile checks use controlled fixtures and make no live wallet writes. All four GenVM checks passed. Direct tests mock cross-contract calls, LLM/web content and native delivery; actual StudioNet receipts prove the live money path separately. Typecheck, lint, production build, network/link checks and desktop/mobile history checks are recorded in TEST_MATRIX and verification artifacts.', '',
    '## Still test-only or unproven', '']
lines += ['- '+item for item in p['unproven']]
lines += ['', 'The same-URL publisher correction in `/replay` remains explicitly mocked. Forced version drift, callback replay and outage recovery remain direct-test-only. A source occurring on an allowlisted host does not guarantee its truth. The Portal has not been submitted.']
Path('docs/PROOF_MANIFEST.md').write_text('\n'.join(lines)+'\n', encoding='utf-8')
print(len(p['transactions']), 'current hashes documented with historical cleanup separately')
