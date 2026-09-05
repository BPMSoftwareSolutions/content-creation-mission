"""Require exact evidence and reviewed mechanical direction before rendering."""
import base64,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def local(path):
    p=(ROOT/path).resolve()
    if not p.is_relative_to(ROOT): raise ValueError('EVIDENCE_PATH_ESCAPE')
    return p
def resolve(ref):
    entry=json.loads(local(ref['snapshot']).read_text(encoding='utf-8'))
    raw=base64.b64decode(entry['entryBytesBase64'],validate=True)
    actual='sha256:'+hashlib.sha256(raw).hexdigest()
    if actual!=ref['entryDigest'] or actual!=entry['entryDigest']: raise ValueError('EVIDENCE_DIGEST_MISMATCH')
    if entry['entryId']!=ref['entryId'] or entry['entryRef']!=ref['entryRef']: raise ValueError('EVIDENCE_IDENTITY_MISMATCH')
    value=json.loads(raw)
    for part in ref.get('pointer','').split('/')[1:]:
        part=part.replace('~1','/').replace('~0','~')
        value=value[int(part)] if isinstance(value,list) else value[part]
    return value
def validate_grounding(job):
    binding=job.get('mechanicsEvidence')
    if not binding: raise ValueError('MECHANICS_EVIDENCE_REQUIRED')
    raw=local(binding['path']).read_bytes()
    if hashlib.sha256(raw).hexdigest()!=binding['sha256']: raise ValueError('MECHANICS_PACKAGE_STALE')
    p=json.loads(raw)
    if p['key']!=job['scenarioKey']: raise ValueError('MECHANICS_SCENARIO_MISMATCH')
    if p.get('disposition')!='MECHANICS_DIRECTION_REVIEWED' or p.get('findings'): raise ValueError('MECHANICS_REVIEW_REQUIRED')
    if not p.get('visualDirection') or not p.get('animationBeats'): raise ValueError('MECHANICS_DIRECTION_REQUIRED')
    for category in ('execution','mechanics','providers','contracts','fixtures'):
        if not p['evidence'].get(category): raise ValueError('MECHANICS_LAYER_MISSING:'+category)
        for evidence in p['evidence'][category]: resolve(evidence['source'])
    for beat in p['animationBeats']:
        if not beat.get('sourceRefs') or not beat.get('visibleChange'): raise ValueError('UNSUPPORTED_ANIMATION_BEAT')
        for ref in beat['sourceRefs']: resolve(ref)
    if not p.get('groundingReview',{}).get('gherkinOnlyInsufficient'): raise ValueError('FEATURE_ONLY_DIRECTION')
    return p
