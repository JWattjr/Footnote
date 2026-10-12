import json, shutil, subprocess
from pathlib import Path
root=Path('docs/legacy/v1')
if root.exists(): raise SystemExit('Already archived: do not reset persisted v2 transactions')
root.mkdir(parents=True)
shutil.copytree('docs/proofs', root/'proofs')
shutil.copy2('public/deployment.json',root/'deployment.json')
shutil.copy2('docs/PROOF_MANIFEST.md',root/'PROOF_MANIFEST.md')
(root/'contracts').mkdir()
for name in ('notes','bonds','recheck','appeals'):
    (root/'contracts'/f'{name}.py').write_bytes(subprocess.check_output(['git','show',f'HEAD:contracts/{name}.py']))
p={'network':'StudioNet','chainId':61999,'generation':2,'timing':{'appealWindowSeconds':900,'cancelGraceSeconds':600,'bondReleaseDelaySeconds':900,'productionAppealWindowSeconds':259200,'productionCancelGraceSeconds':86400},'contracts':{},'transactions':{},'states':{},'proofs':[],'unproven':['New deployment live proof is in progress.','Forced stale-version cancellation and changed-source label replay are test-only.']}
Path('public/deployment.json').write_text(json.dumps(p,indent=2)+'\n',encoding='utf-8')
print('v1 receipts, exact deployed source bytes and manifest archived; v2 journal initialized')
