# Flagship film implementation plan

**The Future of Agentic Engineering — From AI-Generated Script to Managed Capability**

Status: implementation plan for production.

Planning baseline: September 6, 2026.

Audience: practicing software engineers who understand code, tests, APIs, architecture, IDEs, and delivery.

## 1. The production decision

Build a roughly **26-minute film that combines engineering training, product vision, an interaction design specification, and a future demand test** around one useful program. Follow its behavior into explicit meaning, circuit design, capability authority, a capsule, managed change, and another implementation. The audience must see and inspect the transformation. Narration connects the evidence and designed experience; it cannot substitute for either.

**The possibilities are the center of gravity.** The film reveals what engineers can create when meaning becomes explicit: inspect a system beyond its code, design its behavior on a precise canvas, ask an agent for a semantic change, challenge that proposal, compose capabilities, and realize the same meaning in different technologies. Every major sequence should open another engineering possibility and let the viewer experience it through a consequential interaction.

The emotional progression is familiarity → discovery → creative control → expanded possibility. The audience starts with “I know how this code works” and leaves with “I can see how to design, prove, project, and evolve capabilities.” Production constraints belong in the work plan. They do not become the film's recurring subject.

**The current UI and currently shipped implementation do not set the visual ceiling.** Design the complete future engineering environment over the architectural foundation: canonical authority, typed topology, provider slots, mechanics, projections, capsules, and reproducible embodiments. Architecture fidelity gives the design its coherence while leaving the interaction experience open to invention. Build the most compelling intelligible experience the model supports.

Real source files in VS Code, real terminal commands, actual diffs, fixture inputs, failing checks, and resulting artifacts anchor the lesson. Budget **8–10 minutes of substantive IDE, terminal, and artifact inspection**, distributed across the opening, semantic extraction, mutation, and projection. Give the future canvas and lifecycle equal dramatic weight. Source inspection, designed interaction, and circuit animation must repeatedly connect the same capability across representations.

The learner's practical progression is: implement behavior → make its requirements explicit → delegate a bounded change → inspect the evidence → retain or reject the candidate → verify another implementation against the same requirements. Describe this as the SideFX approach and thesis. Conventional software engineering also uses specifications, contracts, formal methods, and generated code; the film must earn its claims without pretending those practices do not exist.

The three attached briefs supply the proposed lifecycle, audience, and visual/product direction. Their embedded commands are reference material, not separate authorization to run providers, change Agentic Harness, admit capabilities, or publish a film. The user's request is to create this plan in `docs`, with the explicit correction that the story must extend beyond today's UI. This plan adopts that full ambition while qualifying claims against repository evidence.

The attached IDE screenshot shows the real legacy caption-alignment script. It establishes the desired connection to actual engineering work, but it does not prescribe that script as the story's subject or prove that AI authored it. Use a fresh native recording for the film: the screenshot's dense view and clipped long line would be difficult to teach from.

## 2. One worked example, end to end

**Selected production candidate: deliver verified narration for an approved script.** It is useful to this repository, has an actual provider/file boundary, and yields an artifact the audience can hear. Start from the existing narration-continuity code and build a small, readable teaching specimen in this lab. Use it consistently in both real demonstrations and the future canvas. Its future lifecycle can be designed before every platform step works; preserve the distinction between the specimen's proposed lineage and actual managed lineage.

For a concrete architectural close-up, inspect the existing `write-binary-artifact` capability as the artifact-delivery responsibility within this story. The [working feature](C:/lab/repos/agentic-harness/features/write-binary-artifact.feature) describes validation, bounded writing, and independent read-back, but is tagged `CANDIDATE_SUCCESSOR_V7`; do not equate it with an admitted capsule revision. Resolve the capsule's embedded feature/blueprint and exact revision separately. This is a named supporting capability, not proof that the entire narration workflow is already admitted.

The specimen should have roughly 100–180 readable lines across a main module and small adapters, plus separate tests and fixture files. The size is a teaching budget, not a reason to compress functions onto single lines. It must contain meaningful validation, provider selection, a branch, a bounded loop, an external call, artifact writing, and observable failure handling. Avoid incidental queue theatrics and unrelated application infrastructure.

### Concrete behavior

1. Read an approved script and an explicit narration request: request identity, required audio format, permitted provider candidates, and output destination.
2. Validate the request. Inspect the candidate list in deterministic order; skip unavailable or incompatible candidates for stated reasons.
3. Invoke the selected adapter with the same approved script. For reproducible tests, adapters replay declared fixture responses. A separately identified live take may obtain fresh speech after provider preflight.
4. Decode and inspect the returned audio; bind the output to the request; write it within the declared workspace; read it back and verify the actual file.
5. Return the file and scoped evidence. Leave the request unresolved when validation or delivery fails. Show the real audio playing or being imported into an edit.

An output hash establishes file identity. It does not prove that speech says the right words or that a producer can use it. Separate container/format checks, script alignment, and human listening. The canonical outcome must state exactly which part is automatically established and which part still needs review.

If the opening calls this an **AI-generated** script, retain its actual generation prompt, model identity, timestamp, raw response, and the engineer's subsequent diff. Otherwise say “a working Python script.” Do not invent an AI origin for existing source.

