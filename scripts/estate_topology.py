"""Source-profile adapters and graph science for complete estate diagrams.

Blueprint routes, native control flow and expression dependencies retain separate
relation vocabularies. Nothing in this module executes a mechanic or a provider.
"""
import copy, hashlib, json
from collections import Counter
import networkx as nx
from scl import resolve_sources, need

PROFILE='sidefx-estate-topology.v1'
def key(value):return 'n-'+hashlib.sha256(value.encode()).hexdigest()[:24]
def readable(value):return str(value).replace('-', ' ').replace('_',' ')
def source_at(source,pointer):return {**source,'pointer':source.get('pointer','')+pointer}

class Diagram:
    def __init__(self,identity,label,kind,source):
        self.id=key(identity);self.identity=identity;self.label=label;self.kind=kind;self.source=source
        self.nodes={};self.edges=[];self.expected_nodes=[];self.expected_edges=[];self.findings=[]
    def node(self,identity,kind,label,detail='',source=None,**facts):
        nid=key(self.identity+'|'+identity)
        if nid not in self.nodes:
            self.nodes[nid]={'id':nid,'identity':identity,'kind':kind,'label':label,'detail':detail,'source':source or self.source,'facts':facts}
        return nid
    def edge(self,identity,a,b,kind,label='',source=None,**facts):
        self.edges.append({'id':key(self.identity+'|edge|'+identity),'identity':identity,'source':a,'target':b,'kind':kind,'label':label or kind,'provenance':source or self.source,'facts':facts})
    def finish(self):
        need(len({e['id'] for e in self.edges})==len(self.edges),'TOPOLOGY_DUPLICATE_EDGE')
        need(all(e['source'] in self.nodes and e['target'] in self.nodes for e in self.edges),'TOPOLOGY_DANGLING_RENDER_EDGE')
        graph=nx.MultiDiGraph();graph.add_nodes_from(self.nodes)
        for e in self.edges:graph.add_edge(e['source'],e['target'],key=e['id'])
        cycles=[sorted(c) for c in nx.strongly_connected_components(graph) if len(c)>1 or any(graph.has_edge(n,n) for n in c)]
        actual_nodes={n['identity'] for n in self.nodes.values()};actual_edges={e['identity'] for e in self.edges}
        need(set(self.expected_nodes)<=actual_nodes,'TOPOLOGY_SOURCE_NODE_OMITTED')
        need(set(self.expected_edges)<=actual_edges,'TOPOLOGY_SOURCE_EDGE_OMITTED')
        analytics={'engine':'networkx','version':nx.__version__,'nodes':len(self.nodes),'edges':len(self.edges),
            'sourceNodes':len(self.expected_nodes),'sourceEdges':len(self.expected_edges),'omittedSourceNodes':0,'omittedSourceEdges':0,
            'nodeKinds':dict(Counter(n['kind'] for n in self.nodes.values())),'routeKinds':dict(Counter(e['kind'] for e in self.edges)),
            'weakComponents':nx.number_weakly_connected_components(graph) if graph else 0,'cyclicComponents':cycles,
            'roots':[n for n,d in graph.in_degree() if d==0],'leaves':[n for n,d in graph.out_degree() if d==0]}
        return {'version':PROFILE,'id':self.id,'identity':self.identity,'label':self.label,'kind':self.kind,'source':self.source,
            'nodes':list(self.nodes.values()),'edges':self.edges,'analytics':analytics,'findings':self.findings}

BLUEPRINT_KINDS={'responsibility':'event','state':'input','junction':'decision','convergence':'convergence','terminal':'termination','provider-slot':'provider-port','outcome':'outcome'}
BLUEPRINT_ROUTES={'TRANSITION','FAN_OUT_MEMBER','CONVERGENCE_REQUIREMENT','BRANCH_ROUTE','ALTITUDE_DESCENT','BOUNDED_RETURN'}

