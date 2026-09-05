"""Validate and publish the source-bound editorial priority ranking."""
import hashlib
import html
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DECLARATION = ROOT / "declarations/editorial-priority-ranking.json"
OUTPUT = ROOT / "outputs/editorial-priority-ranking.json"
PAGE = ROOT / "samples/content-catalog/editorial-ranking.html"


def read(path):
    return json.loads(path.read_bytes())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def esc(value):
    return html.escape(str(value))


def root_package(capability_id, scenario_id):
    candidates = list((ROOT / "outputs/scenario-visual-evidence" / capability_id).glob("*.json"))
    for path in candidates:
        package = read(path)
        if package["scenarioSurface"]["scenarioId"] == scenario_id:
            return path, package
    raise ValueError(f"ROOT_EVIDENCE_PACKAGE_MISSING:{capability_id}:{scenario_id}")


def build():
    declaration = read(DECLARATION)
    inventory = read(ROOT / "inventories/scenario-inventory.json")
    contracts = {path.stem: read(path) for path in (ROOT / "declarations/capability-content").glob("*.json")}
    scenarios = defaultdict(list)
    for scenario in inventory:
        scenarios[scenario["capabilityId"]].append(scenario)
    weights = declaration["scoreModel"]
    candidates = declaration["candidates"]
    if [candidate["rank"] for candidate in candidates] != list(range(1, 11)):
        raise ValueError("RANKS_MUST_BE_EXACTLY_ONE_THROUGH_TEN")
    if len({candidate["capabilityId"] for candidate in candidates}) != 10:
        raise ValueError("RANKING_CONTAINS_DUPLICATE_CAPABILITY")
    enriched = []
    previous_score = 101
    for candidate in candidates:
        capability_id = candidate["capabilityId"]
        if capability_id in declaration["excludes"]:
            raise ValueError(f"EXCLUDED_CAPABILITY_RANKED:{capability_id}")
        if capability_id not in contracts or capability_id not in scenarios:
            raise ValueError(f"UNKNOWN_CAPABILITY:{capability_id}")
        if set(candidate["scores"]) != set(weights):
            raise ValueError(f"SCORE_DIMENSION_MISMATCH:{capability_id}")
        for dimension, score in candidate["scores"].items():
            if not isinstance(score, int) or not 0 <= score <= weights[dimension]:
                raise ValueError(f"SCORE_OUT_OF_RANGE:{capability_id}:{dimension}")
        total = sum(candidate["scores"].values())
        if total > previous_score:
            raise ValueError(f"RANK_ORDER_CONTRADICTS_SCORE:{capability_id}")
        previous_score = total
        root_scenario = scenarios[capability_id][0]
        evidence_path, package = root_package(capability_id, root_scenario["scenarioId"])
        if package["disposition"] != "MECHANICS_EXTRACTED_REQUIRES_DIRECTION":
            raise ValueError(f"MECHANICS_NOT_READY_FOR_DIRECTION:{capability_id}:{package['disposition']}")
        evidence = package["evidence"]
        item = dict(candidate)
        item.update(
            score=total,
            capabilityTitle=contracts[capability_id]["title"],
            scenarioCount=len(scenarios[capability_id]),
            actors=sorted({actor for scenario in scenarios[capability_id] for actor in scenario["actors"]}),
            capsuleDigest=contracts[capability_id]["source"]["capsuleDigest"],
            evidencePackage={"path": evidence_path.relative_to(ROOT).as_posix(), "sha256": digest(evidence_path)},
            rootEvidenceCounts={name: len(values) for name, values in evidence.items()},
            rootDisposition=package["disposition"],
            currentEditorialStatus=contracts[capability_id]["status"],
            nextGate="REVIEW_CONTENT_PACKAGE" if contracts[capability_id]["status"] == "EDITORIALLY_REVIEWED" else "AUTHOR_CAPABILITY_CONTENT_CONTRACT"
        )
        enriched.append(item)
    result = {
        "rankingVersion": declaration["rankingVersion"],
        "status": declaration["status"],
        "generatedFrom": {"declaration": DECLARATION.relative_to(ROOT).as_posix(), "sha256": digest(DECLARATION)},
        "corpus": {"capabilities": len(contracts), "scenarios": len(inventory), "excludedAlreadyReviewed": declaration["excludes"]},
        "scoreModel": weights,
        "interpretation": declaration["interpretation"],
        "demandSignals": declaration["demandSignals"],
        "ranking": enriched
    }
    OUTPUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    PAGE.parent.mkdir(parents=True, exist_ok=True)
    PAGE.write_text(render(result), encoding="utf-8")
    return result


