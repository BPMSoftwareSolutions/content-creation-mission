"""Composition boundary tests: reject stale meaning and verify reusable output."""
import copy
import json
import unittest
from unittest.mock import patch
from urllib.parse import unquote, urlsplit

from lxml import html, etree

import capability_page_contract as contract
from build_capability_pages import compile_page, json_script
from infographic_contract import ROOT, read, digest

INTERLOCK = 'declarations/capability-pages/interlock-agent-operation.json'
NARRATION = 'declarations/capability-pages/generate-governed-narration.json'


class CapabilityPageTests(unittest.TestCase):
    def test_same_template_compiles_two_distinct_contracts(self):
        a, b = compile_page(INTERLOCK, check=True), compile_page(NARRATION, check=True)
        self.assertEqual((a['status'], a['circuitCount'], a['surfaceCount']), ('COMPOSED', 3, 9))
        self.assertEqual((b['status'], b['circuitCount'], b['surfaceCount']), ('COMPOSED_WITH_OPEN_CIRCUIT', 0, 9))
        self.assertNotEqual(a['storyTitle'], b['storyTitle'])
        for filename in ('page.css', 'page.js'):
            self.assertEqual((ROOT / f'samples/capability-pages/interlock-agent-operation/{filename}').read_bytes(), (ROOT / f'samples/capability-pages/generate-governed-narration/{filename}').read_bytes())

    def test_changed_content_bytes_are_rejected(self):
        value = read(INTERLOCK); value['content']['sha256'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'STALE_ARTIFACT'):
            contract.validate_page(value)

    def test_film_must_match_its_receipt(self):
        value = read(INTERLOCK); wrong = read(NARRATION)['film']['media']
        value['film']['media'] = wrong; value['surfaces']['video'] = wrong
        with self.assertRaisesRegex(ValueError, 'FILM_RECEIPT_MISMATCH'):
            contract.validate_page(value)

    def test_surfaces_cannot_expand_beyond_content_contract(self):
        value = read(INTERLOCK); value['surfaces']['execute'] = value['surfaces']['demo']
        with self.assertRaisesRegex(ValueError, 'SURFACE_COVERAGE_MISMATCH'):
            contract.validate_page(value)

    def test_missing_circuit_requires_an_explicit_requirement(self):
        value = read(NARRATION); value.pop('openCircuit')
        with self.assertRaisesRegex(ValueError, 'CIRCUIT_OR_EXPLICIT_GAP_REQUIRED'):
            contract.validate_page(value)

    def test_circuit_cannot_be_assigned_to_an_unrelated_capability(self):
        value = read(NARRATION); value.pop('openCircuit'); value['circuits'] = read(INTERLOCK)['circuits'][:1]
        with self.assertRaisesRegex(ValueError, 'CIRCUIT_CAPABILITY_MISMATCH'):
            contract.validate_page(value)

    def test_edited_compiled_semantics_cannot_bypass_canonical_contract(self):
        original = contract.read
        def altered(path):
            data = original(path)
            if str(path).endswith('projection.json'):
                data = copy.deepcopy(data); data['nodes'][0]['basis'] = 'OBSERVED'
            return data
        with patch.object(contract, 'read', side_effect=altered):
            with self.assertRaisesRegex(ValueError, 'COMPILED_SEMANTIC_DRIFT'):
                contract.validate_page(read(INTERLOCK))

    def test_composed_svg_and_motion_preserve_target_gap(self):
        _, _, circuits, _ = contract.validate_page(read(INTERLOCK))
        target = circuits[0]
        for key in ('baseSvg', 'enhancedSvg'):
            root = etree.fromstring(target[key].encode())
            self.assertEqual(root.xpath('//*[@id="proof"]')[0].get('data-basis'), 'GAP')
            self.assertEqual(root.xpath('//*[@id="join"]')[0].get('data-basis'), 'TARGET')
        self.assertTrue(target['motion'].endswith('circuit-motion-enhanced.mp4'))
        self.assertEqual(target['binding']['relationship'], 'related-scenario')

    def test_paths_cannot_escape_the_content_lab(self):
        with self.assertRaisesRegex(ValueError, 'ARTIFACT_PATH'):
            contract.Inputs().file('../agentic-harness/package.json')

    def test_published_pages_have_valid_local_links_and_complete_claims(self):
        for manifest in (INTERLOCK, NARRATION):
            value = read(manifest); cap = value['capabilityId']; content = read(value['content']['path'])
            directory = ROOT / f'samples/capability-pages/{cap}'
            document = html.fromstring((directory / 'index.html').read_bytes())
            self.assertEqual(set(document.xpath('//*[@data-claim]/@data-claim')), {c['id'] for c in content['claims']})
            for attr in document.xpath('//@href | //@src | //@poster'):
                path = unquote(urlsplit(attr).path)
                if path:
                    self.assertTrue((directory / path).resolve().is_file(), attr)
            for filename, expected in read(directory / 'build-receipt.json')['outputs'].items():
                self.assertEqual(digest(directory / filename), expected)
            self.assertEqual(len(document.xpath('//fieldset')), len(content['training']['questions']))

    def test_embedded_data_cannot_break_out_of_script(self):
        value = {'title': '</script><script>alert(1)</script>\u2028'}
        output = json_script(value)
        self.assertNotIn('<', output)
        self.assertEqual(json.loads(output.removeprefix('window.CAPABILITY_PAGE = ').rstrip(';\n')), value)


if __name__ == '__main__':
    unittest.main()
