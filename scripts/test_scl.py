import copy
import json
import unittest
from lxml import etree
from infographic_contract import ROOT, read
from scl import parse, emit, validate_graph, graph_hash, Parser
from reveal_scl import reveal
from scl_render import compile_graph
from scl_native import native_view
from build_scl_studio import draft_from_projection, starter_scl


class SCLTests(unittest.TestCase):
    def test_playground_starter_accepts_new_labels_and_preserves_typed_flow(self):
        g=parse(starter_scl().replace('Make it happen','Prepare the narration'))
        self.assertEqual(g.status,'DRAFT');self.assertEqual(g.nodes[1].label,'Prepare the narration')
        self.assertEqual(g.trace,['begin','finish'])
        result=compile_graph(g,enhanced=True)
        self.assertIn('Prepare the narration',result['svg'])
        self.assertEqual(result['receipt']['visibleNodes'],3)
        self.assertEqual(result['receipt']['junctions']['findings'],[])
    def draft(self):return draft_from_projection('scenario-target').model_dump()
    def rejects(self,data,code):
        with self.assertRaisesRegex(ValueError,code):validate_graph(data)
    def test_all_sources_roundtrip_with_fixed_generation(self):
        catalog=read('samples/scl/catalog.json')
        self.assertEqual((catalog['capabilities'],catalog['scenarios']),(219,823))
        for row in catalog['results']:
            g=validate_graph(read(f'samples/scl/capabilities/{row["id"]}/circuit.json'))
            self.assertEqual(graph_hash(parse(emit(g))),row['graphSha256'])
            self.assertEqual(g.sourceGeneration,catalog['sourceGeneration'])
    def test_source_adapters_preserve_three_plan_versions_and_all_native_kinds(self):
        catalog=read('samples/scl/catalog.json')
        self.assertEqual(sorted(catalog['plans'].values()),[16,85,118])
        self.assertEqual(catalog['native'],{'cells':4992,'edges':5498})
        self.assertEqual(catalog['recordKinds']['blueprint:canonical-circuit-blueprint.v1'],48)
        for kind in ('sequence','selection','return','recurrence','cancellation','altitude_descent','bounded_return','transition'):
            self.assertGreater(catalog['recordKinds']['route:'+kind],0)
    def test_reveal_is_reproducible_and_does_not_invent_cross_scenario_wiring(self):
        g=reveal('interlock-agent-operation')
        self.assertEqual(len(g.scenarios),7);self.assertEqual(len(g.edges),14);self.assertEqual(g.trace,[])
        self.assertEqual(graph_hash(g),graph_hash(validate_graph(read('samples/scl/capabilities/interlock-agent-operation/circuit.json'))))
        self.assertTrue(any(r.kind=='operation' and r.nativeType=='invoke-scenario' for r in g.records))
    def test_incomplete_stored_blueprint_remains_testimony_with_a_finding(self):
        g=reveal('generate-executable-capability-scaffold')
        self.assertIn('BLUEPRINT_UNRESOLVED_ENDPOINTS',[f.code for f in g.findings])
        self.assertIn('BLUEPRINT_DECLARED_ADMISSION_STATE',[f.code for f in g.findings])
        self.assertTrue(any(r.kind=='blueprint' for r in g.records))
        self.assertFalse(any(n.id=='bind-executable-scaffold-disposition' for n in g.nodes))
    def test_parser_rejects_duplicate_properties_unknown_fields_versions_and_trailing_input(self):
        text=emit(draft_from_projection('scenario-target'))
        for bad,code in [(text.replace('"0.1"','"9.9"',1),'unsupported version'),(text+'\nexecute anything','trailing input'),
                         (text.replace('  title ', '  invented true;\n  title ',1),'extra_forbidden'),
                         (text.replace('  title ', '  title "duplicate";\n  title ',1),'duplicate')]:
            with self.assertRaisesRegex(ValueError,code):parse(bad)
        with self.assertRaisesRegex(ValueError,'duplicate JSON property'):Parser('scl "0.1"; circuit "x" { title {"x":1,"x":2}; }').parse()
    def test_exact_sources_and_pointers_are_verified(self):
        g=self.draft();g['sources'][0]['sha256']='0'*64;self.rejects(g,'STALE_SOURCE')
        g=self.draft();g['sources'][0]['path']='../outside.json';self.rejects(g,'SOURCE_PATH')
    def test_drafts_cannot_claim_observation_or_bridge_reality_modes(self):
        g=self.draft();g['nodes'][0]['basis']='OBSERVED';self.rejects(g,'REALITY_WITHOUT_SOURCE|DRAFT_CANNOT_CLAIM_CURRENT')
        g=self.draft();g['nodes'][0]['basis']='GAP';g['nodes'][0]['sourceRefs']=['gap'];g['nodes'][0]['closure']='Supply the missing input';self.rejects(g,'MIXED_REALITY_FLOW')
    def test_selection_and_fanout_are_different(self):
        g=self.draft();g['junctions'][0]['type']='branch';self.rejects(g,'INCOMPLETE_SELECTION')
        g=draft_from_projection('scenario-current').model_dump();g['trace'].append('e02');self.rejects(g,'TRACE_EXECUTES_ALTERNATIVES')
    def test_convergence_and_trace_require_both_results(self):
        g=self.draft();join=next(n for n in g['junctions'] if n['type']=='convergence');join.update(join='quorum',quorum=3);self.rejects(g,'INVALID_QUORUM')
        g=self.draft();g['trace'].remove('e04');self.rejects(g,'TRACE_INCOMPLETE_END|TRACE_INCOMPLETE_JOIN')
    def test_no_untyped_merge_or_unbounded_retry(self):
        g=self.draft();g['edges'].append({**g['edges'][0],'id':'shortcut','source':'split','target':'check'});self.rejects(g,'UNTYPED_MERGE')
        g=self.draft();g['edges'].append({**g['edges'][0],'id':'retry','source':'check','target':'activation','type':'retry'});self.rejects(g,'UNBOUNDED_RETRY')
    def test_products_have_exact_contracts(self):
        g=draft_from_projection('estate-target').model_dump();e=next(e for e in g['edges'] if e['type']=='product-transfer');e['productContract']='other.v9';self.rejects(g,'PRODUCT_CONTRACT_MISMATCH')
    def test_source_neighborhood_keeps_native_cell_and_edge_ids(self):
        g=reveal('write-binary-artifact');data=native_view(g)
        root=etree.fromstring(data['svg'].encode());nodes=root.xpath('//*[@data-native-cell]');edges=root.xpath('//*[@data-native-edge]')
        self.assertEqual({n.get('data-native-cell') for n in nodes},set(data['receipt']['visibleCellIds']))
        self.assertEqual({e.get('data-native-edge') for e in edges},set(data['receipt']['visibleEdgeIds']))
        self.assertTrue(all(e.get('data-from-port') and e.get('data-to-port') and e.get('data-kind') for e in edges))
        self.assertEqual(data['receipt']['effects'],'NONE')
    def test_static_and_enhanced_lenses_retain_exact_semantics(self):
        g=draft_from_projection('scenario-target');a=compile_graph(g);b=compile_graph(g,enhanced=True)
        from enhance_infographics import strip_material
        self.assertEqual(strip_material(a['svg']),strip_material(b['svg']))
        self.assertEqual(a['projection'],b['projection']);self.assertEqual(a['receipt']['junctions']['findings'],[])


if __name__=='__main__':unittest.main(verbosity=2)
