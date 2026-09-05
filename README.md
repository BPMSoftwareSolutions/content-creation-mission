# Content Creation Mission

## SideFX Circuit Language

The [SCL workbench](http://127.0.0.1:8766/samples/scl/index.html) reveals all
219 capabilities in the frozen corpus as typed circuit data, renders their 823
scenario boundaries, and retains native mechanics and topology for inspection.
Start it with `.venv\Scripts\python.exe scripts/serve_scl.py`. SCL 0.2 adds compact
given/when/then authoring, parallel paths, evidence requirements and source-linked
diagnostics in the live playground. Existing 0.1 drafts remain compatible.
See the [0.2 language specification](docs/SCL-0.2-SPECIFICATION.md) and
[coverage report](evaluations/scl-coverage.json) for exact support and open profiles.
Draft compilation is design testimony, not platform admission or execution.

## Open the workspace

```powershell
git clone https://github.com/BPMSoftwareSolutions/content-creation-mission.git
cd content-creation-mission
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe scripts/serve_content.py --port 8765
```

Open the [infographic studio](http://127.0.0.1:8765/samples/infographic-grammar/index.html#scenario-target),
[content catalog](http://127.0.0.1:8765/samples/content-catalog/index.html), or
[Season 1](http://127.0.0.1:8765/samples/season-1/index.html).
The checked-in workspace includes frozen evidence, authored contracts, generated
images, rendered films, and verification reports. Viewing these outputs needs no
provider key or access to the source repository. Re-extracting the estate requires
the source checkout; generating new provider media requires a configured key.
Virtual environments, downloaded tools, render caches, and local environment
files stay outside version control. Git preserves exact bytes for hash-bound files.

The infographic studio uses shared primitive anchors and constrained Bézier
routing, with independent SVG checks for contact and tangent continuity.
See [the compiler guide](docs/INFOGRAPHIC-COMPILER.md) for reproducible exports and
[the grammar](docs/SIDEFX-INFOGRAPHIC-GRAMMAR.md) for visual semantics.

The studio's **Material edition** adds fifteen individually generated Nano Banana
component treatments, a Base / Enhanced comparison, enhanced SVG/PNG exports at
all three altitudes, and an enhanced 1080p circuit animation. Original vector
geometry, labels, connections and evidence modes remain intact. The
[enhancement guide](docs/INFOGRAPHIC-ENHANCEMENTS.md) documents asset generation,
review, canonical masking and reproducible composition.

## Reusable capability editions

Open [the capability editions](samples/capability-pages/index.html) for a reusable
page combining the human film, living SVG circuit, Nano Banana material, source
evidence, assessment and nine media surfaces. Interlock has three explicitly
scoped circuits; narration reuses the template and identifies its new circuit as
an open production requirement.

```powershell
.\.venv\Scripts\python.exe scripts/build_capability_pages.py
```

The build consumes reviewed artifacts, makes no provider calls, and rejects
stale content, evidence, media or circuit bindings. See the
[three-layer product system](docs/CAPABILITY-VISUAL-PRODUCT-SYSTEM.md) for the
composition contract, template, animation behavior and production workflow.

**Play flow** rolls a silver ball along the exact circuit paths. Fan-out splits
it, the ALL join waits for both arrivals, and validation precedes the intended
outcome. Pause, scrub, replay and speed controls preserve the evidence labels.
See [the flow specification](docs/CIRCUIT-FLOW.md) for geometry, timing and tests.

## Capability content estate

Open `samples/content-catalog/index.html` for the source-bound catalog. The estate
contains 219 capability content contracts: two editorially reviewed stories compiled
into eighteen surfaces and 217 honest `NEEDS_DIRECTION` records. The first complete
content product is **The provider changed. The story stayed hers.**

Its landing page, article, infographic, training assessment, executable local demo,
evidence story, film, vertical Short, and thumbnail are projections of
`declarations/capability-content/generate-governed-narration.json`. The compiler
rejects broken schema, claim/evidence references, changed evidence bytes, mismatched
surface permissions, and an incomplete contract estate.

```powershell
.\.venv\Scripts\python.exe scripts/author_content_catalog.py
.\.venv\Scripts\python.exe scripts/render_content_short.py
.\.venv\Scripts\python.exe scripts/compile_content_products.py
```

The authoring step preserves reviewed contracts. It only creates missing
source-bound records, so a refresh cannot silently erase editorial direction.

The next production slate is published at
`samples/content-catalog/editorial-ranking.html`. It preserves the ten-capability
Season 1 slate and displays its current production progress. It ranks
capabilities with a declared 100-point model covering audience demand, human
stakes, visible transformation, competence spectacle, capsule evidence readiness,
and franchise yield. Rebuild and verify it with:

```powershell
.\.venv\Scripts\python.exe scripts/build_editorial_ranking.py
```

## Watch the human-experience film

### Season 1 / Evidence and intended design

The [Agentic Engineering signature class](samples/agentic-engineering/index.html)
turns the series into a curriculum: nine engineering concepts, ten capability
studies, Episode 1 with its living circuit, and a reference lab that separates
authority, provider readiness and evidence. Learners predict decisions, compare
provider substitutions and export an authority boundary brief for instructor
defense. Six broader school pathways are labeled as a roadmap.

Build with `.\.venv\Scripts\python.exe scripts/build_engineering_school.py`.
See [the teaching and production guide](docs/AGENTIC-ENGINEERING-SCHOOL.md) and
[the instructor guide](samples/agentic-engineering/instructor-guide.md).

Open `samples/season-1/index.html` for **The Future of Agentic Engineering — A
SideFX Training Series**. All ten episodes have lesson objectives, exercises,
and takeaways. Episode 1 has a complete content package; Episodes 2–10 have
curriculum direction and await film production.

For browser playback with working chapter seeks, run
`.\.venv\Scripts\python.exe scripts/serve_content.py` and open
`http://127.0.0.1:8765/samples/season-1/index.html`. The preview binds only to
loopback and supports byte-range requests for video seeking.

**When the Agent Is Ready to Act, Who Decides?** projects Interlock Agent Operation
into its intended experience: retain human authority, hold unauthorized
publication, permit the admitted inspection, and return its evidence. The narrated
film has ten chapters, generated human stills, animated mechanics, and captions.
The 1080p edition embeds the material infographics and rolling silver-ball flow
at **00:55 (current adjudication)** and **02:27 (target certification)**. It uses
the same flow scheduler as the living circuit, with narration-timed cutaways.
See [episode infographic integration](docs/EPISODE-INFOGRAPHICS.md) for the reusable
edit contract, render commands and exact source provenance.
The package includes a vertical short, thumbnail, transcript/article, infographic,
training assessment, target simulation, landing page, and evidence story.

Current source evidence, target architecture, and six specific closure gaps stay
visually distinct. The reference simulation runs seven authored cases with no
live tool dispatch. The episode does not establish live interception by the current
platform. See `docs/EVIDENCE-AND-INTENDED-DESIGN.md` and
`evaluations/episode-01-platform-gap.json`.

Rebuild from selected media (no provider calls):

```powershell
.\.venv\Scripts\python.exe scripts/render_episode_one.py --render --short
.\.venv\Scripts\python.exe scripts/build_season_one.py
.\.venv\Scripts\python.exe scripts/compile_content_products.py
.\.venv\Scripts\python.exe scripts/build_editorial_ranking.py
.\.venv\Scripts\python.exe scripts/test_season_one.py
```

`prepare_season_one.py` authors source bindings and derived declarations from
the season, direction, and target-design inputs. The renderer's `--audio` and
`--short-audio` options call Gemini only when their exact cached speech is absent
or stale. The selected image assets are explicitly pinned in `shot-selection.json`.

### Narration continuity

`samples/narration-continuity/index.html` is the current screening room for
**The story stays hers**, a 64-second directed animatic. A producer's narration
job is interrupted; the local demo rejects an incompatible alternative and
obtains real Gemini speech. The ending plays the generated narration.

Six consistent human keyframes carry concern, active investigation, relief and
resumed editing. Procedural animation shows request flow, provider routing,
waveforms and artifact evidence. Human motion is implied between still frames.
The primary failure is simulated. This is an editorial composition informed by
provider-switch and narration capsules, not managed execution footage.

The screening room includes the per-entity sheet, exact local demo receipt,
source-linked composition direction, two thumbnail/hook hypotheses, and an
empty audience measurement template. See `docs/AUDIENCE-DESIGN-LAW.md`.

Rebuild existing media without paid calls:

```powershell
.\.venv\Scripts\python.exe scripts/render_continuity_film.py
.\.venv\Scripts\python.exe scripts/build_continuity_screening.py
.\.venv\Scripts\python.exe scripts/analyze_audience_observations.py
```

## Current work: capsule-grounded experience preparation

Open `samples/mechanics-workbench/index.html`. It follows a real pending-convergence
fixture through six source-linked beats and exposes the entire 823-scenario evidence
index. The engine reads full verified capsules: execution plans v1/v2/v3, nested
responsibilities, mechanic configurations, provider bindings, contracts, topology,
fixtures and receipts. Sources are stored as inert JSON, never executed.

809 packages have resolved structural evidence; 14 retain explicit findings:
12 scenarios lack declared scenario IDs needed for exact execution linkage, and
two lack the expected fixture entry. Those counts do not claim semantic acceptance.
One convergence direction has been reviewed against actual expressions and fixture
bytes. All corpus directions still require specific editorial mapping and review.

The old visual pilots are rejected explorations under
`docs/MECHANIC-GROUNDED-VISUAL-LAW.md`. No existing imagery is promoted by the new
mechanics extraction. Generation now rejects missing or stale mechanics packages.

```powershell
.\.venv\Scripts\python.exe scripts/extract_capsule_reality.py
.\.venv\Scripts\python.exe scripts/build_mechanic_pilot.py
.\.venv\Scripts\python.exe scripts/test_mechanics_gate.py
.\.venv\Scripts\python.exe scripts/compile_mechanic_generation.py
.\.venv\Scripts\python.exe scripts/generate_gemini.py --manifest samples/mechanics-workbench/generation-manifest.json --limit 1
```

The final command previews only. Add `--execute` to render a candidate; the runner
attaches the exact reviewed mechanical direction and animation beats to the prompt.
Fixture assertions remain declared expectations, not successful run receipts.

## Historical visual pilot (rejected)

Open `samples/visual-pilot/atlas.html`: search the estate, filter families and
step through eight rendered governed-routing scenarios. Single-frame playback,
source/prompt inspection and generation-recipe downloads work locally.
`capability-walkthrough.mp4` is a 3m51s Gemini-narrated walkthrough.
`capability-short.mp4` is a silent 60-second vertical cut. Animation consists of
phase cuts/dissolves, not generated motion. See evaluations/visual-pilot-review.md.

The runner reads `LOC_GEMINI_API_KEY` from the process or Windows User/Machine
environment without printing or saving it. `GEMINI_API_KEY` remains a legacy
process fallback. The key is sent only in the Gemini authentication header.

Rebuild from existing media, without making paid requests:

```powershell
.\.venv\Scripts\python.exe scripts/build_visual_atlas.py
.\.venv\Scripts\python.exe scripts/render_visual_pilot.py
```

`prepare_visual_pilot.py` reproduces curated prompts. The Gemini runner accepts
`--manifest samples/visual-pilot/generation-manifest.json`, `--offset`, `--limit`
and `--reference` (local PNG/JPEG). Add `--execute` only to send paid requests.
`narrate_visual_pilot.py --execute` generates/resumes the eight speech chapters.

A working Python preparation pipeline: verified capsule feature documents →
scenario inventory → rule-based taxonomy → source-preserving visual specs →
Gemini request manifests. It writes only inside this content lab.

## Run on Windows

```powershell
cd C:\lab\repos\content-creation-mission
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe scripts/content_lab.py --source C:\lab\repos\agentic-harness --samples 20 --formats scenario-triptych,linkedin-square,youtube-thumbnail,shorts,website-hero,infographic,capability-cover
.\.venv\Scripts\python.exe scripts/test_content_lab.py
.\.venv\Scripts\python.exe scripts/generate_gemini.py --limit 1
```

On other platforms use `.venv/bin/python`. Source location is an argument.
The default format is scenario-triptych. The full command above builds seven
formats. The command returns nonzero for missing sources or missing phases.
Taxonomy ambiguity remains a review item rather than a fabricated classification.

## Outputs

| Path | Product |
| --- | --- |
| inventories/scenario-inventory.json and .csv | Every extracted scenario, phases, tags, products, actor, dependency pins and source lineage |
| data/source-manifest.json | Frozen manifest identity, capsule/feature identities and source findings |
| data/source-features/ | Exact capsule-carried feature bytes copied into this lab |
| outputs/visual-experience-specs.json | Complete derived spec collection |
| outputs/visual-experience-specs/ | Individual files keyed by capability AND scenario to avoid collisions |
| outputs/scenario-taxonomy-classification.json | Ranked rule evidence, ties and unknowns |
| outputs/generation-manifest.json | Request payloads and model/format selection |
| outputs/batches/ | Family-grouped JSONL request bodies |
| samples/gallery.html | Locally viewable semantic triptych cards |
| samples/scenario-sample-set.json | Deterministic sample across families |
| samples/generation-manifest.json | Sample request payloads |
| evaluations/pipeline-report.json | Coverage, preservation and structural validation results |

## Generation

`generate_gemini.py` previews one request by default. To send a bounded request,
set `LOC_GEMINI_API_KEY` in your environment, then add `--execute --limit 1`.
This is billable. Increase the explicit limit after reviewing sample results.
Use `--model` to override a model identifier. Successful image receipts are
content-addressed and verified on resume. No-image and HTTP failures stop the
run; retryable HTTP statuses have bounded backoff. Uncertain network failures
stop rather than silently repeating a potentially charged call.

Live image and speech generation now succeeds for the eight-scenario pilot.
The remaining estate has specs and payloads, not rendered images.
See docs/gemini-generation-strategy.md for provider and review details.

## Interpretation limits and extension

Classification is transparent lexical scoring, not embeddings or discovered
statistical clusters. Modify data/visual-taxonomy.json to extend terms, motifs
and motion hints, then rerun. Scores are not probabilities. Review ambiguous
and unclassified rows first. The original Given/When/Then statements, tables,
backgrounds and Examples remain embedded in the specs. Scenario outlines are
counted once as templates, not expanded into synthetic scenario identities.

Known actors come from capsule userStory.actor. Providers and altitude are
unknown unless explicitly supplied; dependency pins are not assumed to be
providers. Proposed environments and palettes are creative choices. Every spec
requires semantic review before production rendering; schema checks do not
prove artistic quality. Capability covers are scenario-focused concepts.

Run outputs are deterministic for fixed inputs and configuration. Aggregate
JSON files are authoritative for the current run; old per-item files can remain
after corpus removal and must not be globbed as the current inventory. No
generated media are overwritten by preparation runs.

## Contract-driven infographic grammar

Open [the interactive grammar studio](samples/infographic-grammar/index.html).
It includes 15 primitives, seven typed connectors, scenario/capability/circuit
views, exact source inspection, semantic aggregation, and a Manim circuit film.
The [grammar specification](docs/SIDEFX-INFOGRAPHIC-GRAMMAR.md) fixes the language;
the [compiler guide](docs/INFOGRAPHIC-COMPILER.md) documents the reproducible stack.
Run `.\.venv\Scripts\python.exe scripts/rebuild_infographics.py` to rebuild and
validate the four reference contracts and their exports.
