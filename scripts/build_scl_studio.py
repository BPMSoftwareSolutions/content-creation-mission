"""Publish the local language workbench and reproducible draft examples."""
import json
from infographic_contract import ROOT, read, write, digest
from scl import Circuit, validate_graph, emit, graph_hash, parse
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


def starter_scl():
    source='declarations/scl/playground-intent.json'
    return '''// Your circuit. Change the labels below and watch the preview update.
// Keep identities consistent when adding nodes, routes or scenario members.
scl "0.1";
circuit "my-circuit" {
  title "My first circuit";
  promise "Describe the human experience this capability should create.";
  status "DRAFT";

  input "request" {
    label "A request arrives"; detail "What does the person need?";
    capabilityId "my-capability"; scenarioId "happy-path";
    basis "TARGET"; sourceRefs ["design"];
  }
  event "work" {
    label "Make it happen"; detail "What mechanic changes the situation?";
    capabilityId "my-capability"; scenarioId "happy-path";
    basis "TARGET"; sourceRefs ["design"];
  }
  outcome "result" {
    label "The person gets a result"; detail "What changed for the person?";
    capabilityId "my-capability"; scenarioId "happy-path";
    basis "TARGET"; sourceRefs ["design"];
  }

  // Routes connect exact node identities. Trace selects the rolling-ball path.
  route "begin" {
    source "request"; target "work"; type "transition"; label "begin";
    basis "TARGET"; sourceRefs ["design"];
  }
  route "finish" {
    source "work"; target "result"; type "transition"; label "complete";
    basis "TARGET"; sourceRefs ["design"];
  }
  trace ["begin", "finish"];

  capability "my-capability" {
    label "My capability"; domain "My workspace";
    scenarioIds ["happy-path"]; coverage "One intended scenario";
    sourceRefs ["design"];
  }
  scenario "happy-path" {
    capabilityId "my-capability"; label "The intended experience";
    nodeIds ["request", "work", "result"]; sourceRefs ["design"];
  }
  // This identifies a draft context, not proof of implementation.
  source "design" {
    path "'''+source+'''";
    sha256 "'''+digest(ROOT/source)+'''";
    kind "TARGET"; label "User-authored design context";
  }
}
'''


def main():
    out=ROOT/'samples/scl';out.mkdir(parents=True,exist_ok=True)
    examples=[]
    for identity,label in [('scenario-target','Two probes / ALL convergence'),('scenario-current','One decision / one selected outcome')]:
        g=draft_from_projection(identity);write(f'declarations/scl/{identity}.json',g.model_dump())
        (ROOT/f'declarations/scl/{identity}.scl').write_text(emit(g),encoding='utf-8')
        result=compile_graph(g,enhanced=True)
        write(out/f'{identity}.preview.json',result)
        examples.append(dict(id=identity,label=label,scl=emit(g),graphSha256=graph_hash(g)))
    starter=starter_scl();g=parse(starter)
    (ROOT/'declarations/scl/my-circuit.scl').write_text(starter,encoding='utf-8')
    examples.insert(0,dict(id='my-circuit',label='Simple circuit / start here',scl=starter,graphSha256=graph_hash(g)))
    write(out/'examples.json',examples)
    for file in ('scl-studio.html','scl-studio.css','scl-studio.js','scl-live.js','circuit-flow.js'):
        (out/('index.html' if file.endswith('.html') else file)).write_bytes((ROOT/'templates'/file).read_bytes())
    write('schemas/sidefx-circuit.v0.1.schema.json',{'$schema':'https://json-schema.org/draft/2020-12/schema',**Circuit.model_json_schema()})
    write(out/'build-receipt.json',dict(kind='SCL_WORKBENCH_BUILD',inputs={str(p.relative_to(ROOT)).replace('\\','/'):digest(p) for p in [ROOT/'scripts/scl.py',ROOT/'scripts/reveal_scl.py',ROOT/'scripts/scl_render.py',ROOT/'scripts/build_scl_studio.py',ROOT/'declarations/scl/playground-intent.json',ROOT/'docs/sidefx-circuit-language (SCL).md',*[ROOT/'templates'/f for f in ('scl-studio.html','scl-studio.css','scl-studio.js','scl-live.js')]]},
        outputs={p.name:digest(p) for p in sorted(out.glob('*')) if p.is_file() and p.name!='build-receipt.json'},admission='NOT_PERFORMED'))
    print('SCL workbench built / 3 typed drafts / live playground / shared SideFX renderer')


if __name__=='__main__':main()
