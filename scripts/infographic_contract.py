"""Typed projection authority and graph/provenance conformance. No drawing here."""
import hashlib
import base64
import json
from pathlib import Path
from typing import Literal

import networkx as nx
from pydantic import BaseModel, ConfigDict, Field

ROOT=Path(__file__).resolve().parents[1]
Mode=Literal['DECLARED','OBSERVED','TARGET','GAP','STAGING']
NodeType=Literal['input','event','outcome','provider-port','provider','validation','evidence','human-approval','authority']
JunctionType=Literal['branch','fan-out','convergence','decision','termination','rejection']
EdgeType=Literal['transition','product-transfer','provider-binding','evidence-attachment','authority','dependency','retry']
Phase=Literal['Establish','Activate','Execute','Resolve','Prove']

class Strict(BaseModel):
    model_config=ConfigDict(extra='forbid',strict=True)

class Source(Strict):
    id:str
    path:str
    sha256:str=Field(pattern=r'^[a-f0-9]{64}$')
    pointer:str=''
    kind:Mode
    label:str
    encoding:Literal['json','capsule-entry']='json'

class Entity(Strict):
    id:str
    label:str=Field(min_length=1,max_length=90)
    detail:str=Field(max_length=160)
    capabilityId:str
    scenarioId:str|None=None
    basis:Mode
    sourceRefs:list[str]=Field(min_length=1)
    layer:Literal['mechanic','support']='mechanic'

class Node(Entity):
    type:NodeType
    productContract:str|None=None
    closure:str|None=None

class Junction(Entity):
    type:JunctionType
    rule:str|None=None
    join:Literal['all','any','quorum']|None=None
    quorum:int|None=Field(default=None,ge=1)

class Edge(Strict):
    id:str
    source:str
    target:str
    type:EdgeType
    label:str=Field(max_length=100)
    basis:Mode
    sourceRefs:list[str]=Field(min_length=1)
    guard:str|None=None
    productContract:str|None=None
    maxAttempts:int|None=Field(default=None,ge=1,le=100)
    exitCondition:str|None=None
    stopTarget:str|None=None

class Scenario(Strict):
    id:str
    capabilityId:str
    label:str
    nodeIds:list[str]=Field(min_length=3)
    sourceRefs:list[str]=Field(min_length=1)

class Capability(Strict):
    id:str
    label:str
    domain:str
    scenarioIds:list[str]=Field(min_length=1)
    coverage:str
    sourceRefs:list[str]=Field(min_length=1)

class Provider(Strict):
    nodeId:str|None
    portIds:list[str]=Field(min_length=1)
    binding:Literal['bound','candidate','open']
    state:Literal['active','candidate','simulated','degraded','isolated','unknown']

class Human(Strict):
    person:str
    input:str
    event:str
    outcome:str
    basis:Mode
    sourceRefs:list[str]=Field(min_length=1)

class Beat(Strict):
    phase:Phase
    caption:str
    entityIds:list[str]
    edgeIds:list[str]

class Aggregation(Strict):
    id:str
    label:str
    altitude:Literal['capability','estate']
    memberIds:list[str]=Field(min_length=1)

class Relationship(Strict):
    sourceScenario:str
    targetScenario:str
    kind:Literal['invokes','depends-on']
    sourceRefs:list[str]=Field(min_length=1)

class Projection(Strict):
    contractVersion:Literal['infographic-projection.v1']
    grammarVersion:Literal['sidefx-infographic-grammar.v1']
    id:str
    title:str
    subtitle:str
    altitude:Literal['scenario','capability','estate']
    scope:str
    sources:list[Source]=Field(min_length=1)
    capabilities:list[Capability]=Field(min_length=1)
    scenarios:list[Scenario]=Field(min_length=1)
    nodes:list[Node]=Field(min_length=3)
    junctions:list[Junction]
    edges:list[Edge]=Field(min_length=2)
    providers:list[Provider]
    humanAnchors:list[Human]=Field(min_length=1)
    visualLayers:list[Literal['human','mechanic','support']]
    animationBeats:list[Beat]=Field(min_length=5,max_length=5)
    zoomAggregations:list[Aggregation]
    scenarioRelationships:list[Relationship]

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def read(path):return json.loads((ROOT/path).read_bytes())
def write(path,data):
    path=ROOT/path;path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

