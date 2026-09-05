"""Local editorial demo: declared simulated failure -> compatible live speech -> verified WAV.
This exercises lab code, not admitted managed-capability execution.
"""
import argparse,base64,hashlib,json,time,urllib.request,wave
from pathlib import Path
from generate_gemini import api_key
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'samples/narration-continuity'
SCRIPT='Your story is ready to be heard. Every detail has a purpose. Every voice carries the story forward.'
VOICEOVER='''The cut is ready. The script is ready. Then the voice service stops responding.
One producer. Seven waiting jobs. And a narration track that will not play.
In this demonstration, SideFX's provider-continuity idea becomes visible.
Keep the creative request. Check the permitted alternatives. One cannot deliver audio. The next can.
The same script goes to the compatible provider. Real narration comes back.
But a response is only the beginning. Save the audio. Check the artifact. Keep the request, provider, and file connected by evidence.
Now the producer can listen, bring the voice into the cut, and continue the work.
The provider changed. The story stayed hers.'''
SHORT_VOICEOVER='''Her cut is ready, but the voice provider is not. Keep the script. Check the route. The first alternative cannot make audio. The next one can. Materialize the response, verify the file, and return the narration to the producer. The provider changed. The story stayed hers.'''
def digest(b):return hashlib.sha256(b).hexdigest()
def speech(text,name):
    payload={'contents':[{'parts':[{'text':'Read the following exact script with natural documentary pacing, approximately 145 words per minute. No introduction or added words.\n'+text}]}],
      'generationConfig':{'responseModalities':['AUDIO'],'speechConfig':{'voiceConfig':{'prebuiltVoiceConfig':{'voiceName':'Kore'}}}}}
    raw=json.dumps(payload).encode();request_digest=digest(raw)
    audio=OUT/f'{name}.wav';receipt=OUT/f'{name}.receipt.json'
    if audio.exists() and receipt.exists():
        r=json.loads(receipt.read_bytes())
        if r['requestDigest']==request_digest and digest(audio.read_bytes())==r['audioDigest']:return r
    req=urllib.request.Request('https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-tts:generateContent',data=raw,
      headers={'Content-Type':'application/json','x-goog-api-key':api_key()})
    start=time.monotonic()
    with urllib.request.urlopen(req,timeout=180) as response:result=json.load(response)
    parts=result['candidates'][0]['content']['parts']
    inline=next(p['inlineData'] for p in parts if p.get('inlineData',{}).get('mimeType','').startswith('audio/'))
    if 'rate=24000' not in inline['mimeType']:raise ValueError('UNEXPECTED_AUDIO_FORMAT')
    pcm=base64.b64decode(inline['data'],validate=True)
    if not pcm or len(pcm)%2:raise ValueError('UNUSABLE_AUDIO_PAYLOAD')
    with wave.open(str(audio),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(24000);w.writeframes(pcm)
    r={'provider':'Gemini','model':'gemini-2.5-flash-preview-tts','voice':'Kore','script':text,'requestDigest':request_digest,
       'audioDigest':digest(audio.read_bytes()),'audioFile':audio.name,'durationSeconds':len(pcm)/48000,
       'elapsedSeconds':round(time.monotonic()-start,3),'status':'MATERIALIZED','execution':'LIVE_PROVIDER_IN_LOCAL_LAB'}
    receipt.write_text(json.dumps(r,indent=2));return r
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--execute',action='store_true');args=parser.parse_args()
    OUT.mkdir(parents=True,exist_ok=True)
    if not args.execute:print('Two bounded speech requests prepared; --execute runs the local demo.');return
    if not api_key():raise ValueError('LOC_GEMINI_API_KEY_UNAVAILABLE')
    original=digest(SCRIPT.encode())
    candidates=[{'id':'A','available':False,'modalities':['audio'],'mode':'SIMULATED_FAILURE'},
                {'id':'B','available':True,'modalities':['text'],'mode':'LOCAL_DECLARED_CANDIDATE'},
                {'id':'C','available':True,'modalities':['audio'],'mode':'LIVE_GEMINI'},
                {'id':'D','available':True,'modalities':['audio'],'mode':'STANDBY'}]
    events=[];selected=None
    for candidate in candidates:
        status=('NOT_INVOKED' if selected else 'UNAVAILABLE' if not candidate['available'] else
                'INELIGIBLE' if 'audio' not in candidate['modalities'] else 'SELECTED')
        if status=='SELECTED':selected=candidate['id']
        events.append({'step':candidate['id'],'status':status,'mode':candidate['mode'],'declaredModalities':candidate['modalities']})
    if selected!='C':raise ValueError('DEMO_HAS_NO_SUPPORTED_LIVE_AUDIO_BINDING')
    queue=[{'jobId':f'narration-{i+1:02}','status':'PENDING'} for i in range(7)]
    (OUT/'queue-before.json').write_text(json.dumps(queue,indent=2))
    before=sum(j['status']=='PENDING' for j in queue)
    asset=speech(SCRIPT,'finished-narration')
    assert digest(SCRIPT.encode())==original
    queue[0].update(status='COMPLETED',assetDigest=asset['audioDigest'],audioFile=asset['audioFile'])
    (OUT/'queue-after.json').write_text(json.dumps(queue,indent=2))
    receipt={'demoId':'narration-continuity-film.v1','kind':'LOCAL_EDITORIAL_COMPOSITION',
             'notManagedCapsuleExecution':True,'requestDigestBefore':original,'requestDigestAfter':digest(SCRIPT.encode()),
             'providers':events,'asset':asset,'queueBefore':before,'queueAfter':sum(j['status']=='PENDING' for j in queue),
             'queueMeaning':'Seven local illustrative jobs; this run completes one narration asset, not seven jobs.',
             'outcome':'NARRATION_MATERIALIZED_AND_HASH_VERIFIED'}
    (OUT/'demo.receipt.json').write_text(json.dumps(receipt,indent=2))
    print('DEMO AUDIO VERIFIED',round(asset['durationSeconds'],2),flush=True)
    narrator=speech(VOICEOVER,'film-voiceover')
    print('FILM VOICEOVER READY',round(narrator['durationSeconds'],2),flush=True)
    short_narrator=speech(SHORT_VOICEOVER,'short-voiceover')
    print('SHORT VOICEOVER READY',round(short_narrator['durationSeconds'],2),flush=True)
if __name__=='__main__':main()
