"""Compile explicit director decisions before image generation; no semantic invention."""
import hashlib,json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
director=json.loads((ROOT/'data/visual-director.v2.json').read_text())
source=json.loads((ROOT/'declarations/governed-routing.visual-experiences.v1.json').read_text())
specs={s['scenarioId']:s for s in source['experiences']}
jobs=[]
for index,shot in enumerate(director['shots']):
    spec=specs[shot['scenarioId']]
    # Structural checks are prerequisites, not a visual conformance verdict.
    assert len({shot[p]['camera'] for p in ('input','event','outcome')})==3, 'VISUAL_PHASE_COLLAPSE: repeated camera'
    assert len({shot[p]['action'] for p in ('input','event','outcome')})==3, 'VISUAL_PHASE_COLLAPSE: repeated behavior'
    for field in ('changedReality','evidence','boundary'): assert shot['outcome'].get(field)
    prompt=f'''Direct a sophisticated cinematic story in THREE DIFFERENT SHOTS placed in three equal vertical panels across a 16:9 landscape image. Each panel is a separate cinematic frame. Absolutely NO captions, words, labels, phase titles, arrows, checkmarks, badges, glowing scans or infographic styling. The pictures alone must explain a BEFORE, an ACTION, and a CONSEQUENCE.
Visual style: emotionally legible grounded editorial cinema, realistic people and believable hands, tactile papers, warm daylight, subtle film grain, restrained navy and honey palette, richly composed real room, natural skin, shallow depth only when useful. Not miniature props, not an icon exhibit. The room should feel inhabited and useful.
Continuity: {director['identity']}
Continuity means SAME identities but DIFFERENT camera angle, subject placement, body pose, hand activity, composition and experiential state in each panel. Never repeat a tableau and add an effect. If a reference is supplied, preserve identity and color/world only, NEVER its layout or frozen poses.
LEFT SHOT / WORLD BEFORE: {json.dumps(shot['input'])}
CENTER SHOT / WORLD CHANGING: {json.dumps(shot['event'])}
RIGHT SHOT / WORLD AFTER: {json.dumps(shot['outcome'])}
Human staging is a clearly illustrative analogy for an informational capability, not a claim humans manually operate its runtime. Show working copies being arranged, not source state being changed. The outcome is changed KNOWLEDGE or PERMISSION, not an invented physical service effect. Keep any missing slot empty. Never add the missing piece for a satisfying ending.
Source outcome constraints: {json.dumps(spec['outcomeExperience']['observableState'])}
Non-negotiable: {' '.join(director['sourceInvariants'])}
Make the action visible in hand movement and interaction, and make the consequence legible in the recipient's behavior and evidence organization. The center must not be the left image relabeled. The right must not be the center with a checkmark. Distinct camera blocking is essential. No readable text anywhere.'''
    request={'contents':[{'role':'user','parts':[{'text':prompt}]}],'generationConfig':{'responseModalities':['TEXT','IMAGE'],'imageConfig':{'aspectRatio':'16:9','imageSize':'2K'}}}
    jobs.append({'id':hashlib.sha256(prompt.encode()).hexdigest()[:24],'scenarioKey':source['capabilityId']+'::'+shot['scenarioId'],
                 'title':shot['title'],'index':index,'model':'gemini-3-pro-image','format':'scenario-triptych','request':request,
                 'source':source['source'],'spec':spec,'director':shot,'directorVersion':director['version'],
                 'reviewDisposition':'NOT_REVIEWED'})
out=ROOT/'samples/director-v2';out.mkdir(parents=True,exist_ok=True)
(out/'generation-manifest.json').write_text(json.dumps(jobs,indent=2),encoding='utf-8')
print('Compiled eight directed scenarios; structural checks passed. Visual review still required.')
