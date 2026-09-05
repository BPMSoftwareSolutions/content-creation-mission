# Infographics inside the episode

Episode 1 uses the reviewed material SVGs and the interactive page's silver-ball
language as full-screen teaching sequences. They are encoded into the film and
travel with its audio, captions and download; the viewer needs no second page.

| Chapter | Film time | Visual role |
| --- | --- | --- |
| Open the Event | 00:54.593–01:18.564 | Inspect current adjudication; briefly isolate the activation and certification status rows. |
| Evidence | 02:26.797–02:48.968 | Follow intended deny and permit probes, wait for both results, match identities and expose required live testimony. |

The human story connects these sequences. The output is 1920×1080 at 24 fps.
Circuit chapters render natively at that resolution; the existing human chapters
are upscaled from 1280×720. The ten chapter WAVs, narration, timeline and captions
retain their existing content. Sentence timing is approximate editorial timing.

## Reusable edit contract

`declarations/episode-01-infographic-edit.json` binds exact source projections,
material receipts, timeline and flow engine. Each chapter declares contiguous
scenes, a viewport crop, visible reality labels, narration cue times and highlights.
No crop changes source geometry or relationships. The status closeup intentionally
isolates two separate source scenarios; it creates no execution path between them.

`scripts/episode_infographics.py` validates each bound circuit through the existing
composition boundary. `scripts/export_episode_flow.cjs` consumes the shared pure
JavaScript scheduler and silver sphere artwork from `templates/circuit-flow.js`.
It does not control a browser or invoke a provider.

For offline geometry, every cubic is sampled at 512 intervals and accumulated into
an arc-length table. Distance is interpolated over that table, including exact
junction arms and hubs. Surface rotation is distance divided by sphere radius.
The planner is the same one used by the page. Editorial cue points retime its
clock monotonically to the narration, preserving branch and arrival order.

The current example travels along its authored ALLOW branch. OPERATOR_REQUIRED is
shown as the alternative and highlighted while explained, not traversed as part
of the same request. Both target probes are required at the ALL join. Support
relationships carry no execution balls. Missing proof keeps its GAP label even
after the illustrative outcome lights up. Timing represents teaching, not measured
latency; the film makes no live execution claim.

## Rebuild and inspect

```powershell
.\.venv\Scripts\python.exe scripts/episode_infographics.py --preview
.\.venv\Scripts\python.exe scripts/render_episode_one.py --render
.\.venv\Scripts\python.exe scripts/build_season_one.py
.\.venv\Scripts\python.exe scripts/compile_content_products.py
```

Preview plates and intermediate media live in the ignored
`outputs/episode-infographic-cache/` directory. A durable contact sheet lives at
`evaluations/episode-01-infographic-preview.jpg`. The renderer fully decodes the
new movie before replacing the delivered files. `infographic-edit.receipt.json`
binds the edit, consumed source hashes, flow plans and final movie. The film
receipt binds that receipt. After a reviewed render, update the capability page's
explicit changed-media hashes and rebuild with `scripts/build_capability_pages.py`.
Do not regenerate source circuits or narration just to refresh a movie binding.

Episode integration checks sample frames from the actual encoded MP4 against the
declared cutaways, verify independent support lines and the delayed ALL join, and
check every receipt input. The general season checks still verify unchanged
narration, chapter continuity and all nine delivered surface hashes.
