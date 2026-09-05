"""Adversarial conformance and cross-projection identity tests for the visual compiler."""
import copy
import unittest
from pathlib import Path
from urllib.parse import urlsplit,unquote
from lxml import etree
from jsonschema import Draft202012Validator

from infographic_contract import ROOT,read,validate,digest,Projection
from compile_infographics import layout,inspect_geometry,render,measure_rendered_junctions,tangent_controls
from test_season_one import Links

def contract(name='scenario-target'):return read(f'declarations/infographics/{name}.json')

class InfographicGrammar(unittest.TestCase):
    def reject(self,data,reason):
        with self.assertRaisesRegex(ValueError,reason):validate(data)

    def test_four_contracts_schema_provenance_and_layout(self):
        schema=Draft202012Validator(read('schemas/infographic-projection.schema.json'))
        for name in ('scenario-current','scenario-target','capability-current','estate-target'):
            data=contract(name);schema.validate(data);p=validate(data)
            self.assertEqual(inspect_geometry(p,layout(p)),[])
            compiled=read(f'samples/infographic-grammar/{name}/projection.json')
            self.assertEqual(compiled['contractSha256'],digest(ROOT/f'declarations/infographics/{name}.json'))
            self.assertEqual(compiled['geometryFindings'],[])

    def test_future_cannot_be_relabelled_observed(self):
        data=contract();data['nodes'][0]['basis']='OBSERVED';self.reject(data,'REALITY_WITHOUT_SOURCE')
        data=contract();data['nodes'][0]['basis']='DECLARED';data['nodes'][0]['sourceRefs']=['runtime'];self.reject(data,'MIXED_REALITY_FLOW')

    def test_stale_sources_and_missing_json_pointers(self):
        data=contract();data['sources'][0]['sha256']='0'*64;self.reject(data,'STALE_SOURCE')
        data=contract();data['sources'][0]['pointer']='/absent-source-cell'
        with self.assertRaises(KeyError):validate(data)

    def test_branch_needs_total_selection_and_only_one_animated_route(self):
        data=contract('scenario-current');outgoing=[e for e in data['edges'] if e['source']=='select'];outgoing[-1]['guard']=None;self.reject(data,'INCOMPLETE_BRANCH')
        data=contract('scenario-current');data['animationBeats'][3]['edgeIds'].append('e02');self.reject(data,'MOTION_EXECUTES_ALTERNATIVES')

    def test_fanout_cannot_become_a_branch_without_guards(self):
        data=contract();next(n for n in data['junctions'] if n['id']=='split')['type']='branch';self.reject(data,'INCOMPLETE_BRANCH')

    def test_convergence_needs_policy_and_valid_quorum(self):
        data=contract();join=next(n for n in data['junctions'] if n['type']=='convergence');join.pop('join');self.reject(data,'INCOMPLETE_JOIN')
        data=contract();join=next(n for n in data['junctions'] if n['type']=='convergence');join.update(join='quorum',quorum=3);self.reject(data,'INVALID_QUORUM')

    def test_cross_capability_product_must_match_both_ports(self):
        data=contract('estate-target');edge=next(e for e in data['edges'] if e['type']=='product-transfer');edge['productContract']='target.incompatible.v1';self.reject(data,'PRODUCT_CONTRACT_MISMATCH')
        data=contract('estate-target');edge=next(e for e in data['edges'] if e['type']=='product-transfer');edge['source']='c0-event';self.reject(data,'INVALID_PRODUCT_ENDPOINTS')
        data=contract('estate-target');edge=next(e for e in data['edges'] if e['type']=='product-transfer');edge['type']='transition';self.reject(data,'UNDECLARED_CROSS_CAPABILITY_FLOW')

    def test_active_is_not_an_alias_for_declared_binding(self):
        data=contract('scenario-current');data['providers'][0]['state']='active';self.reject(data,'UNPROVEN_ACTIVE_PROVIDER')

    def test_open_port_needs_no_fictitious_provider(self):
        data=contract();provider=next(n for n in data['nodes'] if n['id']=='provider');data['nodes'].remove(provider)
        data['providers'][0].update(nodeId=None,binding='open',state='unknown')
        data['edges']=[e for e in data['edges'] if e['id']!='e07']
        for beat in data['animationBeats']:
            beat['entityIds']=[id for id in beat['entityIds'] if id!='provider'];beat['edgeIds']=[id for id in beat['edgeIds'] if id!='e07']
        data['zoomAggregations'][0]['memberIds'].remove('provider');validate(data)
        data['providers'][0]['nodeId']='fictitious-provider';self.reject(data,'OPEN_PORT_HAS_FULFILLER')

    def test_retry_requires_bound_exit_and_terminal_stop(self):
        data=contract();template=data['junctions'][0].copy();template.update(id='stop',type='termination',label='Ended',detail='No continuation');data['junctions'].append(template)
        data['scenarios'][0]['nodeIds'].append('stop');data['zoomAggregations'][0]['memberIds'].append('stop')
        retry=dict(id='retry',source='check',target='activation',type='retry',label='Retry under the same identity',basis='TARGET',sourceRefs=['target'])
        data['edges'].append(retry);self.reject(data,'UNBOUNDED_RETRY')
        retry.update(maxAttempts=2,exitCondition='Both proofs match',stopTarget='stop');validate(data)
        retry['source']='stop';self.reject(data,'TERMINAL_CONTINUES')

    def test_aggregation_cannot_drop_or_invent_members(self):
        data=contract();data['zoomAggregations'][0]['memberIds'].pop();self.reject(data,'AGGREGATION_DROPS_MEMBERS')
        data=contract();data['zoomAggregations'][0]['memberIds'].append('imaginary-node');self.reject(data,'INVALID_AGGREGATION')

    def test_gap_requires_a_closure_obligation(self):
        data=contract();next(n for n in data['nodes'] if n['basis']=='GAP')['closure']='';self.reject(data,'GAP_WITHOUT_CLOSURE')

    def test_all_frames_preserve_shapes_ids_text_and_evidence(self):
        for directory in (ROOT/'samples/infographic-grammar').glob('*/projection.json'):
            static=etree.parse(str(directory.parent/'infographic.svg'));ids=static.xpath('//*[@data-entity or @data-edge]')
            expected={n.get('id'):(n.get('data-type'),n.get('data-basis'),''.join(n.itertext()),[etree.QName(x).localname for x in n.iter()]) for n in ids}
            for frame in directory.parent.glob('frame-*.svg'):
                tree=etree.parse(str(frame))
                for material in tree.xpath('//*[@data-enhancement]'):material.getparent().remove(material)
                actual=tree.xpath('//*[@data-entity or @data-edge]')
                values={n.get('id'):(n.get('data-type'),n.get('data-basis'),''.join(n.itertext()),[etree.QName(x).localname for x in n.iter()]) for n in actual}
                self.assertEqual(expected,values)

    def test_geometry_rejects_clipping_collision_and_crossed_bodies(self):
        p=validate(contract());geo=layout(p)
        broken=copy.deepcopy(geo);broken['boxes']['activation'][0]=-30;self.assertTrue(any(x.startswith('OUTSIDE_CANVAS') for x in inspect_geometry(p,broken)))
        broken=copy.deepcopy(geo);broken['boxes']['check']=broken['boxes']['activation'][:];self.assertTrue(any(x.startswith('OVERLAP') for x in inspect_geometry(p,broken)))
        broken=copy.deepcopy(geo);box=broken['boxes']['check'];broken['paths']['e00']={'kind':'line','points':[[box[0]-20,box[1]+20],[box[0]+box[2]+20,box[1]+20]]};self.assertIn('EDGE_THROUGH_NODE:e00:check',inspect_geometry(p,broken))

    def test_motion_join_waits_for_both_arrivals_and_keeps_gap(self):
        directory=ROOT/'samples/infographic-grammar/scenario-target';timeline=read(directory/'motion-timeline.json');receipt=read(directory/'motion-receipt.json')
        events=timeline['events'];arrivals={id:e['seconds'] for e in events if e['action']=='arrive' for id in e['ids']};reveals={id:e['seconds'] for e in events if e['action']=='reveal' for id in e['ids']}
        self.assertGreater(reveals['join'],max(arrivals['e03'],arrivals['e04']))
        self.assertGreater(reveals['certified'],reveals['check'])
        self.assertGreater(reveals['proof'],reveals['certified'])
        self.assertEqual(next(n for n in contract()['nodes'] if n['id']=='proof')['basis'],'GAP')
        self.assertEqual(receipt['contractSha256'],digest(ROOT/'declarations/infographics/scenario-target.json'))
        self.assertEqual(receipt['videoSha256'],digest(directory/'circuit-motion.mp4'))
        self.assertEqual(receipt['staticSvgSha256'],digest(directory/'infographic.svg'))
        self.assertGreater(receipt['frames'],480)

    def test_rendered_junction_contacts_and_tangents(self):
        p=validate(contract());geo=layout(p);proof=measure_rendered_junctions(p,render(p,geo))
        self.assertEqual(proof['checkedContacts'],6)
        self.assertEqual(proof['findings'],[])
        self.assertEqual(proof['maxContactErrorSvgUnits'],0)
        self.assertLess(proof['maxTangentErrorDegrees'],1e-7)
        # Each stem shares the centerline of its adjacent main-flow component.
        for junction,side,neighbor in [('split','inputs','activation'),('join','outputs','check')]:
            baseline=geo['boxes'][neighbor][1]+geo['boxes'][neighbor][3]/2
            self.assertAlmostEqual(geo['junctionGlyphs'][junction][side][0]['point'][1],baseline)

    def test_svg_gate_rejects_detached_contact_and_kink(self):
        p=validate(contract());geo=layout(p)
        broken=copy.deepcopy(geo);points=broken['paths']['e03']['points'];points[-1]=[points[-1][0]+3,points[-1][1]]
        self.assertIn('SVG_DETACHED_ANCHOR:e03:join',measure_rendered_junctions(p,render(p,broken))['findings'])
        broken=copy.deepcopy(geo);broken['paths']['e03']['points'][-2][1]+=5
        self.assertIn('SVG_TANGENT_DISCONTINUITY:e03:join',measure_rendered_junctions(p,render(p,broken))['findings'])

    def test_bending_solution_scales_and_keeps_forward_controls(self):
        a,b=tangent_controls([0,0],[120,0],[1,0],[1,0])
        self.assertEqual((a,b),([40,0],[80,0]))
        u,v=[1,0],[.8,.6];start,end=[0,0],[65,90]
        controls=tangent_controls(start,end,u,v)
        scaled=tangent_controls([17,-31],[65*3+17,90*3-31],u,v)
        for original,actual in zip(controls,scaled):
            for i,offset in enumerate([17,-31]):self.assertAlmostEqual(actual[i],original[i]*3+offset)
        self.assertTrue(0<=controls[0][0]<=controls[1][0]<=65)

    def test_local_studio_exports_and_inventory_links_exist(self):
        page=ROOT/'samples/infographic-grammar/index.html';parser=Links();parser.feed(page.read_text(encoding='utf-8'))
        for link in parser.links:
            url=urlsplit(link)
            if url.scheme:continue
            self.assertTrue((page.parent/unquote(url.path)).resolve().is_file(),link)
        inventory=read('samples/infographic-grammar/estate-inventory.json')
        self.assertEqual((inventory['capabilityCount'],inventory['scenarioCount']),(219,823))
        for cap in inventory['capabilities']:self.assertTrue((ROOT/f'declarations/capability-content/{cap["capabilityId"]}.json').is_file())

if __name__=='__main__':unittest.main(verbosity=2)
