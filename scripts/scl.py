"""SCL 0.1: a data language and candidate graph, never an execution boundary."""
import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Literal

import networkx as nx
from pydantic import Field
from infographic_contract import Strict, Source, Node, Junction, Edge, Scenario, Capability, Provider, ROOT, digest, source_value

VERSION = 'sidefx-circuit.v0.1'


class Meaning(Strict):
    nodeId: str
    altitude: Literal['scenario', 'execution', 'mechanic', 'provider'] = 'scenario'
    parentId: str | None = None
    responsibility: str | None = None
    authorityId: str | None = None
    mechanicProfile: str | None = None
    experience: str | None = None
    variants: list[str] = Field(default_factory=list)
    productIsExperience: Literal[False] = False


class Record(Strict):
    """Exact native data remains in its content-addressed source, not paraphrased."""
    id: str
    kind: Literal['cell', 'route', 'mechanic', 'provider', 'operation', 'policy', 'blueprint']
    nativeType: str
    sourceRef: str
    scenarioIds: list[str] = Field(default_factory=list)
    nativeId: str | None = None
    parentId: str | None = None


class Finding(Strict):
    code: str
    subject: str
    detail: str
    closure: str


class Circuit(Strict):
    version: Literal['sidefx-circuit.v0.1'] = VERSION
    id: str = Field(pattern=r'^[a-zA-Z0-9][a-zA-Z0-9_.-]*$')
    title: str = Field(min_length=1, max_length=120)
    promise: str = Field(min_length=1)
    status: Literal['DRAFT', 'SOURCE_REVEAL'] = 'DRAFT'
    sourceGeneration: str | None = None
    sources: list[Source] = Field(default_factory=list)
    capabilities: list[Capability] = Field(min_length=1)
    scenarios: list[Scenario] = Field(min_length=1)
    nodes: list[Node] = Field(min_length=3)
    junctions: list[Junction] = Field(default_factory=list)
    edges: list[Edge] = Field(min_length=2)
    providers: list[Provider] = Field(default_factory=list)
    meanings: list[Meaning] = Field(default_factory=list)
    records: list[Record] = Field(default_factory=list)
    findings: list[Finding] = Field(default_factory=list)
    # Empty means no chosen execution story. Routes remain visible but do not run.
    trace: list[str] = Field(default_factory=list)


def canonical_bytes(value):
    if hasattr(value, 'model_dump'): value = value.model_dump()
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':'), allow_nan=False).encode()


def graph_hash(value):
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def need(condition, message):
    if not condition: raise ValueError(message)


def resolve_sources(sources):
    documents, values = {}, {}
    for s in sources:
        key = (s.path, s.sha256, s.encoding)
        if key not in documents:
            documents[key] = source_value(s.model_copy(update={'pointer':''}))
        value = documents[key]
        if s.pointer:
            need(s.pointer.startswith('/'), 'INVALID_POINTER:' + s.id)
            for part in s.pointer[1:].split('/'):
                part = part.replace('~1', '/').replace('~0', '~')
                value = value[int(part)] if isinstance(value, list) else value[part]
        values[s.id] = value
    return values


