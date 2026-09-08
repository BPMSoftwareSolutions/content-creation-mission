"""Measure retained estate topology before selecting a visual projection."""
import json
from collections import Counter
from pathlib import Path
from scl import validate_graph, resolve_sources
from infographic_contract import ROOT

def audit():
    rows=[]; profiles=Counter(); kinds=Counter(); routes=Counter()
    for file in sorted((ROOT/'samples/scl/capabilities').glob('*/circuit.json')):
        g=validate_graph(json.loads(file.read_bytes()),verify_sources=False)
        records=[r for r in g.records if r.kind in ('policy','blueprint')]
        sources={s.id:s for s in g.sources}
        values=resolve_sources([sources[r.sourceRef] for r in records])
        row={'id':g.id,'scenarios':len(g.scenarios),'operations':0,'mechanics':0,'cells':0,'routes':0,'blueprintNodes':0,'blueprintEdges':0,'profiles':[]}
        for r in records:
            v=values[r.sourceRef]
            if r.kind=='blueprint':
                row['blueprintNodes']+=len(v.get('nodes',[]));row['blueprintEdges']+=len(v.get('edges',[]));continue
            profile=v.get('executionEmbodimentPlanType');profiles[profile]+=1;row['profiles'].append(profile)
            for n in v.get('nodes',[]):
                row['operations']+=len(n.get('operations',[]))
                kinds.update(o.get('kind','invoke-port') for o in n.get('operations',[]))
            row['mechanics']+=len(v.get('mechanicBindings',[]))
            native=v.get('canonicalGraph',{})
            row['cells']+=len(native.get('cells',[]));row['routes']+=len(native.get('edges',[]))
            routes.update(e['kind'] for e in native.get('edges',[]))
        rows.append(row)
    result={'profiles':dict(profiles),'operationKinds':dict(kinds),'nativeRouteKinds':dict(routes),'totals':{k:sum(r[k] for r in rows) for k in ('scenarios','operations','mechanics','cells','routes','blueprintNodes','blueprintEdges')},'capabilities':rows}
    dest=ROOT/'outputs/estate-topology';dest.mkdir(exist_ok=True)
    (dest/'audit.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps({**{k:v for k,v in result.items() if k!='capabilities'},'largestNative':sorted(rows,key=lambda r:r['cells'],reverse=True)[:3],'largestLegacy':sorted(rows,key=lambda r:r['operations'],reverse=True)[:3]},indent=2))

if __name__=='__main__':audit()
