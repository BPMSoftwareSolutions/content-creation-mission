# SCL playground

The playground now supports [SCL 0.2 Lite and canonical authoring](SCL-0.2-SPECIFICATION.md), while keeping 0.1 drafts compatible.

Run `.venv\Scripts\python.exe scripts/serve_scl.py --port 8766` from the content lab, then open
[the playground](http://127.0.0.1:8766/samples/scl/index.html#playground).

The editor opens with a compact 0.2 three-node circuit, or restores the last draft saved in
this browser. Change a node's `label` or paste your own SCL. With **Live preview**
on, compilation starts 650 ms after the last edit. The material infographic and
selected rolling-ball trace are generated from that SCL.

- **New draft** loads the small input → event → outcome starter.
- **Starting circuit** offers a decision and parallel probes with ALL convergence.
- **Open .scl** imports a local text file, up to 2 MB.
- **Undo replacement** recovers the text before the last new draft, import or
  example selection. This recovery text is also retained across reloads.
- **Update now** or **Ctrl+Enter** compiles immediately. Turn Live preview off
  when you want to make several changes before compiling.
- **Save SCL** downloads the exact editor text, including comments and incomplete
  work. Browser storage is local convenience; save a file for a portable copy.
- **Export canonical graph** and **Export infographic** become available when the
  latest text compiles. **Play selected flow** animates the routes in `trace`.
- **Reveal a capability** keeps the source-inspection workflow available.

Syntax and contract errors appear below the controls, with repair hints, a source excerpt and Go to line when a source location is known. Edits clear the previous
preview and disable derived exports until the new circuit validates. The editor
never replaces your text with the compiler's normalized output. Requests are
serialized; newer edits replace queued work and invalidate older responses.

The starter's `design` source identifies the local draft-authoring context. It
does not certify the claims in your draft. Draft nodes remain TARGET, GAP or
STAGING under the existing SCL rules. Use the [language specification](SCL-SPECIFICATION.md)
for node membership, routing, source identities, joins and trace requirements.
The preview service parses and renders; it does not execute or admit capabilities.

Authoring templates live under `templates/scl-studio.*` and `templates/scl-live.js`.
Rebuild the served files with `.venv\Scripts\python.exe scripts/build_scl_studio.py`.
The queue regression checks run with `node --test scripts/test_scl_live.cjs`;
the starter's semantics and rendering are covered by `scripts/test_scl.py`.
