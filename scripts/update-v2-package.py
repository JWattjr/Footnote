import json, re
from pathlib import Path

DISCLOSURE='the public demo deployment uses a 15-minute appeal window; production default is 72 hours'
p=json.loads(Path('public/deployment.json').read_text(encoding='utf-8'))
old=json.loads(Path('docs/legacy/v1/deployment.json').read_text(encoding='utf-8'))
readme=Path('README.md').read_text(encoding='utf-8')
for key,address in p['contracts'].items():
    readme=readme.replace(old['contracts'][key],address)
    label={'notes':'Notes','bonds':'Bonds','recheck':'Recheck','appeals':'Appeals'}[key]
    readme=re.sub(r'(\| '+label+r' \| `)0x[a-fA-F0-9]{40}(`)', lambda m: m[1]+address+m[2], readme)
readme=readme.replace('during its 72-hour window','during its configured appeal window')
if DISCLOSURE not in readme:
    readme=readme.replace('## Deployed contracts', 'Timing disclosure: '+DISCLOSURE+'. The demo cancellation grace is 10 minutes and bond release delay is 15 minutes. Constructor defaults are 72 hours for appeals and bond release, and 24 hours for cancellation grace. Every window must be 5 minutes–30 days; bond release delay must cover the appeal window. Deadlines use real chain time.\n\nAppeal funding goes directly into Bonds before opening the appeal. Rechecks are rejected before fetching while an appeal is open. Anyone can cancel a stale version or an unjudged appeal after its deadline plus grace, recovering the full deposit through a verified pull withdrawal. Unused funding and stalled callbacks have recovery methods. The previous immutable deployment and its held writer bonds remain separately archived in `docs/legacy/v1`; the app now targets generation 2.\n\n## Deployed contracts')
Path('README.md').write_text(readme,encoding='utf-8')

sec=Path('docs/SECURITY_NOTES.md').read_text(encoding='utf-8')
sec=sec.replace('immutable 72-hour original deadline','immutable constructor-configured original deadline')
sec=sec.replace('A recheck/appeal race is fail-closed by version checks, but a stale paid appeal does not yet have an automated cancel/refund branch; avoid racing these operations in the public simulator demonstration. ', '')
section='''## Escrow liveness audit and fixed exits

Timing disclosure: DISCLOSURE. The demo cancellation grace is 10 minutes and bond release delay is 15 minutes; production defaults are 24 hours and 72 hours respectively. All three constructor windows require 300–2,592,000 seconds. Release delay must cover the appeal window.

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
| Cancel/refund/settlement callback replay | State guards and unique claim keys reject replayed cancellation, refund and settlement callbacks. A second cancel, judge after cancel, repeated close, and repeated withdrawal cannot allocate or pay twice. |

All recovery methods emit protected callbacks on `finalized`; callers cannot change recipients, amounts, deadlines or decisions. Recovery is permissionless; withdrawing remains recipient-only. Direct tests cover forced version drift, timeout boundaries, distinct writer/appellant allocations and exact modeled ledger balances. Cross-contract calls and native delivery are mocked in direct mode; live receipts establish actual StudioNet credit separately.

Native ledger delivery remains a protocol boundary. GenLayer documents that value on a failed emitted message is not automatically returned. This implementation avoids value-bearing contract-to-contract deposit forwarding. If a native withdrawal is explicitly uncredited, its verified claim remains retryable only after full unpaid backing is restored; it never appropriates another user's escrow. A protocol outage or lost native value requires protocol restoration before payment can complete. Receipt unavailability never marks a claim paid or enables a duplicate transfer. This is an external protocol dependency, not an administrative refund override.

'''.replace('DISCLOSURE',DISCLOSURE)
if '## Escrow liveness audit' not in sec: sec=sec.replace('## Remaining limitations', section+'## Remaining limitations')
Path('docs/SECURITY_NOTES.md').write_text(sec,encoding='utf-8')

