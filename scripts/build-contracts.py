"""Produce standalone pinned contracts; shared source is audited once, deployed inlined."""
from pathlib import Path

root = Path(__file__).resolve().parents[1]
header = '# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }\n'
(root / 'contracts').mkdir(exist_ok=True)
for name in ('notes', 'recheck', 'appeals', 'bonds'):
    common = (root / 'contracts-src/common.py').read_text(encoding='utf-8')
    body = (root / f'contracts-src/{name}.py').read_text(encoding='utf-8')
    (root / f'contracts/{name}.py').write_text(header + common + '\n' + body, encoding='utf-8')
