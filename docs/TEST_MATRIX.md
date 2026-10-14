# Test matrix

Current baseline: **107 direct tests** (8 inapplicable parameter combinations explicitly skipped) and **11 frontend/domain unit tests** passed. TypeScript strict, ESLint, all four GenVM contract lint/schema checks, and Next.js production build passed. Counts and final browser/live evidence are also recorded in the proof manifest.

| Requirement | Tests/evidence | Scope |
|---|---|---|
| All four evidence labels × three tone labels | `test_labels_and_independent_tone_are_stored` | 12 direct cases |
| UNSUPPORTED valid and stored | Same label tests | Direct + finalized live |
| Allegation forbidden labels forced neutral; no name, handle or text in state | `test_allegation_forced_unsupported_and_no_name_text_or_handle_state` | Direct |
| Prompt injection cannot bypass grounding | `test_bad_quote_and_injection_cannot_bypass_grounding` | Direct |
| Quote-independent URL-set agreement, typography and exact own-page grounding across Notes/Recheck/Appeals | `test_consensus.py` | 27 direct cases; fresh long-NASA live supported note |
| Disallowed and lookalike hosts before fetch | Host parameterized tests + callback guards | Direct |
| 429 then 200, decoded whitespace-stable canonical digest | Retry and canonical digest test | Direct |
| Address exhaustion does not block another writer | 20 real method calls + second wallet creation | Direct |
| Third inconclusive recheck rejected before fetch | `test_two_uncertain_rechecks_then_pre_fetch_rejection` | Direct |
| Added-source recheck changes UNSUPPORTED to SUPPORTED; both versions retained | Flow tests + authorized append + fresh live receipts | Direct + finalized live; desktop/mobile history |
| Separate writer/appellant wallets, honest appeal settlement and exact credits | Two public CLI wallets, funding receipt, balance table | Finalized live; separate accounts, not verified human identities |
| Unauthorized Notes updates / callback / wiring rejected | Notes and flow access-control tests | Direct |
| Appeal overturn/uphold/uncertain, late/duplicate rejected | Appeal flow tests and settlement allocation tests | Direct |
| Overturn waits for finalized Notes update | Bonds rejection test | Direct |
| Bond released only after original window | Bond withdrawal test | Direct time travel |
| Exact claim allocation, no duplicate payment | Settlement + verified withdrawal tests | Direct native emission stub |
| Failed credit retry only after verified failure | Attempt/replay/receipt-binding tests | Direct |
| Forged recipient, amount, absent credit, unfinalized child, wrong parent | Five forged-receipt cases | Direct |
| Recheck open appeal guard before web/model work | `test_open_appeal_recheck_guard_before_fetch` | Direct + live expected rejection |
| Recheck staging/finalization race preserves appealed version | `test_notes_rechecks_cannot_race_an_open_appeal` | Direct |
| Version drift and never-judged deadline + grace cancellation; replay/judge-after-cancel rejected | `test_cancel_stale_closes_once_and_rejects_replays` | Direct; archived v2 live timeout cancellation |
| Exact full cancellation refund, writer release, appellant/writer/Bonds balances, no double payout | `test_cancel_exact_recipient_balances_and_writer_release` | Direct modeled native ledger |
| Missing activation, unused and reserved funding, callback resumption | Recovery tests in `test_recovery.py` | Direct |
| Production defaults, five-minute minimum, 30-day maximum and independent grace/release bounds | Constructor tests in `test_recovery.py` | 20 direct cases |
| URL checks, bigint bond precision, neutral copy, tone, safe post links, failed finalized execution | `tests/domain.test.ts` | Seven TypeScript tests |
| One connection request shared across concurrent clicks; authorized accounts reused; pending and cancelled requests recover | `tests/wallet.test.ts` | Four TypeScript tests with an injected mock provider; no live wallet writes |
| Pending-request guidance, disabled connection/write controls, cancellation and approved connection on desktop/mobile | `scripts/wallet-browser-check.ts`, `proofs/wallet-ui-check.json` | Controlled provider/feed fixtures; no real permission, signature or transaction |
| Desktop/mobile UI, form validation, four explorer links, no horizontal overflow | `scripts/browser-check.ts` | Production Chrome; saved report/screenshots |
| Contract finality, state matching, native credit | `npm run verify:network` | Read-only live proof |

Direct mode executes one deployed contract per process. Cross-contract views/emissions are monkeypatched through `genlayer.gl.get_contract_at`, matching Bullseye's Windows-compatible harness. LLM replies are JSON-encoded. The validator callback test explicitly invokes the real comparator with independent mocked content; the suite does not claim full validator-network equivalence from direct mode alone.

Fresh production verification reports are saved in `proofs/production-verification.json` and `proofs/production-browser-report.json`; field lengths and every HTTP 200 link are recorded in `submission/link-check.json`. Historical v2 reports remain archived.

Generation 3 production deployment `dpl_7TDZX7PpMsXBo71Wapj15J42NfdG` is ready. Both history versions, their labels and sources passed checks at 1440- and 390-pixel viewports. All 111 packaged HTTP links returned 200. Portal fields are 145/180, 867/1000 and 319/500 characters. `proofs/verification-summary.json` records the tests, build and audit counts; PROOF_MANIFEST lists all 101 current/recovery hashes. `proofs/network-verification.txt` records the successful read-only audit.

Eight parameter combinations do not apply to both contract fixtures and are explicitly skipped. The source-driven SUPPORTED-to-CONTRADICTED replay calls the actual Recheck method with mocked post/source responses, captures its authorized update, and verifies changed canonical evidence. Its public replay is labeled test-only.


## Fixed deployment target

StudioNet 61999, generation 3.

| Contract | Address |
|---|---|
| notes | [0xDc5B83F68928E56B483d3Ec34F0f578f6dD8b2a5](https://explorer-studio.genlayer.com/contracts/0xDc5B83F68928E56B483d3Ec34F0f578f6dD8b2a5) |
| bonds | [0x123Dbc27daCe9939A880E1fcE13Ef8FB60aA4Ea5](https://explorer-studio.genlayer.com/contracts/0x123Dbc27daCe9939A880E1fcE13Ef8FB60aA4Ea5) |
| recheck | [0x5911648404b6C96d0DB941e1bCe430E018024c7B](https://explorer-studio.genlayer.com/contracts/0x5911648404b6C96d0DB941e1bCe430E018024c7B) |
| appeals | [0x2F0e761a1b9584A391814a59cb86Bc8A0df5A2C4](https://explorer-studio.genlayer.com/contracts/0x2F0e761a1b9584A391814a59cb86Bc8A0df5A2C4) |

Timing disclosure: the public demo deployment uses a 15-minute appeal window; production default is 72 hours. Demo grace is 10 minutes and bond release delay is 15 minutes.
