"""Regression checks for record-driven edits and caption orphan prevention."""
import copy,json,tempfile,unittest
from pathlib import Path
from production_store import JsonProductionStore,ROOT,digest
from production_captions import segment
from production_composition import section_spec,svg_composition
from unittest.mock import patch

class ProductionRecordsTests(unittest.TestCase):
    def setUp(self):self.store=JsonProductionStore(ROOT/'data/content-production.json')
    def test_new_identity_and_copy_do_not_require_renderer_change(self):
        record=copy.deepcopy(self.store.revisions()[0]);record['revisionId']='arbitrary-new-revision'
        record['episodeId']='arbitrary-id';record['brandLine']='A new record'
        scene=record['scenes'][0];state=scene['states'][-1];state['title']='Changed in data'
        plan,spec=section_spec(self.store,record,scene)
        svg=svg_composition(record,scene,state,len(scene['states'])-1,plan,spec,self.store.profile(record)['visual'])
        self.assertIn('Changed in data',svg)
    def test_missing_composition_has_no_layout_fallback(self):
        record=self.store.revisions()[0];scene=copy.deepcopy(record['scenes'][0]);scene['sectionVisualId']='missing'
        with self.assertRaisesRegex(ValueError,'exactly one'):section_spec(self.store,record,scene)
        plan,_=section_spec(self.store,record,record['scenes'][0])
        with patch('production_composition.read',side_effect=[{'sections':[plan]},{'sections':{}}]):
            with self.assertRaisesRegex(ValueError,'no layout fallback'):section_spec(self.store,record,record['scenes'][0])
    def test_authored_paths_do_not_invent_filled_regions(self):
        record=self.store.revisions()[0];scene=record['scenes'][0];plan,spec=section_spec(self.store,record,scene)
        spec=copy.deepcopy(spec);spec['elements']=[{'type':'path','d':'M 0 0 L 20 20 L 40 0','stroke':'red'}]
        svg=svg_composition(record,scene,scene['states'][0],0,plan,spec,self.store.profile(record)['visual'])
        self.assertIn('fill="none"',svg)
    def test_content_change_invalidates_revision_digest(self):
        record=copy.deepcopy(self.store.revisions()[0]);before=self.store.input_digest(record)
        record['scenes'][0]['narration']+=' A changed sentence.'
        self.assertNotEqual(before,self.store.input_digest(record))
    def test_duplicate_scene_ids_rejected(self):
        value=copy.deepcopy(self.store.data);r=value['revisions'][0]
        r['scenes'][1]['id']=r['scenes'][0]['id']
        with tempfile.TemporaryDirectory() as directory:
            p=Path(directory)/'store.json';p.write_text(json.dumps(value),encoding='utf-8')
            with self.assertRaisesRegex(ValueError,'Duplicate'):JsonProductionStore(p)
    def test_orphan_word_is_not_a_caption(self):
        config=self.store.profile(self.store.revisions()[0])['captions']
        words='The completed tool call returned a reservation but we still need to check whether the result worked.'.split()
        mapping={i:(i*.28,(i+1)*.28) for i in range(len(words))}
        cues=segment(words,mapping,len(words)*.28,config)
        self.assertEqual(' '.join(t.replace('\n',' ') for _,_,t in cues),' '.join(words))
        self.assertTrue(all(b-a>=config['minimumSeconds'] for a,b,t in cues))
        self.assertTrue(all(len(t.splitlines())<=2 for a,b,t in cues))
        self.assertTrue(all(t.strip()!='worked.' for a,b,t in cues))
        self.assertTrue(all(cues[i][1]<=cues[i+1][0] for i in range(len(cues)-1)))
    def test_paths_outside_workspace_rejected(self):
        with self.assertRaises(ValueError):self.store.resolve('../outside.mp4')

if __name__=='__main__':unittest.main()