def render(result):
    labels = {
        "audienceDemand": "Demand", "humanStakes": "Human stakes", "visibleTransformation": "Transformation",
        "competenceSpectacle": "Competence", "capsuleEvidenceReadiness": "Evidence", "franchiseYield": "Franchise"
    }
    cards = []
    for item in result["ranking"]:
        bars = "".join(
            f"<div class='metric'><span>{labels[key]}</span><i><b style='width:{value/result['scoreModel'][key]*100:.0f}%'></b></i><em>{value}/{result['scoreModel'][key]}</em></div>"
            for key, value in item["scores"].items()
        )
        progress = f"<p><a href='{item['capabilityId']}/index.html'>Open Episode {item['rank']:02} / watch + train</a></p>" if item['currentEditorialStatus'] == 'EDITORIALLY_REVIEWED' else ""
        cards.append(f"""
        <article class='rank-card' id='rank-{item['rank']}'>
          <div class='number'>{item['rank']:02}</div><div class='story'>
            <div class='capability'>{esc(item['capabilityTitle'])}</div><h2>{esc(item['storyTitle'])}</h2>
            <p class='hook'>“{esc(item['hook'])}”</p><p>{esc(item['humanStory'])}</p>{progress}
            <details><summary>Why this ranks here</summary><p>{esc(item['whyNext'])}</p><p class='risk'><strong>Direction risk:</strong> {esc(item['directionRisk'])}</p><p><strong>First package:</strong> {esc(item['recommendedPackage'])}</p></details>
          </div><aside><div class='score'>{item['score']}<small>/100</small></div>{bars}<div class='facts'>{item['scenarioCount']} scenarios · {item['rootEvidenceCounts']['mechanics']} root mechanics · {item['rootEvidenceCounts']['fixtures']} fixtures<br><a href='../../{esc(item['evidencePackage']['path'])}'>inspect source package</a></div></aside>
        </article>""")
    sources = "".join(f"<li><a href='{esc(source['url'])}'>{esc(source['title'])}</a><br><span>{esc(source['use'])}</span></li>" for source in result["demandSignals"]["sources"])
    return f"""<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Next ten capability stories</title><style>
    :root{{--ink:#f3f0e8;--muted:#9badb9;--cyan:#6edfdc;--amber:#edbc77;--bg:#061019;--panel:#0c1b25;--line:#27424e}}*{{box-sizing:border-box}}body{{margin:0;background:radial-gradient(circle at 80% 0,#173946 0,transparent 32%),var(--bg);color:var(--ink);font:16px/1.55 Segoe UI,system-ui,sans-serif}}a{{color:var(--cyan)}}main{{max-width:1240px;margin:auto;padding:28px}}nav{{display:flex;justify-content:space-between;font-size:12px;letter-spacing:.2em}}nav a{{color:var(--ink);text-decoration:none}}header{{padding:85px 0 55px;max-width:1000px}}.eyebrow,.capability{{color:var(--cyan);font-size:12px;letter-spacing:.15em;text-transform:uppercase;font-weight:800}}h1{{font-size:clamp(54px,8vw,104px);line-height:.94;letter-spacing:-.055em;margin:15px 0 25px}}header p{{font-size:21px;color:#c4cfd4;max-width:800px}}.legend{{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:20px 0 55px}}.legend div{{padding:14px;border:1px solid var(--line);border-radius:10px;color:var(--muted)}}.rank-card{{display:grid;grid-template-columns:80px 1fr 330px;gap:24px;border-top:1px solid var(--line);padding:42px 0}}.number{{font-size:44px;color:var(--amber);font-weight:800}}h2{{font-size:36px;line-height:1.07;margin:8px 0 15px;letter-spacing:-.03em}}.hook{{font-size:20px;color:#dce6e8}}summary{{cursor:pointer;color:var(--cyan);font-weight:700;margin-top:18px}}.risk{{border-left:3px solid var(--amber);padding-left:14px}}aside{{background:rgba(12,27,37,.9);border:1px solid var(--line);border-radius:15px;padding:20px}}.score{{font-size:48px;font-weight:800;margin-bottom:14px}}.score small{{font-size:16px;color:var(--muted)}}.metric{{display:grid;grid-template-columns:95px 1fr 42px;align-items:center;gap:8px;font-size:12px;color:var(--muted);margin:7px 0}}.metric i{{height:5px;background:#213944;border-radius:4px;overflow:hidden}}.metric b{{display:block;height:100%;background:var(--cyan)}}.metric em{{font-style:normal;text-align:right}}.facts{{border-top:1px solid var(--line);margin-top:18px;padding-top:15px;font-size:12px;color:var(--muted)}}.method{{margin:60px 0;padding:28px;background:var(--panel);border:1px solid var(--line);border-radius:14px}}.method li{{margin:14px 0}}.method span{{color:var(--muted)}}@media(max-width:850px){{.rank-card{{grid-template-columns:50px 1fr}}aside{{grid-column:2}}.legend{{grid-template-columns:1fr}}h2{{font-size:28px}}}}
    </style></head><body><main><nav><a href='index.html'>SIDEFX / CONTENT ESTATE</a><span>EDITORIAL PRIORITY / 2026-09-05</span></nav><header><div class='eyebrow'>The next production slate</div><h1>Ten capabilities worth making human next.</h1><p>Ranked for audience relevance, human stakes, visible transformation, competence spectacle, capsule evidence, and the number of useful content products each story can support.</p></header><section class='legend'><div><strong>Source gate passed</strong><br>All ten have extracted capsule mechanics and exact evidence packages.</div><div><strong>Direction still required</strong><br>Ranking does not promote a contract to editorially reviewed.</div><div><strong>Demand is a hypothesis</strong><br>Audience behavior must confirm or overturn this order after publication.</div></section>{''.join(cards)}<section class='method'><h2>How the ranking works</h2><p>{esc(result['interpretation'])}</p><ul>{sources}</ul></section></main></body></html>"""


if __name__ == "__main__":
    ranking = build()
    print(json.dumps({"ranked": len(ranking["ranking"]), "top": ranking["ranking"][0]["capabilityId"], "scores": [item["score"] for item in ranking["ranking"]]}, indent=2))
