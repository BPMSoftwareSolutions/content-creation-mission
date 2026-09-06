"""Produce the public Consequences lesson from A-W1; no reserved assessments.

Deterministic SVG decision plates + cached Gemini speech. This editorial film
is neither a circuit execution nor evidence that the learning pilot passed.
"""
import argparse, hashlib, html, json, math, re, shutil, subprocess, sys, wave
from pathlib import Path

import cairosvg
import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont
import run_narration_continuity_demo as tts

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'releases/episode-02'
SITE = ROOT / 'release-site/public/episode-02'
TITLE = 'The Task Finished. Did It Help? | SideFX Episode 2'
URL = 'https://sidefx-agentic-engineering.sjonesbpm.chatgpt.site/episodes/02'
FONT = 'C:/Windows/Fonts/segoeui.ttf'
BOLD = 'C:/Windows/Fonts/segoeuib.ttf'
BG, WHITE, MUTED, TEAL, AMBER = '#091016', '#f3f7f8', '#b3c1ca', '#7cddd8', '#f5c779'

# Public worked example only. The independent diagnostic/transfer bank stays private.
SCENES = [
 dict(id='01', title='The task finished. Did it help?', label='THE QUESTION',
      headline=['The task finished.', 'Did it help?'],
      body='A completed action. A result people can use. Are they the same?',
      narration='The task is finished. The confirmation arrived. But did it help? Before we talk about artificial intelligence, consider an ordinary decision: arranging an outing for a group of people.'),
 dict(id='02', title='A confirmed reservation', label='A FICTIONAL WEEKEND OUTING',
      headline=['The room is booked.'],
      cards=[('COMPLETED', 'Room reservation confirmed.', TEAL),
             ('REPORTED', 'Two members cannot attend: the time conflicts with their last bus home.', AMBER)],
      narration='A volunteer reserves a room for a weekend group outing. The booking is confirmed. But the time conflicts with the last bus home for two members. They say they cannot attend at that time.'),
 dict(id='03', title='Who can decide?', label='THE DECISION',
      headline=['“The reservation succeeded,', 'so the outing is arranged.”'],
      body='The volunteer can ask about options. Only the coordinator can commit to a booking change.',
      narration='The volunteer can ask about another slot. Only the group coordinator can commit to changing the booking. The coordinator says: The reservation succeeded, so the outing is arranged.'),
 dict(id='04', title='Pause and make your call', label='YOUR FIRST JUDGMENT',
      headline=['What should happen next?', 'Why?'],
      body='Pause the video. Write your decision before hearing the discussion.',
      narration='What should happen next, and why? Pause the video and write your decision before hearing the discussion. You can leave the final choice open if you explain what you still need to know.', pause=9),
 dict(id='05', title='Choose what helps explain it', label='BEFORE THE PLATE',
      headline=['Would a table help?', 'What would it leave out?'],
      body='A written account is also a valid choice.',
      narration='Would a small table help you explain this situation? Or would a written account preserve something the table loses? Either can work. Keep the affected people and the unresolved facts in view.', pause=3),
 dict(id='06', title='Separate action, result, and uncertainty', label='A DECISION PLATE',
      headline=['Is the outing arranged for', 'the people who need it?'],
      cards=[('WHAT HAPPENED', 'A room reservation was confirmed.', TEAL),
             ('WHAT PEOPLE NEED', 'An outing the intended participants can actually attend.', WHITE),
             ('WHAT REMAINS OPEN', 'Two report a travel conflict. Other times and costs are unknown.', AMBER)],
      narration='Here is one way to separate the facts. What happened: a room reservation was confirmed. What people need: an outing the intended participants can actually attend. What remains open: two members report a travel conflict. Other times and costs are unknown.'),
 dict(id='07', title='What the confirmation proves', label='THE LIMIT OF THE EVIDENCE',
      headline=['A booking record proves', 'a reservation.'],
      body='It does not prove that everyone can attend.',
      narration='The booking record supports a narrow claim: there is a reservation. It does not establish that everyone can attend. A defensible next step is to ask about alternatives and hear the affected members before promising that the outing is fully arranged.'),
 dict(id='08', title='An objection that matters', label='CHALLENGE YOUR FIRST ANSWER',
      headline=['Moving it could exclude', 'someone else.'],
      body='Some people have already planned around the original time.',
      narration='Now another organizer objects. People have already planned around this time. Moving the outing could inconvenience them, or exclude someone else. That objection matters. Asking about alternatives does not yet justify changing the booking.'),
 dict(id='09', title='Compare the consequences', label='OPTIONS TO DISCUSS',
      headline=['Who bears the cost', 'of each option?'],
      cards=[('EXPLORE', 'A different time.\nTravel support, if feasible.', TEAL),
             ('ALSO CONSIDER', 'Postponement.\nKeeping the booking while explicitly acknowledging the exclusion.', AMBER)],
      narration='Compare a different time, travel support if it is feasible, postponement, and keeping the booking with the exclusion explicitly acknowledged. Hear from the people who bear each cost. The coordinator has a decision role. That role does not make every choice fair.'),
 dict(id='10', title='What would change your judgment?', label='REVISE WITH A REASON',
      headline=['What would change', 'your judgment?'],
      body='Name a specific fact that could change your next step.',
      narration='What would change your judgment? Name a specific fact that could change your next step. Pause and write it down.', pause=8),
 dict(id='11', title='New facts can change the next step', label='CONDITIONAL EXAMPLES',
      headline=['New facts can change', 'the next step.'],
      body='An acceptable travel option? A different time that excludes more people? These are possibilities, not facts in the story.',
      narration='Perhaps the two members identify an acceptable travel option. Perhaps a different time would exclude more people. Neither is established in this story. Either could change the next step. Neither would make the original confirmation proof that the whole arrangement worked.'),
 dict(id='12', title='Completion is one fact', label='CONSEQUENCES · SIDEFX FOUNDATIONS',
      headline=['Completion is one fact.', 'Consequences need judgment.'],
      body='Which result do you mean? Who still cannot get what they need?',
      narration='A conversation and a list of alternatives may be enough. Changing a booking does not necessarily recover preparation time or missed participation. This is the consequences lens we are starting with in SideFX: when someone says a task is complete, ask which result they mean, and who still cannot get what they need.'),
 dict(id='13', title='Carry the question with you', label='CONTINUE THE PRACTICE',
      headline=['Choose one completed task.', 'Whose result is still open?'],
      body='Describe the missing result and the evidence you would need.\nNext: What do we actually know?',
      narration='Think of one completed task in your own work. Whose result might still be unresolved? Describe the missing result and the evidence you would need. Next, we will ask: What do we actually know?', pause=2),
]

