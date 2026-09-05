"""Realize a chapter-timed target-experience lesson with traceable synthetic narration."""
import argparse
import hashlib
import json
import math
import subprocess
from functools import lru_cache
from pathlib import Path

import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'samples/content-catalog/interlock-agent-operation'
FF=imageio_ffmpeg.get_ffmpeg_exe()
W,H,FPS=1280,720,24
WHITE,MUTED,CURRENT,TARGET,GAP='#f4f1e9','#b0c0cd','#73ded5','#b6a4ff','#efbe77'

def read(path):return json.loads(path.read_bytes())
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def write(path,data):path.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
@lru_cache(None)
def font(n,b=False):return ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf' if b else 'C:/Windows/Fonts/segoeui.ttf',n)
def txt(d,xy,s,n=22,color=WHITE,b=False):d.text(xy,s,font=font(n,b),fill=color,spacing=8)
def lines(d,s,width,n,b=False):
    words=s.split(); rows=[]; row=''
    for word in words:
        new=(row+' '+word).strip()
        if d.textlength(new,font=font(n,b))>width and row:rows.append(row);row=word
        else:row=new
    return rows+[row]
def wrap(d,xy,s,width=730,n=42,color=WHITE,b=True):
    rows=lines(d,s,width,n,b)
    for i,row in enumerate(rows):txt(d,(xy[0],xy[1]+i*(n+10)),row,n,color,b)
    return len(rows)*(n+10)
def panel(d,box,color=CURRENT):d.rounded_rectangle(box,12,fill=(6,19,30,232),outline=color,width=2)
def link(d,a,b,t,color,outlined=False):
    length=math.dist(a,b)
    if outlined:
        for i in range(0,int(length),14):
            pa=i/length;pb=min(i+7,length)/length
            d.line((a[0]+(b[0]-a[0])*pa,a[1]+(b[1]-a[1])*pa,a[0]+(b[0]-a[0])*pb,a[1]+(b[1]-a[1])*pb),fill=color,width=3)
    else:d.line((*a,*b),fill=color,width=3)
    p=(t*.27)%1;x=a[0]+(b[0]-a[0])*p;y=a[1]+(b[1]-a[1])*p
    d.ellipse((x-5,y-5,x+5,y+5),fill=color)

def prepare_audio():
    import run_narration_continuity_demo as speech
    speech.OUT=OUT
    d=read(ROOT/'declarations/episode-01-direction.json'); offset=0; chapters=[]
    for i,c in enumerate(d['chapters']):
        r=speech.speech(c['narration'],f'chapter-{i+1:02}')
        duration=round(r['durationSeconds']+1.0,3)
        chapters.append({**c,'start':round(offset,3),'duration':duration,'audioFile':r['audioFile'],'audioDigest':r['audioDigest']})
        offset+=duration
        print('NARRATED',i+1,round(r['durationSeconds'],2),flush=True)
    write(OUT/'timeline.json',{'durationSeconds':round(offset,3),'chapters':chapters,'directionDigest':digest(ROOT/'declarations/episode-01-direction.json')})

def pictures():
    images=[]; refs=[]
    selection=read(OUT/'shot-selection.json')['shots']
    for job,a in zip(read(OUT/'generation-manifest.json'),selection,strict=True):
        p=ROOT/a['path']
        if a['jobId']!=job['id'] or digest(p)!=a['sha256']:raise ValueError('SHOT_DIGEST_MISMATCH')
        images.append(ImageOps.fit(Image.open(p).convert('RGB'),(W,H),method=Image.Resampling.LANCZOS))
        refs.append({'jobId':job['id'],'path':p.relative_to(ROOT).as_posix(),'sha256':a['sha256']})
    return images,refs

