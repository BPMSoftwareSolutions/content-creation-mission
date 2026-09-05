"""Build a portable, searchable atlas and resolve only successful image receipts."""
import hashlib, json, shutil
from pathlib import Path
from PIL import Image
from visual_review import validate_review
from mechanics_gate import validate_grounding

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'samples/visual-pilot'
jobs=json.loads((OUT/'generation-manifest.json').read_text())
receipts={}
for path in sorted((ROOT/'outputs/generated').glob('*.json')):
    receipt=json.loads(path.read_text())
    if receipt.get('status')=='GENERATED': receipts[receipt['jobId']]=receipt
pilot=[]
for job in jobs:
    validate_grounding(job)
    receipt=receipts.get(job['id'])
    if not receipt: continue
    image=receipt['images'][0]
    source=ROOT/'outputs/generated'/image['path']
    if hashlib.sha256(source.read_bytes()).hexdigest()!=image['sha256']: raise ValueError('Image digest mismatch')
    if job.get('directorVersion'):
        review_path=ROOT/'evaluations/director-v2'/f"{job['index']:02}.json"
        if not review_path.exists(): raise ValueError('VISUAL_REVIEW_REQUIRED: '+job['scenarioKey'])
        review=json.loads(review_path.read_text())
        if not validate_review(review,job,source.read_bytes()): raise ValueError('VISUAL_EXPERIENCE_DOES_NOT_CONFORM: '+job['scenarioKey'])
        job={**job,'review':review}
    target=OUT/f"storyboard-{job['index']:02}{source.suffix}"
    shutil.copyfile(source,target)
    with Image.open(source) as picture:
        w,h=picture.size
        for phase in range(3):
            picture.crop((round(w*phase/3),0,round(w*(phase+1)/3),h)).save(OUT/f"frame-{job['index']:02}-{phase}.jpg",quality=94)
    pilot.append({**job,'image':target.name,'receipt':receipt})
(OUT/'pilot-assets.json').write_text(json.dumps(pilot,indent=2),encoding='utf-8')
specs=json.loads((ROOT/'outputs/visual-experience-specs.json').read_text())
recipes=json.loads((ROOT/'data/generation-recipes.json').read_text())
template=(ROOT/'scripts/visual_atlas.template.html').read_text(encoding='utf-8')
data=json.dumps({'specs':specs,'pilot':pilot,'recipes':recipes},ensure_ascii=False).replace('<','\\u003c')
(OUT/'atlas.html').write_text(template.replace('__ATLAS_DATA__',data),encoding='utf-8')
print('Atlas:',len(specs),'scenarios;',len(pilot),'rendered storyboards')
