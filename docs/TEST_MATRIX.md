# Test matrix

Current baseline: **45 direct tests** (4 inapplicable parameter combinations explicitly skipped) and **7 frontend/domain unit tests** passed. TypeScript strict, ESLint, all four GenVM contract lint/schema checks, and Next.js production build passed. Counts and final browser/live evidence are also recorded in the proof manifest.

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
| URL checks, bigint bond precision, neutral copy, tone, safe post links, failed finalized execution | `tests/domain.test.ts` | Seven TypeScript tests |
| Desktop/mobile UI, form validation, four explorer links, no horizontal overflow | `scripts/browser-check.ts` | Real local browser, report/screenshots |
| Contract finality, state matching, native credit | `npm run verify:network` | Read-only live proof |

Direct mode executes one deployed contract per process. Cross-contract views/emissions are monkeypatched through `genlayer.gl.get_contract_at`, matching Bullseye's Windows-compatible harness. LLM replies are JSON-encoded. The validator callback test explicitly invokes the real comparator with independent mocked content; the suite does not claim full validator-network equivalence from direct mode alone.

Four parameter combinations do not apply to both contract fixtures and are explicitly skipped. The source-driven SUPPORTED-to-CONTRADICTED replay calls the actual Recheck method with mocked post/source responses, captures its authorized update, and verifies changed canonical evidence. Its public replay is labeled test-only.
