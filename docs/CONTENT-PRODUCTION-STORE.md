# Production content store

The user selected JSON storage now, with database storage later.
`data/content-production.json` holds versioned editorial records; it is the input
to the new review-edition pipeline. Edit content there, not in Python.
`data/section-production-profile.json` holds current shared typography, captions
and mastering limits. `data/production-profile.json` preserves revision 02 settings. `data/production-companions.json`
contains the companion material. Review criteria are records in
`data/production-review-criteria.json`.

`JsonProductionStore` validates the schema, resolves a revision by stable identity,
and computes a digest including its shared profile and companion. A future database
adapter should provide the same record interface. This is a storage boundary, not
a second capability-authority model. Existing claim/evidence authority remains
upstream; instructional and generated visual layers cannot change its meaning.

The workers are shared across revisions. They contain SVG primitives,
provider adapters, captioning and verification mechanics. They contain no episode
scripts, scene arrays, publication destinations or episode-selection branches.
The older released-film scripts remain historical; they are not the input to the
new pipeline. The abandoned Python draft content module was removed.

```powershell
.venv\Scripts\python.exe scripts\verify_production_records.py --store data/content-production.json --output evaluations/production-record-verification.json
.venv\Scripts\python.exe scripts\build_production.py speech --store data/content-production.json
.venv\Scripts\python.exe scripts\build_production.py render --store data/content-production.json
.venv\Scripts\python.exe scripts\build_production.py review --store data/content-production.json
.venv\Scripts\python.exe scripts\test_production_records.py
```

Use `--revision <revisionId>` to select one record. Speech reuses a clip only when
its request, model, script and audio hash still match. Clip caches include the
actual plate image hashes, audio hash, composition filters and settings. Changing
a companion can rebuild its review surface without changing lesson semantics.
Review rejects a film whose input revision or media bytes no longer match.

Outputs under each record's output directory are projections: films, SVGs,
captions, transcripts, companion pages, thumbnails and receipts. Media remain files
with identities/hashes in records; JSON does not embed video bytes. Read-only review
pages are not authoring surfaces, and local notes are not submitted or persisted.

There is deliberately no publishing operation in this worker. The current
release decision is review before publication. Human listening, unfamiliar-viewer
responses and actual thumbnail deployment are distinct checks; an automated
production receipt cannot mark them complete.

## Individually authored section visuals

Current revision 03 records bind `data/section-visual-direction.json` (teaching
purpose, format, art prompt, camera and motion), `data/section-compositions.json`
(explicit geometry and state reveals) and `data/section-assets-review.json`
(observed material review with exact image hashes). Each subsection has its own
composition. Missing direction or geometry fails; there is no reusable card
fallback. The renderer has no episode-specific branches.

Gemini Nano Banana produced 19 current material images. Asset requests and
receipts are beside those images. Nine earlier images containing generated text
or diagrams were rejected and regenerated; superseded files remain historical.
The provider receives unlettered art direction. Canonical meaning, exact strings,
status, geometry and illustrative traversal are independently authored SVG.

The revision input digest includes selected section directions, compositions and
current image hashes. Clip signatures also bind actual overlays, narration and
filters. Material camera motion never moves canonical relationships. Previous
revision 02 records are archived within the content store. Revised films remain
local review artifacts until the user approves publication.

## Publication facts

`data/youtube-publications.json` records the user-authorized September 6, 2026
publication of revision 03, including channel identity, YouTube IDs, public
descriptions, uploaded hashes and observed thumbnail/caption/visibility checks.
These external publication events are separate from the immutable input snapshot
and its pre-publication review decision. Do not re-render approved media merely
to store a YouTube URL. Earlier uploads and deployed landing pages remain intact.
