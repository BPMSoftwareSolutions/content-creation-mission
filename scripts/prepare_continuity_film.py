"""Compile a human-centered local-demo film from capsule evidence and explicit staging."""
import hashlib,json
from pathlib import Path
from mechanics_gate import resolve,validate_grounding
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'samples/narration-continuity';OUT.mkdir(parents=True,exist_ok=True)
def read(p):return json.loads((ROOT/p).read_bytes())
def write(p,v):p.write_text(json.dumps(v,indent=2),encoding='utf-8')
cid='generate-governed-narration'
p=read(f'outputs/scenario-visual-evidence/{cid}/{cid}.json')
for sid in ('resolve-narration-generation-authority','invoke-governed-narration-provider','materialize-narration-artifact','admit-governed-narration-asset'):
    child=read(f'outputs/scenario-visual-evidence/{cid}/{sid}.json')
    for k in ('execution','mechanics','providers','topology'):p['evidence'][k]+=child['evidence'][k]
switch=read('outputs/scenario-visual-evidence/determine-model-role-provider-switch/determine-model-role-provider-switch.json')
# Keep direct mechanics; nested expression cells repeat their containing exact expression.
p['evidence']['mechanics']=[x for x in p['evidence']['mechanics'] if ':expression' not in x['value'].get('cellId','')]
p['evidence']['providers']=[x for x in p['evidence']['providers'] if ':expression' not in x['value'].get('cellId','')]
fixture=p['evidence']['fixtures'][0];sfixture=next(x for x in switch['evidence']['fixtures'] if x['value']['fixture']['fixtureId']=='switch-after-timeout-disposition')
p['compositionEvidence']={'switchFixture':sfixture,'switchMechanic':switch['evidence']['mechanics'],
 'boundary':'Two source responsibilities inform this editorial composition. Their managed end-to-end integration is not asserted. Actual run is the separately identified local demo.'}
identity='One consistent fictional video producer, mid-30s woman, dark brown hair tied in a loose low bun, olive complexion, charcoal work jacket over an off-white shirt, small silver earrings. Small cinematic editing studio at night, large window with soft orange city bokeh on her left, blue practical monitor light, a marked-up off-white script with yellow highlights and pink tabs, the same silver keyboard and black over-ear headphones throughout. Realistic photographic cinema, elegant restrained production design, natural hands and facial anatomy, subtle 35mm grain, anamorphic depth, rich blue-black shadows and amber accents.'
phases={'input':{'camera':'wide profile establishing frame','action':'Producer discovers silent narration while holding her marked-up script; the cut and queued jobs are waiting.'},
 'event':{'camera':'tight moving inspection angle','action':'Producer leans forward as a local demo isolates simulated failure A, rejects incompatible B and sends the unchanged script to live audio provider C.'},
 'outcome':{'camera':'warm reverse medium listening portrait','action':'Producer puts on headphones, listens to the real generated narration, and resumes her edit; failed A stays disconnected.'}}
shots=[
 {'id':'01','phase':'input','title':'The voice is gone.','duration':7,'intensity':6,'emotion':'concern',
  'direction':'Wide side profile. Producer sits in the RIGHT half of the frame with one hand holding the marked-up script, the other hesitating over the keyboard. Her face shows a genuine interrupted thought. Editing monitor visible as a dark angled surface, no legible UI. Cool blue light and a small amber practical signal. Open LEFT half is dark studio depth for later moving graphics. The frozen creative work is the focus, no giant futuristic control room.'},
 {'id':'02','phase':'input','title':'The work is waiting.','duration':6,'intensity':7,'emotion':'urgency',
  'direction':'Intimate macro-to-portrait composition. Script page with yellow highlights and pink tabs prominent in lower RIGHT foreground; producer face in focus above it on RIGHT, tense eyes toward the silent screen. Same outfit and room. LEFT two thirds softly dark negative space. This is unfinished human work, not abstract icons. No readable marks on paper.'},
 {'id':'03','phase':'event','title':'Keep the request. Change the route.','duration':17,'intensity':9,'emotion':'focused anticipation',
  'direction':'Low dynamic three-quarter angle, producer leans sharply forward in RIGHT third, fingertips ready over keyboard, watching the system intervene. Electric cyan screen illumination brightens her face. Muted red-orange failure light remains in far background. LEFT two thirds dark and unobstructed to composite a large kinetic service-routing field. Show active hopeful attention, materially changed body posture.'},
 {'id':'04','phase':'event','title':'A response must become an artifact.','duration':13,'intensity':8,'emotion':'concentration becoming confidence',
  'direction':'Close over-shoulder shot with producer face in RIGHT profile and hand on trackpad lower right. Focused gaze, relaxed brow as result arrives. Cyan and teal light wash across her hands, same marked-up script visible on desk edge. LEFT two thirds clean dark monitor depth for a moving waveform and artifact assembly. No actual UI words or text.'},
 {'id':'05','phase':'outcome','title':'Now she can hear it.','duration':10,'intensity':6,'emotion':'relief',
  'direction':'Warm reverse medium portrait. The SAME producer is on RIGHT half now wearing black over-ear headphones, shoulders lowered, eyes gently closed for a moment listening, subtle honest relieved smile. Her marked script now rests on desk. Window city glow warms cheek. LEFT half contains softly defocused edit monitor and room depth. Clear emotional release, no triumph pose.'},
 {'id':'06','phase':'outcome','title':'The story stays hers.','duration':11,'intensity':5,'emotion':'renewed creative momentum',
  'direction':'Wider reverse angle in the same studio. Producer on RIGHT wearing headphones is actively editing with one hand on mouse and one on the script, upright easy posture, small satisfied smile as she looks toward edit screen. Rich teal-blue room, warmer amber dawnlike practical light at window (same night exterior). LEFT two thirds dark editorial negative space. The work visibly resumed. No new people, readable text, badges, logos, watermarks or invented numbers.'}]
