"""Frozen local capsule testimony -> SCL. No queries or mutations of the harness."""
import argparse
import base64
import json
from collections import Counter
from pathlib import Path

from content_lab import parse_feature
from infographic_contract import ROOT, digest, read, write
from scl import validate_graph, emit, graph_hash, need

NATIVE_EDGES = {'sequence', 'selection', 'return', 'recurrence', 'cancellation', 'altitude_descent', 'bounded_return', 'transition'}
PLAN_TYPES = {f'consumer-execution-embodiment-plan.v{i}' for i in (1, 2, 3)}


def reveal(capability_id):
    need(capability_id and all(c.isalnum() or c in '-_.' for c in capability_id) and '..' not in capability_id, 'INVALID_CAPABILITY_ID')
    manifest = read('data/source-manifest.json')
    cp = f'data/capsule-evidence/capabilities/{capability_id}.json'; cap = read(cp)
    frozen = next(s for s in manifest['sources'] if Path(s['snapshot']).stem == capability_id)
    need(cap['capabilityId'] == capability_id and cap['capsuleDigest'] == frozen['capsuleDigest']
         and cap['estateManifestDigest'] == manifest['manifestDigest'], 'CAPSULE_GENERATION_MISMATCH')
    entries = {e['entryRef']: e for e in cap['entries']}
    need(len(entries) == len(cap['entries']), 'AMBIGUOUS_ENTRY_REF')
    files, sources, documents = {}, [], {}
    def source(path, pointer='', encoding='json', label='Frozen capsule testimony'):
        if path not in files: files[path] = digest(ROOT/path)
        identity = f'src-{len(sources):05}'
        sources.append(dict(id=identity, path=path, sha256=files[path], pointer=pointer,
                            kind='DECLARED', label=label, encoding=encoding))
        return identity
    def entry(ref):
        e = entries[ref]; path = e['snapshot']
        need((ROOT/path).resolve().is_relative_to(ROOT), 'ENTRY_PATH_ESCAPE')
        if ref not in documents:
            envelope = read(path)
            need(all(envelope[k] == e[k] for k in ('entryId', 'entryRef', 'entryDigest')), 'ENTRY_IDENTITY_MISMATCH')
            body = base64.b64decode(envelope['entryBytesBase64'], validate=True)
            import hashlib
            need('sha256:' + hashlib.sha256(body).hexdigest() == e['entryDigest'], 'ENTRY_DIGEST_MISMATCH')
            documents[ref] = body
        return documents[ref], path
    cs = source(cp, label='Frozen capability snapshot')
    authority = next(e for e in cap['entries'] if e['entryId'] == 'capability.authority.json')
    authority_raw, _ = entry(authority['entryRef']); authority_doc = json.loads(authority_raw)
    feature_raw, feature_path = entry(frozen['featureEntry'])
    need(entries[frozen['featureEntry']]['entryDigest'] == frozen['featureDigest'], 'FEATURE_DIGEST_MISMATCH')
    feature = parse_feature(feature_raw.decode('utf-8-sig'), capability_id, frozen, cap['dependencies'], authority_doc.get('userStory', {}).get('actor'))
    inventory = {s['scenarioId']: s for s in feature}
    need(len(inventory) == len(feature), 'DUPLICATE_SCENARIO_ID')
    inventory_path = 'inventories/scenario-inventory.json'
    stored_inventory = {s['scenarioId']:(i,s) for i,s in enumerate(read(inventory_path)) if s['capabilityId']==capability_id}
    need(set(stored_inventory)==set(inventory),'INVENTORY_SCENARIO_DRIFT')
    for sid, s in inventory.items():
        stored=stored_inventory[sid][1]
        need(all(s[k]==stored[k] for k in ('input','event','outcome','tags','scenarioName')),'INVENTORY_MEANING_DRIFT:'+sid)
    g = dict(version='sidefx-circuit.v0.1', id=capability_id, title=feature[0]['capabilityName'][:120],
             promise=authority_doc.get('experience') or feature[0]['notes'] or feature[0]['capabilityName'],
             status='SOURCE_REVEAL', sourceGeneration=manifest['manifestDigest'], sources=sources,
             capabilities=[], scenarios=[], nodes=[], junctions=[], edges=[], providers=[], meanings=[], records=[], findings=[], trace=[])
    if not isinstance(g['promise'], str): g['promise'] = json.dumps(g['promise'], ensure_ascii=False)
    def finding(code, subject, detail, closure): g['findings'].append(dict(code=code, subject=subject, detail=detail, closure=closure))
    def record(kind, typ, path, pointer, scopes=(), native_id=None, parent=None):
        sid = source(path, pointer, 'capsule-entry', f'{kind} / {typ}')
        g['records'].append(dict(id=f'record-{len(g["records"]):05}', kind=kind, nativeType=typ, sourceRef=sid,
                                 scenarioIds=list(scopes), nativeId=native_id, parentId=parent))
        return sid
    for e in cap['entries']:
        if e['entryId'] == 'blueprint.authority.json':
            raw, path = entry(e['entryRef']); blueprint = json.loads(raw)
            need(blueprint.get('capability', {}).get('capabilityId') == capability_id, 'BLUEPRINT_CAPABILITY_MISMATCH')
            node_ids = {n['nodeId'] for n in blueprint.get('nodes', [])}
            need(len(node_ids) == len(blueprint.get('nodes', [])), 'DUPLICATE_BLUEPRINT_NODE')
            unresolved=sorted({endpoint for edge in blueprint.get('edges', []) for endpoint in (edge['from'],edge['to']) if endpoint not in node_ids})
            if unresolved:
                finding('BLUEPRINT_UNRESOLVED_ENDPOINTS', capability_id,
                    'Stored blueprint routes reference undeclared nodes: '+', '.join(unresolved),
                    'Resolve these exact endpoints through the governed blueprint boundary. Do not fabricate junctions in the infographic.')
            if blueprint.get('admissionState'):
                finding('BLUEPRINT_DECLARED_ADMISSION_STATE', capability_id, blueprint['admissionState'],
                    'Respect the stored blueprint admission state; capsule membership alone does not admit this candidate blueprint.')
            record('blueprint', blueprint.get('carrierVersion', 'UNKNOWN'), path, '', native_id=blueprint.get('blueprintAuthority', {}).get('blueprintId'))
            finding('BLUEPRINT_VISUAL_PROFILE_OPEN', capability_id,
                'The separate canonical blueprint is retained exactly, including topology, semantic progress and observability. It is not conflated with the runtime graph.',
                'Qualify a visual profile for the blueprint carrier before projecting its state and responsibility nodes as execution flow.')
    plan_refs = sorted({b['planEntryRef'] for b in cap['runtimeBindings']})
    plans = []
    for ref in plan_refs:
        raw, path = entry(ref); plan = json.loads(raw)
        need(plan.get('capabilityId') == capability_id, 'PLAN_CAPABILITY_MISMATCH')
        typ = plan.get('executionEmbodimentPlanType')
        if typ not in PLAN_TYPES:
            finding('UNKNOWN_PLAN_PROFILE', capability_id, str(typ), 'Add and prove an adapter for this exact version.'); continue
        plans.append((plan, path))
    need(len(plans) <= 1, 'MULTIPLE_TARGET_PLANS_NEED_SELECTION')
    scenario_nodes = {}; native_count = 0
    for plan, path in plans:
        record('policy', plan['executionEmbodimentPlanType'], path, '')
        for i, n in enumerate(plan.get('nodes', [])):
            sid = n.get('scenario', {}).get('scenarioId', n.get('nodeId'))
            scenario_nodes[sid] = (n['scenario'], path, f'/nodes/{i}/scenario')
            for j, op in enumerate(n.get('operations', [])):
                typ = op.get('kind') or ('invoke-port' if plan['executionEmbodimentPlanType'].endswith('.v1') and 'mechanicBindingId' in op else 'UNKNOWN')
                record('operation', typ, path, f'/nodes/{i}/operations/{j}', [sid] if sid in inventory else [], op.get('operationId'))
            if n.get('transition'): record('route', 'legacy-transition', path, f'/nodes/{i}/transition', [sid] if sid in inventory else [])
        for i, b in enumerate(plan.get('mechanicBindings', [])):
            scope = [n['scenario']['scenarioId'] for n in plan['nodes'] if any(o.get('mechanicBindingId') == b['bindingId'] for o in n['operations'])]
            if b.get('mechanicType') == 'contract-admission': scope = list(inventory)
            record('mechanic', b['mechanicType'], path, f'/mechanicBindings/{i}', [s for s in scope if s in inventory], b['bindingId'])
        native = plan.get('canonicalGraph')
        if native:
            native_count = len(native['cells']); cells = {c['cellId']: c for c in native['cells']}
            need(len(cells) == len(native['cells']), 'DUPLICATE_NATIVE_CELL')
            roots = {c['cellId']: c['cellId'].removeprefix('cell:scenario:') for c in native['cells'] if c['altitude'] == 'scenario'}
            def scope(cell):
                seen = set()
                while cell in cells and cell not in seen:
                    if cell in roots: return [roots[cell]] if roots[cell] in inventory else []
                    seen.add(cell); cell = cells[cell].get('parentCellId')
                need(cell not in seen, 'NATIVE_CONTAINMENT_CYCLE')
                return []
            for i, c in enumerate(native['cells']):
                scopes = scope(c['cellId'])
                record('cell', c['execution']['kind'], path, f'/canonicalGraph/cells/{i}', scopes, c['cellId'], c.get('parentCellId'))
                if c['altitude'] == 'scenario':
                    sid = roots[c['cellId']]
                    n = dict(input={'inputId':c['input']['portId'],'contract':{'contractId':c['input']['contractId']}},
                             event={'eventId':sid,'executionAuthorityId':c['execution']['authorityId']},
                             outcome={'outcomeId':c['outcome']['portId'],'contract':{'contractId':c['outcome']['contractId']},'terminal':False})
                    scenario_nodes[sid] = (n, path, f'/canonicalGraph/cells/{i}')
            for i, e in enumerate(native['edges']):
                for end in ('from', 'to'):
                    need(e[end]['cellId'] in cells, 'NATIVE_DANGLING_CELL')
                    c = cells[e[end]['cellId']]
                    need(e[end]['portId'] in (c['input']['portId'], c['outcome']['portId']), 'NATIVE_DANGLING_PORT')
                scopes = sorted(set(scope(e['from']['cellId']) + scope(e['to']['cellId'])))
                record('route', e['kind'], path, f'/canonicalGraph/edges/{i}', scopes, e['edgeId'])
                if e['kind'] not in NATIVE_EDGES: finding('UNKNOWN_NATIVE_ROUTE', e['edgeId'], e['kind'], 'Register exact semantics; do not approximate as a sequence.')
            for i, b in enumerate(plan.get('realizationOverlay', {}).get('providerBindings', [])):
                record('provider', b.get('mechanicId', 'provider'), path, f'/realizationOverlay/providerBindings/{i}', scope(b['cellId']), b.get('slotId'))
    for ordinal, (sid, s) in enumerate(inventory.items()):
        refs = [source(inventory_path, '/'+str(stored_inventory[sid][0]), label='Exact narrative; verified against capsule feature bytes')]; metadata = scenario_nodes.get(sid)
        if metadata:
            n, path, pointer = metadata; refs.append(source(path, pointer, 'capsule-entry', 'Declared scenario boundary'))
        else:
            n = {}; finding('SCENARIO_PLAN_UNRESOLVED', sid, 'Feature narrative has no matching plan scenario.', 'Resolve the exact scenario-to-plan identity. Do not infer mechanics.')
        ids = [f's{ordinal}-{phase}' for phase in ('input','event','outcome')]
        for phase, identity in zip(('input','event','outcome'), ids):
            tags = s['tags']; tag = lambda prefix: next((t[len(prefix):] for t in tags if t.startswith(prefix)), None)
            contract = n.get(phase, {}).get('contract', {}).get('contractId') or tag('@'+phase+'-contract:')
            label = tag('@'+phase+':') or n.get(phase, {}).get(phase+'Id') or phase.title()
            # Readable labels are a lens. Full source text and identities stay in meanings/sources.
            full = ' '.join(x['text'] for x in s[phase]); label = label.replace('-', ' ')
            g['nodes'].append(dict(id=identity, type=phase, label=label[:87]+'…' if len(label)>90 else label,
                                   detail=full[:157]+'…' if len(full)>160 else full, capabilityId=capability_id,
                                   scenarioId=sid, basis='DECLARED', sourceRefs=refs, layer='mechanic', productContract=contract if phase != 'event' else None))
            g['meanings'].append(dict(nodeId=identity, altitude='scenario', responsibility=full if phase=='event' else None,
                authorityId=n.get('event', {}).get('executionAuthorityId') if phase=='event' else None,
                experience=full if phase=='outcome' else None, variants=(tag('@outcome-variants:') or '').split('|') if phase=='outcome' and tag('@outcome-variants:') else []))
        for i in range(2):
            g['edges'].append(dict(id=f's{ordinal}-e{i}',source=ids[i],target=ids[i+1],type='transition',label='declared boundary',basis='DECLARED',sourceRefs=refs))
        g['scenarios'].append(dict(id=sid,capabilityId=capability_id,label=s['scenarioName'],nodeIds=ids,sourceRefs=refs))
    g['capabilities'] = [dict(id=capability_id,label=g['title'],domain='Frozen source corpus',scenarioIds=list(inventory),
                            coverage=f'{len(inventory)} declared scenarios; native detail remains separately inspectable',sourceRefs=[cs])]
    finding('EDITORIAL_REVIEW_REQUIRED', capability_id, 'Source revelation preserves declarations; human storytelling and visual acceptance are separate.', 'Review the scenario, claim scope, evidence, human experience and selected animation trace before episode use.')
    finding('NATIVE_MOTION_NOT_LOWERED', capability_id, 'Native records are preserved and inspectable. Scenario triads are not a simulation of the native execution graph.', 'Admit explicit visual/trace profiles for native control flow before animating its mechanics.')
    if not native_count:
        finding('NO_NATIVE_CANONICAL_GRAPH', capability_id, 'Legacy plan operations and bindings are retained exactly; no full canonical graph is supplied.', 'Use the governed blueprint projection boundary to obtain the native graph; never infer it from expressions.')
    return validate_graph(g)


