Quota2 withdrawal resumed after a transport timeout

The RPC/SDK poll aborted with DOMException TimeoutError after quota2-verify-bond parent 0x43841b12e91c7cdaae7e6982eec77cc6e84d6627f665a2d01f102914d550c9e5 was FINALIZED successfully. Its callback hash 0xdb28279d03d6b3da6abc499b8f71f10ce620c686c4f5e91036b22ec961d27d37 was already persisted. The withdrawal 0x4b94a147950f061527549ccb8d1b7016088ab7c3f0f6f46f34017dbb53ae7150 and native credit 0xf2788cf76c40f26f369a42a0d936afbf7970711213e06bd6ec740ed79aaee98e had already finalized.

Resuming scripts/deploy.ps1 -Step withdraw-bond with FOOTNOTE_CASE=quota2 re-reads every saved parent and child hash. It does not submit another release, withdrawal or verification. This is receipt-transport recovery, not an on-chain execution failure.

Resumption completed: all saved parents and children are FINALIZED and successful, and get_claim returned paid for bond:climate-quota-2 with attempt 1 and the same native transfer hash. The recorded wallet delta is exactly 2 GEN. No new quota2 hash was submitted.

The full read-only network audit also received a transient HTML response during the historical recovery phase. Re-reading the same hashes completed successfully: all 73 current hashes, all 28 v2 recovery hashes, final states, exact balances and deployed source bytes passed. No write was issued during this audit.
