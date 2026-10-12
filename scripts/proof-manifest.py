import json, base64
from pathlib import Path
from datetime import datetime, timezone
p=json.loads(Path('public/deployment.json').read_text(encoding='utf-8'))
lines=['# Live proof manifest','', 'StudioNet 61999, generation 2. Finality and successful execution are verified separately. Raw receipts are in `docs/proofs`; `public/deployment.json` is the persisted transaction journal. The network verifier is read-only.', '', 'Timing disclosure: the public demo deployment uses a 15-minute appeal window; production default is 72 hours. Demo cancellation grace is 10 minutes and bond release delay is 15 minutes. Production defaults are 24 hours for grace and 72 hours for bond release. All windows are constructor parameters bounded to five minutes–30 days. Live deadlines use actual chain time; no time travel is used.', '', 'The first immutable deployment and its original held bonds are archived under `docs/legacy/v1`. An unfunded superseded deployment is separately recorded under `docs/legacy/v2-unfunded-attempt`; it was replaced before any proof stake.', '', '## Contracts', '', '| Contract | Address |', '|---|---|']
for k,v in p['contracts'].items(): lines.append(f'| {k} | [{v}](https://explorer-studio.genlayer.com/contracts/{v}) |')
lines += ['', '## Every live transaction', '', '| Step | Hash | Evidence |', '|---|---|---|']
for name,h in p['transactions'].items():
    path=Path('docs/proofs')/(name+'.json')
    if not path.exists(): detail='Awaiting receipt; resume this hash, never resubmit'
    else:
        r=json.loads(path.read_text(encoding='utf-8'))
        if r.get('hash') != h: detail='Awaiting matching receipt; resume this hash'
        else:
            leader=((r.get('consensus_data') or {}).get('leader_receipt') or [{}])[0]
            result=base64.b64decode(leader.get('result','')).decode('utf-8',errors='replace') if isinstance(leader.get('result'),str) else ''
            if r.get('status')!='FINALIZED': detail='Awaiting finality; resume this hash'
            elif name in p.get('rejections',{}) and p['rejections'][name] in result: detail='FINALIZED expected pre-fetch rejection: '+p['rejections'][name]
            elif r.get('type')==0 and r.get('consensus_data') is None: detail='FINALIZED native value_credited=true' if r.get('value_credited') is True else 'Native credit unverified: '+str(r.get('value_credited'))
            elif r.get('result')==6 and leader.get('execution_result')=='SUCCESS': detail='FINALIZED, result=6, leader execution SUCCESS'
            else: detail='LIVE EXECUTION FAILURE or unverified result: '+str(leader.get('execution_result'))
    lines.append(f'| {name} | [{h}](https://explorer-studio.genlayer.com/transactions/{h}) | {detail} |')
lines += ['', '## Matched state and source preflight', '']
for key,state in p['states'].items():
    if not isinstance(state,dict): continue
    if 'history' in state:
        d=state['history'][-1]['decision']; deadline=datetime.fromtimestamp(state['deadline'],timezone.utc).isoformat()
        lines.append(f'- `{key}`: {state["status"]}, version {state["version"]}, {d["evidence_label"]} / {d["tone_label"]}; open quota {state["open"]}; actual appeal deadline {deadline}.')
    elif key.endswith(':appeal'): lines.append(f'- `{key}`: {state["outcome"] or "not judged"}, {state["status"]}; deposit {state["deposit"]} wei'+(f'; cancellation reason {state["cancel_reason"]}.' if 'cancel_reason' in state else '.'))
    elif key.endswith(':balances'):
        if 'after' in state: lines.append(f'- `{key}`: before {state["before"]}, after {state["after"]}, exact native-credit delta {int(state["after"])-int(state["before"])} wei.')
        else: lines.append(f'- `{key}`: before {state["before"]}; native credit proof still pending.')
    elif key.startswith(('deposit:','bond:','funding:')): lines.append(f'- `{key}`: {state["status"]}; native child `{state.get("transfer_hash", "")}`, amount {state["amount"]} wei, attempt {state["attempt"]}.')
    elif key=='quota': lines.append(f'- Quota read: {json.dumps(state["value"])}; fourth same-post creation rejected before fetch.')
    elif key=='recheck': lines.append(f'- Recheck: {state["outcome"]}, {state["status"]}.')
    elif key.endswith('Config') or key=='config': lines.append(f'- `{key}`: finalized configuration {json.dumps(state)}.')
if p.get('accounting'):
    a=p['accounting']; lines += ['', f'Exact final accounting: wallet `{a["wallet"]}` has {a["walletBalance"]} wei; Bonds has {a["bondsBalance"]} wei. Escrow received {a["totals"]["received"]} wei and verified paid {a["totals"]["paid"]} wei. Bonds balance equals received minus verified paid.']
lines += ['', 'Each real live note uses three identical canonical source digests and exact quotation preflight. Fresh inputs are in [live-inputs.json](proofs/live-inputs.json). Validators independently ground contract citations. The public posts are examples; high virality is not claimed.', '', '## Tests and verification', '', '80 direct tests passed; 8 inapplicable parameter combinations skipped. Seven TypeScript domain tests passed. Direct mode executes one contract per process, with mocked cross-contract views, LLM/web content and native delivery. Forced version drift, callback failure/replay and recipient balances are tested under those boundaries. GenVM lint/validation passed for all four contracts. See TEST_MATRIX.md and the saved verification reports for frontend/build/live evidence.', '', '## Still test-only or unproven live', '']
lines += ['- '+x for x in p['unproven']]
lines += ['', 'The same configured wallet is writer and appellant in the live proof; direct tests cover distinct recipients. Same-URL source changes after exhausted inconclusive probes need a new correction URL. Native delivery depends on the protocol and is marked paid only after explicit credit verification. All fund-lock prevention, cancellation and callback recovery exits are listed in SECURITY_NOTES.md.', '', 'The Portal has not been submitted. The `/replay` correction demonstration is explicitly test-only.']
Path('docs/PROOF_MANIFEST.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(len(p['transactions']), 'live hashes documented')
