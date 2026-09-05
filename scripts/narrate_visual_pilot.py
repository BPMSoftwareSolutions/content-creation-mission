"""Generate eight resumable Gemini narration chapters; explicit --execute required."""
import argparse, base64, hashlib, json, urllib.request, wave
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from generate_gemini import api_key

ROOT=Path(__file__).resolve().parents[1]
CHAPTERS=[
"An outcome has arrived. What is allowed to happen next? This capability answers that question using three supplied inputs: the admitted outcome, declared route authority, and current route state. Watch the comparison, then the authorization appear. The original evidence remains unchanged. This is permission, not execution. No scenario starts, and the route-state snapshot does not change.",
"First, identify the variant the outcome selected. In this illustrative example, outcome B matches a declared B slot. The comparison makes that match visible. The other variants do not become fallback choices. If an outcome selects a variant that the node does not declare, the result is rejection evidence. The resolver does not invent a default just to keep moving.",
"Next, look only at the routes declared for that exact variant. The route map arrives with the input. The highlighted line represents a resolved route, not a token traveling through the system. Missing route authority produces rejection evidence. Two selectable routes produce ambiguity. Neither ordering nor visual position is permission to pick one. The source authority determines the answer.",
"State is supplied, not secretly remembered. The snapshot records convergence products, completed fan-out members, and iterations already taken. Its governing identity matches the blueprint. The frame around the tablet represents immutability: every recorded value stays the same throughout this operation. If required state is absent from the request, resolution returns evidence of that absence instead of consulting hidden context.",
"A fan-out is a jointly required set. Here, the three member labels are illustrative. Authority declares A, B and C, but the candidate set contains only A and B. During comparison, the empty C slot remains visible. The outcome identifies a missing member. It never pretends the partial set is complete, and none of these members is executed by the resolver.",
"Convergence asks whether every required product is already present under the same governing identity. Our example has products A and B, while C is missing. The comparison does not make C arrive. The empty slot remains empty, and the outcome is pending. This is an informative result. The resolver has explained why the join cannot advance without manufacturing success.",
"A bounded return also needs explicit authority. The supplied snapshot records iterations already taken, and the declared authority fixes the bound. This example shows an exhausted bound. The comparison produces return rejection evidence. The printed loop remains stationary: no retry occurs and no counter increments. A different input may authorize a return, but this example cannot silently turn into that alternative.",
"Finally, the resolved evidence supports exactly one continuation. In this example, convergence remains pending. The continuation record preserves the authorization kind, selected invocation set, source routes, blueprint digest, and state digest. These chapters explain related responsibilities; they are not one asserted execution trace. The central distinction remains visible: authority determines what may happen next. A separate responsibility performs any authorized invocation."
]

def generate(pair):
    index,text=pair
    folder=ROOT/'samples/visual-pilot/audio'
    folder.mkdir(parents=True,exist_ok=True)
    payload={'contents':[{'parts':[{'text':'Read this exact narration in a calm, clear documentary voice, at approximately 135 words per minute. No introduction, no additions.\n'+text}]}],
             'generationConfig':{'responseModalities':['AUDIO'],'speechConfig':{'voiceConfig':{'prebuiltVoiceConfig':{'voiceName':'Kore'}}}}}
    raw=json.dumps(payload).encode(); identity=hashlib.sha256(raw).hexdigest()
    target=folder/f'{index:02}.wav'; receipt=folder/f'{index:02}.json'
    if target.exists() and receipt.exists() and json.loads(receipt.read_text()).get('requestDigest')==identity:
        return index
    request=urllib.request.Request('https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-tts:generateContent',data=raw,headers={'Content-Type':'application/json','x-goog-api-key':api_key()})
    with urllib.request.urlopen(request,timeout=180) as response: result=json.load(response)
    parts=result.get('candidates',[{}])[0].get('content',{}).get('parts',[])
    audio=next(p['inlineData'] for p in parts if p.get('inlineData',{}).get('mimeType','').startswith('audio/'))
    pcm=base64.b64decode(audio['data'])
    with wave.open(str(target),'wb') as output:
        output.setnchannels(1); output.setsampwidth(2); output.setframerate(24000); output.writeframes(pcm)
    receipt.write_text(json.dumps({'requestDigest':identity,'model':'gemini-2.5-flash-preview-tts','mimeType':audio['mimeType'],'duration':len(pcm)/48000,'transcript':text},indent=2))
    return index

if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--execute',action='store_true'); args=parser.parse_args()
    (ROOT/'samples/visual-pilot/narration.json').write_text(json.dumps(CHAPTERS,indent=2))
    if not args.execute: print('Prepared eight narration chapters; pass --execute to synthesize.')
    elif not api_key(): raise SystemExit('LOC_GEMINI_API_KEY unavailable')
    else:
        with ThreadPoolExecutor(max_workers=2) as pool:
            for index in pool.map(generate,enumerate(CHAPTERS)): print('NARRATED',index,flush=True)
