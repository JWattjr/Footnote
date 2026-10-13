"""Publish claims only after the new proof completion checks have passed."""
import json
import re
from pathlib import Path

p = json.loads(Path('public/deployment.json').read_text(encoding='utf-8'))
assert p['generation'] == 3 and len(p['contracts']) == 4
assert p['additionalProofs'].get('completedAt'), 'Do not claim incomplete proofs'
old = json.loads(Path('docs/legacy/v2/deployment.json').read_text(encoding='utf-8'))
for file in ['README.md', 'docs/SECURITY_NOTES.md', 'docs/TEST_MATRIX.md']:
    text = Path(file).read_text(encoding='utf-8')
    for key, address in p['contracts'].items():
        text = text.replace(old['contracts'][key], address)
    text = text.replace('generation 2', 'generation 3').replace('**80 direct tests**', '**107 direct tests**')
    Path(file).write_text(text, encoding='utf-8')

readme = Path('README.md').read_text(encoding='utf-8')
readme = readme.replace('For the live proof, same-wallet writer/appellant demonstrates contract routing but does not prove independent participants. Direct tests use distinct fixture wallets and a controlled native ledger; they do not prove StudioNet consensus.',
    'The finalized live proof preserves an UNSUPPORTED version and appends SUPPORTED after a genuine NASA source is added. Wallet A writes the long-source supported note and wallet B appeals it; the honest decision, settlement, exact balances and native credits are recorded. Two signing wallets demonstrate separate contract participants, not two independently verified human identities. Direct tests additionally exercise adversarial cases with mocked sources and native delivery.')
if 'The finalized live proof preserves an UNSUPPORTED version' not in readme:
    readme = readme.replace('Timing disclosure:', 'The finalized live proof preserves an UNSUPPORTED version and appends SUPPORTED after a genuine NASA source is added. Wallet A writes the long-source supported note and wallet B appeals it; the honest UPHELD decision, settlement, exact balances and native credits are recorded in [PROOF_MANIFEST.md](docs/PROOF_MANIFEST.md). Two signing wallets demonstrate separate contract participants; independently verified human identities are not claimed.\n\nTiming disclosure:', 1)
readme = readme.replace('the app now targets generation 3.', 'the app now targets generation 3. The funded v2 receipts, source bytes and failure diagnosis are archived in `docs/legacy/v2`; its remaining eight GEN were recovered through verified withdrawals.')
if 'Validators compare labels and cited URL sets' not in readme:
    readme = readme.replace('## Trust boundaries and people safety', 'Validators compare labels and cited URL sets rather than independently selected quote spans. Each validator still grounds every leader quote in its own source text, allowing only whitespace and specified typography normalization, with case-sensitive substring matching. The leader quotes remain stored.\n\n## Trust boundaries and people safety')
if '107 direct tests and seven TypeScript tests pass' not in readme:
    readme = readme.replace('## Submission package', '107 direct tests and seven TypeScript tests pass, with eight inapplicable scenario fixtures skipped. Typecheck, lint, all four GenVM checks, production build, read-only network verification and desktop/mobile history checks are recorded in [TEST_MATRIX.md](docs/TEST_MATRIX.md).\n\n## Submission package')
readme = readme.replace('The raw full/runtime audit reports are committed in docs/proofs.', 'The refreshed raw full/runtime audit reports are committed in docs/proofs; historical reports remain in docs/legacy/v2.')
Path('README.md').write_text(readme, encoding='utf-8')

sec = Path('docs/SECURITY_NOTES.md').read_text(encoding='utf-8')
sec = sec.replace('For the live proof, same-wallet writer/appellant demonstrates contract routing but does not prove independent participants. Direct tests use distinct fixture wallets and a controlled native ledger; they do not prove StudioNet consensus.', 'The live proof uses distinct signing wallets for writer and appellant, with a recorded A-to-B funding transaction, honest outcome, and exact verified credits. These are separate accounts operated for the demonstration; independently verified human identities are not claimed. Direct tests additionally model adversarial recipients and native delivery.')
section = '''## Quote consensus fix and live evidence

The v2 long-source NASA note failed consensus with result 7 because independently chosen valid quote spans were compared literally. An earlier leader attempt failed exact grounding on typography. Generation 3 compares evidence label, tone label, allegation flag and a sorted, de-duplicated cited URL set. Appeals also independently compares its outcome. Quote text is excluded from agreement, while each validator checks every leader quote against its own fetched canonical page. Only whitespace, non-breaking spaces, curly quotes and en/em dashes are normalized; leading/trailing quote punctuation is ignored. Matching remains case-sensitive and exact, with a minimum twelve-character normalized quote; changed words and fabricated quotes fail. Digests continue to describe each fetched canonical page without typography rewriting. Prompts request verbatim short sentences, and the leader's quotes are stored.

The three public judging paths each have tests for different valid quotes agreeing, independent-page grounding, typography/whitespace normalization and changed-word/case rejection. The fresh live long-NASA supported note, UNSUPPORTED-to-SUPPORTED added-source recheck with retained history, and distinct-wallet appeal have finalized receipts. The two wallets are separate accounts operated for this demonstration; independent human identities or adversarial ownership are not claimed. The B challenge reuses the authentic NASA source and is judged honestly, without fabricated counterclaims.

The same-URL publisher correction remains a mocked test-only replay. Forced version drift, callback failures/replays and cancellation adversaries remain direct-test-only. Timeout cancellation was genuinely shown on archived v2 and is not claimed as repeated on generation 3.

'''
if '## Quote consensus fix and live evidence' not in sec:
    sec = sec.replace('## Escrow liveness audit and fixed exits', section+'## Escrow liveness audit and fixed exits')
