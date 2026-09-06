"""Composite reviewed Nano Banana staging and timed deterministic infographics.

The approved narration and chapter durations are retained exactly. Human scenes
are camera moves over stills; exact labels and all teaching graphics are SVG.
"""
import argparse, json, math, shutil, subprocess
from pathlib import Path
from PIL import Image, ImageDraw
import cairosvg, imageio_ffmpeg
from produce_episode_two import OUT, ROOT, SITE, SCENES, BG, TEAL, WHITE, MUTED, AMBER, dump, digest, make_svg, text_svg, wrap, public_data

FF=imageio_ffmpeg.get_ffmpeg_exe()
HUMAN={'01':'01','03':'02','07':'02','08':'02','12':'03','13':'03'}
COPY={
 '01':(['The task finished.','Did it help?'],'A completed action.\nA result people can use.'),
 '03':(['“The reservation','succeeded…”'],'Who can commit a change?\nOnly the coordinator.'),
 '07':(['A reservation.','Not the whole','result.'],'Hear the people affected\nbefore promising completion.'),
 '08':(['What if moving it','excludes someone','else?'],'The objection matters.'),
 '12':(['Completion','is one fact.'],'Which result do you mean?\nWho still cannot get it?'),
 '13':(['Whose result','is still open?'],'Carry the question with you.\nNext: What do we actually know?')}

def run(cmd):subprocess.run([FF,'-hide_banner','-loglevel','error','-y']+cmd,check=True)

def hero_overlay(scene):
    headline,body=COPY[scene['id']]
    tag='ILLUSTRATIVE NEXT STEP' if scene['id'] in ('12','13') else 'FICTIONAL TEACHING SCENE'
    s=['<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080"><defs><linearGradient id="shade"><stop stop-color="#040b12" stop-opacity=".97"/><stop offset=".42" stop-color="#040b12" stop-opacity=".80"/><stop offset=".68" stop-color="#040b12" stop-opacity=".06"/><stop offset="1" stop-opacity="0"/></linearGradient></defs><rect width="1920" height="1080" fill="url(#shade)"/>',text_svg(['SideFX / FOUNDATIONS'],90,78,28,TEAL,True),text_svg(['EPISODE 02 · CONSEQUENCES'],90,135,24,MUTED),text_svg(headline,90,335,72,WHITE,True,1.16),text_svg(wrap(body,650,34),90,675,34,WHITE,False,1.45),'<rect x="0" y="965" width="1920" height="115" fill="#040b12" fill-opacity=".82"/>',text_svg([tag+' · AI-GENERATED IMAGERY'],90,1024,24,MUTED),'</svg>']
    return ''.join(s)

def animated_assets(scene,folder,times):
    """Reveal existing canonical panels at fixed x/y; geometry never changes."""
    svg=make_svg(scene,SCENES.index(next(s for s in SCENES if s['id']==scene['id'])))
    (folder/f'{scene["id"]}.svg').write_text(svg,encoding='utf-8')
    cairosvg.svg2png(bytestring=svg.encode(),write_to=str(folder/f'{scene["id"]}.png'))
    source=Image.open(folder/f'{scene["id"]}.png').convert('RGB');back=source.copy();draw=ImageDraw.Draw(back)
    count=len(scene['cards']);gap=28;width=(1720-gap*(count-1))/count;panels=[]
    for i,t in enumerate(times):
        x=round(100+i*(width+gap));right=round(100+i*(width+gap)+width)
        panel=folder/f'{scene["id"]}-panel-{i}.png';source.crop((x,492,right,892)).save(panel)
        draw.rectangle((x,492,right,892),fill=BG)
        panels.append({'path':panel,'x':x,'y':492,'time':t})
    back.save(folder/f'{scene["id"]}-base.png')
    return panels

