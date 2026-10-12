import json
from pathlib import Path
file=Path('docs/proofs/live-inputs.json')
p=json.loads(file.read_text(encoding='utf-8'))
p['supported']['expected']=['SUPPORTED']
for name, note_id in [('quota2','climate-quota-2'),('quota3','climate-quota-3')]: p[name]={**p['supported'],'id':note_id}
file.write_text(json.dumps(p,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print('Fresh canonical checks bound to supported and both same-post quota inputs')
