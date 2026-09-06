"""Validate data-driven content boundaries and replay pinned expression checks.

This verifies stored fixtures and artifacts. It never calls a managed runtime.
"""
import argparse,base64,hashlib
from production_store import JsonProductionStore,ROOT,read,write,artifact_digest

def evaluate(e,inp):
    op=e['op']
    if op=='literal':return e['value']
    if op=='path':
        if e['from']!='input':raise ValueError('Unsupported expression source')
        value=inp
        for key in e['path'].split('.') if e['path'] else []:value=value[key]
        return value
    if op=='equals':return evaluate(e['left'],inp)==evaluate(e['right'],inp)
    if op=='if':return evaluate(e['then'] if evaluate(e['when'],inp) else e['else'],inp)
    if op=='object':return {k:evaluate(v,inp) for k,v in e['fields'].items()}
    if op=='merge':return {k:v for item in e['values'] for k,v in evaluate(item,inp).items()}
    raise ValueError('Unsupported expression operator')

def verify(store):
    results=[]
    for revision in store.revisions():
        record=revision['evidenceRecord'];checks=[]
        if 'sourceDigest' in record:
            wrapper=store.resolve(record['sourceArtifactRef'])
            raw=base64.b64decode(read(wrapper)['entryBytesBase64'],validate=True)
            assert hashlib.sha256(raw).hexdigest()==record['sourceDigest']
            import json
            expression=json.loads(raw)
            for component in record['sourcePointer'].strip('/').split('/'):
                expression=expression[int(component)] if isinstance(expression,list) else expression[component]
            assert expression==record['expression']
            for test in record['classificationTests']:
                actual=evaluate(expression,test['input'])['adjudicationOutcome']
                assert actual==test['returnedLabel'];checks.append({'input':test['input'],'observed':actual})
        if 'simulation' in record:
            simulation=record['simulation'];grant=simulation['grant']
            # Replay the narrow bound-read model from stored request/grant records.
            # The final unavailable-check case is explicitly marked in fixture data.
            for observed in simulation['observations']:
                matched=observed.get('authorizationAvailable',True) and all(observed[k]==grant[k] for k in ('action','object','arguments'))
                assert observed['decision']==('PERMIT' if matched else 'HOLD')
                assert observed['inspectionCalls']==int(matched)
                if matched:
                    report=observed['report'];candidate=simulation['finalCandidates'][observed['object']]
                    assert all(candidate[k] for k in report['passed'])
                    assert all(not candidate[k] for k in report['missing'])
                    assert candidate['published']==report['published']
                checks.append({'request':{k:observed[k] for k in ('action','object','arguments')},'replayedDecision':observed['decision']})
        # Every visual reveal is anchored in its narration, and every asset stays in scope.
        for scene in revision['scenes']:
            for state in scene['states']:
                assert not state['trigger'] or state['trigger'].lower() in scene['narration'].lower()
            if scene.get('photo'):assert store.resolve(scene['photo']).is_file()
            if revision.get('sectionDirectionRef'):
                from production_composition import section_spec,svg_composition
                plan,spec=section_spec(store,revision,scene)
                source=store.resolve(scene['visualAssetRef']);sha=artifact_digest(source)
                assert read(source.with_suffix('.receipt.json'))['imageDigest']==sha
                reviews=read(store.resolve(revision['sectionAssetReviewRef']))['sections']
                matches=[r for r in reviews if r['sectionId']==scene['sectionVisualId']]
                assert len(matches)==1 and matches[0]['imageDigest']==sha and matches[0]['status']=='ACCEPTED_FOR_COMPOSITING'
                for i,state in enumerate(scene['states']):
                    svg_composition(revision,scene,state,i,plan,spec,store.profile(revision)['visual'])
                checks.append({'sectionId':scene['sectionVisualId'],'visualFormat':plan['format'],'reviewedImageDigest':sha})
        results.append(dict(revisionId=revision['revisionId'],inputRevisionDigest=store.input_digest(revision),
            checks=checks,scope='Schema, pinned source expression, and authored local model only. Not live platform or learning validation.'))
    return results

def main():
    p=argparse.ArgumentParser();p.add_argument('--store',required=True);p.add_argument('--output',required=True);a=p.parse_args()
    results=verify(JsonProductionStore(a.store));write(a.output,results)
    print('Verified',len(results),'revision records; no live effects invoked.')
if __name__=='__main__':main()
