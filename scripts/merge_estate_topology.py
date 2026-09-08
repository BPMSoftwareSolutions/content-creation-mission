"""Verify all compiler shards and seal the complete topology import manifest."""
import argparse, hashlib, json, os
from collections import Counter
from pathlib import Path
from infographic_contract import ROOT

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--inventory',type=Path,required=True);parser.add_argument('--shards',type=int,default=4);a=parser.parse_args()
    inventory=json.loads(a.inventory.read_bytes());prior=json.loads((ROOT/'outputs/estate-circuits/index.json').read_bytes())
    dest=ROOT/'outputs/estate-topology'
    merged={'source':inventory['source'],'profile':'DECLARED_SOURCE_TOPOLOGY','files':{},'capabilities':[],'gaps':prior['gaps']}
    for part in range(a.shards):
        shard=json.loads((dest/f'index-{part}.json').read_bytes())
        if shard['source']!=merged['source'] or shard['profile']!=merged['profile']:raise ValueError('TOPOLOGY_SHARD_SOURCE_MISMATCH')
        for file,proof in shard['files'].items():
            if file in merged['files'] and proof!=merged['files'][file]:raise ValueError('TOPOLOGY_SHARD_FILE_MISMATCH:'+file)
            merged['files'][file]=proof
        merged['capabilities'].extend(shard['capabilities'])
    if Counter(c['id'] for c in merged['capabilities'])!=Counter(c['id'] for c in prior['capabilities']):raise ValueError('TOPOLOGY_CAPABILITY_COVERAGE_MISMATCH')
    prior_scenarios={(c['definitionPk'],s['definitionPk']) for c in prior['capabilities'] for s in c['scenarios']}
    if {(c['definitionPk'],s['definitionPk']) for c in merged['capabilities'] for s in c['scenarios']}!=prior_scenarios:raise ValueError('TOPOLOGY_SCENARIO_COVERAGE_MISMATCH')
    totals=Counter();types=Counter();routes=Counter();shapes=Counter();largest=[];blueprint_pks=[]
    for cap in merged['capabilities']:
        views=[]
        for file in cap['original']:
            if not file.startswith('outputs/estate-topology/'+cap['id']+'/') or not file.endswith('.js') or file.endswith('/catalog.js'):continue
            text=(ROOT/file).read_text(encoding='utf-8');prefix='window.ESTATE_TOPOLOGY_VIEW='
            if not text.startswith(prefix) or not text.endswith(';'):raise ValueError('TOPOLOGY_VIEW_FORMAT')
            view=json.loads(text[len(prefix):-1]);views.append(view)
            ids={n['id'] for n in view['nodes']};edgeids={e['id'] for e in view['edges']};stats=view['analytics']
            if len(ids)!=len(view['nodes']) or len(edgeids)!=len(view['edges']):raise ValueError('TOPOLOGY_DUPLICATE_ID')
            if any(e['source'] not in ids or e['target'] not in ids for e in view['edges']):raise ValueError('TOPOLOGY_MISSING_ENDPOINT')
            if stats['nodes']!=len(ids) or stats['edges']!=len(edgeids) or stats['omittedSourceNodes'] or stats['omittedSourceEdges']:raise ValueError('TOPOLOGY_COVERAGE_FAILED')
            if view['geometry']['overlaps'] or view['geometry']['nodes']!=len(ids) or view['geometry']['routes']!=len(edgeids):raise ValueError('TOPOLOGY_GEOMETRY_FAILED')
            totals.update(views=1,nodes=len(ids),edges=len(edgeids),sourceNodes=stats['sourceNodes'],sourceEdges=stats['sourceEdges']);types[view['kind']]+=1;routes.update(stats['routeKinds']);shapes.update(stats['nodeKinds'])
            largest.append({'capabilityId':cap['id'],'kind':view['kind'],'nodes':len(ids),'edges':len(edgeids)})
        if len(views)!=cap['topologyViews']:raise ValueError('TOPOLOGY_VIEW_COUNT_MISMATCH')
        bp=[s for s in inventory['subjects'] if s['kind']=='BLUEPRINT' and s['definition']['semantics'].get('capability',{}).get('capabilityId')==cap['id']]
        if bp:
            if len(bp)!=1 or sum(v['kind']=='blueprint' for v in views)!=1:raise ValueError('TOPOLOGY_BLUEPRINT_COVERAGE_MISMATCH')
            cap['blueprintDefinitionPk']=bp[0]['definitionPk'];blueprint_pks.append(bp[0]['definitionPk'])
    for file,proof in merged['files'].items():
        path=(ROOT/file).resolve();path.relative_to(ROOT.resolve());data=path.read_bytes()
        if hashlib.sha256(data).hexdigest()!=proof['sha256'] or len(data)!=proof['bytes']:raise ValueError('TOPOLOGY_FILE_CHANGED:'+file)
    receipt={'version':1,'source':merged['source'],'profile':merged['profile'],'capabilities':len(merged['capabilities']),'scenarios':len(prior_scenarios),'totals':dict(totals),'viewKinds':dict(types),'routeKinds':dict(routes),'nodeKinds':dict(shapes),'blueprintDefinitions':sorted(blueprint_pks),'omittedSourceNodes':0,'omittedSourceEdges':0,'largest':sorted(largest,key=lambda v:v['nodes'],reverse=True)[:10],'note':'Counts are diagram occurrences; scenario views may share source components. Coverage is relative to the source profile, not execution testimony.'}
    receipt_path=dest/'coverage.json';receipt_path.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    extra=[receipt_path,ROOT/'scripts/merge_estate_topology.py',ROOT/'scripts/test_estate_topology.py',ROOT/'requirements.txt']
    for path in extra:
        data=path.read_bytes();file=path.relative_to(ROOT).as_posix();merged['files'][file]={'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)}
        for cap in merged['capabilities']:cap['original']=sorted(set(cap['original']+[file]))
    merged['capabilities'].sort(key=lambda c:c['id']);merged['coverage']=receipt
    tmp=dest/'index.json.tmp';tmp.write_text(json.dumps(merged,ensure_ascii=False,separators=(',',':')),encoding='utf-8');os.replace(tmp,dest/'index.json')
    print(json.dumps({'state':'TOPOLOGY_SEALED',**receipt,'files':len(merged['files']),'bytes':sum(p['bytes'] for p in merged['files'].values())}))

if __name__=='__main__':main()
