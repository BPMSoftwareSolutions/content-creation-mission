"""Read-only capsule corpus -> reproducible editorial content preparation."""
import argparse
import base64
import csv
import hashlib
import html
import json
import re
from collections import Counter
from pathlib import Path

from gherkin.parser import Parser
from jsonschema import validate

ROOT = Path(__file__).resolve().parents[1]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def tag_value(tags, prefix):
    return next((t['name'][len(prefix):] for t in tags if t['name'].startswith(prefix)), None)


def walk(children, inherited=()):
    background = list(inherited)
    for child in children:
        if 'background' in child:
            background.extend(child['background']['steps'])
        elif 'rule' in child:
            yield from walk(child['rule']['children'], background)
        elif 'scenario' in child:
            yield child['scenario'], background


def parse_feature(text, capability, source, dependencies, actor):
    feature = Parser().parse(text)['feature']
    records = []
    for scenario, background in walk(feature['children']):
        tags = feature.get('tags', []) + scenario.get('tags', [])
        sid = tag_value(scenario.get('tags', []), '@scenario:')
        identity_origin = 'declared' if sid else 'derived-from-source-line'
        sid = sid or f"scenario-line-{scenario['location']['line']}"
        phases = {'input': [], 'event': [], 'outcome': []}
        phase = None
        for step in list(background) + scenario['steps']:
            phase = {'Context': 'input', 'Action': 'event', 'Outcome': 'outcome'}.get(step.get('keywordType'), phase)
            if phase is None:
                raise ValueError(f'Unclassified step: {capability}/{sid}')
            item = {'text': step['text'], 'line': step['location']['line']}
            for key in ('dataTable', 'docString'):
                if key in step:
                    item[key] = step[key]
            phases[phase].append(item)
        records.append({
            'key': f'{capability}::{sid}', 'capabilityId': capability,
            'capabilityName': feature['name'], 'scenarioId': sid,
            'scenarioName': scenario['name'], 'identityOrigin': identity_origin,
            'scenarioKind': scenario['keyword'], 'examples': scenario.get('examples', []),
            'input': phases['input'], 'event': phases['event'], 'outcome': phases['outcome'],
            'products': [tag_value(tags, '@outcome:')] if tag_value(tags, '@outcome:') else [],
            'dependencies': dependencies, 'providers': [], 'providerDiscovery': 'not inferred from dependency names',
            'actors': [actor] if actor else [], 'altitude': None,
            'notes': feature.get('description', ''),
            'source': {**source, 'scenarioLine': scenario['location']['line']},
            'tags': [t['name'] for t in tags]
        })
    return records


