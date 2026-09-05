"""Compile the signature class from editorial direction and exact lesson artifacts."""
import argparse
import html
import json
import os
from pathlib import Path
from string import Template
from typing import Literal
from urllib.parse import quote

from pydantic import Field
from capability_page_contract import Artifact, Inputs, validate_page, require
from infographic_contract import ROOT, Strict, read, digest

DEST = ROOT / 'samples/agentic-engineering'
MANIFEST = ROOT / 'declarations/agentic-engineering-course.json'


class Concept(Strict):
    id: str
    title: str
    question: str
    meaning: str
    example: str
    failure: str


class Module(Strict):
    number: int = Field(ge=1, le=10)
    capabilityId: str
    content: Artifact
    conceptIds: list[str] = Field(min_length=1)
    learnerArtifact: str
    defense: str
    availability: Literal['WORKED_LESSON', 'CURRICULUM_READY']


class Pathway(Strict):
    id: str
    title: str
    audience: str
    outcome: str
    status: Literal['ROADMAP']


class Provider(Strict):
    id: str
    label: str
    compatible: bool
    available: bool
    explanation: str


class BriefField(Strict):
    id: str
    label: str
    prompt: str


class Criterion(Strict):
    id: str
    criterion: str
    defense: str


class Lab(Strict):
    providers: list[Provider] = Field(min_length=2)
    briefFields: list[BriefField] = Field(min_length=1)
    rubric: list[Criterion] = Field(min_length=1)


class Course(Strict):
    version: Literal['agentic-engineering-course.v1']
    title: str
    subtitle: str
    promise: str
    audience: str
    sourceBrief: Artifact
    season: Artifact
    caseStudy: Artifact
    target: Artifact
    gaps: Artifact
    concepts: list[Concept] = Field(min_length=1)
    modules: list[Module] = Field(min_length=1)
    pathways: list[Pathway] = Field(min_length=1)
    lab: Lab


def load_course(path=MANIFEST):
    inputs = Inputs()
    course = Course.model_validate(read(inputs.file(path)))
    inputs.artifact(course.sourceBrief)
    season = read(inputs.artifact(course.season))
    page, content, circuits, inputs = validate_page(read(inputs.artifact(course.caseStudy)), inputs)
    target = read(inputs.artifact(course.target)); gaps = read(inputs.artifact(course.gaps))
    require(page.capabilityId == 'interlock-agent-operation', 'CASE_STUDY_MISMATCH')
    evidence = {e['id']: e for e in content['evidence']}
    for key in ('target', 'gaps'):
        ref = getattr(course, key)
        require(ref.path == evidence[key]['path'] and ref.sha256 == evidence[key]['sha256'], 'LESSON_EVIDENCE_DRIFT')
    require(target['mode'] == 'TARGET_DESIGN_REFERENCE_SIMULATION', 'LAB_MUST_BE_REFERENCE_DESIGN')
    require([m.number for m in course.modules] == [e['number'] for e in season['episodes']], 'COURSE_SEQUENCE')
    concepts = {c.id for c in course.concepts}
    require(len(concepts) == len(course.concepts), 'DUPLICATE_CONCEPT')
    require(set().union(*(set(m.conceptIds) for m in course.modules)) == concepts, 'UNTAUGHT_CONCEPT')
    modules = []
    for module, episode in zip(course.modules, season['episodes'], strict=True):
        require(module.capabilityId == episode['capabilityId'], 'CAPABILITY_SEQUENCE')
        contract = read(inputs.artifact(module.content))
        require(contract['capabilityId'] == module.capabilityId, 'LESSON_CONTENT_MISMATCH')
        require(set(module.conceptIds) <= concepts, 'UNKNOWN_CONCEPT')
        require(module.availability == ('WORKED_LESSON' if module.number == 1 else 'CURRICULUM_READY'), 'UNSUPPORTED_LESSON_AVAILABILITY')
        modules.append({**episode, **module.model_dump()})
    for entries in (course.pathways, course.lab.providers, course.lab.briefFields, course.lab.rubric):
        require(len({e.id for e in entries}) == len(entries), 'DUPLICATE_COURSE_ID')
    circuit = next(c for c in circuits if c['projection']['id'] == 'scenario-target')
    return course, modules, page, target, gaps, circuit, inputs


def esc(value):
    return html.escape(str(value), quote=True)


def link(path):
    return quote(Path(os.path.relpath(ROOT / path, DEST)).as_posix(), safe='/')