def frame(c,local,images):
    image=images[c['shot']].convert('RGBA'); overlay=Image.new('RGBA',(W,H));d=ImageDraw.Draw(overlay)
    for x in range(W):d.line((x,0,x,H),fill=(3,10,19,round(226*(1-x/W)**.9)))
    color={'CURRENT':CURRENT,'TARGET':TARGET,'GAP':GAP}[c['reality']]
    txt(d,(42,25),'THE FUTURE OF AGENTIC ENGINEERING',15,CURRENT,True)
    txt(d,(43,52),'S01 / E01    '+c['section'].upper(),13,MUTED)
    labels={'CURRENT':'CURRENT / SOURCE EVIDENCE','TARGET':'TARGET EXPERIENCE','GAP':'GAP / FUTURE CLOSURE'}
    panel(d,(875,25,1238,70),color);txt(d,(893,36),labels[c['reality']],14,color,True)
    wrap(d,(42,116),c['title'],width=600,n=42)
    v=c['visual']; y=306
    if v in ('pending','scenario','human'):
        panel(d,(42,y,772,y+225),color)
        txt(d,(67,y+20),'ASSIGNMENT',13,MUTED,True);txt(d,(67,y+47),'Inspect candidate capability',26,WHITE,True)
        txt(d,(67,y+102),'AGENT REQUEST',13,MUTED,True);txt(d,(67,y+131),'Publish candidate',29,GAP,True)
        txt(d,(67,y+182),'QUEUED  /  no effect has crossed',18,GAP)
        # A queued request approaches the boundary and stays on its near side.
        yy=566;x=65+min(local/5,1)*395
        d.line((65,yy,610,yy),fill=TARGET,width=2)
        d.line((542,yy-16,542,yy+16),fill=GAP,width=4)
        d.rounded_rectangle((x,yy-7,x+46,yy+7),4,fill=TARGET)
        txt(d,(566,yy-10),'EFFECT',13,MUTED)
        if v=='human':txt(d,(43,575),'She needs progress within the authority she gave.',20,WHITE)
    elif v=='branch':
        panel(d,(42,288,772,585),CURRENT)
        txt(d,(65,310),'payload.operation = ADJUDICATE',22,WHITE,True)
        txt(d,(65,359),'toolId == dangerous-tool',25,WHITE)
        link(d,(259,411),(131,455),local,CURRENT)
        link(d,(355,411),(555,455),local,CURRENT)
        txt(d,(179,429),'TRUE',13,CURRENT,True);txt(d,(432,429),'FALSE',13,CURRENT,True)
        txt(d,(65,470),'OPERATOR_REQUIRED',20,CURRENT,True);txt(d,(519,470),'ALLOW',23,CURRENT,True)
        txt(d,(65,532),'Stored expression / no live interception observed',17,MUTED)
        txt(d,(65,560),'SOURCE  /mechanicBindings/2  ·  linked in the evidence story',12,CURRENT)
    elif v=='principle':
        for i,label in enumerate(['CAPABILITY','AUTHORITY','MECHANIC','BOUNDARY']):
            active=local>=2+i*2.0;ink=TARGET if active else MUTED
            x=42+i*188;panel(d,(x,317,x+168,392),ink);txt(d,(x+10,341),label,17,ink,True)
            if i<3 and active:link(d,(x+168,354),(x+188,354),local,TARGET,True)
        if local>=9:txt(d,(42,457),'PERMIT  →  exact admitted execution',26,TARGET,True)
        if local>=12:txt(d,(42,507),'OPERATOR_REQUIRED  →  separate human decision',20,WHITE)
        if local>=15:txt(d,(42,550),'DENY / RESOLVE  →  reason + next legal action',20,WHITE)
    elif v=='contrast':
        panel(d,(42,302,340,507),CURRENT);txt(d,(66,328),'WHAT EXISTS',16,CURRENT,True);txt(d,(66,373),'Decision logic',26,WHITE,True);txt(d,(66,418),'ALLOW / operator',20,MUTED)
        panel(d,(470,302,777,507),TARGET);txt(d,(494,328),'WHAT SHOULD EXIST',16,TARGET,True);txt(d,(494,373),'Before-effect hook',23,WHITE,True);txt(d,(494,418),'Bound dispatch',20,MUTED)
        d.line((342,405,386,405),fill=GAP,width=4);d.line((432,405,468,405),fill=GAP,width=4)
        txt(d,(389,391),'?',28,GAP,True);txt(d,(42,554),'MISSING: live interception + effect testimony',23,GAP,True)
        if local>12:
            link(d,(342,405),(468,405),local,TARGET,True)
            txt(d,(350,523),'TARGET',12,TARGET,True)
    elif v=='cases':
        states=[('Publish','RESOLVE','Inspection is the next legal action'),('Inspect','PERMIT','Illustrative report is returned'),('Uncovered path','HOLD','Establish exact coverage first')]
        for i,(action,outcome,reason) in enumerate(states):
            if local<i*5:continue
            yy=285+i*103;panel(d,(42,yy,776,yy+87),TARGET if i==1 else GAP)
            txt(d,(61,yy+12),action,23,WHITE,True);txt(d,(467,yy+12),outcome,22,TARGET if i==1 else GAP,True);txt(d,(61,yy+51),reason,17,MUTED)
    elif v=='evidence':
        for i,label in enumerate(['Same session / same boundary','Unmanaged probe denied before effect','Declared inspection permitted + observed','Request → decision → actual effect receipt']):
            yy=285+i*74
            d.rounded_rectangle((42,yy,77,yy+35),8,outline=GAP,width=2)
            txt(d,(91,yy+2),label,23,WHITE)
            if local>=4+i*3:
                d.line((49,yy+18,58,yy+25,70,yy+9),fill=TARGET,width=3)
        txt(d,(42,599),'Animated target closure / live proof still required',18,GAP)
    elif v=='takeaway':
        panel(d,(42,298,772,526),TARGET);txt(d,(65,321),'TARGET OUTCOME',14,TARGET,True)
        txt(d,(65,365),'Inspection report ready.',31,WHITE,True);txt(d,(65,416),'Publication still pending.',29,GAP,True)
        txt(d,(65,474),'Useful work. Human authority intact.',22,TARGET)
    elif v=='next':
        txt(d,(42,305),'NEXT / EPISODE 02',17,TARGET,True)
        wrap(d,(42,353),'Reveal and Refine Capability Meaning',width=705,n=42)
        txt(d,(42,505),'Make it visible enough to challenge.',24,WHITE)
    txt(d,(42,653),'SOURCE EVIDENCE  /  TARGET DESIGN  /  ENGINEERING RUNWAY',13,MUTED)
    d.line((42,696,1238,696),fill=(130,170,180,70),width=3)
    d.line((42,696,42+1196*min(1,local/c['duration']),696),fill=color,width=3)
    return Image.alpha_composite(image,overlay).convert('RGB')

