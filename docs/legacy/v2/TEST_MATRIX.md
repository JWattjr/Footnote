# Test matrix

Current baseline: **80 direct tests** (8 inapplicable parameter combinations explicitly skipped) and **7 frontend/domain unit tests** passed. TypeScript strict, ESLint, all four GenVM contract lint/schema checks, and Next.js production build passed. Counts and final browser/live evidence are also recorded in the proof manifest.

| Requirement | Tests/evidence | Scope |
|---|---|---|
| All four evidence labels × three tone labels | `test_labels_and_independent_tone_are_stored` | 12 direct cases |
| UNSUPPORTED valid and stored | Same label tests | Direct + finalized live |
| Allegation forbidden labels forced neutral; no name, handle or text in state | `test_allegation_forced_unsupported_and_no_name_text_or_handle_state` | Direct |
| Prompt injection cannot bypass grounding | `test_bad_quote_and_injection_cannot_bypass_grounding` | Direct |
| Leader quote checked against own page | Grounding helper + actual validator callback tests | Direct mocked validator invocation |
| Disallowed and lookalike hosts before fetch | Host parameterized tests + callback guards | Direct |
| 429 then 200, decoded whitespace-stable canonical digest | Retry and canonical digest test | Direct |
| Address exhaustion does not block another writer | 20 real method calls + second wallet creation | Direct |
| Third inconclusive recheck rejected before fetch | `test_two_uncertain_rechecks_then_pre_fetch_rejection` | Direct |
| Recheck emits version update; history retained | Flow tests + authorized append test | Direct cross-contract stub |
| Unauthorized Notes updates / callback / wiring rejected | Notes and flow access-control tests | Direct |
| Appeal overturn/uphold/uncertain, late/duplicate rejected | Appeal flow tests and settlement allocation tests | Direct |
| Overturn waits for finalized Notes update | Bonds rejection test | Direct |
| Bond released only after original window | Bond withdrawal test | Direct time travel |
| Exact claim allocation, no duplicate payment | Settlement + verified withdrawal tests | Direct native emission stub |
| Failed credit retry only after verified failure | Attempt/replay/receipt-binding tests | Direct |
| Forged recipient, amount, absent credit, unfinalized child, wrong parent | Five forged-receipt cases | Direct |
| Recheck open appeal guard before web/model work | `test_open_appeal_recheck_guard_before_fetch` | Direct + live expected rejection |
| Recheck staging/finalization race preserves appealed version | `test_notes_rechecks_cannot_race_an_open_appeal` | Direct |
| Version drift and never-judged deadline + grace cancellation; replay/judge-after-cancel rejected | `test_cancel_stale_closes_once_and_rejects_replays` | Direct; finalized live timeout cancellation |
| Exact full cancellation refund, writer release, appellant/writer/Bonds balances, no double payout | `test_cancel_exact_recipient_balances_and_writer_release` | Direct modeled native ledger |
| Missing activation, unused and reserved funding, callback resumption | Recovery tests in `test_recovery.py` | Direct |
| Production defaults, five-minute minimum, 30-day maximum and independent grace/release bounds | Constructor tests in `test_recovery.py` | 20 direct cases |
| URL checks, bigint bond precision, neutral copy, tone, safe post links, failed finalized execution | `tests/domain.test.ts` | Seven TypeScript tests |
| Desktop/mobile UI, form validation, four explorer links, no horizontal overflow | `scripts/browser-check.ts` | Production Chrome; saved report/screenshots |
| Contract finality, state matching, native credit | `npm run verify:network` | Read-only live proof |

Direct mode executes one deployed contract per process. Cross-contract views/emissions are monkeypatched through `genlayer.gl.get_contract_at`, matching Bullseye's Windows-compatible harness. LLM replies are JSON-encoded. The validator callback test explicitly invokes the real comparator with independent mocked content; the suite does not claim full validator-network equivalence from direct mode alone.

The Vercel production build and deployment passed on 12 October after the approval-review usage limit reset. The contract proof completed on 11 October. `proofs/production-verification.json` confirms the production address/hash journal, four live notes and timing disclosure; `proofs/production-browser-report.json` records desktop/mobile checks. `submission/link-check.json` records all 80 links returning HTTP 200. Portal fields use 145/180, 865/1000 and 357/500 characters.

Eight parameter combinations do not apply to both contract fixtures and are explicitly skipped. The source-driven SUPPORTED-to-CONTRADICTED replay calls the actual Recheck method with mocked post/source responses, captures its authorized update, and verifies changed canonical evidence. Its public replay is labeled test-only.


## Fixed deployment target

StudioNet 61999, generation 2.

| Contract | Address |
|---|---|
| notes | [0xA71d317f87AAa68287901bAF1C6210F34AAD3675](https://explorer-studio.genlayer.com/contracts/0xA71d317f87AAa68287901bAF1C6210F34AAD3675) |
| bonds | [0x55CE2f217257e9CB94C83954ff635c5131Ef71ba](https://explorer-studio.genlayer.com/contracts/0x55CE2f217257e9CB94C83954ff635c5131Ef71ba) |
| recheck | [0x24AE6019820999664F95085e0775Cfe6968BB082](https://explorer-studio.genlayer.com/contracts/0x24AE6019820999664F95085e0775Cfe6968BB082) |
| appeals | [0x45FC5215210E8D7A856cC630923a26b216cD9565](https://explorer-studio.genlayer.com/contracts/0x45FC5215210E8D7A856cC630923a26b216cD9565) |
