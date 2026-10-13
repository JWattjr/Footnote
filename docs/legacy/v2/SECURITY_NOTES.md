# Security notes

## Enforced boundaries

- Exact HTTPS hostname membership; no suffix matching, userinfo, nonstandard ports or fragment URLs. Lookalike domains are rejected before nondeterminism.
- HTML script/style removal, decoded entities, stripped tags and collapsed whitespace. JSON is parsed and serialized with sorted keys. Digest canonical extracted text, never raw bytes.
- One immediate retry on HTTP 429 or 5xx; subsequently unavailable. A source outage can yield a valid UNSUPPORTED judgment, never a fabricated quote.
- The post and page text are untrusted data. Prompt instructions say to ignore embedded instructions, while deterministic code validates labels, URL membership, quote membership and person restrictions.
- Each non-UNSUPPORTED result requires at least one exact quoted supplied source. Validators independently classify and validate leader quotes against their own reads. Comparison excludes free-form text.
- Person allegations allow only SUPPORTED/UNSUPPORTED. SUPPORTED additionally requires the validator's explicit-public-report field. Names, handles and post text are never saved. Allegation quotes are stored only as fingerprints. This is source reporting, not a guilt/innocence finding.
- All label changes and monetary settlement effects wait for protected finalized self-callbacks. Only Recheck/Appeals update Notes. Only Bonds marks deposit settlement and closes open-note quota.
- One appeal per version, immutable constructor-configured original deadline, per-address open/post quotas, and pre-fetch UNCERTAIN limits. There is no small shared global quota.
- Pull withdrawals reserve attempts; paid requires finalized positive native-credit evidence with exact parent and child binding. A failed transfer alone does not enable retries before verification finalizes.

## Escrow liveness audit and fixed exits

Timing disclosure: the public demo deployment uses a 15-minute appeal window; production default is 72 hours. The demo cancellation grace is 10 minutes and bond release delay is 15 minutes; production defaults are 24 hours and 72 hours respectively. All three constructor windows require 300–2,592,000 seconds. Release delay must cover the appeal window.

| Previously stuck or stalled state | Fixed exit and protection |
|---|---|
| Recheck changes a funded appeal's version | Recheck rejects before any fetch with `[EXPECTED] note has an open appeal; recheck after it is decided`. Notes repeats the guard while staging and finalizing updates, discarding a racing staged recheck. |
| Stale open appeal or unapplied stale decision | Anyone calls `cancel_stale` when versions differ. Protected finalized cancellation allocates the full deposit to the appellant, settles it through Bonds, and closes the appeal. An already-applied overturn settles normally. |
| Open appeal never judged, or judgment continually fails | Anyone cancels at the immutable note deadline plus configured grace. Before that time, matching versions cannot cancel. |
| Failed value-bearing deposit forwarding | Removed. `Bonds.fund_appeal` receives funds directly; Appeals only sends state callbacks without value. `refund_unopened` allocates unused funding back to its appellant, including a losing competing funder. Reserved funding cannot be reclaimed underneath an appeal. |
| Stake or funding callback stalls | Permissionless `resume_bond` / `resume_funding` repeat the protected finalized callback. Unpublished writer bonds release after their real release time; closing a nonexistent note is harmless. |
| Appeal opening or deposit activation/holding callback stalls | `resume_appeal` / `resume_deposit` activate and finalize the bound deposit. Cancellation also supports missing activation; resuming finishes holding and then settlement. No second payment is forwarded. |
| Judging finalization or overturned Notes update stalls | `resume_appeal` resumes judging finality, the missing authorized update, or `Notes.resume_note` for staged updates. A genuinely stale unapplied update can cancel instead. |
| Deposit allocation or appeal-close callback stalls | `resume_deposit` completes allocation or repeats the Bonds-only `mark_settled` close. The open count remains held until finalized settlement, preventing premature bond release. |
| Writer release or note-close callback stalls | `resume_bond` finishes claim allocation or note closure. Release requires mature real time and no open appeal; CANCELLED deposits leave the writer's normal release rules intact. |
| Credit verification callback stalls | `resume_claim` finalizes the verified attempt. Unknown/pending native credit stays reserved and can be verified again against the same parent hash. |
| Refunded funding races appeal opening | Timeout/version cancellation recognizes the existing funding refund claim, marks its deposit settled, and closes the appeal without allocating a second refund. Pending refund finality resumes through `resume_funding`. |
| Cancel/refund/settlement callback replay | State guards and unique claim keys reject replayed cancellation, refund and settlement callbacks. A second cancel, judge after cancel, repeated close, and repeated withdrawal cannot allocate or pay twice. |

