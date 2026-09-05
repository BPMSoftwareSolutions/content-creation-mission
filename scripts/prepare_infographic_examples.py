"""Bind reviewed reference graphs to exact capsule facts and explicit future designs."""
from infographic_contract import ROOT,read,write,digest,validate

CAP='interlock-agent-operation'
PKG='outputs/scenario-visual-evidence/interlock-agent-operation/interlock-agent-operation.json'

def source(id,path,kind,label,pointer=''):
    return dict(id=id,path=path,sha256=digest(ROOT/path),pointer=pointer,kind=kind,label=label,encoding='capsule-entry' if path.startswith('data/capsule-evidence/entries/') else 'json')

def base(id,title,subtitle,altitude='scenario',mode='DECLARED'):
    p=read(PKG);runtime=p['evidence']['execution'][0]['source']['snapshot']
    return dict(contractVersion='infographic-projection.v1',grammarVersion='sidefx-infographic-grammar.v1',id=id,title=title,subtitle=subtitle,altitude=altitude,
      scope='Stored capsule semantics, source references and authored visual direction. No observed live interception.' if mode=='DECLARED' else 'Explicit target design. Animated outcomes do not establish current implementation or completed proof.',
      sources=[source('runtime',runtime,'DECLARED','Exact runtime execution plan'),source('capsule',PKG,'DECLARED','Verified capsule evidence package'),
               source('story','declarations/episode-01-direction.json','STAGING','Fictional human experience'),source('target','declarations/infographic-design-intent.v1.json','TARGET','Intended visual circuit'),
               source('gap','evaluations/episode-01-platform-gap.json','GAP','Missing live enforcement and testimony')],
      capabilities=[],scenarios=[],nodes=[],junctions=[],edges=[],providers=[],humanAnchors=[],visualLayers=['human','mechanic','support'],animationBeats=[],zoomAggregations=[],scenarioRelationships=[])

def node(p,id,type,label,detail='',basis='DECLARED',cap=CAP,scenario='adjudication',layer='mechanic',refs=None,**extra):
    n=dict(id=id,type=type,label=label,detail=detail,capabilityId=cap,scenarioId=scenario,basis=basis,sourceRefs=refs or [{'DECLARED':'runtime','TARGET':'target','GAP':'gap'}[basis]],layer=layer,**extra)
    p['junctions' if type in ('branch','fan-out','convergence','decision','termination','rejection') else 'nodes'].append(n)
    return id

def edge(p,a,b,type='transition',label='',basis='DECLARED',refs=None,**extra):
    id=f'e{len(p["edges"]):02}'
    p['edges'].append(dict(id=id,source=a,target=b,type=type,label=label,basis=basis,sourceRefs=refs or [{'DECLARED':'runtime','TARGET':'target','GAP':'gap'}[basis]],**extra))
    return id

def group(p,scenario,label,cap=CAP,caplabel='Interlock Agent Operation',coverage='One source scenario',basis='DECLARED'):
    refs=['runtime' if basis=='DECLARED' else 'target']
    members=[n['id'] for n in p['nodes']+p['junctions'] if n['scenarioId']==scenario]
    p['scenarios'].append(dict(id=scenario,capabilityId=cap,label=label,nodeIds=members,sourceRefs=refs))
    existing=next((c for c in p['capabilities'] if c['id']==cap),None)
    if existing:existing['scenarioIds'].append(scenario)
    else:p['capabilities'].append(dict(id=cap,label=caplabel,domain='Governed agent work',scenarioIds=[scenario],coverage=coverage,sourceRefs=refs))

def human(p,input,event,outcome,person='Platform engineer'):
    p['humanAnchors']=[dict(person=person,input=input,event=event,outcome=outcome,basis='STAGING',sourceRefs=['story'])]

def beats(p,groups,captions,edges=None):
    for i,phase in enumerate(['Establish','Activate','Execute','Resolve','Prove']):
        p['animationBeats'].append(dict(phase=phase,caption=captions[i],entityIds=groups[i],edgeIds=(edges or [[],[],[],[],[]])[i]))
    for c in p['capabilities']:
        p['zoomAggregations'].append(dict(id='aggregate:'+c['id'],label=c['label'],altitude='capability',memberIds=[n['id'] for n in p['nodes']+p['junctions'] if n['capabilityId']==c['id']]))

