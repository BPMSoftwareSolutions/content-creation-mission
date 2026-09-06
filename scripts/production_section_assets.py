"""Gemini Nano Banana adapter for source-bound section art-direction records.

Extends the local editorial image workflow. No managed execution is claimed.
"""
import argparse,base64,json,urllib.request,urllib.error,concurrent.futures,hashlib
from pathlib import Path
from production_store import JsonProductionStore,read,write,artifact_digest,digest
from generate_gemini import api_key

def generate(store,revision,scene,direction):
    plan=next(p for p in direction['sections'] if p['key']==scene['sectionVisualId'])
    for key in ('format','purpose','camera','assetPrompt','composition','motion'):
        if not plan.get(key):raise ValueError('Section direction incomplete: '+key)
    image=store.resolve(scene['visualAssetRef']);receipt=image.with_suffix('.receipt.json')
    image.parent.mkdir(parents=True,exist_ok=True)
    prompt='\n'.join([direction['imageConstraints'],'CAMERA: '+plan['camera'],plan['assetPrompt'],
        'FINAL OUTPUT: The unlettered physical scene only. Do not infer or add a layout, annotation, diagram, UI, writing, display contents, data or graphics. All such layers will be added separately after this image is generated.'])
    parts=[{'text':prompt}];reference_digest=None
    if plan.get('reference'):
        reference=store.resolve(plan['reference']);reference_digest=artifact_digest(reference)
        parts.append({'inlineData':{'mimeType':'image/png' if reference.suffix.lower()=='.png' else 'image/jpeg','data':base64.b64encode(reference.read_bytes()).decode()}})
    provider=direction['provider'];model=provider['model']
    if not all(c.isalnum() or c in '-._' for c in model):raise ValueError('Invalid model id')
    payload={'contents':[{'role':'user','parts':parts}],'generationConfig':{'responseModalities':['TEXT','IMAGE'],
              'imageConfig':{'aspectRatio':provider['aspectRatio'],'imageSize':provider['imageSize']}}}
    request_digest=digest({'model':model,'request':payload})
    if image.exists() and receipt.exists():
        previous=read(receipt)
        if previous['requestDigest']==request_digest and previous.get('imageDigest')==artifact_digest(image):
            print('CACHED SECTION',plan['key'],flush=True);return previous
        import shutil
        rejected=image.parent/'superseded';rejected.mkdir(exist_ok=True)
        shutil.copy2(image,rejected/(artifact_digest(image)+'.png'))
        shutil.copy2(receipt,rejected/(artifact_digest(image)+'.receipt.json'))
    request=urllib.request.Request('https://generativelanguage.googleapis.com/v1beta/models/'+model+':generateContent',
        data=json.dumps(payload).encode(),headers={'Content-Type':'application/json','x-goog-api-key':api_key()})
    try:
        with urllib.request.urlopen(request,timeout=180) as stream:response=json.load(stream)
    except urllib.error.HTTPError as exc:
        write(receipt,{'requestDigest':request_digest,'status':'HTTP_FAILED','httpStatus':exc.code,'sectionId':plan['key']})
        raise RuntimeError(f'Section {plan["key"]}: Gemini HTTP {exc.code}; credentials omitted.') from None
    except (TimeoutError,urllib.error.URLError):
        raise RuntimeError(f'Section {plan["key"]}: network outcome uncertain; no automatic retry.') from None
    inline=next((p['inlineData'] for c in response.get('candidates',[]) for p in c.get('content',{}).get('parts',[])
                 if p.get('inlineData',{}).get('mimeType','').startswith('image/')),None)
    if inline is None:raise RuntimeError('No image returned for '+plan['key'])
    from PIL import Image
    import io
    raw=base64.b64decode(inline['data'],validate=True)
    with Image.open(io.BytesIO(raw)) as decoded:decoded.convert('RGB').save(image)
    result={'sectionId':plan['key'],'visualFormatType':plan['format'],'requestDigest':request_digest,
            'provider':provider['name'],'model':model,'imageDigest':artifact_digest(image),
            'path':scene['visualAssetRef'],'prompt':prompt,'referenceDigest':reference_digest,
            'sourceSceneDigest':digest(scene['narration']),'directionDigest':digest(plan),'semanticReview':'REQUIRED'}
    write(receipt,result);print('GENERATED SECTION',plan['key'],plan['format'],flush=True);return result

def main():
    p=argparse.ArgumentParser();p.add_argument('--store',required=True);p.add_argument('--section',nargs='+');a=p.parse_args()
    store=JsonProductionStore(a.store);jobs=[]
    for r in store.revisions():
        direction=read(store.resolve(r['sectionDirectionRef']))
        for scene in r['scenes']:
            if not a.section or scene['sectionVisualId'] in a.section:jobs.append((store,r,scene,direction))
    if not api_key():raise SystemExit('Gemini API key unavailable in existing environment.')
    with concurrent.futures.ThreadPoolExecutor(max_workers=direction['provider']['maximumConcurrentRequests']) as pool:
        futures=[pool.submit(generate,*job) for job in jobs]
        results=[];errors=[]
        for future in concurrent.futures.as_completed(futures):
            try:results.append(future.result())
            except Exception as exc:errors.append(str(exc));print('ASSET ERROR',str(exc),flush=True)
    if errors:raise SystemExit('\n'.join(errors))
    print('SECTION ASSETS READY',len(results),flush=True)
if __name__=='__main__':main()