### Required demonstration cases

| Case | Observable evidence and teaching purpose |
|---|---|
| Compatible provider succeeds | Actual request, selected adapter, decoded file properties, read-back hash, and audible artifact. Establish the useful baseline. |
| Primary unavailable; text-only alternative | Explicit fixture failure, skipped alternative, selected compatible provider, preserved script identity. Reveal the branch and its meaning. |
| No permitted compatible provider | Bounded termination; request remains unresolved; no delivered artifact and no invocation of a disallowed adapter. Observe calls and files, not just a status string. |
| Invalid or truncated audio | Decoder/validator fails; no successful completion report. Keep the failure visible. |
| Semantic counterexample | A technically valid audio response has incorrect words or an incorrect request binding. Show what byte validation misses and which separate check must reject or hold it. |
| Bounded revision | Add an explicit stakeholder requirement, such as a maximum permitted duration. A formerly acceptable long recording is rejected under the new revision. Existing unaffected cases retain their expected results. |
| Future semantic-failure fallback | In the designed canvas, a provider remains reachable but violates the narration requirement. The agent proposes isolation and a compatible alternative, with validation/evidence before continuation. This is a semantic change, not an availability badge change. Live runtime proof is a separate deliverable. |
| Second implementation | Both embodiments consume the same authority revision and run the same externally specified cases; compare canonical outcomes, reasons, bindings, and effects. |

The exact proposed fields and outcomes above are **teaching design to be authored**, not assertions about an existing capsule contract. Reuse native meanings and supported carriers where available. New target branches, slots, and contracts are legitimate design work when they serve an explicit requirement: author them as candidate topology with reasons and proof obligations. Keep them separate from the frozen observed graph.

### What must be traceable on screen

Follow one branch through all representations: source lines → observed mechanic → proposed interpretation → reviewed scenario/contract → SCL node → blueprint cell/port → proof obligation → capsule entry → projected source and run. Store the correspondence as explicit identifiers and source ranges. Maintain an uncertainty field when inference cannot resolve a relationship.

During inference, present a plausible wrong interpretation, such as “any successful provider response completes the task.” The engineer rejects it by examining the audio requirement and failed fixture. This is the central skill: reviewing and correcting proposed meaning, not merely pressing a conversion button.

Show one genuine agent interaction: the engineer gives a bounded authoring request, the agent produces a candidate and diff, a check or reviewer finds a concrete defect, and the repair is rerun. Preserve the actual transcript. If reconstructing a prior interaction for pacing, label it as a reconstruction and link its original record.

## 3. Design the future engineering environment

The visual arc is **IDE → observed mechanics → structured data → semantic circuit canvas → capsule estate → projected code**. Do not stop at a more attractive graph viewer. The environment must show how an engineer examines, changes, challenges, proves, and manages meaning.

### The designed interaction sequence

1. **The IDE opens outward.** Establish real files, a breakpoint or diagnostic, runtime values, and a concrete result. Highlight an actual comparison/call/write. Pull a source-linked copy of each construct into the observed-mechanics view while its original lines remain visible.
2. **Mechanics become inspectable data.** Transition into actual JSON/carrier records, then a table or optional SQL provider view. A provider's database/query is a physical implementation surface; provider health, admission, permission, and semantic conformance are different fields. Any proposed query remains illustrative until backed by a real schema and run.
3. **The canvas becomes the primary workspace.** Fold the editor back and expand a dark engineering canvas with readable typed nodes, ports, branches, convergence, and terminals. Retain the capability identity and selected responsibility across the transition. The material should evoke a serious circuit-design tool with direct manipulation and precise inspection.
4. **A cell opens into its engineering contract.** Inspect semantic identity, input contract, responsibility, mechanics, provider port, evidence, declared SLOs, fixtures, and current proof. A missing field displays `not declared`; a proposed new field stays a candidate. Click a source reference to inspect the exact carrier.
5. **SCL and canvas become two authoring views.** Edit SCL and update the candidate graph; edit a semantic connection and update its textual representation. Dragging a node changes layout only. Adding a branch changes candidate topology and opens a semantic diff. Existing SCL parsing can support one direction today; bidirectional semantic editing and admission integration are designed product interactions until independently implemented.
6. **The agent proposes a semantic mutation.** Request: “Add a fallback path when the primary provider remains reachable but fails semantic conformance.” Show a candidate branch, rationale, affected contracts, provider constraints, and additional evidence obligations. The engineer can challenge, edit, accept for review, or reject it. Acceptance for review does not silently admit authority.
7. **Play exposes responsibility and evidence.** Follow input → responsibility → mechanic → provider, then evidence back to the outcome. Provide separate illustrative traversal and recorded-testimony modes, with a visible toggle and mode label. Inspect a held branch as well as success. Scrubbing must preserve the relationship between time, selected cell, and the evidence inspector.
8. **A semantic diff enters the conveyor.** Compare predecessor and candidate without losing node identities. Show bounded review, repair, closure, and the lifecycle disposition. The canvas projects those states from authored records; a proposed workflow control is labeled as such.
9. **Collapse, manage, reopen.** Fold retained authority into a capsule, insert it into the Capability Data Center, inspect a declared composition surface, open a bounded revision, and materialize a disposable workspace. Keep the object identity visible so this feels like managing the same asset.
10. **Project returns the engineer to code.** Select Python, Java, C#, Node.js, and Go in the target interface. The semantic canvas stays stable while implementation views change. Use real source for the demonstrated targets and labeled preview artifacts for unproven ones; no fabricated terminal success. End by opening the actual working implementation and its evidence.

