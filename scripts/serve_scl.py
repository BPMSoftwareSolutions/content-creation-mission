"""Loopback workbench: parse data and render SVG; never invoke a capability."""
import argparse
import json
from http.server import ThreadingHTTPServer
from urllib.parse import urlsplit
from serve_content import ContentHandler
from infographic_contract import ROOT
from scl import parse, graph_hash, emit, need, resolve_sources
from reveal_scl import reveal
from scl_render import compile_graph
from scl_v02 import Circuit02, select_trace, diagnostic


class SCLHandler(ContentHandler):
    def send_json(self, status, value):
        raw=json.dumps(value,ensure_ascii=False).encode();self.send_response(status)
        self.send_header('Content-Type','application/json; charset=utf-8');self.send_header('Content-Length',str(len(raw)))
        self.send_header('Cache-Control','no-store');self.end_headers();self.wfile.write(raw)
    def do_GET(self):
        if self.path=='/api/health': self.send_json(200,{'compiler':'scl.v0.2','languages':['0.1','0.2'],'effects':'NONE'})
        else: super().do_GET()
    def do_POST(self):
        data={}
        try:
            expected=f'127.0.0.1:{self.server.server_port}'
            need(self.headers.get('Host')==expected, 'INVALID_HOST')
            need(self.headers.get('Origin') in (None,'http://'+expected), 'CROSS_ORIGIN_REQUEST')
            need(self.headers.get('Content-Type','').split(';')[0]=='application/json', 'JSON_REQUIRED')
            size=int(self.headers.get('Content-Length','0'));need(0<size<=8_000_000,'REQUEST_SIZE')
            data=json.loads(self.rfile.read(size));need(isinstance(data,dict),'JSON_OBJECT_REQUIRED')
            if self.path=='/api/reveal':
                g=reveal(data['capabilityId'])
            elif self.path=='/api/native':
                from scl_native import native_view
                self.send_json(200,native_view(reveal(data['capabilityId']),data.get('cellId')));return
            elif self.path=='/api/draft':
                g=parse(data['scl']);need(g.status=='DRAFT','EDITOR_REQUIRES_DRAFT')
                need(len(g.nodes)+len(g.junctions)<=80 and len(g.edges)<=200,'DRAFT_PREVIEW_SIZE')
            elif self.path=='/api/record':
                g=reveal(data['capabilityId']);r=next(r for r in g.records if r.id==data['recordId'])
                s=next(s for s in g.sources if s.id==r.sourceRef)
                self.send_json(200,dict(record=r.model_dump(),source=s.model_dump(),value=resolve_sources([s])[s.id]));return
            else: self.send_json(404,{'error':'UNKNOWN_ENDPOINT'});return
            scenario=data.get('scenarioId') or g.scenarios[0].id
            if isinstance(g,Circuit02) and g.traces:
                authored=next((t.id for t in g.traces if t.id==g.selectedTrace and t.scenarioId==scenario),None)
                selected=data.get('traceId') or authored or next((t.id for t in g.traces if t.scenarioId==scenario),None)
                need(selected is not None,'NO_TRACE_FOR_SCENARIO')
                g=select_trace(g,selected)
                need(next(t for t in g.traces if t.id==selected).scenarioId==scenario,'TRACE_SCENARIO_MISMATCH')
            result=compile_graph(g,scenario,data.get('enhanced',True))
            if self.path=='/api/draft':
                import hashlib
                result['receipt']['authoredTextSha256']=hashlib.sha256(data['scl'].encode()).hexdigest()
            self.send_json(200,dict(**result,graph=g.model_dump(),scl=emit(g),graphSha256=graph_hash(g)))
        except (ValueError,KeyError,StopIteration,TypeError,OSError) as e:
            source=data.get('scl','') if isinstance(data,dict) else ''
            self.send_json(422,{'error':str(e)[:2500] or 'UNRESOLVED_IDENTITY','diagnostic':diagnostic(source,e) if isinstance(source,str) else None})
    def log_message(self,format,*args): pass


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=8766);a=p.parse_args()
    print(f'SCL workbench: http://127.0.0.1:{a.port}/samples/scl/index.html',flush=True)
    ThreadingHTTPServer(('127.0.0.1',a.port),SCLHandler).serve_forever()
