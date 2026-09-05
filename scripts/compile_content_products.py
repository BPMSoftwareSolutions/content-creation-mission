"""Validate capability content contracts and compile their permitted media surfaces."""
import hashlib
import html
import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = ROOT / "declarations/capability-content"
SITE = ROOT / "samples/content-catalog"
PRODUCT = SITE / "generate-governed-narration"
ALL_SURFACES = {"video", "short", "thumbnail", "article", "infographic", "training", "demo", "landing-page", "evidence-story"}


def read(path):
    return json.loads(path.read_bytes())


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def esc(value):
    return html.escape(str(value))


def validate_contracts():
    schema = read(ROOT / "schemas/capability-content-contract.schema.json")
    validator = Draft202012Validator(schema)
    contracts = []
    errors = []
    for path in sorted(CONTRACTS.glob("*.json")):
        contract = read(path)
        for error in validator.iter_errors(contract):
            errors.append(f"{path.name}:{'/'.join(map(str, error.path))}:{error.message}")
        if path.stem != contract.get("capabilityId"):
            errors.append(f"{path.name}:capabilityId does not match filename")
        if contract["status"] == "EDITORIALLY_REVIEWED":
            claim_ids = {claim["id"] for claim in contract["claims"]}
            evidence_ids = {evidence["id"] for evidence in contract["evidence"]}
            if set(contract["permittedSurfaces"]) != set(contract["surfaceContracts"]):
                errors.append(f"{path.name}:permitted surfaces and surface contracts differ")
            for surface, projection in contract["surfaceContracts"].items():
                if not set(projection["claimIds"]).issubset(claim_ids):
                    errors.append(f"{path.name}:{surface}:unknown claim reference")
                if not set(projection["evidenceIds"]).issubset(evidence_ids):
                    errors.append(f"{path.name}:{surface}:unknown evidence reference")
            for claim in contract["claims"]:
                if not set(claim["evidenceIds"]).issubset(evidence_ids):
                    errors.append(f"{path.name}:{claim['id']}:unknown evidence reference")
            for evidence in contract["evidence"]:
                evidence_path = ROOT / evidence["path"]
                if not evidence_path.is_file():
                    errors.append(f"{path.name}:{evidence['id']}:missing evidence")
                elif digest(evidence_path) != evidence["sha256"]:
                    errors.append(f"{path.name}:{evidence['id']}:digest mismatch")
        contracts.append(contract)
    if len(contracts) != 219:
        errors.append(f"expected 219 contracts, found {len(contracts)}")
    if errors:
        raise ValueError("CONTRACT_VALIDATION_FAILED\n" + "\n".join(errors))
    return contracts


