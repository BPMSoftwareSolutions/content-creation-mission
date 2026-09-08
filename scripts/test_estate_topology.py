import json, unittest
from infographic_contract import ROOT
from scl import validate_graph, resolve_sources
from estate_topology import Diagram, blueprint_view, topology_views, expression_views

INVENTORY=json.loads((ROOT.parent.parent/'sidefx-database/data/media/inventory.json').read_bytes())
def graph(cid):return validate_graph(json.loads((ROOT/'samples/scl/capabilities'/cid/'circuit.json').read_bytes()))

class EstateTopologyTests(unittest.TestCase):
    def test_every_selected_blueprint_route_survives_with_exact_semantics(self):
        for subject in (s for s in INVENTORY['subjects'] if s['kind']=='BLUEPRINT'):
            body=subject['definition']['semantics'];view=blueprint_view(body['capability']['capabilityId'],body,{'path':'fixture','sha256':subject['definitionDigest'],'pointer':'/semantics'})
            self.assertEqual({e['edgeId'] for e in body['edges']},{e['identity'] for e in view['edges']})
            self.assertTrue({n['nodeId'] for n in body['nodes']}<={n['identity'] for n in view['nodes']})
            for original,rendered in zip(body['edges'],view['edges']):
                self.assertEqual(original['topology'],rendered['kind'])
                self.assertEqual(original.get('selectingVariant'),rendered['facts'].get('selectingVariant'))
                self.assertEqual(original.get('boundedReturn'),rendered['facts'].get('boundedReturn'))

    def test_native_speech_graph_does_not_drop_cells_routes_or_ports(self):
        g=graph('speech-provider');r=next(r for r in g.records if r.kind=='policy');s=next(s for s in g.sources if s.id==r.sourceRef);plan=resolve_sources([s])[s.id];native=plan['canonicalGraph'];view=topology_views(g,INVENTORY)[0]
        self.assertEqual({c['cellId'] for c in native['cells']},{n['identity'] for n in view['nodes']})
        self.assertEqual({e['edgeId'] for e in native['edges']},{e['identity'] for e in view['edges']})
        actual={e['identity']:e for e in view['edges']}
        for e in native['edges']:
            self.assertEqual(e['from'],actual[e['edgeId']]['facts']['from']);self.assertEqual(e['to'],actual[e['edgeId']]['facts']['to'])
        self.assertGreater(view['analytics']['nodes'],500)
        self.assertIn('selection',view['analytics']['routeKinds'])

    def test_operation_view_expands_declared_calls_and_keeps_provider_bindings(self):
        views=topology_views(graph('adapt-job-market-intelligence-evidence'),INVENTORY);root=next(v for v in views if v.get('scenarioId')=='adapt-job-market-intelligence-evidence')
        self.assertGreater(len(root['nodes']),15)
        self.assertEqual(3,sum(e['kind']=='scenario-call' for e in root['edges']))
        self.assertEqual(4,sum(e['kind']=='provider-binding' for e in root['edges']))
        self.assertTrue(any(v['kind']=='expression' and len(v['nodes'])>70 for v in views))

    def test_literal_objects_never_become_fake_mechanics(self):
        g=graph('adapt-job-market-intelligence-evidence');plan={'nodes':[],'mechanicBindings':[{'bindingId':'fixture','configuration':{'expression':{'op':'literal','value':{'op':'fake-effect','value':42}}}}]}
        views=expression_views(g,plan,{'pointer':'','path':'fixture','sha256':'0'*64},{})
        self.assertEqual(['literal'],[n['facts']['mechanicId'] for n in views[0]['nodes']]);self.assertEqual([],views[0]['edges'])

    def test_coverage_gate_rejects_omitted_source_nodes_and_routes(self):
        d=Diagram('fixture','Fixture','blueprint',{});d.node('a','event','A');d.expected_nodes=['a','b']
        with self.assertRaisesRegex(ValueError,'SOURCE_NODE_OMITTED'):d.finish()
        d.expected_nodes=['a'];d.expected_edges=['missing']
        with self.assertRaisesRegex(ValueError,'SOURCE_EDGE_OMITTED'):d.finish()

if __name__=='__main__':unittest.main()
