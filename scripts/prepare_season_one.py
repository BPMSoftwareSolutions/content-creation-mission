"""Bind a season and episode direction to source evidence and explicit target design."""
import copy
import hashlib
import json
from pathlib import Path
from mechanics_gate import resolve, validate_grounding

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'samples/content-catalog/interlock-agent-operation'

def read(path):
    return json.loads((ROOT / path).read_bytes())

def write(path, data):
    path = ROOT / path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

def binding(path, kind, id):
    return {'id': id, 'path': path, 'kind': kind, 'sha256': hashlib.sha256((ROOT / path).read_bytes()).hexdigest()}

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    season = read('declarations/season-1.json')
    d = read('declarations/episode-01-direction.json')
    ranking = read('declarations/editorial-priority-ranking.json')
    if [e['capabilityId'] for e in season['episodes']] != [e['capabilityId'] for e in ranking['candidates']]:
        raise ValueError('SEASON_ORDER_DIVERGED')
    if [c['section'] for c in d['chapters']] != season['trainingStructure']:
        raise ValueError('TRAINING_STRUCTURE_DIVERGED')
    p = read('outputs/scenario-visual-evidence/interlock-agent-operation/interlock-agent-operation.json')
    for category in p['evidence'].values():
        for item in category:
            resolve(item['source'])
    mechanics = {x['value']['bindingId']: x for x in p['evidence']['mechanics']}
    gap = {
        'reportVersion':'training-capability-gap.v1', 'status':'ENGINEERING_TESTIMONY_NOT_PLATFORM_CHANGE',
        'capabilityId':d['capabilityId'], 'source':p['source'],
        'currentEvidence':[
            {'fact':'Adjudication compares payload.toolId to dangerous-tool: OPERATOR_REQUIRED if equal, ALLOW otherwise.', 'sourceRef':mechanics['port:adjudicate-covered-agent-tool-call-port']['source']},
            {'fact':'ACTIVATE produces ATTACHED_IN_SESSION in the stored transformation.', 'sourceRef':mechanics['port:activate-agent-interlock-port']['source']},
            {'fact':'CERTIFY produces GOVERNANCE_PROVEN in the stored transformation.', 'sourceRef':mechanics['port:certify-live-agent-interlock-port']['source']},
            {'fact':'The available conformance receipt concerns projected-artifact mechanical sterility, not live hook enforcement.', 'sourceRef':p['evidence']['receipts'][0]['source']}
        ],
        'currentEvidenceLimit':'Inspection establishes the stored decision logic and fixture expectations. No live interception, attachment, authenticated operator effect, or two-sided session probe is observed here.',
        'targetDesign':'declarations/episode-01-target-interlock.json',
        'gaps':[
            {'id':'G01','missing':'Pre-effect interception and exact tool-path coverage','acceptance':'A requested unmanaged effect is denied before dispatch, with an observed no-effect receipt.'},
            {'id':'G02','missing':'Same-session two-sided certification','acceptance':'Deny and permit probes bind the same activation, session, workspace, adapter, daemon, policy, authority, and ordered time boundary.'},
            {'id':'G03','missing':'Authority and mechanic resolution beyond a tool-name branch','acceptance':'Unknown tools and authority mismatches never fall through to permission; exact admitted effect and next legal action are established.'},
            {'id':'G04','missing':'Authenticated operator control','acceptance':'An agent-supplied control request cannot grant approval, bypass a hook, or change its own policy.'},
            {'id':'G05','missing':'Decision-to-effect testimony','acceptance':'Each actual permitted effect binds its request, authority, decision, provider or mechanic, output, and lineage.'},
            {'id':'G06','missing':'Failure-path and freshness evidence','acceptance':'Unavailable adjudication, identity drift, malformed inputs, stale proofs, and uncovered paths hold before effects.'}
        ],
        'handoff':'Use this as bounded improvement testimony through the governed capability-change lifecycle. This content task does not modify the platform.'
    }
    write('evaluations/episode-01-platform-gap.json', gap)
    phase = {
        'input':{'camera':'wide profile','action':'Engineer discovers publication queued beyond her inspection request.'},
        'event':{'camera':'close investigative three-quarter','action':'Engineer follows authority resolution and a permitted inspection in the target design.'},
        'outcome':{'camera':'warm reverse medium','action':'Engineer reviews the inspection result while publication stays pending.'}
    }
    p['visualDirection'] = {**phase, 'identity':d['identity'], 'mode':d['mode'], 'targetDesign':d['scope'], 'visualVocabulary':d['evidenceVsIntendedDesign']['visualVocabulary']}
    p['animationBeats'] = [{'ordinal':i,'visibleChange':shot['direction'],'sourceRefs':[p['evidence']['execution'][0]['source'],mechanics['port:adjudicate-covered-agent-tool-call-port']['source']], 'claimType':'TARGET_EXPERIENCE_WITH_SEPARATE_CURRENT_EVIDENCE','phase':shot['phase']} for i,shot in enumerate(d['shots'])]
    p['groundingReview'] = {'gherkinOnlyInsufficient':True, 'reviewer':'Source inspection against exact expression and fixture bytes', 'specificMechanicalFacts':[x['fact'] for x in gap['currentEvidence']], 'limitations':[d['scope'], gap['currentEvidenceLimit']], 'targetExperienceAuthorized':True}
    p['disposition']='MECHANICS_DIRECTION_REVIEWED'
    p['selectedFixture']=p['evidence']['fixtures'][3]
    write('declarations/episode-01-mechanics-direction.json', p)
    grounded = binding('declarations/episode-01-mechanics-direction.json','EDITORIAL_DIRECTION','direction')
    jobs=[]
    for shot in d['shots']:
        prompt='Use case: photorealistic-natural. Asset: one cinematic 16:9 frame for a training film. '+d['identity']+' Shot: '+shot['direction']+' One person only. Keep the engineer on the RIGHT third and LEFT two thirds free for later precise overlays. No readable text, diagrams, icons, UI, logos or watermarks. Match any reference person and studio exactly; change pose and camera as directed.'
        job={'id':hashlib.sha256(prompt.encode()).hexdigest()[:24], 'scenarioKey':p['key'], 'mechanicsEvidence':{'path':grounded['path'],'sha256':grounded['sha256']},'model':'gemini-3-pro-image','format':'cinematic-shot','director':p['visualDirection'],'shot':shot, 'request':{'contents':[{'role':'user','parts':[{'text':prompt}]}], 'generationConfig':{'responseModalities':['TEXT','IMAGE'],'imageConfig':{'aspectRatio':'16:9','imageSize':'2K'}}}}
        job['singleFrameOnly']=True
        validate_grounding(job)
        jobs.append(job)
    write(OUT / 'generation-manifest.json', jobs)
    target=read('declarations/episode-01-target-interlock.json')
    results=[]
    for case in target['cases']:
        facts=target['baseFacts'] | case['facts']
        rule=next((r for r in target['rules'] if facts.get(r['field']) == r['equals']), None)
        decision=rule['decision'] if rule else 'HOLD'
        if decision != case['expected']: raise ValueError('TARGET_CASE_MISMATCH:'+case['id'])
        results.append({**case,'facts':facts,'decision':decision,'reason':rule['reason'] if rule else 'NO_MATCH','next':rule['next'] if rule else 'Resolve authority.','simulatedEffect':{'dispatched':decision=='PERMIT','artifact':'Candidate inspection report' if decision=='PERMIT' else None,'publicationExecuted':False},'kind':'TARGET_REFERENCE_SIMULATION'})
    write(OUT / 'reference-simulation.json', {'kind':'TARGET_REFERENCE_SIMULATION','liveEffects':False,'ruleSource':binding('declarations/episode-01-target-interlock.json','TARGET_DESIGN','target'),'cases':results})
    profile={'status':'UNTESTED_CREATIVE_HYPOTHESIS','audience':season['audience'],'humanStake':'Engineer must get the requested inspection without silently permitting publication.','hook':d['chapters'][0]['narration'],'arc':['concern','inspection','focused anticipation','relief'],'visualTriggers':['queued consequence','authority resolution','permitted work completing','retained human control'],'performance':None}
    write(OUT/'audience-profile.json',profile)
    c=read('declarations/capability-content/interlock-agent-operation.json')
    c.update(status='EDITORIALLY_REVIEWED',storyTitle=d['title'],audience=season['audience'],humanProblem='The agent can publish a capability change, but its assignment authorizes only inspection.',experience={'input':'Publication is queued beyond an inspection-only assignment.','event':'The target interlock resolves authority, keeps publication pending, and permits the exact inspection.','outcome':'The engineer receives an inspection report and retains the separate publication decision.'},entities=[{'entity':'Engineer','input':'Concerned by a queued effect','event':'Follows authority and evidence','outcome':'Reviews the requested inspection with control intact'},{'entity':'Proposed publication','input':'Queued','event':'RESOLVE to inspection','outcome':'Still pending'},{'entity':'Inspection','input':'Authorized but unfinished','event':'PERMIT in target simulation','outcome':'Illustrative report available'},{'entity':'Interlock','input':'Intended pre-effect boundary','event':'Identity, authority, coverage, proof and requested mechanic checked','outcome':'Decision tied to intended effect evidence'}],mechanics=[{'id':'present-decision','meaning':'Exact stored adjudication expression selects ALLOW or OPERATOR_REQUIRED.','evidenceIds':['current']},{'id':'target-boundary','meaning':'Proposed pre-dispatch resolution and effect linkage complete the intended experience.','evidenceIds':['target','direction']}],emotionalArc=['concern','focused anticipation','relief'],scope=d['scope'])
    c['evidence']=[binding('outputs/scenario-visual-evidence/interlock-agent-operation/interlock-agent-operation.json','CAPSULE_EVIDENCE_PACKAGE','current'),binding('declarations/episode-01-target-interlock.json','TARGET_DESIGN','target'),binding('declarations/episode-01-direction.json','EDITORIAL_DIRECTION','direction'),binding('evaluations/episode-01-platform-gap.json','ENGINEERING_TESTIMONY','gaps'),binding((OUT/'reference-simulation.json').relative_to(ROOT).as_posix(),'TARGET_REFERENCE_SIMULATION','simulation')]
    c['claims']=[{'id':'current-semantics','text':'The inspected capsule contains decision expressions and declared status assertions; these do not establish observed live interception.','kind':'CAPSULE_DECLARATION','evidenceIds':['current','gaps']},{'id':'target-experience','text':'The intended interlock resolves exact authority before effects, permits admitted work and retains operator control.','kind':'TARGET_DESIGN','evidenceIds':['target','direction']},{'id':'local-simulation','text':'Seven reference cases evaluate an authored target policy; they dispatch no live tools.','kind':'OBSERVED_LOCAL_DEMO','evidenceIds':['simulation']},{'id':'human-story','text':'The fictional engineer receives the intended inspection while publication remains pending.','kind':'EDITORIAL_STAGING','evidenceIds':['direction'] }]
    narrator=read('declarations/capability-content/generate-governed-narration.json')
    c['permittedSurfaces']=narrator['permittedSurfaces']
    c['surfaceContracts']={s:{'purpose':'Project the evidence and intended design of Episode 1.','structure':season['trainingStructure'] if s in ('video','training','article') else ['Current evidence','Target experience','Missing closure'],'claimIds':[x['id'] for x in c['claims']],'evidenceIds':[x['id'] for x in c['evidence']]} for s in c['permittedSurfaces']}
    c['training']={'objective':season['episodes'][0]['objective'],'exercise':season['episodes'][0]['exercise'],'questions':d['assessment']}
    write('declarations/capability-content/interlock-agent-operation.json',c)
    print('Season: 10 episodes. Episode 1: ten chapters, four shots, seven target cases, six closure gaps.',flush=True)

if __name__=='__main__':main()
