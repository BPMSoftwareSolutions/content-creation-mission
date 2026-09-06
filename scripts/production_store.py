"""JSON adapter and revision lookup. Renderers consume records, not episode code."""
import hashlib,json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def read(path):return json.loads(Path(path).read_text(encoding='utf-8'))
def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def artifact_digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def write(path,value):
    p=Path(path);p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

class JsonProductionStore:
    def __init__(self,path):
        self.path=Path(path);self.data=read(path)
        from jsonschema import Draft202012Validator
        Draft202012Validator(read(ROOT/'schemas/content-production.schema.json')).validate(self.data)
        if self.data['storeVersion']!='content-production.v1':raise ValueError('Unsupported content store version')
        ids=[r['revisionId'] for r in self.data['revisions']]
        if len(ids)!=len(set(ids)):raise ValueError('Duplicate revision identity')
        for revision in self.data['revisions']:
            ids=[s['id'] for s in revision['scenes']]
            scene_ids=[s['sceneId'] for s in revision['scenes']]
            state_ids=[t['stateId'] for s in revision['scenes'] for t in s['states']]
            if any(len(x)!=len(set(x)) for x in (ids,scene_ids,state_ids)):raise ValueError('Duplicate scene or state identity')
    def revisions(self):return self.data['revisions']
    def get_revision(self,revision_id):
        matches=[r for r in self.revisions() if r['revisionId']==revision_id]
        if len(matches)!=1:raise ValueError('Expected one matching revision')
        return matches[0]
    def resolve(self,path):
        target=(ROOT/path).resolve()
        if not target.is_relative_to(ROOT):raise ValueError('Artifact path escapes workspace')
        return target
    def profile(self,revision):return read(self.resolve(revision['productionProfileRef']))
    def input_digest(self,revision):
        companions=read(self.resolve(revision['companionStoreRef']))['records']
        matches=[c for c in companions if c['id']==revision['companionId']]
        if len(matches)!=1:raise ValueError('Expected one companion record')
        inputs={'revision':revision,'profile':self.profile(revision),'companion':matches[0]}
        if revision.get('sectionDirectionRef'):
            from production_composition import section_spec
            inputs['sections']=[{'sceneId':s['sceneId'],'direction':section_spec(self,revision,s)[0],
               'composition':section_spec(self,revision,s)[1],'imageDigest':artifact_digest(self.resolve(s['visualAssetRef']))} for s in revision['scenes']]
        return digest(inputs)