def main():
    p=argparse.ArgumentParser();p.add_argument('--execute',action='store_true');args=p.parse_args()
    folder=OUT/'film-plates';folder.mkdir(exist_ok=True);clips=OUT/'directed-clips';clips.mkdir(exist_ok=True)
    selection=json.loads((OUT/'shot-selection.json').read_text())
    review=json.loads((OUT/'film-visual-review.json').read_text())
    for shot in selection['shots']:
        assert digest(ROOT/shot['path'])==shot['imageDigest']
        assert review['imageDigests'][shot['shot']]==shot['imageDigest']
    assert review['disposition']=='VISUAL_EXPERIENCE_CONFORMS'
    timeline=json.loads((OUT/'timeline.json').read_text());motions=[]
    modified={s['id']:s for s in SCENES}
    modified['11']={**modified['11'],'body':'','cards':[('POSSIBILITY · NOT ESTABLISHED','An acceptable travel option could change the next step.',TEAL),('POSSIBILITY · NOT ESTABLISHED','A different time could exclude more people.',AMBER)]}
    for scene in SCENES:
        if scene['id'] in HUMAN:
            svg=folder/f'{scene["id"]}-overlay.svg';svg.write_text(hero_overlay(scene),encoding='utf-8');cairosvg.svg2png(url=str(svg),write_to=str(svg.with_suffix('.png')))
    animated={'02':[0,6.8],'06':[3.6,7.0,11.5],'09':[0,4.8],'11':[0,3.0]}
    assets={sid:animated_assets(modified[sid],folder,times) for sid,times in animated.items()}
    if not args.execute:print('COMPOSITE ASSETS READY');return
    for scene,c in zip(SCENES,timeline):
        sid=scene['id'];duration=round(c['duration']*24)/24
        cmd=[];filters=[]
        if sid in HUMAN:
            photo=OUT/'film-assets'/f'{HUMAN[sid]}.png'
            cmd=['-loop','1','-framerate','24','-i',str(photo),'-loop','1','-framerate','24','-i',str(folder/f'{sid}-overlay.png')]
            frames=round(duration*24)
            filters=[f"[0:v]scale=2048:1152:force_original_aspect_ratio=increase,crop=2048:1152,zoompan=z='1+0.02*on/{frames}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s=1920x1080:fps=24[photo]",'[photo][1:v]overlay=0:0:shortest=1[composite]']
            audioidx=2;last='composite'
            motions.append({'chapter':sid,'kind':'CAMERA_PUSH_OVER_GENERATED_STILL','shot':HUMAN[sid],'semanticText':f'film-plates/{sid}-overlay.svg','zoom':1.02,'generatedPerformance':False})
        elif sid in animated:
            cmd=['-loop','1','-framerate','24','-i',str(folder/f'{sid}-base.png')];last='0:v'
            for i,a in enumerate(assets[sid]):
                cmd+=['-loop','1','-framerate','24','-i',str(a['path'])]
                filters.append(f'[{i+1}:v]format=rgba,fade=t=in:st={a["time"]}:d=0.65:alpha=1[p{i}]')
                filters.append(f'[{last}][p{i}]overlay={a["x"]}:{a["y"]}:shortest=1[v{i}]');last=f'v{i}'
            audioidx=len(assets[sid])+1
            motions.append({'chapter':sid,'kind':'FIXED_GEOMETRY_PANEL_REVEAL','canonicalSvg':f'film-plates/{sid}.svg','panels':[{'x':a['x'],'y':a['y'],'start':a['time'],'duration':.65} for a in assets[sid]],'semanticRelationshipsChanged':False})
        else:
            cmd=['-loop','1','-framerate','24','-i',str(OUT/'plates'/f'{sid}.png')];last='0:v';audioidx=1
            motions.append({'chapter':sid,'kind':'STILL_REFLECTION_HOLD','canonicalSvg':f'plates/{sid}.svg','countdown':False})
        cmd+=['-i',str(OUT/'audio'/f'{sid}.wav')]
        filters += [f'[{last}]fade=t=in:st=0:d=0.2,format=yuv420p[final]',f'[{audioidx}:a]apad[audio]']
        clip=clips/f'{sid}.mp4'
        run(cmd+['-filter_complex',';'.join(filters),'-map','[final]','-map','[audio]','-t',str(duration),'-c:v','libx264','-preset','fast','-crf','19','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart',str(clip)])
        # Inspect an actual encoded frame from every chapter, including a late reveal.
        run(['-ss',str(min(duration-1,12)),'-i',str(clip),'-frames:v','1',str(folder/f'{sid}-review.png')])
        print('DIRECTED CHAPTER',sid,'READY',flush=True)
    listing=clips/'concat.txt';listing.write_text(''.join(f"file '{s['id']}.mp4'\n" for s in SCENES),encoding='utf-8')
    film=OUT/'episode-02-directed.mp4'
    run(['-f','concat','-safe','0','-i',str(listing),'-c','copy','-movflags','+faststart',str(film)])
    run(['-xerror','-i',str(film),'-f','null','-'])
    thumb=Image.open(folder/'01-review.png').convert('RGB');thumb.resize((1280,720),Image.Resampling.LANCZOS).save(OUT/'thumbnail-directed.jpg',quality=95,optimize=True)
    shutil.copy2(film,SITE/'episode-02.mp4');shutil.copy2(OUT/'thumbnail-directed.jpg',SITE/'thumbnail.jpg')
    dump(OUT/'motion-timeline.json',motions)
    receipt={'film':'episode-02-directed.mp4','filmSha256':digest(film),'durationSeconds':sum(round(c['duration']*24)/24 for c in timeline),'format':'1920x1080 H264 AAC, 24fps','shots':selection['shots'],'directionSha256':digest(OUT/'film-direction.json'),'visualReviewSha256':digest(OUT/'film-visual-review.json'),'motionTimelineSha256':digest(OUT/'motion-timeline.json'),'narration':'Existing approved chapter WAVs unchanged','animatedInfographics':list(animated),'sourceLayer':'Clean SVG files retained independently','nanoBanana':'Human staging only; no semantic geometry generated','learningOutcomes':'UNMEASURED'}
    dump(OUT/'film.receipt.json',receipt)
    release=json.loads((OUT/'release.json').read_text(encoding='utf-8'));release.update(filmSha256=digest(film),filmFile=film.name,status='DIRECTED_CUT_READY',videoUrl=release.get('videoUrl'),disclosure='Fictional scenario; AI-generated human imagery; synthetic narration; deterministic animated SVG plates.')
    dump(OUT/'release.json',release);dump(ROOT/'release-site/app/episode-two.json',public_data(release))
    description=OUT/'description.txt'
    description.write_text(description.read_text(encoding='utf-8').replace('Synthetic narration. Deterministic visual plates.','AI-generated human scenes. Synthetic narration. Deterministic animated infographics.'),encoding='utf-8')
    print('DIRECTED FILM READY',film.stat().st_size,flush=True)

if __name__=='__main__':main()
