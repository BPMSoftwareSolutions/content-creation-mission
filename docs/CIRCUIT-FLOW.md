# Silver-ball circuit flow

The capability page now plays an end-to-end flow through the existing SVG.
`templates/circuit-flow.js` is a reusable, dependency-free browser module. The
page builder ships the exact module bytes alongside both capability editions and
binds them in each build receipt. No new images or provider calls are required.

## Motion language

- A silver sphere appears at the input outlet and rolls along the authored path.
- Fan-out carries one sphere to the exact junction hub, then emits one per dependent.
- An event absorbs the sphere at its inlet, pulses during illustrative processing,
  and emits a sphere at its outlet. Motion never invents a wire through node text.
- At an ALL join, early arrivals wait at the visible hub. The counter reads
  `1 / 2 · waiting`, then `2 / 2 · merge`. Only then does one sphere continue.
- Validation precedes the outcome. A target outcome stays conditional; missing
  testimony receives an amber emphasis and remains `GAP / REQUIRED`.

Provider bindings, authority links, dependencies and evidence attachments do not
carry execution spheres. They remain visible support relationships. A decision
plays only the alternative selected by its existing animation contract. The
capability overview animates seven independent scenario paths; it invents no
sequence between them.

## Geometry and timing

The browser takes the original edge's `d` attribute verbatim. When a source or
target is a line-based junction, it adds the exact compiled arm between the
endpoint and `layout.junctionGlyphs[id].hub`. Thus the sphere crosses the glyph
itself, with no jump between an arm tip and its connecting curve.

Let `L` be the route's SVG arc length, `v = 260` SVG units per second, and `t0`
the node's release time. The sphere position is:

```text
s(t) = clamp(v × (t − t0), 0, L)
position(t) = SVGPath.getPointAtLength(s(t))
rotation(t) = s(t) / effectiveRadius
```

This uses distance along the rendered curve, not the Bézier parameter, so bends
do not change the rolling speed. The metallic lighting remains fixed while the
surface bands rotate. A short silver trail uses the same path geometry. The
sphere maintains a minimum readable screen size within a bounded scale factor;
rotation uses that effective radius.

Node dwell times and a 0.65-second offset between sibling probe presentations
make cause, effect and the wait visible. These are declared presentation choices,
not observations of provider latency. The plan labels its timing
`ILLUSTRATIVE_NOT_TELEMETRY`. The target reference takes about 10.3 seconds at 1×.

The scheduler computes downstream release from required arrivals. `all` waits
for every input, `any` for the first, and `quorum` for its declared threshold.
Incomplete fan-out, an unsatisfied ALL join, multiple chosen decision branches,
an undeclared merge, invalid path lengths, cycles, or attempted GAP execution
stop scheduling. Retry loops require a future explicit iteration contract; the
player refuses to infer iteration counts.

## Controls and preservation

**Play flow**, pause/resume, restart/replay, a seek bar and 0.5×–2× speed are
available on each circuit. Base/Material switching retains the exact flow time,
join state and playback rate. Geometry is shared at every zoom. Manual phase
buttons remain available for static inspection and clear the flow overlay.

Playback is opt-in. Reduced-motion preference makes Play advance to the next
event boundary without continuous motion. Node inspection pauses playback;
changing circuits cancels it; hiding or leaving the page stops the frame loop.
Seeking reconstructs the state deterministically, including backward seeks.

All added paths, spheres, gradients and counters live in one
`data-flow-overlay` group, hidden from assistive technology and pointer input.
The original vectors, labels, links and evidence attributes stay intact. Runtime
CSS provides node emphasis; static SVG exports remain the original artifacts.
The existing MP4 remains a separate rendered composition; this silver-ball
edition is the interactive browser player.

## Verification

```powershell
.\.venv\Scripts\python.exe scripts/build_capability_pages.py
node --test scripts/circuit-flow.test.cjs
.\.venv\Scripts\python.exe -m unittest discover -s scripts -p 'test_*.py' -v
```

Node.js 20+ is needed only for the JavaScript tests. Python builds the pages;
the browser plays them without Node.js. The repository suite invokes the same
JavaScript scheduler tests, including skewed arrivals, threshold policies,
single-branch selection, source preservation, and refusal cases.