def validate_graph(data, verify_sources=True):
    g = Circuit.model_validate(data)
    nodes = {n.id: n for n in g.nodes + g.junctions}
    edges = {e.id: e for e in g.edges}
    sources = {s.id: s for s in g.sources}
    need(len(nodes) == len(g.nodes) + len(g.junctions) and len(edges) == len(g.edges)
         and not nodes.keys() & edges.keys(), 'DUPLICATE_ID')
    need(len(sources) == len(g.sources), 'DUPLICATE_SOURCE')
    caps = {c.id: c for c in g.capabilities}; scenarios = {s.id: s for s in g.scenarios}
    need(len(caps) == len(g.capabilities) and len(scenarios) == len(g.scenarios), 'DUPLICATE_SCOPE')
    if verify_sources:
        resolve_sources(g.sources)
    for x in [*nodes.values(), *g.edges, *g.capabilities, *g.scenarios]:
        need(set(x.sourceRefs) <= sources.keys(), 'UNKNOWN_SOURCE:' + x.id)
    for n in nodes.values():
        need(n.capabilityId in caps and (n.scenarioId is None or n.scenarioId in scenarios), 'UNKNOWN_SCOPE:' + n.id)
        need(n.basis in {sources[r].kind for r in n.sourceRefs}, 'REALITY_WITHOUT_SOURCE:' + n.id)
        if g.status == 'DRAFT': need(n.basis in ('TARGET', 'GAP', 'STAGING'), 'DRAFT_CANNOT_CLAIM_CURRENT:' + n.id)
        if n.basis == 'GAP': need(bool(getattr(n, 'closure', None)), 'GAP_WITHOUT_CLOSURE:' + n.id)
    for c in g.capabilities:
        need(set(c.scenarioIds) == {s.id for s in g.scenarios if s.capabilityId == c.id}, 'SCENARIO_COVERAGE:' + c.id)
    for s in g.scenarios:
        need(s.capabilityId in caps, 'UNKNOWN_CAPABILITY:' + s.id)
        need(set(s.nodeIds) == {n.id for n in nodes.values() if n.scenarioId == s.id}, 'SCENARIO_MEMBERSHIP:' + s.id)
        need(all(nodes[i].capabilityId == s.capabilityId for i in s.nodeIds), 'SCENARIO_CAPABILITY_MISMATCH:' + s.id)
        need({'input', 'event', 'outcome'} <= {nodes[i].type for i in s.nodeIds}, 'MISSING_IEO:' + s.id)
    flow = nx.DiGraph(); flow.add_nodes_from(nodes)
    for e in g.edges:
        need(e.source in nodes and e.target in nodes, 'UNKNOWN_ENDPOINT:' + e.id)
        a, b = nodes[e.source], nodes[e.target]
        need(e.basis in {sources[r].kind for r in e.sourceRefs}, 'EDGE_WITHOUT_REALITY_SOURCE:' + e.id)
        if e.type in ('transition', 'product-transfer', 'retry'):
            need(a.basis == b.basis == e.basis, 'MIXED_REALITY_FLOW:' + e.id)
            need(a.basis != 'GAP', 'GAP_CANNOT_EXECUTE:' + e.id)
            if a.capabilityId != b.capabilityId: need(e.type == 'product-transfer', 'CROSS_CAPABILITY_NEEDS_PRODUCT:' + e.id)
            if e.type != 'retry': flow.add_edge(a.id, b.id)
        if e.type == 'product-transfer':
            need(a.type == 'outcome' and b.type == 'input' and bool(e.productContract)
                 and e.productContract == a.productContract == b.productContract, 'PRODUCT_CONTRACT_MISMATCH:' + e.id)
        if e.type == 'provider-binding': need(a.type == 'provider' and b.type == 'provider-port', 'INVALID_PROVIDER_BINDING:' + e.id)
        if e.type == 'authority': need(a.type == 'authority', 'INVALID_AUTHORITY_EDGE:' + e.id)
        if e.type == 'evidence-attachment': need('evidence' in (a.type, b.type), 'INVALID_EVIDENCE_EDGE:' + e.id)
        if e.type == 'retry':
            need(bool(e.maxAttempts and e.exitCondition) and e.stopTarget in nodes, 'UNBOUNDED_RETRY:' + e.id)
            need(nodes[e.stopTarget].type in ('termination', 'rejection'), 'RETRY_WITHOUT_STOP:' + e.id)
    need(nx.is_directed_acyclic_graph(flow), 'UNDECLARED_CYCLE')
    for n in nodes.values():
        ins, outs = flow.in_degree(n.id), flow.out_degree(n.id)
        if n.type in ('branch', 'decision', 'fan-out'): need(ins == 1 and outs >= 2, 'JUNCTION_CARDINALITY:' + n.id)
        if n.type in ('branch', 'decision'):
            routes = [e for e in g.edges if e.source == n.id and e.type == 'transition']
            guards = [e.guard for e in routes]
            need(bool(n.rule) and all(guards) and guards.count('otherwise') == 1 and len(set(guards)) == len(guards), 'INCOMPLETE_SELECTION:' + n.id)
        if n.type == 'convergence':
            need(ins >= 2 and outs == 1 and bool(n.join), 'INCOMPLETE_JOIN:' + n.id)
            if n.join == 'quorum': need(n.quorum is not None and n.quorum <= ins, 'INVALID_QUORUM:' + n.id)
        if n.type in ('termination', 'rejection'):
            need(not any(e.source == n.id and e.type in ('transition', 'product-transfer', 'retry') for e in g.edges), 'TERMINAL_CONTINUES:' + n.id)
        if ins > 1: need(n.type == 'convergence', 'UNTYPED_MERGE:' + n.id)
        if outs > 1: need(n.type in ('branch', 'decision', 'fan-out'), 'UNTYPED_SPLIT:' + n.id)
    for e in g.edges:
        if e.type == 'retry':
            need(nx.has_path(flow, e.target, e.source), 'RETRY_IS_NOT_RETURN:' + e.id)
            need(nodes[e.source].capabilityId == nodes[e.stopTarget].capabilityId, 'RETRY_STOP_SCOPE:' + e.id)
    for s in g.scenarios:
        starts = [i for i in s.nodeIds if nodes[i].type == 'input']
        for end in (i for i in s.nodeIds if nodes[i].type == 'outcome'):
            need(any(nx.has_path(flow, start, end) for start in starts), 'UNREACHABLE_OUTCOME:' + end)
    ports = {n.id for n in g.nodes if n.type == 'provider-port'}; bound = set()
    for p in g.providers:
        need(set(p.portIds) <= ports and not set(p.portIds) & bound, 'INVALID_OR_DUPLICATE_PROVIDER_SLOT')
        bindings = [e for e in g.edges if e.type == 'provider-binding' and e.target in p.portIds]
        if p.binding == 'open': need(p.nodeId is None and not bindings and p.state in ('unknown', 'isolated'), 'OPEN_SLOT_HAS_PROVIDER')
        else:
            need(p.nodeId in nodes and nodes[p.nodeId].type == 'provider', 'UNKNOWN_PROVIDER')
            need({e.target for e in bindings if e.source == p.nodeId} == set(p.portIds), 'MISSING_PROVIDER_BINDING')
            if p.state == 'active': need(p.binding == 'bound' and nodes[p.nodeId].basis == 'OBSERVED', 'UNPROVEN_ACTIVE_PROVIDER')
        bound.update(p.portIds)
    need(bound == ports, 'UNBOUND_PROVIDER_SLOT')
    meanings = {m.nodeId: m for m in g.meanings}
    need(len(meanings) == len(g.meanings) and meanings.keys() <= nodes.keys(), 'INVALID_MEANING_ID')
    hierarchy = nx.DiGraph(); hierarchy.add_nodes_from(nodes)
    for m in g.meanings:
        need(len(m.variants) == len(set(m.variants)), 'DUPLICATE_VARIANT:' + m.nodeId)
        if m.parentId:
            need(m.parentId in nodes, 'UNKNOWN_PARENT:' + m.nodeId); hierarchy.add_edge(m.parentId, m.nodeId)
            need(nodes[m.parentId].capabilityId == nodes[m.nodeId].capabilityId, 'CROSS_CAPABILITY_CONTAINMENT')
            if m.parentId in meanings:
                levels = {'scenario':0,'execution':1,'mechanic':2,'provider':3}
                need(levels[m.altitude] >= levels[meanings[m.parentId].altitude], 'ALTITUDE_INVERSION:' + m.nodeId)
    need(nx.is_directed_acyclic_graph(hierarchy), 'CONTAINMENT_CYCLE')
    need(len({r.id for r in g.records}) == len(g.records), 'DUPLICATE_RECORD')
    for r in g.records:
        need(r.sourceRef in sources and set(r.scenarioIds) <= scenarios.keys(), 'INVALID_NATIVE_RECORD:' + r.id)
    need(len(g.trace) == len(set(g.trace)) and set(g.trace) <= edges.keys(), 'INVALID_TRACE')
    # Selection is an authored illustration; guards are never evaluated as code.
    if g.trace:
        chosen = [edges[i] for i in g.trace]
        need(all(e.type in ('transition', 'product-transfer') for e in chosen), 'TRACE_UNSUPPORTED_RELATION')
        used = {i for e in chosen for i in (e.source, e.target)}
        for i in used:
            n = nodes[i]; incoming = [e for e in chosen if e.target == i]; outgoing = [e for e in chosen if e.source == i]
            if not incoming: need(n.type == 'input', 'TRACE_MUST_START_AT_INPUT:' + i)
            if not outgoing: need(n.type in ('outcome', 'termination', 'rejection'), 'TRACE_INCOMPLETE_END:' + i)
            if n.type == 'fan-out': need(len(outgoing) == flow.out_degree(i), 'TRACE_INCOMPLETE_FANOUT:' + i)
            if n.type in ('branch', 'decision'): need(len(outgoing) == 1, 'TRACE_EXECUTES_ALTERNATIVES:' + i)
            if n.type == 'convergence':
                required = flow.in_degree(i) if n.join == 'all' else 1 if n.join == 'any' else n.quorum
                need(len(incoming) >= required, 'TRACE_INCOMPLETE_JOIN:' + i)
    return g


