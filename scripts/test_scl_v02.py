import copy
import json
import unittest
from infographic_contract import ROOT, read
from scl import parse, emit, validate_graph, graph_hash
from scl_v02 import DiagnosticError, diagnostic, flatten, select_trace, Circuit02, TraceStep
from scl_render import compile_graph
from build_scl_studio import draft_from_projection


class SCL02Tests(unittest.TestCase):
    def text(self,name='certification'):
        return (ROOT/f'declarations/scl/{name}.v02.scl').read_text(encoding='utf-8')
    def draft(self):return parse(self.text())
    def rejects(self,data,code):
        with self.assertRaisesRegex(ValueError,code):validate_graph(data)

    def test_lite_compiles_scope_routes_and_inline_meaning(self):
        g=parse(self.text('my-circuit'))
        self.assertIsInstance(g,Circuit02);self.assertEqual(len(g.nodes),3);self.assertEqual(len(g.edges),2)
        self.assertEqual(g.scenarios[0].nodeIds,['request','work','result'])
        self.assertEqual(next(m for m in g.meanings if m.nodeId=='result').experience,'What changed for the person?')
        self.assertEqual(g.trace,flatten(g.traces[0].steps))

    def test_exact_proposed_lite_specimen_is_supported(self):
        notes=(ROOT/'docs/SCL-0.2-DESIGN-NOTES.md').read_text(encoding='utf-8')
        specimen=notes.split('```scl\nscl 0.2;')[1].split('```')[0]
        g=parse('scl 0.2;'+specimen)
        self.assertEqual(len(g.nodes)+len(g.junctions),10)
        self.assertEqual(next(n for n in g.nodes if n.type=='evidence').basis,'GAP')
        self.assertIn('EVIDENCE_REQUIREMENT_OPEN',[f.code for f in g.findings])

    def test_certification_retains_all_eleven_relationships(self):
        g=self.draft();self.assertEqual((len(g.nodes)+len(g.junctions),len(g.edges)),(10,11))
        self.assertEqual(sum(e.type=='dependency' for e in g.edges),2)
        self.assertEqual(sum(e.type=='evidence-attachment' for e in g.edges),1)
        self.assertEqual(g.providers[0].binding,'candidate')
        self.assertEqual(next(n for n in g.nodes if n.type=='evidence').closure,'Execute both probes in the same exact live session; bind actual effects and ordered identities.')

    def test_roundtrip_is_lossless_for_both_new_fixtures(self):
        for name in ('my-circuit','certification'):
            g=parse(self.text(name));self.assertEqual(graph_hash(g),graph_hash(parse(emit(g))))
            self.assertEqual(graph_hash(g),graph_hash(validate_graph(json.loads(g.model_dump_json()))))

    def test_original_zero_one_fixtures_keep_their_graph_hashes(self):
        for identity in ('scenario-target','scenario-current'):
            g=draft_from_projection(identity)
            self.assertEqual(g.version,'sidefx-circuit.v0.1')
            self.assertEqual(graph_hash(g),read(f'samples/scl/{identity}.preview.json')['receipt']['graphSha256'])
            self.assertNotIn('traces',g.model_dump());self.assertNotIn('plane',g.nodes[0].model_dump())

    def test_parallel_keeps_two_separate_paths_and_all_barrier(self):
        g=self.draft();parallel=g.traces[0].steps[1]
        self.assertEqual(len(parallel.paths),2)
        edges={e.id:e for e in g.edges}
        for path in parallel.paths:
            self.assertEqual(edges[path[0].edgeId].source,'both-probes')
            self.assertEqual(edges[path[-1].edgeId].target,'both-results')
        self.assertEqual(next(n for n in g.junctions if n.id=='both-results').join,'all')

    def test_sequential_spelling_cannot_misrepresent_parallel_edges(self):
        data=self.draft().model_dump();t=data['traces'][0];t['steps']=[{'edgeId':e} for e in data['trace']]
        self.rejects(data,'TRACE_SEQUENCE_DISCONNECTED')

    def test_parallel_rejects_duplicate_paths_and_wrong_boundaries(self):
        data=self.draft().model_dump();p=data['traces'][0]['steps'][1]
        p['paths'][1]=copy.deepcopy(p['paths'][0]);data['trace']=flatten([TraceStep.model_validate(s) for s in data['traces'][0]['steps']])
        self.rejects(data,'PARALLEL_PATHS_OVERLAP')
        data=self.draft().model_dump();next(n for n in data['junctions'] if n['id']=='both-results')['join']='any'
        self.rejects(data,'PARALLEL_REQUIRES_FANOUT_AND_ALL_JOIN')

    def test_parallel_trace_cannot_claim_to_cover_an_omitted_branch(self):
        data=self.draft().model_dump();edge=next(e for e in data['edges'] if e['source']=='both-probes')
        data['edges'].append({**edge,'id':'unselected-branch','target':'identities'})
        self.rejects(data,'PARALLEL_INCOMPLETE_BRANCHES')

    def test_trace_and_selected_geometry_cannot_drift(self):
        data=self.draft().model_dump();data['trace']=data['trace'][:-1];self.rejects(data,'TRACE_SELECTION_DRIFT')
        data=self.draft().model_dump();data['selectedTrace']='missing';self.rejects(data,'UNKNOWN_SELECTED_TRACE')

    def test_nested_parallel_paths_remain_structured(self):
        text='''scl 0.2; capability nested { promise "Nested work";
          scenario work { given start "Request";
            when outer { parallel {
              path { when inner { parallel { when a "A"; when b "B"; } } when c "C"; }
              path { when d "D"; }
            } }
            then finish "Done";
          }
        }'''
        g=parse(text);self.assertEqual(len(g.junctions),4)
        self.assertIsNotNone(g.traces[0].steps[1].paths[0][1].paths)
        self.assertEqual(graph_hash(g),graph_hash(parse(emit(g))))

    def test_multiple_scenarios_have_independent_selected_traces(self):
        g=parse('''scl 0.2; capability two { promise "Two views";
          scenario first { given a "A"; when b "B"; then c "C"; }
          scenario second { given d "D"; when e "E"; then f "F"; }
        }''')
        self.assertEqual(len(g.traces),2);selected=select_trace(g,'second.flow')
        view=compile_graph(selected,'second');self.assertEqual(view['receipt']['visibleNodes'],3)
        self.assertTrue(set(g.trace).isdisjoint(selected.trace))

    def test_altitude_and_plane_remain_independent(self):
        text=self.text().replace('altitude scenario;','altitude capability;')
        g=parse(text);n=next(n for n in g.junctions if n.id=='both-probes');m=next(m for m in g.meanings if m.nodeId==n.id)
        self.assertEqual(n.plane,'primary');self.assertEqual(m.altitude,'capability')
        g.meanings[0].altitude='physical'
        self.assertEqual(graph_hash(g),graph_hash(parse(emit(g))))

    def test_plane_conflicts_and_upward_containment_reject(self):
        data=self.draft().model_dump();data['nodes'][0]['plane']='primary';self.rejects(data,'PLANE_LAYER_CONFLICT')
        data=self.draft().model_dump();m=next(m for m in data['meanings'] if m['nodeId']=='activation');m.update(altitude='strategy',parentId='hook-runtime')
        self.rejects(data,'ALTITUDE_INVERSION')

    def test_evidence_and_port_sugar_validate_target_kinds(self):
        text=self.text().replace('requires-port live-probe-port;','requires-port probe-testimony;',1)
        with self.assertRaisesRegex(ValueError,'INVALID_SUGAR_RELATION'):parse(text)
        text=self.text().replace('requires-port live-probe-port;','requires-port not-declared;',1)
        with self.assertRaises(DiagnosticError) as caught:parse(text)
        self.assertEqual(caught.exception.diagnostic['code'],'UNKNOWN_RELATION_TARGET')
        self.assertIn('unmanaged-probe',caught.exception.diagnostic['message'])

    def test_typed_proved_and_observed_do_not_become_draft_authority(self):
        for basis in ('PROVED','OBSERVED','CANDIDATE'):
            text=self.text('my-circuit').replace('label "Make it happen";',f'label "Make it happen"; basis {basis};')
            with self.assertRaises(ValueError):parse(text)

    def test_unknown_fields_duplicate_ids_and_nonfinite_values_reject(self):
        for bad in [self.text('my-circuit').replace('responsibility ', 'made-up-field '),
                    self.text('my-circuit').replace('then result','then work'),
                    self.text('my-circuit').replace('responsibility "What mechanic changes the situation?";', 'variants [NaN];')]:
            with self.assertRaises(ValueError):parse(bad)

    def test_syntax_diagnostic_has_source_location_and_repair_hint(self):
        text=self.text('my-circuit').replace('label "Make it happen";','label "Make it happen"')
        with self.assertRaises(DiagnosticError) as caught:parse(text)
        d=caught.exception.diagnostic;self.assertEqual(d['code'],'SCL_SYNTAX');self.assertGreater(d['line'],8)
        self.assertIn('semicolon',d['hint']);self.assertGreater(d['offset'],0)

    def test_contract_error_locates_the_authored_node(self):
        text=self.text('my-circuit').replace('responsibility "What mechanic changes the situation?";','plane sideways;')
        with self.assertRaises(DiagnosticError) as caught:parse(text)
        d=caught.exception.diagnostic;self.assertEqual(d['line'],9);self.assertEqual(d['code'],'SCL_CONTRACT')

    def test_zero_one_errors_also_receive_clickable_diagnostics(self):
        text=emit(draft_from_projection('scenario-target')).replace('target "split";','target "missing";',1)
        try:parse(text)
        except ValueError as e:
            d=diagnostic(text,e);self.assertEqual(d['code'],'UNKNOWN_ENDPOINT');self.assertGreater(d['line'],1);self.assertIn('existing node',d['hint'])
        else:self.fail('Expected unknown endpoint')

    def test_material_render_retains_trace_planes_and_open_proof(self):
        g=self.draft();a=compile_graph(g,enhanced=False);b=compile_graph(g,enhanced=True)
        from enhance_infographics import strip_material
        self.assertEqual(strip_material(a['svg']),strip_material(b['svg']))
        self.assertEqual(a['projection'],b['projection'])
        self.assertEqual(b['receipt']['proofDisposition'],'NOT_ESTABLISHED')
        self.assertFalse(b['receipt']['evidenceRequirements'][0]['established'])
        self.assertEqual(b['projection']['semanticPlanes']['probe-testimony'],'evidence')
        self.assertEqual(len(b['projection']['traceGeometry'][0]['steps'][1]['paths']),2)

    def test_canonical_02_named_trace_blocks_normalize_without_semantic_loss(self):
        g=parse(self.text('my-circuit'));canonical=emit(g)
        canonical='\n'.join(line for line in canonical.splitlines() if not line.startswith(('  trace ','  traces ','  selectedTrace ')))
        block='  trace "a-story" { '+''.join('step '+json.dumps(e)+'; ' for e in g.trace)+'}\n'
        canonical=canonical.rsplit('}',1)[0]+block+'}'
        result=parse(canonical);self.assertEqual(result.selectedTrace,'a-story');self.assertEqual(result.trace,g.trace)

    def test_auto_identity_does_not_depend_on_labels(self):
        a=self.draft();b=parse(self.text().replace('Observe no unmanaged effect','Observe the denied attempt'))
        self.assertEqual([e.id for e in a.edges],[e.id for e in b.edges])
        self.assertEqual([n.id for n in a.nodes+a.junctions],[n.id for n in b.nodes+b.junctions])

    def test_canonical_02_preserves_existing_selection_and_product_mechanics(self):
        for identity in ('scenario-current','scenario-target','estate-target'):
            before=draft_from_projection(identity);after=parse(emit(before).replace('scl "0.1";','scl "0.2";',1))
            self.assertEqual([e.model_dump() for e in before.edges],[e.model_dump() for e in after.edges])
            self.assertEqual(before.trace,after.trace)
            if identity=='estate-target':
                data=after.model_dump();next(e for e in data['edges'] if e['type']=='product-transfer')['productContract']='wrong.v1'
                self.rejects(data,'PRODUCT_CONTRACT_MISMATCH')

    def test_canonical_02_keeps_bounded_retry_and_stop_requirements(self):
        data=parse(self.text('my-circuit')).model_dump();data.update(traces=[],selectedTrace=None,trace=[])
        stop={**data['nodes'][0],'id':'stop','type':'rejection','label':'Stop'};stop.pop('productContract');stop.pop('closure')
        data['junctions'].append(stop);data['scenarios'][0]['nodeIds'].append('stop')
        data['edges'].append({**data['edges'][0],'id':'retry','source':'work','target':'request','type':'retry','maxAttempts':3,'exitCondition':'ready','stopTarget':'stop'})
        self.assertEqual(validate_graph(data).edges[-1].maxAttempts,3)
        data['edges'][-1]['maxAttempts']=None;self.rejects(data,'UNBOUNDED_RETRY')

    def test_exported_schema_rejects_ambiguous_and_empty_trace_steps(self):
        from jsonschema import Draft202012Validator, ValidationError
        validator=Draft202012Validator(Circuit02.model_json_schema());data=self.draft().model_dump()
        validator.validate(data)
        for invalid in ({'edgeId':'e','paths':[[{'edgeId':'a'}],[{'edgeId':'b'}]]}, {'edgeId':None,'paths':None}, {'paths':[[],[]]}):
            changed=copy.deepcopy(data);changed['traces'][0]['steps'][0]=invalid
            with self.assertRaises(ValidationError):validator.validate(changed)


if __name__=='__main__':unittest.main(verbosity=2)
