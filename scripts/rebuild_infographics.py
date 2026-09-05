"""Reproduce and validate the complete local infographic reference."""
import argparse
import subprocess
import sys
from infographic_contract import ROOT,read,write

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--skip-motion',action='store_true');args=parser.parse_args()
    steps=['setup_infographic_runtime.py','infographic_contract.py','prepare_infographic_examples.py','compile_infographics.py']
    if not args.skip_motion:steps.append('animate_infographic.py')
    steps.append('build_infographic_studio.py')
    for step in steps:subprocess.run([sys.executable,str(ROOT/'scripts'/step)],cwd=ROOT,check=True)
    result=subprocess.run([sys.executable,'-m','unittest','discover','-s','scripts','-p','test_infographic_grammar.py','-v'],cwd=ROOT,capture_output=True,text=True)
    print(result.stdout+result.stderr)
    (ROOT/'evaluations/infographic-conformance.txt').write_text(result.stdout+result.stderr,encoding='utf-8')
    report=read('evaluations/infographic-compiler-report.json');report['conformance']='PASS' if result.returncode==0 else 'FAIL';report['testLog']='evaluations/infographic-conformance.txt';write('evaluations/infographic-compiler-report.json',report)
    if result.returncode:raise SystemExit(result.returncode)

if __name__=='__main__':main()
