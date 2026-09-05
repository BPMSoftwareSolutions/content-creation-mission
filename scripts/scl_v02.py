"""SCL 0.2 authoring and canonical data. No expressions or capability execution."""
import hashlib
import json
import re
from typing import Literal

from pydantic import ConfigDict, Field, model_validator
from infographic_contract import Strict, Node, Junction, ROOT, digest
from scl import Circuit, Meaning, Parser, need, validate_graph

ALTITUDES = ('strategy','product','capability','scenario','execution','mechanic','provider','physical')
Plane = Literal['primary','support','evidence','provider','observation']


class Node02(Node):
    plane: Plane = 'primary'


class Junction02(Junction):
    plane: Plane = 'primary'


class Meaning02(Meaning):
    altitude: Literal['strategy','product','capability','scenario','execution','mechanic','provider','physical'] = 'scenario'


class TraceStep(Strict):
    model_config=ConfigDict(json_schema_extra={'oneOf':[
        {'required':['edgeId'],'properties':{'edgeId':{'type':'string','minLength':1},'paths':{'type':'null'}}},
        {'required':['paths'],'properties':{'edgeId':{'type':'null'},'paths':{'type':'array','minItems':2,'items':{'type':'array','minItems':1}}}}
    ]})
    edgeId: str | None = Field(default=None,min_length=1)
    paths: list[list['TraceStep']] | None = Field(default=None,min_length=2)

    @model_validator(mode='after')
    def one_form(self):
        need((self.edgeId is not None) != (self.paths is not None), 'TRACE_STEP_NEEDS_EDGE_OR_PARALLEL')
        if self.paths is not None:
            need(len(self.paths)>=2 and all(self.paths), 'PARALLEL_NEEDS_TWO_NONEMPTY_PATHS')
        return self


class Trace(Strict):
    id: str
    scenarioId: str
    steps: list[TraceStep] = Field(min_length=1)


class Circuit02(Circuit):
    version: Literal['sidefx-circuit.v0.2'] = 'sidefx-circuit.v0.2'
    nodes: list[Node02] = Field(min_length=3)
    junctions: list[Junction02] = Field(default_factory=list)
    meanings: list[Meaning02] = Field(default_factory=list)
    traces: list[Trace] = Field(default_factory=list)
    selectedTrace: str | None = None


def flatten(steps):
    return [edge for s in steps for edge in ([s.edgeId] if s.edgeId is not None else
            [e for path in s.paths for e in flatten(path)])]


def validate_extensions(g):
    nodes={n.id:n for n in g.nodes+g.junctions}; edges={e.id:e for e in g.edges}
    for n in nodes.values():
        need(n.layer == ('mechanic' if n.plane=='primary' else 'support'), 'PLANE_LAYER_CONFLICT:'+n.id)
    need(len({t.id for t in g.traces})==len(g.traces), 'DUPLICATE_TRACE')
    if g.traces:
        selected=next((t for t in g.traces if t.id==g.selectedTrace),None)
        need(selected is not None, 'UNKNOWN_SELECTED_TRACE')
        need(g.trace==flatten(selected.steps), 'TRACE_SELECTION_DRIFT')
    else: need(g.selectedTrace is None, 'UNKNOWN_SELECTED_TRACE')

    def chain(steps, depth=0):
        need(depth<24, 'TRACE_NESTING_LIMIT')
        start=end=None; used=set(); visited=set()
        for step in steps:
            if step.edgeId is not None:
                need(step.edgeId in edges, 'UNKNOWN_TRACE_EDGE:'+step.edgeId)
                e=edges[step.edgeId];a,b=e.source,e.target;ids={e.id};points={a,b}
            else:
                paths=[chain(p,depth+1) for p in step.paths]
                a,b=paths[0][:2]
                need(all(p[0]==a and p[1]==b for p in paths), 'PARALLEL_BOUNDARY_MISMATCH')
                need(a in nodes and b in nodes and nodes[a].type=='fan-out' and
                     nodes[b].type=='convergence' and nodes[b].join=='all', 'PARALLEL_REQUIRES_FANOUT_AND_ALL_JOIN')
                ids=set();internal=set();points={a,b}
                for _,_,pathids,pathnodes in paths:
                    need(not ids & pathids and not internal & (pathnodes-{a,b}), 'PARALLEL_PATHS_OVERLAP')
                    ids |= pathids;internal |= pathnodes-{a,b};points |= pathnodes
                outgoing={e.id for e in g.edges if e.source==a and e.type in ('transition','product-transfer')}
                incoming={e.id for e in g.edges if e.target==b and e.type in ('transition','product-transfer')}
                need(outgoing<=ids and incoming<=ids, 'PARALLEL_INCOMPLETE_BRANCHES')
            need(end is None or end==a, 'TRACE_SEQUENCE_DISCONNECTED')
            need(not used & ids, 'TRACE_REPEATS_EDGE')
            if start is None:start=a
            end=b;used |= ids;visited |= points
        return start,end,used,visited

    for t in g.traces:
        start,end,ids,points=chain(t.steps)
        need(t.scenarioId in {s.id for s in g.scenarios}, 'UNKNOWN_TRACE_SCENARIO:'+t.id)
        need(all(i in nodes and nodes[i].scenarioId==t.scenarioId for i in points), 'TRACE_SCENARIO_MISMATCH:'+t.id)


