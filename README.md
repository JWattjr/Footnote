# Footnote

Is this viral post backed by its sources, and is it built to provoke? Footnote attaches source-grounded community notes to public Bluesky posts. GenLayer validators independently fetch the post and its sources. Evidence gets SUPPORTED, CONTRADICTED, UNSUPPORTED, or MISLEADING; tone separately gets RAGE_BAIT, NOT_RAGE_BAIT, or UNCLEAR.

UNSUPPORTED is a valid stored judgment. New evidence can create a new version. The original is never rewritten. Anyone can contest a note version during its 72-hour window. Writers lock 2–20 simulated GEN; successful appellants receive overturned writer bonds. Withdrawals use pull payments and independently verified native credit.

Live app: [footnote-genlayer.vercel.app](https://footnote-genlayer.vercel.app). Public repository: [JWattjr/Footnote](https://github.com/JWattjr/Footnote).

## Deployed contracts

StudioNet, chain **61999**, RPC `https://studio.genlayer.com/api`. The reproducible deployment manifest is [public/deployment.json](public/deployment.json); all deployment/write hashes and raw receipts are in [docs/proofs](docs/proofs).

| Contract | Address | Responsibility |
|---|---|---|
| Notes | `0x2b027eE3e14662E2D70cb0C94edD46f18473EcF9` | Exclusive note state, judgments and immutable versions |
| Recheck | `0x875453E32f1b7E1B319Ecb7052176a258919F515` | Independent source rereads, new evidence and bounded inconclusive attempts |
| Bonds | `0xBDd887bAD156dE83147823DaaA3838480Aa17b1b` | Writer escrow, appeal deposits, reputation, verified pull payouts |
| Appeals | `0xd99886f31cEB34Cd9E5D050aeBB152A8f93e7Cf0` | One contest per version, counter-evidence, UPHELD/OVERTURNED/UNCERTAIN |

These are deployment addresses, not a claim that every requested live flow is proven. See [PROOF_MANIFEST.md](docs/PROOF_MANIFEST.md) for the exact evidence and remaining gaps.

## Run

Requires Node.js 24, Python 3.14, and an unlocked configured GenLayer CLI account for deploy scripts. Reading the app requires no wallet; writes use a connected wallet with the GenLayer plugin.

```sh
npm ci
python -m pip install -r requirements.txt
python scripts/build-contracts.py
genvm-lint check contracts/notes.py
genvm-lint check contracts/recheck.py
genvm-lint check contracts/bonds.py
genvm-lint check contracts/appeals.py
python -m pytest tests/direct -q
npm test
npm run typecheck
npm run lint
npm run build
npm run start
```

The app serves port 3117. `npm run dev` starts development mode. `npm run verify:network` only reads receipts and finalized contract state. `npm run verify:submission` prints field lengths and checks every submission URL. `npx tsx scripts/browser-check.ts` checks the local app on desktop and mobile with an installed Chrome.

## Deployment

`contracts-src/` contains the shared helpers and four contract bodies. `scripts/build-contracts.py` inlines them into four standalone deployable contracts, all pinned to the requested GenVM runner. The deployed bytecode sources are committed under `contracts/`.

`genlayer network set studionet`, then `npm run deploy:contracts`. The CLI retains its signing key. The deploy script records each transaction hash before polling, resumes that same hash after a timeout, recursively verifies finalized callbacks, and checks execution success separately from lifecycle status. Wiring is one-time deployer bootstrap, resolving the four-contract address cycle; Notes rejects later rewiring. There is no owner label override.

## Trust boundaries and people safety

Labels are judgments about supplied public sources, not proof of objective truth. Grounding establishes that a quote occurs in a source, not that the source is truthful. The fixed host allowlist is a policy choice. The app reads Bluesky only; it does not authenticate a Bluesky author as the owner of an Ethereum wallet. Anyone may appeal.

An allegation of crime or misconduct about an identifiable person only permits SUPPORTED or UNSUPPORTED. The latter appears as **“No credible public source found yet.”** Neither label establishes guilt or innocence. Code enforces the restriction independently of the model. The person flag remains sticky across versions. Post text, names, handles and free-form model explanations are never stored in contract state. For allegation citations even exact quote text is withheld from state, retaining source URLs and quote fingerprints. A post URI, SHA-256 text fingerprint, labels, source URLs and operational metadata remain.

Bluesky post text is fetched off-chain for display and checked against its stored fingerprint. A deleted or changed post displays “post unavailable” while the note history stays available. StudioNet is a simulator; GEN here is simulated and this is not production financial infrastructure. Direct tests are mocked execution, not network-consensus proof.

## Submission package

- [Architecture](docs/ARCHITECTURE.md), [security](docs/SECURITY_NOTES.md), [test matrix](docs/TEST_MATRIX.md)
- [Live proof manifest](docs/PROOF_MANIFEST.md), [tutorial](docs/TUTORIAL.md), [60-second demo](docs/DEMO.md)
- [Portal fields](docs/submission/portal-fields.json)

The Portal submission remains manual. This project does not submit to Builder → Projects.