beats=[]
for i,s in enumerate(shots):
    refs=[fixture['source']]
    if s['id']=='03':refs.append(sfixture['source'])
    else:refs += [x['source'] for x in p['evidence']['execution']][:1]
    beats.append({'ordinal':i,'phase':s['phase'],'title':s['title'],'visibleChange':s['direction'],
                  'sourceRefs':refs,'claimType':'EDITORIAL_COMPOSITION_WITH_LOCAL_DEMO','durationSeconds':s['duration']})
p['visualDirection']={**phases,'identity':identity,'entities':['producer','marked-up script','editing console','simulated failed provider A','incompatible B','live speech provider C','standby D','narration waveform','artifact and receipt','local queue'],
 'sourceBoundary':'Human world, seven-job local queue, screen staging and inter-capability composition are explicit editorial/demo choices.',
 'providerReality':'A is simulated unavailable, B is locally declared text-only, C is Gemini speech invoked live, D is not invoked.',
 'continuity':['Same script digest before and after provider change','Same producer, wardrobe and studio','A remains outside active path','One completed local job changes the illustrative queue from seven to six'],
 'materialChange':'A producer unable to hear her narration receives a real playable WAV and returns to editing.'}
p['animationBeats']=beats;p['selectedFixture']=fixture
p['disposition']='MECHANICS_DIRECTION_REVIEWED';p['findings']=[]
p['groundingReview']={'gherkinOnlyInsufficient':True,'reviewer':'Codex source inspection and explicitly scoped local-demo direction',
 'specificMechanicalFacts':['Narration provider modality and payload rejection boundaries','Binary artifact materialization port','Audio digest and provider lineage in admitted asset fixture','Switch timeout fixture preserves non-provider digests and user-facing continuity'],
 'limitations':['Not an observed managed end-to-end recovery','Provider failure is injected in local demo','Capsule fixtures contain simulated portOutcomes','Cinematic frames are editorial staging, not a recording of a real customer']}
path=ROOT/'declarations/narration-continuity.film.json';write(path,p)
binding={'path':str(path.relative_to(ROOT)).replace('\\','/'),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
jobs=[]
for s in shots:
    prompt='Generate ONE cinematic 16:9 film frame, not a triptych, collage, storyboard sheet, illustration or technical diagram. '+identity+' SHOT: '+s['direction']+' Absolutely no readable text, logos, digits, fake interfaces, arrows or floating labels. All precise software motion and identifiers will be composited separately. Keep the human on the right and generous usable dark space on the left. The story is a producer recovering interrupted creative work. Match the reference person and room exactly if provided; change the shot and pose as directed.'
    repairs=ROOT/'data/continuity-shot-repairs.json'
    if repairs.exists():prompt+=json.loads(repairs.read_bytes()).get(s['id'],'')
    j={'id':hashlib.sha256(prompt.encode()).hexdigest()[:24],'scenarioKey':p['key'],'mechanicsEvidence':binding,
       'model':'gemini-3-pro-image','format':'cinematic-shot','director':p['visualDirection'],'directorVersion':'human-experience-film.v1',
       'shot':s,'request':{'contents':[{'role':'user','parts':[{'text':prompt}]}],
           'generationConfig':{'responseModalities':['TEXT','IMAGE'],'imageConfig':{'aspectRatio':'16:9','imageSize':'2K'}}}}
    validate_grounding(j);jobs.append(j)
write(OUT/'generation-manifest.json',jobs);write(OUT/'film-direction.json',{'identity':identity,'shots':shots,'evidence':binding,'durationSeconds':64})
profile={'profileVersion':'audience-design.v1','status':'UNTESTED_CREATIVE_HYPOTHESIS','filmId':'narration-continuity-film.v1',
 'demandTheme':'AI reliability interrupting creative work','audience':'People building or depending on AI production workflows',
 'demandEvidence':None,'humanStake':'A producer cannot finish the narration for her cut',
 'triggers':['recognition','unresolved tension','visible transformation','competence','relief'],
 'intensityCurve':[6,7,9,8,6,5],'emotionArc':['concern','urgency','anticipation','confidence','relief','creative momentum'],
 'hookVariants':[{'id':'A','title':'The cut was ready. The voice was gone.','hypothesis':'Concrete creative interruption earns attention.'},
                 {'id':'B','title':'How did her narration come back?','hypothesis':'A visible relief payoff creates curiosity about the recovery.'}],
 'payoff':'Hear the finished narration and see the producer return to the cut.',
 'prohibitedClaims':['Guaranteed virality','Uninterrupted production','Proven 30-second recovery','Unmeasured performance uplift'],
 'metrics':{k:None for k in ['impressions','ctr','viewedVsSwipedAway','firstSecondRetention','retention30Seconds','averagePercentViewed','shares','rewatchMoments','subscriberConversion','websiteClicks']},
 'research':[{'url':'https://support.google.com/youtube/answer/16559650?hl=en','verified':'2026-09-05','finding':'Appeal, engagement and satisfaction; opening delivers title/thumbnail promise.','evidenceType':'PLATFORM_GUIDANCE'},
             {'url':'https://www.sciencedirect.com/science/article/abs/pii/S0747563226001573','status':'UNVERIFIED_ACCESS_DENIED','usedForClaims':False}]}
write(OUT/'audience-profile.json',profile)
print('Six human-centered shots and an untested audience profile compiled from explicit composition evidence.')