def dump(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

def public_data(release):
    return {k:release.get(k) for k in ('title','videoUrl','landingPage','durationSeconds','chapters','filmSha256','webFilmSha256','disclosure')}

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def wrap(text, width, size, bold=False):
    font = ImageFont.truetype(BOLD if bold else FONT, size)
    lines = []
    for paragraph in text.split('\n'):
        line = ''
        for word in paragraph.split():
            candidate = (line + ' ' + word).strip()
            if font.getlength(candidate) > width and line:
                lines.append(line)
                line = word
            else:
                line = candidate
        lines.append(line)
    return lines

def text_svg(lines, x, y, size, color=WHITE, bold=False, leading=1.22):
    font = ImageFont.truetype(BOLD if bold else FONT, size)
    for line in lines:
        assert x + font.getlength(line) < 1840, (line, x, size)
    return ''.join(f'<text x="{x}" y="{y + i*size*leading:.1f}" font-family="Segoe UI" font-size="{size}" font-weight="{700 if bold else 400}" fill="{color}">{html.escape(line)}</text>' for i,line in enumerate(lines))

def make_svg(scene, index):
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080"><title>{html.escape(scene["title"])}</title><desc>Illustrative teaching plate based on fictional case A-W1. This is not an execution trace.</desc>',
         f'<rect width="1920" height="1080" fill="{BG}"/>',
         '<defs><linearGradient id="line"><stop stop-color="#7cddd8"/><stop offset="1" stop-color="#ac98ff"/></linearGradient></defs>',
         '<rect x="100" y="107" width="62" height="5" fill="url(#line)"/>']
    s.append(text_svg(['SideFX'], 100, 77, 30, WHITE, True))
    s.append(text_svg(['02 / CONSEQUENCES'], 1370, 77, 25, MUTED))
    s.append(text_svg([scene['label']], 100, 175, 29, TEAL, True))
    size = 79 if max(len(t) for t in scene['headline']) < 34 else 70
    s.append(text_svg(scene['headline'], 100, 302, size, WHITE, True, 1.16))
    if 'cards' in scene:
        cards = scene['cards']; n = len(cards); gap=28; width=(1720-gap*(n-1))/n
        for i,(label,body,color) in enumerate(cards):
            x=100+i*(width+gap)
            s.append(f'<rect x="{x}" y="495" width="{width}" height="393" rx="10" fill="#121e28" stroke="#2c3c49"/>')
            s.append(f'<rect x="{x}" y="495" width="{width}" height="4" fill="{color}"/>')
            s.append(text_svg([label], x+30, 553, 25, color, True))
            lines=wrap(body,width-64,39)
            assert len(lines)<=6, lines
            s.append(text_svg(lines, x+30, 628, 39, WHITE, False, 1.27))
    else:
        s.append(text_svg(wrap(scene['body'],1550,45),100,574,45,MUTED,False,1.4))
        if scene.get('pause',0)>=8:
            s.append(text_svg(['PAUSE HERE · TAKE THE TIME YOU NEED'],100,830,28,AMBER,True))
    s.append('<path d="M100 963 H1820" stroke="#2c3c49"/>')
    s.append(f'<path d="M100 963 H{100+1720*(index+1)/len(SCENES):.1f}" stroke="{TEAL}" stroke-width="3"/>')
    s.append(text_svg(['ILLUSTRATIVE · FICTIONAL CASE A-W1'],100,1019,23,MUTED))
    s.append(text_svg([f'{index+1:02d} / {len(SCENES):02d}'],1650,1019,23,MUTED))
    s.append('</svg>')
    return ''.join(s)

