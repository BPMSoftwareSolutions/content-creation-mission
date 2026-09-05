# Capability visual product system v1

One reviewed capability can carry a human story, an inspectable circuit, material
art, motion, a lesson, and reusable media. These are three production components
with separate responsibilities and one composition boundary.

| Component | Owns | Canonical inputs | Production boundary |
| --- | --- | --- | --- |
| Base SVG grammar | Shapes, labels, ports, topology, evidence modes, source references, animation beats | `declarations/infographic-grammar.v1.json`, `declarations/infographics/*.json` | `scripts/compile_infographics.py` |
| Nano Banana material overlays | Reviewed color, texture, glow and surface treatment inside the canonical component | `declarations/infographic-enhancement.v1.json`, `evaluations/component-enhancement-review.json` | `scripts/generate_component_assets.py`, `scripts/enhance_infographics.py` |
| Composite capability page | Human experience, film, circuit interaction, claims, training, surface links | A reviewed capability content contract plus `declarations/capability-pages/*.json` | `scripts/build_capability_pages.py`, `templates/capability-page.*` |

The [SVG grammar](SIDEFX-INFOGRAPHIC-GRAMMAR.md) and its
[compiler](INFOGRAPHIC-COMPILER.md) retain structural authority. The
[material system](INFOGRAPHIC-ENHANCEMENTS.md) owns appearance only. The page
consumes their exact artifacts; it does not redraw the graph or ask a model to
reconstruct it.

## The composition contract

`schemas/capability-page.schema.json` is exported from the strict models in
`scripts/capability_page_contract.py`. A `capability-page.v1` manifest binds:

- The capability ID and exact reviewed content contract bytes.
- The film, its existing media receipt, poster and optional captions.
- Exactly the surfaces permitted by the content contract; each link binds a file hash.
- Zero or more compiled circuits, their material receipts and optional motion receipt.
- The relationship of each circuit to the story, with explicit editorial context.
- An explicit production requirement when no new grammar circuit is available.

The manifest selects artifacts and explains their relationship. The content
contract supplies the title, audience, problem, input/event/outcome, mechanics,
claims, evidence, exercise, and assessment. The template contains no capability
names, provider names, scenario IDs or hard-coded claim counts.

Circuit relationships are `scenario`, `related-scenario`, or
`capability-overview`. An estate graph cannot be substituted into a single
capability page. Current adjudication and future certification are separate
scenarios, not frames of an observed execution.

The film's receipt establishes media integrity. It never upgrades the film's
claims to observed platform behavior. The page prints the content contract's
scope beside the player and gives each claim its original evidence category.

## Build from reviewed artifacts

Run from this content lab:

```powershell
.\.venv\Scripts\python.exe scripts/build_capability_pages.py
```

This compiles every declared page, the editions index and build receipts. It
uses existing media without making provider calls. A single page can be rebuilt:

```powershell
.\.venv\Scripts\python.exe scripts/build_capability_pages.py --manifest declarations/capability-pages/interlock-agent-operation.json
```

Use `--check` to validate inputs without writing outputs, or `--schema` to export
the schema from the typed models. The entire requested batch is validated before
the first page is written. Each build receipt records the exact input closure,
templates, compiler sources and output hashes. An interrupted filesystem write
is not a successful build; rerun the command to complete the deterministic output.

Open `samples/capability-pages/index.html`, directly or through the local preview
server. The pages work with `file://`; HTTP is preferable for video seeking and
caption-track browser support.

## Add another capability

1. Finish and review its capability content contract. `NEEDS_DIRECTION` is refused.
2. Produce the surfaces that its contract permits, with the film receipt and exact source bindings.
3. Author its scenario projection using the base grammar; compile and inspect it.
4. Reuse the existing 15 reviewed material assets through the compositor. New image generation is needed only when material direction changes.
5. Declare a page manifest with exact file hashes and honest circuit relationships.
6. Run the page build, inspect the result, and publish the reviewed artifact set.

If a story is ready before its new circuit, declare `openCircuit` with the
specific remaining direction and supporting evidence IDs. This yields
`COMPOSED_WITH_OPEN_CIRCUIT`. It does not invent topology or claim a finished
three-layer circuit. A page with bound, validated circuits yields `COMPOSED`.
Both statuses concern content production, never managed capability admission.

For a fresh infographic build, use the existing commands in order:

```powershell
.\.venv\Scripts\python.exe scripts/rebuild_infographics.py --skip-motion
.\.venv\Scripts\python.exe scripts/enhance_infographics.py
.\.venv\Scripts\python.exe scripts/build_infographic_studio.py
```

`scripts/animate_infographic.py --enhanced` renders the existing target
certification film. That Manim film renderer currently targets this one scenario;
it is not a generic arbitrary-capability film compiler. The page's five-phase
browser player is generic across validated projection contracts. Rebuild receipts
and intentionally update the page's artifact hashes after a reviewed upstream
change; the page build never silently repins stale inputs.

## Animation and interaction contract

The inline SVG is the exact compiled base or its reviewed composite. Material
groups stay inside their owning entities. Switching appearance preserves the
selected component, phase, zoom and scroll. SVG exports follow the selected
appearance. The independently rendered film is explicitly the composed edition.

The [silver-ball flow player](CIRCUIT-FLOW.md) follows the selected paths in
`animationBeats`, splits at fan-out, and schedules continuation only after the
join's required arrivals. Timing is illustrative, never execution telemetry.
Five manual phases—Establish, Activate, Execute, Resolve, Prove—remain available
for cumulative emphasis. The existing Manim film retains its separate timeline.
GAP components remain visible throughout, and evidence labels never change.

Playback is opt-in. Reduced-motion users advance one flow event per activation.
Changing tabs, inspecting a node, hiding the page or leaving it stops playback.
Nodes support keyboard activation; the circuit has fit/zoom and scrolling.
Claims, media, source links and lesson text remain available without JavaScript.
Assessment answers are checked locally and are never submitted or persisted.

## Integrity checks and reference editions

The boundary rejects stale content/evidence/media hashes, unreviewed content,
unpermitted surfaces, wrong-capability graphs, changed compiled semantics,
invalid geometry, material drift, stale material review, and mismatched motion.
It re-renders the frozen layout and compares canonical SVG, then independently
measures the final junction contacts. Removing decoration must recover the base.

These are mechanical conformance checks. Human review still owns whether an
editorial relationship, metaphor or scenario direction says the right thing.

- **Interlock Agent Operation:** full three-layer reference edition, three
  separately labeled circuits, the existing film, four assessment questions,
  four evidence categories, and all nine permitted media surfaces.
- **Generate Governed Narration:** the same page template with its own film,
  seven claims, three assessment questions and nine surfaces. The existing story
  infographic remains available; a new canonical circuit is explicitly open.

Neither example changes the source capsule estate or claims live interlock
execution. Visual production can expose the engineering runway without erasing
the distinction between declared semantics, local observations and intended design.
