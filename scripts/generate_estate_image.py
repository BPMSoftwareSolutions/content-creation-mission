"""Nano Banana entity-image transport for SQL-backed estate jobs.

Uses the content lab's existing Gemini credential resolver and provider protocol.
The caller commits the request before invoking this transport and commits returned
original bytes to SQL before completing the job. No automatic model substitution.
"""
import argparse,base64,hashlib,io,json,sys,time,urllib.request,urllib.error
from pathlib import Path
from PIL import Image
from generate_gemini import api_key, ROOT

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--job',required=True)
    parser.add_argument('--request',type=Path,required=True)
    args=parser.parse_args()
    if len(args.job)!=64 or any(c not in '0123456789abcdef' for c in args.job):raise ValueError('INVALID_JOB_ID')
    job=json.loads(args.request.read_text(encoding='utf-8'))
    if job['model']!='gemini-3-pro-image':raise ValueError('NANO_BANANA_MODEL_REQUIRED')
    key=api_key()
    if not key:raise ValueError('GEMINI_CREDENTIAL_UNAVAILABLE')
    folder=ROOT/'outputs/estate-generated'/args.job
    folder.mkdir(parents=True,exist_ok=True)
    receipt_path=folder/'receipt.json'
    if receipt_path.exists():
        prior=json.loads(receipt_path.read_text(encoding='utf-8'))
        if prior['status']=='GENERATED':
            data=(ROOT/prior['image']).read_bytes()
            if hashlib.sha256(data).hexdigest()!=prior['imageSha256']:raise ValueError('GENERATED_BYTES_CHANGED')
            print(json.dumps(prior));return
        if not (prior.get('status')=='HTTP_FAILED' and prior.get('httpStatus') in (429,500,502,503,504) and prior.get('retryAuthorized')):
            raise ValueError('PRIOR_REQUEST_REQUIRES_RECONCILIATION')
    request={'contents':[{'parts':[{'text':job['prompt']}]}], 'generationConfig':{'responseModalities':['TEXT','IMAGE'],'maxOutputTokens':8192,'imageConfig':{'aspectRatio':'16:9','imageSize':'1K'}}}
    for ref in job.get('references',[]):
        p=(ROOT/ref['path']).resolve()
        if not p.is_relative_to(ROOT):raise ValueError('REFERENCE_PATH_ESCAPE')
        data=p.read_bytes()
        if hashlib.sha256(data).hexdigest()!=ref['sha256']:raise ValueError('STALE_STYLE_REFERENCE')
        request['contents'][0]['parts'].append({'inlineData':{'mimeType':ref['mediaType'],'data':base64.b64encode(data).decode()}})
    payload=json.dumps(request).encode()
    receipt={'jobId':args.job,'provider':'Gemini','model':job['model'],'requestSha256':hashlib.sha256(payload).hexdigest(),'status':'REQUEST_IN_FLIGHT','semanticReview':'REQUIRED'}
    save=lambda r:receipt_path.write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8')
    save(receipt)
    req=urllib.request.Request('https://generativelanguage.googleapis.com/v1beta/models/'+job['model']+':generateContent',data=payload,headers={'Content-Type':'application/json','x-goog-api-key':key})
    for attempt in range(4):
        receipt['transportAttempt']=attempt+1
        save(receipt)
        try:
            with urllib.request.urlopen(req,timeout=240) as response:result=json.load(response)
            break
        except urllib.error.HTTPError as e:
            failed={**receipt,'status':'HTTP_FAILED','httpStatus':e.code};save(failed)
            (folder/('transport-attempt-'+str(attempt+1)+'.json')).write_text(json.dumps(failed),encoding='utf-8')
            if e.code not in (429,500,502,503,504) or attempt==3:raise ValueError('GEMINI_HTTP_'+str(e.code)) from None
            time.sleep(min(2**(attempt+1),8))
        except (TimeoutError,urllib.error.URLError):
            save({**receipt,'status':'NETWORK_UNCERTAIN'});raise ValueError('NETWORK_UNCERTAIN') from None
    images=[p['inlineData'] for c in result.get('candidates',[]) for p in c.get('content',{}).get('parts',[]) if p.get('inlineData',{}).get('mimeType','').startswith('image/') and not p.get('thought')]
    if len(images)!=1:
        save({**receipt,'status':'IMAGE_CARDINALITY','count':len(images)});raise ValueError('IMAGE_CARDINALITY')
    data=base64.b64decode(images[0]['data'],validate=True)
    im=Image.open(io.BytesIO(data));im.load()
    ext={'PNG':'png','JPEG':'jpg','WEBP':'webp'}.get(im.format)
    if not ext:raise ValueError('UNSUPPORTED_IMAGE_FORMAT')
    out=folder/('original.'+ext);out.write_bytes(data)
    receipt={**receipt,'status':'GENERATED','image':out.relative_to(ROOT).as_posix(),'imageSha256':hashlib.sha256(data).hexdigest(),'mediaType':images[0]['mimeType'],'width':im.width,'height':im.height,'usage':result.get('usageMetadata')}
    save(receipt);print(json.dumps(receipt))

if __name__=='__main__':
    try:main()
    except Exception as e:
        print(str(e) if isinstance(e,ValueError) else 'ESTATE_IMAGE_TRANSPORT_FAILED',file=sys.stderr);sys.exit(1)