CSS = """
:root{--ink:#f3f0e8;--muted:#9badb9;--cyan:#6edfdc;--amber:#edbc77;--red:#ed8776;--bg:#061019;--panel:#0d1d28;--line:#25404d}*{box-sizing:border-box}body{margin:0;background:radial-gradient(circle at 75% 8%,#163642 0,transparent 32%),var(--bg);color:var(--ink);font:16px/1.55 Segoe UI,system-ui,sans-serif}a{color:inherit}.shell{max-width:1180px;margin:auto;padding:26px}.brand{display:flex;justify-content:space-between;align-items:center;letter-spacing:.24em;font-size:13px}.brand a{text-decoration:none}.eyebrow{color:var(--cyan);font-size:12px;letter-spacing:.18em;text-transform:uppercase;font-weight:700}.hero{display:grid;grid-template-columns:1.05fr .95fr;gap:42px;align-items:center;padding:82px 0 46px}h1{font-size:clamp(46px,7vw,88px);line-height:.96;margin:12px 0 24px;letter-spacing:-.055em}h2{font-size:34px;line-height:1.1;margin:56px 0 18px}h3{font-size:19px;margin:0 0 8px}.lead{font-size:21px;color:#c6d0d5;max-width:720px}.card,.surface,.claim,.quiz{background:rgba(13,29,40,.88);border:1px solid var(--line);border-radius:16px;padding:24px}.visual{width:100%;border-radius:18px;border:1px solid #365260;box-shadow:0 24px 80px #0009}video{width:100%;border-radius:16px;background:#000}.pills{display:flex;flex-wrap:wrap;gap:8px;margin:22px 0}.pill{border:1px solid var(--line);border-radius:999px;padding:7px 11px;font-size:12px;color:#c6d0d5}.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}.surface{text-decoration:none;display:block;transition:.18s transform,.18s border-color}.surface:hover{transform:translateY(-3px);border-color:var(--cyan)}.surface span{color:var(--cyan);font-size:12px;letter-spacing:.12em}.flow{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}.flow>div{padding:22px;border-left:3px solid var(--cyan);background:#0b1a24}.flow small,.muted{color:var(--muted)}.claims{display:grid;gap:12px}.claim strong{color:var(--cyan)}.scope{border-left:3px solid var(--amber);padding:16px 22px;background:#191b1c}.button{display:inline-block;text-decoration:none;background:var(--cyan);color:#061019;font-weight:800;padding:12px 17px;border-radius:9px}.button.secondary{background:transparent;color:var(--ink);border:1px solid var(--line)}footer{margin-top:70px;padding:30px 0;border-top:1px solid var(--line);color:var(--muted)}.catalog-head{padding:80px 0 28px}.controls{display:flex;gap:10px;margin:24px 0}.controls input,.controls select{background:#0d1d28;color:var(--ink);border:1px solid var(--line);padding:12px;border-radius:8px}.controls input{flex:1}.catalog{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}.product{border:1px solid var(--line);border-radius:12px;padding:18px;background:#0b1922}.product.ready{border-color:#407f80}.product small{color:var(--muted)}.product a{text-decoration:none}.status{font-size:11px;color:var(--amber);letter-spacing:.09em}.ready .status{color:var(--cyan)}label.option{display:block;border:1px solid var(--line);padding:11px;margin:8px 0;border-radius:8px}.result{margin-top:14px;color:var(--cyan);font-weight:700}@media(max-width:780px){.hero,.grid,.flow,.catalog{grid-template-columns:1fr}.hero{padding-top:48px}.shell{padding:20px}h1{font-size:49px}}
"""


def page(title, body):
    return f"<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>{esc(title)}</title><style>{CSS}</style></head><body><main class='shell'><nav class='brand'><a href='../index.html'>SIDEFX / CONTENT ESTATE</a><span>CONTRACT PROJECTION</span></nav>{body}<footer>Meaning is authored once. Every surface projects the same reviewed contract.</footer></main></body></html>"


def evidence_links(contract):
    return "".join(f"<li><a href='../../../{esc(item['path'])}'>{esc(item['id'])}</a> <span class='muted'>{esc(item['kind'])} · {item['sha256'][:12]}</span></li>" for item in contract["evidence"])


