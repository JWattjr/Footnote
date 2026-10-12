# Live proof manifest

StudioNet 61999, generation 2. Finality and successful execution are verified separately. Raw receipts are in `docs/proofs`; `public/deployment.json` is the persisted transaction journal. The network verifier is read-only.

Timing disclosure: the public demo deployment uses a 15-minute appeal window; production default is 72 hours. Demo cancellation grace is 10 minutes and bond release delay is 15 minutes. Production defaults are 24 hours for grace and 72 hours for bond release. All windows are constructor parameters bounded to five minutes–30 days. Live deadlines use actual chain time; no time travel is used.

The first immutable deployment and its original held bonds are archived under `docs/legacy/v1`. An unfunded superseded deployment is separately recorded under `docs/legacy/v2-unfunded-attempt`; it was replaced before any proof stake.

## Contracts

| Contract | Address |
|---|---|
| notes | [0xA71d317f87AAa68287901bAF1C6210F34AAD3675](https://explorer-studio.genlayer.com/contracts/0xA71d317f87AAa68287901bAF1C6210F34AAD3675) |
| bonds | [0x55CE2f217257e9CB94C83954ff635c5131Ef71ba](https://explorer-studio.genlayer.com/contracts/0x55CE2f217257e9CB94C83954ff635c5131Ef71ba) |
| recheck | [0x24AE6019820999664F95085e0775Cfe6968BB082](https://explorer-studio.genlayer.com/contracts/0x24AE6019820999664F95085e0775Cfe6968BB082) |
| appeals | [0x45FC5215210E8D7A856cC630923a26b216cD9565](https://explorer-studio.genlayer.com/contracts/0x45FC5215210E8D7A856cC630923a26b216cD9565) |

## Every live transaction

| Step | Hash | Evidence |
|---|---|---|
| deploy-notes | [0xfb6e3f9287d0be8a75387a2edbf288d365dc3a81fbaec8660c71f1b468e267e5](https://explorer-studio.genlayer.com/transactions/0xfb6e3f9287d0be8a75387a2edbf288d365dc3a81fbaec8660c71f1b468e267e5) | FINALIZED, result=6, leader execution SUCCESS |
| deploy-bonds | [0x683ff13b9e5a895f4e274b5a11b8e424d692e56f994cd12884fd85dfbd0ed581](https://explorer-studio.genlayer.com/transactions/0x683ff13b9e5a895f4e274b5a11b8e424d692e56f994cd12884fd85dfbd0ed581) | FINALIZED, result=6, leader execution SUCCESS |
| deploy-recheck | [0x6401098f4af4b7982e14ddfd85d1e675df564935b7a992039528f68674dd419c](https://explorer-studio.genlayer.com/transactions/0x6401098f4af4b7982e14ddfd85d1e675df564935b7a992039528f68674dd419c) | FINALIZED, result=6, leader execution SUCCESS |
| deploy-appeals | [0x64376e42b9009068aad03df35f445ab103e00c015da65f17c8f52811eb9d51c6](https://explorer-studio.genlayer.com/transactions/0x64376e42b9009068aad03df35f445ab103e00c015da65f17c8f52811eb9d51c6) | FINALIZED, result=6, leader execution SUCCESS |
| wire-bonds | [0xa09a34639430b79a2d8da568dda41a6a5138e5bd8c3bac057b5ef98cbe872051](https://explorer-studio.genlayer.com/transactions/0xa09a34639430b79a2d8da568dda41a6a5138e5bd8c3bac057b5ef98cbe872051) | FINALIZED, result=6, leader execution SUCCESS |
| wire-notes | [0x308db8d290c3ab61a55c41c310fcac636790ce43d2d8ea7a7027f60d3d690103](https://explorer-studio.genlayer.com/transactions/0x308db8d290c3ab61a55c41c310fcac636790ce43d2d8ea7a7027f60d3d690103) | FINALIZED, result=6, leader execution SUCCESS |
| supported-stake | [0x33db031a4dbb811288be6c0763b2c13a4b48f4d727286985269cca0863c242d6](https://explorer-studio.genlayer.com/transactions/0x33db031a4dbb811288be6c0763b2c13a4b48f4d727286985269cca0863c242d6) | FINALIZED, result=6, leader execution SUCCESS |
| supported-stake-child-0 | [0xa2f92fe3293e656817f5ce1fbb2b9d255819d98f5990dec982a320fbd27a57ff](https://explorer-studio.genlayer.com/transactions/0xa2f92fe3293e656817f5ce1fbb2b9d255819d98f5990dec982a320fbd27a57ff) | FINALIZED, result=6, leader execution SUCCESS |
| supported-note | [0xc5c95748986bec0fec19a4cde0bfeade107673fbfa92ed61b43ef2f90292e2c4](https://explorer-studio.genlayer.com/transactions/0xc5c95748986bec0fec19a4cde0bfeade107673fbfa92ed61b43ef2f90292e2c4) | FINALIZED, result=6, leader execution SUCCESS |
| supported-note-child-0 | [0xabc09fef52eda346bc7bdbd9457ef85e843cbe706d0cf6ba2ce524c25376f6cf](https://explorer-studio.genlayer.com/transactions/0xabc09fef52eda346bc7bdbd9457ef85e843cbe706d0cf6ba2ce524c25376f6cf) | FINALIZED, result=6, leader execution SUCCESS |
| supported-fund-appeal | [0xfa0ab7ef3c0b60b434dbe01302cb50d36833677d3a870a44d7b670efcd923e30](https://explorer-studio.genlayer.com/transactions/0xfa0ab7ef3c0b60b434dbe01302cb50d36833677d3a870a44d7b670efcd923e30) | FINALIZED, result=6, leader execution SUCCESS |
| supported-fund-appeal-child-0 | [0x71b294f034d814b274b327882b610a7ed952d9e8e87c5510ce61d48e0f448615](https://explorer-studio.genlayer.com/transactions/0x71b294f034d814b274b327882b610a7ed952d9e8e87c5510ce61d48e0f448615) | FINALIZED, result=6, leader execution SUCCESS |
| supported-contest | [0xf952ccedd2f4e17ca31e2d6d7fbc067a02faee4eaea1cafcf37262b9547ad088](https://explorer-studio.genlayer.com/transactions/0xf952ccedd2f4e17ca31e2d6d7fbc067a02faee4eaea1cafcf37262b9547ad088) | FINALIZED, result=6, leader execution SUCCESS |
| supported-contest-child-0 | [0xe11c81035447da19cfb312e62bd6178b5dddbf533aed14d4e87fde599b5586e7](https://explorer-studio.genlayer.com/transactions/0xe11c81035447da19cfb312e62bd6178b5dddbf533aed14d4e87fde599b5586e7) | FINALIZED, result=6, leader execution SUCCESS |
| supported-contest-child-0-child-0 | [0x748d7f772305880cbf95b01a6ec863ff72bdc69dffb6c97736bc21ed74d4bb8b](https://explorer-studio.genlayer.com/transactions/0x748d7f772305880cbf95b01a6ec863ff72bdc69dffb6c97736bc21ed74d4bb8b) | FINALIZED, result=6, leader execution SUCCESS |
| supported-contest-child-0-child-0-child-0 | [0x6b0d3d8d122fd3094755487aab019875531df0ef206a6706473de059431d8872](https://explorer-studio.genlayer.com/transactions/0x6b0d3d8d122fd3094755487aab019875531df0ef206a6706473de059431d8872) | FINALIZED, result=6, leader execution SUCCESS |
| reject-open-recheck | [0xbd561da00cd21c05efced66501bd588084a5307bc7aad93f92f57fbede06f0f3](https://explorer-studio.genlayer.com/transactions/0xbd561da00cd21c05efced66501bd588084a5307bc7aad93f92f57fbede06f0f3) | FINALIZED expected pre-fetch rejection: [EXPECTED] note has an open appeal; recheck after it is decided |
| unsupported-stake | [0x38c1749872299abd4305ff40ae0c9619ebf5c0b43e1bc748300277a5fbedb2a3](https://explorer-studio.genlayer.com/transactions/0x38c1749872299abd4305ff40ae0c9619ebf5c0b43e1bc748300277a5fbedb2a3) | FINALIZED, result=6, leader execution SUCCESS |
| unsupported-stake-child-0 | [0x83740202af1e09b7e7890a33d0e992a46f16c18dd9cc48e34f5e66733a9002f3](https://explorer-studio.genlayer.com/transactions/0x83740202af1e09b7e7890a33d0e992a46f16c18dd9cc48e34f5e66733a9002f3) | FINALIZED, result=6, leader execution SUCCESS |
| unsupported-note | [0xdc6a2755679a2172277c04fdd98b8af765b71a57b96e5b6bc9c85795f7e278b7](https://explorer-studio.genlayer.com/transactions/0xdc6a2755679a2172277c04fdd98b8af765b71a57b96e5b6bc9c85795f7e278b7) | FINALIZED, result=6, leader execution SUCCESS |
| unsupported-note-child-0 | [0x90f7158dabe91272d1db467288ed6cfebdb2915fbc9b5368ffa68f66b5ec246e](https://explorer-studio.genlayer.com/transactions/0x90f7158dabe91272d1db467288ed6cfebdb2915fbc9b5368ffa68f66b5ec246e) | FINALIZED, result=6, leader execution SUCCESS |
| unsupported-fund-appeal | [0xc9cc1e8cd239c7467b371ee91a5ab546e4034e3ee3c79e2ad839d0f251e746ee](https://explorer-studio.genlayer.com/transactions/0xc9cc1e8cd239c7467b371ee91a5ab546e4034e3ee3c79e2ad839d0f251e746ee) | FINALIZED, result=6, leader execution SUCCESS |
| unsupported-fund-appeal-child-0 | [0xf28fa6fb7384b3312da10cca8e111ce08db47f4f53d655de89cbe2a31074732a](https://explorer-studio.genlayer.com/transactions/0xf28fa6fb7384b3312da10cca8e111ce08db47f4f53d655de89cbe2a31074732a) | FINALIZED, result=6, leader execution SUCCESS |
| unsupported-contest | [0x94e5c1a530c6102cbb772d4149505af65c24b68127165f95abb540af93cd5d56](https://explorer-studio.genlayer.com/transactions/0x94e5c1a530c6102cbb772d4149505af65c24b68127165f95abb540af93cd5d56) | FINALIZED, result=6, leader execution SUCCESS |
| unsupported-contest-child-0 | [0x04cb5d6901d579df09b1acd009435126eca3004a2bb8460cd46b5bcdb08c24d2](https://explorer-studio.genlayer.com/transactions/0x04cb5d6901d579df09b1acd009435126eca3004a2bb8460cd46b5bcdb08c24d2) | FINALIZED, result=6, leader execution SUCCESS |
| unsupported-contest-child-0-child-0 | [0x63e8b1a8971275c90bfde0d701a7c138ad0caee98e948ecf36277f0631caa7b3](https://explorer-studio.genlayer.com/transactions/0x63e8b1a8971275c90bfde0d701a7c138ad0caee98e948ecf36277f0631caa7b3) | FINALIZED, result=6, leader execution SUCCESS |
| unsupported-contest-child-0-child-0-child-0 | [0xcf832570d0d8cebf6dc7799735b576f147bc1903d0469206c99b2786d0e44b19](https://explorer-studio.genlayer.com/transactions/0xcf832570d0d8cebf6dc7799735b576f147bc1903d0469206c99b2786d0e44b19) | FINALIZED, result=6, leader execution SUCCESS |
| reject-host | [0x949f5e066ee7994d0dd6f25dcc1404cdbe63f653357516ac9411169c6cdbe249](https://explorer-studio.genlayer.com/transactions/0x949f5e066ee7994d0dd6f25dcc1404cdbe63f653357516ac9411169c6cdbe249) | FINALIZED expected pre-fetch rejection: source host is not allowed |
| supported-judge | [0x57034b40b28eeaa94e9a5dda8e5d9efd433fd88d407ffd86ae111325d574aa3c](https://explorer-studio.genlayer.com/transactions/0x57034b40b28eeaa94e9a5dda8e5d9efd433fd88d407ffd86ae111325d574aa3c) | FINALIZED, result=6, leader execution SUCCESS |
| supported-judge-child-0 | [0xb33ea05e9218962586332dfff7154e613b6e99fd50584bfbd8e31f9267329c9f](https://explorer-studio.genlayer.com/transactions/0xb33ea05e9218962586332dfff7154e613b6e99fd50584bfbd8e31f9267329c9f) | FINALIZED, result=6, leader execution SUCCESS |
| supported-settle | [0x9e1536eef620ac172295edcabbce36f8fdd977fcfdfcee51cbf9afce11d74e04](https://explorer-studio.genlayer.com/transactions/0x9e1536eef620ac172295edcabbce36f8fdd977fcfdfcee51cbf9afce11d74e04) | FINALIZED, result=6, leader execution SUCCESS |
| supported-settle-child-0 | [0x9da0f1d1bc382416b0efc929127aa485aa261c5b8a9ab6b7dabf27b9b8075e6f](https://explorer-studio.genlayer.com/transactions/0x9da0f1d1bc382416b0efc929127aa485aa261c5b8a9ab6b7dabf27b9b8075e6f) | FINALIZED, result=6, leader execution SUCCESS |
| supported-settle-child-0-child-0 | [0x19ba01ad2e735d9a38eb1936851b0b5cf665f021510546f4e4a5577e51bcbe18](https://explorer-studio.genlayer.com/transactions/0x19ba01ad2e735d9a38eb1936851b0b5cf665f021510546f4e4a5577e51bcbe18) | FINALIZED, result=6, leader execution SUCCESS |
| quota2-stake | [0xe11ac0e9e705b6583cf25465080fc0158b45cbff284e6223bea2ebe03b841f43](https://explorer-studio.genlayer.com/transactions/0xe11ac0e9e705b6583cf25465080fc0158b45cbff284e6223bea2ebe03b841f43) | FINALIZED, result=6, leader execution SUCCESS |
| quota2-stake-child-0 | [0x4bda125e913d4f8a631af08c050e49d90892f6732c9aa284c81efc6eb4bb8953](https://explorer-studio.genlayer.com/transactions/0x4bda125e913d4f8a631af08c050e49d90892f6732c9aa284c81efc6eb4bb8953) | FINALIZED, result=6, leader execution SUCCESS |
| quota2-note | [0x18f5a238ed0209916d0568c4728c7223c338165916aa3e578ca9d07ab16e6580](https://explorer-studio.genlayer.com/transactions/0x18f5a238ed0209916d0568c4728c7223c338165916aa3e578ca9d07ab16e6580) | FINALIZED, result=6, leader execution SUCCESS |
| quota2-note-child-0 | [0xd740839f8c060c4f71330e8605f125dbd184ec99f8ff68f3292055e9a79b551a](https://explorer-studio.genlayer.com/transactions/0xd740839f8c060c4f71330e8605f125dbd184ec99f8ff68f3292055e9a79b551a) | FINALIZED, result=6, leader execution SUCCESS |
| quota3-stake | [0x759eb9912100b1de88e0f1b7f7eaa541a2774af477c9939afa491c3da8547933](https://explorer-studio.genlayer.com/transactions/0x759eb9912100b1de88e0f1b7f7eaa541a2774af477c9939afa491c3da8547933) | FINALIZED, result=6, leader execution SUCCESS |
| quota3-stake-child-0 | [0x973ed5c0f53d7c9b40bd0ec8d34b02f0593e4246486687eda21733e4a6c88e8c](https://explorer-studio.genlayer.com/transactions/0x973ed5c0f53d7c9b40bd0ec8d34b02f0593e4246486687eda21733e4a6c88e8c) | FINALIZED, result=6, leader execution SUCCESS |
| quota3-note | [0xf93815aa6aa62d08389a1b330531560257576a65582ae250b6dcb01ad272085f](https://explorer-studio.genlayer.com/transactions/0xf93815aa6aa62d08389a1b330531560257576a65582ae250b6dcb01ad272085f) | FINALIZED, result=6, leader execution SUCCESS |
| quota3-note-child-0 | [0x67728df55e4f8890364bf69c83cc7bd264cb86eea367f707c27ea599899ec9af](https://explorer-studio.genlayer.com/transactions/0x67728df55e4f8890364bf69c83cc7bd264cb86eea367f707c27ea599899ec9af) | FINALIZED, result=6, leader execution SUCCESS |
| reject-quota | [0x27628d14260dbf8dba9df00205bc13fb958cb0ba6364c5f2e414043b7dada1f7](https://explorer-studio.genlayer.com/transactions/0x27628d14260dbf8dba9df00205bc13fb958cb0ba6364c5f2e414043b7dada1f7) | FINALIZED expected pre-fetch rejection: three notes per post per address quota |
| supported-withdraw-deposit | [0xbb24c6e3c4ac43489cccb4b870f1cc7d37ec5787701df0d5dec57c83ccc30c08](https://explorer-studio.genlayer.com/transactions/0xbb24c6e3c4ac43489cccb4b870f1cc7d37ec5787701df0d5dec57c83ccc30c08) | FINALIZED, result=6, leader execution SUCCESS |
| supported-withdraw-deposit-child-0 | [0x111e6b5deee41e34247c40aef480e7a5a3bbee1a5910af98b3e86f873b6d8ff1](https://explorer-studio.genlayer.com/transactions/0x111e6b5deee41e34247c40aef480e7a5a3bbee1a5910af98b3e86f873b6d8ff1) | FINALIZED native value_credited=true |
| supported-verify-deposit | [0x0b530796a36f7eb779a3e4ea4cf357d6f25cca6bd1a4e698007590747de5ab0c](https://explorer-studio.genlayer.com/transactions/0x0b530796a36f7eb779a3e4ea4cf357d6f25cca6bd1a4e698007590747de5ab0c) | FINALIZED, result=6, leader execution SUCCESS |
| supported-verify-deposit-child-0 | [0xf342f74b486338ed7325698a697c88861ab40d5dcc2d7b3e909a3d4582eb4d2f](https://explorer-studio.genlayer.com/transactions/0xf342f74b486338ed7325698a697c88861ab40d5dcc2d7b3e909a3d4582eb4d2f) | FINALIZED, result=6, leader execution SUCCESS |
| supported-release | [0xb8b4fda190c2879cc372f0f2c8dc3c1c4cf75db15f669c595c352420564fd4f2](https://explorer-studio.genlayer.com/transactions/0xb8b4fda190c2879cc372f0f2c8dc3c1c4cf75db15f669c595c352420564fd4f2) | FINALIZED, result=6, leader execution SUCCESS |
| supported-release-child-0 | [0x7f04d35dc4d23ab418ce7ae79954e07cbc4ef267e371c00e2129ff4e47b96691](https://explorer-studio.genlayer.com/transactions/0x7f04d35dc4d23ab418ce7ae79954e07cbc4ef267e371c00e2129ff4e47b96691) | FINALIZED, result=6, leader execution SUCCESS |
| supported-release-child-0-child-0 | [0xe9e01d0dddb639a8e5d83ac4d51d9527a457fe008714518a5ddea76bc2a837b7](https://explorer-studio.genlayer.com/transactions/0xe9e01d0dddb639a8e5d83ac4d51d9527a457fe008714518a5ddea76bc2a837b7) | FINALIZED, result=6, leader execution SUCCESS |
| supported-withdraw-bond | [0x494e31cf11e9852b7c4991849c5d266a42837ff6b631b392cfe933a703cb7367](https://explorer-studio.genlayer.com/transactions/0x494e31cf11e9852b7c4991849c5d266a42837ff6b631b392cfe933a703cb7367) | FINALIZED, result=6, leader execution SUCCESS |
| supported-withdraw-bond-child-0 | [0xac5860dd66dbc521f53fd65fa030a10168d8d054861910ac58c7f5b979cf881a](https://explorer-studio.genlayer.com/transactions/0xac5860dd66dbc521f53fd65fa030a10168d8d054861910ac58c7f5b979cf881a) | FINALIZED native value_credited=true |
| supported-verify-bond | [0x2c8d23316f0b365eb66110d602836692730fb0e35d7c06f716682ebe240d17c7](https://explorer-studio.genlayer.com/transactions/0x2c8d23316f0b365eb66110d602836692730fb0e35d7c06f716682ebe240d17c7) | FINALIZED, result=6, leader execution SUCCESS |
| supported-verify-bond-child-0 | [0x0a60e2cde1cfcb1ed6f0129dd6afef5388225e622b69de4369895ff110c19ba3](https://explorer-studio.genlayer.com/transactions/0x0a60e2cde1cfcb1ed6f0129dd6afef5388225e622b69de4369895ff110c19ba3) | FINALIZED, result=6, leader execution SUCCESS |
| unsupported-cancel-stale | [0x772ffbd700b795e021d3b771730acd63e9eba6657b7108b3dad16a1f7ac03446](https://explorer-studio.genlayer.com/transactions/0x772ffbd700b795e021d3b771730acd63e9eba6657b7108b3dad16a1f7ac03446) | FINALIZED, result=6, leader execution SUCCESS |
| unsupported-cancel-stale-child-0 | [0x0a099718a7d9568102650eb2d87fbc51046a0cd92553b359dd4e9d0e9d92b12f](https://explorer-studio.genlayer.com/transactions/0x0a099718a7d9568102650eb2d87fbc51046a0cd92553b359dd4e9d0e9d92b12f) | FINALIZED, result=6, leader execution SUCCESS |
| unsupported-cancel-stale-child-0-child-0 | [0x3c6b2137accbdbdeeaed20d3a7efcc3b03708322dbbb8ca1f4c61ebec595ee47](https://explorer-studio.genlayer.com/transactions/0x3c6b2137accbdbdeeaed20d3a7efcc3b03708322dbbb8ca1f4c61ebec595ee47) | FINALIZED, result=6, leader execution SUCCESS |
| unsupported-cancel-stale-child-0-child-0-child-0 | [0x88f614a07245ad7750902ea0f4befa03f4c5206062dcff12b2471bd2a62d1de4](https://explorer-studio.genlayer.com/transactions/0x88f614a07245ad7750902ea0f4befa03f4c5206062dcff12b2471bd2a62d1de4) | FINALIZED, result=6, leader execution SUCCESS |
| unsupported-cancel-stale-child-0-child-0-child-0-child-0 | [0xb9f4efde9093af16be39858bd98926c942ee8fee905789312d263d36e95814f5](https://explorer-studio.genlayer.com/transactions/0xb9f4efde9093af16be39858bd98926c942ee8fee905789312d263d36e95814f5) | FINALIZED, result=6, leader execution SUCCESS |
| unsupported-cancel-stale-child-0-child-0-child-0-child-0-child-0 | [0x7ea1c7c11351ca11ffc0f0ca42917d97f2326add14f554ecc8b6c12ec8711c62](https://explorer-studio.genlayer.com/transactions/0x7ea1c7c11351ca11ffc0f0ca42917d97f2326add14f554ecc8b6c12ec8711c62) | FINALIZED, result=6, leader execution SUCCESS |
| unsupported-withdraw-deposit | [0xc3eaa8c8cfb13c21f238945d696648f8b19d539b4f55875a94fb33c287ddd297](https://explorer-studio.genlayer.com/transactions/0xc3eaa8c8cfb13c21f238945d696648f8b19d539b4f55875a94fb33c287ddd297) | FINALIZED, result=6, leader execution SUCCESS |
| unsupported-withdraw-deposit-child-0 | [0x7f958a4c0d34a0db27a399aa0d22e1730e6bf693a2a56038d12e60b5de1024b1](https://explorer-studio.genlayer.com/transactions/0x7f958a4c0d34a0db27a399aa0d22e1730e6bf693a2a56038d12e60b5de1024b1) | FINALIZED native value_credited=true |
| unsupported-verify-deposit | [0x0c5974b56c4474e91ca9642df1cdd342c37bda109aee62119d06a755896b89e4](https://explorer-studio.genlayer.com/transactions/0x0c5974b56c4474e91ca9642df1cdd342c37bda109aee62119d06a755896b89e4) | FINALIZED, result=6, leader execution SUCCESS |
| unsupported-verify-deposit-child-0 | [0x7980cbb1303b45891e7254b8eb849782daa741e2ef479e25a1cdf6f3ce7de64b](https://explorer-studio.genlayer.com/transactions/0x7980cbb1303b45891e7254b8eb849782daa741e2ef479e25a1cdf6f3ce7de64b) | FINALIZED, result=6, leader execution SUCCESS |
| unsupported-release | [0x2354913ada6a50b7c3887fe83acbd4453eac9cf7cd083de083f89ed01742fdaf](https://explorer-studio.genlayer.com/transactions/0x2354913ada6a50b7c3887fe83acbd4453eac9cf7cd083de083f89ed01742fdaf) | FINALIZED, result=6, leader execution SUCCESS |
| unsupported-release-child-0 | [0x9e1d7906a3a18b32b9074b61d26ce798aae1c6d17bed00808010e36e0aa7a150](https://explorer-studio.genlayer.com/transactions/0x9e1d7906a3a18b32b9074b61d26ce798aae1c6d17bed00808010e36e0aa7a150) | FINALIZED, result=6, leader execution SUCCESS |
| unsupported-release-child-0-child-0 | [0x0cf40341e3fdbdb64e5fe5a04c458554875478081b9c7e04e3504c72dbabab37](https://explorer-studio.genlayer.com/transactions/0x0cf40341e3fdbdb64e5fe5a04c458554875478081b9c7e04e3504c72dbabab37) | FINALIZED, result=6, leader execution SUCCESS |
| unsupported-withdraw-bond | [0x33dc451ae2e01c29212763e4768d5aa4c2e65f30f41032b7646cc421e085a31c](https://explorer-studio.genlayer.com/transactions/0x33dc451ae2e01c29212763e4768d5aa4c2e65f30f41032b7646cc421e085a31c) | FINALIZED, result=6, leader execution SUCCESS |
| unsupported-withdraw-bond-child-0 | [0x4999e79840f94b85658352937749307d0d3469a2bbc9ae590292e10d7309324d](https://explorer-studio.genlayer.com/transactions/0x4999e79840f94b85658352937749307d0d3469a2bbc9ae590292e10d7309324d) | FINALIZED native value_credited=true |
| unsupported-verify-bond | [0xc2f56e38d6103c66598c581b5759550b87bf3c4cff81af34c86046ae973fefcb](https://explorer-studio.genlayer.com/transactions/0xc2f56e38d6103c66598c581b5759550b87bf3c4cff81af34c86046ae973fefcb) | FINALIZED, result=6, leader execution SUCCESS |
| unsupported-verify-bond-child-0 | [0x3eb6f24bbce51f97342e4aa1700626c19c7d48e6c03299731188d672c51b10a3](https://explorer-studio.genlayer.com/transactions/0x3eb6f24bbce51f97342e4aa1700626c19c7d48e6c03299731188d672c51b10a3) | FINALIZED, result=6, leader execution SUCCESS |

## Matched state and source preflight

- `config`: finalized configuration {"appeal_window_seconds": 900, "appeals": "0x45FC5215210E8D7A856cC630923a26b216cD9565", "bonds": "0x55CE2f217257e9CB94C83954ff635c5131Ef71ba", "hosts": ["apnews.com", "climate.copernicus.eu", "en.wikipedia.org", "europepmc.org", "science.nasa.gov", "svs.gsfc.nasa.gov", "www.bbc.com", "www.ebi.ac.uk", "www.gov.uk", "www.justice.gov", "www.nasa.gov", "www.ncei.noaa.gov", "www.noaa.gov", "www.reuters.com", "www.theguardian.com"], "recheck": "0x24AE6019820999664F95085e0775Cfe6968BB082", "wired": true}.
- `bondsConfig`: finalized configuration {"appeal_window_seconds": 900, "release_delay_seconds": 900}.
- `appealsConfig`: finalized configuration {"appeal_window_seconds": 900, "cancel_grace_seconds": 600}.
- `climate-record`: active, version 1, SUPPORTED / NOT_RAGE_BAIT; open quota False; actual appeal deadline 2026-10-11T22:19:43+00:00.
- `climate-record:appeal`: UPHELD, settled; deposit 2000000000000000000 wei.
- `open-question`: active, version 1, UNSUPPORTED / NOT_RAGE_BAIT; open quota False; actual appeal deadline 2026-10-11T22:27:50+00:00.
- `open-question:appeal`: CANCELLED, CANCELLED; deposit 2000000000000000000 wei; cancellation reason JUDGING_TIMEOUT.
- `climate-quota-2`: active, version 1, SUPPORTED / NOT_RAGE_BAIT; open quota True; actual appeal deadline 2026-10-11T22:40:24+00:00.
- `climate-quota-3`: active, version 1, SUPPORTED / NOT_RAGE_BAIT; open quota True; actual appeal deadline 2026-10-11T22:43:10+00:00.
- Quota read: {"open": 2, "per_post": 3}; fourth same-post creation rejected before fetch.
- `deposit:climate-record:1:balances`: before 999999999999998, after 2000999999999999998, exact native-credit delta 2000000000000000000 wei.
- `deposit:climate-record:1`: paid; native child `0x111e6b5deee41e34247c40aef480e7a5a3bbee1a5910af98b3e86f873b6d8ff1`, amount 2000000000000000000 wei, attempt 1.
- `bond:climate-record:balances`: before 2000999999999999998, after 4000999999999999998, exact native-credit delta 2000000000000000000 wei.
- `bond:climate-record`: paid; native child `0xac5860dd66dbc521f53fd65fa030a10168d8d054861910ac58c7f5b979cf881a`, amount 2000000000000000000 wei, attempt 1.
- `deposit:open-question:1:balances`: before 4000999999999999998, after 6000999999999999998, exact native-credit delta 2000000000000000000 wei.
- `deposit:open-question:1`: paid; native child `0x7f958a4c0d34a0db27a399aa0d22e1730e6bf693a2a56038d12e60b5de1024b1`, amount 2000000000000000000 wei, attempt 1.
- `bond:open-question:balances`: before 6000999999999999998, after 8000999999999999998, exact native-credit delta 2000000000000000000 wei.
- `bond:open-question`: paid; native child `0x4999e79840f94b85658352937749307d0d3469a2bbc9ae590292e10d7309324d`, amount 2000000000000000000 wei, attempt 1.

Exact final accounting: wallet `0xdb433ff614bdd1ece21aa97221c3e0a7ecf79c92` has 8000999999999999998 wei; Bonds has 4000000000000000000 wei. Escrow received 12000000000000000000 wei and verified paid 8000000000000000000 wei. Bonds balance equals received minus verified paid.

Each real live note uses three identical canonical source digests and exact quotation preflight. Fresh inputs are in [live-inputs.json](proofs/live-inputs.json). Validators independently ground contract citations. The public posts are examples; high virality is not claimed.

## Tests and verification

80 direct tests passed; 8 inapplicable parameter combinations skipped. Seven TypeScript domain tests passed. Direct mode executes one contract per process, with mocked cross-contract views, LLM/web content and native delivery. Forced version drift, callback failure/replay and recipient balances are tested under those boundaries. GenVM lint/validation passed for all four contracts. See TEST_MATRIX.md and the saved verification reports for frontend/build/live evidence. All 70 recorded transactions and callbacks passed read-only network verification. All 80 package links returned HTTP 200, with portal field lengths 145/180, 865/1000 and 357/500. The Vercel production build and desktop/mobile production Chrome checks passed on 12 October after the approval-review usage limit reset; the contract proof completed on 11 October. Production evidence is saved in `proofs/production-verification.json` and `proofs/production-browser-report.json`.

## Still test-only or unproven live

- Forced version-drift cancellation, adversarial callback failures/replays and distinct recipient accounting are direct-test-only.
- The changed-source evidence-label replay is test-only; no real publisher correction is claimed.
- Quota-note writer bonds remain unwithdrawn: climate-quota-2 (2000000000000000000 wei; mature=true, open appeal=false); climate-quota-3 (2000000000000000000 wei; mature=true, open appeal=false). The core supported and cancelled-note bonds are withdrawn separately.

The same configured wallet is writer and appellant in the live proof; direct tests cover distinct recipients. Same-URL source changes after exhausted inconclusive probes need a new correction URL. Native delivery depends on the protocol and is marked paid only after explicit credit verification. All fund-lock prevention, cancellation and callback recovery exits are listed in SECURITY_NOTES.md.

The Portal has not been submitted. The `/replay` correction demonstration is explicitly test-only.
