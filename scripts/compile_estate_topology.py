"""Compile complete SQL-bound topology products into the media import contract."""
import argparse,hashlib,html,json,os,uuid
from pathlib import Path
from infographic_contract import ROOT
from scl import validate_graph
from estate_topology import topology_views,blueprint_view,PROFILE
from estate_topology_render import render_topology

def dump(v):return json.dumps(v,ensure_ascii=False,separators=(',',':'))
def sha(b):return hashlib.sha256(b).hexdigest()

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--inventory',type=Path,required=True);parser.add_argument('--capabilities');parser.add_argument('--part',type=int,default=0);parser.add_argument('--shards',type=int,default=1);parser.add_argument('--index-name');a=parser.parse_args()
    if a.index_name and (Path(a.index_name).name!=a.index_name or not a.index_name.endswith('.json')):raise ValueError('TOPOLOGY_INDEX_NAME_INVALID')
    inventory=json.loads(a.inventory.read_bytes());prior=json.loads((ROOT/'outputs/estate-circuits/index.json').read_bytes())
    if prior['source']!=inventory['source']:raise ValueError('TOPOLOGY_SOURCE_CHANGED')
    dest=ROOT/'outputs/estate-topology';dest.mkdir(exist_ok=True)
    index={'source':prior['source'],'profile':'DECLARED_SOURCE_TOPOLOGY','files':{},'capabilities':[],'gaps':prior['gaps']}
    def add(path):
        data=path.read_bytes();name=path.relative_to(ROOT).as_posix();index['files'][name]={'sha256':sha(data),'bytes':len(data)};return name
    def write(name,value):
        path=dest/name;path.parent.mkdir(parents=True,exist_ok=True);data=value.encode() if isinstance(value,str) else value
        if not path.exists() or path.read_bytes()!=data:
            tmp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');tmp.write_bytes(data);os.replace(tmp,path)
        return add(path)
    shared=[add(ROOT/'scripts'/name) for name in ('estate_topology.py','estate_topology_render.py','compile_estate_topology.py')]
    shared.extend(add(f) for f in (ROOT/'templates/estate-topology').iterdir() if f.is_file())
    requested=set(a.capabilities.split(',')) if a.capabilities else None
    totals={'views':0,'nodes':0,'edges':0,'blueprints':0,'expressions':0,'native':0,'operations':0}
    for ordinal,cap in enumerate(prior['capabilities']):
        if ordinal%a.shards!=a.part or requested and cap['id'] not in requested:continue
        g=validate_graph(json.loads((ROOT/'samples/scl/capabilities'/cap['id']/'circuit.json').read_bytes()))
        if not any(l['definitionPk']==cap['definitionPk'] and l['capsuleDigest']==cap['capsuleDigest'] for l in inventory['lineage']):raise ValueError('TOPOLOGY_CAPSULE_LINEAGE_CHANGED')
        original=[add(ROOT/f) for f in cap['original'] if not f.startswith('templates/estate-circuit')]+shared
        views=topology_views(g,inventory)
        blueprints=[s for s in inventory['subjects'] if s['kind']=='BLUEPRINT' and s['definition']['semantics'].get('capability',{}).get('capabilityId')==cap['id']]
        if len(blueprints)>1:raise ValueError('TOPOLOGY_BLUEPRINT_SELECTION_REQUIRED')
        if blueprints:
            bp=blueprints[0];raw=(dump(bp['definition'])+'\n').encode();file=write('sources/'+bp['definitionDigest']+'.json',raw);original.append(file)
            source={'path':file,'sha256':sha(raw),'pointer':'/semantics','kind':'DECLARED','label':'SQL selected blueprint definition','definitionPk':bp['definitionPk'],'definitionDigest':bp['definitionDigest']}
            views.insert(0,blueprint_view(cap['id'],bp['definition']['semantics'],source))
        if not views:raise ValueError('TOPOLOGY_NO_SOURCE_VIEWS:'+cap['id'])
        materials=[];summaries=[];artifacts=[]
        def texture_writer(kind,w,h,bytes):
            file=write('textures/'+sha(bytes)+'.webp',bytes);materials.append(file);return '/media/library/'+file
        for view in views:
            rendered=render_topology(view,texture_writer);view.update(rendered)
            svgfile=write(cap['id']+'/'+view['id']+'.svg',view['svg']);artifacts.append(svgfile)
            file=write(cap['id']+'/'+view['id']+'.js','window.ESTATE_TOPOLOGY_VIEW='+dump(view).replace('<','\\u003c')+';');artifacts.append(file)
            summaries.append({k:view[k] for k in ('id','label','kind','analytics','scenarioId','scenarioIds') if k in view}|{'url':'/media/library/'+file})
            totals['views']+=1;totals['nodes']+=len(view['nodes']);totals['edges']+=len(view['edges']);totals[{'blueprint':'blueprints','expression':'expressions'}.get(view['kind'],view['kind'])]+=1
        catalog=write(cap['id']+'/catalog.js','window.ESTATE_TOPOLOGY_CATALOG='+dump({'version':PROFILE,'capabilityId':cap['id'],'views':summaries,'source':inventory['source']}).replace('<','\\u003c')+';')
        original.extend([catalog,*artifacts,*set(materials)])
        products=[]
        for n,scenario in enumerate(cap['scenarios']):
            choices=[v for v in summaries if v.get('scenarioId')==scenario['scenarioId']]
            default=summaries[0] if n==0 and summaries[0]['kind']=='blueprint' else next(iter(choices),summaries[0])
            folder=cap['id']+'/scenario/'+scenario['scenarioId']
            data=write(folder+'/data.js','window.ESTATE_TOPOLOGY_ENTRY='+dump({'scenarioId':scenario['scenarioId'],'viewId':default['id']})+';')
            template=(ROOT/'templates/estate-topology/index.html').read_text(encoding='utf-8').replace('{{TITLE}}',html.escape(g.title)).replace('{{CATALOG}}','/media/library/'+catalog)
            entry=write(folder+'/index.html',template)
            products.append({k:scenario[k] for k in ('scenarioId','definitionPk','objectPk','definitionDigest','label')}|{'folder':folder,'files':[data,entry],'data':data,'entry':entry,'topologyViews':len(views)})
        index['capabilities'].append({k:cap[k] for k in ('id','definitionPk','definitionDigest','capsuleDigest')}|{'original':sorted(set(original)),'scenarios':products,'topologyViews':len(views)}|({'blueprintDefinitionPk':blueprints[0]['definitionPk']} if blueprints else {}))
        output=dest/(a.index_name or ('index.json' if a.shards==1 else 'index-'+str(a.part)+'.json'));output.write_text(dump(index),encoding='utf-8')
        print(dump({'capability':cap['id'],'views':len(views),'nodes':sum(len(v['nodes']) for v in views),'edges':sum(len(v['edges']) for v in views),'totals':totals}),flush=True)
    print(dump({'state':'FULL_TOPOLOGY_COMPILED','totals':totals}),flush=True)

if __name__=='__main__':main()
