"""Protect lesson provenance, availability, source semantics and local delivery."""
import copy
import json
import subprocess
import unittest
from unittest.mock import patch
from urllib.parse import unquote, urlsplit

from build_engineering_school import ROOT, DEST, MANIFEST, Course, load_course, read, digest
from test_season_one import Links


class EngineeringSchool(unittest.TestCase):
    def test_course_is_source_bound_and_covers_the_curriculum(self):
        course, modules, page, target, gaps, circuit, inputs = load_course()
        self.assertEqual(len(modules),10)
        self.assertEqual({c.id for c in course.concepts},set().union(*(set(m['conceptIds']) for m in modules)))
        self.assertEqual(sum(m['availability']=='WORKED_LESSON' for m in modules),1)
        self.assertTrue(all(p.status=='ROADMAP' for p in course.pathways))
        self.assertEqual(circuit['projection']['id'],'scenario-target')
        self.assertEqual(target['mode'],'TARGET_DESIGN_REFERENCE_SIMULATION')
        self.assertEqual(page.film.media.sha256,read(ROOT/'samples/content-catalog/interlock-agent-operation/film.receipt.json')['filmDigest'])

    def altered(self, mutate):
        original=read(MANIFEST);data=copy.deepcopy(original);mutate(data)
        def replacement(path): return data if str(path)==str(MANIFEST) else read(path)
        with patch('build_engineering_school.read',side_effect=replacement): return load_course()

    def test_stale_case_study_and_invented_availability_are_rejected(self):
        with self.assertRaisesRegex(ValueError,'STALE_ARTIFACT'):
            self.altered(lambda d:d['caseStudy'].update(sha256='0'*64))
        with self.assertRaisesRegex(ValueError,'UNSUPPORTED_LESSON_AVAILABILITY'):
            self.altered(lambda d:d['modules'][1].update(availability='WORKED_LESSON'))
        with self.assertRaisesRegex(ValueError,'CAPABILITY_SEQUENCE'):
            self.altered(lambda d:d['modules'][1].update(capabilityId='invented-capability'))

    def test_untaught_concepts_and_wrong_evidence_cannot_enter_the_class(self):
        with self.assertRaisesRegex(ValueError,'UNTAUGHT_CONCEPT'):
            self.altered(lambda d:d['concepts'].append({**d['concepts'][0],'id':'extra'}))
        with self.assertRaisesRegex(ValueError,'LESSON_EVIDENCE_DRIFT'):
            self.altered(lambda d:d.update(target=d['gaps']))
        data=read(MANIFEST);data['enrollmentOpen']=True
        with self.assertRaises(ValueError): Course.model_validate(data)

    def test_every_build_input_output_and_navigation_link_resolves(self):
        receipt=read(DEST/'build-receipt.json')
        for path,sha in receipt['inputs'].items(): self.assertEqual(digest(ROOT/path),sha,path)
        for name,sha in receipt['outputs'].items(): self.assertEqual(digest(DEST/name),sha,name)
        parser=Links();parser.feed((DEST/'index.html').read_text(encoding='utf-8'))
        for raw in parser.links:
            url=urlsplit(raw)
            if url.scheme or url.netloc: continue
            path=(DEST/unquote(url.path)).resolve() if url.path else DEST/'index.html'
            self.assertTrue(path.is_file(),raw);self.assertTrue(path.is_relative_to(ROOT),raw)
            if url.fragment and path.suffix=='.html':
                destination=Links();destination.feed(path.read_text(encoding='utf-8'))
                self.assertIn(url.fragment,destination.ids,raw)

    def test_reference_lab_semantic_invariants(self):
        result=subprocess.run(['node','--test','scripts/engineering-lab.test.cjs'],cwd=ROOT,capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)

    def test_browser_export_preserves_open_cells_and_the_exact_course(self):
        export=read(ROOT/'evaluations/engineering-school-learner-export.json')
        self.assertEqual(export['courseSha256'],digest(MANIFEST))
        self.assertEqual(export['kind'],'LEARNER_DESIGN_TESTIMONY')
        self.assertEqual(export['status'],'DRAFT_WITH_OPEN_CELLS')
        self.assertEqual(len(export['missingFields']),4)
        self.assertFalse(export['liveEffects'])
        self.assertEqual(export['comparisons'][0]['decision'],'HOLD')


if __name__=='__main__':unittest.main(verbosity=2)