sec = sec.replace('## Immutable legacy instance', '## Immutable legacy instances')
sec = sec.replace('## Fixed deployment target', 'The funded v2 instance retains literal quote-span consensus. Its remaining eight GEN were released and withdrawn after maturity, with every native credit verified; see `docs/legacy/v2/cleanup/journal.json`. Its addresses are historical recovery targets only and are absent from the Portal fields.\n\n## Fixed deployment target')
Path('docs/SECURITY_NOTES.md').write_text(sec, encoding='utf-8')

matrix = Path('docs/TEST_MATRIX.md').read_text(encoding='utf-8')
matrix = matrix.replace('| Leader quote checked against own page | Grounding helper + actual validator callback tests | Direct mocked validator invocation |',
    '| Quote-independent URL-set agreement, typography and exact own-page grounding across Notes/Recheck/Appeals | `test_consensus.py` | 27 direct cases; fresh long-NASA live supported note |')
matrix = matrix.replace('| Recheck emits version update; history retained | Flow tests + authorized append test | Direct cross-contract stub |',
    '| Added-source recheck changes UNSUPPORTED to SUPPORTED; both versions retained | Flow tests + authorized append + fresh live receipts | Direct + finalized live; desktop/mobile history |\n| Separate writer/appellant wallets, honest appeal settlement and exact credits | Two public CLI wallets, funding receipt, balance table | Finalized live; separate accounts, not verified human identities |')
matrix = matrix.replace('Direct; finalized live timeout cancellation', 'Direct; archived v2 live timeout cancellation')
matrix = re.sub(r'The Vercel production build and deployment passed on 12 October.*?characters\.',
    'Fresh production verification reports are saved in `proofs/production-verification.json` and `proofs/production-browser-report.json`; field lengths and every HTTP 200 link are recorded in `submission/link-check.json`. Historical v2 reports remain archived.', matrix, flags=re.S)
matrix += '\nTiming disclosure: the public demo deployment uses a 15-minute appeal window; production default is 72 hours. Demo grace is 10 minutes and bond release delay is 15 minutes.\n' if 'the public demo deployment uses a 15-minute appeal window; production default is 72 hours' not in matrix else ''
Path('docs/TEST_MATRIX.md').write_text(matrix, encoding='utf-8')