# Every property value is strict JSON. Braces delimit typed declarations, not code.
# Strings use JSON escaping. No eval, expressions, include, macros, or network imports.
class Parser:
    whitespace = re.compile(r'(?:\s+|//[^\n]*(?:\n|$))')
    keyword = re.compile(r'[a-zA-Z][a-zA-Z0-9_-]*')
    def __init__(self, text): self.text, self.pos = text, 0
    def error(self, message):
        line = self.text.count('\n', 0, self.pos) + 1
        col = self.pos - self.text.rfind('\n', 0, self.pos)
        raise ValueError(f'SCL_SYNTAX {line}:{col}: {message}')
    def space(self):
        while True:
            m = self.whitespace.match(self.text, self.pos)
            if not m: return
            self.pos += len(m[0])
    def token(self, value):
        self.space()
        if not self.text.startswith(value, self.pos): self.error('expected ' + value)
        self.pos += len(value)
    def word(self):
        self.space(); m = self.keyword.match(self.text, self.pos)
        if not m: self.error('expected keyword')
        self.pos += len(m[0]); return m[0]
    def value(self):
        self.space()
        def pairs(items):
            obj = {}
            for k, v in items:
                if k in obj: self.error('duplicate JSON property ' + k)
                obj[k] = v
            return obj
        def constant(value): self.error('non-finite number ' + value)
        try: value, end = json.JSONDecoder(object_pairs_hook=pairs, parse_constant=constant).raw_decode(self.text, self.pos)
        except json.JSONDecodeError as e: self.pos = e.pos; self.error(e.msg)
        self.pos = end; return value
    def props(self):
        self.token('{'); result = {}
        while True:
            self.space()
            if self.text[self.pos:self.pos+1] == '}': self.pos += 1; return result
            key = self.word()
            if key in result: self.error('duplicate property ' + key)
            result[key] = self.value(); self.token(';')
    def parse(self):
        self.token('scl'); version = self.value(); self.token(';')
        if version != '0.1': self.error('unsupported version')
        self.token('circuit'); identity = self.value(); self.token('{')
        data = dict(version=VERSION, id=identity)
        collections = {'source':'sources','capability':'capabilities','scenario':'scenarios','node':'nodes',
                       'junction':'junctions','route':'edges','binding':'providers','meaning':'meanings','record':'records','finding':'findings'}
        node_types = {'input','event','outcome','provider-port','provider','validation','evidence','human-approval','authority'}
        junction_types = {'branch','fan-out','convergence','decision','termination','rejection'}
        while True:
            self.space()
            if self.text[self.pos:self.pos+1] == '}': self.pos += 1; break
            key = self.word()
            if key in collections or key in node_types or key in junction_types:
                self.space()
                identity = None if self.text[self.pos:self.pos+1] == '{' else self.value()
                value = self.props()
                if identity is not None:
                    if 'id' in value: self.error('identity given twice')
                    value['id'] = identity
                if key in node_types or key in junction_types:
                    if 'type' in value: self.error('type given twice')
                    value['type'] = key
                    field = 'nodes' if key in node_types else 'junctions'
                else: field = collections[key]
                data.setdefault(field, []).append(value)
            else:
                if key in data or key in collections.values(): self.error('duplicate or reserved property ' + key)
                data[key] = self.value(); self.token(';')
        self.space()
        if self.pos != len(self.text): self.error('trailing input')
        return data