matrix=Path('docs/TEST_MATRIX.md').read_text(encoding='utf-8').replace('45 direct tests','80 direct tests').replace('75 direct tests','80 direct tests').replace('4 inapplicable','8 inapplicable').replace('Four parameter combinations','Eight parameter combinations')
if 'test_cancel_stale_closes_once' not in matrix:
    matrix=matrix.replace('| URL checks,', '''| Recheck open appeal guard before web/model work | `test_open_appeal_recheck_guard_before_fetch` | Direct + live expected rejection |
| Recheck staging/finalization race preserves appealed version | `test_notes_rechecks_cannot_race_an_open_appeal` | Direct |
| Version drift and never-judged deadline + grace cancellation; replay/judge-after-cancel rejected | `test_cancel_stale_closes_once_and_rejects_replays` | Direct; live timeout if recorded |
| Exact full cancellation refund, writer release, appellant/writer/Bonds balances, no double payout | `test_cancel_exact_recipient_balances_and_writer_release` | Direct modeled native ledger |
| Missing activation, unused and reserved funding, callback resumption | Recovery tests in `test_recovery.py` | Direct |
| Production defaults, five-minute minimum, 30-day maximum and independent grace/release bounds | Constructor tests in `test_recovery.py` | 20 direct cases |
| URL checks,''')
Path('docs/TEST_MATRIX.md').write_text(matrix,encoding='utf-8')

fields=json.loads(Path('docs/submission/portal-fields.json').read_text(encoding='utf-8'))
fields['description']='Footnote adds source-grounded context to public Bluesky posts. GenLayer validators independently judge evidence (Supported, Contradicted, Unsupported, Misleading) and tone. Notes preserves versions; Recheck blocks open appeals before fetching; Appeals judges counter-evidence and cancels stale or timed-out appeals; Bonds holds deposits directly and uses receipt-verified pull withdrawals. Allegations use a stricter two-label rule; names, handles and post text stay off-chain. Reading needs no wallet. StudioNet is a simulator: '+DISCLOSURE+'. Demo cancellation grace is 10 minutes and bond release delay is 15 minutes. Production cancellation grace is 24 hours. Forced version-drift cancellation and source-change replay are test-only; finalized live receipts show the recorded lifecycle.'
fields['howTo'][3]='Choose Write a note: Stake bond then Publish note. To challenge, Fund appeal · 2 GEN then Contest note; inspect decision/cancellation and verified withdrawals.'
for key,address in p['contracts'].items(): fields['contractExplorerLinks'][key]='https://explorer-studio.genlayer.com/contracts/'+address
Path('docs/submission/portal-fields.json').write_text(json.dumps(fields,indent=2)+'\n',encoding='utf-8')
target='## Fixed deployment target\n\nStudioNet 61999, generation 2.\n\n| Contract | Address |\n|---|---|\n'+'\n'.join('| '+key+' | ['+address+'](https://explorer-studio.genlayer.com/contracts/'+address+') |' for key,address in p['contracts'].items())+'\n\n'
for filename in ('docs/SECURITY_NOTES.md','docs/TEST_MATRIX.md'):
    text=Path(filename).read_text(encoding='utf-8')
    text=re.sub(r'## Fixed deployment target\n.*?(?=\n## |\Z)', '', text, flags=re.S)
    text+='\n'+target
    Path(filename).write_text(text,encoding='utf-8')

