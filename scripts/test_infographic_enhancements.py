"""Adversarial preservation checks for generated material over canonical SVG."""
import copy
import unittest
from unittest.mock import patch
from lxml import etree

import enhance_infographics as enhancement
from infographic_contract import ROOT, read, digest, validate
from compile_infographics import GRAMMAR, OUT, measure_rendered_junctions


class EnhancementTests(unittest.TestCase):
    def test_complete_reviewed_alphabet_and_asset_bytes(self):
        receipts = enhancement.asset_receipts()
        self.assertEqual(set(receipts), set(GRAMMAR['nodeTypes']) | set(GRAMMAR['junctionTypes']))
        for kind in receipts:
            self.assertTrue((OUT / 'enhancements' / (kind + '.png')).is_file())
            self.assertTrue((OUT / 'enhancements' / (kind + '.svg')).is_file())

    def test_changed_image_or_review_cannot_be_consumed(self):
        receipt = enhancement.asset_receipts()['input']
        with self.assertRaisesRegex(ValueError, 'STALE_MATERIAL_BYTES'):
            enhancement.plate(receipt['image'], '0' * 64)
        real_read = enhancement.read
        def wrong_review(path):
            data = copy.deepcopy(real_read(path))
            if str(path).endswith('component-enhancement-review.json'):
                data['assets']['input']['imageSha256'] = '0' * 64
            return data
        with patch.object(enhancement, 'read', side_effect=wrong_review):
            with self.assertRaisesRegex(ValueError, 'UNREVIEWED_ENHANCEMENT_ASSET:input'):
                enhancement.asset_receipts()
        def wrong_prompt(path):
            data = copy.deepcopy(real_read(path))
            if str(path).endswith('infographic-enhancement.v1.json'):
                data['assets'][0]['prompt'] += '\nUnreviewed change.'
            return data
        with patch.object(enhancement, 'read', side_effect=wrong_prompt):
            with self.assertRaisesRegex(ValueError, 'STALE_COMPONENT_REQUEST:input'):
                enhancement.asset_receipts()

    def test_every_export_recovers_the_exact_base(self):
        count = 0
        for directory in [p.parent for p in OUT.glob('*/projection.json')]:
            for source in [directory/'infographic.svg', *directory.glob('frame-[1-5].svg')]:
                composed = source.with_stem(source.stem + '-enhanced')
                self.assertEqual(enhancement.strip_material(source.read_bytes()), enhancement.strip_material(composed.read_bytes()))
                count += 1
        self.assertEqual(count, 24)

    def test_semantic_mutation_is_not_hidden_by_layer_removal(self):
        base = (OUT/'scenario-target/infographic.svg').read_bytes()
        altered = etree.parse(str(OUT/'scenario-target/infographic-enhanced.svg'))
        altered.xpath('//*[@id="proof"]')[0].set('data-basis', 'OBSERVED')
        self.assertNotEqual(enhancement.strip_material(base), enhancement.strip_material(etree.tostring(altered)))
        altered = etree.parse(str(OUT/'scenario-target/infographic-enhanced.svg'))
        path = altered.xpath('//*[@id="e03"]/*[@marker-end]')[0]
        path.set('d', 'M0 0 C10 0 20 0 30 0')
        self.assertNotEqual(enhancement.strip_material(base), enhancement.strip_material(etree.tostring(altered)))

    def test_material_stays_out_of_text_and_original_contacts_hold(self):
        report = read('evaluations/infographic-enhancement-report.json')
        for product in report['products']:
            directory = OUT/product['id']
            self.assertEqual(product['enhancedSvgSha256'], digest(directory/'infographic-enhanced.svg'))
            self.assertEqual(product['baseSvgSha256'], digest(directory/'infographic.svg'))
            self.assertTrue(product['baseRecoveredExactly'])
            for mask in product['maskProofs']:
                self.assertEqual(mask['guardLeakPixels'], 0)
                self.assertGreater(mask['materialPixels'], 0)
        contract = validate(read('declarations/infographics/scenario-target.json'))
        proof = measure_rendered_junctions(contract, (OUT/'scenario-target/infographic-enhanced.svg').read_text(encoding='utf-8'))
        self.assertEqual(proof['checkedContacts'], 6)
        self.assertEqual(proof['maxContactErrorSvgUnits'], 0)
        self.assertEqual(proof['findings'], [])

    def test_decorations_cannot_capture_interaction_or_evidence(self):
        root = etree.parse(str(OUT/'scenario-target/infographic-enhanced.svg'))
        layers = root.xpath('//*[@data-enhancement]')
        self.assertEqual(len(layers), 10)
        for layer in layers:
            self.assertEqual(layer.get('aria-hidden'), 'true')
            self.assertEqual(layer.get('pointer-events'), 'none')
            self.assertTrue(layer.getparent().get('data-entity'))
            self.assertFalse(layer.xpath('.//*[@data-entity or @data-edge or @data-basis]'))
        self.assertEqual(root.xpath('//*[@id="proof"]')[0].get('data-basis'), 'GAP')

    def test_enhanced_motion_keeps_timing_and_exact_source(self):
        directory = OUT/'scenario-target'
        base = read(directory/'motion-timeline.json')
        enhanced = read(directory/'motion-timeline-enhanced.json')
        self.assertEqual(enhanced, base)
        receipt = read(directory/'motion-receipt-enhanced.json')
        self.assertEqual(receipt['staticSvgSha256'], digest(directory/'infographic-enhanced.svg'))
        self.assertEqual(receipt['videoSha256'], digest(directory/'circuit-motion-enhanced.mp4'))
        self.assertEqual(receipt['timelineSha256'], digest(directory/'motion-timeline-enhanced.json'))
        self.assertEqual((receipt['width'], receipt['height'], receipt['frames']), (1920, 1080, 534))


if __name__ == '__main__':
    unittest.main(verbosity=2)