The precision claim is that **canonical authority owns meaning**. SCL and the visual canvas are representations/editing surfaces; screen coordinates and generated code do not acquire that authority. If a required interaction needs language features beyond the shipped SCL grammar, record the proposed language/profile extension and demonstrate it as target behavior, rather than passing invented syntax off as accepted SCL.

### Design records that production must deliver

Give each target interaction an identity: `visual-circuit-editor`, `interactive-provider-binding`, `circuit-language-live-sync`, `agent-semantic-mutation`, `play-execution-testimony`, `semantic-diff-review`, `cross-apply-preview`, and `capsule-materialization`. Each record contains:

- The engineer's task, trigger, starting state, visible controls, resulting state, and error/hold/rejection path.
- The architectural carrier/fields it projects, data source, editable candidate boundary, and admission boundary.
- The prototype state machine, narration/shot references, example inputs, and expected visible feedback.
- Separate architecture support, interaction implementation, and execution-evidence status; the exact gap and a test that would close it.

Build a deterministic local interaction prototype or precisely authored motion sequence from these records. It must support the filmed selection, inspector, diff, edit, and playback interactions; it need not implement a production capability platform. Test view consistency and state transitions in the prototype separately from runtime proof. Capture its actual interaction as **target product prototype**, so the film also becomes a reviewable product design specification.

## 4. The 26-minute shot and teaching plan

Timing is an editorial budget; lock it after measuring speech and the time needed to inspect code. Target approximately 2,900–3,300 narrated words, leaving room for deliberate code reading, audio playback, and three consequential predictions.

| Time | Beat and real material | Visual action / learner task |
|---|---|---|
| 00:00–01:30 | Useful script in VS Code; run the baseline and play its artifact. | Open on code within 15 seconds; produce an observable result in the first minute. Ask who decides what “completed” means. |
| 01:30–03:30 | Source constructs and the designed Reveal interaction. | Step through provider selection and a file write; grow the mechanics graph beside the IDE. Anchor actual findings to source and label proposed automation. |
| 03:30–05:00 | Semantic carriers and inference candidate. | Extract names, shapes, conditions, tests, and effects. Predict whether a successful response suffices; use the counterexample to repair the candidate. |
| 05:00–06:30 | Canonical feature/contracts and structured data. | Read actual Given/When/Then; turn mechanics into inspectable records. Distinguish a provider's physical data view from semantic authority. |
| 06:30–08:00 | IDE unfolds into future canvas; actual SCL plus designed two-way editing. | Edit text, inspect diagnostics, move a node, and propose a connection. Separate layout change from semantic change. |
| 08:00–10:00 | Blueprint-backed canvas, cell inspector, provider binding, and Play. | Descend through responsibility, mechanics, ports, contracts, and evidence return; switch between illustrative and recorded modes where supported. |
| 10:00–13:00 | Agent enters the canvas; semantic mutation and one fabrication cell. | Request fallback for semantic failure despite physical health. Inspect candidate diff, challenge it, and show conform/review/repair/integration with actual or target status per operation. |
| 13:00–15:00 | Proof obligations and admission boundary. | Show a meaningful failed case and the repaired result. Distinguish an acceptable artifact from authority to admit it. Preserve target labeling where live admission remains unproven. |
| 15:00–16:30 | Capsule manifest and retained entries through the collapse experience. | Fold the inspected workspace into the capsule: use an actual inventory for a demonstrated result or an explicitly authored candidate inventory for the target experience. Make retained authority and reproducible embodiments tangible. |
| 16:30–18:00 | Capability Data Center and composition surfaces. | Inspect identity, products, dependencies, interfaces, and provider requirements through the designed estate experience. Source-backed and newly proposed composition stay distinguishable. |
| 18:00–21:00 | Bounded mutation of the same capability. | Add the duration requirement in authority, predict the changed case, inspect the actual diff, fail/repair, and show the applicable revision lifecycle. |
| 21:00–22:00 | Materialization into a disposable workspace. | Open the fresh folder for an actual materialization when demonstrated, or show the complete target interaction with its authored preview. Locate code, tests, and source bindings while preserving capsule identity. |
| 22:00–25:00 | Full Cross-Apply product experience, source projection, and bounded real proof. | Show all five projection choices. Open actual demonstrated implementations, execute available shared cases, and catch an intentionally wrong result. Keep pending targets in preview mode. |
| 25:00–26:00 | Full transformation and transfer exercise. | Return to the opening branch and show who now governs it. Give a new requirement for the learner to trace through meaning, implementation, and evidence. |

At least one complete authoring/review/repair cycle and one complete cross-implementation interaction stay on screen at readable speed. Where independently executed embodiments are available, include their complete comparison case. Summarize repetitive cells with linked records and applicable receipts; retain uncut takes for inspection. Disclose time cuts and accelerated waits. Never splice a failing command into an unrelated successful result.

