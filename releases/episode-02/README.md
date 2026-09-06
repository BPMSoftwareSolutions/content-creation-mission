# Episode 2 — The Task Finished. Did It Help?

This is the public film adaptation of **A-W1 v1 / Consequences**, the first
foundational lesson in the wisdom strategy. It is not evidence that the
three-lesson learning experiment passed. The reserved diagnostic and transfer
bank are not included in the public release.

The final release uses `episode-02-directed.mp4`: three Gemini Nano Banana
human scenes, restrained camera motion, four animated infographic sequences,
fixed canonical SVG text/geometry, two reflection holds, and aligned captions.
The earlier `episode-02.mp4` is the plain teaching workprint. Its YouTube upload
is retained privately and must not be confused with the final film.

Direction carries forward Episode 1's film workflow: input/event/outcome,
continuous cast and room, shot scale and blocking, audience hypotheses,
exact-image visual review, compositing, and separate deterministic graphics.
SCL is not applicable to this ordinary decision lesson: there is no circuit
topology or traversal to represent. No synthetic circuit is invented to use a tool.

## Artifacts

- `film-direction.json`: human direction, source hash, animation rules, audience hypotheses.
- `shot-selection.json`: selected generated assets with hashes and prompts.
- `film-visual-review.json`: eight visual review dimensions and observations.
- `film.receipt.json`: final film, direction, image, motion and review bindings.
- `motion-timeline.json`: fixed panel reveals and camera motion by chapter.
- `plates/` and `film-plates/`: clean deterministic SVGs and compositing assets.
- `captions.srt`, `captions.vtt`, `transcript.txt`: accessible text.
- `narration-review.json`: independent recognition comparison and alignment evidence.
- `release.json`: actual publication state and destinations.

## Reproduction

From the repository root, use the project Python environment:

```powershell
.\.venv\Scripts\python.exe scripts/produce_episode_two.py --execute
.\.venv\Scripts\python.exe scripts/align_episode_two_captions.py
.\.venv\Scripts\python.exe scripts/direct_episode_two.py --execute
.\.venv\Scripts\python.exe scripts/render_episode_two_directed.py --execute
.\.venv\Scripts\python.exe scripts/prepare_episode_two_web.py
```

Speech and generated image requests are cached by exact request and asset hash.
The caption alignment helper additionally uses faster-whisper 1.2.1 / base.en.
If a selected image changes, inspect it and replace the exact-image review before
rendering. Publishing is separate from reproduction. The draft observation bank
continues to have no learner findings.