def inventory(source_root):
    manifest_path = source_root / 'capsules/capsule-estate.manifest.json'
    manifest_bytes = manifest_path.read_bytes()
    manifest = json.loads(manifest_bytes)
    records, findings, sources = [], [], []
    for item in manifest['capsules']:
        cid = item['capabilityId']
        path = (manifest_path.parent / item['file']).resolve()
        if not path.is_relative_to(manifest_path.parent.resolve()):
            raise ValueError('Capsule path outside estate')
        raw = path.read_bytes()
        if 'sha256:' + digest(raw) != item['capsuleDigest']:
            raise ValueError(f'Capsule digest mismatch: {cid}')
        capsule = json.loads(raw)
        candidates, actor = [], None
        for entry in capsule['entries']:
            body = base64.b64decode(entry['entryBytesBase64'], validate=True)
            if 'sha256:' + digest(body) != entry['entryDigest']:
                raise ValueError(f'Entry digest mismatch: {cid}/{entry["entryId"]}')
            if entry['entryId'] == 'capability.authority.json':
                authority = json.loads(body)
                actor = authority.get('userStory', {}).get('actor')
            if '.feature' in entry['entryRef'] or '.feature' in entry['entryId']:
                text = body.decode('utf-8-sig')
                if entry['entryRef'] in capsule.get('lineage', []) or re.search(r'@capability:' + re.escape(cid) + r'(?:\s|$)', text):
                    candidates.append((entry, body, text))
        lineage_candidates = [c for c in candidates if c[0]['entryRef'] in capsule.get('lineage', [])]
        if lineage_candidates:
            candidates = lineage_candidates
        unique = {digest(body): (entry, body, text) for entry, body, text in candidates}
        if len(unique) != 1:
            findings.append({'capabilityId': cid, 'code': 'FEATURE_MISSING_OR_AMBIGUOUS', 'candidates': len(unique)})
            continue
        entry, body, text = next(iter(unique.values()))
        snapshot = ROOT / 'data/source-features' / (cid + '.feature')
        snapshot.parent.mkdir(parents=True, exist_ok=True)
        snapshot.write_bytes(body)
        source = {'capsuleFile': item['file'], 'capsuleDigest': item['capsuleDigest'],
                  'featureEntry': entry['entryRef'], 'featureDigest': entry['entryDigest'],
                  'estateManifestDigest': 'sha256:' + digest(manifest_bytes),
                  'snapshot': str(snapshot.relative_to(ROOT)).replace('\\', '/')}
        try:
            parsed = parse_feature(text, cid, source, capsule.get('declaredDependencies', []), actor)
        except Exception as exc:
            findings.append({'capabilityId': cid, 'code': 'FEATURE_PARSE_ERROR', 'detail': str(exc)})
            continue
        if not parsed:
            findings.append({'capabilityId': cid, 'code': 'NO_SCENARIOS'})
        records.extend(parsed)
        sources.append(source)
    if manifest_path.read_bytes() != manifest_bytes:
        raise ValueError('Estate manifest changed during read; rerun')
    keys = [r['key'] for r in records]
    if len(set(keys)) != len(keys):
        raise ValueError('Duplicate capability/scenario identity')
    write(ROOT / 'data/source-manifest.json', {'sourceRoot': str(source_root), 'manifestDigest': digest(manifest_bytes),
          'capabilityCount': len(manifest['capsules']), 'sources': sources, 'findings': findings})
    write(ROOT / 'inventories/scenario-inventory.json', records)
    with (ROOT / 'inventories/scenario-inventory.csv').open('w', encoding='utf-8-sig', newline='') as stream:
        fields = ['key', 'capabilityId', 'capabilityName', 'scenarioId', 'scenarioName', 'input', 'event', 'outcome', 'products', 'dependencies', 'providers', 'actors', 'altitude', 'notes', 'source']
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction='ignore')
        writer.writeheader()
        for record in records:
            writer.writerow({k: json.dumps(v, ensure_ascii=False) if isinstance(v, (list, dict)) else v for k, v in record.items()})
    return records


def classify(record, taxonomy):
    title = (record['scenarioId'] + ' ' + record['scenarioName']).lower()
    event = ' '.join(x['text'] for x in record['event']).lower()
    evidence = []
    for family in taxonomy:
        matches = [term for term in family['terms'] if re.search(r'\b' + re.escape(term) + r'\b', title.replace('-', ' '))]
        event_matches = [term for term in family['terms'] if re.search(r'\b' + re.escape(term) + r'\b', event)]
        score = len(matches) * 3 + len(event_matches)
        if score:
            evidence.append({'family': family['id'], 'score': score, 'titleMatches': matches, 'eventMatches': event_matches})
    evidence.sort(key=lambda x: (-x['score'], x['family']))
    tie = len(evidence) > 1 and evidence[0]['score'] == evidence[1]['score']
    return {'key': record['key'], 'primary': evidence[0]['family'] if evidence else 'unclassified',
            'candidates': evidence, 'status': 'AMBIGUOUS' if tie else 'RULE_ASSIGNED' if evidence else 'UNCLASSIFIED',
            'method': 'lexical-rules-v1', 'confidence': 'uncalibrated; scores are rule weights, not probabilities'}