architecture = Path('docs/ARCHITECTURE.md').read_text(encoding='utf-8').replace('a sorted deduplicated citation set', 'a sorted deduplicated cited URL set; quote spans are excluded from agreement, while leader quotes remain independently grounded after exact typography normalization')
Path('docs/ARCHITECTURE.md').write_text(architecture, encoding='utf-8')
tutorial = Path('docs/TUTORIAL.md').read_text(encoding='utf-8').replace('sorted(set((c[\'url\'], c[\'quote\'])', 'sorted(set(c[\'url\']')
tutorial = tutorial.replace('a sorted deduplicated citation set.', 'a sorted deduplicated cited URL set. Quote spans can differ across models. Every leader quote must still occur in each validator\'s own canonical page after whitespace, curly-quote and en/em-dash normalization; case and words stay exact.')
tutorial = tutorial.replace('A source change must be real to count as live proof.', 'Select temperature-update-2025 to inspect the finalized UNSUPPORTED v1 and SUPPORTED v2. A genuine existing NASA page was added to the supplied evidence. This proves an added-source label change, not a publisher edit or newly published page. A source change must be real to count as live proof.')
tutorial = tutorial.replace('`python scripts/preflight.py`', '`python scripts/preflight-extra.py`')
tutorial = tutorial.replace('The climate example uses NASA\'s record-temperature visualization and a real public post about the 2024 temperature record. The unsupported example uses NASA\'s search-for-life page with a real prediction that future biosignature searches will never tell us anything. The latter is intentionally a source-scoped uncertainty demonstration: a source about present knowledge does not establish every prediction about the future. The actual result is the finalized validator judgment, not the builder\'s hoped-for label.', 'The current long-source example uses NASA\'s global-temperature page and Scott Duncan\'s real post about the 2024 record. For temperature-update-2025, the original supplied NASA page covers 2021 and does not establish the post\'s 2025 claim; the finalized initial judgment is UNSUPPORTED. Adding the genuine NASA global-temperature page through Recheck produces SUPPORTED v2, retaining the original. This proves a change in supplied evidence, not that the claim lacked a source anywhere on the internet or that a publisher edited its page. The exact outcomes and per-write preflights are in PROOF_MANIFEST.md.')
Path('docs/TUTORIAL.md').write_text(tutorial, encoding='utf-8')
demo = Path('docs/DEMO.md').read_text(encoding='utf-8').replace('climate-record', 'independent-climate-appeal')
demo = demo.replace('22–32 seconds: Select the finalized **open-question**. Show UNSUPPORTED as a valid label for a prediction the supplied evidence does not establish.', '22–32 seconds: Select **temperature-update-2025**, then v1 in **Follow the changes**. Show UNSUPPORTED: the original 2021 source does not establish the post\'s 2025 claim.')
demo = re.sub(r'32–42 seconds:.*?(?=\n\n42–52 seconds:)', '32–42 seconds: Select v2. Show the live SUPPORTED label, added authentic NASA source and retained v1. Explain that this is new evidence supplied to the note, not a staged publisher correction. The separate /replay remains explicitly mocked.', demo, flags=re.S)
demo = demo.replace('Explain the one-appeal-per-version rule', 'Point to the distinct public writer/appellant addresses and honest UPHELD appeal in the manifest. Explain the one-appeal-per-version rule')
demo = re.sub(r'52–60 seconds:.*?(?=\n\nDo not spend)', '52–60 seconds: Open **Live proof**, the four current explorer links and the manifest. Show the paid appeal-deposit and writer-bond claims, their verified native credits and exact 2-GEN deltas. The balance table ends with zero held by the current Bonds contract. Timeout cancellation is archived v2 evidence and has not been repeated on v3. End with the trust boundary: supplied public sources, independent validators, immutable history and simulated StudioNet GEN.', demo, flags=re.S)
Path('docs/DEMO.md').write_text(demo, encoding='utf-8')

fields = json.loads(Path('docs/submission/portal-fields.json').read_text(encoding='utf-8'))
fields['description'] = 'Footnote adds source-grounded notes to public Bluesky posts. Four GenLayer contracts separate evidence from tone, preserve versions, hold writer bonds and judge appeals. Validators agree on labels and cited URLs while independently grounding the leader quotes. Finalized StudioNet proof shows an UNSUPPORTED note become SUPPORTED after adding a real NASA source, with both versions retained, plus a note by wallet A appealed by wallet B and settled with receipt-verified native credits. Host, quota and open-appeal recheck guards are proven live. Reading needs no wallet. StudioNet is a simulator: the public demo deployment uses a 15-minute appeal window; production default is 72 hours. Demo grace is 10 minutes and bond release delay is 15 minutes; production grace is 24 hours. Allegations use stricter labels and withhold names, handles and post text from state.'
fields['expectedOutcome'] = 'Demonstrate an auditable UNSUPPORTED-to-SUPPORTED recheck with immutable history, and an appeal signed by a second wallet with exact settlement balances and verified withdrawals. Help readers inspect sources, distinguish evidence from tone, and challenge notes. Labels reflect supplied sources, not guarantees of truth.'
fields['howTo'][2] = 'Select temperature-update-2025 and switch between v1 Unsupported and v2 Supported in Follow the changes; inspect the newly added NASA source. Live proof links the two-wallet appeal receipts.'
for key, address in p['contracts'].items():
    fields['contractExplorerLinks'][key] = 'https://explorer-studio.genlayer.com/contracts/'+address
fields['evidenceLinks'] = ['https://science.nasa.gov/earth/explore/earth-indicators/global-temperature/', 'https://svs.gsfc.nasa.gov/4964/', 'https://github.com/JWattjr/Footnote/blob/main/docs/PROOF_MANIFEST.md', 'https://footnote-genlayer.vercel.app/?note=temperature-update-2025']
for key, limit in [('oneLiner',180),('description',1000),('expectedOutcome',500)]:
    assert len(fields[key]) <= limit
    print(key, len(fields[key]), '/', limit)
Path('docs/submission/portal-fields.json').write_text(json.dumps(fields,indent=2)+'\n')
