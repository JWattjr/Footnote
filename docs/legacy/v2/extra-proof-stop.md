# Additional live proofs: stopped on failure

Stopped at 2026-10-12T22:43:21.554Z. Contracts were not changed or redeployed. No transaction was resubmitted. The Portal was not submitted.

The attempted independent note was FINALIZED with result 7 and three disagree votes. Its leader returned SUPPORTED / NOT_RAGE_BAIT, but consensus did not accept the publication. No finalized callback was triggered and finalized Notes reads confirm the note is absent. An earlier leader round returned `[EXPECTED] citation quote not found in fetched source`. Exact raw receipts and decoded leader outputs are saved alongside this report.

## Every new transaction

| Step | Hash | Outcome |
|---|---|---|
| extra-change-stake | [0xb4e03050f291d19b0f39366b9f7e17c2dcbb6ec3efe0d4857e2f45cd847f09e8](https://explorer-studio.genlayer.com/transactions/0xb4e03050f291d19b0f39366b9f7e17c2dcbb6ec3efe0d4857e2f45cd847f09e8) | FINALIZED successful execution |
| extra-change-stake-child-0 | [0x967a7f1aa18fcf106c8ef182d72fe5dfb45f74fea013b6fe1d8db7fbe7892bc3](https://explorer-studio.genlayer.com/transactions/0x967a7f1aa18fcf106c8ef182d72fe5dfb45f74fea013b6fe1d8db7fbe7892bc3) | FINALIZED successful execution |
| extra-change-note | [0x2d906eafa7bf7e0f46a2c6818e63cc3147f57a0c035bf408c3846a344dd4425c](https://explorer-studio.genlayer.com/transactions/0x2d906eafa7bf7e0f46a2c6818e63cc3147f57a0c035bf408c3846a344dd4425c) | FINALIZED successful execution |
| extra-change-note-child-0 | [0x7842ad14b17edf371a41418b97eb6e9269d5dc5eaa657041b9f64293b9365432](https://explorer-studio.genlayer.com/transactions/0x7842ad14b17edf371a41418b97eb6e9269d5dc5eaa657041b9f64293b9365432) | FINALIZED successful execution |
| extra-independent-stake | [0xf5738d0d95a684adda0128a33b0d327cf54b00c262e6fc8d5c47424b9d1567a7](https://explorer-studio.genlayer.com/transactions/0xf5738d0d95a684adda0128a33b0d327cf54b00c262e6fc8d5c47424b9d1567a7) | FINALIZED successful execution |
| extra-independent-stake-child-0 | [0xff0aeaa66805ec367f3abeaa4ccff922827c890571f5dda9f7fbe4a219861a97](https://explorer-studio.genlayer.com/transactions/0xff0aeaa66805ec367f3abeaa4ccff922827c890571f5dda9f7fbe4a219861a97) | FINALIZED successful execution |
| extra-independent-note | [0x4aa7085e10e758f949f9f631c35de195be6fc3ca563a1f91b7137cacb2e193e8](https://explorer-studio.genlayer.com/transactions/0x4aa7085e10e758f949f9f631c35de195be6fc3ca563a1f91b7137cacb2e193e8) | FINALIZED consensus rejection; result 7 |

## Incomplete proofs

`temperature-update-2025` is active, version 1, UNSUPPORTED / NOT_RAGE_BAIT. Its earlier history is finalized. Recheck was not sent after the independent-note failure; there is no live label change.

The prepared added source is https://science.nasa.gov/earth/explore/earth-indicators/global-temperature/. Exact preflight quotation: "the two years are effectively tied according to an analysis by NASA scientists.". This source returned 200 with the quote present and three identical canonical digests before writes. The existing page would be new evidence supplied to this note, not a publisher correction or a newly published source. Full post, source URL, quote and fetch records are in `extra-inputs.json`.

Wallet B was created using the GenLayer CLI, and its key remains in the CLI/OS keychain. It was never funded, so there is no funding hash, appeal, decision or withdrawal in the additional two-wallet proof.

## Public wallets and exact balances (wei)

- Writer wallet A: `0xdb433ff614bdd1ece21aa97221c3e0a7ecf79c92`.
- Intended appellant wallet B: `0xbc1a363b1427531fcb05d03ddf4d34e729011186`.

| Account | Before attempted proofs | At stop |
|---|---:|---:|
| Wallet A | 8000999999999999956 | 4000999999999999956 |
| Wallet B | 0 | 0 |
| Bonds | 4000000000000000000 | 8000000000000000000 |

Both new stakes are 2 simulated GEN, finalized and held in Bonds. Neither has an open appeal. The failed publication does not remove its ordinary mature-release route. These stakes were not released or withdrawn after the stop.
- `temperature-update-2025`: normal release time 2026-10-12T23:50:13+01:00 (Africa/Lagos); bond status `locked`.
- `independent-climate-appeal`: normal release time 2026-10-12T23:54:22+01:00 (Africa/Lagos); bond status `locked`.

Bonds totals at stop: received 16000000000000000000 wei; verified paid 8000000000000000000 wei; held 8000000000000000000 wei. Its 8 GEN balance consists of 4 GEN from the earlier quota bonds plus the 4 GEN of new stakes. The three-account balance sum is conserved exactly.

## Verification and package status

80 direct tests passed, with 8 fixture skips. Seven frontend tests passed. Typecheck and lint passed. The production build passed after rerunning outside the sandbox that denied a Next.js generated directory. Contract files were not modified.

Submission fields remain unchanged because neither new proof completed. Lengths: oneLiner 145/180, description 865/1000, expectedOutcome 357/500. New-link verification, final network verification, Vercel deployment, commit and push were stopped. Main remains at `9005422`; diagnostic changes are local and uncommitted.
