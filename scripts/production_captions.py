"""Word alignment and globally segmented clauses; no episode content."""
import difflib,re,textwrap,wave
from production_store import read,write,artifact_digest

def norm(s):return re.sub('[^a-z0-9]','',s.lower())
def timecode(t,comma=False):
    ms=round(t*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000)
    return f'{h:02}:{m:02}:{s:02}{"," if comma else "."}{ms:03}'

def align(audio,script,model,minimum_similarity):
    cache=audio.with_suffix('.recognition.json');digest=artifact_digest(audio)
    if cache.exists() and read(cache).get('audioSha256')==digest:words=read(cache)['words']
    else:
        segs,_=model.transcribe(str(audio),language='en',word_timestamps=True,vad_filter=True,condition_on_previous_text=False)
        words=[dict(word=w.word.strip(),start=w.start,end=w.end) for s in segs for w in s.words]
        write(cache,dict(audioSha256=digest,words=words))
    expected=script.split();a=list(map(norm,expected));b=[norm(w['word']) for w in words]
    matcher=difflib.SequenceMatcher(None,a,b,autojunk=False);mapping={};changes=[]
    for tag,a0,a1,b0,b1 in matcher.get_opcodes():
        if tag=='equal':
            for i,j in zip(range(a0,a1),range(b0,b1)):mapping[i]=(words[j]['start'],words[j]['end'])
        else:
            changes.append(dict(script=' '.join(expected[a0:a1]),recognized=' '.join(w['word'] for w in words[b0:b1])))
            if a1>a0 and b1>b0:
                lo=words[b0]['start'];hi=words[b1-1]['end']
                for i in range(a0,a1):mapping[i]=(lo+(hi-lo)*(i-a0)/(a1-a0),lo+(hi-lo)*(i+1-a0)/(a1-a0))
    print('ALIGN',audio.stem,round(matcher.ratio(),3),changes,flush=True)
    if matcher.ratio()<minimum_similarity:raise ValueError('Narration mismatch requires review')
    with wave.open(str(audio)) as w:duration=w.getnframes()/w.getframerate()
    for i in range(len(expected)):
        if i not in mapping:
            prev=max((n for n in mapping if n<i),default=None);nxt=min((n for n in mapping if n>i),default=None)
            lo=mapping[prev][1] if prev is not None else 0;hi=mapping[nxt][0] if nxt is not None else duration
            mapping[i]=(lo,max(lo+.02,hi))
    return expected,mapping,duration,dict(similarity=matcher.ratio(),differences=changes,audioSha256=digest)

def segment(words,mapping,duration,config):
    """Choose all cue boundaries together, so a short tail is not stranded."""
    n=len(words);best={n:(0,[])}
    for i in range(n-1,-1,-1):
        options=[]
        for j in range(i+2,min(n,i+18)+1):
            if j not in best:continue
            text=' '.join(words[i:j]);lines=textwrap.wrap(text,width=config['lineCharacters'],break_long_words=False,break_on_hyphens=False)
            lo=mapping[i][0];nextstart=mapping[j][0] if j<n else duration+.65
            hi=min(nextstart,max(mapping[j-1][1]+.12,lo+config['preferredMinimumSeconds']));span=hi-lo
            if len(lines)>2 or len(text)>config['maximumCharacters'] or span<config['minimumSeconds'] or span>config['maximumSeconds']:continue
            boundary=0 if words[j-1][-1] in '.?!' else 2 if words[j-1][-1] in ',;:' else 7
            cost=boundary+abs(len(text)-53)/18+(5 if span<config['preferredMinimumSeconds'] else 0)+(4 if j-i<3 else 0)+best[j][0]
            options.append((cost,[(lo,hi,'\n'.join(lines))]+best[j][1]))
        if options:best[i]=min(options,key=lambda v:v[0])
    if 0 not in best:raise ValueError('No readable caption segmentation; inspect word timings')
    return best[0][1]

def trigger_time(trigger,words,mapping):
    if not trigger:return 0
    needle=list(map(norm,trigger.split()));hay=list(map(norm,words))
    for i in range(len(hay)-len(needle)+1):
        if hay[i:i+len(needle)]==needle:return mapping[i][0]
    raise ValueError('Missing direction cue: '+trigger)

def save_captions(folder,cues):
    assert all(b<=cues[i+1][0]+.001 for i,(a,b,t) in enumerate(cues[:-1]))
    (folder/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{timecode(a,True)} --> {timecode(b,True)}\n{t}' for i,(a,b,t) in enumerate(cues))+'\n',encoding='utf-8')
    (folder/'captions.vtt').write_text('WEBVTT\n\n'+'\n\n'.join(f'{timecode(a)} --> {timecode(b)}\n{t}' for a,b,t in cues)+'\n',encoding='utf-8')
    write(folder/'caption-cues.json',cues)
