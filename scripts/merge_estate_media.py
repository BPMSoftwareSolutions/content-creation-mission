"""Validate and merge disjoint compiler shards, retaining exact input closure."""
import json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];dest=ROOT/'outputs/estate-circuits'
def sha(data):return hashlib.sha256(data).hexdigest()
def main():
    parts=[json.loads((dest/('index-'+str(i)+'.json')).read_bytes()) for i in range(4)]
    index={'source':parts[0]['source'],'files':{},'capabilities':[],'gaps':[]};seen=set()
    for part in parts:
        if part['source']!=index['source']:raise ValueError('MIXED_GENERATION')
        for f,v in part['files'].items():
            if f in index['files'] and index['files'][f]!=v:raise ValueError('MIXED_FILE_REVISION')
            index['files'][f]=v
        for c in part['capabilities']:
            if c['id'] in seen:raise ValueError('DUPLICATE_CAPABILITY')
            seen.add(c['id']);index['capabilities'].append(c)
        index['gaps'].extend(part['gaps'])
    extras=['requirements.txt','scripts/compile_estate_media.py','scripts/merge_estate_media.py','scripts/generate_component_assets.py','declarations/infographic-enhancement.v1.json','evaluations/component-enhancement-review.json']
    enhancement=json.loads((ROOT/'declarations/infographic-enhancement.v1.json').read_bytes())
    for asset in enhancement['assets']:
        receipt=json.loads((ROOT/asset['receipt']).read_bytes())
        if sha((ROOT/receipt['image']).read_bytes())!=receipt['imageSha256']:raise ValueError('MATERIAL_CHANGED')
        extras.extend([asset['receipt'],receipt['image']])
    for f in extras:
        data=(ROOT/f).read_bytes();index['files'][f]={'sha256':sha(data),'bytes':len(data)}
    for cap in index['capabilities']:cap['original']=sorted(set(cap['original']+extras))
    index['capabilities'].sort(key=lambda c:c['id'])
    for f,v in index['files'].items():
        if sha((ROOT/f).read_bytes())!=v['sha256']:raise ValueError('FILE_CHANGED '+f)
    (dest/'index.json').write_text(json.dumps(index,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
    print(json.dumps({'capabilities':len(index['capabilities']),'scenarios':sum(len(c['scenarios']) for c in index['capabilities']),'files':len(index['files']),'bytes':sum(f['bytes'] for f in index['files'].values()),'gaps':len(index['gaps'])}))
if __name__=='__main__':main()
