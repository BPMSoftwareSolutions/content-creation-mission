"""Shared SVG/film renderer. Every editorial value comes from store records."""
import html,math,json,subprocess
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import cairosvg,imageio_ffmpeg
from production_store import ROOT,write,read,digest,artifact_digest
from production_captions import align,segment,trigger_time,save_captions

FF=imageio_ffmpeg.get_ffmpeg_exe()
def run(args,**kwargs):return subprocess.run([FF,'-hide_banner','-y']+args,check=True,**kwargs)

def text(value,x,y,size,profile,color=None,bold=False,width=1740):
    font=ImageFont.truetype(profile['boldFontFile'] if bold else profile['fontFile'],size)
    if font.getlength(value)>width:raise ValueError(f'Text overflows {width}px at {size}px: {value}')
    return f'<text x="{x}" y="{y}" font-family="{profile["fontFamily"]}" font-size="{size}" font-weight="{700 if bold else 400}" fill="{color or profile["foreground"]}">{html.escape(value)}</text>'

def plate(revision,scene,state,p):
    w,h=p['width'],p['height']
    # Reusable template geometry; narratives, style selection and semantic states are records.
    if p['templateId']!='large-decision-plate-v1':raise ValueError('Unsupported plate template')
    if (w,h)!=(1920,1080):raise ValueError('This template requires a 1920x1080 design canvas')
    s=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
       f'<rect width="{w}" height="{h}" fill="{p["background"]}"/>',
       f'<rect x="90" y="80" width="64" height="8" fill="{p["accent"]}"/>',
       text(revision['brandLine'],178,96,32,p,p['muted']),
       text(scene['status'],90,188,p['statusSize'],p,p['status'],True),
       text(state['title'],90,322,p['titleSize'],p,bold=True)]
    if len(state['lines'])>2:raise ValueError('One plate supports at most two semantic rows')
    for i,line in enumerate(state['lines'] if state.get('kind') not in ('route','time','comparison','report') else []):
        y=406+i*192
        s += [f'<rect x="90" y="{y}" width="1740" height="160" rx="18" fill="{p["panel"]}"/>',
              text(line,126,y+105,p['bodySize'],p,p['foreground'],width=1668)]
    if state.get('kind')=='route':
        for i,label in enumerate(state['routeNodes']):
            x=90+i*610
            s += [f'<rect x="{x}" y="406" width="520" height="180" rx="18" fill="{p["panel"]}" stroke="{p["status"] if i==state["routeStopIndex"] else p["muted"]}" stroke-width="4"/>',
                  text(label,x+30,515,58,p,bold=True,width=465)]
            if i<2:s.append(f'<path d="M {x+520} 496 H {x+598} l -12 -10 m 12 10 l -12 10" fill="none" stroke="{p["muted"]}" stroke-width="4"/>')
        s.append(text(state['routeCaption'],90,732,p['bodySize'],p))
    if state.get('kind')=='strike':
        s.append(f'<path d="M 122 497 L 1120 497" stroke="{p["status"]}" stroke-width="8"/>')
    if state.get('kind')=='time':
        s.append(f'<path d="M 320 526 H 1510 l -20 -15 m 20 15 l -20 15" fill="none" stroke="{p["muted"]}" stroke-width="6"/>')
        for x,label in zip((320,1500),state['eventLabels']):
            s.append(f'<circle cx="{x}" cy="526" r="16" fill="{p["status"]}"/>')
            s.append(text(label,x-210,455,64,p,width=480))
        for x in (145,255):
            s.append(f'<circle cx="{x}" cy="590" r="22" fill="{p["foreground"]}"/><path d="M {x-32} 651 V 627 Q {x} 594 {x+32} 627 V 651 M {x-12} 651 V 683 M {x+12} 651 V 683" fill="none" stroke="{p["foreground"]}" stroke-width="17"/>')
        s.append(text(state['affectedLabel'],360,635,70,p))
        s.append(text(state['comparisonNote'],90,742,64,p,width=1740))
    if state.get('kind')=='comparison':
        for i,column in enumerate(state['columns']):
            x=90+i*900
            s.append(f'<rect x="{x}" y="390" width="840" height="405" rx="18" fill="{p["panel"]}"/>')
            s.append(text(column['title'],x+40,485,76,p,bold=True,width=760))
            for j,line in enumerate(column['lines']):s.append(text(line,x+40,610+j*92,60,p,width=760))
    if state.get('kind')=='report':
        s.append(f'<path d="M 90 370 H 880 L 980 460 V 738 H 90 Z M 880 370 V 460 H 980" fill="{p["panel"]}" stroke="{p["muted"]}" stroke-width="3"/>')
        for i,field in enumerate(state['fields']):
            y=460+i*110
            s.append(text(field['label'],130,y,62,p,width=410))
            s.append(text(field['value'],560,y,62,p,p['status'] if field['attention'] else p['accent'],True,width=370))
        for i,line in enumerate(state['resultLines']):s.append(text(line,1080,500+i*130,68,p,width=760))
    s.append('</svg>');return ''.join(s)