def source_value(source):
    path=(ROOT/source.path).resolve()
    if not path.is_relative_to(ROOT) or not path.is_file():raise ValueError('SOURCE_PATH:'+source.id)
    if digest(path)!=source.sha256:raise ValueError('STALE_SOURCE:'+source.id)
    value=read(source.path)
    if source.encoding=='capsule-entry':
        raw=base64.b64decode(value['entryBytesBase64'],validate=True)
        if 'sha256:'+hashlib.sha256(raw).hexdigest()!=value['entryDigest']:raise ValueError('ENTRY_DIGEST:'+source.id)
        value=json.loads(raw)
    if not source.pointer:return value
    if not source.pointer.startswith('/'):raise ValueError('JSON_POINTER:'+source.id)
    for part in source.pointer[1:].split('/'):
        part=part.replace('~1','/').replace('~0','~')
        value=value[int(part)] if isinstance(value,list) else value[part]
    return value

def validate(data):
    p=Projection.model_validate(data)
    def require(condition,code):
        if not condition:raise ValueError(code)
    items=p.nodes+p.junctions;ids={n.id:n for n in items};edges={e.id:e for e in p.edges};sources={s.id:s for s in p.sources}
    require(len(ids)==len(items) and len(edges)==len(p.edges) and not set(ids)&set(edges),'DUPLICATE_ID')
    require(len(sources)==len(p.sources),'DUPLICATE_SOURCE')
    for source in p.sources:source_value(source)
    for x in [*items,*p.edges,*p.scenarios,*p.capabilities,*p.humanAnchors,*p.scenarioRelationships]:
        require(set(x.sourceRefs)<=set(sources),'UNKNOWN_SOURCE')
    for n in items:
        kinds={sources[s].kind for s in n.sourceRefs}
        require(n.basis in kinds,'REALITY_WITHOUT_SOURCE:'+n.id)
        if n.basis=='GAP':require(bool(getattr(n,'closure',None)),'GAP_WITHOUT_CLOSURE:'+n.id)
    caps={c.id:c for c in p.capabilities};scenarios={s.id:s for s in p.scenarios}
    require(len(caps)==len(p.capabilities) and len(scenarios)==len(p.scenarios),'DUPLICATE_GROUP')
    require(all(n.capabilityId in caps for n in items),'UNKNOWN_CAPABILITY')
    require(all(n.scenarioId is None or n.scenarioId in scenarios for n in items),'UNKNOWN_SCENARIO')
    for c in p.capabilities:
        require(set(c.scenarioIds)=={s.id for s in p.scenarios if s.capabilityId==c.id},'SCENARIO_COVERAGE:'+c.id)
    for s in p.scenarios:
        require(set(s.nodeIds)<=set(ids),'UNKNOWN_SCENARIO_NODE')
        require(set(s.nodeIds)=={n.id for n in items if n.scenarioId==s.id},'SCENARIO_MEMBERSHIP:'+s.id)
        require({'input','event','outcome'}<={ids[i].type for i in s.nodeIds},'MISSING_IEO:'+s.id)
    for r in p.scenarioRelationships:
        require(r.sourceScenario in scenarios and r.targetScenario in scenarios,'UNKNOWN_SCENARIO_RELATIONSHIP')
    flow=nx.DiGraph();flow.add_nodes_from(ids)
    for e in p.edges:
        require(e.source in ids and e.target in ids,'UNKNOWN_ENDPOINT:'+e.id)
        a,b=ids[e.source],ids[e.target]
        require(e.basis in {sources[s].kind for s in e.sourceRefs},'EDGE_WITHOUT_REALITY_SOURCE:'+e.id)
        if e.type in ('transition','product-transfer','retry'):
            require(a.basis==b.basis==e.basis,'MIXED_REALITY_FLOW:'+e.id)
            require(e.basis in {sources[s].kind for s in e.sourceRefs},'EDGE_WITHOUT_REALITY_SOURCE:'+e.id)
            if e.type!='retry':flow.add_edge(a.id,b.id,id=e.id)
            if a.capabilityId!=b.capabilityId:require(e.type=='product-transfer','UNDECLARED_CROSS_CAPABILITY_FLOW:'+e.id)
        if e.type=='product-transfer':
            require(a.type=='outcome' and b.type=='input' and a.capabilityId!=b.capabilityId,'INVALID_PRODUCT_ENDPOINTS:'+e.id)
            require(bool(e.productContract) and e.productContract==a.productContract==b.productContract,'PRODUCT_CONTRACT_MISMATCH:'+e.id)
        if e.type=='provider-binding':require(a.type=='provider' and b.type=='provider-port','INVALID_PROVIDER_BINDING:'+e.id)
        if e.type=='evidence-attachment':require('evidence' in (a.type,b.type),'INVALID_EVIDENCE_ATTACHMENT:'+e.id)
        if e.type=='authority':require(a.type=='authority','INVALID_AUTHORITY_EDGE:'+e.id)
        if e.type=='retry':
            require(bool(e.maxAttempts and e.exitCondition) and e.stopTarget in ids,'UNBOUNDED_RETRY:'+e.id)
            require(ids[e.stopTarget].type in ('termination','rejection'),'RETRY_WITHOUT_STOP:'+e.id)
    require(nx.is_directed_acyclic_graph(flow),'UNDECLARED_CYCLE')
    for n in p.junctions:
        ins,outs=flow.in_degree(n.id),flow.out_degree(n.id)
        if n.type in ('branch','decision','fan-out'):require(ins==1 and outs>=2,'JUNCTION_CARDINALITY:'+n.id)
        if n.type in ('branch','decision'):
            outgoing=[e for e in p.edges if e.source==n.id and e.type=='transition']
            require(bool(n.rule) and all(e.guard for e in outgoing) and sum(e.guard=='otherwise' for e in outgoing)==1,'INCOMPLETE_BRANCH:'+n.id)
            require(len({e.guard for e in outgoing})==len(outgoing),'DUPLICATE_GUARD:'+n.id)
        if n.type=='convergence':
            require(ins>=2 and outs==1 and n.join is not None,'INCOMPLETE_JOIN:'+n.id)
            if n.join=='quorum':require(n.quorum is not None and n.quorum<=ins,'INVALID_QUORUM:'+n.id)
        if n.type=='termination':require(not any(e.source==n.id and e.type in ('transition','product-transfer','retry') for e in p.edges),'TERMINAL_CONTINUES:'+n.id)
    for e in p.edges:
        if e.type=='retry':
            require(nx.has_path(flow,e.target,e.source),'RETRY_IS_NOT_RETURN:'+e.id)
            require(ids[e.stopTarget].capabilityId==ids[e.source].capabilityId,'RETRY_STOP_SCOPE:'+e.id)
    for s in p.scenarios:
        starts=[i for i in s.nodeIds if ids[i].type=='input'];ends=[i for i in s.nodeIds if ids[i].type=='outcome']
        require(all(any(nx.has_path(flow,a,b) for a in starts) for b in ends),'UNREACHABLE_OUTCOME:'+s.id)
    ports={n.id for n in p.nodes if n.type=='provider-port'};bound=set()
    for provider in p.providers:
        require(set(provider.portIds)<=ports,'UNKNOWN_PROVIDER_PORT')
        if provider.binding=='open':
            require(provider.nodeId is None and provider.state in ('unknown','isolated'),'OPEN_PORT_HAS_FULFILLER')
            require(not any(e.type=='provider-binding' and e.target in provider.portIds for e in p.edges),'OPEN_PORT_HAS_BINDING')
            bound.update(provider.portIds);continue
        require(provider.nodeId in ids and ids[provider.nodeId].type=='provider','UNKNOWN_PROVIDER')
        for port in provider.portIds:
            require(any(e.type=='provider-binding' and e.source==provider.nodeId and e.target==port for e in p.edges),'MISSING_PROVIDER_EDGE:'+port)
        if provider.state=='active':require(ids[provider.nodeId].basis=='OBSERVED' and provider.binding=='bound','UNPROVEN_ACTIVE_PROVIDER')
        bound.update(provider.portIds)
    require(bound==ports,'UNBOUND_PROVIDER_PORT')
    require(p.visualLayers==['human','mechanic','support'],'VISUAL_LAYER_ORDER')
    require([b.phase for b in p.animationBeats]==['Establish','Activate','Execute','Resolve','Prove'],'MOTION_PHASE_ORDER')
    highlighted=set()
    for beat in p.animationBeats:
        require(set(beat.entityIds)<=set(ids) and set(beat.edgeIds)<=set(edges),'UNKNOWN_MOTION_ENTITY')
        highlighted.update(beat.edgeIds)
    for n in p.junctions:
        if n.type in ('branch','decision'):
            require(sum(e.id in highlighted for e in p.edges if e.source==n.id and e.type=='transition')<=1,'MOTION_EXECUTES_ALTERNATIVES:'+n.id)
    for group in p.zoomAggregations:
        require(set(group.memberIds)<=set(ids) and len(group.memberIds)==len(set(group.memberIds)),'INVALID_AGGREGATION')
    require(set().union(*(set(g.memberIds) for g in p.zoomAggregations))==set(ids),'AGGREGATION_DROPS_MEMBERS')
    return p

if __name__=='__main__':
    write('schemas/infographic-projection.schema.json',{'$schema':'https://json-schema.org/draft/2020-12/schema',**Projection.model_json_schema()})
    print('Infographic projection schema exported from strict typed models.')
