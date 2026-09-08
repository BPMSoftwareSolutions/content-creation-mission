"""Compile source-matched SCL with the content lab's existing grammar and renderer.

No generation API is called. All original sources remain in a closed SQL import
bundle; the website gets only declared visual projections and their receipts.
"""
import argparse,base64,copy,hashlib,html,json,re,sys,os,uuid
from pathlib import Path
from scl import validate_graph
from scl_render import compile_graph,materials
from enhance_infographics import composite
from infographic_contract import ROOT

def sha(b):return hashlib.sha256(b).hexdigest()
def dump(x):return json.dumps(x,ensure_ascii=False,separators=(',',':'))
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--inventory',type=Path,required=True);p.add_argument('--limit',type=int);p.add_argument('--shards',type=int,default=1);p.add_argument('--part',type=int,default=0);a=p.parse_args()
    inventory=json.loads(a.inventory.read_bytes());dest=ROOT/'outputs/estate-circuits';dest.mkdir(parents=True,exist_ok=True)
    index={'source':inventory['source'],'files':{},'capabilities':[],'gaps':[]}
    prior_path=dest/'index.json';prior=json.loads(prior_path.read_bytes()) if prior_path.exists() else None
    if prior and prior['source']!=inventory['source']:raise ValueError('RESUME_SOURCE_CHANGED')
    completed={c['id'] for c in prior['capabilities']} if prior else set()
    if prior and a.part==0:index=prior
    index_path=dest/('index.json' if a.shards==1 else 'index-'+str(a.part)+'.json')
    def add(file):
        file=file.resolve()
        if not file.is_relative_to(ROOT):raise ValueError('SOURCE_PATH_ESCAPE')
        data=file.read_bytes();key=file.relative_to(ROOT).as_posix();index['files'][key]={'sha256':sha(data),'bytes':len(data)};return key
    def write(relative,data):
        f=dest/relative;f.parent.mkdir(parents=True,exist_ok=True);raw=data.encode() if isinstance(data,str) else data
        if not f.exists() or f.read_bytes()!=raw:
            temp=f.with_name(f.name+'.'+uuid.uuid4().hex+'.tmp');temp.write_bytes(raw);os.replace(temp,f)
        return add(f)
    lines={}
    for row in inventory['lineage']:lines.setdefault(row['definitionPk'],set()).add(row['capsuleDigest'])
    caps=[s for s in inventory['subjects'] if s['kind']=='CAPABILITY' and s['managed']]
    scenarios=[s for s in inventory['subjects'] if s['kind']=='SCENARIO']
    shared=[add(ROOT/'scripts/compile_infographics.py'),add(ROOT/'scripts/scl.py'),add(ROOT/'scripts/scl_render.py'),add(ROOT/'scripts/enhance_infographics.py'),add(ROOT/'scripts/infographic_contract.py'),add(ROOT/'declarations/infographic-grammar.v1.json'),add(ROOT/'samples/scl/circuit-flow.js')]
    for f in (ROOT/'templates/estate-circuit').iterdir():
        if f.is_file():shared.append(add(f))
    grammar=json.loads((ROOT/'declarations/infographic-grammar.v1.json').read_bytes())
    shared.append(write('grammar.js','window.SIDEFX_GRAMMAR='+dump(grammar).replace('<','\\u003c')+';'))
    rendered=0
    for number,cap in enumerate(caps[:a.limit]):
        if cap['entityId'] in completed or number%a.shards!=a.part:continue
        cid=cap['entityId'];graph_file=ROOT/'samples/scl/capabilities'/cid/'circuit.json';evidence_file=ROOT/'data/capsule-evidence/capabilities'/(cid+'.json')
        if not graph_file.exists() or not evidence_file.exists():index['gaps'].append({'id':cid,'reason':'SOURCE_ABSENT'});continue
        evidence=json.loads(evidence_file.read_bytes())
        if evidence['capsuleDigest'].removeprefix('sha256:') not in lines.get(cap['definitionPk'],set()):index['gaps'].append({'id':cid,'reason':'CAPSULE_LINEAGE_CHANGED'});continue
        g=validate_graph(json.loads(graph_file.read_bytes()))
        if not g.scenarios:index['gaps'].append({'id':cid,'reason':'NO_DECLARED_SCENARIO'});continue
        original=[add(graph_file),add(graph_file.with_suffix('.scl')),add(evidence_file),*shared]
        for source in g.sources:
            key=add(ROOT/source.path)
            if index['files'][key]['sha256']!=source.sha256:raise ValueError('SOURCE_DIGEST_MISMATCH')
            original.append(key)
        products=[]
        for scenario in g.scenarios:
            matches=[s for s in scenarios if s['entityId']==scenario.id and cid in s['definition']['semantics'].get('tags',{}).get('capability',[])]
            if len(matches)!=1:index['gaps'].append({'id':cid+'/'+scenario.id,'reason':'SCENARIO_IDENTITY_UNRESOLVED'});continue
            subject=matches[0];result=compile_graph(g,scenario.id,False);projection=result['projection'];base=result['svg'];enhanced,proof=composite(base,projection,materials())
            # Remove unused source descriptors only; preserve every visible source ref.
            visible=set()
            for group in ('nodes','junctions','edges','capabilities','scenarios','humanAnchors','providers'):
                for item in projection[group]:visible.update(item.get('sourceRefs',[]))
            public_projection=copy.deepcopy(projection);public_projection['sources']=[s for s in projection['sources'] if s['id'] in visible]
            folder=cid+'/'+scenario.id;files=[];textures=[]
            def externalize(match):
                data=base64.b64decode(match.group(1));h=sha(data);textures.append(write('textures/'+h+'.webp',data));return '/media/library/outputs/estate-circuits/textures/'+h+'.webp'
            public_svg=re.sub(r'data:image/webp;base64,([A-Za-z0-9+/=]+)',externalize,enhanced)
            source_svg=write(folder+'/original.svg',enhanced)
            files.extend([source_svg,write(folder+'/projection.json',projection and dump(projection)),write(folder+'/receipt.json',dump({**result['receipt'],'materialReview':proof}))])
            data={'projection':public_projection,'receipt':result['receipt'],'baseSVG':base,'materialSVG':public_svg}
            public_data=write(folder+'/data.js','window.ESTATE_CIRCUIT='+dump(data).replace('<','\\u003c')+';')
            files.extend([public_data,*textures]);products.append({'scenarioId':scenario.id,'definitionPk':subject['definitionPk'],'objectPk':subject['objectPk'],'definitionDigest':subject['definitionDigest'],'label':scenario.label,'folder':folder,'files':files,'data':public_data,'originalSvg':source_svg})
            rendered+=1
        for product in products:
            opts=''.join('<option value="/media/library/outputs/estate-circuits/'+html.escape(c['folder'],quote=True)+'/index.html"'+(' selected' if c is product else '')+'>'+html.escape(c['label'])+'</option>' for c in products)
            template=(ROOT/'templates/estate-circuit/index.html').read_text(encoding='utf-8').replace('{{TITLE}}',html.escape(product['label'])).replace('{{OPTIONS}}',opts)
            product['entry']=write(product['folder']+'/index.html',template);product['files'].append(product['entry'])
        index['capabilities'].append({'id':cid,'definitionPk':cap['definitionPk'],'definitionDigest':cap['definitionDigest'],'capsuleDigest':evidence['capsuleDigest'].removeprefix('sha256:'),'original':sorted(set(original)),'scenarios':products})
        index_path.write_text(dump(index),encoding='utf-8');print(dump({'capability':cid,'scenarios':len(products),'total':rendered}),flush=True)
    index_path.write_text(dump(index),encoding='utf-8');print(dump({'state':'COMPILED','capabilities':len(index['capabilities']),'scenarios':rendered,'files':len(index['files']),'gaps':index['gaps']}),flush=True)

if __name__=='__main__':
    try:main()
    except Exception as e:print('ESTATE_CIRCUIT_COMPILE_FAILED',str(e)[:300],file=sys.stderr);raise