def derive(record, assignment, families):
    family = families.get(assignment['primary'], {'motif': 'three evidence-linked panels', 'motion': 'highlight the requested change'})
    spec = {'key': record['key'], 'capabilityId': record['capabilityId'], 'scenarioId': record['scenarioId'],
            'source': record['source'], 'status': 'EDITORIAL_CANDIDATE', 'visualFamily': assignment['primary'],
            'classificationStatus': assignment['status'], 'actors': record['actors'],
            'environment': {'kind': 'creative-choice', 'description': 'abstract architectural exhibit with labeled evidence objects'},
            'visualMotifs': [family['motif']], 'motionHints': [family['motion']],
            'styleHints': ['proposed palette: indigo authority, teal positive, amber pending, coral rejection', 'pair colors with labels and shapes'],
            'tone': 'clear, precise, curious', 'objects': record['products'],
            'animationPotential': 'Three editorial phases; no implied runtime transition between different scenarios.',
            'generationNotes': ['Keep negatives and alternative outcomes intact.', 'Do not invent a success or execution effect.', 'Do not treat creative objects as canonical actors.'],
            'unresolved': ['physical environment', 'official brand profile', 'provider identity', 'semantic altitude'],
            'reviewRequired': True}
    for phase in ('input', 'event', 'outcome'):
        spec[phase + 'Experience'] = {'sourceSteps': record[phase], 'meaning': '\n'.join(x['text'] for x in record[phase]),
                                    'overlay': {'input': 'INPUT', 'event': 'EVENT', 'outcome': 'OUTCOME'}[phase]}
    if not record['actors']:
        spec['unresolved'].append('source-supported actor')
    if record['examples']:
        spec['examples'] = record['examples']
        spec['generationNotes'].append('Scenario outline template: select an Examples row before final rendering.')
    return spec