def timecode(seconds, srt=False):
    ms=round(seconds*1000); h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000)
    return f'{h:02}:{m:02}:{s:02}{"," if srt else "."}{ms:03}'

def main():
    p=argparse.ArgumentParser();p.add_argument('--execute', action='store_true');args=p.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    for folder in ['plates','audio','clips']:(OUT/folder).mkdir(exist_ok=True)
    dump(OUT/'direction.json',{'title':TITLE,'series':'SideFX Foundations','source':'docs/wisdom-pilot/teaching/lesson-a.md','sourceSha256':digest(ROOT/'docs/wisdom-pilot/teaching/lesson-a.md'),'case':'A-W1 v1','status':'ILLUSTRATIVE','learningValidation':'NOT_YET_EVALUATED','visualGrammar':'principle decision plates; instructional composition; no authored circuit is required','scl':'NOT_APPLICABLE: no circuit topology or traversal is represented','nanoBanana':'NOT_USED: optional restrained pilot enhancement','canonicalLayer':'plates/*.svg','scenes':SCENES})
    for i,scene in enumerate(SCENES):
        svg=OUT/'plates'/f'{scene["id"]}.svg'; svg.write_text(make_svg(scene,i),encoding='utf-8')
        cairosvg.svg2png(url=str(svg),write_to=str(svg.with_suffix('.png')))
    # A typographic thumbnail is derived directly from the canonical opening plate.
    thumb=dict(SCENES[0],label='SIDEFX · EPISODE 02',body='Completed ≠ helpful')
    svg=OUT/'thumbnail.svg';svg.write_text(make_svg(thumb,0),encoding='utf-8')
    cairosvg.svg2png(url=str(svg),write_to=str(OUT/'thumbnail.png'),output_width=1280,output_height=720)
    Image.open(OUT/'thumbnail.png').convert('RGB').save(OUT/'thumbnail.jpg',quality=95,optimize=True)
    (OUT/'script.md').write_text('# '+TITLE+'\n\nFictional worked example A-W1. Synthetic narration. No evidence of learner outcomes is claimed.\n\n'+'\n\n'.join('## '+s['title']+'\n\n'+s['narration']+ ('\n\n[Reflection hold: '+str(s['pause'])+' seconds. Viewer invited to pause.]' if s.get('pause') else '') for s in SCENES)+'\n',encoding='utf-8')
    if not args.execute:
        print('PLATES AND SCRIPT READY. --execute generates narration and assembles film.', flush=True);return
    tts.OUT=OUT/'audio'
    ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()
    timeline=[];cues=[];start=0
    for i,scene in enumerate(SCENES):
        r=tts.speech(scene['narration'],scene['id'])
        length=math.ceil((r['durationSeconds']+scene.get('pause',.8))*24)/24
        chapter={'id':scene['id'],'title':scene['title'],'seconds':round(start,3),'duration':round(length,3),'speechDuration':r['durationSeconds'],'timestamp':f'{int(start)//60:02}:{int(start)%60:02}'}
        timeline.append(chapter)
        # Approximate phrase timing is refined to measured WAV chapter boundaries.
        phrases=[]
        for sentence in re.split(r'(?<=[.!?])\s+',scene['narration']):
            words=sentence.split()
            while words:phrases.append(' '.join(words[:12]));words=words[12:]
        total=sum(len(s.split()) for s in phrases);t=start
        for phrase in phrases:
            span=r['durationSeconds']*len(phrase.split())/total
            cues.append((t,t+span,phrase));t+=span
        if scene.get('pause',0)>=8:cues.append((start+r['durationSeconds'],start+length,'[Pause and write your answer. Take the time you need.]'))
        clip=OUT/'clips'/f'{scene["id"]}.mp4'
        cmd=[ffmpeg,'-hide_banner','-loglevel','error','-y','-loop','1','-framerate','24','-i',str(OUT/'plates'/f'{scene["id"]}.png'),'-i',str(OUT/'audio'/f'{scene["id"]}.wav'),'-vf','fade=t=in:st=0:d=0.2','-af','apad','-t',str(length),'-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart',str(clip)]
        subprocess.run(cmd,check=True)
        start+=length
        print(f'CHAPTER {i+1}/{len(SCENES)} READY ({length:.1f}s)',flush=True)
    listing=OUT/'clips/concat.txt';listing.write_text(''.join(f"file '{s['id']}.mp4'\n" for s in SCENES),encoding='utf-8')
    film=OUT/'episode-02.mp4'
    subprocess.run([ffmpeg,'-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(listing),'-c','copy','-movflags','+faststart',str(film)],check=True)
    subprocess.run([ffmpeg,'-hide_banner','-loglevel','error','-xerror','-i',str(film),'-f','null','-'],check=True)
    vtt='WEBVTT\n\n'+'\n\n'.join(f'{timecode(a)} --> {timecode(b)}\n{text}' for a,b,text in cues)+'\n'
    srt='\n\n'.join(f'{i+1}\n{timecode(a,True)} --> {timecode(b,True)}\n{text}' for i,(a,b,text) in enumerate(cues))+'\n'
    (OUT/'captions.vtt').write_text(vtt,encoding='utf-8');(OUT/'captions.srt').write_text(srt,encoding='utf-8')
    transcript=TITLE+'\n\nFictional worked example. Synthetic narration.\n\n'+'\n\n'.join(c['timestamp']+' '+s['title']+'\n'+s['narration'] for c,s in zip(timeline,SCENES))+'\n'
    (OUT/'transcript.txt').write_text(transcript,encoding='utf-8')
    description='The booking is confirmed. Two people still cannot attend. Has the task succeeded?\n\nIn this SideFX Foundations lesson, make your own judgment, hear an objection, and separate a completed action from the result people need. No technical background is required.\n\nWatch with the decision plate and transcript:\n'+URL+'\n\nCHAPTERS\n'+'\n'.join(c['timestamp']+' '+c['title'] for c in timeline)+'\n\nFictional teaching scenario (A-W1). Synthetic narration. Deterministic visual plates. This lesson illustrates a way to reason about consequences; it does not establish learning outcomes or demonstrate AI system execution.\n\nWhat specific fact would change your judgment? Share your reasoning without naming private individuals.\n\nNext: What do we actually know?\n\n#SideFX #DecisionMaking #AI\n'
    (OUT/'title.txt').write_text(TITLE+'\n',encoding='utf-8');(OUT/'description.txt').write_text(description,encoding='utf-8')
    (OUT/'pinned-comment.txt').write_text('Before the challenge, what did you think should happen next? What specific new fact would change your judgment? Keep names and private details out of your example.\n\nDecision plate and transcript: '+URL+'\n',encoding='utf-8')
    dump(OUT/'timeline.json',timeline)
    releasefile=OUT/'release.json';previous=json.loads(releasefile.read_text(encoding='utf-8')) if releasefile.exists() else {}
    release={'title':TITLE,'status':previous.get('status','PREPARED'),'videoUrl':previous.get('videoUrl'),'landingPage':URL,'durationSeconds':round(start,3),'chapters':timeline,'filmSha256':digest(film),'captionTiming':'Approximate phrase timing within measured chapter audio boundaries; not word-level forced alignment.','disclosure':'Fictional scenario; synthetic narration; deterministic SVG plates.','learningValidation':'NOT_YET_EVALUATED'}
    dump(releasefile,release)
    SITE.mkdir(parents=True,exist_ok=True)
    for name in ['episode-02.mp4','thumbnail.jpg','captions.vtt','transcript.txt']:
        shutil.copy2(OUT/name,SITE/name)
    shutil.copy2(OUT/'plates/06.svg',SITE/'decision-plate.svg')
    dump(ROOT/'release-site/app/episode-two.json',public_data(release))
    dump(OUT/'release-checks.json',{'filmDecode':'PASS: FFmpeg full stream decode with -xerror','filmSha256':digest(film),'canonicalSvgPlates':len(SCENES),'privateAssessmentIncluded':False,'sourceSha256':digest(ROOT/'docs/wisdom-pilot/teaching/lesson-a.md'),'learningValidation':'NOT_YET_EVALUATED'})
    print('FILM READY',round(start,2),'seconds',film.stat().st_size,'bytes',flush=True)

if __name__=='__main__':main()
