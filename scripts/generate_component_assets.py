"""Generate bounded, resumable Nano Banana material assets from the visual grammar.

These are isolated component treatments, not scenario illustrations or execution
evidence. The scene director and mechanics gate remain owned by generate_gemini.
"""
import argparse
import base64
import hashlib
import io
import json
import re
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

import cairosvg
import svgwrite
from PIL import Image

from generate_gemini import api_key
from infographic_contract import ROOT, read, write, digest
from compile_infographics import GRAMMAR, shape

DEST = ROOT / 'outputs/component-enhancements'
MANIFEST = ROOT / 'declarations/infographic-enhancement.v1.json'
STYLE = ROOT / 'docs/visual-assets/sidefx-visual-alphabet-enhanced.png'
MODEL = 'gemini-3-pro-image'
ART = {
    'input': 'A blue smoked-glass admission capsule. Rounded rectangle, broad bevel, layered optical edge, empty dark central face.',
    'event': 'A cyan beveled execution module. Machined chamfered corners, tiny warm energy glint along the right inner bevel, dark empty central face.',
    'outcome': 'An emerald horizontal capsule. Rounded pill silhouette, luminous glass lip, deep green translucent interior. No checkmark, badge, trophy or success symbol.',
    'provider-port': 'A sapphire socket with an unmistakable stepped plug receptacle on the LEFT. Two contact slots. Wide dark empty face. No provider inserted.',
    'provider': 'A violet machined provider module. A raised tab at upper left and narrow luminous vertical rail near the right edge. Dark empty central face.',
    'validation': 'A mint shield with a broad straight top and curved lower edge. Layered optical glass. The small check glyph is only the validation alphabet mark, never a passed badge.',
    'evidence': 'Three ice-blue thin document plates, stacked with small upward and right offsets. Deep dark front face with three short fine lines at upper right. No seal or check.',
    'human-approval': 'An amber gate frame enclosing the simple person pictogram at upper right, exactly as the guide. Golden glass, subtle machined details. No tick or approval badge.',
    'authority': 'An ivory-gold authority frame with a thick top band and a slim left interior rail. Architectural, precise. Empty face. No courthouse, scales or invented icon.',
    'branch': 'Exactly one incoming light channel at left diverges to exactly TWO outgoing channels at right. A fine machined Y fork. No arrows, extra branches or enclosing plate.',
    'fan-out': 'One inlet at left enters a circular glass hub. Exactly TWO spokes leave upper right and lower right. Crisp radial geometry. No extra spokes, arrows or enclosing plate.',
    'convergence': 'Exactly TWO incoming channels at upper left and lower left merge into exactly ONE horizontal channel to the right. A luminous precision combiner. No arrows or enclosing plate.',
    'decision': 'One horizontal diamond, four clean sharp corners. Cyan optical glass with a dark empty center. No smaller diamonds, question marks, arrows or extra paths.',
    'termination': 'A solid ice-blue circular end cap with a separate vertical stop bar on its left, exactly as the guide. It is a closed disk, never a hollow portal or ring.',
    'rejection': 'A coral-red chamfered octagonal hold module. Thin machined rim, dark empty face, one small horizontal minus bar at upper right. No other icon.',
}