def run(source_root, formats, sample_count):
    formats = sorted(set(formats))
    for folder in ('docs', 'data', 'inventories', 'schemas', 'prompts', 'scripts', 'notebooks', 'outputs', 'evaluations', 'samples'):
        (ROOT / folder).mkdir(exist_ok=True)
    records = inventory(source_root)
    taxonomy = load(ROOT / 'data/visual-taxonomy.json')
    families = {f['id']: f for f in taxonomy}
    assignments = [classify(r, taxonomy) for r in records]
    specs = [derive(r, a, families) for r, a in zip(records, assignments)]
    schema = load(ROOT / 'schemas/visual-experience.schema.json')
    for spec in specs:
        validate(spec, schema)
        slug = spec['capabilityId'] + '--' + spec['scenarioId']
        if not re.fullmatch(r'[a-zA-Z0-9_.-]+', slug):
            slug = digest(spec['key'].encode())
        write(ROOT / 'outputs/visual-experience-specs' / (slug + '.json'), spec)
    write(ROOT / 'outputs/visual-experience-specs.json', specs)
    write(ROOT / 'outputs/scenario-taxonomy-classification.json', assignments)
    recipes = load(ROOT / 'data/generation-recipes.json')
    jobs = []
    template = (ROOT / 'prompts/scenario_visual_prompt_template.md').read_text(encoding='utf-8')
    for spec in specs:
        for format_name in formats:
            recipe = recipes[format_name]
            prompt = template.replace('{{SPEC}}', json.dumps(spec, ensure_ascii=False)).replace('{{COMPOSITION}}', recipe['composition'])
            request = {'contents': [{'role': 'user', 'parts': [{'text': prompt}]}],
                       'generationConfig': {'responseModalities': ['TEXT', 'IMAGE'], 'imageConfig': {'aspectRatio': recipe['aspectRatio']}}}
            jobs.append({'id': digest((spec['key'] + format_name + prompt).encode())[:24], 'scenarioKey': spec['key'],
                         'family': spec['visualFamily'], 'format': format_name, 'model': recipe['model'],
                         'sourceDigest': spec['source']['featureDigest'], 'reviewRequired': True, 'request': request})
    write(ROOT / 'outputs/generation-manifest.json', jobs)
    for family in sorted({j['family'] for j in jobs}):
        path = ROOT / 'outputs/batches' / (family + '.jsonl')
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(''.join(json.dumps({'key': j['id'], 'request': j['request']}, ensure_ascii=False) + '\n' for j in jobs if j['family'] == family), encoding='utf-8')
    # Deterministic round-robin across families, then fill without duplicates.
    samples = []
    for family in sorted({s['visualFamily'] for s in specs}):
        candidates = [s for s in specs if s['visualFamily'] == family]
        if candidates and len(samples) < sample_count:
            samples.append(candidates[0])
    for spec in specs:
        if len(samples) >= sample_count:
            break
        if spec not in samples:
            samples.append(spec)
    write(ROOT / 'samples/scenario-sample-set.json', samples)
    sample_keys = {s['key'] for s in samples}
    write(ROOT / 'samples/generation-manifest.json', [j for j in jobs if j['scenarioKey'] in sample_keys])
    findings = load(ROOT / 'data/source-manifest.json')['findings']
    missing = [r['key'] for r in records if any(not r[p] for p in ('input', 'event', 'outcome'))]
    report = {'scenarioCount': len(records), 'specCount': len(specs), 'jobCount': len(jobs), 'sampleCount': len(samples),
              'capabilitiesProcessed': len({r['capabilityId'] for r in records}), 'taxonomyCounts': dict(sorted(Counter(a['primary'] for a in assignments).items())),
              'ambiguousCount': sum(a['status'] == 'AMBIGUOUS' for a in assignments), 'unclassifiedCount': sum(a['status'] == 'UNCLASSIFIED' for a in assignments),
              'sourceFindings': findings, 'missingPhases': missing, 'schemaValidation': 'PASS',
              'phaseTextPreserved': all(s[p + 'Experience']['sourceSteps'] == r[p] for s, r in zip(specs, records) for p in ('input', 'event', 'outcome')),
              'imageGeneration': 'NOT_RUN', 'semanticReview': 'REQUIRED', 'pass': not findings and not missing}
    write(ROOT / 'evaluations/pipeline-report.json', report)
    lines = ['# Processed sample', '', 'Generated from the full inventory. Rendering and semantic review remain separate.', '']
    for s in samples:
        lines += ['## ' + s['key'], '', 'Family: ' + s['visualFamily'], '']
        for p in ('input', 'event', 'outcome'):
            lines += ['**' + p.title() + ':** ' + s[p + 'Experience']['meaning'], '']
    (ROOT / 'samples/scenario-sample-report.md').write_text('\n'.join(lines), encoding='utf-8')
    rows = Counter(r['capabilityId'] for r in records)
    (ROOT / 'samples/capability-sample-report.md').write_text('# Capability coverage\n\n' + '\n'.join(f'- {c}: {n} scenarios' for c, n in sorted(rows.items())), encoding='utf-8')
    taxonomy_doc = ['# Visual taxonomy', '', 'Version 1: explicit lexical rules; editorial hypotheses, not statistical clusters. Ties remain ambiguous. Review scores are not probabilities.', '']
    for f in taxonomy:
        examples = [a['key'] for a in assignments if a['primary'] == f['id']][:3]
        taxonomy_doc += ['## ' + f['id'], '', f['definition'], '', 'Motif: ' + f['motif'], '', 'Examples: ' + '; '.join(examples), '']
    (ROOT / 'docs/visual-taxonomy.md').write_text('\n'.join(taxonomy_doc), encoding='utf-8')
    cards = []
    for s in samples:
        panels = ''.join('<section><h3>' + p.upper() + '</h3><p>' + html.escape(s[p + 'Experience']['meaning']) + '</p></section>' for p in ('input', 'event', 'outcome'))
        cards.append('<article><h2>' + html.escape(s['key']) + '</h2><small>' + html.escape(s['visualFamily']) + ' · editorial draft</small><div>' + panels + '</div></article>')
    (ROOT / 'samples/gallery.html').write_text('<!doctype html><meta charset="utf-8"><title>Scenario content lab</title><style>body{font:16px system-ui;margin:3rem;background:#f4f4f0;color:#182339}article{background:white;padding:2rem;margin:2rem 0;border-radius:12px}div{display:grid;grid-template-columns:repeat(3,1fr);gap:2rem}h2{overflow-wrap:anywhere}h3{color:#5048a5}p{line-height:1.6}@media(max-width:800px){div{grid-template-columns:1fr}}</style><h1>Architecture → visual experience</h1><p>Source-derived semantic cards. These are not generated images.</p>' + ''.join(cards), encoding='utf-8')
    print(json.dumps(report, indent=2))
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', required=True, type=Path)
    parser.add_argument('--formats', default='scenario-triptych', help='Comma-separated recipe names')
    parser.add_argument('--samples', type=int, default=20)
    args = parser.parse_args()
    source_root = args.source.resolve()
    if ROOT == source_root or ROOT.is_relative_to(source_root):
        parser.error('Content lab must be outside the source repository')
    result = run(source_root, args.formats.split(','), args.samples)
    raise SystemExit(0 if result['pass'] else 2)
