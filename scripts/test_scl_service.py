import copy
import json
import threading
import unittest
from http.server import ThreadingHTTPServer
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from infographic_contract import ROOT
from scl import parse, emit, validate_graph
from build_scl_studio import starter_scl
from serve_scl import SCLHandler


class SCLServiceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server=ThreadingHTTPServer(('127.0.0.1',0),SCLHandler)
        cls.thread=threading.Thread(target=cls.server.serve_forever,daemon=True);cls.thread.start()
        cls.url=f'http://127.0.0.1:{cls.server.server_port}'
    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown();cls.server.server_close();cls.thread.join()
    def post(self,data):
        request=Request(self.url+'/api/draft',data=json.dumps(data).encode(),headers={'Content-Type':'application/json'})
        try:
            with urlopen(request,timeout=20) as response:return response.status,json.load(response)
        except HTTPError as response:return response.code,json.load(response)
    def starter(self):return (ROOT/'declarations/scl/my-circuit.v02.scl').read_text(encoding='utf-8')

    def test_health_explicitly_advertises_both_language_versions(self):
        with urlopen(self.url+'/api/health') as response:data=json.load(response)
        self.assertEqual(data['languages'],['0.1','0.2']);self.assertEqual(data['effects'],'NONE')

    def test_both_versions_reach_the_same_service_with_authored_text_receipts(self):
        import hashlib
        for text,version in ((starter_scl(),'0.1'),(self.starter(),'0.2')):
            status,data=self.post({'scl':text,'enhanced':False});self.assertEqual(status,200)
            self.assertEqual(data['graph']['version'],'sidefx-circuit.v'+version)
            self.assertEqual(data['receipt']['authoredTextSha256'],hashlib.sha256(text.encode()).hexdigest())

    def test_authored_named_trace_selection_is_not_replaced_by_first_trace(self):
        data=parse(self.starter()).model_dump();alternate=copy.deepcopy(data['traces'][0]);alternate['id']='alternate'
        data['traces'].append(alternate);data['selectedTrace']='alternate';text=emit(validate_graph(data))
        status,result=self.post({'scl':text,'enhanced':False});self.assertEqual(status,200)
        self.assertEqual(result['graph']['selectedTrace'],'alternate')
        status,result=self.post({'scl':text,'traceId':data['traces'][0]['id'],'enhanced':False})
        self.assertEqual(result['graph']['selectedTrace'],data['traces'][0]['id'])

    def test_scenario_switch_selects_its_own_trace_and_rejects_wrong_explicit_trace(self):
        text='''scl 0.2; capability two { promise "Two views";
          scenario first { given a "A"; when b "B"; then c "C"; }
          scenario second { given d "D"; when e "E"; then f "F"; }
        }'''
        status,data=self.post({'scl':text,'scenarioId':'second','enhanced':False});self.assertEqual(status,200)
        self.assertEqual(data['graph']['selectedTrace'],'second.flow')
        status,data=self.post({'scl':text,'scenarioId':'second','traceId':'first.flow','enhanced':False})
        self.assertEqual(status,422);self.assertIn('TRACE_SCENARIO_MISMATCH',data['error'])

    def test_invalid_source_returns_repairable_diagnostic_not_partial_preview(self):
        text=self.starter().replace('label "Make it happen";', 'label "Make it happen"')
        status,data=self.post({'scl':text});self.assertEqual(status,422)
        self.assertEqual(data['diagnostic']['code'],'SCL_SYNTAX');self.assertGreater(data['diagnostic']['line'],1)
        self.assertIn('semicolon',data['diagnostic']['hint']);self.assertNotIn('svg',data)

    def test_unproved_draft_basis_explains_the_evidence_boundary(self):
        text=self.starter().replace('label "Make it happen";', 'label "Make it happen"; basis PROVED;')
        status,data=self.post({'scl':text});self.assertEqual(status,422)
        self.assertEqual(data['diagnostic']['code'],'DRAFT_BASIS');self.assertIn('execution evidence',data['diagnostic']['hint'])


if __name__=='__main__':unittest.main(verbosity=2)