def prepare():
    DEST.mkdir(parents=True, exist_ok=True)
    (DEST / 'guides').mkdir(exist_ok=True)
    specs = GRAMMAR['nodeTypes'] | GRAMMAR['junctionTypes']
    assets = []
    for kind, spec in specs.items():
        d = svgwrite.Drawing(size=(1024, 1024), viewBox='0 0 1024 1024', debug=False)
        d.add(d.rect((0, 0), (1024, 1024), fill='#000000'))
        # Enlarge the real primitive uniformly; fixed-size notches and junction
        # arms must scale with it instead of becoming tiny ambiguous details.
        pw, ph = (160, 174) if kind in GRAMMAR['junctionTypes'] else (300, 170)
        scale = min(680 / pw, 420 / ph)
        glyph = d.g(transform=f'translate({512-pw*scale/2},{512-ph*scale/2}) scale({scale})')
        shape(d, glyph, kind, 0, 0, pw, ph, spec['color'], fill='#06111b')
        d.add(glyph)
        guide = DEST / 'guides' / (kind + '.png')
        cairosvg.svg2png(bytestring=d.tostring().encode(), write_to=str(guide))
        prompt = (
            'Use case: stylized-concept. Asset: ONE isolated reusable SideFX component material plate.\n'
            'Image 1 is style reference only: its luminous machined glass, material depth and controlled energy. '
            'Do not copy its poster layout, labels, captions, logos or surrounding cards.\n'
            'Image 2 is the EXACT shape and placement guide for this asset. Preserve its silhouette, '
            'orientation, number of parts and position. It is not a request to design a new symbol.\n'
            f'Component: {spec["label"]}. Semantic role: {spec["meaning"]}\n'
            f'Art direction: {ART[kind]}\n'
            f'Primary family color: {spec["color"]}. Material: smoked optical glass, polished titanium microbevels, '
            'fine internal reflections, photoreal product-render lighting. BRILLIANT luminous colored optical edges '
            'with a bright white-hot thin core and saturated family-color halo, like the style reference. '
            'The colored emission is the hero. Avoid dull silver, gray chrome and underlit objects.\n'
            'Composition: 1024 square, front orthographic view, horizontal component matching image 2. '
            'Very shallow extrusion only. Keep guide silhouette and location exact; do not rotate or tilt. '
            'Pure BLACK background all the way to the four image edges; isolated object, no floor, no environment. '
            'Keep a broad uninterrupted near-black central face for vector labels to be composited later. '
            'Concentrate detail on the perimeter and material surface. Tight saturated glow, polished highlights. '
            'For branch, fan-out and convergence, each line is a slender glowing solid cable; the space between '
            'cables stays pure black. Never fill or enclose the spaces between cables. No plate or horizontal borders.\n'
            'Absolutely NO text, letters, numbers, logo, labels, words, watermark, arrows, status badges, '
            'additional connections, floating particles, starfield, poster frame, grid or enclosing box. '
            'No claims of proven, active, passed or deployed state. Output exactly ONE image, not a contact sheet.'
        )
        assets.append({'id': kind, 'label': spec['label'], 'semanticShape': spec['shape'],
                       'prompt': prompt, 'guide': guide.relative_to(ROOT).as_posix(),
                       'guideSha256': digest(guide), 'receipt': f'outputs/component-enhancements/{kind}/receipt.json'})
    write(MANIFEST, {
        'version': 'sidefx-component-enhancement.v1', 'model': MODEL,
        'grammar': 'declarations/infographic-grammar.v1.json',
        'grammarSha256': digest(ROOT / 'declarations/infographic-grammar.v1.json'),
        'styleReference': STYLE.relative_to(ROOT).as_posix(), 'styleReferenceSha256': digest(STYLE),
        'scope': 'Decorative component artwork only. No scenario facts, layout, connectivity, labels or evidence status are generated.',
        'compositing': 'Generated color is masked by canonical primitive geometry. Original vector contours, labels, ports and edge paths stay intact.',
        'assets': assets,
    })
    return read(MANIFEST)


def component_request(manifest, asset):
    if digest(ROOT / manifest['grammar']) != manifest['grammarSha256']:
        raise ValueError('STALE_COMPONENT_GRAMMAR')
    parts = [{'text': asset['prompt']}]
    for path, expected in [(ROOT / manifest['styleReference'], manifest['styleReferenceSha256']),
                           (ROOT / asset['guide'], asset['guideSha256'])]:
        if digest(path) != expected:
            raise ValueError('STALE_COMPONENT_REFERENCE')
        parts.append({'inlineData': {'mimeType': 'image/png', 'data': base64.b64encode(path.read_bytes()).decode()}})
    model = manifest['model']
    if not re.fullmatch(r'[a-zA-Z0-9_.-]+', model):
        raise ValueError('INVALID_COMPONENT_MODEL')
    payload = json.dumps({'contents': [{'parts': parts}], 'generationConfig': {
        'responseModalities': ['TEXT', 'IMAGE'], 'imageConfig': {'aspectRatio': '1:1', 'imageSize': '1K'}}}).encode()
    identity = hashlib.sha256(model.encode() + payload).hexdigest()
    return model, payload, identity