def select_trace(g, identity):
    need(isinstance(g,Circuit02), 'NAMED_TRACE_REQUIRES_SCL_02')
    t=next((t for t in g.traces if t.id==identity),None);need(t is not None,'UNKNOWN_SELECTED_TRACE')
    return validate_graph({**g.model_dump(),'selectedTrace':identity,'trace':flatten(t.steps)})


class DiagnosticError(ValueError):
    def __init__(self, text, pos, code, message, hint=None):
        pos=max(0,min(pos,len(text)));line=text.count('\n',0,pos)+1;column=pos-text.rfind('\n',0,pos)
        self.diagnostic=dict(code=code,message=message,line=line,column=column,
            offset=len(text[:pos].encode('utf-16-le'))//2, hint=hint or 'Check this declaration and its referenced identities.')
        super().__init__(f'{code} {line}:{column}: {message}')


ALIASES={'given':'input','when':'event','then':'outcome','validate':'validation','deny':'event','permit':'event'}
NODES={'input','event','outcome','validation','human-approval','authority','evidence','provider-port','provider'}
JUNCTIONS={'branch','decision','fan-out','convergence','termination','rejection'}
INLINE={'altitude','parentId','responsibility','authorityId','mechanicProfile','experience','variants','productIsExperience'}
HINTS={
    'UNKNOWN_ENDPOINT':'Connect the route to an existing node ID, or declare the missing node.',
    'SCENARIO_MEMBERSHIP':'Add every scenario node to nodeIds and remove IDs that belong elsewhere.',
    'MISSING_IEO':'A scenario needs an input, an event and an outcome.',
    'UNTYPED_SPLIT':'Use a decision for alternatives or a parallel block for concurrent paths.',
    'UNTYPED_MERGE':'Declare a convergence and its all, any or quorum policy.',
    'PLANE_LAYER_CONFLICT':'Primary maps to mechanic; every other plane maps to support. Omit layer in authored 0.2.',
    'PARALLEL_REQUIRES_FANOUT_AND_ALL_JOIN':'Parallel paths must leave one fan-out and meet at one ALL convergence.',
    'TRACE_SEQUENCE_DISCONNECTED':'Each step must begin where the preceding step ends. Put concurrent paths inside parallel.',
    'TRACE_SELECTION_DRIFT':'The flat trace must equal the edges in the selected named trace.',
    'REALITY_WITHOUT_SOURCE':'A draft uses TARGET, GAP or STAGING sources. Provider state and proof status are separate.',
    'DRAFT_CANNOT_CLAIM_CURRENT':'Keep the draft TARGET. Observed execution requires a source-backed reveal.',
    'ALTITUDE_INVERSION':'A contained node must have the same or a lower semantic altitude than its parent.',
}


class Parser02(Parser):
    """A bounded recursive descent reader. Bare names are inert enum/identity strings."""
    keyword=re.compile(r'[a-zA-Z_][a-zA-Z0-9_.-]*')
    def __init__(self,text):
        super().__init__(text);self.spans={};self.model_spans={};self.pending_traces=[];self.depth=0

    def error(self,message):
        hint='Use quotes for prose and a semicolon after each property.'
        if message.startswith('expected ;'):hint='Add a semicolon to the preceding statement.'
        raise DiagnosticError(self.text,self.pos,'SCL_SYNTAX',message,hint)

    def value(self):
        self.space()
        m=self.keyword.match(self.text,self.pos)
        if m and m[0] not in ('true','false','null'):
            self.pos=m.end();return m[0]
        return super().value()

    def peek(self):
        self.space();m=self.keyword.match(self.text,self.pos);return m[0] if m else self.text[self.pos:self.pos+1]

    def accept(self,token):
        if self.peek()==token:self.pos+=len(token);return True
        return False

    def identity(self):
        self.space();pos=self.pos;identity=self.value()
        if not isinstance(identity,str) or not identity:self.error('expected identity')
        if identity.startswith('__scl.'):self.error('__scl. identities are reserved for compiler-generated nodes and routes')
        return identity,pos

    def put(self,props,key,value,pos):
        if key in props:self.error('duplicate property '+key)
        props[key]=value

    def props(self):
        self.token('{');result={}
        while not self.accept('}'):
            key=self.word();self.put(result,key,self.value(),self.pos);self.token(';')
        return result

    def trace_steps(self,depth=0):
        if depth>=20:self.error('trace nesting limit is 20')
        self.token('{');steps=[]
        while not self.accept('}'):
            kind=self.word()
            if kind=='step':steps.append({'edgeId':self.value()});self.token(';')
            elif kind=='parallel':
                self.token('{');paths=[]
                while not self.accept('}'):
                    self.token('path')
                    if self.peek()=='{':paths.append(self.trace_steps(depth+1))
                    else:
                        values=self.value();self.token(';')
                        if not isinstance(values,list) or not all(isinstance(v,str) for v in values):self.error('path needs an array of route IDs')
                        paths.append([{'edgeId':v} for v in values])
                steps.append({'paths':paths})
            else:self.error('expected step or parallel in trace')
        return steps

    def parse(self):
        self.token('scl');v=self.value();self.token(';')
        if v not in ('0.2',.2):self.error('unsupported version')
        form=self.word()
        if form=='circuit':data=self.canonical()
        elif form=='capability':data=self.lite()
        else:self.error('expected capability or circuit')
        self.space()
        if self.pos!=len(self.text):self.error('trailing input')
        return data

    def canonical(self):
        identity,pos=self.identity();self.token('{')
        data={'version':'sidefx-circuit.v0.2','id':identity};self.spans[identity]=pos
        collections={'source':'sources','capability':'capabilities','scenario':'scenarios','route':'edges',
            'binding':'providers','meaning':'meanings','record':'records','finding':'findings','node':'nodes','junction':'junctions'}
        inline=[];relations=[]
        while not self.accept('}'):
            self.space();pos=self.pos;key=self.word()
            if key=='trace' and self.peek() not in ('[','null'):
                identity,_=self.identity();self.spans[identity]=pos
                self.pending_traces.append({'id':identity,'steps':self.trace_steps()});continue
            if key in collections or key in NODES or key in JUNCTIONS:
                identity=None if self.peek()=='{' else self.value()
                values=self.props()
                if identity is not None:
                    if 'id' in values:self.error('identity given twice')
                    values['id']=identity;self.spans[identity]=pos
                field=collections.get(key,'nodes' if key in NODES else 'junctions')
                if key in NODES|JUNCTIONS:
                    if 'type' in values:self.error('type given twice')
                    values['type']=key
                if field in ('nodes','junctions'):
                    self.decorate(values,inline,relations)
                self.model_spans[(field,len(data.get(field,[])))]=pos
                data.setdefault(field,[]).append(values)
            else:
                if key in data or key in collections.values() and key not in ('meanings',):self.error('duplicate or reserved property '+key)
                data[key]=self.value();self.token(';')
        data.setdefault('meanings',[]).extend(inline)
        self.add_relations(data,relations)
        if self.pending_traces:
            if data.get('traces'):self.error('use named trace blocks or normalized traces, not both')
            byedge={e['id']:e for e in data.get('edges',[])};bynode={n['id']:n for n in data.get('nodes',[])+data.get('junctions',[])}
            traces=[]
            for t in self.pending_traces:
                ids=flatten([TraceStep.model_validate(s) for s in t['steps']]);first=byedge.get(ids[0],{}) if ids else {}
                traces.append({**t,'scenarioId':bynode.get(first.get('source'),{}).get('scenarioId','')})
            data['traces']=traces;data.setdefault('selectedTrace',traces[0]['id'])
            chosen=next((t for t in traces if t['id']==data['selectedTrace']),None)
            if chosen:data.setdefault('trace',flatten([TraceStep.model_validate(s) for s in chosen['steps']]))
        return data

    def decorate(self,node,meanings,relations):
        meaning={k:node.pop(k) for k in list(node) if k in INLINE}
        if meaning:meanings.append({'nodeId':node['id'],**meaning})
        plane=node.setdefault('plane','primary' if node.get('layer','mechanic')=='mechanic' else
            'evidence' if node['type']=='evidence' else 'provider' if node['type']=='provider' else 'support')
        node.setdefault('layer','mechanic' if plane=='primary' else 'support')
        if 'detail' not in node:node['detail']=meaning.get('responsibility',meaning.get('experience',''))
        for key in ('requires-evidence','requires-port','establishes'):
            if key in node:
                refs=node.pop(key);refs=refs if isinstance(refs,list) else [refs]
                relations.extend((node['id'],key,r) for r in refs)

    def auto_id(self,role,*parts):
        raw=json.dumps(parts,ensure_ascii=False,separators=(',',':')).encode()
        return '__scl.'+role+'.'+hashlib.sha256(raw).hexdigest()[:20]

    def edge(self,data,a,b,kind='transition',label='',basis=None):
        node=next(n for n in data['nodes']+data['junctions'] if n['id']==a)
        identity=self.auto_id(kind,a,b)
        edge=dict(id=identity,source=a,target=b,type=kind,label=label,basis=basis or node['basis'],sourceRefs=node['sourceRefs'])
        if not any(e['id']==identity for e in data['edges']):data['edges'].append(edge)
        self.spans[identity]=self.spans.get(a,0)
        return identity

    def add_relations(self,data,relations):
        byid={n['id']:n for n in data.get('nodes',[])+data.get('junctions',[])}
        for owner,kind,ref in relations:
            if not isinstance(ref,str) or ref not in byid:
                raise DiagnosticError(self.text,self.spans.get(owner,0),'UNKNOWN_RELATION_TARGET',f'{owner} references missing {ref}.','Declare the referenced evidence or provider-port with this exact identity.')
            a,b=(owner,ref) if kind=='establishes' else (ref,owner)
            expected='provider-port' if kind=='requires-port' else 'evidence'
            checked=ref if kind!='establishes' else owner
            need(byid[checked]['type']==expected,'INVALID_SUGAR_RELATION:'+owner)
            if kind=='requires-evidence' or kind=='establishes':need(byid[b]['type']=='outcome','EVIDENCE_REQUIRES_OUTCOME:'+owner)
            self.edge(data,a,b,'dependency' if kind=='requires-port' else 'evidence-attachment',
                'required responsibility' if kind=='requires-port' else 'required to establish')

    def lite(self):
        cap,pos=self.identity();self.spans[cap]=pos;self.token('{')
        props={};scenarios=[];support=[];providers=[]
        while not self.accept('}'):
            key=self.word()
            if key=='scenario':
                identity,p=self.identity();self.spans[identity]=p;self.token('{');meta={};items=[];requirements=[]
                while not self.accept('}'):
                    kind=self.word()
                    if kind=='label':self.put(meta,kind,self.value(),self.pos);self.token(';')
                    elif kind=='requires':self.token('evidence');requirements.append(self.value());self.token(';')
                    else:items.append(self.item(kind))
                scenarios.append((identity,meta,items,requirements))
            elif key=='provider':
                state=self.value()
                if state not in ('candidate','bound'):self.error('provider state must be candidate or bound')
                identity,p=self.identity();self.spans[identity]=p;self.token('through');port=self.value();self.token(';')
                providers.append((state,identity,port))
            elif key in ('evidence','provider-port','authority'):support.append(self.item(key))
            elif key in ('promise','label','domain'):self.put(props,key,self.value(),self.pos);self.token(';')
            else:self.error('unknown capability item '+key)
        need(bool(props.get('promise')),'MISSING_CAPABILITY_PROMISE')
        context='declarations/scl/playground-intent.json'
        sources=[dict(id='__scl.design.'+b.lower(),path=context,sha256=digest(ROOT/context),kind=b,label='User-authored '+b.lower()+' design context') for b in ('TARGET','GAP','STAGING')]
        data=dict(version='sidefx-circuit.v0.2',id=cap,title=props.get('label',self.label(cap)),promise=props['promise'],status='DRAFT',
            sources=sources,capabilities=[dict(id=cap,label=props.get('label',self.label(cap)),domain=props.get('domain','Authored capability'),
            scenarioIds=[s[0] for s in scenarios],coverage='Intended scenarios authored in SCL 0.2',sourceRefs=['__scl.design.target'])],
            scenarios=[],nodes=[],junctions=[],edges=[],providers=[],meanings=[],traces=[],findings=[])
        relations=[]
        for item in support:self.make_node(data,item,cap,None,relations)
        for state,identity,port in providers:
            need(isinstance(port,str),'INVALID_PROVIDER_PORT')
            if not any(n['id']==port for n in data['nodes']):self.make_node(data,dict(kind='provider-port',id=port,props={'label':self.label(port),'detail':'Provider responsibility','plane':'support'}),cap,None,relations)
            self.make_node(data,dict(kind='provider',id=identity,props={'label':self.label(identity),'detail':state.title()+' / not observed','plane':'provider'}),cap,None,relations)
            self.edge(data,identity,port,'provider-binding',state)
            data['providers'].append(dict(nodeId=identity,portIds=[port],binding=state,state='candidate' if state=='candidate' else 'unknown'))
        for identity,meta,items,requirements in scenarios:
            first,last,steps=self.sequence(data,items,cap,identity,relations)
            members=[n['id'] for n in data['nodes']+data['junctions'] if n.get('scenarioId')==identity]
            data['scenarios'].append(dict(id=identity,capabilityId=cap,label=meta.get('label',self.label(identity)),nodeIds=members,sourceRefs=['__scl.design.target']))
            if steps:data['traces'].append(dict(id=identity+'.flow',scenarioId=identity,steps=steps))
            for ref in requirements:
                if not any(n['id']==ref for n in data['nodes']):
                    self.make_node(data,dict(kind='evidence',id=ref,props={'label':self.label(ref),'basis':'GAP','plane':'evidence','closure':'Supply scoped execution testimony that establishes the outcome.','detail':'Required / not observed'}),cap,None,relations)
                    data['findings'].append(dict(code='EVIDENCE_REQUIREMENT_OPEN',subject=ref,detail='Evidence was required but no evidence object was supplied.',closure='Supply the exact required scope and its execution testimony.'))
                relations.append((last,'requires-evidence',ref))
        ports={n['id'] for n in data['nodes'] if n['type']=='provider-port'}
        bound={p for b in data['providers'] for p in b['portIds']}
        for port in sorted(ports-bound):data['providers'].append(dict(nodeId=None,portIds=[port],binding='open',state='unknown'))
        self.add_relations(data,relations)
        if data['traces']:
            data['selectedTrace']=data['traces'][0]['id'];data['trace']=flatten([TraceStep.model_validate(s) for s in data['traces'][0]['steps']])
        return data

    @staticmethod
    def label(identity):return str(identity).replace('-',' ').replace('_',' ').capitalize()

    def item(self,kind):
        if kind not in ALIASES and kind not in NODES:self.error('unknown scenario item '+kind)
        identity,pos=self.identity();self.spans[identity]=pos;props={};defaults={};paths=None;join=None
        if kind in ('deny','permit'):
            self.token('expect');expect=self.value();defaults.update(label=self.label(kind+'-'+identity),responsibility='Expect '+str(expect));props['variants']=[kind,str(expect)]
        elif kind=='validate' and self.accept('on'):
            fields=[self.value()]
            while self.accept(','):fields.append(self.value())
            defaults.update(label=self.label(identity),responsibility='Match '+', '.join(map(str,fields)));props['variants']=list(map(str,fields))
        elif self.peek()=='"':props['label']=self.value()
        if self.accept('{'):
            while not self.accept('}'):
                key=self.word()
                if key=='parallel':
                    if paths is not None:self.error('duplicate parallel block')
                    self.depth+=1
                    if self.depth>16:self.error('parallel nesting limit is 16')
                    self.token('{');paths=[]
                    while not self.accept('}'):
                        k=self.word()
                        if k=='path':
                            self.token('{');path=[]
                            while not self.accept('}'):path.append(self.item(self.word()))
                            paths.append(path)
                        else:paths.append([self.item(k)])
                    self.depth-=1
                elif key=='join':
                    if join is not None:self.error('duplicate join')
                    join,jpos=self.identity();self.spans[join]=jpos;self.token('all');self.token(';')
                else:self.put(props,key,self.value(),self.pos);self.token(';')
        self.accept(';')
        for key,value in defaults.items():props.setdefault(key,value)
        if paths is not None:
            if kind!='when':self.error('parallel belongs in a when block')
            if len(paths)<2 or not all(paths):self.error('parallel needs at least two nonempty paths')
            props.setdefault('label',self.label(identity));return dict(kind='parallel',id=identity,props=props,paths=paths,join=join or self.auto_id('join',identity))
        if join is not None:self.error('join requires a parallel block')
        return dict(kind=ALIASES.get(kind,kind),id=identity,props=props)

    def make_node(self,data,item,cap,scenario,relations):
        identity=item['id'];kind=item['kind'];props=dict(item['props'])
        if any(n['id']==identity for n in data['nodes']+data['junctions']):
            raise DiagnosticError(self.text,self.spans.get(identity,0),'DUPLICATE_ID',f'{identity} is already declared.','Give every node and junction a unique identity.')
        if any(k in props for k in ('id','type','capabilityId','scenarioId','sourceRefs')):self.error('Lite owns identity, scope and design sources; use canonical circuit form for explicit references')
        basis=props.setdefault('basis','TARGET');props.setdefault('label',self.label(identity))
        if basis not in ('TARGET','GAP','STAGING'):
            raise DiagnosticError(self.text,self.spans.get(identity,0),'DRAFT_BASIS',f'{basis} is not a draft evidence basis.',
                'Use TARGET for intended behavior, GAP for a missing obligation, or STAGING for illustration. Candidate is provider state; observed or proved behavior needs execution evidence.')
        props.update(id=identity,type=kind,capabilityId=cap,scenarioId=scenario,sourceRefs=['__scl.design.'+str(basis).lower()])
        if kind in ('evidence','provider','provider-port','authority'):props.setdefault('plane','evidence' if kind=='evidence' else 'provider' if kind=='provider' else 'support')
        props.setdefault('altitude','scenario' if scenario else 'provider' if kind=='provider' else 'execution')
        self.decorate(props,data['meanings'],relations)
        field='junctions' if kind in JUNCTIONS else 'nodes';self.model_spans[(field,len(data[field]))]=self.spans.get(identity,0)
        data[field].append(props);return identity

    def sequence(self,data,items,cap,scenario,relations):
        first=previous=None;steps=[]
        for item in items:
            if item['kind']=='parallel':
                fork=self.make_node(data,{**item,'kind':'fan-out'},cap,scenario,relations)
                join=self.make_node(data,dict(id=item['join'],kind='convergence',props={'label':'Both results' if len(item['paths'])==2 else 'All results','join':'all'}),cap,scenario,relations)
                if previous:steps.append({'edgeId':self.edge(data,previous,fork)})
                branches=[]
                for path in item['paths']:
                    a,b,inside=self.sequence(data,path,cap,scenario,relations)
                    need(a is not None and b is not None,'EMPTY_PARALLEL_PATH')
                    branches.append([{'edgeId':self.edge(data,fork,a)},*inside,{'edgeId':self.edge(data,b,join)}])
                steps.append({'paths':branches});start,end=fork,join
            else:
                start=end=self.make_node(data,item,cap,scenario if item['kind'] not in ('provider-port','provider','evidence','authority') else None,relations)
                if item['kind'] in ('provider-port','provider','evidence','authority'):continue
                if previous:steps.append({'edgeId':self.edge(data,previous,start)})
            if first is None:first=start
            previous=end
        return first,previous,steps


def parse_v02(text,verify_sources=True):
    parser=Parser02(text)
    try:
        data=parser.parse();g=validate_graph(data,verify_sources)
        return g,dict(declarations=parser.spans,language='0.2')
    except DiagnosticError:raise
    except ValueError as e:
        pos=0;message=str(e);code=message.split(':',1)[0];subject=message.split(':',1)[-1]
        if hasattr(e,'errors'):
            first=e.errors(include_url=False)[0];loc=first['loc'];code='SCL_CONTRACT';message=first['msg']+' ('+'.'.join(map(str,loc))+')'
            if len(loc)>=2:pos=parser.model_spans.get(tuple(loc[:2]),0)
        else:pos=parser.spans.get(subject,parser.spans.get(next(iter(parser.spans),''),0))
        raise DiagnosticError(text,pos,code,message,HINTS.get(code)) from e


def diagnostic(text,error):
    if isinstance(error,DiagnosticError):return error.diagnostic
    message=str(error);match=re.match(r'SCL_SYNTAX (\d+):(\d+): (.*)',message)
    if match:
        line,col=int(match[1]),int(match[2]);lines=text.splitlines(keepends=True)
        pos=sum(len(s) for s in lines[:line-1])+col-1
        return DiagnosticError(text,pos,'SCL_SYNTAX',match[3],
            'Add a semicolon to the preceding statement.' if match[3]=='expected ;' else 'Check quotes, braces and statement terminators.').diagnostic
    code=message.split(':',1)[0];subject=message.split(':',1)[-1]
    declaration=re.search(r'\b(?:route|input|event|outcome|scenario|convergence|fan-out|provider|evidence)\s+'+re.escape(json.dumps(subject)),text)
    if declaration:return DiagnosticError(text,declaration.start(),code,message,HINTS.get(code)).diagnostic
    return dict(code=code if re.fullmatch('[A-Z_]+',code) else 'SCL_CONTRACT',message=message[:2500],
        line=None,column=None,offset=None,hint=HINTS.get(code,'Check the reported property, type or identity against the language reference.'))
