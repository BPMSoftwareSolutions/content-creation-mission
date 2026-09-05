"""Prepare source-bound contracts for the estate; author one complete editorial package."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'declarations/capability-content';OUT.mkdir(parents=True,exist_ok=True)
def read(p):return json.loads((ROOT/p).read_bytes())
def write(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
records=read('inventories/scenario-inventory.json');groups={}
for r in records:groups.setdefault(r['capabilityId'],[]).append(r)
for cid,scenarios in groups.items():
    path=OUT/(cid+'.json')
    # Source inventory must never erase an already authored story.
    if path.exists():continue
    src=read('data/capsule-evidence/capabilities/'+cid+'.json')
    c={'contractVersion':'capability-content.v1','capabilityId':cid,'title':scenarios[0]['capabilityName'],
       'status':'NEEDS_DIRECTION','source':{k:src[k] for k in ('capsuleDigest','estateManifestDigest')},
       'scenarioKeys':[s['key'] for s in scenarios],'audience':None,'humanProblem':None,'experience':None,
       'entities':[],'mechanics':[],'claims':[],'evidence':[],'emotionalArc':[],
       'permittedSurfaces':[],'surfaceContracts':{},'scope':'Source-bound editorial inventory. Human story and permitted projections require direction.'}
    write(path,c)
cid='generate-governed-narration';path=OUT/(cid+'.json');c=read(str(path.relative_to(ROOT)))
if c['status']=='NEEDS_DIRECTION':
    def evidence(id,p,kind):return {'id':id,'path':p,'sha256':hashlib.sha256((ROOT/p).read_bytes()).hexdigest(),'kind':kind}
    c.update(title='Generate Governed Narration',status='EDITORIALLY_REVIEWED',
      audience='Video producers and engineers responsible for dependable AI-assisted content production.',
      humanProblem='A producer has a script and a ready cut, but cannot continue the edit without usable narration.',
      experience={'input':'A producer has unfinished narration, a marked-up script and waiting work.',
        'event':'The local demo retains the script, skips an unavailable primary and an incompatible candidate, obtains live speech, and verifies its file.',
        'outcome':'The producer can hear her narration and return to the cut; one local job is complete.'},
      entities=read('samples/narration-continuity/entity-sheet.json'),
      emotionalArc=['concern','focused anticipation','relief'],
      scope='Editorial composition led by Generate Governed Narration, with provider-switching context. The local demo is observed; a managed end-to-end recovery is not asserted. The fictional producer and studio dramatize the human experience.')
    c['evidence']=[evidence('narration-capsule','data/capsule-evidence/capabilities/generate-governed-narration.json','CAPSULE_INDEX'),
      evidence('narration-reality','outputs/scenario-visual-evidence/generate-governed-narration/generate-governed-narration.json','CAPSULE_EVIDENCE_PACKAGE'),
      evidence('switch-reality','outputs/scenario-visual-evidence/determine-model-role-provider-switch/determine-model-role-provider-switch.json','CAPSULE_EVIDENCE_PACKAGE'),
      evidence('demo','samples/narration-continuity/demo.receipt.json','OBSERVED_LOCAL_DEMO'),
      evidence('audio','samples/narration-continuity/finished-narration.wav','GENERATED_AUDIO'),
      evidence('direction','declarations/narration-continuity.film.json','EDITORIAL_DIRECTION')]
    c['claims']=[
      {'id':'promise','text':'The narration capability accepts an admitted scene graph and returns one narration asset or exact held/rejection evidence.','kind':'CAPSULE_DECLARATION','evidenceIds':['narration-reality']},
      {'id':'boundaries','text':'The declared narration flow resolves authority, invokes a speech provider, materializes an artifact, and admits the resulting asset.','kind':'CAPSULE_DECLARATION','evidenceIds':['direction','narration-reality']},
      {'id':'switch-scope','text':'Provider-switching declarations preserve non-provider meaning and user-facing continuity; they are a supporting responsibility in this editorial composition.','kind':'CAPSULE_DECLARATION','evidenceIds':['switch-reality']},
      {'id':'same-script','text':'The local demo preserves the exact script digest through provider selection.','kind':'OBSERVED_LOCAL_DEMO','evidenceIds':['demo']},
      {'id':'provider-change','text':'In the local demo, A is unavailable by simulation, B is text-only and ineligible, C makes a live Gemini speech call, and D is not invoked.','kind':'OBSERVED_LOCAL_DEMO','evidenceIds':['demo']},
      {'id':'playable','text':'A real 8.21-second WAV is saved and hash-verified; one of seven illustrative local jobs completes.','kind':'OBSERVED_LOCAL_DEMO','evidenceIds':['demo','audio']},
      {'id':'human-payoff','text':'The fictional producer listens with relief and returns to editing.','kind':'EDITORIAL_STAGING','evidenceIds':['direction']}]
    c['mechanics']=[{'id':'authority','meaning':'Bind narration to admitted scene intent and performance profile.','evidenceIds':['narration-reality','direction']},
      {'id':'selection','meaning':'Preserve the request while distinguishing unavailable, incompatible and selected demo providers.','evidenceIds':['demo','switch-reality']},
      {'id':'realization','meaning':'Speech response becomes a materialized audio artifact with digest and provenance.','evidenceIds':['demo','audio','direction']}]
    structures={
      'video':['Human interruption','Provider action','Artifact and evidence','Audible payoff'],
      'short':['Compressed interruption','One provider transformation','One audible payoff'],
      'thumbnail':['Recognizable producer','Unfinished work or relief','A truthful curiosity hook'],
      'article':['Human problem','Capability promise','Mechanics','Observed demonstration','Interpretation and limits'],
      'infographic':['Persistent entities','Input relationships','Event transformation','Outcome evidence'],
      'training':['Learning objective','Scenario','Demonstration','Exercise','Assessment and answer rationale'],
      'demo':['Failure injection scope','Ordered candidate checks','Live audio result','Verified receipt'],
      'landing-page':['Audience and problem','Experience promise','Watch/read/learn/inspect','Evidence'],
      'evidence-story':['Claim','Source authority or observed receipt','What it proves','What it does not prove']}
    c['permittedSurfaces']=list(structures)
    for surface,structure in structures.items():
        c['surfaceContracts'][surface]={'purpose':'Express the same human experience as '+surface+'.',
          'structure':structure,'claimIds':[x['id'] for x in c['claims']],
          'evidenceIds':[e['id'] for e in c['evidence']]}
    c['storyTitle']='The provider changed. The story stayed hers.'
    c['training']={'objective':'Distinguish capability meaning, provider selection, media materialization, and evidence of completion.',
      'exercise':'A returns unavailable; B can only return text; C returns an audio payload. Describe the next permitted action and the evidence still needed before declaring an asset ready.',
      'questions':[{'question':'Does selecting C prove that narration exists?','options':['Yes, selection completes the job.','No, the media must be returned and materialized.'],'correct':1,'rationale':'Selection and artifact completion are separate boundaries.'},
       {'question':'Which part of the film is an observed fact?','options':['The fictional producer experienced a real outage.','The local demo produced a hash-verified WAV.'],'correct':1,'rationale':'The producer is staging. The local audio and receipt are inspectable artifacts.'},
       {'question':'Can B serve this audio request?','options':['No: its declared modality is text only.','Yes: any provider is interchangeable.'],'correct':0,'rationale':'Provider substitution must satisfy the requested modality and other constraints.'}]}
    write(path,c)
write(ROOT/'data/content-provider-bindings.json',{'bindingVersion':'content-realization.v1','providers':{
 'video':'existing-reviewed-animatic','short':'ffmpeg-editorial-cut','thumbnail':'existing-composited-image','article':'deterministic-html',
 'infographic':'deterministic-svg','training':'deterministic-html','demo':'existing-local-demo','landing-page':'deterministic-html','evidence-story':'deterministic-html'},
 'assets':{'video':'samples/narration-continuity/the-story-stays-hers.mp4','thumbnail':'samples/narration-continuity/thumbnail-a.jpg',
 'audio':'samples/narration-continuity/finished-narration.wav','demoReceipt':'samples/narration-continuity/demo.receipt.json'}})
print('Source-bound contracts:',len(groups),'; one editorial contract authored. Existing authored contracts preserved.')