def blueprint_view(capability,body,source):
    d=Diagram(capability+'/blueprint', 'Capability blueprint','blueprint',source)
    ids={};native={n['nodeId']:n for n in body.get('nodes',[])}
    need(len(native)==len(body.get('nodes',[])),'BLUEPRINT_DUPLICATE_NODE')
    for i,n in enumerate(body.get('nodes',[])):
        typ=BLUEPRINT_KINDS.get(n['kind']);need(typ,'BLUEPRINT_UNSUPPORTED_NODE:'+n['kind'])
        outgoing=[e for e in body.get('edges',[]) if e['from']==n['nodeId']]
        if any(e['topology']=='FAN_OUT_MEMBER' for e in outgoing):typ='fan-out'
        disposition=n.get('terminalDisposition','')
        # A terminal's declared disposition stays verbatim; do not classify it by a keyword.
        if disposition=='REJECTED':typ='rejection'
        label=readable(n['nodeId']);detail=disposition or n.get('altitude','')
        ids[n['nodeId']]=d.node(n['nodeId'],typ,label,detail,source_at(source,'/nodes/'+str(i)),nativeKind=n['kind'],altitude=n.get('altitude'),terminalDisposition=disposition or None,cell=n.get('cell'),providerSlot=n.get('providerSlot'),requiredProducts=n.get('requiredProducts'),observability=n.get('observability'))
        d.expected_nodes.append(n['nodeId'])
    for i,e in enumerate(body.get('edges',[])):
        need(e['topology'] in BLUEPRINT_ROUTES,'BLUEPRINT_UNSUPPORTED_ROUTE:'+e['topology'])
        for endpoint in (e['from'],e['to']):
            if endpoint not in ids:
                ids[endpoint]=d.node(endpoint,'unresolved',readable(endpoint),'Endpoint is referenced but its node is absent.',source_at(source,'/edges/'+str(i)))
                d.findings.append({'code':'UNRESOLVED_BLUEPRINT_ENDPOINT','identity':endpoint})
        d.edge(e['edgeId'],ids[e['from']],ids[e['to']],e['topology'],e.get('selectingVariant') or e.get('semanticProgress') or e.get('contractRelation') or e['topology'],source_at(source,'/edges/'+str(i)),**{k:v for k,v in e.items() if k not in ('edgeId','from','to','topology')})
        d.expected_edges.append(e['edgeId'])
    return d.finish()

def native_views(g,plan,source):
    native=plan['canonicalGraph'];cells={c['cellId']:c for c in native['cells']}
    need(len(cells)==len(native['cells']),'NATIVE_DUPLICATE_CELL')
    parents=nx.DiGraph();parents.add_nodes_from(cells)
    for c in cells.values():
        if c.get('parentCellId'):
            need(c['parentCellId'] in cells,'NATIVE_UNKNOWN_PARENT');parents.add_edge(c['parentCellId'],c['cellId'])
    need(nx.is_directed_acyclic_graph(parents),'NATIVE_CONTAINMENT_CYCLE')
    records={r.nativeId:r for r in g.records if r.kind=='cell'}
    views=[]
    for scenario in g.scenarios:
        selected={cid for cid,r in records.items() if scenario.id in r.scenarioIds}
        if not selected:continue
        internal=[e for e in native['edges'] if e['from']['cellId'] in selected or e['to']['cellId'] in selected]
        visible=selected|{e[end]['cellId'] for e in internal for end in ('from','to')}
        d=Diagram(g.id+'/native/'+scenario.id,'Execution · '+scenario.label,'native',source);ids={}
        for i,c in enumerate(native['cells']):
            if c['cellId'] not in visible:continue
            ex=c['execution'];authority=ex['authorityId'];typ='decision' if ex['kind']=='junction' else 'event'
            if ex['kind']=='scenario':typ='outcome'
            label=authority.removeprefix('mechanic:').removeprefix('operation:').removeprefix('junction:')
            detail=c.get('semanticAddress',c['cellId']).split('#')[-1]
            ids[c['cellId']]=d.node(c['cellId'],typ,readable(label),detail,source_at(source,'/canonicalGraph/cells/'+str(i)),nativeKind=ex['kind'],altitude=c['altitude'],parent=c.get('parentCellId'),input=c['input'],outcome=c['outcome'],authority={k:v for k,v in ex.items() if k!='configuration'},external=c['cellId'] not in selected)
            d.expected_nodes.append(c['cellId'])
        for i,e in enumerate(native['edges']):
            if e not in internal:continue
            for end in ('from','to'):
                c=cells[e[end]['cellId']];need(e[end]['portId'] in (c['input']['portId'],c['outcome']['portId']),'NATIVE_UNKNOWN_PORT')
            d.edge(e['edgeId'],ids[e['from']['cellId']],ids[e['to']['cellId']],e['kind'],e.get('selectsVariant') or e['kind'],source_at(source,'/canonicalGraph/edges/'+str(i)),**{k:v for k,v in e.items() if k not in ('edgeId','kind')})
            d.expected_edges.append(e['edgeId'])
        views.append({**d.finish(),'scenarioId':scenario.id})
    return views

