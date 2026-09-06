"""Check the narration and align the exact approved script to recognized words.

Optional editorial QA dependency: faster-whisper==1.2.1, base.en model.
Saves recognition evidence; does not treat recognition as a human review.
"""
import difflib, json, re, shutil
from pathlib import Path
from faster_whisper import WhisperModel
from produce_episode_two import OUT, ROOT, SITE, SCENES, dump, timecode, public_data

def norm(s): return re.sub(r'[^a-z0-9]', '', s.lower())

def main():
    model=WhisperModel('base.en', device='cpu', compute_type='int8', cpu_threads=8,
                       download_root=str(ROOT/'.tools/whisper'))
    timeline=json.loads((OUT/'timeline.json').read_text(encoding='utf-8'))
    evidence=[];cues=[]
    for scene,chapter in zip(SCENES,timeline):
        cache=OUT/'audio'/f'{scene["id"]}.recognition.json'
        if cache.exists():
            words=json.loads(cache.read_text(encoding='utf-8'))
        else:
            segments,_=model.transcribe(str(OUT/'audio'/f'{scene["id"]}.wav'),language='en',word_timestamps=True,vad_filter=True,condition_on_previous_text=False)
            words=[{'word':w.word.strip(),'start':w.start,'end':w.end} for seg in segments for w in seg.words]
            dump(cache,words)
        expected=scene['narration'].split();a=[norm(w) for w in expected];b=[norm(w['word']) for w in words]
        matcher=difflib.SequenceMatcher(None,a,b,autojunk=False)
        changed=[];mapping={}
        for tag,a0,a1,b0,b1 in matcher.get_opcodes():
            if tag=='equal':
                for n,j in zip(range(a0,a1),range(b0,b1)):mapping[n]=(words[j]['start'],words[j]['end'])
            else:
                changed.append({'script':' '.join(expected[a0:a1]),'recognized':' '.join(w['word'] for w in words[b0:b1])})
                if a1>a0 and b1>b0:
                    lo=words[b0]['start'];hi=words[b1-1]['end']
                    for n in range(a0,a1):mapping[n]=(lo+(hi-lo)*(n-a0)/(a1-a0),lo+(hi-lo)*(n+1-a0)/(a1-a0))
        ratio=matcher.ratio();evidence.append({'chapter':scene['id'],'similarity':ratio,'differences':changed})
        print(scene['id'],round(ratio,3),json.dumps(changed),flush=True)
        if ratio<.90: raise ValueError('Review narration mismatch before generating final captions')
        for n in range(len(a)):
            if n not in mapping:
                prev=max((i for i in mapping if i<n),default=None);nxt=min((i for i in mapping if i>n),default=None)
                lo=mapping[prev][1] if prev is not None else 0
                hi=mapping[nxt][0] if nxt is not None else chapter['speechDuration']
                mapping[n]=(lo,max(lo+.05,hi))
        # Sentence-aware, short cues; preserve every approved word and punctuation.
        begin=0
        for n,word in enumerate(expected):
            group=' '.join(expected[begin:n+1])
            if len(group)>65 or word[-1] in '.?!' or n==len(expected)-1:
                start=chapter['seconds']+mapping[begin][0];end=chapter['seconds']+mapping[n][1]
                if len(group)>48:
                    midpoint=min(range(1,n-begin+1),key=lambda x:abs(len(' '.join(expected[begin:begin+x]))-len(group)/2)) if n>begin else 0
                    if midpoint:group=' '.join(expected[begin:begin+midpoint])+'\n'+' '.join(expected[begin+midpoint:n+1])
                cues.append((start,max(start+.15,end),group));begin=n+1
        if scene.get('pause',0)>=8:
            cues.append((chapter['seconds']+chapter['speechDuration'],chapter['seconds']+chapter['duration'],'[Pause and write your answer.\nTake the time you need.]'))
    # Clamp any recognition overlap at the following cue boundary.
    cues=[(a,min(b,cues[i+1][0]) if i+1<len(cues) else b,text) for i,(a,b,text) in enumerate(cues)]
    assert all(b>a>=0 for a,b,_ in cues)
    (OUT/'captions.vtt').write_text('WEBVTT\n\n'+'\n\n'.join(f'{timecode(a)} --> {timecode(b)}\n{text}' for a,b,text in cues)+'\n',encoding='utf-8')
    (OUT/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{timecode(a,True)} --> {timecode(b,True)}\n{text}' for i,(a,b,text) in enumerate(cues))+'\n',encoding='utf-8')
    dump(OUT/'narration-review.json',{'method':'Independent base.en speech recognition compared with exact script; recognized word timestamps used for caption alignment. Not a human listening review.','chapters':evidence})
    release=json.loads((OUT/'release.json').read_text(encoding='utf-8'));release['captionTiming']='Script aligned to base.en recognized word timestamps; chapter WAV boundaries measured.'
    dump(OUT/'release.json',release);dump(ROOT/'release-site/app/episode-two.json',public_data(release))
    shutil.copy2(OUT/'captions.vtt',SITE/'captions.vtt')
    print('ALIGNED CAPTIONS READY',len(cues),flush=True)

if __name__=='__main__':main()
