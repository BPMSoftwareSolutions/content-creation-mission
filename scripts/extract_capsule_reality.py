"""Read verified capsules into evidence packages. Never execute capsule content."""
import base64, hashlib, json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def sha(b): return hashlib.sha256(b).hexdigest()
def write(p, value):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(value, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
def walk(value, pointer=''):
    yield pointer, value
    if isinstance(value, dict):
        for k,v in value.items(): yield from walk(v, pointer+'/'+k.replace('~','~0').replace('/','~1'))
    elif isinstance(value, list):
        for i,v in enumerate(value): yield from walk(v, pointer+'/'+str(i))

def extract():
    frozen=json.loads((ROOT/'data/source-manifest.json').read_text(encoding='utf-8'))
    estate=Path(frozen['sourceRoot'])/'capsules'
    manifest_bytes=(estate/'capsule-estate.manifest.json').read_bytes()
    if sha(manifest_bytes)!=frozen['manifestDigest']: raise ValueError('ESTATE_GENERATION_CHANGED')
    manifest=json.loads(manifest_bytes)
    inventory=json.loads((ROOT/'inventories/scenario-inventory.json').read_text(encoding='utf-8'))
    groups={}
    for s in inventory: groups.setdefault(s['capabilityId'],[]).append(s)
    index=[]; coverage=Counter()
    for item in manifest['capsules']:
        cid=item['capabilityId']; path=(estate/item['file']).resolve()
        if not path.is_relative_to(estate.resolve()): raise ValueError('CAPSULE_PATH_ESCAPE')
        raw=path.read_bytes()
        if 'sha256:'+sha(raw)!=item['capsuleDigest']: raise ValueError('CAPSULE_DIGEST_MISMATCH')
        c=json.loads(raw); entries=[]; docs={}
        for e in c['entries']:
            b=base64.b64decode(e['entryBytesBase64'],validate=True)
            if 'sha256:'+sha(b)!=e['entryDigest']: raise ValueError('ENTRY_DIGEST_MISMATCH')
            # Store bytes as inert base64 JSON, never materialize executable entries.
            snapshot=f"data/capsule-evidence/entries/{sha(b)}-{sha((cid+e['entryId']).encode())[:16]}.json"
            write(ROOT/snapshot,e)
            ref={'entryId':e['entryId'],'entryRef':e['entryRef'],'entryDigest':e['entryDigest'],
                 'snapshot':snapshot}
            entries.append(ref)
            try: docs[e['entryId']]=(json.loads(b),ref)
            except (ValueError,UnicodeError): pass
        plans=[(d,r) for d,r in docs.values() if isinstance(d,dict) and 'executionEmbodimentPlanType' in d]
        cap={'capabilityId':cid,'capsuleDigest':item['capsuleDigest'],'estateManifestDigest':sha(manifest_bytes),
             'dependencies':c.get('declaredDependencies',[]),'runtimeBindings':c.get('runtimeBindings',[]),
             'externalToolRoots':c.get('externalToolRoots',[]),'entries':entries}
        write(ROOT/'data/capsule-evidence/capabilities'/f'{cid}.json',cap)
        for s in groups.get(cid,[]):
            sid=s['scenarioId']; evidence={k:[] for k in ('execution','mechanics','providers','contracts','topology','fixtures','receipts')}
            def add(layer,value,ref,pointer):
                evidence[layer].append({'source':{**ref,'pointer':pointer},'value':value})
            for plan,ref in plans:
                graph=plan.get('canonicalGraph',{})
                cells=graph.get('cells',[])
                selected_cells={'cell:scenario:'+sid}
                while True:
                    expanded=selected_cells | {n['cellId'] for n in cells if n.get('parentCellId') in selected_cells}
                    if expanded==selected_cells: break
                    selected_cells=expanded
                for i,n in enumerate(cells):
                    if n.get('cellId') in selected_cells:
                        add('mechanics' if n.get('altitude')=='mechanic' else 'execution',n,ref,f'/canonicalGraph/cells/{i}')
                for i,b in enumerate(plan.get('realizationOverlay',{}).get('providerBindings',[])):
                    if b.get('cellId') in selected_cells: add('providers',b,ref,f'/realizationOverlay/providerBindings/{i}')
                for i,e in enumerate(graph.get('edges',[])):
                    if any(v in selected_cells for _,v in walk(e) if isinstance(v,str)): add('topology',e,ref,f'/canonicalGraph/edges/{i}')
                for field in ('executionPolicy','effectPolicy','bindingAuthorities','contractCatalog'):
                    if field in plan: add('contracts' if field=='contractCatalog' else 'topology',plan[field],ref,'/'+field)
                nodes=plan.get('nodes',[]); selected={sid}; pending=[sid]
                # Follow exact invoke-scenario identities, not lexical similarity.
                while pending:
                    current=pending.pop()
                    for n in nodes:
                        if n.get('scenario',{}).get('scenarioId',n.get('nodeId'))!=current: continue
                        for op in n.get('operations',[]):
                            target=op.get('scenarioNodeId')
                            if target and target not in selected: selected.add(target);pending.append(target)
                binding_ids=set()
                for i,n in enumerate(nodes):
                    if n.get('scenario',{}).get('scenarioId',n.get('nodeId')) in selected:
                        add('execution',n,ref,f'/nodes/{i}')
                        binding_ids.update(op['mechanicBindingId'] for op in n.get('operations',[]) if 'mechanicBindingId' in op)
                for i,b in enumerate(plan.get('mechanicBindings',[])):
                    if b.get('bindingId') in binding_ids or b.get('mechanicType')=='contract-admission':
                        add('mechanics',b,ref,f'/mechanicBindings/{i}')
                        add('providers',{k:b[k] for k in ('bindingId','providerCapabilityId','provider','implementationRef') if k in b},ref,f'/mechanicBindings/{i}')
                if 'compositionPolicy' in plan: add('topology',plan['compositionPolicy'],ref,'/compositionPolicy')
            for eid,(d,ref) in docs.items():
                if eid.startswith('contracts/') and eid.endswith('.schema.json'): add('contracts',d,ref,'')
                if eid=='blueprint.authority.json':
                    for i,n in enumerate(d.get('nodes',[])):
                        if n.get('nodeId')==sid: add('topology',n,ref,f'/nodes/{i}')
                    for i,e in enumerate(d.get('edges',[])):
                        if any(v==sid for _,v in walk(e) if isinstance(v,str)): add('topology',e,ref,f'/edges/{i}')
                if eid=='fixtures.authority.json':
                    # Capability-scoped fixtures remain explicitly scoped; not asserted node runs.
                    for i,f in enumerate(d.get('fixtures',[])):
                        add('fixtures',{'scope':'capability','executionStatus':'DECLARED_EXPECTATION_NOT_EXECUTED','fixture':f},ref,f'/fixtures/{i}')
                if 'receipt' in eid or 'conformance' in eid: add('receipts',d,ref,'')
            findings=[{'code':'MISSING_'+k.upper(),'detail':'No structurally resolved evidence; requires inspection.'}
                      for k in ('execution','mechanics','providers','contracts','fixtures') if not evidence[k]]
            package={'packageVersion':'scenario-visual-evidence.v1','key':s['key'],
                     'source':{'estateManifestDigest':sha(manifest_bytes),'capsuleDigest':item['capsuleDigest']},
                     'scenarioSurface':s,'evidence':evidence,
                     'providerQualification':'Bindings are declared suppliers, not proof of live availability. Simulation requires explicit fixture/provider evidence.',
                     'inputReality':{'sourceSteps':s['input'],'contracts':evidence['contracts'],'actors':s['actors'],
                                     'humanSituation':'Requires editorial interpretation from the cited input contracts.'},
                     'eventExecutionReality':{'responsibilities':evidence['execution'],'mechanics':evidence['mechanics'],
                                              'providers':evidence['providers'],'topology':evidence['topology'],
                                              'sideEffects':'Inspect exact mechanic configuration and effect policy; no inference from capability name.'},
                     'outcomeReality':{'sourceSteps':s['outcome'],'evidence':evidence['fixtures'],
                                       'observedExecution':False},
                     'visualDirection':{'status':'CANDIDATE_REQUIRES_SEMANTIC_REVIEW',
                         'input':'Establish the human situation and supplied artifacts described by the input contracts.',
                         'event':'Expose each cited responsibility and its concrete transformation, validation, or provider interaction.',
                         'outcome':'Show only the resulting product and disposition supported by the selected fixture and contracts.',
                         'continuity':['Preserve source identities','Keep declared inputs distinct from derived working products'],
                         'mechanicalOverlays':evidence['providers']+evidence['topology'],
                         'unresolved':['Specific human environment','Fixture selection','Mechanical-to-visible mapping','Audience legibility']},
                     'animationBeats':[{'ordinal':i,'status':'EXECUTION_FACT_REQUIRES_VISUAL_DIRECTION',
                         'executionFact':x['value'],'sourceRefs':[x['source']],
                         'visibleChange':None} for i,x in enumerate(evidence['execution'])],
                     'disposition':'MECHANICS_EXTRACTED_REQUIRES_DIRECTION' if not findings else 'MECHANICS_UNRESOLVED',
                     'findings':findings,'reviewRequired':True}
            target=f'outputs/scenario-visual-evidence/{cid}/{sid}.json'
            write(ROOT/target,package)
            index.append({'key':s['key'],'path':target,'disposition':package['disposition'],
                          'evidenceCounts':{k:len(v) for k,v in evidence.items()},'findings':findings})
            coverage[package['disposition']]+=1
    if (estate/'capsule-estate.manifest.json').read_bytes()!=manifest_bytes: raise ValueError('ESTATE_CHANGED_DURING_READ')
    write(ROOT/'outputs/scenario-visual-evidence-index.json',index)
    write(ROOT/'evaluations/capsule-reality-coverage.json',{'estateManifestDigest':sha(manifest_bytes),
          'capabilities':len(manifest['capsules']),'scenarios':len(index),'dispositions':dict(coverage),
          'note':'Extraction is not semantic review, fixture execution, or visual acceptance.'})
    print(json.dumps(dict(coverage)))

if __name__=='__main__': extract()