def legacy_views(g,plan,source):
    views=[];byid={n['nodeId']:n for n in plan['nodes']};bindings={b['bindingId']:(i,b) for i,b in enumerate(plan.get('mechanicBindings',[]))}
    for scenario in g.scenarios:
        candidates=[n for n in plan['nodes'] if n.get('scenario',{}).get('scenarioId')==scenario.id]
        if not candidates:continue
        d=Diagram(g.id+'/execution/'+scenario.id,'Execution · '+scenario.label,'operations',source)
        expanded=set();rows={}
        def expand(n):
            nid=n['nodeId'];index=plan['nodes'].index(n);ns=source_at(source,'/nodes/'+str(index));sem=n['scenario']
            inp=d.node(nid+'/input','input',readable(sem['input']['inputId']),'Input contract',source_at(ns,'/scenario/input'),contract=sem['input'].get('contract'))
            out=d.node(nid+'/outcome','outcome',readable(sem['outcome']['outcomeId']),'Declared outcome',source_at(ns,'/scenario/outcome'),contract=sem['outcome'].get('contract'),terminal=sem['outcome'].get('terminal'))
            rows[nid]=(inp,out)
            if nid in expanded:return inp,out
            expanded.add(nid);previous=inp
            for j,op in enumerate(n.get('operations',[])):
                opid=op['operationId'];kind=op.get('kind','invoke-port');os=source_at(ns,'/operations/'+str(j));label=op.get('scenarioNodeId') or op.get('mechanicBindingId') or opid
                cur=d.node(opid,'provider-port' if kind=='invoke-port' else 'event',readable(label.removeprefix('port:')),kind,os,operation=op)
                d.expected_nodes.append(opid);d.edge(nid+'/order/'+str(j),previous,cur,'operation-order',str(j+1),os,ordinal=j);previous=cur
                if kind=='invoke-scenario':
                    target=byid.get(op['scenarioNodeId'])
                    if target:
                        ti,to=rows[target['nodeId']] if target['nodeId'] in rows else expand(target)
                        d.edge(opid+'/call',cur,ti,'scenario-call','invoke scenario',os)
                        d.edge(opid+'/return',to,cur,'scenario-return','return to caller',os)
                    else:d.findings.append({'code':'UNRESOLVED_SCENARIO_CALL','identity':op['scenarioNodeId']})
                if kind=='invoke-port':
                    binding=bindings.get(op.get('mechanicBindingId'))
                    if binding:
                        bi,b=binding;bs=source_at(source,'/mechanicBindings/'+str(bi))
                        provider=d.node(b['bindingId']+'/provider','provider',readable(b.get('providerCapabilityId',b.get('provider','Provider'))),'Declared implementation',bs,provider=b.get('provider'),implementationRef=b.get('implementationRef'),mechanicType=b['mechanicType'],bindingId=b['bindingId'])
                        d.edge(opid+'/binding',provider,cur,'provider-binding',b['mechanicType'],bs)
                    else:d.findings.append({'code':'UNRESOLVED_MECHANIC_BINDING','identity':op.get('mechanicBindingId')})
            d.edge(nid+'/result',previous,out,'operation-result','result',ns)
            transition=n.get('transition')
            if transition and transition.get('nextNodeId') in byid:
                target=byid[transition['nextNodeId']];ti,to=rows[target['nodeId']] if target['nodeId'] in rows else expand(target)
                d.edge(transition['transitionId'],out,ti,'scenario-transition','transition',source_at(ns,'/transition'),transition=transition)
            return inp,out
        expand(candidates[0]);views.append({**d.finish(),'scenarioId':scenario.id})
    return views

