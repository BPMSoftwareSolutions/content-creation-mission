"""Loopback-only content preview with byte ranges for chapter-addressable media."""
import argparse
import os
import re
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

class ContentHandler(SimpleHTTPRequestHandler):
    def __init__(self,*args,**kwargs):super().__init__(*args,directory=str(ROOT),**kwargs)

    def end_headers(self):
        self.send_header('Accept-Ranges','bytes')
        super().end_headers()

    def send_head(self):
        self.remaining=None
        requested=self.headers.get('Range')
        path=Path(self.translate_path(self.path))
        if not requested or not path.is_file():return super().send_head()
        match=re.fullmatch(r'bytes=(\d*)-(\d*)',requested.strip())
        size=path.stat().st_size
        start,end=0,-1
        if match and any(match.groups()):
            first,last=match.groups()
            if first:
                start=int(first);end=min(int(last),size-1) if last else size-1
            elif int(last)>0:
                start=max(0,size-int(last));end=size-1
        if start<0 or start>=size or end<start:
            self.send_response(416)
            self.send_header('Content-Range',f'bytes */{size}')
            self.send_header('Content-Length','0')
            self.end_headers()
            return None
        try:source=path.open('rb')
        except OSError:
            self.send_error(404,'File not found');return None
        source.seek(start);self.remaining=end-start+1
        self.send_response(206)
        self.send_header('Content-Type',self.guess_type(str(path)))
        self.send_header('Content-Range',f'bytes {start}-{end}/{size}')
        self.send_header('Content-Length',str(self.remaining))
        self.send_header('Last-Modified',self.date_time_string(os.fstat(source.fileno()).st_mtime))
        self.end_headers()
        return source

    def copyfile(self,source,output):
        try:
            if self.remaining is None:return super().copyfile(source,output)
            remaining=self.remaining
            while remaining:
                chunk=source.read(min(65536,remaining))
                if not chunk:break
                output.write(chunk);remaining-=len(chunk)
        except (BrokenPipeError,ConnectionResetError,ConnectionAbortedError):
            pass  # The viewer sought elsewhere or left the page.

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--port',type=int,default=8765)
    args=parser.parse_args()
    print(f'Content preview: http://127.0.0.1:{args.port}/samples/season-1/index.html',flush=True)
    ThreadingHTTPServer(('127.0.0.1',args.port),ContentHandler).serve_forever()
