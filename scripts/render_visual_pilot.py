"""Render phase-by-phase narrated walkthrough and a 60-second vertical cut."""
import json, subprocess, textwrap, wave
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
import imageio_ffmpeg

ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'samples/visual-pilot'
FFMPEG=imageio_ffmpeg.get_ffmpeg_exe()
jobs=json.loads((OUT/'pilot-assets.json').read_text())
if len(jobs)!=8: raise SystemExit('All eight pilot images are required')
font_path=Path('C:/Windows/Fonts/segoeui.ttf')
def font(size): return ImageFont.truetype(str(font_path),size) if font_path.exists() else ImageFont.load_default(size=size)
def paragraph(draw,text,xy,width,size,fill):
    f=font(size); lines=[]; line=''
    for word in text.split():
        trial=(line+' '+word).strip()
        if draw.textlength(trial,font=f)>width and line: lines.append(line);line=word
        else: line=trial
    lines.append(line)
    draw.multiline_text(xy,'\n'.join(lines),font=f,fill=fill,spacing=10)

frames=OUT/'video-frames';frames.mkdir(exist_ok=True)
clips=[];vertical=[];durations=[]
for j in jobs:
    index=j['index'];audio=OUT/'audio'/f'{index:02}.wav'
    with wave.open(str(audio),'rb') as w: duration=max(22.5,w.getnframes()/w.getframerate()+1)
    durations.append(duration)
    for phase in range(3):
        im=Image.open(OUT/f'frame-{index:02}-{phase}.jpg').convert('RGB')
        canvas=Image.new('RGB',(1280,720),'#f3f0e8');draw=ImageDraw.Draw(canvas)
        panel=ImageOps.contain(im,(430,664));canvas.paste(panel,(24+(430-panel.width)//2,28+(664-panel.height)//2))
        draw.text((500,42),f'SIDEFX / GOVERNED ROUTING     {index+1:02} / 08',font=font(15),fill='#635e91')
        paragraph(draw,j['title'],(500,104),730,38,'#272b3b')
        draw.text((500,240),['INPUT','EVENT','OUTCOME'][phase],font=font(18),fill='#514d98')
        phase_meaning=j['spec'][['inputExperience','eventExperience','outcomeExperience'][phase]]
        text=phase_meaning.get('state') or phase_meaning.get('action') or ' '.join(phase_meaning['observableState'])
        paragraph(draw,text,(500,292),718,24,'#303845')
        for n in range(3): draw.rounded_rectangle((500+n*80,617,560+n*80,623),radius=3,fill='#514d98' if n==phase else '#d7d2c6')
        draw.text((500,660),'Editorial illustration / authorization is not execution',font=font(16),fill='#77796f')
        canvas.save(frames/f'wide-{index:02}-{phase}.png')
        phone=Image.new('RGB',(720,1280),'#f3f0e8');d=ImageDraw.Draw(phone)
        d.text((40,35),'SIDEFX / ARCHITECTURE EXPLAINED',font=font(18),fill='#635e91')
        paragraph(d,j['title'],(40,88),640,36,'#272b3b')
        pic=ImageOps.contain(im,(620,840));phone.paste(pic,((720-pic.width)//2,205+(840-pic.height)//2))
        d.text((40,1080),f'{index+1:02}/08  ·  '+['INPUT','EVENT','OUTCOME'][phase],font=font(25),fill='#514d98')
        d.text((40,1150),'Permission and evidence. No execution.',font=font(22),fill='#303845')
        phone.save(frames/f'vertical-{index:02}-{phase}.png')
        vertical += [f"file 'video-frames/vertical-{index:02}-{phase}.png'",'duration 2.5']
    chapter=OUT/f'chapter-{index:02}.mp4'
    # Three continuous phase views, with short dissolves between them.
    section=(duration+1.0)/3
    cmd=[FFMPEG,'-hide_banner','-loglevel','error','-y']
    for p in range(3): cmd+=['-loop','1','-t',str(section),'-i',str(frames/f'wide-{index:02}-{p}.png')]
    cmd+=['-i',str(audio),'-filter_complex',f'[0:v][1:v]xfade=transition=fade:duration=0.5:offset={section-0.5}[v1];[v1][2:v]xfade=transition=fade:duration=0.5:offset={2*section-1}[v];[3:a]apad[a]',
          '-map','[v]','-map','[a]','-t',str(duration),'-r','24','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-movflags','+faststart',str(chapter)]
    subprocess.run(cmd,check=True)
    clips.append(f"file '{chapter.name}'")
    print('RENDERED CHAPTER',index,round(duration,1),flush=True)
(OUT/'chapters.concat.txt').write_text('\n'.join(clips))
subprocess.run([FFMPEG,'-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(OUT/'chapters.concat.txt'),'-c','copy','-movflags','+faststart',str(OUT/'capability-walkthrough.mp4')],check=True)
vertical.append("file 'video-frames/vertical-07-2.png'")
(OUT/'short.concat.txt').write_text('\n'.join(vertical))
subprocess.run([FFMPEG,'-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(OUT/'short.concat.txt'),'-t','60','-vf','fps=24','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',str(OUT/'capability-short.mp4')],check=True)
(OUT/'video-receipt.json').write_text(json.dumps({'chapters':8,'phaseFrames':24,'walkthroughSeconds':sum(durations),'shortSeconds':60,'narration':'Gemini synthetic voice Kore','animation':'Phase dissolves; not generative motion or runtime execution','shortAudio':'silent'},indent=2))
print('VIDEO EXPORTS COMPLETE',round(sum(durations),1))