def generate(manifest, asset, key):
    model, payload, identity = component_request(manifest, asset)
    folder = DEST / asset['id']; folder.mkdir(exist_ok=True)
    receipt_path = ROOT / asset['receipt']
    if receipt_path.exists():
        prior = read(receipt_path)
        write(folder / (prior['requestSha256'] + '.receipt.json'), prior)
        if prior.get('requestSha256') == identity:
            if prior.get('status') == 'GENERATED' and digest(ROOT / prior['image']) == prior['imageSha256']:
                return asset['id'], 'RESUMED'
            if prior.get('status') in ('REQUEST_IN_FLIGHT', 'NETWORK_UNCERTAIN'):
                raise ValueError('UNCERTAIN_PRIOR_REQUEST:' + asset['id'])
    receipt = {'assetId': asset['id'], 'provider': 'Gemini', 'model': model, 'requestSha256': identity,
               'grammarSha256': manifest['grammarSha256'], 'guideSha256': asset['guideSha256'],
               'styleReferenceSha256': manifest['styleReferenceSha256'], 'semanticReview': 'REQUIRED',
               'status': 'REQUEST_IN_FLIGHT'}
    write(receipt_path, receipt)
    request = urllib.request.Request('https://generativelanguage.googleapis.com/v1beta/models/' + model + ':generateContent',
                                     data=payload, headers={'Content-Type': 'application/json', 'x-goog-api-key': key})
    response = None
    for attempt in range(4):
        try:
            with urllib.request.urlopen(request, timeout=240) as stream:
                response = json.load(stream)
            break
        except urllib.error.HTTPError as exc:
            if exc.code not in (429, 500, 502, 503, 504) or attempt == 3:
                write(receipt_path, {**receipt, 'status': 'HTTP_FAILED', 'httpStatus': exc.code})
                raise ValueError(f'COMPONENT_HTTP_{exc.code}:' + asset['id']) from None
            time.sleep(min(2 ** attempt, 8))
        except (TimeoutError, urllib.error.URLError):
            write(receipt_path, {**receipt, 'status': 'NETWORK_UNCERTAIN'})
            raise ValueError('NETWORK_UNCERTAIN:' + asset['id']) from None
    images = [part['inlineData'] for candidate in response.get('candidates', [])
              for part in candidate.get('content', {}).get('parts', [])
              if part.get('inlineData', {}).get('mimeType', '').startswith('image/') and not part.get('thought')]
    if len(images) != 1:
        write(receipt_path, {**receipt, 'status': 'IMAGE_CARDINALITY', 'count': len(images)})
        raise ValueError('COMPONENT_IMAGE_CARDINALITY:' + asset['id'])
    data = base64.b64decode(images[0]['data'], validate=True)
    image = Image.open(io.BytesIO(data)); image.load()
    path = folder / (identity + '.' + image.format.lower().replace('jpeg', 'jpg'))
    path.write_bytes(data)
    completed = {**receipt, 'status': 'GENERATED', 'image': path.relative_to(ROOT).as_posix(),
                        'imageSha256': digest(path), 'width': image.width, 'height': image.height,
                        'usage': response.get('usageMetadata'), 'finishReasons': [c.get('finishReason') for c in response.get('candidates', [])]}
    write(receipt_path, completed)
    write(folder / (identity + '.receipt.json'), completed)
    return asset['id'], 'GENERATED'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prepare', action='store_true')
    parser.add_argument('--execute', action='store_true')
    parser.add_argument('--only', nargs='+', choices=list(ART))
    parser.add_argument('--workers', type=int, default=3, choices=range(1, 4))
    args = parser.parse_args()
    manifest = prepare() if args.prepare or not MANIFEST.exists() else read(MANIFEST)
    assets = [a for a in manifest['assets'] if not args.only or a['id'] in args.only]
    if not args.execute:
        print('PREPARED', len(assets), 'component requests; no provider calls.'); return
    key = api_key()
    if not key: raise SystemExit('LOC_GEMINI_API_KEY is unavailable.')
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(generate, manifest, asset, key) for asset in assets]
        for future in as_completed(futures):
            kind, status = future.result(); print(status, kind, flush=True)


if __name__ == '__main__':
    main()
