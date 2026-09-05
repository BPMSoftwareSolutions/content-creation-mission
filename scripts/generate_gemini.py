"""Bounded, resumable Gemini manifest consumer. Dry-run is the default."""
import argparse
import base64
import hashlib
import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def api_key():
    key = os.environ.get('LOC_GEMINI_API_KEY') or os.environ.get('GEMINI_API_KEY')
    if key or os.name != 'nt':
        return key
    import winreg
    for hive, path in ((winreg.HKEY_CURRENT_USER, 'Environment'),
                       (winreg.HKEY_LOCAL_MACHINE, r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment')):
        try:
            with winreg.OpenKey(hive, path) as handle:
                return winreg.QueryValueEx(handle, 'LOC_GEMINI_API_KEY')[0]
        except OSError:
            continue
    return None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, default=ROOT / 'samples/generation-manifest.json')
    parser.add_argument('--limit', type=int, default=1)
    parser.add_argument('--model', help='Optional explicit model override')
    parser.add_argument('--execute', action='store_true', help='Send requests to Gemini (billable)')
    parser.add_argument('--offset', type=int, default=0)
    parser.add_argument('--reference', type=Path, help='Local PNG/JPEG style reference')
    args = parser.parse_args()
    if args.limit < 1:
        parser.error('--limit must be positive')
    jobs = json.loads(args.manifest.read_text(encoding='utf-8'))[args.offset:args.offset + args.limit]
    if not args.execute:
        print(json.dumps({'mode': 'DRY_RUN', 'requests': len(jobs), 'models': sorted({args.model or j['model'] for j in jobs}), 'ids': [j['id'] for j in jobs]}, indent=2))
        return
    key = api_key()
    if not key:
        parser.error('Set LOC_GEMINI_API_KEY in the Windows environment; never place it in a manifest')
    output = ROOT / 'outputs/generated'
    output.mkdir(parents=True, exist_ok=True)
    for job in jobs:
        from mechanics_gate import validate_grounding
        grounded = validate_grounding(job)
        job['request']['contents'][0]['parts'].append({'text':
            'Mandatory mechanic-grounded direction. Preserve these source-backed facts and motion beats. '
            'Fixture expectations are not observed execution. Do not invent provider substitutions or side effects.\n' +
            json.dumps({**{k:grounded[k] for k in ('source','visualDirection','animationBeats','groundingReview')},
                        'selectedFixture':grounded.get('selectedFixture'),
                        'mechanics':grounded['evidence']['mechanics'],
                        'providers':grounded['evidence']['providers'],
                        'execution':grounded['evidence']['execution']})})
        direction = job.get('director')
        if not direction:
            raise SystemExit('DIRECTOR_REQUIRED: compile explicit shots with direct_visual_experience.py before live generation')
        if len({direction[p]['camera'] for p in ('input','event','outcome')}) != 3:
            raise SystemExit('VISUAL_PHASE_COLLAPSE: director repeats camera composition')
        if len({direction[p]['action'] for p in ('input','event','outcome')}) != 3:
            raise SystemExit('VISUAL_PHASE_COLLAPSE: director repeats phase behavior')
        model = args.model or job['model']
        if not all(c.isalnum() or c in '-._' for c in model):
            parser.error('Invalid model identifier')
        if args.reference:
            mime = 'image/png' if args.reference.suffix.lower() == '.png' else 'image/jpeg'
            job['request']['contents'][0]['parts'].append({'inlineData': {'mimeType': mime, 'data': base64.b64encode(args.reference.read_bytes()).decode()}})
        if job.get('singleFrameOnly'):
            job['request']['contents'][0]['parts'].append({'text':
                'FINAL RENDER INSTRUCTION: All preceding multi-phase direction is continuity context only. '
                'Output ONE uninterrupted 16:9 photograph for this ONE shot: '+job['shot']['direction']+
                ' Absolutely NO grid, NO collage, NO split screen, NO storyboard, NO panels. '
                'Show the person only once in the rightmost third. Left two thirds remain unoccupied dark space.'})
        payload = json.dumps(job['request']).encode()
        identity = hashlib.sha256(model.encode() + payload).hexdigest()
        receipt_path = output / (identity + '.json')
        if receipt_path.exists():
            receipt = json.loads(receipt_path.read_text())
            if receipt.get('status') == 'GENERATED' and all((output / f['path']).exists() and hashlib.sha256((output / f['path']).read_bytes()).hexdigest() == f['sha256'] for f in receipt['images']):
                print('RESUMED', job['id'])
                continue
        request = urllib.request.Request('https://generativelanguage.googleapis.com/v1beta/models/' + model + ':generateContent',
            data=payload, headers={'Content-Type': 'application/json', 'x-goog-api-key': key})
        response = None
        for attempt in range(4):
            try:
                with urllib.request.urlopen(request, timeout=180) as stream:
                    response = json.load(stream)
                break
            except urllib.error.HTTPError as exc:
                if exc.code not in (429, 500, 502, 503, 504) or attempt == 3:
                    receipt_path.write_text(json.dumps({'status': 'HTTP_FAILED', 'httpStatus': exc.code, 'jobId': job['id']}))
                    raise SystemExit(f'Gemini HTTP {exc.code}; stopped without logging credentials') from None
                time.sleep(min(2 ** attempt, 8))
            except (TimeoutError, urllib.error.URLError):
                raise SystemExit('Network outcome uncertain; stopped. Review provider usage before retrying.') from None
        images = []
        for candidate in response.get('candidates', []):
            for part in candidate.get('content', {}).get('parts', []):
                inline = part.get('inlineData', {})
                mime = inline.get('mimeType')
                if mime in ('image/png', 'image/jpeg', 'image/webp'):
                    data = base64.b64decode(inline['data'], validate=True)
                    ext = {'image/png': '.png', 'image/jpeg': '.jpg', 'image/webp': '.webp'}[mime]
                    name = identity + '-' + str(len(images)) + ext
                    (output / name).write_bytes(data)
                    images.append({'path': name, 'sha256': hashlib.sha256(data).hexdigest()})
        receipt_path.write_text(json.dumps({'status': 'GENERATED' if images else 'NO_IMAGE', 'jobId': job['id'],
            'requestDigest': identity, 'model': model, 'images': images, 'semanticReview': 'REQUIRED',
            'finishReasons': [c.get('finishReason') for c in response.get('candidates', [])]}, indent=2))
        if not images:
            raise SystemExit('Provider returned no image; inspect receipt before retrying')
        print('GENERATED', job['id'], len(images))


if __name__ == '__main__':
    main()