def main():
    p = argparse.ArgumentParser(description=__doc__); p.add_argument('capability', nargs='?'); p.add_argument('--all', action='store_true'); a = p.parse_args()
    ids = sorted(p.stem for p in (ROOT/'data/capsule-evidence/capabilities').glob('*.json')) if a.all else [a.capability]
    rows = []; kinds = Counter(); plans = Counter(); native = Counter()
    for cid in ids:
        g = reveal(cid); out = ROOT/'samples/scl/capabilities'/cid; out.mkdir(parents=True, exist_ok=True)
        write(out/'circuit.json', g.model_dump()); (out/'circuit.scl').write_text(emit(g), encoding='utf-8')
        from scl import parse
        need(graph_hash(parse(emit(g))) == graph_hash(g), 'ROUNDTRIP_CHANGED_GRAPH')
        for r in g.records:
            kinds[r.kind + ':' + r.nativeType] += 1
            if r.kind == 'cell': native['cells'] += 1
            if r.kind == 'route' and r.nativeType in NATIVE_EDGES: native['edges'] += 1
            if r.kind == 'policy' and r.nativeType in PLAN_TYPES: plans[r.nativeType] += 1
        row = dict(id=cid,title=g.title,scenarios=len(g.scenarios),nodes=len(g.nodes),nativeRecords=len(g.records),
                   graphSha256=graph_hash(g), findings=[f.code for f in g.findings],sourceGeneration=g.sourceGeneration)
        rows.append(row)
        print('REVEALED', cid, len(g.scenarios), len(g.records), flush=True)
    if a.all:
        report = dict(status='SOURCE_REVEAL_NOT_EPISODE_APPROVAL',capabilities=len(rows),scenarios=sum(r['scenarios'] for r in rows),
                      sourceGeneration=read('data/source-manifest.json')['manifestDigest'],plans=dict(plans),native=dict(native),recordKinds=dict(sorted(kinds.items())),
                      roundTrip='PASS', before={'curatedInfographicContracts':4,'automaticCircuitEstate':False}, results=rows)
        write('samples/scl/catalog.json', report); write('evaluations/scl-coverage.json',report)


if __name__ == '__main__': main()