def prepare_photo(source,destination,p):
    im=Image.open(source).convert('RGB');w,h=p['width'],p['height'];scale=max(w/im.width,h/im.height)
    im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS)
    x=(im.width-w)//2;y=(im.height-h)//2;im=im.crop((x,y,x+w,y+h))
    ImageDraw.Draw(im,'RGBA').rectangle((0,0,w,h),fill=(8,19,30,90));im.save(destination)

def prepare_intro(revision,scene,destination,p):
    def wrap(value,size,width=650):
        font=ImageFont.truetype(p['boldFontFile'],size);lines=[];line=''
        for word in value.split():
            test=(line+' '+word).strip()
            if line and font.getlength(test)>width:lines.append(line);line=word
            else:line=test
        if line:lines.append(line)
        return lines
    svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080"><defs><linearGradient id="shade"><stop stop-color="#08131e" stop-opacity=".97"/><stop offset=".67" stop-color="#08131e" stop-opacity=".94"/><stop offset="1" stop-color="#08131e" stop-opacity="0"/></linearGradient></defs><rect width="1140" height="1080" fill="url(#shade)"/>',
         text(revision['brandLine'].split('/')[0].strip(),70,90,36,p,p['accent'],True)]
    for i,line in enumerate(wrap(scene['status'],38)):
        svg.append(text(line,70,175+i*48,38,p,p['status'],True,width=690))
    for i,line in enumerate(wrap(scene['states'][0]['title'],86)):
        svg.append(text(line,70,365+i*105,86,p,bold=True,width=690))
    svg.append('</svg>');cairosvg.svg2png(bytestring=''.join(svg).encode(),write_to=str(destination))

def master(raw,final,config,folder):
    params=f'I={config["integratedLUFS"]}:TP={config["targetTruePeakDBTP"]}:LRA={config["loudnessRangeLU"]}'
    def measure(path):
        log=run(['-i',str(path),'-af','loudnorm='+params+':print_format=json','-vn','-f','null','NUL'],capture_output=True,text=True).stderr
        return json.JSONDecoder().raw_decode(log[log.rfind('{'):])[0]
    values=measure(raw);write(folder/'pre-master-measurement.json',values)
    filt=('loudnorm='+params+':linear=true:measured_I='+values['input_i']+':measured_TP='+values['input_tp']+
          ':measured_LRA='+values['input_lra']+':measured_thresh='+values['input_thresh']+':offset='+values['target_offset'])
    run(['-loglevel','error','-i',str(raw),'-c:v','copy','-af',filt,'-c:a','aac','-b:a',config['audioBitrate'],
         '-ar',str(config['sampleRate']),'-movflags','+faststart',str(final)])
    actual=measure(final);write(folder/'final-audio-measurement.json',actual)
    if float(actual['input_tp'])>config['maximumEncodedTruePeakDBTP']:raise ValueError('Final AAC true peak needs further headroom')
    run(['-loglevel','error','-xerror','-i',str(final),'-f','null','NUL'])
    return actual