def compile_product(contract):
    story = contract["storyTitle"]
    surfaces = contract["permittedSurfaces"]
    if set(surfaces) != ALL_SURFACES:
        raise ValueError("FIRST_PRODUCT_MUST_PROJECT_ALL_NINE_SURFACES")
    nav = "".join(f"<a class='surface' href='{ {'video':'../../narration-continuity/the-story-stays-hers.mp4','short':'../../narration-continuity/the-story-stays-hers-short.mp4','thumbnail':'../../narration-continuity/thumbnail-a.jpg','infographic':'infographic.svg','demo':'demo.html','landing-page':'index.html','evidence-story':'evidence.html'}.get(surface, surface+'.html')}'><span>{surface.upper()}</span><h3>{esc(contract['surfaceContracts'][surface]['structure'][0])}</h3></a>" for surface in surfaces)
    landing = f"""
    <section class='hero'><div><div class='eyebrow'>Capability content product / 01</div><h1>{esc(story)}</h1><p class='lead'>{esc(contract['humanProblem'])}</p><div class='pills'><span class='pill'>9 contract projections</span><span class='pill'>7 evidence-bound claims</span><span class='pill'>5 source scenarios</span></div><a class='button' href='../../narration-continuity/the-story-stays-hers.mp4'>Watch the 64-second film</a></div><img class='visual' src='../../narration-continuity/thumbnail-a.jpg' alt='Producer interrupted at her editing console'></section>
    <h2>The experience contract</h2><div class='flow'><div><small>INPUT</small><h3>{esc(contract['experience']['input'])}</h3></div><div><small>EVENT</small><h3>{esc(contract['experience']['event'])}</h3></div><div><small>OUTCOME</small><h3>{esc(contract['experience']['outcome'])}</h3></div></div>
    <h2>One capability. Nine surfaces.</h2><div class='grid'>{nav}</div><h2>Scope</h2><p class='scope'>{esc(contract['scope'])}</p>"""
    write(PRODUCT / "index.html", page(story, landing))

    article = f"""<article><section class='catalog-head'><div class='eyebrow'>Article projection</div><h1>{esc(story)}</h1><p class='lead'>{esc(contract['humanProblem'])}</p></section><h2>What the capability promises</h2><p>{esc(contract['claims'][0]['text'])}</p><h2>What happens underneath</h2>{''.join(f"<div class='card'><h3>{esc(m['meaning'])}</h3><span class='muted'>Evidence: {', '.join(map(esc,m['evidenceIds']))}</span></div>" for m in contract['mechanics'])}<h2>What we observed</h2><p>{esc(contract['claims'][3]['text'])} {esc(contract['claims'][4]['text'])} {esc(contract['claims'][5]['text'])}</p><h2>What it means for the producer</h2><p>{esc(contract['experience']['outcome'])}</p><h2>Interpretation boundary</h2><p class='scope'>{esc(contract['scope'])}</p></article>"""
    write(PRODUCT / "article.html", page("Article — " + story, article))

    evidence = f"""<section class='catalog-head'><div class='eyebrow'>Evidence story</div><h1>Every sentence has a source.</h1><p class='lead'>Claims are separated by authority: capsule declaration, observed local demo, or editorial staging.</p></section><div class='claims'>{''.join(f"<div class='claim'><strong>{esc(c['kind'])}</strong><h3>{esc(c['text'])}</h3><span class='muted'>Evidence: {', '.join(map(esc,c['evidenceIds']))}</span></div>" for c in contract['claims'])}</div><h2>Inspectable evidence</h2><ul>{evidence_links(contract)}</ul><h2>Claim boundary</h2><p class='scope'>{esc(contract['scope'])}</p>"""
    write(PRODUCT / "evidence.html", page("Evidence — " + story, evidence))

    demo = f"""<section class='catalog-head'><div class='eyebrow'>Executable demo projection</div><h1>Hear the artifact.</h1><p class='lead'>The request survives provider selection and becomes a hash-verified WAV.</p></section><div class='card'><h3>Actual generated narration</h3><audio controls src='../../narration-continuity/finished-narration.wav' style='width:100%'></audio><p class='muted'>{demo_asset_text()}</p></div><h2>Observed route</h2><div class='flow'><div><small>A</small><h3>Unavailable</h3><p>Injected failure</p></div><div><small>B</small><h3>Ineligible</h3><p>Text only</p></div><div><small>C</small><h3>Selected</h3><p>Live Gemini speech</p></div></div><p><a class='button secondary' href='../../../samples/narration-continuity/demo.receipt.json'>Inspect the receipt</a></p><p class='scope'>This is a local editorial demonstration. It is not managed capsule execution.</p>"""
    write(PRODUCT / "demo.html", page("Demo — " + story, demo))

    training_data = contract["training"]
    quiz = "".join(f"<div class='quiz' data-correct='{q['correct']}' data-rationale='{esc(q['rationale'])}'><h3>{i+1}. {esc(q['question'])}</h3>{''.join(f'<label class="option"><input type="radio" name="q{i}" value="{j}"> {esc(option)}</label>' for j,option in enumerate(q['options']))}<div class='result'></div></div>" for i,q in enumerate(training_data["questions"]))
    training = f"""<section class='catalog-head'><div class='eyebrow'>Training projection</div><h1>Provider selection is not completion.</h1><p class='lead'>{esc(training_data['objective'])}</p></section><h2>Scenario</h2><p>{esc(contract['experience']['event'])}</p><h2>Exercise</h2><p class='card'>{esc(training_data['exercise'])}</p><h2>Assessment</h2><div class='claims'>{quiz}</div><p><button class='button' id='grade'>Check answers</button></p><script>document.getElementById('grade').onclick=()=>{{document.querySelectorAll('.quiz').forEach(q=>{{const a=q.querySelector('input:checked');const ok=a&&a.value===q.dataset.correct;q.querySelector('.result').textContent=(ok?'Correct. ':'Try again. ')+q.dataset.rationale}})}};</script>"""
    write(PRODUCT / "training.html", page("Training — " + story, training))

    infographic = f"""<svg xmlns='http://www.w3.org/2000/svg' width='1200' height='1500' viewBox='0 0 1200 1500'><rect width='1200' height='1500' fill='#061019'/><style>text{{font-family:'Segoe UI',sans-serif;fill:#f3f0e8}}.m{{fill:#9badb9}}.c{{fill:#6edfdc}}.box{{fill:#0d1d28;stroke:#25404d;stroke-width:2}}.route{{stroke:#6edfdc;stroke-width:6;fill:none}}</style><text x='80' y='90' class='c' font-size='24' letter-spacing='8'>SIDEFX / CAPABILITY INFOGRAPHIC</text><text x='80' y='190' font-size='70' font-weight='700'>The provider changed.</text><text x='80' y='270' font-size='70' font-weight='700'>The story stayed hers.</text><text x='80' y='330' class='m' font-size='27'>{esc(contract['humanProblem'])}</text><rect class='box' x='80' y='420' width='1040' height='210' rx='24'/><text x='125' y='480' class='c' font-size='23'>INPUT / HUMAN INTENT</text><text x='125' y='545' font-size='38'>Marked script + waiting edit</text><text x='125' y='590' class='m' font-size='24'>Exact request digest retained</text><path class='route' d='M600 630 V710'/><rect class='box' x='80' y='710' width='1040' height='330' rx='24'/><text x='125' y='775' class='c' font-size='23'>EVENT / PROVIDER CONTINUITY</text><text x='135' y='860' font-size='42' fill='#ed8776'>A</text><text x='200' y='860' class='m' font-size='26'>UNAVAILABLE · SIMULATED</text><text x='135' y='930' font-size='42' fill='#edbc77'>B</text><text x='200' y='930' class='m' font-size='26'>INELIGIBLE · TEXT ONLY</text><text x='135' y='1000' class='c' font-size='42'>C</text><text x='200' y='1000' font-size='26'>SELECTED · LIVE AUDIO</text><path class='route' d='M600 1040 V1120'/><rect class='box' x='80' y='1120' width='1040' height='250' rx='24'/><text x='125' y='1180' class='c' font-size='23'>OUTCOME / PLAYABLE EVIDENCE</text><text x='125' y='1250' font-size='38'>8.21s WAV · hash verified</text><text x='125' y='1305' class='m' font-size='24'>One local job completes. The producer returns to her cut.</text><text x='80' y='1450' class='m' font-size='20'>Observed local demo + editorial staging. See evidence story for claim boundaries.</text></svg>"""
    write(PRODUCT / "infographic.svg", infographic)


