import copy
import unittest
from content_lab import ROOT, classify, derive, load, parse_feature


class CorpusTests(unittest.TestCase):
    def test_background_outline_tables_and_negation(self):
        text = '''@capability:example
Feature: Example
  Background:
    Given a fixed authority
  @scenario:choice
  Scenario Outline: Choose <name>
    Given a candidate
      | key | value |
      | a | b |
    When selection is requested
    Then no execution occurs
    And rejection remains visible
    Examples:
      | name |
      | first |
'''
        record = parse_feature(text, 'example', {}, [], None)[0]
        self.assertEqual(len(record['input']), 2)
        self.assertIn('dataTable', record['input'][1])
        self.assertEqual(len(record['examples']), 1)
        spec = derive(record, {'primary': 'unclassified', 'status': 'UNCLASSIFIED'}, {})
        self.assertIn('no execution occurs', spec['outcomeExperience']['meaning'])
        self.assertEqual(len(spec['outcomeExperience']['sourceSteps']), 2)

    def test_full_corpus_coverage_and_source_preservation(self):
        records = load(ROOT / 'inventories/scenario-inventory.json')
        specs = load(ROOT / 'outputs/visual-experience-specs.json')
        self.assertGreater(len(records), 100)
        self.assertEqual({r['key'] for r in records}, {s['key'] for s in specs})
        self.assertEqual(len(specs), len({s['key'] for s in specs}))
        by_key = {s['key']: s for s in specs}
        for r in records:
            for phase in ('input', 'event', 'outcome'):
                self.assertEqual(r[phase], by_key[r['key']][phase + 'Experience']['sourceSteps'])

    def test_classification_does_not_mutate_semantics(self):
        record = load(ROOT / 'inventories/scenario-inventory.json')[0]
        before = copy.deepcopy(record)
        classify(record, load(ROOT / 'data/visual-taxonomy.json'))
        self.assertEqual(record, before)

    def test_payloads_cover_all_formats_and_unique_ids(self):
        jobs = load(ROOT / 'outputs/generation-manifest.json')
        recipes = load(ROOT / 'data/generation-recipes.json')
        self.assertEqual(len(jobs), len({j['id'] for j in jobs}))
        self.assertEqual({j['format'] for j in jobs}, set(recipes))
        for job in jobs:
            self.assertEqual(job['request']['generationConfig']['imageConfig']['aspectRatio'], recipes[job['format']]['aspectRatio'])


if __name__ == '__main__':
    unittest.main()
