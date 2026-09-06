"""Apply the established film/director workflow to the non-circuit A-W1 lesson.

Lesson authority replaces capsule mechanics for this fictional teaching case.
Existing managed/capsule generation gates remain unchanged. Nano Banana provides
only unlettered human staging; the renderer owns all semantic text and motion.
"""
import argparse, base64, hashlib, json, shutil, urllib.request
from pathlib import Path
from generate_gemini import api_key
from produce_episode_two import ROOT, OUT, dump, digest

DIRECTION = {
 'version':'lesson-film-direction.v1', 'source':'docs/wisdom-pilot/teaching/lesson-a.md',
 'case':'A-W1 v1', 'claimKind':'ILLUSTRATIVE',
 'inheritedWorkflow':['docs/VISUAL-EXPERIENCE-LAW.md','docs/AUDIENCE-DESIGN-LAW.md','declarations/episode-01-direction.json'],
 'identity':'A fictional volunteer, a woman about 40 with short dark curls, an indigo overshirt and a muted rust shirt; a fictional coordinator, a man about 50 with short greying hair and a charcoal cardigan. A modest community planning room, walnut table, pale plaster walls, dark blue notice board, warm practical lamp, late-afternoon window light. A plain cream booking folio with a teal corner tab stays on the table. Natural documentary photography, believable faces and hands, restrained teal and amber light, no science-fiction styling.',
 'members':'Two additional adult group members: a woman about 55 with silver shoulder-length hair and an olive jacket, and a man about 35 with closely cropped dark hair and a sand-colored sweater. These are the same two members in all subsequent shots.',
 'invariants':['The room reservation is confirmed, not the success of the outing.', 'Two members report they cannot attend at that time.', 'The volunteer can ask; only the coordinator can commit a booking change.', 'Other times and costs remain unknown.', 'No booking change, travel support, consensus, or successful outing is depicted as having happened.','A proposed listening conversation is illustrative, not a new fact in A-W1.','Generated imagery contains no legible text, diagram, map, route, status or evidence record.'],
 'shots':[
  {'id':'01','phase':'input','title':'An apparently finished task','camera':'wide oblique establishing shot','action':'The volunteer is handing the closed cream booking folio to the coordinator; both look down at it with modest satisfaction. They are close together at the right side of the walnut table. Physical exchange in progress, two people only. The LEFT 45 percent is quiet dark room depth for later editorial text. No group outing is shown.','meaning':'A booking has been completed; the wider result has not been examined.'},
  {'id':'02','phase':'event','title':'Hear the reported obstacle','camera':'closer eye-level reverse group shot','action':'The same volunteer and coordinator have turned away from the closed folio toward the TWO described members, who stand on the far side of the table. The silver-haired member is speaking with an open hand, while the sand-sweater member stands beside her, concerned but composed. The volunteer has stopped packing away. The coordinator listens attentively. Four people total; visible shift from paperwork to listening. Stage the group in the RIGHT 60 percent; LEFT 40 percent is dark quiet room. No pointing at unreadable screens, no angry gestures, no invented bus schedule.','meaning':'The people affected make the unresolved consequence visible.'},
  {'id':'03','phase':'outcome','title':'Make room for an open decision','camera':'lower table-level side view, wider than the prior close shot','action':'A clearly proposed next-step conversation in the SAME room. All four SAME adults now sit around the table at the RIGHT half of the frame, leaning toward the silver-haired member as she explains what she needs. The volunteer has pulled up a chair and listens with empty hands. The coordinator keeps the cream folio closed near his elbow; a blank notepad lies nearby but nobody signs or changes a booking. Calm focused inquiry, not celebratory relief. LEFT half softly dark negative space. No handshake, applause, departure, group outing, agreed time or happy-ending symbolism.','meaning':'The proposed improvement is whose needs are heard; the final arrangement remains open.'}
 ],
 'motion':{
  'human':'Restrained 2 percent camera push on generated stills, changes in shot scale and blocking. No generated video performance claimed.',
  'plates':'Fixed canonical SVG geometry. Reveal known fact, needed result, and unknowns at their narrated times; gently emphasize the active panel without moving identities or changing relationships.',
  'reflection':'Hold the full prompt still. No countdown or scoring.',
  'semanticBoundary':'No SCL circuit is authored because this lesson represents no executable topology or traversal.'},
 'audienceProfile':{'status':'UNTESTED_CREATIVE_HYPOTHESIS','audience':'People making everyday and AI-assisted decisions','humanStake':'Two intended participants may be excluded despite a completed booking','hook':'The task finished. Did it help?','curiosityQuestion':'What would justify the next step?','emotionalArc':['initial satisfaction','recognition of exclusion','uncertainty','attentive inquiry'],'payoff':'A more careful next question; no invented resolution','shareHypothesis':'Viewers recognize a completed task that missed a human need','demandEvidence':None,'retention':None,'learningOutcomes':None}
}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--execute',action='store_true');args=parser.parse_args()
    directory=OUT/'film-assets';directory.mkdir(exist_ok=True)
    DIRECTION['sourceSha256']=digest(ROOT/DIRECTION['source'])
    dump(OUT/'film-direction.json',DIRECTION)
    assert len({x['camera'] for x in DIRECTION['shots']})==3
    assert len({x['action'] for x in DIRECTION['shots']})==3
    if not args.execute:print('DIRECTED SHOTS READY');return
    selected=[];reference=None
    for shot in DIRECTION['shots']:
        prompt='Generate ONE uninterrupted 16:9 cinematic documentary photograph. No collage, grid, panels, diagram, readable letters or digits, logos, icons, captions, watermarks or interface. '+DIRECTION['identity']+' '+(DIRECTION['members'] if shot['id']!='01' else '')+' CAMERA: '+shot['camera']+'. ACTION: '+shot['action']+' Boundary: '+' '.join(DIRECTION['invariants'])+' Match the reference volunteer, coordinator, wardrobe, folio and room exactly where supplied. Change camera and blocking as directed. Physical staging is fictional, not a record of a real event.'
        parts=[{'text':prompt}]
        if reference:parts.append({'inlineData':{'mimeType':'image/png','data':base64.b64encode(reference.read_bytes()).decode()}})
        payload={'contents':[{'role':'user','parts':parts}],'generationConfig':{'responseModalities':['TEXT','IMAGE'],'imageConfig':{'aspectRatio':'16:9','imageSize':'2K'}}}
        raw=json.dumps(payload).encode();request_digest=hashlib.sha256(raw).hexdigest()
        receipt=directory/f'{shot["id"]}.receipt.json';image=directory/f'{shot["id"]}.png'
        if receipt.exists() and image.exists():
            r=json.loads(receipt.read_text())
            if r.get('requestDigest')==request_digest and r.get('imageDigest')==digest(image):
                selected.append(r);reference=image if shot['id'] in ('01','02') else reference
                print('RESUMED SHOT',shot['id'],flush=True);continue
        request=urllib.request.Request('https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image:generateContent',data=raw,headers={'Content-Type':'application/json','x-goog-api-key':api_key()})
        with urllib.request.urlopen(request,timeout=180) as stream:response=json.load(stream)
        inline=next(part['inlineData'] for c in response.get('candidates',[]) for part in c.get('content',{}).get('parts',[]) if part.get('inlineData',{}).get('mimeType','').startswith('image/'))
        image.write_bytes(base64.b64decode(inline['data'],validate=True))
        r={'shot':shot['id'],'model':'gemini-3-pro-image','provider':'Gemini Nano Banana','requestDigest':request_digest,'imageDigest':digest(image),'path':image.relative_to(ROOT).as_posix(),'prompt':prompt,'sourceSha256':DIRECTION['sourceSha256'],'referenceImageDigest':digest(reference) if reference else None,'semanticReview':'REQUIRED'}
        dump(receipt,r);selected.append(r)
        if shot['id'] in ('01','02'):reference=image
        print('GENERATED SHOT',shot['id'],flush=True)
    dump(OUT/'shot-selection.json',{'shots':selected})

if __name__=='__main__':main()
