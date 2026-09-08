"""Local browser QA of the media URL layout, before SQL publication."""
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class Handler(SimpleHTTPRequestHandler):
    def __init__(self,*args,**kwargs):super().__init__(*args,directory=str(ROOT),**kwargs)
    def translate_path(self,path):
        if path.startswith('/media/library/'):path=path[len('/media/library'):]
        return super().translate_path(path)
if __name__=='__main__':ThreadingHTTPServer(('127.0.0.1',3110),Handler).serve_forever()