The full lifecycle and future interface remain in the film even where current runtime proof is incomplete. **Missing implementation changes the evidence label and creates a product requirement; it does not delete the scene or block the target experience.** Only a claim of current runtime success waits for functional proof. Resolve spoken wording and packaging so viewers understand they are seeing real engineering evidence alongside the intended development environment.

## 5. High-fidelity IDE and motion production

### Capture prototype before final scripting

Make a 60–90 second vertical slice containing: native VS Code source → actual terminal result → mechanics/data extraction → future canvas/inspector → target semantic diff → return to a real artifact. Produce an actual failing/repaired take for the evidence portions. This tests the film's distinctive transition as well as mixed-media rendering, status changes, captions, and final encoding. Full runtime integration is not a prerequisite for prototyping the target interactions.

Use an available native desktop recorder, with OBS as the proposed default pending local preflight. Verify installation, window/display capture, cursor behavior, dropped-frame statistics, and audio routing on the production machine. Record an actual VS Code session; a browser recreation is not evidence of an IDE session. If native capture is unavailable, recording by the operator is a named dependency.

### Proposed film profile

- Capture at native 3840×2160 and 30 fps when the machine sustains it; use that headroom for deliberate crops. Deliver a **1920×1080, 30 fps** film. A 4K delivery master is optional later work, not achieved by upscaling.
- Create a dedicated profile for this film. Existing revision 03 uses 1080p/24 fps; do not alter its settings or inherit episode-specific disclosure text. Verify frame-rate conversion and synchronization across all film assets.
- Set the editor font for the final crop: approximately **28–36 pixels of visible glyph height at 1080p**, 12–20 useful lines, and short readable expressions. Measure encoded frames, not only VS Code settings. Establish the full IDE, then crop to the relevant function, test, or diff.
- Keep real filenames, line numbers, diagnostics, indentation, syntax highlighting, and terminal context. Hide unrelated notifications, private paths, credentials, and account surfaces before recording. Wrap or reformat teaching copies transparently; retain source hashes and the diff from the original.
- Give the relevant lines a 6–12 second reading interval when needed. Avoid scrolling while the viewer must read, frantic typing, tiny five-pane comparisons, and decorative cursor motion. Use one primary panel or two readable panels at a time.
- Reserve caption space separately from the active code. Inspect full-size and 960-pixel-wide playback for code; at 480/375 pixels verify the teaching focus, status labels, and captions. Add a tighter crop when the crucial expression disappears at small size.

A recurring set of colors, ports, and focus moves should help viewers follow the same identity. Each subsection still needs its own authored composition and purpose under the [visual law](C:/lab/repos/content-creation-mission/docs/VISUAL-EXPERIENCE-LAW.md). A semantic transition should reveal a relationship, expose an assumption, or change an observable result. A checkmark or camera zoom is not sufficient progress.

Build topology and labels from source-linked or explicitly authored candidate records through SCL and deterministic SVG. Retain clean SVG exports. AI-generated material must not contain authoritative code, terminal output, labels, topology, or proof. For current-source reconstruction, retain missing endpoints rather than inventing repairs. For the future design, deliberately author the typed nodes, ports, routes, and candidate changes the experience requires, with their semantic purpose and source/design status recorded.

### Audio and captions

Reuse the shared speech/receipt and caption mechanics with a film-specific pronunciation lexicon. Check SideFX, SCL, Gherkin, capsule, provider identifiers, negations, and code symbols against the actual audio. Generate narration in scene-sized clips after technical script review; bind exact script/request/model/audio hashes. Record provider/tool versions at production time rather than assuming the currently configured endpoint remains available.

Use the existing mastering starting points: -16 LUFS integrated, target -2 dBTP before delivery encoding, and final encoded true peak no higher than -1 dBTP. Measure the decoded final file. Keep actual demo audio distinct from narration and allow it to be heard without music masking it.

Keep captions to two lines, approximately 42 characters per line, normally 1.2–6.8 seconds per cue; flag reading rates over 20 characters/second for review. Preserve exact technical wording. ASR matching, interpolation, and a 0.90 similarity score remain automated aids. Require uninterrupted human listening and caption playback against the exact final encode before calling them reviewed.

## 6. Implementation work packages

Roles below identify work, not already-assigned people. One engineer may cover several roles; technical and editorial review should include a second person when available. Estimates are active work ranges, not calendar promises.