def demo_asset_text():
    receipt = read(ROOT / "samples/narration-continuity/demo.receipt.json")
    return f"{receipt['asset']['durationSeconds']:.2f} seconds · PCM 24 kHz · SHA-256 {receipt['asset']['audioDigest'][:20]}…"


def compile_catalog(contracts):
    ready = [contract for contract in contracts if contract["status"] == "EDITORIALLY_REVIEWED"]
    cards = []
    for contract in contracts:
        is_ready = contract["status"] == "EDITORIALLY_REVIEWED"
        href = f"{contract['capabilityId']}/index.html" if is_ready else f"../../declarations/capability-content/{contract['capabilityId']}.json"
        count = len(contract["scenarioKeys"])
        cards.append(f"<article class='product {'ready' if is_ready else ''}' data-status='{contract['status']}' data-search='{esc((contract['title']+' '+contract['capabilityId']).lower())}'><a href='{href}'><span class='status'>{contract['status'].replace('_',' ')}</span><h3>{esc(contract['title'])}</h3><small>{count} scenario{'s' if count != 1 else ''} · {len(contract['permittedSurfaces'])} permitted surfaces</small></a></article>")
    body = f"""<section class='catalog-head'><div class='eyebrow'>Capability content estate</div><h1>{len(contracts)} capabilities.<br>{len(contracts)} product stories.</h1><p class='lead'>{len(ready)} stories have directed content packages. {len(contracts)-len(ready)} await direction. Every package preserves what the sources establish, what the experience should become, and the evidence needed to connect them.</p><div class='pills'><span class='pill'>{len(contracts)} source-bound contracts</span><span class='pill'>{len(ready)} editorially reviewed</span><span class='pill'>{len(contracts)-len(ready)} need direction</span></div><p><a class='button' href='../season-1/index.html'>Watch + train / Season 1</a> <a class='button secondary' href='editorial-ranking.html'>Inspect the production slate</a></p></section><div class='controls'><input id='search' aria-label='Search capabilities' placeholder='Search capabilities'><select id='status' aria-label='Editorial status'><option value=''>All statuses</option><option>EDITORIALLY_REVIEWED</option><option>NEEDS_DIRECTION</option></select></div><div class='catalog' id='catalog'>{''.join(cards)}</div><script>const q=document.getElementById('search'),s=document.getElementById('status');function f(){{document.querySelectorAll('.product').forEach(x=>x.hidden=!x.dataset.search.includes(q.value.toLowerCase())||(s.value&&x.dataset.status!==s.value))}}q.oninput=f;s.onchange=f;</script>"""
    write(SITE / "index.html", page("Capability Content Estate", body).replace("href='../index.html'", "href='index.html'"))


