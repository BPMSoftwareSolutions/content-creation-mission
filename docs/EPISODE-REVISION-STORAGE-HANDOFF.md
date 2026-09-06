# Episode revision storage handoff

The user requires production content to move into a database and explicitly chose
**a JSON file for now**. `data/content-production.json` is the current production
content store. `data/production-profile.json` holds provider, voice, visual,
caption and mastering settings. `scripts/production_store.py` supplies the JSON
adapter and stable revision lookup; the renderer consumes records from it.

The two Python files started for this revision were removed before rendering.
Their editorial work was imported into the content store: two unreviewed drafts,
19 scenes, narration, visual states, direction, asset references and audience
hypotheses. The temporary import file and importer were removed after import;
current authoring belongs in the content store. The production schema is
`schemas/content-production.schema.json`; capability claim authority remains with
the existing source contracts and frozen evidence.

Production loads a specific revision through the store adapter.
Episode identities, ordered scenes, copy, claim/evidence references, direction,
asset bindings, provider/voice choices, section compositions, timing instructions,
review status and publication destinations belong in versioned records. Shared
rendering, alignment and verification code consumes those records. It must not
contain branches naming particular episodes or embedded lesson narratives.
Generated media and render receipts reference the exact input revision and asset
digests. A changed record invalidates the relevant rendered/reviewed projection.

The prior published films and landing pages remain unchanged. The user selected
review before publication. Generation and rendering write versioned local artifacts
and bind them to input records; they do not approve or publish the content.
Narration is reused only when script, provider request, model and file hash match.

Build using `.venv/Scripts/python scripts/build_production.py speech --store
data/content-production.json`, followed by the same command with `render`.
Select one revision with `--revision <revisionId>`. There are no episode-specific
branches in the shared rendering or captioning code.

The original critique task remains open: complete the revised films and companion
materials through that data model, repair caption segmentation and final encoded
audio headroom, inspect small-screen outputs, and present the revisions for review.
Continuous human listening and unfamiliar-viewer assessment remain pending.

## Revision 03 section direction

The current revisions use `section-visual-direction.json`,
`section-compositions.json`, `section-production-profile.json` and
`section-assets-review.json` under `data/`. These are the authoring records for
19 distinct subsection designs and their material asset acceptance. Revision 02
records are preserved in `archivedRevisions`. Reusing narration is intentional;
no new speech generation was needed for the visual rebuild.

The current renderer requires an explicit composition for every subsection, uses
reviewed Nano Banana material as the camera layer and keeps exact SVG text and
relationships stationary. It exports the clean SVG separately. Missing direction
or stale image acceptance stops rendering. Python supplies mechanics only.