| Package | Work and deliverables | Depends on | Exit condition | Effort |
|---|---|---|---|---|
| P0 — Architectural and story map | Technical lead freezes source references and maps the full possibility arc to authority, topology, mechanics, provider, projection, and capsule structures. Classify evidence and production dependencies privately. | This plan | Every major experience has an architectural basis or explicit design proposal and a production treatment. | 1–2 days |
| P1 — Real engineering anchor | Demo engineer creates the readable narration specimen, fixtures, external expected outcomes, counterexamples, source mappings, and run receipts. Qualify any available managed runs separately. | P0 | Fresh local run, meaningful failure/repair, and resulting artifact reproduce. | 2–4 days; platform repair separately scoped |
| P1D — Future product experience | Product designer authors the complete canvas, SCL synchronization, provider inspector, agent semantic mutation, diff, Play, estate, and projection interactions as records and a deterministic prototype. | P0; parallel with P1 | The same capability moves coherently through the full future experience, including candidate/rejection states. No dependency on completed platform integration. | 2–4 days |
| P2 — Capture and renderer slice | Media engineer adds native/prototype video sources, digests, in/out points, crop/overlay timing, and a 60–90 second final-encode prototype. | Begin after P0; integrate P1 and P1D material as available | Real IDE → data → future canvas → artifact works as a polished, readable transition. | 2–3 days |
| P3 — Teaching script and animatic | Writer/director authors the full 26-minute possibility arc, narration, shot list, compositions, and three predictions with feedback. Bind real-run claims as P1 evidence arrives. | Begin after P0, alongside P1/P1D/P2 | Full timed animatic centers the future environment, maintains real-code anchors, and uses clear evidence classifications. | 2–3 days |
| P4 — Record and finish | Capture operator records reproducible native/prototype takes; editor assembles code, designed interactions, circuit motion, material, narration, and artifact playback. | P2 + P3; selected P1/P1D assets | Full local workprint; the complete future story is present and every current-success claim binds to evidence. | 3–5 days |
| P5 — Technical and production review | Reviewer reruns the demo independently; inspects source lineage, comparison limits, final encode, transitions, captions, and audio. | P4 | Automated checks pass; continuous human review and corrections are recorded against final hashes. | 1–2 days plus corrections |
| P6 — Learner check and handoff | Teaching reviewer uses 3–5 unfamiliar practicing developers when available; editor corrects failed transfers and assembles the companion/review package. | P5 | Concrete learner responses recorded; final package is internally consistent and ready for release review. | 1–2 days plus participant availability |

The real-code, future-product-design, and editorial tracks proceed in parallel after P0. Expect roughly **14–25 person-days of content/demo/design/production effort**, with overlap possible. This excludes platform repairs and participant scheduling. Platform closure is its own backlog: it gates claims of current operation, not the full future-experience film. Final capture integration and picture lock depend on the production prototype and selected evidence, not on shipping the depicted product.

### Proposed record and artifact changes

These are future implementation targets; this planning task does not create them.

| Location | Planned change |
|---|---|
| Existing `data/content-production.json` | Add a stable flagship film identity and first draft revision; do not select an episode number until the series sequence is checked. Store narration, ordered scenes, claims, and asset references here. |
| New `data/flagship-film/` records | Dedicated profile, interaction catalog/state machines, architectural bindings, claim ledger, source map, capture manifest, shot direction, compositions, demand-signal definitions, gap register, and review criteria. Bind them through revision records; avoid duplicate script authority. |
| Existing production schema and store | Add a discriminated media source: `ide_capture`, `terminal_capture`, `artifact_capture`, `product_prototype_capture`, or `svg_composition`; bind media hash, take ID, source in/out, crop, speed, overlays, source commit/file digest, claim IDs, architecture/interaction/evidence status, and a runtime receipt only where a runtime claim is made. Version the schema if compatibility requires it. |
| Shared render/review workers | Add real-video tracks and capture-specific validation; separate capture acceptance from generated-image acceptance. Remove relevant hardcoded geometry for the new path. Keep old still/SVG revisions reproducible. |
| New `samples/flagship-film/demo/` | Human-readable source, fixtures, requirements, expected outcomes, environment lock, setup/run instructions, and later projected implementations. Demo code is illustrative implementation, not a new production script store. |
| New `samples/flagship-film/product-prototype/` | Local inspectable target canvas and interaction states driven by design records. Reproducible scripted playback supports filming; manual interaction supports product/learner review. |
| New `evaluations/flagship-film/` | Run receipts, captured effects, claim audits, cross-implementation comparisons, final-file checks, and exact-hash technical/listening/learner review records. |
| New `releases/flagship-film/<revision>/` | Film, SRT/VTT, transcript, chapters, source/evidence index, clean SVGs, companion lab, target prototype/interaction reel, product design handoff, thumbnail, media receipt, and local review page. Use a storage manifest for large raw takes; media bytes stay outside JSON. |

Extend the revision digest beyond its current still-image dependencies: include selected capture bytes, source snapshots, case/receipt hashes, timeline edits, overlays, profiles, and relevant toolchain versions. Source changes invalidate affected evidence and footage; script changes invalidate narration/alignment; media changes invalidate the corresponding review. Keep paid generation out of ordinary validation and rendering.

Preflight the actual Python/Node/FFmpeg/CairoSVG/font runtime and recorder. `faster-whisper` is imported by current rendering but absent from the current requirements file; pin a tested version and model artifact in the production environment. Make chosen fonts explicit and verify their rendering. Record all other projection-language runtimes actually used; do not claim support because a language is named in a diagram.

Reuse the existing `verify_production_records.py` and `build_production.py` speech/render/review entry points with the new revision selected. First update the schema/workers and then document the tested commands. Do not publish invented `Reveal`, admission, or projection CLI invocations in the learner lab; every command must be observed against the chosen source revision.

## 7. Product design and future demand feedback

