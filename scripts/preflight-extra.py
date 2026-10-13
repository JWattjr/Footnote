"""Record real public inputs before either additional proof sends a transaction."""
import ast
import hashlib
import html
import json
import re
import unicodedata
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
# Execute the exact deployed helper definitions, without importing the GenVM runtime.
tree = ast.parse((ROOT / 'contracts-src/common.py').read_text(encoding='utf-8'))
helpers = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name in ('canonical', 'packed', 'normalized_text', 'normalized_quote')]
exec(compile(ast.Module(body=helpers, type_ignores=[]), 'contract-canonicalization', 'exec'))

def get(url):
    request = urllib.request.Request(url, headers={'User-Agent': 'Footnote-evidence-preflight/2.0'})
    with urllib.request.urlopen(request, timeout=40) as response:
        if response.status != 200:
            raise RuntimeError(f'{url}: HTTP {response.status}')
        return response.read().decode('utf-8', errors='replace'), response.status, response.url

def check(url, exact):
    records = []
    for _ in range(3):
        raw, status, final_url = get(url)
        try:
            text = canonical(packed(json.loads(raw)))
        except ValueError:
            text = canonical(raw)
        if normalized_quote(exact) not in normalized_text(text):
            raise RuntimeError(f'Exact quote absent after deployed canonicalization: {url}')
        records.append({'status': status, 'finalUrl': final_url, 'digest': hashlib.sha256(text.encode()).hexdigest(), 'quotePresent': True, 'canonicalLength': len(text), 'rawUtf8Bytes': len(raw.encode('utf-8'))})
    if len({record['digest'] for record in records}) != 1:
        (ROOT / 'docs/proofs/preflight-digest-failure.json').write_text(json.dumps({
            'checkedAt': datetime.now(timezone.utc).isoformat(), 'url': url, 'quote': exact,
            'fetches': records, 'result': 'Rejected off-chain; no publication transaction may be sent.'
        }, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
        raise RuntimeError(f'Three canonical digests differ: {url}')
    return {'url': url, 'quote': exact, 'fetches': records}

if __name__ == '__main__':
    old = 'https://svs.gsfc.nasa.gov/4964/'
    added = 'https://science.nasa.gov/earth/explore/earth-indicators/global-temperature/'
    appeal_source = added
    counter = added
    checks = {
        old: check(old, 'Earth’s global average surface temperature in 2021 tied with 2018 as the sixth warmest on record'),
        added: check(added, 'the two years are effectively tied according to an analysis by NASA scientists.'),
    }
    checks[added]['additionalQuotes'] = [
        'Since record-keeping began in 1880, the hottest year on record remains 2024',
        'The 10 most recent years are the warmest on record.',
    ]
    # Verify the supported post's complete claim, too; use the same three-fetch rule.
    checks[added]['supportedClaimChecks'] = [check(added, q) for q in checks[added]['additionalQuotes']]
    cases = {
        'labelChange': {'id': 'temperature-update-2025', 'uri': 'at://did:plc:s56x2jo2ii7s3zti6mto3sgo/app.bsky.feed.post/3mcfvit5dx22e', 'initialSources': [old], 'addedSources': [added], 'expectedBefore': 'UNSUPPORTED', 'expectedAfter': 'SUPPORTED'},
        'twoWallet': {'id': 'independent-climate-appeal', 'uri': 'at://did:plc:nw2knj6hxl4dpewp5prhnqjc/app.bsky.feed.post/3lgdujb37sk2m', 'initialSources': [appeal_source], 'counterSources': [counter], 'expectedBefore': 'SUPPORTED'},
    }
    for case in cases.values():
        raw, status, _ = get('https://public.api.bsky.app/xrpc/app.bsky.feed.getPosts?uris=' + quote(case['uri'], safe=''))
        posts = json.loads(raw)['posts']
        if not posts or posts[0]['uri'] != case['uri']:
            raise RuntimeError('Real post is missing: ' + case['uri'])
        case['post'] = posts[0]
        case['fingerprint'] = hashlib.sha256(posts[0]['record']['text'].encode()).hexdigest()
        case['postStatus'] = status
        print(case['id'] + ': ' + posts[0]['record']['text'])
    report = {'checkedAt': datetime.now(timezone.utc).isoformat(), 'canonicalization': 'deployed canonical, packed, normalized_text and normalized_quote helpers; case-sensitive substring', 'checks': checks, 'cases': cases,
              'disclosure': 'The initial supplied page predates the 2025 measurement and does not establish the complete post claim. Adding an existing credible page demonstrates new evidence supplied to this note, not a publisher correction or newly published source.'}
    (ROOT / 'docs/proofs/extra-inputs.json').write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    live = {
        'supported': {'id': cases['twoWallet']['id'], 'uri': cases['twoWallet']['uri'], 'sources': [added], 'expected': ['SUPPORTED'], 'preflightPassed': True},
        'unsupported': {'id': cases['labelChange']['id'], 'uri': cases['labelChange']['uri'], 'sources': [old], 'expected': ['UNSUPPORTED'], 'preflightPassed': True},
    }
    for key, suffix in [('quota2','2'),('quota3','3')]:
        live[key] = {**live['supported'], 'id': 'climate-quota-' + suffix}
    (ROOT / 'docs/proofs/live-inputs.json').write_text(json.dumps(live, indent=2) + '\n', encoding='utf-8')
    print('Real sources: HTTP 200, normalized exact quotes, three identical canonical digests each.')
