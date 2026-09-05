"""Publish the local language workbench and reproducible draft examples."""
import json
from infographic_contract import ROOT, read, write, digest
from scl import Circuit, validate_graph, emit, graph_hash
from scl_render import compile_graph


def draft_from_projection(identity):
    p = read(f'declarations/infographics/{identity}.json')
    keys = ('id','title','sources','capabilities','scenarios','nodes','junctions','edges','providers')
    g = {k:p[k] for k in keys}; g.update(version='sidefx-circuit.v0.1',status='DRAFT',promise=p['scope'],
        trace=[e['id'] for e in p['edges'] if e['type'] in ('transition','product-transfer')
               and any(e['id'] in b['edgeIds'] for b in p['animationBeats'])])
    for n in g['nodes']+g['junctions']+g['edges']:
        if n['basis']=='DECLARED': n['basis']='TARGET'
    for s in g['sources']:
        if s['kind']=='DECLARED': s['kind']='TARGET'
    g['meanings']=[dict(nodeId=n['id'],altitude='scenario' if n['scenarioId'] else 'provider' if n['type']=='provider' else 'execution',
                        experience=n['detail'] if n['type']=='outcome' else None,
                        responsibility=n['detail'] if n['type']=='event' else None) for n in g['nodes']]
    return validate_graph(g)


def main():
    out=ROOT/'samples/scl';out.mkdir(parents=True,exist_ok=True)
    examples=[]
    for identity,label in [('scenario-target','Two probes / ALL convergence'),('scenario-current','One decision / one selected outcome')]:
        g=draft_from_projection(identity);write(f'declarations/scl/{identity}.json',g.model_dump())
        (ROOT/f'declarations/scl/{identity}.scl').write_text(emit(g),encoding='utf-8')
        result=compile_graph(g,enhanced=True)
        write(out/f'{identity}.preview.json',result)
        examples.append(dict(id=identity,label=label,scl=emit(g),graphSha256=graph_hash(g)))
    write(out/'examples.json',examples)
    for file in ('scl-studio.html','scl-studio.css','scl-studio.js','circuit-flow.js'):
        (out/('index.html' if file.endswith('.html') else file)).write_bytes((ROOT/'templates'/file).read_bytes())
    write('schemas/sidefx-circuit.v0.1.schema.json',{'$schema':'https://json-schema.org/draft/2020-12/schema',**Circuit.model_json_schema()})
    write(out/'build-receipt.json',dict(kind='SCL_WORKBENCH_BUILD',inputs={str(p.relative_to(ROOT)).replace('\\','/'):digest(p) for p in [ROOT/'scripts/scl.py',ROOT/'scripts/reveal_scl.py',ROOT/'scripts/scl_render.py',ROOT/'docs/sidefx-circuit-language (SCL).md']},
        outputs={p.name:digest(p) for p in sorted(out.glob('*')) if p.is_file() and p.name!='build-receipt.json'},admission='NOT_PERFORMED'))
    print('SCL workbench built / 2 typed drafts / shared SideFX renderer')


if __name__=='__main__':main()