def render(store,revision):
    if store.profile(revision)['visual']['templateId']=='section-authored-svg-v1':
        from production_section_render import render_sections
        return render_sections(store,revision)
    from faster_whisper import WhisperModel
    profile=store.profile(revision);p=profile['visual'];c=profile['captions'];fps=p['fps']
    folder=store.resolve(revision['outputDirectory']);plates=folder/'plates';clips=folder/'clips'
    plates.mkdir(parents=True,exist_ok=True);clips.mkdir(exist_ok=True)
    model=WhisperModel(c['model'],device='cpu',compute_type='int8',cpu_threads=8,download_root=str(ROOT/'.tools/whisper'))
    captions=[];timeline=[];reviews=[];start=0;photos=[]
    for scene in revision['scenes']:
        sid=scene['id'];audio=store.resolve(scene['audioRef'])
        receipt=read(audio.with_suffix('.receipt.json'))
        if receipt['script']!=scene['narration'] or receipt['audioDigest']!=artifact_digest(audio):raise ValueError('Stale narration; run speech first')
        words,mapping,speechdur,qa=align(audio,scene['narration'],model,c['minimumSimilarity']);reviews.append(dict(sceneId=scene['sceneId'],**qa))
        duration=math.ceil((speechdur+p['chapterTailSeconds']+scene['pause'])*fps)/fps
        captions.extend((start+a,start+b,t) for a,b,t in segment(words,mapping,speechdur,c))
        states=[]
        for i,state in enumerate(scene['states']):
            svg=plate(revision,scene,state,p);path=plates/f'{sid}-{i}.svg';path.write_text(svg,encoding='utf-8')
            cairosvg.svg2png(bytestring=svg.encode(),write_to=str(path.with_suffix('.png')))
            states.append(dict(index=i,seconds=trigger_time(state['trigger'],words,mapping),svg=path.name,**state))
        inputs=[];filters=[]
        if scene.get('photo'):
            source=store.resolve(scene['photo']);prepare_photo(source,plates/'establishing.png',p)
            photos.append(dict(source=scene['photo'],sha256=artifact_digest(source),use='Brief establishing still; not generated action or outcome.'))
            inputs+=['-loop','1','-framerate',str(fps),'-i',str(plates/'establishing.png')]
            filters.append("[0:v]scale=2016:1134,crop=1920:1080:x='48+20*sin(t/3)':y=27[back]")
            prepare_intro(revision,scene,plates/'intro.png',p)
            inputs+=['-loop','1','-framerate',str(fps),'-i',str(plates/'intro.png')]
            filters.append('[back][1:v]overlay=0:0:shortest=1[vbase]');last='vbase';index=2
        else:
            inputs+=['-f','lavfi','-i',f'color=c={p["background"]}:s={p["width"]}x{p["height"]}:r={fps}'];last='0:v';index=1
        for i,state in enumerate(states):
            inputs+=['-loop','1','-framerate',str(fps),'-i',str(plates/f'{sid}-{i}.png')]
            st=state['seconds'] if i or not scene.get('photo') else p['establishingSeconds']
            filters.append(f'[{index}:v]format=rgba,fade=t=in:st={st:.3f}:d={p["revealSeconds"]}:alpha=1[s{i}]')
            filters.append(f'[{last}][s{i}]overlay=0:0:shortest=1[v{i}]');last=f'v{i}';index+=1
        for i,state in enumerate(states):
            if state.get('kind')=='route':
                inputs+=['-f','lavfi','-i',f'color=c={p["accent"]}:s=24x24:r={fps}']
                stop=states[i+1]['seconds'] if i+1<len(states) else duration
                filters.append(f"[{last}][{index}:v]overlay=x='610+min(max(t-{state['seconds']},0),3)*24':y=484:enable='between(t,{state['seconds']},{stop})'[trace{i}]")
                last=f'trace{i}';index+=1
        inputs+=['-i',str(audio)]
        filters += [f'[{last}]format=yuv420p[video]',f'[{index}:a]apad[audio]']
        clip=clips/f'{sid}.mp4';stamp=clip.with_suffix('.json')
        clip_inputs=dict(scene=scene,profile=profile,brand=revision['brandLine'],audio=qa['audioSha256'],
                              filters=filters,svgImages=[artifact_digest(plates/f'{sid}-{i}.png') for i in range(len(states))],
                              photo=artifact_digest(store.resolve(scene['photo'])) if scene.get('photo') else None)
        if scene.get('photo'):clip_inputs.update(intro=artifact_digest(plates/'intro.png'),establishing=artifact_digest(plates/'establishing.png'))
        signature=digest(clip_inputs)
        if not(clip.exists() and stamp.exists() and read(stamp).get('signature')==signature):
            run(['-loglevel','error']+inputs+['-filter_complex',';'.join(filters),'-map','[video]','-map','[audio]',
                '-t',str(duration),'-c:v','libx264','-preset',p['videoPreset'],'-crf',str(p['videoCRF']),
                '-c:a','aac','-b:a',profile['mastering']['audioBitrate'],'-ar',str(profile['mastering']['sampleRate']),str(clip)])
            write(stamp,dict(signature=signature))
        timeline.append(dict(sceneId=scene['sceneId'],id=sid,seconds=start,duration=duration,speechDuration=speechdur,states=states,direction=scene['direction']))
        start+=duration;print('RENDERED',revision['revisionId'],sid,round(duration,2),flush=True)
    listing=clips/'concat.txt';listing.write_text(''.join(f"file '{s['id']}.mp4'\n" for s in revision['scenes']),encoding='utf-8')
    raw=folder/'unmastered.mp4';run(['-loglevel','error','-f','concat','-safe','0','-i',str(listing),'-c','copy',str(raw)])
    final=folder/revision['filmFile'];actual=master(raw,final,profile['mastering'],folder)
    write(folder/'worked-evidence.json',revision['evidenceRecord'])
    write(folder/'direction.json',dict(revisionId=revision['revisionId'],inputRevisionDigest=store.input_digest(revision),
          audience=revision['audience'],scenes=revision['scenes'],source='Projection of JSON content store; edit the store.'))
    write(folder/'input-record.json',dict(revision=revision,profile=profile,
          companion=next(c for c in read(store.resolve(revision['companionStoreRef']))['records'] if c['id']==revision['companionId'])))
    save_captions(folder,captions);write(folder/'timeline.json',timeline)
    write(folder/'narration-review.json',dict(method='base.en recognition against script; not continuous human listening',chapters=reviews))
    (folder/'script.md').write_text('# '+revision['title']+'\n\n'+profile['review']['label']+'\n\n'+
        '\n\n'.join('## '+s['id']+' / '+s['status']+'\n\n'+s['narration'] for s in revision['scenes'])+'\n',encoding='utf-8')
    write(folder/'release.json',dict(revisionId=revision['revisionId'],inputRevisionDigest=store.input_digest(revision),
        title=revision['title'],publication=revision['publication'],filmFile=final.name,filmSha256=artifact_digest(final),
        evidenceSha256=artifact_digest(folder/'worked-evidence.json'),
        durationSeconds=start,format=f'{p["width"]}x{p["height"]} H264 AAC {fps}fps',
        captionCount=len(captions),shortestCaptionSeconds=min(b-a for a,b,t in captions),
        longestCaptionSeconds=max(b-a for a,b,t in captions),longestCaptionCharacters=max(len(t.replace('\n',' ')) for a,b,t in captions),
        finalAudio=dict(integratedLUFS=actual['input_i'],truePeakDBTP=actual['input_tp'],loudnessRangeLU=actual['input_lra']),
        imagery=photos,canonicalLayer='Independent SVG instructional plates. Not SCL execution traces.',review=profile['review']))
    print('REVIEW FILM READY',revision['revisionId'],round(start,2),final.stat().st_size,actual['input_tp'],flush=True)