All recovery methods emit protected callbacks on `finalized`; callers cannot change recipients, amounts, deadlines or decisions. Recovery is permissionless; withdrawing remains recipient-only. Direct tests cover forced version drift, timeout boundaries, distinct writer/appellant allocations and exact modeled ledger balances. Cross-contract calls and native delivery are mocked in direct mode; live receipts establish actual StudioNet credit separately.

Native ledger delivery remains a protocol boundary. GenLayer documents that value on a failed emitted message is not automatically returned. This implementation avoids value-bearing contract-to-contract deposit forwarding. If a native withdrawal is explicitly uncredited, its verified claim remains retryable only after full unpaid backing is restored; it never appropriates another user's escrow. A protocol outage or lost native value requires protocol restoration before payment can complete. Receipt unavailability never marks a claim paid or enables a duplicate transfer. This is an external protocol dependency, not an administrative refund override.

## Remaining limitations and threat model

The allegation detector and assessment of reputable explicit reporting still require honest validator consensus. Code constrains the consequences of a positive allegation flag; it cannot determine every allegation without semantic interpretation. The fixed allowlist permits particular hosts, not every factual claim hosted there. A government site or reputable outlet can be mistaken. A quote occurring on a page is not proof that its claim is accurate.

The runtime web transport may follow redirects; the contract validates the submitted host but does not claim an independently audited redirect chain. Fixed trusted-domain policy reduces exposure, and deployers must avoid open-redirect source endpoints. Full-page content can include changing navigation; canonical extraction stabilizes markup changes, not substantive text changes. Validators compare semantic decisions and citation sets rather than digests, so digest metadata describes the leader's observation and does not claim byte equality across validators.

The spam requirement and automatic detection of a same-URL edit conflict after two inconclusive attempts: a new allowlisted correction URL is necessary to open another probe without fetching first. False/nonrelevant new URLs can still consume bounded consensus. History grows over time. The current index shows the first twelve records, not a complete production indexing service.

A wire operation is deployer-only and one-time. Its addresses are not changeable afterward, so a flawed deployed contract requires replacement and explicit migration of the app configuration. There is no administrative label, payout-recipient or balance override.

For the live proof, same-wallet writer/appellant demonstrates contract routing but does not prove independent participants. Direct tests use distinct fixture wallets and a controlled native ledger; they do not prove StudioNet consensus. Native transfer credit requires explicit protocol evidence, and unknown receipt schemas fail closed. Sources and network reads may throttle, and the API's short cache can delay presentation of a freshly finalized version.

StudioNet GEN and chain state are simulated. This release has not undergone an external security audit. The documented tests and proof manifest define the actual verified scope; no broader guarantee is implied.

## Dependency audit

The runtime-only npm audit reports zero vulnerabilities. The full audit reports five high-severity development-tool entries, all arising from the same braces <=3.0.3 stack-exhaustion advisory through the Next ESLint plugin, fast-glob and micromatch. These tools consume the fixed repository lint patterns and are not shipped as application request handlers. npm proposes downgrading eslint-config-next to Next 14; that incompatible downgrade was not applied. The raw full/runtime audit reports are committed in docs/proofs. Revisit the upstream tooling patch before accepting arbitrary glob input in a build service.

## Immutable legacy instance

Generation 1 cannot be patched or rewired. Its original eight simulated GEN of writer bonds remain in the old Bonds contract under the original 72-hour deadlines on 14 October; redeployment does not migrate those funds. The legacy contracts retain the confirmed stale-appeal defect. The public app and new proofs target the fixed generation 2 addresses only. Do not fund or open new appeals on generation 1. Its existing bonds still have their ordinary mature-release path if no appeal is open; see the archived exact addresses and state in `docs/legacy/v1/deployment.json`.


## Fixed deployment target

StudioNet 61999, generation 2.

| Contract | Address |
|---|---|
| notes | [0xA71d317f87AAa68287901bAF1C6210F34AAD3675](https://explorer-studio.genlayer.com/contracts/0xA71d317f87AAa68287901bAF1C6210F34AAD3675) |
| bonds | [0x55CE2f217257e9CB94C83954ff635c5131Ef71ba](https://explorer-studio.genlayer.com/contracts/0x55CE2f217257e9CB94C83954ff635c5131Ef71ba) |
| recheck | [0x24AE6019820999664F95085e0775Cfe6968BB082](https://explorer-studio.genlayer.com/contracts/0x24AE6019820999664F95085e0775Cfe6968BB082) |
| appeals | [0x45FC5215210E8D7A856cC630923a26b216cD9565](https://explorer-studio.genlayer.com/contracts/0x45FC5215210E8D7A856cC630923a26b216cD9565) |