def compile_manifest(contracts):
    media = [ROOT / "samples/narration-continuity/the-story-stays-hers.mp4", ROOT / "samples/narration-continuity/the-story-stays-hers-short.mp4", ROOT / "samples/narration-continuity/thumbnail-a.jpg", ROOT / "samples/narration-continuity/finished-narration.wav"]
    manifest = {"catalogVersion": "capability-content-products.v2", "contractCount": len(contracts),
                "statusCounts": {status: sum(c["status"] == status for c in contracts) for status in ["EDITORIALLY_REVIEWED", "NEEDS_DIRECTION"]},
                "products": {},
                "rule": "Every emitted surface is a projection of one validated capability content contract."}
    mappings = {"landing-page": PRODUCT / "index.html", "article": PRODUCT / "article.html", "infographic": PRODUCT / "infographic.svg", "training": PRODUCT / "training.html", "demo": PRODUCT / "demo.html", "evidence-story": PRODUCT / "evidence.html", "video": media[0], "short": media[1], "thumbnail": media[2]}
    narrator = {"capabilityId": "generate-governed-narration", "contractSha256": digest(CONTRACTS / "generate-governed-narration.json"), "status": "COMPILED_FOR_REVIEW", "surfaces": {surface: {"path": path.relative_to(ROOT).as_posix(), "sha256": digest(path), "status": "COMPILED"} for surface, path in mappings.items()}}
    write(ROOT / "outputs/content-products/generate-governed-narration.json", json.dumps(narrator, indent=2) + "\n")
    for contract in contracts:
        if contract["status"] != "EDITORIALLY_REVIEWED":
            continue
        cid = contract["capabilityId"]
        product = read(ROOT / f"outputs/content-products/{cid}.json")
        if product["capabilityId"] != cid or product["contractSha256"] != digest(CONTRACTS / f"{cid}.json"):
            raise ValueError(f"STALE_PRODUCT_CONTRACT:{cid}")
        if set(product["surfaces"]) != set(contract["permittedSurfaces"]):
            raise ValueError(f"PRODUCT_SURFACE_PERMISSION_MISMATCH:{cid}")
        for surface, asset in product["surfaces"].items():
            path = (ROOT / asset["path"]).resolve()
            if not path.is_relative_to(ROOT) or not path.is_file() or digest(path) != asset["sha256"]:
                raise ValueError(f"PRODUCT_ASSET_MISMATCH:{cid}:{surface}")
        manifest["products"][cid] = product
    manifest["compiledSurfaceCount"] = sum(len(p["surfaces"]) for p in manifest["products"].values())
    output = ROOT / "outputs/capability-content-products.json"
    write(output, json.dumps(manifest, indent=2) + "\n")
    return manifest


def main():
    contracts = validate_contracts()
    reviewed = [contract for contract in contracts if contract["status"] == "EDITORIALLY_REVIEWED"]
    narrator = next(c for c in reviewed if c["capabilityId"] == "generate-governed-narration")
    compile_product(narrator)
    manifest = compile_manifest(contracts)
    compile_catalog(contracts)
    print(json.dumps({"contracts": len(contracts), "reviewed": len(reviewed), "compiledSurfaces": manifest["compiledSurfaceCount"]}, indent=2))


if __name__ == "__main__":
    main()