def expression_views(g,plan,source,mechanics):
    views=[]
    for bi,b in enumerate(plan.get('mechanicBindings',[])):
        expression=b.get('configuration',{}).get('expression')
        if not isinstance(expression,dict):continue
        bs=source_at(source,'/mechanicBindings/'+str(bi)+'/configuration/expression')
        d=Diagram(g.id+'/mechanic/'+b['bindingId'],'Mechanics · '+readable(b['bindingId'].removeprefix('port:')),'expression',bs)
        def visit(value,pointer=''):
            if not isinstance(value,dict) or not isinstance(value.get('op'),str):return []
            op=value['op'];definition=mechanics.get(op);nid=d.node(pointer or '/', 'decision' if op=='if' else 'event',readable(op),pointer or 'Expression result',source_at(bs,pointer),mechanicId=op,definitionPk=definition.get('definitionPk') if definition else None,responsibility=definition.get('definition',{}).get('semantics',{}).get('mechanic',{}).get('meaning') if definition else None,parameters={k:v for k,v in value.items() if isinstance(v,(str,int,float,bool)) or v is None})
            d.expected_nodes.append(pointer or '/')
            if op in ('literal','path'):return [nid]
            def children(child,ptr,argument):
                if isinstance(child,dict) and 'op' in child:
                    child_nodes=visit(child,ptr)
                    for cn in child_nodes:d.edge(ptr,cn,nid,'conditional-argument' if op=='if' and argument in ('then','else') else 'argument-dependency',argument,source_at(bs,ptr),argument=argument)
                elif isinstance(child,dict):
                    for k,v in child.items():children(v,ptr+'/'+k.replace('~','~0').replace('/','~1'),argument+'/'+k)
                elif isinstance(child,list):
                    for i,v in enumerate(child):children(v,ptr+'/'+str(i),argument+'/'+str(i))
            for k,v in value.items():
                if k!='op':children(v,pointer+'/'+k,k)
            return [nid]
        visit(expression);scopes=sorted({n['scenario']['scenarioId'] for n in plan['nodes'] if any(o.get('mechanicBindingId')==b['bindingId'] for o in n.get('operations',[]))})
        views.append({**d.finish(),'scenarioIds':scopes})
    return views

def topology_views(g,inventory):
    sm={s.id:s for s in g.sources};records=[r for r in g.records if r.kind=='policy' and r.nativeType.startswith('consumer-execution-embodiment-plan.')]
    need(len(records)<=1,'AMBIGUOUS_EXECUTION_PLAN')
    values=resolve_sources([sm[r.sourceRef] for r in records]);views=[]
    for r in records:
        plan=values[r.sourceRef];source=sm[r.sourceRef].model_dump()
        if plan.get('canonicalGraph'):views.extend(native_views(g,plan,source))
        else:
            views.extend(legacy_views(g,plan,source))
            mechanics={s['entityId']:s for s in inventory['subjects'] if s['kind']=='MECHANIC'}
            views.extend(expression_views(g,plan,source,mechanics))
    return views
