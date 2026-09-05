"""A named SCL lens lowers into the existing, unchanged SideFX SVG grammar."""
import argparse
import json
from functools import lru_cache
from pathlib import Path

from infographic_contract import ROOT, Projection, digest, write
from compile_infographics import layout, render, inspect_geometry, measure_rendered_junctions, font
from scl import validate_graph, parse, emit, graph_hash, need, resolve_sources


def lower(g, scenario_id):
    scenario = next((s for s in g.scenarios if s.id == scenario_id), None)
    need(scenario is not None, 'UNKNOWN_SCENARIO')
    cap = next(c for c in g.capabilities if c.id == scenario.capabilityId)
    items = [n for n in g.nodes + g.junctions if n.scenarioId == scenario_id or n.scenarioId is None and n.capabilityId == cap.id]
    ids = {n.id for n in items}; edges = [e for e in g.edges if e.source in ids and e.target in ids]
    edgeids = {e.id for e in edges}; trace = [e for e in g.trace if e in edgeids]
    need(not trace or set(trace) == set(g.trace), 'TRACE_CROSSES_LENS_BOUNDARY')
    phases = ['Establish','Activate','Execute','Resolve','Prove']
    beats = [dict(phase=p, caption='Selected declared structure; illustrative timing, never execution testimony.',
                  entityIds=[], edgeIds=trace if i == 2 else []) for i, p in enumerate(phases)]
    def visual_node(n):
        data=n.model_dump();data.pop('plane',None);return data
    language=g.version.rsplit('v',1)[-1]
    data = dict(contractVersion='infographic-projection.v1',grammarVersion='sidefx-infographic-grammar.v1',
        id=g.id,title=scenario.label[:100],subtitle='SCL '+language+' / '+('Target design' if g.status=='DRAFT' else 'Declared source boundary'),
        altitude='scenario',scope='A scenario lens over '+graph_hash(g)+'. Native records and omitted relationships remain in SCL. No live effect proof.',
        sources=[s.model_dump() for s in g.sources],capabilities=[{**cap.model_dump(),'scenarioIds':[scenario_id]}],
        scenarios=[scenario.model_dump()],nodes=[visual_node(n) for n in g.nodes if n.id in ids],junctions=[visual_node(n) for n in g.junctions if n.id in ids],
        edges=[e.model_dump() for e in edges],providers=[p.model_dump() for p in g.providers if set(p.portIds)<=ids],
        humanAnchors=[dict(person='Declared input',input='Read the input contract and its source.',event='Open the responsibility and its mechanics.',
                           outcome='Separate the promised experience from its product.',basis='STAGING',sourceRefs=[g.sources[0].id])],
        visualLayers=['human','mechanic','support'],animationBeats=beats,
        zoomAggregations=[dict(id='scope',label=cap.label,altitude='capability',memberIds=sorted(ids))],scenarioRelationships=[])
    # SCL is validated before lowering. Virtual presentation captions are not source claims.
    return Projection.model_validate(data)


@lru_cache(maxsize=1)
def materials():
    from enhance_infographics import asset_receipts
    return asset_receipts()


def compile_graph(g, scenario_id=None, enhanced=False):
    scenario_id = scenario_id or g.scenarios[0].id
    p = lower(g, scenario_id); geo = layout(p)
    # The source label stays in the graph; the fixed-height editorial header is one line.
    title=p.title
    while title and font(38,True).getlength(title+'…')>geo['width']-88:title=title[:-1]
    if title!=p.title:p=p.model_copy(update={'title':title.rstrip()+'…'})
    findings = inspect_geometry(p, geo); need(not findings, 'GEOMETRY:' + str(findings))
    svg = render(p, geo); contacts = measure_rendered_junctions(p, svg)
    need(not contacts['findings'], 'JUNCTION_GEOMETRY:' + str(contacts['findings']))
    compiled = {**p.model_dump(),'layout':geo}
    if g.version=='sidefx-circuit.v0.2':
        compiled['semanticPlanes']={n.id:n.plane for n in g.nodes+g.junctions if n.id in {x.id for x in p.nodes+p.junctions}}
        # Keep the full structured trace in the export; the established scheduler
        # derives simultaneous flights and ALL release from the validated topology.
        compiled['traceGeometry']=[t.model_dump() for t in g.traces if t.scenarioId==scenario_id]
        compiled['selectedTrace']=g.selectedTrace
    if enhanced:
        from enhance_infographics import composite
        svg, _ = composite(svg, compiled, materials())
    visible_ids = {n.id for n in p.nodes+p.junctions}
    receipt = dict(kind='SCL_VISUAL_PROJECTION',graphSha256=graph_hash(g),scenarioId=scenario_id,
        sourceGeneration=g.sourceGeneration,visibleNodes=len(visible_ids),totalNodes=len(g.nodes)+len(g.junctions),
        visibleEdges=len(p.edges),totalEdges=len(g.edges),retainedNativeRecords=len(g.records),
        hiddenNodes=[n.id for n in g.nodes+g.junctions if n.id not in visible_ids],
        hiddenEdges=[e.id for e in g.edges if e.id not in {x.id for x in p.edges}],
        nativeRecordsAreExecutionAnimation=False,geometryFindings=findings,junctions=contacts,
        rendererSha256=digest(ROOT/'scripts/compile_infographics.py'),grammarSha256=digest(ROOT/'declarations/infographic-grammar.v1.json'),
        effect='NONE',admission='NOT_PERFORMED',enhanced=enhanced)
    if g.version=='sidefx-circuit.v0.2':
        node_types={n.id:n.type for n in p.nodes}
        required=[(e.source,e.target) if node_types.get(e.source)=='evidence' else (e.target,e.source) for e in p.edges
            if e.type=='evidence-attachment' and {node_types.get(e.source),node_types.get(e.target)}=={'evidence','outcome'}]
        receipt['evidenceRequirements']=[dict(evidenceId=evidence,outcomeId=outcome,basis=next(n for n in p.nodes if n.id==evidence).basis,established=False) for evidence,outcome in required]
        receipt['proofDisposition']='NOT_ESTABLISHED' if required else 'NO_EVIDENCE_REQUIREMENT_DECLARED'
        receipt['languageVersion']='0.2';receipt['selectedTrace']=g.selectedTrace
    return dict(svg=svg,projection=compiled,receipt=receipt)


def native_records(g, scenario_id):
    refs = {r.sourceRef for r in g.records if not r.scenarioIds or scenario_id in r.scenarioIds}
    values = resolve_sources([s for s in g.sources if s.id in refs])
    # Records expose exact objects, including original configuration, guards and bounds.
    return [{**r.model_dump(),'value':values[r.sourceRef]} for r in g.records if r.sourceRef in refs]


def main():
    p = argparse.ArgumentParser(description=__doc__); p.add_argument('input'); p.add_argument('--scenario'); p.add_argument('--trace'); p.add_argument('--enhanced',action='store_true'); p.add_argument('--output',required=True); a=p.parse_args()
    path=Path(a.input);g=parse(path.read_text(encoding='utf-8')) if path.suffix=='.scl' else validate_graph(json.loads(path.read_bytes()))
    if a.trace:
        from scl_v02 import select_trace
        g=select_trace(g,a.trace)
    result=compile_graph(g,a.scenario,a.enhanced);out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
    (out/'infographic.svg').write_text(result.pop('svg'),encoding='utf-8');write(out/'projection.json',result['projection']);write(out/'receipt.json',result['receipt'])
    print('RENDERED',g.id,result['receipt']['scenarioId'])


if __name__=='__main__':main()