def parse(text, verify_sources=True): return validate_graph(Parser(text).parse(), verify_sources)


def emit(graph):
    g = graph.model_dump(); out = ['scl "0.1";', 'circuit ' + json.dumps(g.pop('id')) + ' {']; g.pop('version')
    names = {'sources':'source','capabilities':'capability','scenarios':'scenario','nodes':'node','junctions':'junction',
             'edges':'route','providers':'binding','meanings':'meaning','records':'record','findings':'finding'}
    for key, value in g.items():
        if key in names:
            for item in value:
                item = dict(item)
                keyword = item.pop('type') if key in ('nodes','junctions') else names[key]
                identity = (' ' + json.dumps(item.pop('id'))) if 'id' in item else ''
                out.append('  ' + keyword + identity + ' {')
                for k, v in item.items():
                    if v is not None: out.append('    ' + k + ' ' + json.dumps(v, ensure_ascii=False) + ';')
                out.append('  }')
        else: out.append('  ' + key + ' ' + json.dumps(value, ensure_ascii=False) + ';')
    return '\n'.join(out + ['}', ''])


def handoff(graph):
    return dict(kind='SCL_BLUEPRINT_DESIGN_TESTIMONY',graphSha256=graph_hash(graph),candidateGraph=graph.model_dump(),
        admission='NOT_PERFORMED',execution='NOT_AVAILABLE',changeMode='UNRESOLVED',
        obligations=['Resolve FIRST_ADMISSION or REVISION and the exact predecessor when applicable.',
            'Resolve current managed authoring contracts and admit an SCL-to-blueprint adapter.',
            'Resolve exact input/output contracts, responsibility authorities and semantic progress.',
            'Qualify provider-candidate completeness and mechanic feasibility through the managed dependencies.',
            'Approve and admit the blueprint, then follow the current governed capability-change lifecycle.'],
        openFindings=[f.model_dump() for f in graph.findings])


def main():
    p = argparse.ArgumentParser(description=__doc__); p.add_argument('input', nargs='?'); p.add_argument('--output'); p.add_argument('--schema', action='store_true'); p.add_argument('--handoff', action='store_true'); a = p.parse_args()
    if a.schema:
        data = {'$schema':'https://json-schema.org/draft/2020-12/schema', **Circuit.model_json_schema()}
    else:
        path = Path(a.input); g = parse(path.read_text(encoding='utf-8')) if path.suffix == '.scl' else validate_graph(json.loads(path.read_bytes()))
        data = handoff(g) if a.handoff else g.model_dump()
        print('VALID_CANDIDATE', g.id, graph_hash(g), '(not admitted or executable)')
    if a.output: Path(a.output).write_text(json.dumps(data, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')


if __name__ == '__main__': main()