def current():
    p=base('scenario-current','A decision is not yet an interlock.','One adjudication scenario · current stored semantics')
    p['sources'].append(source('adjudication',p['sources'][0]['path'],'DECLARED','Adjudication expression','/mechanicBindings/2'))
    node(p,'request','input','Admitted call envelope','ADJUDICATE / safe-tool',productContract='covered-agent-tool-call.v1')
    node(p,'act','event','Adjudicate call','Stored authority transformation',refs=['adjudication'])
    node(p,'select','decision','Tool name?','dangerous-tool',rule='toolId equals dangerous-tool; otherwise ALLOW',refs=['adjudication'])
    node(p,'operator','outcome','OPERATOR_REQUIRED','Returned decision label',productContract='agent-tool-call-disposition.v1',refs=['adjudication'])
    node(p,'allow','outcome','ALLOW','Returned decision label',productContract='agent-tool-call-disposition.v1',refs=['adjudication'])
    node(p,'provider','provider','Authority transformation','Bound provider / live state unknown',scenario=None,layer='support')
    node(p,'port','provider-port','Adjudication port','Required responsibility',scenario=None,layer='support',refs=['adjudication'])
    node(p,'receipt','evidence','Expression + fixtures','Declared expectations; no live hook proof',scenario=None,layer='support',refs=['capsule','adjudication'])
    a=edge(p,'request','act');b=edge(p,'act','select')
    edge(p,'select','operator',label='equals',guard='toolId == dangerous-tool',refs=['adjudication'])
    c=edge(p,'select','allow',label='otherwise',guard='otherwise',refs=['adjudication'])
    d=edge(p,'provider','port','provider-binding','declared binding')
    edge(p,'port','act','dependency','supplies responsibility')
    e=edge(p,'receipt','act','evidence-attachment','source semantics')
    p['providers']=[dict(nodeId='provider',portIds=['port'],binding='bound',state='unknown')]
    group(p,'adjudication','Adjudicate covered agent tool call')
    human(p,'She authorized inspection.','A queued publication needs a decision.','A stored label does not establish that a tool was stopped.')
    beats(p,[['request'],['act','port','provider'],['select'],['allow'],['receipt']],
      ['Establish the supplied call envelope.','Open the stored responsibility and its provider binding.','Compare the tool name; illustrate the safe-tool alternative.','The illustrated branch returns ALLOW. This is not effect dispatch.','Inspect source semantics and fixture expectations; live enforcement remains unproven.'],[[],[a,d],[b],[c],[e]])
    return p

def certification():
    p=base('scenario-target','Prove both sides of the boundary.','One intended certification scenario · fan-out → join → validation',mode='TARGET')
    def n(id,t,label,detail='',**kw):return node(p,id,t,label,detail,**({'basis':'TARGET','scenario':'certification'}|kw))
    n('activation','input','Exact activation','One session / workspace / policy')
    n('split','fan-out','Both probes','Same identity envelope')
    n('deny-probe','event','Deny unmanaged probe','Observe no effect')
    n('permit-probe','event','Permit read-only probe','Observe the declared effect')
    n('join','convergence','Both results','ALL / 2 of 2',join='all')
    n('check','validation','Match identities','Session, coverage, time, authority')
    n('certified','outcome','Scoped boundary','Only if every obligation closes')
    n('port','provider-port','Live probe port','Responsibility remains to be supplied',scenario=None,layer='support')
    n('provider','provider','Hook runtime candidate','Candidate / not observed',scenario=None,layer='support')
    node(p,'proof','evidence','Required probe testimony','Not an observed receipt',basis='GAP',scenario=None,layer='support',closure='Execute both probes in the same exact live session; bind actual effects and ordered identities.')
    e1=edge(p,'activation','split',basis='TARGET')
    e2=edge(p,'split','deny-probe',label='dependent 1',basis='TARGET');e3=edge(p,'split','permit-probe',label='dependent 2',basis='TARGET')
    e4=edge(p,'deny-probe','join',basis='TARGET');e5=edge(p,'permit-probe','join',basis='TARGET')
    e6=edge(p,'join','check',label='both arrived',basis='TARGET');e7=edge(p,'check','certified',label='matching proof',basis='TARGET')
    edge(p,'provider','port','provider-binding','candidate',basis='TARGET')
    edge(p,'port','deny-probe','dependency','probe responsibility',basis='TARGET')
    edge(p,'port','permit-probe','dependency','probe responsibility',basis='TARGET')
    edge(p,'proof','certified','evidence-attachment','required to establish',basis='GAP')
    p['providers']=[dict(nodeId='provider',portIds=['port'],binding='candidate',state='candidate')]
    group(p,'certification','Two-sided live certification',basis='TARGET',coverage='One intended scenario')
    human(p,'An operator needs to trust the exact boundary.','Both denial and permitted work must be observed.','Confidence comes from scoped evidence, not an activation label.',person='Operator')
    beats(p,[['activation'],['split','provider','port'],['deny-probe','permit-probe','join','check'],['certified'],['proof']],
      ['Start with one exact activation identity.','Fan-out supplies both required dependents. It does not choose one.','Join waits for both arrivals, then identity validation applies.','The target outcome remains conditional on complete matching proof.','Required testimony stays GAP / REQUIRED throughout the animation.'],[[],[e1,'e07'],[e2,e3,e4,e5,e6,'e08','e09'],[e7],['e10']])
    return p

