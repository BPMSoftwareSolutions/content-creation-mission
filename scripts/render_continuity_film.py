"""Render a 64-second editorial animatic with moving entities and live-demo audio."""
import array,hashlib,json,math,subprocess,wave
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps
import imageio_ffmpeg
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'samples/narration-continuity'
W,H,FPS,DURATION=1280,720,24,64
FF=imageio_ffmpeg.get_ffmpeg_exe();WHITE='#f2f1ec';MUTED='#a8b9c8';CYAN='#6edfdc';AMBER='#edbc77';RED='#ed8776'
FONT='C:/Windows/Fonts/segoeui.ttf';BOLD='C:/Windows/Fonts/segoeuib.ttf'
def font(n,b=False):return ImageFont.truetype(BOLD if b else FONT,n)
FONTS={(n,b):font(n,b) for n in [12,14,16,18,20,24,28,32,40,48,58,68] for b in (False,True)}
def text(d,xy,s,n=20,fill=WHITE,b=False):d.text(xy,s,font=FONTS[n,b],fill=fill,spacing=4)
def clamp(v):return max(0,min(1,v))
def ease(v):v=clamp(v);return v*v*(3-2*v)
def panel(d,box,fill=(9,23,33,222),outline=(130,180,190,65),r=12):d.rounded_rectangle(box,radius=r,fill=fill,outline=outline,width=1)
def read(p):return json.loads(p.read_bytes())
jobs=read(OUT/'generation-manifest.json');receipts={}
for f in (ROOT/'outputs/generated').glob('*.json'):
    r=read(f)
    if r.get('status')=='GENERATED':receipts[r['jobId']]=r
pictures=[];media=[]
for j in jobs:
    r=receipts.get(j['id'])
    if not r:raise ValueError('SHOT_NOT_GENERATED:'+j['shot']['id'])
    a=r['images'][0];src=ROOT/'outputs/generated'/a['path']
    if hashlib.sha256(src.read_bytes()).hexdigest()!=a['sha256']:raise ValueError('IMAGE_DIGEST_MISMATCH')
    pictures.append(ImageOps.fit(Image.open(src).convert('RGB'),(W,H),method=Image.Resampling.LANCZOS))
    media.append({'shot':j['shot']['id'],'jobId':j['id'],'imageDigest':a['sha256'],'receipt':r})
demo=read(OUT/'demo.receipt.json')
with wave.open(str(OUT/'finished-narration.wav'),'rb') as wav:
    samples=array.array('h',wav.readframes(wav.getnframes()));rate=wav.getframerate()
