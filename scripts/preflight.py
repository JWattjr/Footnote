"""Off-chain exact quote + three canonical-digest checks, with real public posts only."""
import hashlib
import html
import json
import re
import urllib.request
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]

def canonical(text):
    try:
        text = json.dumps(json.loads(text), sort_keys=True, separators=(',', ':'))
    except ValueError:
        pass
    text = re.sub(r'<(script|style)\b[^>]*>.*?</\1>', ' ', text, flags=re.S | re.I)
    return ' '.join(html.unescape(re.sub(r'<[^>]+>', ' ', text)).split())

def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Footnote-evidence-preflight/1.0'}), timeout=30).read().decode('utf-8', errors='replace')

def run(name, uri, source_urls, exact_quotes, expected, note_id=None):
    posts = json.loads(get('https://public.api.bsky.app/xrpc/app.bsky.feed.getPosts?uris=' + quote(uri, safe='')))['posts']
    if not posts or posts[0]['uri'] != uri:
        raise RuntimeError('Exact public post missing')
    checks = {}
    for url in source_urls:
        digests = []
        for i in range(3):
            text = canonical(get(url))
            digests.append(hashlib.sha256(text.encode()).hexdigest())
            exact = exact_quotes.get(url)
            if exact and exact not in text:
                raise RuntimeError('Exact quote absent: ' + exact)
        if len(set(digests)) != 1:
            raise RuntimeError('Canonical digest changed across three fetches: ' + url)
        checks[url] = {'digests': digests, 'quote': exact_quotes.get(url), 'quotePresent': bool(exact_quotes.get(url)), 'canonicalLength': len(text)}
    file = ROOT / 'docs/proofs/live-inputs.json'
    all_inputs = json.loads(file.read_text(encoding='utf-8')) if file.exists() else {}
    all_inputs[name] = {'id': note_id or ('climate-record' if name == 'supported' else 'open-question'), 'uri': uri,
                        'sources': source_urls, 'expected': expected, 'preflightPassed': True,
                        'checks': checks, 'post': posts[0], 'fingerprint': hashlib.sha256(posts[0]['record']['text'].encode()).hexdigest()}
    file.parent.mkdir(parents=True, exist_ok=True)
    file.write_text(json.dumps(all_inputs, indent=2, ensure_ascii=False), encoding='utf-8')
    print(name, posts[0]['record']['text'])
    print(json.dumps(checks, indent=2))

if __name__ == '__main__':
    run('supported', 'at://did:plc:bdhx5rofmoqde5hhpaa2dwza/app.bsky.feed.post/3lfi6htqc6k2j',
        ['https://svs.gsfc.nasa.gov/5376/'],
        {'https://svs.gsfc.nasa.gov/5376/': "2024 was the warmest year in NASA's 145-year record."}, ['SUPPORTED', 'CONTRADICTED'])
    run('unsupported', 'at://did:plc:tcvoifn6tdqpumvnqpmsxjim/app.bsky.feed.post/3lptp22lvqs2x',
        ['https://science.nasa.gov/exoplanets/search-for-life/'],
        {'https://science.nasa.gov/exoplanets/search-for-life/': 'But so far, we have no evidence of life beyond Earth.'}, ['UNSUPPORTED'])
