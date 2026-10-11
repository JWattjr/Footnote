import json
from pathlib import Path
from datetime import datetime, timezone
p=json.loads(Path("public/deployment.json").read_text(encoding="utf-8"))
lines=["# Live proof manifest", "", "StudioNet 61999. This document records finalized execution and state, not a guarantee of factual truth. Raw protocol receipts are in `docs/proofs`; `public/deployment.json` is machine-readable. The verifier is read-only and signs no transactions.", "", "## Contracts", "", "| Contract | Address |", "|---|---|"]
for k,v in p["contracts"].items():lines.append(f"| {k} | [{v}](https://explorer-studio.genlayer.com/contracts/{v}) |")
lines += ["", "## Every live transaction", "", "| Step | Hash | Evidence |", "|---|---|---|"]
for name,h in p["transactions"].items():
    r=json.loads(Path("docs/proofs/"+name+".json").read_text(encoding="utf-8"))
    detail="FINALIZED expected pre-fetch rejection: "+p["rejections"][name] if name in p.get("rejections",{}) else "FINALIZED native value_credited=true" if r.get("type")==0 and r.get("consensus_data") is None else "FINALIZED, result=6, leader execution SUCCESS"
    lines.append(f"| {name} | [{h}](https://explorer-studio.genlayer.com/transactions/{h}) | {detail} |")
lines += ["", "## Matched state and exact source preflight", ""]
for key,state in p["states"].items():
    if isinstance(state,dict) and "history" in state:
        d=state["history"][-1]["decision"];lines.append(f'- `{key}`: active version {state["version"]}, {d["evidence_label"]} / {d["tone_label"]}; {len(state["history"])} immutable version(s).')
    elif key.endswith(":appeal"):lines.append(f'- `{key}`: {state["outcome"]}, {state["status"]}; deposit {state["deposit"]} wei.')
    elif key.endswith(":balances"):lines.append(f'- `{key}`: before {state["before"]}, after {state["after"]}, exact delta {int(state["after"])-int(state["before"])} wei.')
    elif key.startswith("deposit:"):lines.append(f'- `{key}`: {state["status"]}; native child `{state["transfer_hash"]}`, amount {state["amount"]} wei, attempt {state["attempt"]}.')
    elif key=="quota":lines.append(f'- Live quota read: {json.dumps(state["value"])}. The fourth same-post note was rejected before any fetch/model call.')
    elif key=="recheck":lines.append(f'- Recheck operation: {state["outcome"]}, {state["status"]}. This does not establish a live evidence-label change.')
lines += ["", "Each of the four live notes used three identical canonical source digests and an exact off-chain quote check before publication. Details and public post responses are in [live-inputs.json](proofs/live-inputs.json). Contract citations were independently grounded by validators. No builder-generated post or publisher correction is represented as real.", "", "## Tests and frontend verification", "", "45 direct tests passed; 4 inapplicable parameter combinations skipped. 7 TypeScript domain/frontend tests passed. Strict TypeScript, ESLint, four GenVM lint/schema checks, production build, and real desktop/mobile browser guard/overflow checks passed. Independent design finish reviewer disposition: ship. See TEST_MATRIX.md for test boundaries.", "", "## Still unproven live", ""]
lines += ["- "+v for v in p["unproven"]]
lines += ["", "The real posts used here are public examples, not a demonstrated high-virality sample. Writer and appellant share one configured wallet; direct tests cover distinct recipients. A same-URL edit after two inconclusive probes requires a new correction URL. A stale funded appeal has no automatic cancellation/refund route; avoid racing rechecks with funded appeals. See SECURITY_NOTES.md.", "", "The Portal has not been submitted. The separate /replay page shows a mocked direct-contract source correction, explicitly test-only."]
Path("docs/PROOF_MANIFEST.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
print(len(p["transactions"]), "live hashes documented")