def media_render():
    from episode_infographics import EpisodeInfographics, CACHE
    editor=EpisodeInfographics()
    tl=read(OUT/'timeline.json'); chapters=tl['chapters'];images,refs=pictures()
    for c in chapters:
        if digest(OUT/c['audioFile'])!=c['audioDigest']:raise ValueError('STALE_CHAPTER_AUDIO')
    if digest(ROOT/'declarations/episode-01-direction.json')!=tl['directionDigest']:raise ValueError('STALE_EPISODE_DIRECTION')
    frames=math.ceil(tl['durationSeconds']*FPS)
    silent=CACHE/'episode-silent.mp4'; output=CACHE/'episode-01.mp4'
    proc=subprocess.Popen([FF,'-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1920x1080','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p',str(silent)],stdin=subprocess.PIPE)
    ci=0
    for i in range(frames):
        t=i/FPS
        while ci+1<len(chapters) and t>=chapters[ci+1]['start']:ci+=1
        c=chapters[ci];local=t-c['start']
        im=editor.frame(c,local) if c['id'] in editor.edit['chapters'] else frame(c,local,images).resize((1920,1080),Image.Resampling.LANCZOS)
        proc.stdin.write(im.tobytes())
        if i==round((c['start']+1)*FPS):im.save(CACHE/f'qa-chapter-{ci+1:02}.jpg',quality=93)
        if i%(FPS*30)==0:print('RENDERED',round(t),flush=True)
    proc.stdin.close()
    if proc.wait():raise ValueError('ENCODE_FAILED')
    cmd=[FF,'-hide_banner','-loglevel','error','-y','-i',str(silent)]
    filters=[]
    for i,c in enumerate(chapters):
        cmd+=['-i',str(OUT/c['audioFile'])]
        filters.append(f'[{i+1}:a]adelay={round(c["start"]*1000)}:all=1,apad[a{i}]')
    filters.append(''.join(f'[a{i}]' for i in range(len(chapters)))+f'amix=inputs={len(chapters)}:duration=longest:normalize=0,alimiter=limit=0.95[mix]')
    cmd+=['-filter_complex',';'.join(filters),'-map','0:v','-map','[mix]','-t',str(tl['durationSeconds']),'-c:v','copy','-c:a','aac','-b:a','160k','-movflags','+faststart',str(output)]
    subprocess.run(cmd,check=True)
    # Keep the previous episode usable until the new picture and sound fully decode.
    subprocess.run([FF,'-hide_banner','-loglevel','error','-xerror','-i',str(output),'-f','null','-'],check=True)
    output.replace(OUT/'episode-01.mp4');silent.replace(OUT/'episode-silent.mp4')
    for preview in CACHE.glob('qa-chapter-*.jpg'):preview.replace(OUT/preview.name)
    receipt=editor.receipt()
    receipt.update({'filmDigest':digest(OUT/'episode-01.mp4'),'format':'1920x1080 H264 AAC','fps':FPS,'frameCount':frames,'fullDecodeVerified':True,'audio':'Existing chapter WAVs, unchanged scripts and timeline; no new generation.'})
    write(OUT/'infographic-edit.receipt.json',receipt)
    write(OUT/'film.receipt.json',{'kind':'TARGET_EXPERIENCE_TRAINING_FILM','durationSeconds':tl['durationSeconds'],'format':'1920x1080 H264 AAC','fps':FPS,'filmDigest':digest(OUT/'episode-01.mp4'),'timelineDigest':digest(OUT/'timeline.json'),'shots':refs,'motion':'Generated human stills and chapter cuts, with native 1080p source-bound circuit cutaways in Open the Event and Evidence. Shared silver-ball flow, branch choice and arrival-aware ALL join. Human movement is implied.','infographicEdit':{'path':(OUT/'infographic-edit.receipt.json').relative_to(ROOT).as_posix(),'sha256':digest(OUT/'infographic-edit.receipt.json')},'humanChapterRaster':'1280x720 upscaled to 1920x1080','liveEnforcementClaimed':False})
    print('EPISODE COMPLETE',tl['durationSeconds'],flush=True)