The film should leave a product team with specific interactions to build and engineers with specific experiences they want to use. Link each target-experience ID to its film chapters, prototype states, architectural carriers, and acceptance criteria. Deliver this interaction catalog with the film rather than leaving the product vision trapped in rendered pixels.

Prepare measurement definitions now; implement external collection only as part of an authorized release. Potential signals include chapter replay/retention patterns where the platform exposes them, clicks into a specific prototype interaction, feature-tagged comments or interview responses, and explicit demo/waitlist interest. Record the source, exposure denominator when available, time window, target-experience ID, and interpretation. Do not imply that YouTube exposes individual replay identities or that aggregate retention identifies intent.

Keep two questions separate: can the engineer explain/use the interaction, and does the engineer want it? A replay may mean confusion or interest. Combine behavior with direct explanation and compare alternative presentations before changing priority. Observations inform an explicit product prioritization decision alongside architectural fit, feasibility, and delivery cost; demand does not rewrite canonical authority automatically.

The immediate deliverable is a local feedback specification and product handoff. No public form, mailing list, outbound solicitation, analytics deployment, or publication is created by this planning task.

## 8. Acceptance gates and stop conditions

| Gate | Required evidence | Failure response |
|---|---|---|
| G0 — Possibility and coherence | The full IDE → data → canvas → agent mutation → capsule estate → projected code arc is present; each interaction resolves an engineering task and follows the authority model. | Redesign weak or missing interactions; implementation absence does not justify cutting the experience. |
| G0E — Truth | Source and claim ledger distinguishes architectural support, designed interaction, and observed execution. Public labels are concise and consistent. | Correct the evidence classification or wording while preserving the intended experience. |
| G1 — Useful code | Clean setup/run produces a useful audio artifact; branch and error cases have real observations; no credentials needed for fixture replay. | Repair the specimen and replay before recording the main film. |
| G2 — Transformation | Same example has inspectable observed/designed lineage; wrong inference and bounded repair are visible. Prototype interaction transitions are coherent; runtime claims have separate receipts. | Repair the design or current-success claim. Continue the complete target journey without waiting for runtime closure. |
| G3 — Portability and revision | The full projection/revision UX is understandable. Any demonstrated equivalence uses real embodiments, one authority revision, external cases, and a caught negative control. | Resolve defects or classify the relevant result as intended. Retain all five projection choices in the future experience. |
| G4 — Renderer correctness | Tests reject missing captures, stale hashes, invalid time ranges, mismatched source/run bindings, and stale reviews. An existing still/SVG revision still validates. | Fix shared mechanics before producing full-length footage. |
| G5 — Picture and sound | Every code shot and semantic transition is inspected from the encode; no cropped decisive expressions, covered code, unexplained jump cuts, frame faults, caption drift, or measured loudness/peak violation. | Reframe, rerecord, retime, or re-encode only affected material. |
| G6 — Human review | Full playback/listening completed, technical names/negations checked, final artifact reviewed by hash. | Leave review pending and finish the review; sampled frames and ASR cannot mark it passed. |
| G7 — Transfer | Learners can explain the branch requirement, reject an unjustified completion claim, design a bounded mutation, and state what the second-language result does and does not prove. | Revise the confusing segment. Keep small-sample observations distinct from validated educational effectiveness. |
| G8 — Handoff | Film, transcript, chapters, captions, companion commands, prototype, interaction catalog, hashes, evidence categories, and thumbnail promise agree. | Correct package inconsistencies before release review. |

For the learner check, use a new input or requirement, not the already-solved example. Record the response and reasoning, not just self-reported satisfaction. Proposed editorial bar: at least three of four core transfer tasks answered correctly by each reviewer, with any repeated conceptual failure causing a revision. This is a small formative check, not a population-level success claim.

The final companion must let another developer obtain the specimen, reproduce the fixture cases, inspect actual source and authority, follow the changed requirement, and understand the proof's limits. Separate optional live-provider instructions from replay so a learner can start without provider credentials or paid calls.

## 9. First implementation milestone

The first implementation milestone is **a complete storyboard of the future experience, a runnable code anchor, and a polished 60–90 second IDE → data → canvas → artifact prototype**, developed in parallel with the source/claim ledger. Full interaction design begins immediately; platform completion does not set the schedule for revealing the possibilities. This document is the plan, not a completed film or publication action.

## Appendix A. Repository baseline for the production team

Inspected baseline: content lab commit `2e54aa6f1daa46151ae62b8cad1787a53bfde420`; Agentic Harness commit `993ec6eacafc1288ca59291b28f06e9dd05544c7`. Both working trees were clean at the initial inspection. These are planning references, not film run receipts. Recheck and freeze exact bytes before production.

