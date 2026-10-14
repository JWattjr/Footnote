# Footnote

Is this viral post backed by its sources, and is it built to provoke? Footnote attaches source-grounded community notes to public Bluesky posts. GenLayer validators independently fetch the post and its sources. Evidence gets SUPPORTED, CONTRADICTED, UNSUPPORTED, or MISLEADING; tone separately gets RAGE_BAIT, NOT_RAGE_BAIT, or UNCLEAR.

UNSUPPORTED is a valid stored judgment. New evidence can create a new version. The original is never rewritten. Anyone can contest a note version during its configured appeal window. Writers lock 2–20 simulated GEN; successful appellants receive overturned writer bonds. Withdrawals use pull payments and independently verified native credit.

Live app: [footnote-genlayer.vercel.app](https://footnote-genlayer.vercel.app). Public repository: [JWattjr/Footnote](https://github.com/JWattjr/Footnote).

The finalized live proof preserves an UNSUPPORTED version and appends SUPPORTED after a genuine NASA source is added. Wallet A writes the long-source supported note and wallet B appeals it; the honest UPHELD decision, settlement, exact balances and native credits are recorded in [PROOF_MANIFEST.md](docs/PROOF_MANIFEST.md). Two signing wallets demonstrate separate contract participants; independently verified human identities are not claimed.

Timing disclosure: the public demo deployment uses a 15-minute appeal window; production default is 72 hours. The demo cancellation grace is 10 minutes and bond release delay is 15 minutes. Constructor defaults are 72 hours for appeals and bond release, and 24 hours for cancellation grace. Every window must be 5 minutes–30 days; bond release delay must cover the appeal window. Deadlines use real chain time and run from the original writer stake; finalization consumes part of that window.

Appeal funding goes directly into Bonds before opening the appeal. Rechecks are rejected before fetching while an appeal is open. Anyone can cancel a stale version or an unjudged appeal after its deadline plus grace, recovering the full deposit through a verified pull withdrawal. Unused funding and stalled callbacks have recovery methods. The previous immutable deployment is archived in `docs/legacy/v1`; all four original writer bonds were released after their real deadlines and eight GEN were recovered through verified native credits. Its Bonds escrow is zero. The app targets generation 3. The funded v2 receipts, source bytes and failure diagnosis are archived in `docs/legacy/v2`; its remaining eight GEN were recovered through verified withdrawals.

## Deployed contracts

StudioNet, chain **61999**, RPC `https://studio.genlayer.com/api`. The reproducible deployment manifest is [public/deployment.json](public/deployment.json); all deployment/write hashes and raw receipts are in [docs/proofs](docs/proofs).

| Contract | Address | Responsibility |
|---|---|---|
| Notes | `0xDc5B83F68928E56B483d3Ec34F0f578f6dD8b2a5` | Exclusive note state, judgments and immutable versions |
| Recheck | `0x5911648404b6C96d0DB941e1bCe430E018024c7B` | Independent source rereads, new evidence and bounded inconclusive attempts |
| Bonds | `0x123Dbc27daCe9939A880E1fcE13Ef8FB60aA4Ea5` | Writer escrow, appeal deposits, reputation, verified pull payouts |
| Appeals | `0x2F0e761a1b9584A391814a59cb86Bc8A0df5A2C4` | One contest per version, counter-evidence, UPHELD/OVERTURNED/UNCERTAIN |

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

Validators compare labels and cited URL sets rather than independently selected quote spans. Each validator still grounds every leader quote in its own source text, allowing only whitespace and specified typography normalization, with case-sensitive substring matching. The leader quotes remain stored.

## Trust boundaries and people safety

Labels are judgments about supplied public sources, not proof of objective truth. Grounding establishes that a quote occurs in a source, not that the source is truthful. The fixed host allowlist is a policy choice. The app reads Bluesky only; it does not authenticate a Bluesky author as the owner of an Ethereum wallet. Anyone may appeal.

An allegation of crime or misconduct about an identifiable person only permits SUPPORTED or UNSUPPORTED. The latter appears as **“No credible public source found yet.”** Neither label establishes guilt or innocence. Code enforces the restriction independently of the model. The person flag remains sticky across versions. Post text, names, handles and free-form model explanations are never stored in contract state. For allegation citations even exact quote text is withheld from state, retaining source URLs and quote fingerprints. A post URI, SHA-256 text fingerprint, labels, source URLs and operational metadata remain.

Bluesky post text is fetched off-chain for display and checked against its stored fingerprint. A deleted or changed post displays “post unavailable” while the note history stays available. StudioNet is a simulator; GEN here is simulated and this is not production financial infrastructure. Direct tests are mocked execution, not network-consensus proof.

107 direct tests and eleven TypeScript tests pass, with eight inapplicable scenario fixtures skipped. Four wallet regression tests cover overlapping requests, existing permissions, pending requests and cancellation recovery. Typecheck, lint, all four GenVM checks, production build, read-only network verification and desktop/mobile history checks are recorded in [TEST_MATRIX.md](docs/TEST_MATRIX.md).

## Submission package

- [Architecture](docs/ARCHITECTURE.md), [security](docs/SECURITY_NOTES.md), [test matrix](docs/TEST_MATRIX.md)
- [Live proof manifest](docs/PROOF_MANIFEST.md), [tutorial](docs/TUTORIAL.md), [60-second demo](docs/DEMO.md)
- [Portal fields](docs/submission/portal-fields.json)

The Portal submission remains manual. This project does not submit to Builder → Projects.