desk=Path('components/desk.tsx').read_text(encoding='utf-8')
desk=desk.replace('<button disabled={!canAct} onClick={()=>void action(\'Contest note\')}>Contest note · 2 GEN</button>', '<button disabled={!canAct} onClick={()=>void action(\'Fund appeal\')}>Fund appeal · 2 GEN</button><button disabled={!canAct} onClick={()=>void action(\'Contest note\')}>Contest note</button>')
desk=desk.replace('Anyone can contest one note version once. An uncertain appeal returns the deposit.', 'First fund the deposit directly in Bonds, then contest after funding finalizes. One appeal per version. A cancelled or uncertain appeal refunds the deposit. Rechecks wait until the appeal closes.')
desk=desk.replace("['Release bond','Withdraw bond','Withdraw deposit']", "['Release bond','Withdraw bond','Withdraw deposit','Cancel stale appeal','Resume appeal','Resume deposit','Resume bond','Resume note','Refund unused funding','Resume funding','Withdraw unused funding']")
desk=desk.replace("['Verify bond withdrawal','Verify deposit withdrawal']", "['Verify bond withdrawal','Verify deposit withdrawal','Verify funding withdrawal']")
desk=desk.replace('key={a} disabled={!canAct}', 'key={a} disabled={!canManage}').replace('key={a} disabled={!canAct||', 'key={a} disabled={!canManage||')
desk=re.sub(r"(setVersion\(undefined\);setCounter\(''\);)(?:setAppealVersion\(''\);)*", r"\1setAppealVersion('');", desk)
desk=desk.replace("'Resume note','Refund unused funding'", "'Resume note','Resume bond verification','Resume deposit verification','Refund unused funding'")
desk=desk.replace("'Withdraw unused funding'].map", "'Withdraw unused funding','Resume funding verification'].map")
desk=desk.replace('<div><p>Writer bond: 2–20 simulated GEN.', '<div><label>Existing appeal version<input type="number" min={1} max={note.version} value={appealVersion||String(note.version)} onChange={e=>setAppealVersion(e.target.value)}/></label><p className="small">Use the original appealed version for judging, cancellation, settlement and deposit withdrawals.</p><p>Writer bond: 2–20 simulated GEN.')
Path('components/desk.tsx').write_text(desk,encoding='utf-8')
readme=Path('README.md').read_text(encoding='utf-8').replace('Deadlines use real chain time.', 'Deadlines use real chain time and run from the original writer stake; finalization consumes part of that window.')
Path('README.md').write_text(readme,encoding='utf-8')

arch=Path('docs/ARCHITECTURE.md').read_text(encoding='utf-8')
arch=arch.replace('Browser -->|counter-evidence + deposit| Appeals','Browser -->|fund appeal deposit| Bonds\n  Browser -->|counter-evidence + finalized funding| Appeals').replace('Appeals -->|finalized deposit forwarding| Bonds','Appeals -->|finalized state-only activation| Bonds')
arch=arch.replace('An appeal deposits at least 2 GEN, snapshots the version, validates sources, and reserves its unique `note:version` key. A protected callback forwards the deposit to Bonds; Bonds checks the appeal binding and exact value and marks it held only after its own finality callback.', 'A wallet first funds at least 2 GEN directly in Bonds. Nonpayable contest snapshots the version and finalized funding, validates sources, and reserves its unique `note:version` key. Protected state-only callbacks activate and hold that funding. Unused funding is refundable without opening an appeal.')
arch=arch.replace('A stale appeal following a racing recheck requires operational resolution; there is no privileged override in this version.', 'Recheck rejects open appeals before fetching and Notes checks again during staging/finalization. Anyone can cancel a mismatched version or an unjudged appeal after deadline plus grace. Finalized cancellation refunds its deposit and closes the appeal; writer release then follows the normal rules. See SECURITY_NOTES.md for every callback recovery exit.')
arch=arch.replace('finalized forwarded deposits','directly funded deposits').replace('after the original 72-hour window','after the configured real release delay')
if DISCLOSURE not in arch: arch+='\nTiming disclosure: '+DISCLOSURE+'. Demo grace: 10 minutes; bond delay: 15 minutes. Defaults: 24-hour grace and 72-hour bond delay. Constructor bounds: five minutes–30 days.\n'
Path('docs/ARCHITECTURE.md').write_text(arch,encoding='utf-8')
sec=Path('docs/SECURITY_NOTES.md').read_text(encoding='utf-8')
if '## Immutable legacy instance' not in sec:
    sec+='\n## Immutable legacy instance\n\nGeneration 1 cannot be patched or rewired. Its original eight simulated GEN of writer bonds remain in the old Bonds contract under the original 72-hour deadlines on 14 October; redeployment does not migrate those funds. The legacy contracts retain the confirmed stale-appeal defect. The public app and new proofs target the fixed generation 2 addresses only. Do not fund or open new appeals on generation 1. Its existing bonds still have their ordinary mature-release path if no appeal is open; see the archived exact addresses and state in `docs/legacy/v1/deployment.json`.\n'