def capability():
    p=base('capability-current','One capability. Seven scenario boundaries.','Complete scenario inventory · stored mechanics and shared declared providers',altitude='capability')
    inventory=[s for s in read('inventories/scenario-inventory.json') if s['capabilityId']==CAP]
    records={x['value']['nodeId']:x['value'] for x in read(PKG)['evidence']['execution']}
    short={CAP:('Root operation','Select final disposition','Ready / established / adjudicated / applied / held'),
      'admit-agent-interlock-request':('Request admission','Check operation variant','ADMITTED / HELD'),
      'activate-agent-interlock':('Activation','Write activation status','ATTACHED_IN_SESSION'),
      'certify-live-agent-interlock':('Certification','Write certification status','GOVERNANCE_PROVEN'),
      'adjudicate-covered-agent-tool-call':('Adjudication','Compare tool name','ALLOW / OPERATOR_REQUIRED'),
      'protect-agent-interlock-control-plane':('Operator control','Write control status','OPERATOR_ACTION_APPLIED'),
      'hold-untrusted-or-uncovered-agent-operation':('Hold','Check admissionStatus','MALFORMED_HOOK_INPUT')}
    phases=[[],[],[],[],[]];paths=[[],[],[],[],[]]
    for i,s in enumerate(inventory):
        sid=s['scenarioId'];label,action,result=short[sid];record=records[sid]['scenario']
        p['sources'].append(source('scenario-'+str(i),p['sources'][0]['path'],'DECLARED',s['scenarioName'],f'/nodes/{i}'))
        refs=['scenario-'+str(i)];a,b,c=f's{i}-input',f's{i}-event',f's{i}-outcome'
        node(p,a,'input',label+' request',record['input']['contract']['contractId'],scenario=sid,refs=refs,productContract=record['input']['contract']['contractId'])
        node(p,b,'event',action,'Stored expression / not live-effect proof',scenario=sid,refs=['runtime'])
        node(p,c,'outcome',result,'Status meaning requires its own evidence',scenario=sid,refs=['runtime'],productContract=record['outcome']['contract']['contractId'])
        paths[1].append(edge(p,a,b));paths[3].append(edge(p,b,c))
        phases[0].append(a);phases[1].append(b);phases[3].append(c)
        group(p,sid,label,coverage='All 7 of 7 source scenarios')
    for i,provider in enumerate([('Authority transformation','7 event responsibilities'),('Schema admission','Contract shape boundary')]):
        node(p,f'p{i}','provider',provider[0],'Declared binding / live state unknown',scenario=None,layer='support')
        node(p,f'port{i}','provider-port',provider[1],'Shared responsibility boundary',scenario=None,layer='support')
        edge(p,f'p{i}',f'port{i}','provider-binding','declared binding')
        p['providers'].append(dict(nodeId=f'p{i}',portIds=[f'port{i}'],binding='bound',state='unknown'))
        phases[2]+=[f'p{i}',f'port{i}']
    node(p,'evidence','evidence','Exact capsule evidence','Expressions, fixtures, conformance scope',scenario=None,layer='support',refs=['capsule'])
    edge(p,'evidence','s0-event','evidence-attachment','source package');phases[4]=['evidence']
    for operation in records[CAP]['operations']:
        if operation['kind']=='invoke-scenario':p['scenarioRelationships'].append(dict(sourceScenario=CAP,targetScenario=operation['scenarioNodeId'],kind='invokes',sourceRefs=['runtime']))
    human(p,'An engineer needs the whole capability to be legible.','Seven boundaries can be inspected without merging their proof.','Status labels stay distinct from the stronger intended experience.')
    beats(p,phases,['Enumerate every source scenario.','Each scenario retains input, event and outcome identities.','Shared providers are bindings; their operating state is unknown.','Stored status results do not upgrade into live-effect claims.','Inspect all six root invocations and the exact source evidence.'],paths)
    return p

