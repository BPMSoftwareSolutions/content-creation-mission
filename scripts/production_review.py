"""Build a local, responsive review surface and inspectable encoded-frame samples."""
import html,json,math
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from production_store import read,write,artifact_digest
from production_render import run

def esc(t):return html.escape(str(t),quote=True)

def review(store,revision):
    folder=store.resolve(revision['outputDirectory']);profile=store.profile(revision);p=profile['visual']
    receipt=read(folder/'release.json')
    if receipt['inputRevisionDigest']!=store.input_digest(revision):raise ValueError('Review requested for stale input revision; render current records first')
    film=folder/receipt['filmFile']
    if artifact_digest(film)!=receipt['filmSha256']:raise ValueError('Film hash no longer matches receipt')
    qa=folder/'review';qa.mkdir(exist_ok=True)
    timeline=read(folder/'timeline.json');cues=read(folder/'caption-cues.json');samples=[];contact=[]
    for chapter in timeline:
        for i,state in enumerate(chapter['states']):
            end=chapter['states'][i+1]['seconds'] if i+1<len(chapter['states']) else chapter['duration']
            sample=chapter['seconds']+min(end-.15,max(state['seconds']+1,(state['seconds']+end)/2))
            cue=next((t for a,b,t in cues if a<=sample<=b),'')
            name=f"{chapter['id']}-{i}";frame=qa/f'{name}.png'
            run(['-loglevel','error','-ss',str(sample),'-i',str(film),'-frames:v','1',str(frame)])
            im=Image.open(frame).convert('RGB');draw=ImageDraw.Draw(im)
            # Representative caption burn-in for inspection. Native player rendering remains configurable.
            if cue:
                font=ImageFont.truetype(p['fontFile'],52)
                for n,line in enumerate(cue.splitlines()):
                    w=draw.textlength(line,font=font);y=922+n*60
                    draw.rectangle(((1920-w)/2-14,y-5,(1920+w)/2+14,y+60),fill='#000000')
                    draw.text(((1920-w)/2,y),line,font=font,fill='white')
            im.save(qa/f'{name}-captioned.png')
            for width in profile['captions']['sampleWidths']:
                im.resize((width,round(width*1080/1920)),Image.Resampling.LANCZOS).save(qa/f'{name}-{width}.jpg',quality=94)
            tile=im.resize((480,270),Image.Resampling.LANCZOS)
            card=Image.new('RGB',(480,310),'#ffffff');card.paste(tile,(0,0))
            ImageDraw.Draw(card).text((10,280),f'{chapter["id"]}.{i} / {sample:.2f}s',font=ImageFont.truetype(p['fontFile'],18),fill='#000000')
            contact.append(card);samples.append(dict(sceneId=chapter['sceneId'],stateId=state['stateId'],seconds=sample,caption=cue,path=f'review/{name}.png'))
    grid=Image.new('RGB',(1440,math.ceil(len(contact)/3)*310),'#dddddd')
    for i,im in enumerate(contact):grid.paste(im,((i%3)*480,(i//3)*310))
    grid.save(qa/'contact-sheet.jpg',quality=93)
    write(qa/'sample-manifest.json',dict(filmSha256=artifact_digest(film),samples=samples,
       scope='Actual encoded frames with representative caption overlay; sampled visual QA is not uninterrupted listening or playback.'))
    # Thumbnail design uses the same records and the existing cast as the film.
    im=Image.new('RGB',(1280,720),p['background'])
    source=next((s.get('visualAssetRef') or s.get('photo') for s in revision['scenes'] if s.get('visualAssetRef') or s.get('photo')),None)
    if source:
        photo=Image.open(store.resolve(source)).convert('RGB');scale=max(1280/photo.width,720/photo.height)
        photo=photo.resize((round(photo.width*scale),round(photo.height*scale)),Image.Resampling.LANCZOS)
        x=(photo.width-1280)//2;y=(photo.height-720)//2;photo=photo.crop((x,y,x+1280,y+720))
        im.paste(photo,(0,0));ImageDraw.Draw(im,'RGBA').rectangle((0,0,680,720),fill=(8,19,30,230))
    draw=ImageDraw.Draw(im);draw.rectangle((52,64,120,72),fill=p['accent'])
    for i,line in enumerate(revision['thumbnail']):
        font=ImageFont.truetype(p['boldFontFile'],108)
        while draw.textlength(line,font=font)>650:font=ImageFont.truetype(p['boldFontFile'],font.size-1)
        draw.text((50,220+i*135),line,font=font,fill=p['foreground'])
    draw.text((52,624),revision['brandLine'].split('/')[0].strip(),font=ImageFont.truetype(p['boldFontFile'],36),fill=p['accent'])
    im.save(folder/'thumbnail.jpg',quality=95);im.resize((320,180),Image.Resampling.LANCZOS).save(qa/'thumbnail-320.jpg',quality=95)
    companion=next(v for v in read(store.resolve(revision['companionStoreRef']))['records'] if v['id']==revision['companionId'])
    md='# '+companion['title']+'\n\n'+companion['scope']+'\n\n'
    body=''
    for section in companion['sections']:
        md+='## '+section['title']+'\n\n'+'\n'.join('- '+t for t in section['items'])+'\n\n'
        body+='<section><h3>'+esc(section['title'])+'</h3><ul>'+''.join('<li>'+esc(t)+'</li>' for t in section['items'])+'</ul></section>'
    for link in companion['links']:md+='['+link['label']+']('+link['url']+')\n'
    (folder/companion['filename']).write_text(md,encoding='utf-8')
    (folder/'description.txt').write_text(revision['description'],encoding='utf-8')
    (folder/'title.txt').write_text(revision['title']+'\n',encoding='utf-8')
    # Seek inside the first encoded frame of the chapter, past container rounding.
    chapterlinks=''.join(f'<button type="button" data-time="{ch["seconds"]+min(.2,ch["duration"]/2)}">{esc(ch["states"][0]["title"])}</button>' for ch in timeline)
    page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'''+esc(revision['title'])+'''</title>
<style>:root{color-scheme:dark}*{box-sizing:border-box}body{margin:0;background:#08131e;color:#f2f5ed;font:18px/1.6 system-ui,sans-serif}main{max-width:1100px;margin:auto;padding:32px 24px}h1{font-size:clamp(30px,5vw,54px);line-height:1.12;max-width:950px}h2{margin-top:2em}a{color:#6ce4cd}video{width:100%;border:1px solid #425666;background:black}video::cue{font-size:1em;background:#000d}nav{display:flex;gap:12px;flex-wrap:wrap}button{background:#142633;color:inherit;border:1px solid #596e7c;border-radius:6px;padding:10px;font:inherit;cursor:pointer;text-align:left}button:focus-visible,a:focus-visible{outline:3px solid #ffc884;outline-offset:3px}.tag{color:#ffc884;font-weight:bold}section{padding:16px 0;border-top:1px solid #425666}li{margin:12px 0}.technical{font-size:15px;color:#b1c1cb}textarea{width:100%;min-height:180px;background:#142633;color:inherit;padding:15px;font:inherit}img{max-width:100%}@media(max-width:500px){main{padding:20px 14px}body{font-size:17px}nav{display:grid}h1{font-size:31px}}@media print{video,nav,textarea,.review-only{display:none}body{background:white;color:black}a{color:black}}</style>
<main><p class="tag">'''+esc(profile['review']['label'])+'''</p><h1>'''+esc(revision['title'])+'''</h1><p>'''+esc(revision['promise'])+'''</p>
<video id="film" controls preload="metadata" poster="thumbnail.jpg?v='''+artifact_digest(folder/'thumbnail.jpg')+'''"><source src="'''+esc(revision['filmFile'])+'?v='+receipt['filmSha256']+'''" type="video/mp4"><track kind="captions" label="English" srclang="en" src="captions.vtt?v='''+artifact_digest(folder/'captions.vtt')+'''" default></video>
<p>'''+esc(profile['review']['disclosure'])+'''</p><nav><a href="'''+esc(companion['filename'])+'''" download>Download the worksheet</a><a href="script.md">Transcript</a><a href="captions.srt">Captions</a><a href="review/contact-sheet.jpg">Captioned frame samples</a><a href="worked-evidence.json">Evidence scope</a></nav>
<h2>Jump to a teaching beat</h2><nav>'''+chapterlinks+'''</nav><h2>'''+esc(companion['title'])+'''</h2>'''+body+'''
<p class="technical">'''+esc(companion['scope'])+'''</p><section class="review-only"><h2>Review this edition</h2><p>Watch once without interruption. Listen on headphones and a small speaker. Note pronunciation, uncomfortable pauses, cuts, caption timing, and anything hard to read. Then try the worksheet without replaying the explanation.</p><p>Ask an unfamiliar viewer: What conflict did you see? What evidence changed the conclusion? Which parts were simulated? What can be justified next? Record their own words before explaining the intended answer.</p><textarea aria-label="Private review notes" placeholder="Timestamp, issue, and proposed correction. Notes stay in this tab and are not submitted."></textarea><p>These checks are pending. No learning, retention or marketing performance is claimed.</p></section>
<p class="technical">Input revision: '''+esc(receipt['inputRevisionDigest'])+'''</p></main><script>document.querySelectorAll('[data-time]').forEach(b=>b.addEventListener('click',()=>{const v=document.getElementById('film');v.currentTime=Number(b.dataset.time);v.focus()}));</script></html>'''
    (folder/'index.html').write_text(page,encoding='utf-8')
    print('REVIEW SURFACE READY',revision['revisionId'],len(samples),'encoded samples',flush=True)

def review_hub(store):
    import os
    package=store.data['reviewPackage'];folder=store.resolve(package['outputDirectory']);folder.mkdir(parents=True,exist_ok=True)
    criteria=read(store.resolve(package['criteriaRef']));cards=[];metrics=[];section_tiles=[]
    for r in store.revisions():
        path=store.resolve(r['outputDirectory']);receipt=read(path/'release.json')
        if receipt['inputRevisionDigest']!=store.input_digest(r):raise ValueError('Cannot bundle a stale revision')
        link=os.path.relpath(path/'index.html',folder).replace('\\','/')
        poster=os.path.relpath(path/'thumbnail.jpg',folder).replace('\\','/')
        minutes,seconds=divmod(round(receipt['durationSeconds']),60)
        cards.append(f'<article><a href="{esc(link)}"><img src="{esc(poster)}" alt="{esc(" ".join(r["thumbnail"]))}"><h2>{esc(r["title"])}</h2></a><p>{esc(r["promise"])}</p><p>{minutes}:{seconds:02} · Captions, worksheet and evidence included.</p></article>')
        metrics.append(dict(revisionId=r['revisionId'],filmSha256=receipt['filmSha256'],durationSeconds=receipt['durationSeconds'],
                            finalAudio=receipt['finalAudio'],shortestCaptionSeconds=receipt['shortestCaptionSeconds']))
        for ch in read(path/'timeline.json'):
            source=path/'review'/f"{ch['id']}-{len(ch['states'])-1}.png"
            im=Image.open(source).convert('RGB').resize((480,270),Image.Resampling.LANCZOS)
            tile=Image.new('RGB',(480,310),'#ffffff');tile.paste(im,(0,0))
            label=f"{r['episodeId']}/{ch['id']}  {ch.get('visualFormatType','')}"
            ImageDraw.Draw(tile).text((12,279),label,font=ImageFont.truetype(store.profile(r)['visual']['fontFile'],16),fill='#102530')
            section_tiles.append(tile)
    gallery=Image.new('RGB',(1920,math.ceil(len(section_tiles)/4)*310),'#dfe3e3')
    for i,tile in enumerate(section_tiles):gallery.paste(tile,((i%4)*480,(i//4)*310))
    gallery.save(folder/'section-gallery.jpg',quality=94)
    rows=''.join('<tr><td>'+esc(c['id'])+'</td><td>'+esc(c['issue'])+'</td><td>'+esc(c['change'])+'</td><td>'+esc(c['status'])+'</td></tr>' for c in criteria['criteria'])
    page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'''+esc(package['title'])+'''</title><style>*{box-sizing:border-box}body{margin:0;background:#08131e;color:#f2f5ed;font:18px/1.6 system-ui}main{max-width:1120px;margin:auto;padding:40px 24px}a{color:#6ce4cd}h1{font-size:46px;line-height:1.12}.films{display:grid;grid-template-columns:1fr 1fr;gap:32px}img{width:100%;border-radius:8px}h2{font-size:25px;line-height:1.3}.tag{color:#ffc884}table{border-collapse:collapse;font-size:15px}td,th{padding:14px;text-align:left;border-bottom:1px solid #425666;vertical-align:top}details{margin-top:50px}summary{cursor:pointer}.table{overflow:auto}@media(max-width:720px){.films{grid-template-columns:1fr}h1{font-size:34px}main{padding:24px 16px}}</style><main><p class="tag">LOCAL REVIEW / NOT PUBLISHED</p><h1>'''+esc(package['title'])+'''</h1><p>'''+esc(package['description'])+'''</p><div class="films">'''+''.join(cards)+'''</div><p>Publishing and live thumbnail checks wait for your review. Continuous human listening and unfamiliar-viewer assessment remain pending.</p><details><summary>What changed against the critiques</summary><div class="table"><table><thead><tr><th>ID</th><th>Issue</th><th>Change</th><th>Status</th></tr></thead><tbody>'''+rows+'''</tbody></table></div></details></main></html>'''
    page=page.replace('<details>','<p><a href="section-gallery.jpg">See every subsection design</a></p><details>',1)
    (folder/'index.html').write_text(page,encoding='utf-8')
    write(folder/'review-manifest.json',dict(publication=criteria['publicationDecision'],films=metrics,criteriaRef=package['criteriaRef']))
    md='# '+package['title']+'\n\n'+package['description']+'\n\n'
    for c in criteria['criteria']:md+='## '+c['id']+' · '+c['issue']+'\n\n'+c['change']+'\n\nEvidence: '+c['evidence']+'\n\nStatus: '+c['status']+'\n\n'
    (folder/'critique-response.md').write_text(md,encoding='utf-8')
    print('REVIEW PACKAGE READY',folder,flush=True)