if '| Refunded funding races appeal opening |' not in sec:
    sec=sec.replace('| Cancel/refund/settlement callback replay |', '| Refunded funding races appeal opening | Timeout/version cancellation recognizes the existing funding refund claim, marks its deposit settled, and closes the appeal without allocating a second refund. Pending refund finality resumes through `resume_funding`. |\n| Cancel/refund/settlement callback replay |')
Path('docs/SECURITY_NOTES.md').write_text(sec,encoding='utf-8')

tutorial=Path('docs/TUTORIAL.md').read_text(encoding='utf-8')
tutorial=tutorial.replace('immutable 72-hour deadline','immutable configured deadline')
tutorial=tutorial.replace('The same panel offers **Contest note · 2 GEN**. Anyone may appeal during the original 72-hour bond window; the app does not pretend to authenticate the post author as a wallet. An appeal reserves one `note:version` key and forwards its deposit to Bonds on finality.', 'The panel offers **Fund appeal · 2 GEN** followed by **Contest note**. First finalize funding directly in Bonds, then open the nonpayable appeal during the configured window. The app does not authenticate the post author as a wallet. An appeal reserves one `note:version` key and activates bound funding through state-only callbacks.')
tutorial=tutorial.replace('Avoid racing rechecks and funded appeals in this simulator release; the documented stale-version recovery limitation is not hidden behind an administrative override.', 'Rechecks reject open appeals before fetching. Anyone can use **Cancel stale appeal** when the version no longer matches, or an open appeal outlives its deadline plus grace. Cancellation refunds the full deposit, closes the appeal, and permits normal writer release. **Existing appeal version** selects the original version for recovery after version drift. Resume controls finish stalled callbacks; unused funding can be refunded and withdrawn without opening an appeal.')
tutorial=tutorial.replace('including the original-window bond withdrawal until its deadline actually passes', 'including any lifecycle steps still listed as unproven')
if '## Complete the deferred writer-bond proof' in tutorial:
    tutorial=tutorial.split('## Complete the deferred writer-bond proof')[0]+'## Wait for real maturity\n\nRun `$env:FOOTNOTE_CASE="supported"; ./scripts/deploy.ps1 -Step withdraw-bond` only after the actual release time and appeal closure. For an unjudged appeal, wait until its deadline plus grace, then use `cancel-stale`, `withdraw-deposit`, and `withdraw-bond`. Scripts persist each hash before polling and resume it after timeout. Never advance the live clock or resubmit a pending write.\n'
if DISCLOSURE not in tutorial: tutorial+='\nTiming disclosure: '+DISCLOSURE+'. Demo grace is 10 minutes and bond delay is 15 minutes. Production defaults are 24 hours and 72 hours respectively.\n'
Path('docs/TUTORIAL.md').write_text(tutorial,encoding='utf-8')
demo=Path('docs/DEMO.md').read_text(encoding='utf-8').replace('**Contest note · 2 GEN**','**Fund appeal · 2 GEN**, **Contest note**').replace('original 72-hour deadline','demo 15-minute deadline and the production 72-hour default').replace('State that the writer bond remains locked until 14 October.', 'Show the writer-bond claim and verified credit when recorded; otherwise identify it as unproven. Show live timeout cancellation only if its FINALIZED receipts are recorded.')
if DISCLOSURE not in demo: demo+='\nTiming disclosure: '+DISCLOSURE+'. Demo cancellation grace: 10 minutes; bond release delay: 15 minutes.\n'
Path('docs/DEMO.md').write_text(demo,encoding='utf-8')
print('Updated v2 documentation, portal fields and recovery controls; description',len(fields['description']))
