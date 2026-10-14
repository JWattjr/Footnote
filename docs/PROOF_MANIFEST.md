# Live proof manifest

StudioNet 61999, generation 3. Finality and successful execution are verified separately. Raw receipts are in `docs/proofs`; `public/deployment.json` is the persisted transaction journal. The network verifier is read-only.

Timing disclosure: the public demo deployment uses a 15-minute appeal window; production default is 72 hours. Demo cancellation grace is 10 minutes and bond release delay is 15 minutes. Production defaults are 24 hours for grace and 72 hours for bond release. Constructor bounds are five minutes–30 days. Deadlines use actual chain time; no time travel is used.

Generation 3 fixes literal quote-span consensus. Validators compare evidence, tone, allegation flag and sorted unique cited URLs; Appeals also compares its outcome. Every leader quote still passes an exact, case-sensitive substring check against each validator’s own page, after specified typography/whitespace normalization. Stored quotes are the leader’s. See SECURITY_NOTES.md.

## Current contracts

| Contract | Address |
|---|---|
| notes | [0xDc5B83F68928E56B483d3Ec34F0f578f6dD8b2a5](https://explorer-studio.genlayer.com/contracts/0xDc5B83F68928E56B483d3Ec34F0f578f6dD8b2a5) |
| bonds | [0x123Dbc27daCe9939A880E1fcE13Ef8FB60aA4Ea5](https://explorer-studio.genlayer.com/contracts/0x123Dbc27daCe9939A880E1fcE13Ef8FB60aA4Ea5) |
| recheck | [0x5911648404b6C96d0DB941e1bCe430E018024c7B](https://explorer-studio.genlayer.com/contracts/0x5911648404b6C96d0DB941e1bCe430E018024c7B) |
| appeals | [0x2F0e761a1b9584A391814a59cb86Bc8A0df5A2C4](https://explorer-studio.genlayer.com/contracts/0x2F0e761a1b9584A391814a59cb86Bc8A0df5A2C4) |

## Every current live transaction

| Step | Hash | Evidence |
|---|---|---|
| deploy-notes | [0xb64add76871bf995ac1f76a8776f2611815aa7aa5115b44078762fbb2fe95792](https://explorer-studio.genlayer.com/transactions/0xb64add76871bf995ac1f76a8776f2611815aa7aa5115b44078762fbb2fe95792) | FINALIZED, result=6, leader execution SUCCESS |
| deploy-bonds | [0x0322473bbd47a52c14ba5f2a78cc25394fe66427ee2d446937e0e55df30aac65](https://explorer-studio.genlayer.com/transactions/0x0322473bbd47a52c14ba5f2a78cc25394fe66427ee2d446937e0e55df30aac65) | FINALIZED, result=6, leader execution SUCCESS |
| deploy-recheck | [0xce6cfc7e01c4340b8b528ad232528a9f3f1f2f08c71411866f7a9bf3658c16ce](https://explorer-studio.genlayer.com/transactions/0xce6cfc7e01c4340b8b528ad232528a9f3f1f2f08c71411866f7a9bf3658c16ce) | FINALIZED, result=6, leader execution SUCCESS |
| deploy-appeals | [0xf0ea6d12f525a4af72bffc3e991a6f67544ee224e0a551132f3dc542ed90f55e](https://explorer-studio.genlayer.com/transactions/0xf0ea6d12f525a4af72bffc3e991a6f67544ee224e0a551132f3dc542ed90f55e) | FINALIZED, result=6, leader execution SUCCESS |
| wire-bonds | [0xa124f786495d38086faebb51f0d0d18bcb81e0ba5bc12793d79d3e74bf880e40](https://explorer-studio.genlayer.com/transactions/0xa124f786495d38086faebb51f0d0d18bcb81e0ba5bc12793d79d3e74bf880e40) | FINALIZED, result=6, leader execution SUCCESS |
| wire-notes | [0x847efae4c645bcd20f7252e1f76208ccee85d33f6f85c56bdc8d457027e05a03](https://explorer-studio.genlayer.com/transactions/0x847efae4c645bcd20f7252e1f76208ccee85d33f6f85c56bdc8d457027e05a03) | FINALIZED, result=6, leader execution SUCCESS |
| extra-independent-stake | [0xf63b54532f486c99b9255fe995fb0c298f1416086ec8f277e98c3c4933b33e56](https://explorer-studio.genlayer.com/transactions/0xf63b54532f486c99b9255fe995fb0c298f1416086ec8f277e98c3c4933b33e56) | FINALIZED, result=6, leader execution SUCCESS |
| extra-independent-stake-child-0 | [0xef62ef015c89000b457c47bc111ad041ebf14e1738afbb7c5e44fbfa5dd561a5](https://explorer-studio.genlayer.com/transactions/0xef62ef015c89000b457c47bc111ad041ebf14e1738afbb7c5e44fbfa5dd561a5) | FINALIZED, result=6, leader execution SUCCESS |
| extra-independent-note | [0xe1e4da9905fe8a2e73f7c5767c337a80bef905b85763b44896156c1828ebf9ef](https://explorer-studio.genlayer.com/transactions/0xe1e4da9905fe8a2e73f7c5767c337a80bef905b85763b44896156c1828ebf9ef) | FINALIZED, result=6, leader execution SUCCESS |
| extra-independent-note-child-0 | [0xc07859f1a89085a614d5b1d5aa1347e4b25b3c9751d6d7202cd3cec249560549](https://explorer-studio.genlayer.com/transactions/0xc07859f1a89085a614d5b1d5aa1347e4b25b3c9751d6d7202cd3cec249560549) | FINALIZED, result=6, leader execution SUCCESS |
| extra-fund-wallet-b | [0xc4fd62ee04620325b501cb5927722a2c724062dbd0c27ed810e4a82578e371d8](https://explorer-studio.genlayer.com/transactions/0xc4fd62ee04620325b501cb5927722a2c724062dbd0c27ed810e4a82578e371d8) | FINALIZED native value_credited=true |
| extra-independent-fund-appeal | [0x7f29e0dbdddeb655158ebac6b3e1a8e43787fcd7cddf4ab0b56a1083107db502](https://explorer-studio.genlayer.com/transactions/0x7f29e0dbdddeb655158ebac6b3e1a8e43787fcd7cddf4ab0b56a1083107db502) | FINALIZED, result=6, leader execution SUCCESS |
| extra-independent-fund-appeal-child-0 | [0x5a265a02c5a50c6645bc3db7c7ee3816d68db3c622fdf3d012f6febe7fb1060b](https://explorer-studio.genlayer.com/transactions/0x5a265a02c5a50c6645bc3db7c7ee3816d68db3c622fdf3d012f6febe7fb1060b) | FINALIZED, result=6, leader execution SUCCESS |
| extra-independent-contest | [0xce90cc3cb29d9a0396f8bec327a168c161c6e8d8f8d1446851cf700fc6c8eca6](https://explorer-studio.genlayer.com/transactions/0xce90cc3cb29d9a0396f8bec327a168c161c6e8d8f8d1446851cf700fc6c8eca6) | FINALIZED, result=6, leader execution SUCCESS |
| extra-independent-contest-child-0 | [0xe6e9d147158a723fb84a0a927164faf8be9aa81ae09fb4dd256b016b19fb009e](https://explorer-studio.genlayer.com/transactions/0xe6e9d147158a723fb84a0a927164faf8be9aa81ae09fb4dd256b016b19fb009e) | FINALIZED, result=6, leader execution SUCCESS |
| extra-independent-contest-child-0-child-0 | [0xc541ee76c44024c980c1d405dd03e74e09544e58c32c863fd4eeb2772855a83b](https://explorer-studio.genlayer.com/transactions/0xc541ee76c44024c980c1d405dd03e74e09544e58c32c863fd4eeb2772855a83b) | FINALIZED, result=6, leader execution SUCCESS |
| extra-independent-contest-child-0-child-0-child-0 | [0x0a4ca8f059162ffe45ddf05c0af887a13532b49293507c769350354ec66011bc](https://explorer-studio.genlayer.com/transactions/0x0a4ca8f059162ffe45ddf05c0af887a13532b49293507c769350354ec66011bc) | FINALIZED, result=6, leader execution SUCCESS |
| reject-open-recheck | [0xc497e7a49d770017560a125391cf718c44eb6a9d772e8d43f6a8f696a3c33ac1](https://explorer-studio.genlayer.com/transactions/0xc497e7a49d770017560a125391cf718c44eb6a9d772e8d43f6a8f696a3c33ac1) | FINALIZED expected pre-fetch rejection: [EXPECTED] note has an open appeal; recheck after it is decided |
| reject-host | [0x6f9078cde084a3d16d614fdea92d7f049079eab0f6c4733ef80bb2ae73849fe4](https://explorer-studio.genlayer.com/transactions/0x6f9078cde084a3d16d614fdea92d7f049079eab0f6c4733ef80bb2ae73849fe4) | FINALIZED expected pre-fetch rejection: source host is not allowed |
| extra-independent-judge | [0xad61fd76d6b99ab842c61ff8e59bbedfc0b122d8086613f7e2399a946377d2b4](https://explorer-studio.genlayer.com/transactions/0xad61fd76d6b99ab842c61ff8e59bbedfc0b122d8086613f7e2399a946377d2b4) | FINALIZED, result=6, leader execution SUCCESS |
| extra-independent-judge-child-0 | [0xa2bc0c6e3eda373915068807de55761ead005201dd8398ca3e44ed749921ae35](https://explorer-studio.genlayer.com/transactions/0xa2bc0c6e3eda373915068807de55761ead005201dd8398ca3e44ed749921ae35) | FINALIZED, result=6, leader execution SUCCESS |
| extra-independent-settle | [0xe3b162e5906a70ff65af7d8fbaf0c67d6195d846b8760f2b6f17f491c85a5efa](https://explorer-studio.genlayer.com/transactions/0xe3b162e5906a70ff65af7d8fbaf0c67d6195d846b8760f2b6f17f491c85a5efa) | FINALIZED, result=6, leader execution SUCCESS |
| extra-independent-settle-child-0 | [0xed4f3aa6be17ac3ab5a1bc503bccbebe2c9ddbc729d19957622e946982e8f41f](https://explorer-studio.genlayer.com/transactions/0xed4f3aa6be17ac3ab5a1bc503bccbebe2c9ddbc729d19957622e946982e8f41f) | FINALIZED, result=6, leader execution SUCCESS |
| extra-independent-settle-child-0-child-0 | [0xdd26149fd4e6d50d0c32b9160f3f22c5bf0664f8b1b6778d79d6910ddbec0a2b](https://explorer-studio.genlayer.com/transactions/0xdd26149fd4e6d50d0c32b9160f3f22c5bf0664f8b1b6778d79d6910ddbec0a2b) | FINALIZED, result=6, leader execution SUCCESS |
| extra-change-stake | [0x236cfb6d221a3a052570df9a086360c0cd3f2053e618eb4d72ee8befca7cdd26](https://explorer-studio.genlayer.com/transactions/0x236cfb6d221a3a052570df9a086360c0cd3f2053e618eb4d72ee8befca7cdd26) | FINALIZED, result=6, leader execution SUCCESS |
| extra-change-stake-child-0 | [0xdc5f8e614fbddb8a46503355f4bead0087934a316f7bbd7693b38a5b3fea9329](https://explorer-studio.genlayer.com/transactions/0xdc5f8e614fbddb8a46503355f4bead0087934a316f7bbd7693b38a5b3fea9329) | FINALIZED, result=6, leader execution SUCCESS |
| extra-change-note | [0xaf88379bf20465b48dafdf460a2aa663acd97c6cc45bd91298d0fe4f6ccdb22b](https://explorer-studio.genlayer.com/transactions/0xaf88379bf20465b48dafdf460a2aa663acd97c6cc45bd91298d0fe4f6ccdb22b) | FINALIZED, result=6, leader execution SUCCESS |
| extra-change-note-child-0 | [0x22bb546f1014988712782263b65e61faa9b9607004406038ed7da4120420c294](https://explorer-studio.genlayer.com/transactions/0x22bb546f1014988712782263b65e61faa9b9607004406038ed7da4120420c294) | FINALIZED, result=6, leader execution SUCCESS |
| extra-change-recheck | [0x20a7775758928f1b3e320bc9bcbf76bf2cfccaa94af4ee33d519959b79f03c5d](https://explorer-studio.genlayer.com/transactions/0x20a7775758928f1b3e320bc9bcbf76bf2cfccaa94af4ee33d519959b79f03c5d) | FINALIZED, result=6, leader execution SUCCESS |
| extra-change-recheck-child-0 | [0x6638569a79d770eb062c166ee5152de21fc6436d4e310e2a850c0feddd0d961a](https://explorer-studio.genlayer.com/transactions/0x6638569a79d770eb062c166ee5152de21fc6436d4e310e2a850c0feddd0d961a) | FINALIZED, result=6, leader execution SUCCESS |
| extra-change-recheck-child-0-child-0 | [0x578e9861416bf82e4bf7e7ce90aba394932b8711e59a9af243d0ac67b6a7dd4c](https://explorer-studio.genlayer.com/transactions/0x578e9861416bf82e4bf7e7ce90aba394932b8711e59a9af243d0ac67b6a7dd4c) | FINALIZED, result=6, leader execution SUCCESS |
| extra-change-recheck-child-0-child-0-child-0 | [0x57d4cc6575d293a185a344b8af53d6b76b895e8d0df1443ef7defb2dec836422](https://explorer-studio.genlayer.com/transactions/0x57d4cc6575d293a185a344b8af53d6b76b895e8d0df1443ef7defb2dec836422) | FINALIZED, result=6, leader execution SUCCESS |
| quota2-stake | [0xf6acbed7b94b202ff507c685ff03cb5062b0188219536882b8815d9d782b70cd](https://explorer-studio.genlayer.com/transactions/0xf6acbed7b94b202ff507c685ff03cb5062b0188219536882b8815d9d782b70cd) | FINALIZED, result=6, leader execution SUCCESS |
| quota2-stake-child-0 | [0xbc6dde677f472732c5abc99bd0e086417ea4b4430d5e53ba3fb1357c87172ac4](https://explorer-studio.genlayer.com/transactions/0xbc6dde677f472732c5abc99bd0e086417ea4b4430d5e53ba3fb1357c87172ac4) | FINALIZED, result=6, leader execution SUCCESS |
| quota2-note | [0x3537611ef5329600701fb45a50e9d48ae0638e6d3439fa17ed2ce9a6cf4419f3](https://explorer-studio.genlayer.com/transactions/0x3537611ef5329600701fb45a50e9d48ae0638e6d3439fa17ed2ce9a6cf4419f3) | FINALIZED, result=6, leader execution SUCCESS |
| quota2-note-child-0 | [0x3a5ba3cd4363d36ded67a7fd68cddea8f85b57559352cc7954ea8b34f46b8bf9](https://explorer-studio.genlayer.com/transactions/0x3a5ba3cd4363d36ded67a7fd68cddea8f85b57559352cc7954ea8b34f46b8bf9) | FINALIZED, result=6, leader execution SUCCESS |
| quota3-stake | [0xe7b8358ad775c33b901a7b8c6a240d35b781505d0607599f46369f300db29a52](https://explorer-studio.genlayer.com/transactions/0xe7b8358ad775c33b901a7b8c6a240d35b781505d0607599f46369f300db29a52) | FINALIZED, result=6, leader execution SUCCESS |
| quota3-stake-child-0 | [0x35b703d5ac2ab9586231f7b89f658893e98eab123b1569cee066cb2c16dd4a21](https://explorer-studio.genlayer.com/transactions/0x35b703d5ac2ab9586231f7b89f658893e98eab123b1569cee066cb2c16dd4a21) | FINALIZED, result=6, leader execution SUCCESS |
| quota3-note | [0xf2a6b10c1aeb2fdb4f392e8b980512a48cfae8ac0edf0fad6de62d03e6570dd6](https://explorer-studio.genlayer.com/transactions/0xf2a6b10c1aeb2fdb4f392e8b980512a48cfae8ac0edf0fad6de62d03e6570dd6) | FINALIZED, result=6, leader execution SUCCESS |
| quota3-note-child-0 | [0xccdfbbc7c7104e7ce388b4672c72953ad7ebebf034945a253c5134b0ab2de7a6](https://explorer-studio.genlayer.com/transactions/0xccdfbbc7c7104e7ce388b4672c72953ad7ebebf034945a253c5134b0ab2de7a6) | FINALIZED, result=6, leader execution SUCCESS |
| reject-quota | [0xaf3afa11bfab9a3f56e391f028a0d22a44aa00d24d72c6b99fac2a48ea28b46f](https://explorer-studio.genlayer.com/transactions/0xaf3afa11bfab9a3f56e391f028a0d22a44aa00d24d72c6b99fac2a48ea28b46f) | FINALIZED expected pre-fetch rejection: three notes per post per address quota |
| extra-independent-deposit-withdraw | [0x0eb26fc3c7ec34a0ad9d7fce7892e97454595956d838f19e1266a74eadac5c84](https://explorer-studio.genlayer.com/transactions/0x0eb26fc3c7ec34a0ad9d7fce7892e97454595956d838f19e1266a74eadac5c84) | FINALIZED, result=6, leader execution SUCCESS |
| extra-independent-deposit-withdraw-child-0 | [0x80e2b9d0788f850d430bf57b8a2b11bae01d20d651e911e22e428b1baae0065b](https://explorer-studio.genlayer.com/transactions/0x80e2b9d0788f850d430bf57b8a2b11bae01d20d651e911e22e428b1baae0065b) | FINALIZED native value_credited=true |
| extra-independent-deposit-verify | [0x317883dad352df3fa3ddacc38a3904b5bc57b09f34bc2ae613a0d95ed7fc29bf](https://explorer-studio.genlayer.com/transactions/0x317883dad352df3fa3ddacc38a3904b5bc57b09f34bc2ae613a0d95ed7fc29bf) | FINALIZED, result=6, leader execution SUCCESS |
| extra-independent-deposit-verify-child-0 | [0xdf788e952b568f591173eced5f13c3ed3063257ae032560194c44605caa8c7aa](https://explorer-studio.genlayer.com/transactions/0xdf788e952b568f591173eced5f13c3ed3063257ae032560194c44605caa8c7aa) | FINALIZED, result=6, leader execution SUCCESS |
| extra-independent-bond-release | [0x50b52fc38688a449e1eaa83d3a7ef7a01dc4c940901190360e65d1ffe4a458a8](https://explorer-studio.genlayer.com/transactions/0x50b52fc38688a449e1eaa83d3a7ef7a01dc4c940901190360e65d1ffe4a458a8) | FINALIZED, result=6, leader execution SUCCESS |
| extra-independent-bond-release-child-0 | [0x85d904ade66ae50bbc517142a71ffb576801c3da8061b821cc340a183e1ca5ed](https://explorer-studio.genlayer.com/transactions/0x85d904ade66ae50bbc517142a71ffb576801c3da8061b821cc340a183e1ca5ed) | FINALIZED, result=6, leader execution SUCCESS |
| extra-independent-bond-release-child-0-child-0 | [0x39738434dd6a7719c312e02ae620524b865f18cf4c0ab52792b97a0a9b6af4cf](https://explorer-studio.genlayer.com/transactions/0x39738434dd6a7719c312e02ae620524b865f18cf4c0ab52792b97a0a9b6af4cf) | FINALIZED, result=6, leader execution SUCCESS |
| extra-independent-bond-withdraw | [0xe9d7cbcfa47d547faf598fcb8d30d1a4fca55b61233f7ae57b16a2d879c0311b](https://explorer-studio.genlayer.com/transactions/0xe9d7cbcfa47d547faf598fcb8d30d1a4fca55b61233f7ae57b16a2d879c0311b) | FINALIZED, result=6, leader execution SUCCESS |
| extra-independent-bond-withdraw-child-0 | [0xc577e9141ea6d1bc9d6d7b319413cd329e26754a52d18ecc1deb53b1b2a335e6](https://explorer-studio.genlayer.com/transactions/0xc577e9141ea6d1bc9d6d7b319413cd329e26754a52d18ecc1deb53b1b2a335e6) | FINALIZED native value_credited=true |
| extra-independent-bond-verify | [0xfe064d6069ccaac3ef5abd5fb70cc5ef111b0990759674e99782f494aece48e8](https://explorer-studio.genlayer.com/transactions/0xfe064d6069ccaac3ef5abd5fb70cc5ef111b0990759674e99782f494aece48e8) | FINALIZED, result=6, leader execution SUCCESS |
| extra-independent-bond-verify-child-0 | [0xf7371d9a7c4550f0bd55d607a7fb27d69f4ea23287124cd70d4a0861ec804c3c](https://explorer-studio.genlayer.com/transactions/0xf7371d9a7c4550f0bd55d607a7fb27d69f4ea23287124cd70d4a0861ec804c3c) | FINALIZED, result=6, leader execution SUCCESS |
| extra-change-bond-release | [0xb375777966d22f6ec05160ff7a70364439a3ea89b93e48e2e6c5c14856cb2f2f](https://explorer-studio.genlayer.com/transactions/0xb375777966d22f6ec05160ff7a70364439a3ea89b93e48e2e6c5c14856cb2f2f) | FINALIZED, result=6, leader execution SUCCESS |
| extra-change-bond-release-child-0 | [0x0d6390552c619bbd79a9d29373bba177e85a81e07b58914d2025d182827ab998](https://explorer-studio.genlayer.com/transactions/0x0d6390552c619bbd79a9d29373bba177e85a81e07b58914d2025d182827ab998) | FINALIZED, result=6, leader execution SUCCESS |
| extra-change-bond-release-child-0-child-0 | [0x865263d8e35737f48eb6429f17fa9cc925cd7fc94fcb85d2faf24673ed77c943](https://explorer-studio.genlayer.com/transactions/0x865263d8e35737f48eb6429f17fa9cc925cd7fc94fcb85d2faf24673ed77c943) | FINALIZED, result=6, leader execution SUCCESS |
| extra-change-bond-withdraw | [0xab12d500bbc24de3541e7b319dac46d1e221c6971ff78b61dbca07a9ea7ee584](https://explorer-studio.genlayer.com/transactions/0xab12d500bbc24de3541e7b319dac46d1e221c6971ff78b61dbca07a9ea7ee584) | FINALIZED, result=6, leader execution SUCCESS |
| extra-change-bond-withdraw-child-0 | [0xfe166b6dfae62c9d10f4b9072c531827156fc74d535af66acef2cb0520a0b7b5](https://explorer-studio.genlayer.com/transactions/0xfe166b6dfae62c9d10f4b9072c531827156fc74d535af66acef2cb0520a0b7b5) | FINALIZED native value_credited=true |
| extra-change-bond-verify | [0x54fe902ae30047aa7d2e4dad90b0205f5069675100da106abead323c103e5ad7](https://explorer-studio.genlayer.com/transactions/0x54fe902ae30047aa7d2e4dad90b0205f5069675100da106abead323c103e5ad7) | FINALIZED, result=6, leader execution SUCCESS |
| extra-change-bond-verify-child-0 | [0x3a06cd8a2483675473f464afc0d4e767c1be7d4969340a299fa1151cafac3faa](https://explorer-studio.genlayer.com/transactions/0x3a06cd8a2483675473f464afc0d4e767c1be7d4969340a299fa1151cafac3faa) | FINALIZED, result=6, leader execution SUCCESS |
| quota2-release | [0x0dcd929e37dc50560719e12b80c27f76ff9626b892fe9a78bcc9c9f5aa5f695d](https://explorer-studio.genlayer.com/transactions/0x0dcd929e37dc50560719e12b80c27f76ff9626b892fe9a78bcc9c9f5aa5f695d) | FINALIZED, result=6, leader execution SUCCESS |
| quota2-release-child-0 | [0xaca84ae08aa12bf9434c442d5835982fb4847dc30d91e045c289f54c68400b95](https://explorer-studio.genlayer.com/transactions/0xaca84ae08aa12bf9434c442d5835982fb4847dc30d91e045c289f54c68400b95) | FINALIZED, result=6, leader execution SUCCESS |
| quota2-release-child-0-child-0 | [0x5c6e32fce0ccf2f93ef3ac23bd0ebac1e5675eddddf8272edc51b341f8a203a5](https://explorer-studio.genlayer.com/transactions/0x5c6e32fce0ccf2f93ef3ac23bd0ebac1e5675eddddf8272edc51b341f8a203a5) | FINALIZED, result=6, leader execution SUCCESS |
| quota2-withdraw-bond | [0x4b94a147950f061527549ccb8d1b7016088ab7c3f0f6f46f34017dbb53ae7150](https://explorer-studio.genlayer.com/transactions/0x4b94a147950f061527549ccb8d1b7016088ab7c3f0f6f46f34017dbb53ae7150) | FINALIZED, result=6, leader execution SUCCESS |
| quota2-withdraw-bond-child-0 | [0xf2788cf76c40f26f369a42a0d936afbf7970711213e06bd6ec740ed79aaee98e](https://explorer-studio.genlayer.com/transactions/0xf2788cf76c40f26f369a42a0d936afbf7970711213e06bd6ec740ed79aaee98e) | FINALIZED native value_credited=true |
| quota2-verify-bond | [0x43841b12e91c7cdaae7e6982eec77cc6e84d6627f665a2d01f102914d550c9e5](https://explorer-studio.genlayer.com/transactions/0x43841b12e91c7cdaae7e6982eec77cc6e84d6627f665a2d01f102914d550c9e5) | FINALIZED, result=6, leader execution SUCCESS |
| quota2-verify-bond-child-0 | [0xdb28279d03d6b3da6abc499b8f71f10ce620c686c4f5e91036b22ec961d27d37](https://explorer-studio.genlayer.com/transactions/0xdb28279d03d6b3da6abc499b8f71f10ce620c686c4f5e91036b22ec961d27d37) | FINALIZED, result=6, leader execution SUCCESS |
| quota3-release | [0x98b80b0f912ea66c65d97040912d1685cdbfa5874e17fc9d7f59864163fcaee7](https://explorer-studio.genlayer.com/transactions/0x98b80b0f912ea66c65d97040912d1685cdbfa5874e17fc9d7f59864163fcaee7) | FINALIZED, result=6, leader execution SUCCESS |
| quota3-release-child-0 | [0x85d6b98300c9b95657d54e90e3d7ccbb04173074001a705bb4fd4f4646b37ca0](https://explorer-studio.genlayer.com/transactions/0x85d6b98300c9b95657d54e90e3d7ccbb04173074001a705bb4fd4f4646b37ca0) | FINALIZED, result=6, leader execution SUCCESS |
| quota3-release-child-0-child-0 | [0x78b53d192c588165acba6e36c4f8eeb157c3be8e36cdca454e35614cb009ae9f](https://explorer-studio.genlayer.com/transactions/0x78b53d192c588165acba6e36c4f8eeb157c3be8e36cdca454e35614cb009ae9f) | FINALIZED, result=6, leader execution SUCCESS |
| quota3-withdraw-bond | [0x68bba3450bfda810a1f047e8e06dc302c27819a5dc3875f1408dcecedf4db144](https://explorer-studio.genlayer.com/transactions/0x68bba3450bfda810a1f047e8e06dc302c27819a5dc3875f1408dcecedf4db144) | FINALIZED, result=6, leader execution SUCCESS |
| quota3-withdraw-bond-child-0 | [0xbf59b888db47a7810d6cb93e7aba7095bc1a357666f062c6d59a6c85ad01a113](https://explorer-studio.genlayer.com/transactions/0xbf59b888db47a7810d6cb93e7aba7095bc1a357666f062c6d59a6c85ad01a113) | FINALIZED native value_credited=true |
| quota3-verify-bond | [0xe3821591c7056f84a02858fcae62f8aca275b8f8f21a73ad9b990f9d969b396b](https://explorer-studio.genlayer.com/transactions/0xe3821591c7056f84a02858fcae62f8aca275b8f8f21a73ad9b990f9d969b396b) | FINALIZED, result=6, leader execution SUCCESS |
| quota3-verify-bond-child-0 | [0x5c2090ad7bdc68cb6df6c5c79eeb55b42915418ec0a0e9bd24059c79134ad1d6](https://explorer-studio.genlayer.com/transactions/0x5c2090ad7bdc68cb6df6c5c79eeb55b42915418ec0a0e9bd24059c79134ad1d6) | FINALIZED, result=6, leader execution SUCCESS |

## Matched finalized state

- `config`: `{"appeal_window_seconds": 900, "appeals": "0x2F0e761a1b9584A391814a59cb86Bc8A0df5A2C4", "bonds": "0x123Dbc27daCe9939A880E1fcE13Ef8FB60aA4Ea5", "hosts": ["apnews.com", "climate.copernicus.eu", "en.wikipedia.org", "europepmc.org", "science.nasa.gov", "svs.gsfc.nasa.gov", "www.bbc.com", "www.ebi.ac.uk", "www.gov.uk", "www.justice.gov", "www.nasa.gov", "www.ncei.noaa.gov", "www.noaa.gov", "www.reuters.com", "www.theguardian.com"], "recheck": "0x5911648404b6C96d0DB941e1bCe430E018024c7B", "wired": true}`.
- `bondsConfig`: `{"appeal_window_seconds": 900, "release_delay_seconds": 900}`.
- `appealsConfig`: `{"appeal_window_seconds": 900, "cancel_grace_seconds": 600}`.
- `independent-climate-appeal`: active, v1, SUPPORTED / NOT_RAGE_BAIT, open quota False; actual original appeal deadline 2026-10-13T07:28:44+00:00.
- `independent-climate-appeal:appeal`: UPHELD, settled; deposit 2000000000000000000 wei.
- `temperature-update-2025`: active, v2, SUPPORTED / NOT_RAGE_BAIT, open quota False; actual original appeal deadline 2026-10-13T07:47:10+00:00.
- Recheck operation: UPDATED, finalized.
- `climate-quota-2`: active, v1, SUPPORTED / NOT_RAGE_BAIT, open quota False; actual original appeal deadline 2026-10-13T07:55:52+00:00.
- `climate-quota-3`: active, v1, SUPPORTED / NOT_RAGE_BAIT, open quota False; actual original appeal deadline 2026-10-13T07:59:24+00:00.
- Quota read: `{"open": 0, "per_post": 3}`; fourth same-post creation rejected before fetching.
- `deposit:independent-climate-appeal:1`: paid, amount 2000000000000000000 wei; verified native child `0x80e2b9d0788f850d430bf57b8a2b11bae01d20d651e911e22e428b1baae0065b`; withdrawal attempt 1.
- `bond:independent-climate-appeal`: paid, amount 2000000000000000000 wei; verified native child `0xc577e9141ea6d1bc9d6d7b319413cd329e26754a52d18ecc1deb53b1b2a335e6`; withdrawal attempt 1.
- `bond:temperature-update-2025`: paid, amount 2000000000000000000 wei; verified native child `0xfe166b6dfae62c9d10f4b9072c531827156fc74d535af66acef2cb0520a0b7b5`; withdrawal attempt 1.
- `bond:climate-quota-2`: paid, amount 2000000000000000000 wei; verified native child `0xf2788cf76c40f26f369a42a0d936afbf7970711213e06bd6ec740ed79aaee98e`; withdrawal attempt 1.
- `bond:climate-quota-3`: paid, amount 2000000000000000000 wei; verified native child `0xbf59b888db47a7810d6cb93e7aba7095bc1a357666f062c6d59a6c85ad01a113`; withdrawal attempt 1.

Historical finalized quota read immediately after the fourth-note rejection: `{"open": 4, "per_post": 3}`. The current quota falls as mature bonds are released; the historical saturation snapshot is retained separately.

## Added-source label change and distinct-wallet appeal

Wallet A (writer/funder): `0xdb433ff614bdd1ece21aa97221c3e0a7ecf79c92`. Wallet B (appellant): `0xbc1a363b1427531fcb05d03ddf4d34e729011186`. The signing key stays in the encrypted CLI keystore and OS credential store; only public addresses are recorded. These are two separate signing accounts operated for the demonstration, not independently verified human identities.

`temperature-update-2025`: v1 **UNSUPPORTED** → v2 **SUPPORTED**, reason RECHECK, operation `recheck-1`. The earlier history entry is retained unchanged in finalized state.

Wallet B’s appeal of A’s note is **UPHELD**, settled and closed. The challenge reuses the authentic NASA evidence, without fabricated opposing claims. The deposit and writer bond are paid through verified native credits after the real release window.

Stored v2 leader citation: [https://science.nasa.gov/earth/explore/earth-indicators/global-temperature/](https://science.nasa.gov/earth/explore/earth-indicators/global-temperature/) — “Earth’s global surface temperature in 2025 was slightly warmer than 2023 – but within the margin of error: the two years are effectively tied according to an analysis by NASA scientists. Since record-keeping began in 1880, the hottest year on record remains 2024 (source: NASA/GISS ).”

### Off-chain evidence preflight

The initial supplied page predates the 2025 measurement and does not establish the complete post claim. Adding an existing credible page demonstrates new evidence supplied to this note, not a publisher correction or newly published source.

Source: [https://svs.gsfc.nasa.gov/4964/](https://svs.gsfc.nasa.gov/4964/). Preflight quote: “Earth’s global average surface temperature in 2021 tied with 2018 as the sixth warmest on record”. Three HTTP 200 fetches, case-sensitive normalized quote presence, identical canonical SHA-256 `89843b1ba734d2de4975ed3fdbe7d06a483414b9358d454fa707408ced06fc35`.

Source: [https://science.nasa.gov/earth/explore/earth-indicators/global-temperature/](https://science.nasa.gov/earth/explore/earth-indicators/global-temperature/). Preflight quote: “the two years are effectively tied according to an analysis by NASA scientists.”. Three HTTP 200 fetches, case-sensitive normalized quote presence, identical canonical SHA-256 `1e25c7c2a80cfaf650927f9ca3e672b505cea66175e435170357c1fe0993098f`.

Source: [https://science.nasa.gov/earth/explore/earth-indicators/global-temperature/](https://science.nasa.gov/earth/explore/earth-indicators/global-temperature/). Preflight quote: “Since record-keeping began in 1880, the hottest year on record remains 2024”. Three HTTP 200 fetches, case-sensitive normalized quote presence, identical canonical SHA-256 `1e25c7c2a80cfaf650927f9ca3e672b505cea66175e435170357c1fe0993098f`.

Source: [https://science.nasa.gov/earth/explore/earth-indicators/global-temperature/](https://science.nasa.gov/earth/explore/earth-indicators/global-temperature/). Preflight quote: “The 10 most recent years are the warmest on record.”. Three HTTP 200 fetches, case-sensitive normalized quote presence, identical canonical SHA-256 `1e25c7c2a80cfaf650927f9ca3e672b505cea66175e435170357c1fe0993098f`.

Fresh snapshots precede each new note and the recheck in `docs/proofs/preflight-<step>.json`. The quota3 preflight briefly refused changing navigation digests; it resumed the same existing stake only after the unchanged URL and quotes passed three fresh matching fetches. No publication was sent during that off-chain pause; see `proofs/quota3-preflight-pause.md`. The fresh NASA HTML was 265,616 UTF-8 bytes before canonical extraction. The long NASA source is independently fetched by validators; digests describe the observed full canonical source and do not claim equality across validators.

### Exact balances (wei)

| Stage | Wallet A | Wallet B | Current Bonds |
|---|---:|---:|---:|
| start | 12000999999999999956 | 0 | 0 |
| two-wallet-before | 12000999999999999956 | 0 | 0 |
| funding-before | 10000999999999999956 | 0 | 2000000000000000000 |
| funding-after | 8000999999999999956 | 2000000000000000000 | 2000000000000000000 |
| two-wallet-settled | 8000999999999999956 | 0 | 4000000000000000000 |
| label-change-before | 8000999999999999956 | 0 | 4000000000000000000 |
| extra-independent-deposit-before | 2000999999999999956 | 0 | 10000000000000000000 |
| extra-independent-deposit-after | 4000999999999999956 | 0 | 8000000000000000000 |
| extra-independent-bond-before | 4000999999999999956 | 0 | 8000000000000000000 |
| extra-independent-bond-after | 6000999999999999956 | 0 | 6000000000000000000 |
| extra-change-bond-before | 6000999999999999956 | 0 | 6000000000000000000 |
| extra-change-bond-after | 8000999999999999956 | 0 | 4000000000000000000 |
| finish | 12000999999999999956 | 0 | 0 |

A → B funding: `0xc4fd62ee04620325b501cb5927722a2c724062dbd0c27ed810e4a82578e371d8`, 2 GEN. Measured funding fee: 0 wei. Parent withdrawals, native credit children and verification callbacks all require FINALIZED success. Outcome-specific balance deltas and escrow received-minus-verified-paid totals are checked by `verify:network`.

Final escrow accounting: wallet A 12000999999999999956 wei; Bonds 0 wei; received 10000000000000000000 wei, verified paid 10000000000000000000 wei. Bonds balance equals received minus verified paid.

## Historical deployment recovery

Both old deployments are absent from Portal contract fields. Their immutable addresses are retained solely in archived diagnosis and recovery records.

v2 recovery journal: [docs/legacy/v2/cleanup/journal.json](legacy/v2/cleanup/journal.json). Complete: True.

| Recovery step | Hash |
|---|---|
| climate-quota-2-release | [0x79dc2fb993004d1aa300f4ce71a9753b0c2b0ea0d9b82f2661b4ddffce234f32](https://explorer-studio.genlayer.com/transactions/0x79dc2fb993004d1aa300f4ce71a9753b0c2b0ea0d9b82f2661b4ddffce234f32) |
| climate-quota-2-release-child-0 | [0x79427538f8d52c5eeab260a0a8c757d42f961406dc1c5b0071fa24adadf16a10](https://explorer-studio.genlayer.com/transactions/0x79427538f8d52c5eeab260a0a8c757d42f961406dc1c5b0071fa24adadf16a10) |
| climate-quota-2-release-child-0-child-0 | [0xb47e12e933a442a66ef6dfd75e8843afab02e41e712a9760ea8e48cec586928b](https://explorer-studio.genlayer.com/transactions/0xb47e12e933a442a66ef6dfd75e8843afab02e41e712a9760ea8e48cec586928b) |
| climate-quota-2-withdraw | [0x54cb144140469de1bdd1054ad442a2504f5439df50038cebb7116caaf2b73339](https://explorer-studio.genlayer.com/transactions/0x54cb144140469de1bdd1054ad442a2504f5439df50038cebb7116caaf2b73339) |
| climate-quota-2-withdraw-child-0 | [0x2f2bc23da3d8784ef4ec903fd0cd4c563455ab95f1bf54796d0ce6325cf5bb7d](https://explorer-studio.genlayer.com/transactions/0x2f2bc23da3d8784ef4ec903fd0cd4c563455ab95f1bf54796d0ce6325cf5bb7d) |
| climate-quota-2-verify | [0xcfe93586de77a1dde678850875cdf910b43977b1bc93899fc67a3d6c033ce199](https://explorer-studio.genlayer.com/transactions/0xcfe93586de77a1dde678850875cdf910b43977b1bc93899fc67a3d6c033ce199) |
| climate-quota-2-verify-child-0 | [0x4787c355a2990271e5811f01fed5c001897cc7821bcb261129006a3cb6b7b6a0](https://explorer-studio.genlayer.com/transactions/0x4787c355a2990271e5811f01fed5c001897cc7821bcb261129006a3cb6b7b6a0) |
| climate-quota-3-release | [0x7685e89429144804d80fdf0cdaa18bc7a372070cff93a2e9b8ea8019d90191a9](https://explorer-studio.genlayer.com/transactions/0x7685e89429144804d80fdf0cdaa18bc7a372070cff93a2e9b8ea8019d90191a9) |
| climate-quota-3-release-child-0 | [0x6dcc82bf8c737a9f8e27e0bdb292f944310dc3716a92babdd21691ac0a77656c](https://explorer-studio.genlayer.com/transactions/0x6dcc82bf8c737a9f8e27e0bdb292f944310dc3716a92babdd21691ac0a77656c) |
| climate-quota-3-release-child-0-child-0 | [0x2512c57ac78a5709f1e602963acfccc8e7569b485cb99920bad96cd77324b8bb](https://explorer-studio.genlayer.com/transactions/0x2512c57ac78a5709f1e602963acfccc8e7569b485cb99920bad96cd77324b8bb) |
| climate-quota-3-withdraw | [0x5aea13a36abcb71917b5638fe3eea0ad56b5be93eec52e172d01fe4e6bd5ee1f](https://explorer-studio.genlayer.com/transactions/0x5aea13a36abcb71917b5638fe3eea0ad56b5be93eec52e172d01fe4e6bd5ee1f) |
| climate-quota-3-withdraw-child-0 | [0xfbba5716a970cd7b2fecac1e62682a2f69130f286a0a8d627ac55dff7f46f16d](https://explorer-studio.genlayer.com/transactions/0xfbba5716a970cd7b2fecac1e62682a2f69130f286a0a8d627ac55dff7f46f16d) |
| climate-quota-3-verify | [0x62d3d34b177f29fbffec6ea2991a0523bc688e079da92090a378f488651ebafa](https://explorer-studio.genlayer.com/transactions/0x62d3d34b177f29fbffec6ea2991a0523bc688e079da92090a378f488651ebafa) |
| climate-quota-3-verify-child-0 | [0x64b4300a5534c9977842d52e105dda37e136e2d04b7d62dcb1ca7ee38d420821](https://explorer-studio.genlayer.com/transactions/0x64b4300a5534c9977842d52e105dda37e136e2d04b7d62dcb1ca7ee38d420821) |
| temperature-update-2025-release | [0x66bd822d17c1323f6de421e9330908a5c8baf38028f7c84b915c73f852f26b64](https://explorer-studio.genlayer.com/transactions/0x66bd822d17c1323f6de421e9330908a5c8baf38028f7c84b915c73f852f26b64) |
| temperature-update-2025-release-child-0 | [0x93c42f4c11f858cfb6c773fd642ad43ee79a12f9568b39becb6407b2e40d4707](https://explorer-studio.genlayer.com/transactions/0x93c42f4c11f858cfb6c773fd642ad43ee79a12f9568b39becb6407b2e40d4707) |
| temperature-update-2025-release-child-0-child-0 | [0xa2cf31a4f84e56821bbd8af96c65ccf452724f4c4810b22769db5b44537f815c](https://explorer-studio.genlayer.com/transactions/0xa2cf31a4f84e56821bbd8af96c65ccf452724f4c4810b22769db5b44537f815c) |
| temperature-update-2025-withdraw | [0x0cf6808f13e8fa41dc0e6004cd3445f9b885b74bf820bd15e2f8994e30747cb7](https://explorer-studio.genlayer.com/transactions/0x0cf6808f13e8fa41dc0e6004cd3445f9b885b74bf820bd15e2f8994e30747cb7) |
| temperature-update-2025-withdraw-child-0 | [0x2db7dc6f8ee8ff6d40f22ce82f888150938c159ce9c6c4acbd93a72aeb6e30ca](https://explorer-studio.genlayer.com/transactions/0x2db7dc6f8ee8ff6d40f22ce82f888150938c159ce9c6c4acbd93a72aeb6e30ca) |
| temperature-update-2025-verify | [0x593a09040b18c9ae3cf577a7213dfa6b8c5b01ef199243a7234f02b9af8c1877](https://explorer-studio.genlayer.com/transactions/0x593a09040b18c9ae3cf577a7213dfa6b8c5b01ef199243a7234f02b9af8c1877) |
| temperature-update-2025-verify-child-0 | [0xf06c4c9e70b0432ff16e101dca9370ed609ec0f94c6b11997ce3c7c2a7ca457a](https://explorer-studio.genlayer.com/transactions/0xf06c4c9e70b0432ff16e101dca9370ed609ec0f94c6b11997ce3c7c2a7ca457a) |
| independent-climate-appeal-release | [0x0928ceeb873378181651cef24eda933366288eb035c195fa20219e816728f4ec](https://explorer-studio.genlayer.com/transactions/0x0928ceeb873378181651cef24eda933366288eb035c195fa20219e816728f4ec) |
| independent-climate-appeal-release-child-0 | [0xce3f8ca9b0f4d46d2bde51984550ad0daad99c13451add8a2febea9231287e98](https://explorer-studio.genlayer.com/transactions/0xce3f8ca9b0f4d46d2bde51984550ad0daad99c13451add8a2febea9231287e98) |
| independent-climate-appeal-release-child-0-child-0 | [0x57111795407da3808be1b295f6f983b4aedfb6991632ed3efb16f4c8d3aa5f1c](https://explorer-studio.genlayer.com/transactions/0x57111795407da3808be1b295f6f983b4aedfb6991632ed3efb16f4c8d3aa5f1c) |
| independent-climate-appeal-withdraw | [0x218a415fab9e05dfb1e22a0a06ec26904c2ef726dd99904030607016ab717119](https://explorer-studio.genlayer.com/transactions/0x218a415fab9e05dfb1e22a0a06ec26904c2ef726dd99904030607016ab717119) |
| independent-climate-appeal-withdraw-child-0 | [0xafe3990b005c297f587d38e11ddcec18894c6ec9736314a013a42dcbd5a72509](https://explorer-studio.genlayer.com/transactions/0xafe3990b005c297f587d38e11ddcec18894c6ec9736314a013a42dcbd5a72509) |
| independent-climate-appeal-verify | [0xb04600639902d4755a74bca3fb197d5052aec98ad41cc303ab38f8dfd64f0993](https://explorer-studio.genlayer.com/transactions/0xb04600639902d4755a74bca3fb197d5052aec98ad41cc303ab38f8dfd64f0993) |
| independent-climate-appeal-verify-child-0 | [0xa19b4805fc5ba1e430b80083c5cf5155ddb8e8ffaf7b2032138d3b6ac08d4642](https://explorer-studio.genlayer.com/transactions/0xa19b4805fc5ba1e430b80083c5cf5155ddb8e8ffaf7b2032138d3b6ac08d4642) |

Exact historical start/end: `{"wallet": "4000999999999999956", "bonds": "8000000000000000000"}` → `{"wallet": "12000999999999999956", "bonds": "0"}`. Four 2-GEN verified credits recover eight GEN; the legacy escrow is zero.

V1 recovery remains pending real maturity on 14 October 2026 (Africa/Lagos): climate-record 20:40:31, open-question 20:49:10, climate-quota-2 21:12:01 and climate-quota-3 21:15:14. The eight GEN cannot be withdrawn earlier. This future cleanup is not a completed live result. A one-time follow-up, `footnote-v1-bond-recovery`, is scheduled for 14 October at 21:16 Africa/Lagos, after the last deadline.

## Tests and verification

107 direct tests passed; 8 inapplicable scenario combinations skipped. Eleven TypeScript tests passed, including four wallet connection regressions with a mock provider. The wallet fix prevents overlapping permission requests and provides pending-request/cancellation recovery; desktop/mobile checks use controlled fixtures and make no live wallet writes. All four GenVM checks passed. Direct tests mock cross-contract calls, LLM/web content and native delivery; actual StudioNet receipts prove the live money path separately. Typecheck, lint, production build, network/link checks and desktop/mobile history checks are recorded in TEST_MATRIX and verification artifacts.

## Still test-only or unproven

- Forced version-drift cancellation and adversarial callback failures/replays remain direct-test-only.
- Same-URL publisher correction in /replay remains test-only. The live recheck adds an existing credible source; it does not claim a publisher edited or newly published that page.
- Timeout cancel_stale is proven on archived v2; it has not been repeated on this deployment.

The same-URL publisher correction in `/replay` remains explicitly mocked. Forced version drift, callback replay and outage recovery remain direct-test-only. A source occurring on an allowlisted host does not guarantee its truth. The Portal has not been submitted.
