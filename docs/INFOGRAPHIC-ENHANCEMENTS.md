# Material edition: preserve the SVG, enhance the experience

The [studio](../samples/infographic-grammar/index.html#scenario-target) offers Base
and Enhanced views of the same circuit. The enhanced alphabet, four infographic
projections, five phase frames per projection and a 1080p animation share the
original semantic contracts. No capability fact changes with visual treatment.

## Three layers

1. **Authority:** the existing grammar, projection contracts, SVG contours,
   labels, evidence modes, node IDs, port anchors and routed edge paths.
2. **Material:** fifteen individually generated Gemini Nano Banana plates with
   dark glass, optical edges and machined bevels. Each has its own prompt, guide,
   request digest, image digest and review disposition.
3. **Composition:** Python applies the material through a mask derived from the
   original vector primitive. Original labels and status captions remain on top.

The user-supplied [alphabet](visual-assets/sidefx-visual-alphabet-enhanced.png)
guides material and color. The [capability circuit reference](visual-assets/sidefx-capability-circuit.png)
guides the layered art direction, not the sample's domain, connections, metrics,
deployment state or proof claims. The certification sample retains its actual
target design and missing testimony.

## Generate one component or the alphabet

From the repository root, using the existing Python environment:

```powershell
.\.venv\Scripts\python.exe scripts/generate_component_assets.py --prepare
.\.venv\Scripts\python.exe scripts/generate_component_assets.py --execute --only provider
.\.venv\Scripts\python.exe scripts/generate_component_assets.py --execute
```

Preparation is local and makes no provider calls. Explicit `--execute` uses
`LOC_GEMINI_API_KEY` from the process or Windows environment and sends requests
to Gemini. The key is never written to the manifest or receipts. At most three
independent requests run concurrently. Identical completed requests resume after
image digest verification; uncertain network outcomes stop for review.

The selected model is `gemini-3-pro-image`. The provider's current image API is
documented in [Google's image-generation guide](https://ai.google.dev/gemini-api/docs/image-generation).
This is the user's requested Gemini provider path, not OpenAI image generation.

`declarations/infographic-enhancement.v1.json` contains all fifteen prompts and
guide bindings. `outputs/component-enhancements/` retains the original provider
images and receipts. The generator is deliberately separate from the scenario
image runner: an isolated decorative primitive has no scenario, provider effect,
human story or execution claim to invent. Scenario generation still uses the
existing mechanics and director gates.

## Review and composite

Inspect each generated plate and bind its exact image hash in
`evaluations/component-enhancement-review.json`. Acceptance is **for masked
material use**, not for substituting a model-generated symbol. The compiler
rejects missing review, stale grammar, changed guide bindings and changed images.

```powershell
.\.venv\Scripts\python.exe scripts/enhance_infographics.py
.\.venv\Scripts\python.exe scripts/animate_infographic.py --enhanced
.\.venv\Scripts\python.exe scripts/build_infographic_studio.py
.\.venv\Scripts\python.exe -m unittest discover -s scripts -p 'test_*.py'
```

These commands reuse selected assets and make no provider calls. After changing
the base infographic, rebuild the base first, then run this sequence. Enhanced
outputs are siblings of the originals; base SVGs, PNGs and films are preserved.

## What the mask guarantees

The compositor samples the generated plate as color and surface detail. A
canonical vector rim owns its footprint. Branch, fan-out and convergence retain
the exact original arms; labels have measured exclusion regions; the interior
stays quiet. Original vector icons supply checks, person marks, stop bars and
document lines. Generated interior symbols do not get to replace them.

This distinction matters in the reviewed batch: the convergence plate proposed
an enclosing surface and the termination plate proposed a hollow rim. Those raw
shapes are not approved glyphs. The composition removes the enclosing surface
and retains the original solid termination disk. The reference atlas shows the
composited primitives, never those raw proposals as semantic authority.

Each added layer is tagged `data-enhancement`, is hidden from assistive
technology, ignores pointer input and lives inside its original entity group.
Removing those layers recovers the exact canonicalized XML of the base SVG.
Independent checks measure contact and tangent continuity on the final SVG.
Pixel-mask checks reject material inside the original text exclusion regions.
These are rendering guarantees, not evidence of live capability execution.

The PNG provider output is retained unchanged. Black-matte extraction and masking
produce a local RGBA derivative; provider-native transparency is not claimed.
Shallow material depth is decorative. It is not a new container or authority box.

## Motion and exports

Manim extracts the enhanced entity groups from that same composed SVG. Each
material moves or fades with its owning node; the edge centerlines and arrival
timing remain the original contract projection. Convergence still waits for both
probe arrivals. Required testimony stays GAP / REQUIRED through the final frame.
Browser phase playback is opt-in and honors reduced motion.

- `samples/infographic-grammar/symbol-atlas-enhanced.svg` and `.png`: full alphabet.
- `samples/infographic-grammar/enhancements/`: individual composited symbols.
- Each projection directory: `infographic-enhanced.svg`, `.png`, phase SVGs and
  `enhancement-receipt.json`.
- `scenario-target/circuit-motion-enhanced.mp4`: 1920×1080 material edition.
- `evaluations/infographic-enhancement-report.json`: source recovery, masks and
  exact junction measurements.

An asset's art direction can change independently. Its permitted semantic type,
canonical mask, source binding and review must still agree before it is composed.