def estate():
    p=base('estate-target','Keep the work moving. Keep authority visible.','A three-capability intended circuit · typed product transfers',altitude='estate',mode='TARGET')
    rows=[(CAP,'Interlock','Inspect-only assignment','Resolve authority','Permitted inspection','target.assignment.v1','target.permitted-inspection-request.v1'),
      ('inspect-canonical-circuit-blueprint-candidate','Inspect candidate','Permitted inspection','Inspect candidate','Inspection report','target.permitted-inspection-request.v1','target.reviewable-inspection-report.v1'),
      ('reveal-and-refine-capability-meaning','Reveal meaning','Inspection report','Project for challenge','Human review surface','target.reviewable-inspection-report.v1','target.review-surface.v1')]
    phases=[[],[],[],[],[]];paths=[[],[],[],[],[]]
    for i,(cap,label,inlabel,event,outlabel,inc,outc) in enumerate(rows):
        s=f'target-{i}';a,b,c=f'c{i}-input',f'c{i}-event',f'c{i}-outcome'
        node(p,a,'input',inlabel,'Authored target port',basis='TARGET',cap=cap,scenario=s,productContract=inc)
        node(p,b,'event',event,'Intended capability responsibility',basis='TARGET',cap=cap,scenario=s)
        node(p,c,'outcome',outlabel,'Authored target port',basis='TARGET',cap=cap,scenario=s,productContract=outc)
        paths[1].append(edge(p,a,b,basis='TARGET'));paths[3].append(edge(p,b,c,basis='TARGET'))
        if i:paths[2].append(edge(p,f'c{i-1}-outcome',a,'product-transfer',label=inc,basis='TARGET',productContract=inc))
        phases[0].append(a);phases[1].append(b);phases[3].append(c)
        group(p,s,'Intended '+label,cap=cap,caplabel=label,coverage='Target slice; current scenario internals are not aggregated here',basis='TARGET')
        p['capabilities'][-1]['domain']='Human-governed capability review / editorial cluster'
    node(p,'required-lineage','evidence','Required execution lineage','Request → authority → decision → effect',basis='GAP',scenario=None,layer='support',closure='Admit the exact product interfaces, execute all three boundaries, and bind actual outputs and human review evidence.')
    edge(p,'required-lineage','c2-outcome','evidence-attachment','future closure',basis='GAP');phases[4]=['required-lineage']
    p['scope']=read('declarations/infographic-design-intent.v1.json')['integratedCircuit']['coverage']+' All cross-capability ports here are proposed target contracts; no current deployment is implied.'
    human(p,'The assignment authorizes inspection, not publication.','A permitted inspection yields a report that can be challenged.','The engineer gets useful work and retains publication authority.')
    beats(p,phases,['Keep capability boundaries and input ports visible.','Resolve responsibilities without merging the three authorities.','Only matching target product contracts cross capability boundaries.','The report becomes a human review surface; publication remains pending.','Actual interfaces, dispatch, providers and lineage still need closure.'],paths)
    p['zoomAggregations'].append(dict(id='estate-review',label='Human-governed review circuit',altitude='estate',memberIds=[n['id'] for n in p['nodes']]))
    return p

if __name__=='__main__':
    for factory in [current,certification,capability,estate]:
        p=factory();validate(p);write(f'declarations/infographics/{p["id"]}.json',p)
        print('BOUND',p['id'],len(p['nodes'])+len(p['junctions']),'entities')
