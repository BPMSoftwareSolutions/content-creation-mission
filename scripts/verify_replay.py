"""Rerun preparation and compare every non-evaluation artifact byte for byte."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def snapshot():
    result = {}
    for folder in ('inventories', 'outputs', 'samples', 'data/source-features'):
        for path in sorted((ROOT / folder).rglob('*')):
            if path.is_file() and 'generated' not in path.relative_to(ROOT).parts:
                result[path.relative_to(ROOT).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result


before = snapshot()
source = json.loads((ROOT / 'data/source-manifest.json').read_text())['sourceRoot']
subprocess.run([sys.executable, str(ROOT / 'scripts/content_lab.py'), '--source', source, '--samples', '20',
                '--formats', ','.join(json.loads((ROOT / 'data/generation-recipes.json').read_text()))], check=True, stdout=subprocess.DEVNULL)
after = snapshot()
changed = sorted(k for k in before.keys() | after.keys() if before.get(k) != after.get(k))
receipt = {'status': 'PASS' if not changed else 'FAIL', 'filesCompared': len(after), 'changedFiles': changed,
           'scope': 'Preparation artifacts; not Gemini image determinism'}
(ROOT / 'evaluations/replay-report.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(receipt, indent=2))
raise SystemExit(bool(changed))
