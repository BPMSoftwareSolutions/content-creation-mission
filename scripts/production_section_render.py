"""Compose section-specific Nano Banana art with authored, exact SVG layers."""
import math
from pathlib import Path
import cairosvg
from PIL import Image
from production_store import ROOT,read,write,digest,artifact_digest
from production_composition import section_spec,svg_composition
from production_captions import align,segment,trigger_time,save_captions
from production_render import run,master

def render_sections(store,revision):
    from faster_whisper import WhisperModel
    profile=store.profile(revision);p=profile['visual'];c=profile['captions'];fps=p['fps']
    folder=store.resolve(revision['outputDirectory']);plates=folder/'plates';clips=folder/'clips'
    plates.mkdir(parents=True,exist_ok=True);clips.mkdir(exist_ok=True)
    asset_reviews=read(store.resolve(revision['sectionAssetReviewRef']))['sections']
    model=WhisperModel(c['model'],device='cpu',compute_type='int8',cpu_threads=8,download_root=str(ROOT/'.tools/whisper'))
    captions=[];timeline=[];narration_reviews=[];images=[];offset=0
    for scene in revision['scenes']:
        sid=scene['id'];plan,spec=section_spec(store,revision,scene)
        source=store.resolve(scene['visualAssetRef']);image_digest=artifact_digest(source)
        asset_receipt=read(source.with_suffix('.receipt.json'))
        review=next((r for r in asset_reviews if r['sectionId']==scene['sectionVisualId']),None)
        if not review or review['imageDigest']!=image_digest or review['status']!='ACCEPTED_FOR_COMPOSITING':
            raise ValueError('Section image needs a current visual review: '+scene['sectionVisualId'])
        if asset_receipt['imageDigest']!=image_digest:raise ValueError('Image receipt mismatch')
        audio=store.resolve(scene['audioRef']);speech_receipt=read(audio.with_suffix('.receipt.json'))
        if speech_receipt['script']!=scene['narration'] or speech_receipt['audioDigest']!=artifact_digest(audio):raise ValueError('Narration is stale')
        words,mapping,speechdur,qa=align(audio,scene['narration'],model,c['minimumSimilarity'])
        narration_reviews.append(dict(sceneId=scene['sceneId'],**qa))
        duration=math.ceil((speechdur+p['chapterTailSeconds']+scene['pause'])*fps)/fps
        captions.extend((offset+a,offset+b,t) for a,b,t in segment(words,mapping,speechdur,c))
        image=Image.open(source).convert('RGB');scale=max(2016/image.width,1134/image.height)
        image=image.resize((round(image.width*scale),round(image.height*scale)),Image.Resampling.LANCZOS)
        left=(image.width-2016)//2;top=(image.height-1134)//2
        image=image.crop((left,top,left+2016,top+1134));back=plates/f'{sid}-material.png';image.save(back)
        x0,y0,x1,y1=spec['camera']
        inputs=['-loop','1','-framerate',str(fps),'-i',str(back)]
        filters=[f"[0:v]crop=1920:1080:x='48+{x0}+({x1-x0})*min(t/{duration},1)':y='27+{y0}+({y1-y0})*min(t/{duration},1)'[material]"]
        states=[];last='material';index=1
        for i,state in enumerate(scene['states']):
            start=trigger_time(state['trigger'],words,mapping)
            overlay=svg_composition(revision,scene,state,i,plan,spec,p)
            clean=svg_composition(revision,scene,state,i,plan,spec,p,clean=True)
            (plates/f'{sid}-{i}.svg').write_text(clean,encoding='utf-8')
            (plates/f'{sid}-{i}-overlay.svg').write_text(overlay,encoding='utf-8')
            overlay_path=plates/f'{sid}-{i}-overlay.png';cairosvg.svg2png(bytestring=overlay.encode(),write_to=str(overlay_path))
            inputs+=['-loop','1','-framerate',str(fps),'-i',str(overlay_path)]
            # Switch full semantic overlays, not alpha-stack old and new claims.
            stop=trigger_time(scene['states'][i+1]['trigger'],words,mapping) if i+1<len(scene['states']) else duration+.1
            filters.append(f'[{last}][{index}:v]overlay=0:0:enable=\'gte(t,{start})*lt(t,{stop})\'[section{i}]')
            last=f'section{i}';index+=1
            states.append(dict(index=i,seconds=start,svg=f'{sid}-{i}.svg',visualFormatType=plan['format'],**state))
        for j,trace in enumerate(spec.get('traces',[])):
            stop=states[min(trace['states'][-1]+1,len(states)-1)]['seconds'] if trace['states'][-1]+1<len(states) else duration
            start=trace['start'];x,y=trace['from'];endx,endy=trace['to'];size=trace['size']
            inputs+=['-f','lavfi','-i',f'color=c={trace["color"]}:s={size}x{size}:r={fps}']
            filters.append(f"[{last}][{index}:v]overlay=x='{x-size/2}+({endx-x})*min(max((t-{start})/{trace['duration']},0),1)':y='{y-size/2}+({endy-y})*min(max((t-{start})/{trace['duration']},0),1)':enable='between(t,{start},{stop})'[trace{j}]")
            last=f'trace{j}';index+=1
        inputs+=['-i',str(audio)]
        filters += [f'[{last}]format=yuv420p[video]',f'[{index}:a]apad[audio]']
        signature=digest(dict(scene=scene,profile=profile,plan=plan,spec=spec,material=artifact_digest(back),
            overlays=[artifact_digest(plates/f'{sid}-{i}-overlay.png') for i in range(len(states))],audio=artifact_digest(audio),filters=filters))
        clip=clips/f'{sid}.mp4';stamp=clip.with_suffix('.json')
        if not (clip.exists() and stamp.exists() and read(stamp)['signature']==signature):
            run(['-loglevel','error']+inputs+['-filter_complex',';'.join(filters),'-map','[video]','-map','[audio]',
                '-t',str(duration),'-c:v','libx264','-preset',p['videoPreset'],'-crf',str(p['videoCRF']),
                '-c:a','aac','-b:a',profile['mastering']['audioBitrate'],'-ar',str(profile['mastering']['sampleRate']),str(clip)])
            write(stamp,dict(signature=signature))
        timeline.append(dict(sceneId=scene['sceneId'],id=sid,seconds=offset,duration=duration,speechDuration=speechdur,
            states=states,direction=plan['composition'],visualFormatType=plan['format'],teachingPurpose=plan['purpose'],
            camera=plan['camera'],motion=plan['motion'],canonicalLayer='Section-authored SVG; illustrative, not an execution trace.'))
        images.append(dict(sectionId=scene['sectionVisualId'],source=scene['visualAssetRef'],sha256=image_digest,format=plan['format']))
        offset+=duration;print('SECTION FILM',scene['sectionVisualId'],plan['format'],'READY',flush=True)
    listing=clips/'concat.txt';listing.write_text(''.join(f"file '{s['id']}.mp4'\n" for s in revision['scenes']),encoding='utf-8')
    raw=folder/'unmastered.mp4';run(['-loglevel','error','-f','concat','-safe','0','-i',str(listing),'-c','copy',str(raw)])
    final=folder/revision['filmFile'];actual=master(raw,final,profile['mastering'],folder)
    save_captions(folder,captions);write(folder/'timeline.json',timeline);write(folder/'worked-evidence.json',revision['evidenceRecord'])
    write(folder/'narration-review.json',dict(method='Existing script and narration retained; word alignment and caption segmentation rechecked. No human listening claim.',chapters=narration_reviews))
    write(folder/'direction.json',dict(revisionId=revision['revisionId'],scenes=timeline,source='Authored section direction and composition records; no blanket layouts.'))
    write(folder/'input-record.json',dict(revision=revision,profile=profile,direction=read(store.resolve(revision['sectionDirectionRef'])),compositions=read(store.resolve(revision['sectionCompositionRef']))))
    (folder/'script.md').write_text('# '+revision['title']+'\n\n'+profile['review']['label']+'\n\n'+'\n\n'.join('## '+s['id']+' / '+s['status']+'\n\n'+s['narration'] for s in revision['scenes'])+'\n',encoding='utf-8')
    write(folder/'release.json',dict(revisionId=revision['revisionId'],inputRevisionDigest=store.input_digest(revision),
        title=revision['title'],publication=revision['publication'],filmFile=final.name,filmSha256=artifact_digest(final),
        evidenceSha256=artifact_digest(folder/'worked-evidence.json'),durationSeconds=offset,
        format=f'1920x1080 H264 AAC {fps}fps',captionCount=len(captions),shortestCaptionSeconds=min(b-a for a,b,t in captions),
        longestCaptionSeconds=max(b-a for a,b,t in captions),longestCaptionCharacters=max(len(t.replace('\n',' ')) for a,b,t in captions),
        finalAudio=dict(integratedLUFS=actual['input_i'],truePeakDBTP=actual['input_tp'],loudnessRangeLU=actual['input_lra']),
        imagery=images,canonicalLayer='Individually authored SVG compositions over reviewed Nano Banana material layers.',review=profile['review']))
    print('SECTION-DIRECTED FILM READY',revision['revisionId'],final.stat().st_size,flush=True)