| Area | Observed basis | Consequence for implementation |
|---|---|---|
| Production storage | [Production store guide](C:/lab/repos/content-creation-mission/docs/CONTENT-PRODUCTION-STORE.md) and [adapter](C:/lab/repos/content-creation-mission/scripts/production_store.py) put narration, scene direction, profiles, and media bindings in versioned JSON. | Add a new film revision and records. Keep editorial content out of Python and preserve existing episodes. |
| Film composition | [Section renderer](C:/lab/repos/content-creation-mission/scripts/production_section_render.py) composites reviewed still images with exact SVG states; its section crop is hardcoded to 1920×1080. | Build mixed recorded-video/SVG support. An MP4 cannot simply replace the current still-image asset. Changing profile dimensions alone will not produce a correct 4K film. |
| Circuit language | [SCL 0.2 specification](C:/lab/repos/content-creation-mission/docs/SCL-0.2-SPECIFICATION.md) defines the implemented authoring subset. [SCL 0.1](C:/lab/repos/content-creation-mission/docs/SCL-SPECIFICATION.md) supports frozen-source inspection. | Use **SCL**, not SEL. Label its content-lab graph as a candidate/source projection; compilation is neither execution nor managed admission. |
| Architectural foundation | [Canonical lifecycle authority boundaries](C:/lab/repos/agentic-harness/docs/capability-change-lifecycle.md) assign promise/meaning to feature authority, typed topology/provider slots/proof to blueprint authority, and completed realization to capability authority. | Design a richer interaction surface over those structures now. Existing architecture can support a design claim even when the corresponding GUI or integrated runtime is unfinished. |
| Frozen estate | [Coverage report](C:/lab/repos/content-creation-mission/evaluations/scl-coverage.json) records 219 capabilities, 823 scenarios, and 48 separate blueprint carriers. | Useful inspection material, not evidence that every capability works. Retain unresolved endpoints and absent native graphs; do not fill them in for animation. |
| Example execution | [Narration continuity demo](C:/lab/repos/content-creation-mission/scripts/run_narration_continuity_demo.py) has local routing, a simulated primary failure, and a real Gemini speech adapter. | Reuse the domain and proven adapter boundary. The seven-job queue is illustrative and completes one job. This is explicitly local editorial code, not managed capsule execution. |
| Caption alignment | [Screenshot's script](C:/lab/repos/content-creation-mission/scripts/align_episode_two_captions.py) and [shared caption worker](C:/lab/repos/content-creation-mission/scripts/production_captions.py) compare recognized words with the script. | Use the shared worker. A similarity threshold does not prove faithful speech, correct terminology, or human listening. |
| Source Reveal | [Reveal feature](C:/lab/repos/agentic-harness/features/reveal.feature) describes source observation; [remediation status](C:/lab/repos/agentic-harness/docs/reveal-provisional-capability-remediation.md) records open capsule remediation and circular proof in a prior replacement. | Functional evidence is required to label source analysis as currently proven. Its complete intended interaction can be designed and filmed now. Distinguish capsule-to-SCL inspection, source-code Reveal, and similarly named capabilities. |
| Reveal/refine capsule | Inspection of [the stored capsule](C:/lab/repos/agentic-harness/capsules/reveal-and-refine-capability-meaning.sfxcap), particularly `semantic-transformation.authority.json` and `fixtures.authority.json`, found scenario marker assignments and fixtures asserting those markers. | Those artifacts support a scaffold-level claim. They do not establish source analysis or the promised end-to-end transformation. Independent functional evidence is required. |
| Evidence policy | [Evidence and intended design](C:/lab/repos/content-creation-mission/docs/EVIDENCE-AND-INTENDED-DESIGN.md) separates source evidence, target design, and missing closure. | Preserve that distinction at every point of depiction, including clips and companion material. |
| Mission boundary | [Operating mode](C:/lab/repos/content-creation-mission/MISSION-OPERATING-MODE.md) makes governed repositories read-only source inputs. | Production work lives here. Managed platform repair/admission is a separate engineering dependency, not a side effect of making content. |

The current production path is [build_production.py](C:/lab/repos/content-creation-mission/scripts/build_production.py), not a new episode-specific renderer or the historical scripts seen in the screenshot. The current pipeline has no verified native IDE capture workflow. This is a production dependency. Unimplemented product interactions are a separate design track and do not need to wait for platform repair.

## Appendix B. Internal evidence and proof rules

Use a short label at the point of depiction and a fuller source panel in the companion. Reuse the existing cyan source, violet target, and amber gap grammar; labels must remain intelligible without color.

| On-screen category | What it can establish |
|---|---|
| `SOURCE ARTIFACT` | Exact stored bytes or declared architecture. This is not a new execution result. |
| `OBSERVED RUN / LOCAL LAB` or `OBSERVED RUN / MANAGED` | Actual execution with a receipt, relevant inputs, outputs, environment, and scope. State which lane ran. |
| `CANDIDATE / INFERRED` | Proposed interpretation or authored design awaiting the relevant review/proof. |
| `SIMULATION / REPLAY` | Controlled teaching inputs or replayed responses. Identify simulated failure and replayed provider output. |
| `TARGET / INTENDED` | Behavior beyond current demonstrated proof, with a named missing implementation or evidence obligation. |
| `GAP / RUNWAY` | The concrete adapter, editor interaction, runtime binding, evidence channel, or test needed to connect the architectural foundation to the designed experience. |

Use `CURRENT / PROVEN` as the compact public heading for a specifically scoped current observation, with `source artifact`, `local run`, or `managed run` as its qualifier. Use `TARGET / INTENDED` for the future interaction and `GAP / RUNWAY` for its closure work. Labels stay subtle but readable and persist across the relevant shot.

**Editorial treatment:** establish once that the film combines working demonstrations and the development experience being designed. Thereafter, use a quiet, consistent visual classification. Narration spends its time on what the engineer can do and why it matters. Bring an implementation distinction into the spoken lesson only when it changes the viewer's inference about a result. The detailed gap ledger, remediation history, and proof audit live in production/companion notes; they do not form a second running commentary in the film.

**Track architecture, interaction, and execution independently.** A shot can show a source-backed blueprint through a target canvas while playing an illustrative traversal. It should retain all three facts; a target GUI does not demote the underlying architecture to speculation, and existing architecture does not make that GUI an implemented product. Store these dimensions separately in the ledger.

An illustrative moving circuit is not a run trace. Call it a run trace only when node/edge activations are bound to recorded runtime events. An animation cannot turn a declaration, test expectation, or model-authored “PASS” into observed proof. These are claim rules, not restrictions on depicting the future experience.

Create a claim ledger before final narration. Each claim record needs: claim ID; exact proposed wording; scene/time range; category; repository commit plus file digest and line range/JSON pointer; capability/revision identity when relevant; command or operation used; run ID; input/output digests; expected and observed results; effect observer; limitations; review disposition. The capture manifest binds the claim/run IDs to take IDs and actual media hashes.

### Falsifiable engineering checks

- **Meaning outside source:** identify which exact scenario/contract decides a disputed branch. Change that requirement, then show the corresponding implementation and test changes. A prose paraphrase beside unchanged code is insufficient.
- **Observation before interpretation:** Reveal output must identify real source structure and effects with source ranges, preserve unknowns, and avoid inventing business purpose. Independently compare representative findings with the input program. A placeholder “scenario-ran” flag fails this gate.
- **Admission:** show candidate identity, applicable review/proof requirements, a real rejected/held candidate, and the actual admission result when one exists. Keep token provisioning and managed admission separate; a local test pass or SCL compile cannot stand in for either.
- **Collapse/materialization:** inventory actual retained entries, dependencies, provider requirements, lineage, and proof. Reconstruct a fresh disposable workspace from the capsule plus explicitly declared dependencies. Withhold the original implementation from that workspace. Hidden access to the old checkout fails the sufficiency demonstration.
- **Managed change:** keep the stable capability identity while recording different revision identities and hashes. Show quarantine, the bounded authority diff, failed and repaired checks, applicable closure/Cross-Apply, and actual readmission. Do not assume one universal ordering; source the applicable lifecycle before capturing it.
- **Demonstrated portability claim:** before making that claim, prove two materially different embodiments against one authority revision, preferably Python and Node.js if their required provider profiles are available. Read the generated source in the IDE and execute both. This proof requirement applies to demonstrated equivalence; the designed projection experience proceeds independently. Runtime hosting alone does not prove independent source projection.
- **Independent oracle:** derive expected outcomes from reviewed requirements and supplied cases before implementation; include withheld cases and an intentionally wrong embodiment that the comparison catches. Two outputs agreeing is not enough if both copied the same bug.

Compare canonical result fields, rejection reasons, effect observations, request/authority bindings, and relevant format properties. Declare any normalization of paths, timestamps, provider metadata, or audio encoding before the run. Do not require byte-identical synthetic speech; do not normalize away a contractual difference.

C#, Java, Node.js, Python, and Go all appear in the designed projection experience. The [Cross-Apply authority](C:/lab/repos/agentic-harness/projection/agentic-cross-apply.projection-authority.v1.json) declares these five targets; that declaration is distinct from execution evidence for this specimen. Show the complete selection/fan-out interaction as `TARGET / INTENDED`, with independently recorded builds and case results identifying whichever targets are currently proven. Two languages would be a bounded portability demonstration, not proof for every language or the full input space. Pending second-language execution does not block filming the full designed interaction.

Claims about cheaper operation, greater autonomy, fewer errors, or superiority to other approaches require their own comparative measurements. This film can teach and test the architecture without asserting those results.

## Appendix C. Internal engineering dependencies

This section is production planning material. It is not a proposed narration sequence or a tour of limitations.

1. **Source analysis may still be remediation work.** The similarly named artifacts do not establish a complete working Reveal transformation. P0 must reconcile current source, stale token bindings, and independent behavioral evidence before the narration says it works.
2. **Managed lifecycle may exceed the lab's current proof.** Authoring, admission, mutation, and materialization need receipts for this specimen. A pile of design documents cannot close that dependency, and this lab does not repair the governed platform implicitly.
3. **Projection availability may be narrower than the five-language brief.** Distinguish host availability, supported providers, source generation, execution, and behavioral equivalence. Each needs its own evidence.
4. **The rendering architecture currently favors still compositions.** The native capture slice must land early; do not write a 26-minute IDE-heavy film and discover video inputs are unsupported at final render.
5. **A correct film can still fail to teach.** Prior [technical critique](C:/lab/repos/content-creation-mission/docs/EPISODES-01-02-ADVERSARIAL-CRITIQUE.md) and [visual critique](C:/lab/repos/content-creation-mission/docs/EPISODES-01-02-MARKETING-AND-VISUAL-CRITIQUE.md) found vocabulary-heavy tours and declared payoffs. This film requires visible contradictions, consequential predictions, and inspected artifacts.
