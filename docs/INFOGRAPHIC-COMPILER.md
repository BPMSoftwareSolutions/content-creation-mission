# SideFX infographic compiler

Open [the reference studio](../samples/infographic-grammar/index.html). It works
from `file://` and HTTP; projections, symbols, and the estate inventory are bundled
locally. It needs no API key and invokes no live platform capabilities.

All executable authorship stays in this content lab. Frozen capsule snapshots
are read-only evidence; this work does not change Agentic Harness or its estate.

## Rebuild

Use Python 3.12 on Windows with Segoe UI installed. From this lab:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe scripts/rebuild_infographics.py
```

The rebuild verifies a portable official Graphviz archive under `.tools/`,
exports the schema, binds four reference contracts, produces SVG/PNG and phase
frames, renders the 1080p Manim specimen, packages the studio, and tests it.
`--skip-motion` reuses the movie; tests reject stale source or contract bindings.
No system PATH change is needed. Graphviz source URL and both archive/executable
digests are recorded in `data/infographic-runtime.json`.

For HTTP preview: `.\.venv\Scripts\python.exe scripts/serve_content.py --port 8765`.
Open `http://127.0.0.1:8765/samples/infographic-grammar/index.html`.
The loopback server supports media byte ranges.

## Real library responsibilities

| Library | Work performed |
| --- | --- |
| Pydantic + jsonschema | Strict semantic models and exported JSON Schema |
| NetworkX | Cardinality, reachability, cycles, graph traversal, obstacle routing |
| Graphviz dot 14.1.2 | Hierarchical circuit and aggregate placement |
| svgwrite | Fifteen fixed SideFX primitives and seven typed connector families |
| lxml | Inspect SVG identity and extract original groups for motion |
| CairoSVG | Render exact SVG primitives and text to PNG |
| Pillow | Measure labels and crop rendered groups for animation |
| Polars | Aggregate the 219-capability / 823-scenario source inventory |
| Manim | Reveal source-bound entities and trace compiled paths in dependency order |
| FFmpeg + PyAV | Package seekable MP4 and decode every frame |

igraph, OpenCV, Plotly, embeddings, and NLP remain optional additions for specific
scale, raster comparison, analytical, or motif-discovery needs. No report claims
they ran. Discovery may propose classification; it cannot invent execution edges.
Gemini may later supply scenery outside the protected graph. It must never invent
topology, labels, identifiers, provider state, or evidence status.

Installation references: [Graphviz](https://graphviz.org/download/),
[Manim](https://docs.manim.community/en/stable/installation.html),
[CairoSVG](https://cairosvg.org/documentation/).

## Authority and projection

`declarations/infographic-grammar.v1.json` owns the vocabulary.
`declarations/infographics/*.json` bind explicit meanings and source references.
`infographic_contract.py` validates schema, graph rules, hashes, and JSON pointers.
`compile_infographics.py` supplies replaceable geometry and SVG/raster exports.
`build_infographic_studio.py` adds interaction over the same IDs.
`animate_infographic.py` uses those original SVG groups and compiled paths.

The compiled `projection.json` adds layout, topology, aggregation evidence counts,
and a contract digest. `motion.json` describes five illustrative phases.
`motion-timeline.json` records arrival and reveal times. `motion-receipt.json`
verifies rendered media only; it asserts no capability execution.

| Reference | Coverage |
| --- | --- |
| scenario-current | Stored adjudication returns ALLOW or OPERATOR_REQUIRED; no live tool interception claimed |
| scenario-target | Intended two-sided certification: fan-out, two probes, ALL join, validation, conditional outcome, and missing testimony |
| capability-current | All seven source scenarios, shared declared providers, and six exact root invocation relationships |
| estate-target | Three-capability future circuit with two explicitly authored target product interfaces |

The current and target scenario views teach different boundaries: adjudication
and certification. They are not a before/after pair of one identical scenario.
Capability/estate interiors summarize I/E/O boundaries; detailed branches and
joins expand at scenario altitude. Row order is not product flow. Every collapse
retains exact member IDs and evidence counts; expansion recovers those members.
The searchable inventory is complete for the frozen generation. Four directed
infographic contracts are compiled; the entire estate is not yet editorialized.

## Exact junction geometry

Each junction owns its visible arm endpoints and unit direction vectors. The
renderer and connector router consume that same geometry. Branch and fan-out
arm counts follow actual outgoing edges; convergence arms follow incoming edges.
Status captions add no enclosing component box.

For endpoint positions S and E and unit flow tangents u and v, each connecting
cubic Bézier has controls P1 = S + a u and P2 = E - b v. The router solves for
positive handle lengths a and b by minimizing the parameter-space bending energy
integral of |B''(t)|². With d = E - S, the equivalent quadratic objective is:

```text
a² + b² + (u·v)ab - (d·u)a - (d·v)b
```

Linear constraints keep the control polygon monotone along axes where both
endpoint tangents agree with the displacement. An active-set solve compares the
unconstrained optimum, constrained boundary optima, and boundary intersections.
It preserves endpoint contact (C0) and tangent direction (G1), with no fixed
pixel handle length. This is not a claim of C1/C2 continuity or minimum geometric
curvature along arc length.

The final SVG is measured independently: connector endpoints must coincide with
the actual rendered arm endpoints, and their derivatives must align with those
arms. Every exposed arm must have a connection. `junctionGeometryProof` in each
compiled projection records contact and angular errors. Gates reject contact
error above 0.000001 SVG units or tangent error above 0.0000001 degrees; fixtures
deliberately detach a connector and kink its tangent to exercise both gates.

## Verification and limits

Geometry checks reject node overlap, canvas overflow, insufficient label height,
and routed edges penetrating unrelated node bodies. Execution paths leave a
background clearance over information-line crossings so they do not look like
junctions. This complements visual review; it does not prove optimal edge-label
placement for every arbitrary graph.

SVG labels use 23 px for node titles, 16 px for body/edge text, and 13 px for
evidence captions. Fit view is an overview; zoom and the inspector provide detail.
Semantic gates cannot decide whether a sentence overstates its source; that
remains an editorial review responsibility.

Adversarial tests exercise stale provenance, unsupported observed claims,
incompatible product ports, incomplete branch/join rules, lost aggregation
members, false active providers, unbounded retries, and geometry failures.
Export checks preserve shapes, text, IDs, and evidence modes across all frames.
The Manim check requires both probe arrivals before convergence is revealed.
