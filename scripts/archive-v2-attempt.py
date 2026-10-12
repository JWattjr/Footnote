import json, shutil
from pathlib import Path
root=Path('docs/legacy/v2-unfunded-attempt')
if root.exists(): raise SystemExit('Already archived: do not reset live journal')
p=json.loads(Path('public/deployment.json').read_text(encoding='utf-8'))
assert not any('stake' in x for x in p['transactions']), 'Do not archive a funded deployment'
root.mkdir(parents=True)
shutil.copy2('public/deployment.json',root/'deployment.json')
for name in p['transactions']: shutil.copy2(Path('docs/proofs')/(name+'.json'),root/(name+'.json'))
p.update(contracts={},transactions={},states={},deploymentAttempt=2)
Path('public/deployment.json').write_text(json.dumps(p,indent=2)+'\n',encoding='utf-8')
print('Unfunded deployment journal preserved; final deployment journal initialized')