peaks=[]
for i in range(90):
    chunk=samples[len(samples)*i//90:len(samples)*(i+1)//90]
    peaks.append(max(.04,max(abs(x) for x in chunk)/32768))
gradient=Image.new('RGBA',(W,H));gd=ImageDraw.Draw(gradient)
for x in range(W):gd.line((x,0,x,H),fill=(3,12,20,int(210*(1-x/W)**1.75)))
bounds=[0,7,13,30,43,53,64]
def waveform(d,x,y,width,height,t,progress=1,color=CYAN):
    for i,amp in enumerate(peaks):
        if i/len(peaks)>progress:continue
        xx=x+i*width/len(peaks);a=amp*height*(.8+.2*math.sin(t*3+i*.5))
        d.line((xx,y-a,xx,y+a),fill=color,width=3)
def route(d,a,b,t,color=CYAN,active=False):
    mid=(a[0]+b[0])//2
    pts=[a,(mid,a[1]),(mid,b[1]),b];d.line(pts,fill=color,width=2)
    if active:
        length=sum(math.dist(pts[i],pts[i+1]) for i in range(3))
        for offset in [0,.25,.5,.75]:
            remaining=((t*.3+offset)%1)*length
            for i in range(3):
                seg=math.dist(pts[i],pts[i+1])
                if remaining<=seg:
                    p=remaining/seg if seg else 0;xx=pts[i][0]+p*(pts[i+1][0]-pts[i][0]);yy=pts[i][1]+p*(pts[i+1][1]-pts[i][1]);d.ellipse((xx-4,yy-4,xx+4,yy+4),fill=WHITE);break
                remaining-=seg
def frame(t):
    scene=next(i for i in range(6) if bounds[i]<=t<bounds[i+1]);local=(t-bounds[scene])/(bounds[scene+1]-bounds[scene])
    zoom=1+.025*ease(local);ww,hh=int(W/zoom),int(H/zoom);xx=int((W-ww)*.75);yy=(H-hh)//2
    im=pictures[scene].crop((xx,yy,xx+ww,yy+hh)).resize((W,H),Image.Resampling.BICUBIC).convert('RGBA')
    im=Image.alpha_composite(im,gradient);layer=Image.new('RGBA',(W,H));d=ImageDraw.Draw(layer)
    text(d,(52,28),'S I D E F X',16,b=True);text(d,(900,30),'DRAMATIZED LOCAL DEMO',12,MUTED)
    if scene==0:
        text(d,(52,115),'The cut is ready.',40);text(d,(52,168),'The voice\nis gone.',68,b=True)
        panel(d,(52,390,600,554));text(d,(76,409),'NARRATION TRACK',14,MUTED)
        for x in range(80,570,16):d.line((x,475,x+6,475),fill=RED,width=2)
        cursor=90+(t%3)/3*430;d.line((cursor,443,cursor,508),fill=AMBER,width=2)
        text(d,(76,519),'Primary voice service unavailable',18,RED)
    elif scene==1:
        text(d,(52,115),'One producer.',48,b=True);text(d,(52,176),'Seven waiting jobs.',40)
        text(d,(52,257),'The script is still hers.\nThe work is still waiting.',24,MUTED)
        for i in range(7):
            x=55+i*67;y=407+int(5*math.sin(t+i*.2));panel(d,(x,y,x+52,y+81),fill=(23,47,64,220))
            for k in range(3):d.line((x+10,y+20+k*11,x+39,y+20+k*11),fill='#7591a5',width=2)
        text(d,(55,518),'No narration to bring into the cut.',20,AMBER)
    elif scene==2:
        text(d,(52,112),'Keep the request.',40,b=True);text(d,(52,161),'Change the route.',40,b=True)
        p=local;panel(d,(52,263,220,340));text(d,(70,277),'HER SCRIPT',16,b=True);text(d,(70,306),demo['requestDigestBefore'][:12],12,MUTED)
        hub=(278,397);d.ellipse((246,365,310,429),fill='#123c4a',outline=CYAN,width=2);text(d,(265,377),'S',28,CYAN,b=True)
        route(d,(220,301),hub,t,CYAN,p>.1)
        for n,(label,y,color,caption) in enumerate([('A',485,RED,'SIMULATED FAILURE'),('B',291,AMBER,'TEXT ONLY'),('C',420,CYAN,'AUDIO'),('D',549,'#728697','STANDBY')]):
            x=70 if label=='A' else 420
            if label!='A':route(d,hub,(x,y),t, color if (label=='C' and p>.5) else '#304553',label=='C' and p>.5)
            panel(d,(x-15,y-28,x+155,y+48),fill=(9,25,37,238),outline=color)
            text(d,(x,y-17),label,24,color,b=True);text(d,(x+32,y-9),caption,12,color)
            if label=='A':
                for z in range(7):d.line((x+z*17,y+24,x+z*17+8,y+24+(6 if z%2 else -6)),fill=RED,width=2)
            elif label=='B' and p>.3:text(d,(x,y+18),'INCOMPATIBLE',12,AMBER)
            elif label=='C' and p>.52:waveform(d,x+3,y+26,125,10,t,min(1,(p-.52)*3))
        if p>.65:text(d,(52,620),'Same script. Compatible audio provider.',20,CYAN)
    elif scene==3:
        text(d,(52,112),'A response is\nonly the beginning.',48,b=True)
        panel(d,(52,275,606,552));waveform(d,79,340,495,42,t,min(1,local*2.5))
        if local>.23:
            panel(d,(80,408,304,490),fill=(22,53,64,245));text(d,(96,420),'narration.wav',20,b=True);text(d,(96,454),f"{demo['asset']['durationSeconds']:.2f}s  /  PCM 24 kHz",14,MUTED)
            route(d,(304,450),(380,450),t,CYAN,True)
        if local>.5:
            panel(d,(378,408,578,490),fill=(22,53,64,245));text(d,(394,420),'HASH VERIFIED',16,CYAN,b=True);text(d,(394,454),demo['asset']['audioDigest'][:18],12,MUTED)
        if local>.7:text(d,(52,588),'Request → provider → playable artifact',20,CYAN)
    elif scene==4:
        text(d,(52,123),'Now she\ncan hear it.',58,b=True)
        panel(d,(52,367,587,524));waveform(d,79,427,475,36,t)
        text(d,(78,484),'The narration is ready for her edit.',20,CYAN)
        text(d,(55,579),'One local job completed. Six remain queued.',16,MUTED)
    else:
        text(d,(52,117),'The provider changed.',32);text(d,(52,169),'The story\nstays hers.',58,b=True)
        panel(d,(52,372,606,552));text(d,(78,391),'LISTEN TO THE ACTUAL DEMO OUTPUT',14,CYAN,b=True)
        waveform(d,80,467,493,35,t)
        pos=80+clamp((t-54)/demo['asset']['durationSeconds'])*493;d.line((pos,425,pos,507),fill=WHITE,width=2)
        text(d,(80,520),'Gemini / synthetic voice',14,MUTED)
    text(d,(52,672),['INPUT  /  INTERRUPTION','INPUT  /  HUMAN STAKES','EVENT  /  PROVIDER CONTINUITY','EVENT  /  ARTIFACT + EVIDENCE','OUTCOME  /  RELIEF','OUTCOME  /  CREATIVE WORK RESUMES'][scene],12,MUTED)
    d.line((52,704,1228,704),fill=(110,150,160,60),width=2);d.line((52,704,52+1176*t/DURATION,704),fill=CYAN,width=2)
    if t<3:text(d,(52,641),'Injected failure · live Gemini narration',12,MUTED)
    im=Image.alpha_composite(im,layer).convert('RGB')
    return im

def render():
    silent=OUT/'film-silent.mp4'
    cmd=[FF,'-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-',
         '-an','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p',str(silent)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    qa=[2,10,24,39,48,59]
    for i in range(DURATION*FPS):
        t=i/FPS;im=frame(t);proc.stdin.write(im.tobytes())
        if t in qa:im.save(OUT/f'qa-{int(t):02}.jpg',quality=94)
        if i%(FPS*10)==0:print('RENDERED',int(t),'seconds',flush=True)
    proc.stdin.close()
    if proc.wait():raise ValueError('VIDEO_RENDER_FAILED')
    # A quiet original synthesized bed, with relief in the final act; no licensed music.
    sample_rate=24000;bed=array.array('h')
    for i in range(sample_rate*DURATION):
        t=i/sample_rate;env=min(1,t/2,(DURATION-t)/2)*(.55 if 13<t<43 else .32)
        v=(math.sin(2*math.pi*110*t)+.4*math.sin(2*math.pi*164.81*t)+.2*math.sin(2*math.pi*220*t))*env*210
        bed.append(int(v))
    with wave.open(str(OUT/'original-bed.wav'),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(sample_rate);w.writeframes(bed.tobytes())
    subprocess.run([FF,'-hide_banner','-loglevel','error','-y','-i',str(silent),'-i',str(OUT/'film-voiceover.wav'),'-i',str(OUT/'finished-narration.wav'),'-i',str(OUT/'original-bed.wav'),
        '-filter_complex','[1:a]apad[v];[2:a]adelay=54000|54000,apad[n];[3:a]volume=0.7[b];[v][n][b]amix=inputs=3:duration=longest:normalize=0,alimiter=limit=0.95[a]',
        '-map','0:v','-map','[a]','-t',str(DURATION),'-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart',str(OUT/'the-story-stays-hers.mp4')],check=True)
    frame(2).save(OUT/'thumbnail-a.jpg',quality=95)
    thumb=frame(48);d=ImageDraw.Draw(thumb);thumb.save(OUT/'thumbnail-b.jpg',quality=95)
    write={'format':'1280x720 H264 AAC','durationSeconds':DURATION,'fps':FPS,'shots':media,
      'animation':'AI-generated still keyframes with procedural routing, request flow, waveform, artifact assembly, camera motion and editorial cuts. No generated human motion.',
      'audio':'Actual Gemini demo output at 54s; separate Gemini synthetic documentary narration; original synthesized bed',
      'demoReceipt':'demo.receipt.json','failure':'Explicitly simulated A outage; C speech call was live',
      'audiencePerformance':'UNMEASURED','filmDigest':hashlib.sha256((OUT/'the-story-stays-hers.mp4').read_bytes()).hexdigest()}
    (OUT/'film.receipt.json').write_text(json.dumps(write,indent=2))
    print('FILM COMPLETE',flush=True)
if __name__=='__main__':render()