def compile_course(check=False):
    course, modules, page, target, gaps, circuit, inputs = load_course()
    for path in ['scripts/build_engineering_school.py', 'templates/engineering-school.html',
                 'templates/engineering-school.css', 'templates/engineering-school.js',
                 'templates/engineering-lab.js', 'templates/circuit-flow.js']:
        inputs.file(path)
    data = {'course': course.model_dump(), 'courseSha256': digest(MANIFEST), 'modules': modules,
            'target': target, 'gaps': gaps, 'projection': circuit['projection'],
            'film': page.film.media.model_dump(), 'liveEffects': False}
    concepts = ''.join(f'<button class="concept" data-concept="{esc(c.id)}" aria-pressed="false"><span>{i+1:02}</span>{esc(c.title)}<span aria-hidden="true">↗</span></button>' for i,c in enumerate(course.concepts))
    lessons = ''
    for m in modules:
        concepts_text = ' / '.join(c.title for c in course.concepts if c.id in m['conceptIds'])
        action = '<a href="#lesson">Watch + practice ↗</a>' if m['number']==1 else '<span class="availability">Curriculum ready · film planned</span>'
        lessons += f'<details class="lesson-row"{ " open" if m["number"]==1 else ""}><summary><span class="ordinal">{m["number"]:02}</span><span>{esc(m["title"])}</span><span class="lesson-status">{"WORKED LESSON" if m["number"]==1 else "PLANNED FILM"}</span></summary><div class="lesson-detail"><p class="eyebrow">{esc(concepts_text)}</p><p>{esc(m["objective"])}</p><p><strong>Make:</strong> {esc(m["learnerArtifact"])}</p><p><strong>Defend:</strong> {esc(m["defense"])}</p>{action}<a class="source-link" href="{link(m["content"]["path"])}">Capability source ↗</a></div></details>'
    pathways = ''.join(f'<article class="pathway"><span class="eyebrow">{i+1:02} / ROADMAP</span><h3>{esc(p.title)}</h3><p>{esc(p.outcome)}</p><small>{esc(p.audience)}</small></article>' for i,p in enumerate(course.pathways))
    fields = ''.join(f'<label class="brief-field" for="brief-{esc(f.id)}"><span>{esc(f.label)}</span><textarea id="brief-{esc(f.id)}" name="{esc(f.id)}" maxlength="8000" rows="3" placeholder="{esc(f.prompt)}"></textarea></label>' for f in course.lab.briefFields)
    rubric = ''.join(f'<label class="rubric-item"><input type="checkbox" name="{esc(r.id)}"><span>{esc(r.criterion)}<small>{esc(r.defense)}</small></span></label>' for r in course.lab.rubric)
    providers = ''.join(f'<option value="{esc(p.id)}">{esc(p.label)}</option>' for p in course.lab.providers)
    cases = ''.join(f'<option value="{esc(c["id"])}">{esc(c["title"])}</option>' for c in target['cases'])
    template = Template((ROOT/'templates/engineering-school.html').read_text(encoding='utf-8'))
    html_page = template.substitute(title=esc(course.title), subtitle=esc(course.subtitle), promise=esc(course.promise),
        concepts=concepts, lessons=lessons, pathways=pathways, brief_fields=fields, rubric=rubric,
        providers=providers, cases=cases, film=link(page.film.media.path), poster=link(page.film.poster.path),
        captions=link(page.film.captions.path), circuit_svg=circuit['enhancedSvg'],
        circuit_link=link('samples/capability-pages/interlock-agent-operation/index.html')+'#circuit',
        evidence_link=link('samples/content-catalog/interlock-agent-operation/evidence.html'),
        brief_link=link('declarations/agentic-engineering-course.json'))
    guide = '# '+course.title+': '+course.subtitle+'\n\n'+course.promise+'\n\n'
    guide += '## Teaching model\n\nThis is the SideFX teaching frame. Frameworks and models are implementations within it.\n\n'
    for c in course.concepts:
        guide += f'### {c.title}\n\n**{c.question}**\n\n{c.meaning}\n\nEpisode 1: {c.example}\n\nFailure to expose: {c.failure}\n\n'
    guide += '## Studio sequence\n\n1. Watch Episode 1; pause at 00:55 and 02:27.\n2. Inspect the two-sided certification circuit and its missing testimony.\n3. Predict each reference decision before revealing it.\n4. Change the provider while retaining the same request and evidence assumptions.\n5. Author the boundary brief and defend it against the rubric.\n\n'
    for m in modules:
        guide += f'### {m["number"]:02} / {m["title"]}\n\n{m["objective"]}\n\nExercise: {m["exercise"]}\n\nDeliverable: {m["learnerArtifact"]}\n\nDefense: {m["defense"]}\n\nAvailability: {m["availability"]}\n\n'
    guide += '## Instructor defense rubric\n\nScore each dimension 0 (absent), 1 (asserted), or 2 (specific and supported). A self-check is not an instructor assessment or professional credential.\n\n'
    for r in course.lab.rubric:
        guide += f'- **{r.criterion}** Ask: {r.defense}\n'
    guide += '\nRequire revision when any dimension is 0. A complete classroom brief does not certify a live capability. Unresolved gaps become engineering testimony for a separate platform review.\n'
    outputs = {'index.html': html_page.encode(), 'instructor-guide.md': guide.encode(),
        'course-data.js': ('window.ENGINEERING_COURSE = '+json.dumps(data,ensure_ascii=False).replace('<','\\u003c')+';\n').encode()}
    for filename in ['engineering-school.css','engineering-school.js','engineering-lab.js','circuit-flow.js']:
        outputs[filename] = (ROOT/'templates'/filename).read_bytes()
    receipt = {'version':course.version,'status':'SIGNATURE_CLASS_WITH_FIRST_WORKED_LESSON',
        'courseSha256':digest(MANIFEST),'inputs':dict(sorted(inputs.hashes.items())),
        'moduleCount':len(modules),'workedLessons':1,'plannedFilms':9,'liveEffects':False}
    if not check:
        DEST.mkdir(parents=True,exist_ok=True)
        for name,payload in outputs.items(): (DEST/name).write_bytes(payload)
        receipt['outputs']={name:digest(DEST/name) for name in outputs}
        (DEST/'build-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    return receipt


if __name__ == '__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');parser.add_argument('--schema',action='store_true');args=parser.parse_args()
    if args.schema:
        (ROOT/'schemas/agentic-engineering-course.schema.json').write_text(json.dumps(Course.model_json_schema(),indent=2)+'\n',encoding='utf-8')
    else:
        result=compile_course(args.check)
        print(result['status'], '10 modules / 9 concepts / 1 worked lesson / 6 roadmap pathways')