def thumbnail(images=None):
    if images is None:images,_=pictures()
    im=images[0].convert('RGBA');overlay=Image.new('RGBA',(W,H));d=ImageDraw.Draw(overlay)
    for x in range(W):d.line((x,0,x,H),fill=(3,10,19,round(236*(1-x/W)**.8)))
    txt(d,(48,38),'SIDEFX  /  EPISODE 01',23,CURRENT,True)
    txt(d,(47,180),'READY TO ACT.',76,WHITE,True)
    txt(d,(47,270),'WHO',99,WHITE,True)
    txt(d,(47,380),'DECIDES?',99,TARGET,True)
    txt(d,(49,553),'The future of agentic engineering',25,WHITE)
    panel(d,(48,622,368,670),TARGET);txt(d,(68,635),'TARGET EXPERIENCE',17,TARGET,True)
    Image.alpha_composite(im,overlay).convert('RGB').save(OUT/'thumbnail.jpg',quality=95)

def short_audio():
    import run_narration_continuity_demo as speech
    speech.OUT=OUT
    r=speech.speech(read(ROOT/'declarations/episode-01-short.json')['narration'],'short-voiceover')
    print('SHORT NARRATED',round(r['durationSeconds'],2),flush=True)

def short_render():
    direction=read(ROOT/'declarations/episode-01-short.json');r=read(OUT/'short-voiceover.receipt.json')
    if r['script']!=direction['narration'] or digest(OUT/r['audioFile'])!=r['audioDigest']:raise ValueError('STALE_SHORT_AUDIO')
    duration=r['durationSeconds']+0.7;images,refs=pictures(); beats=direction['beats'];sw,sh=720,1280
    silent=OUT/'short-silent.mp4'
    proc=subprocess.Popen([FF,'-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{sw}x{sh}','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p',str(silent)],stdin=subprocess.PIPE)
    for i in range(math.ceil(duration*FPS)):
        t=i/FPS;b=next(b for b in reversed(beats) if t/duration>=b['at']);c={'CURRENT':CURRENT,'TARGET':TARGET,'GAP':GAP}[b['reality']]
        im=Image.new('RGB',(sw,sh),'#080f19');d=ImageDraw.Draw(im)
        # Reframe the selected wide shot around the performer, retain a separate authored text field.
        photo=ImageOps.fit(images[b['shot']].crop((580,0,1280,720)),(720,525),method=Image.Resampling.LANCZOS)
        im.paste(photo,(0,190));d=ImageDraw.Draw(im)
        txt(d,(36,35),'THE FUTURE OF',20,CURRENT,True);txt(d,(36,67),'AGENTIC ENGINEERING',26,WHITE,True)
        txt(d,(36,132),'S01 / E01',17,MUTED)
        d.rectangle((0,682,sw,sh),fill='#080f19')
        txt(d,(36,719),b['reality']+' / '+b['label'],16,c,True)
        wrap(d,(36,770),b['title'],width=645,n=45)
        wrap(d,(36,960),b['detail'],width=640,n=24,b=False,color=MUTED)
        txt(d,(36,1165),'When the agent is ready to act,',21,WHITE)
        txt(d,(36,1196),'who decides?',25,c,True)
        d.line((36,1252,684,1252),fill='#2b394a',width=4);d.line((36,1252,36+648*t/duration,1252),fill=c,width=4)
        proc.stdin.write(im.tobytes())
        if i==round((b['at']*duration+0.5)*FPS):im.save(OUT/f'qa-short-{beats.index(b)+1:02}.jpg',quality=93)
    proc.stdin.close()
    if proc.wait():raise ValueError('SHORT_ENCODE_FAILED')
    subprocess.run([FF,'-hide_banner','-loglevel','error','-y','-i',str(silent),'-i',str(OUT/r['audioFile']),'-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','160k','-t',str(duration),'-movflags','+faststart',str(OUT/'short.mp4')],check=True)
    write(OUT/'short.receipt.json',{'kind':'TARGET_EXPERIENCE_SHORT','durationSeconds':duration,'directionDigest':digest(ROOT/'declarations/episode-01-short.json'),'audioDigest':r['audioDigest'],'filmDigest':digest(OUT/'short.mp4'),'format':'720x1280 H264 AAC','shots':refs,'liveEnforcementClaimed':False})
    print('SHORT COMPLETE',duration,flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--audio',action='store_true');p.add_argument('--render',action='store_true');p.add_argument('--short-audio',action='store_true');p.add_argument('--short',action='store_true');p.add_argument('--thumbnail',action='store_true');args=p.parse_args()
    if args.audio:prepare_audio()
    if args.render:media_render()
    if args.short_audio:short_audio()
    if args.short:short_render()
    if args.thumbnail:thumbnail()
