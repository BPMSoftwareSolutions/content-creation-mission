"""Reproduce every source graph and measure every automatic scenario infographic."""
from collections import Counter
from time import perf_counter
from infographic_contract import ROOT, read, write, digest
from reveal_scl import reveal
from scl import validate_graph, graph_hash, parse, emit, need
from scl_render import compile_graph
from scl_native import native_view


def main():
    started=perf_counter();catalog=read('samples/scl/catalog.json');rows=[];totals=Counter();native=[]
    inputs={str(p.relative_to(ROOT)).replace('\\','/'):digest(p) for p in [ROOT/'scripts/scl.py',ROOT/'scripts/reveal_scl.py',ROOT/'scripts/scl_render.py',ROOT/'scripts/scl_native.py',ROOT/'scripts/compile_infographics.py']}
    for item in catalog['results']:
        g=reveal(item['id']);saved=validate_graph(read(f'samples/scl/capabilities/{g.id}/circuit.json'))
        need(graph_hash(g)==graph_hash(saved)==item['graphSha256'],'REVEAL_DRIFT:'+g.id)
        need(graph_hash(parse((ROOT/f'samples/scl/capabilities/{g.id}/circuit.scl').read_text(encoding='utf-8')))==graph_hash(g),'SCL_DRIFT:'+g.id)
        records=[]
        for s in g.scenarios:
            result=compile_graph(g,s.id);r=result['receipt'];need(not r['geometryFindings'],'GEOMETRY')
            totals['scenarios']+=1;totals['nodes']+=r['visibleNodes'];records.append(dict(scenarioId=s.id,svgSha256=__import__('hashlib').sha256(result['svg'].encode()).hexdigest(),geometry='PASS'))
        if any(r.kind=='cell' for r in g.records):
            result=native_view(g);native.append(dict(capabilityId=g.id,**result['receipt']))
        rows.append(dict(capabilityId=g.id,graphSha256=graph_hash(g),scenarios=records))
        print('VERIFIED',g.id,len(records),flush=True)
    need(all(digest(ROOT/p)==h for p,h in inputs.items()),'COMPILER_CHANGED_DURING_VERIFICATION')
    report=dict(status='PASS',scope='Frozen corpus / scenario-lens SVG and native neighborhood rendering; not semantic admission or motion proof',
                sourceGeneration=catalog['sourceGeneration'],capabilities=len(rows),totals=dict(totals),nativeViews=len(native),
                roundTrip='PASS',reproducibleReveal='PASS',geometry='PASS',seconds=round(perf_counter()-started,2),results=rows,native=native,
                inputs=inputs)
    write('evaluations/scl-estate-verification.json',report)
    print('PASS',len(rows),'capabilities',totals['scenarios'],'scenario infographics',len(native),'native topology views')


if __name__=='__main__':main()
