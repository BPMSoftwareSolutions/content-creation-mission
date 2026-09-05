# SideFX Circuit Language 0.2

Status: implemented authoring language in the content lab. SCL 0.2 compiles human
authoring into a versioned, inspectable candidate graph and the existing SideFX
infographic renderer. It is not a capability execution or admission boundary.

The [design notes](SCL-0.2-DESIGN-NOTES.md) are proposals, retained verbatim.
This specification defines the shipped subset precisely. The
[0.1 specification](SCL-SPECIFICATION.md) remains the compatibility reference.

## Start here

Open the [live playground](http://127.0.0.1:8766/samples/scl/index.html#playground)
and choose **0.2 / Simple circuit — start here** or **New draft**. Existing saved
drafts are restored as written; they are not silently migrated.

This is a complete circuit:

```scl
scl 0.2;
capability narration {
  promise "The producer receives narration she can use.";
  scenario produce {
    given script "A script is ready";
    when narrate {
      responsibility "Generate the narration";
    }
    then ready {
      experience "The producer can finish her story";
    }
  }
}
```

Edit the text and pause. The compiler derives scenario membership, the two
transition routes and the selected illustrative trace. It retains responsibility
and experience as canonical meaning records. **Save SCL** preserves your authored
text; canonical JSON, canonical SCL inspection and SVG expose compiled results.

## Two forms, one 0.2 graph

| Form | Use |
|---|---|
| `scl 0.2; capability identity { ... }` | Lite: nested scenarios, sequential progress and structured parallel paths. Scope and design provenance are supplied deterministically. |
| `scl "0.2"; circuit "identity" { ... }` | Canonical authoring: explicit sources, scopes, typed nodes, all existing route families, named traces and inline meaning. |
| `scl "0.1"; circuit "identity" { ... }` | Unchanged 0.1 compatibility. Frozen estate reveals continue to use this representation. |

The canonical carrier is `sidefx-circuit.v0.2` with its own
[JSON Schema](../schemas/sidefx-circuit.v0.2.schema.json). It extends the 0.1 graph
with node/junction `plane`, expanded meaning altitudes, `traces` and
`selectedTrace`. `trace` remains the exact flattened edge selection of the
selected named trace. A mismatch is rejected. No 0.1 defaults or emitted graph
fields are added to an existing 0.1 circuit.

The canonical exports of the certification fixture are available as
[SCL](../samples/scl/certification.v02.canonical.scl) and
[JSON](../samples/scl/certification.v02.canonical.json).

## Lexical rules

SCL is UTF-8 and case sensitive. `//` begins a comment. JSON strings carry prose
and escaping. Bare names such as `scenario`, `TARGET` and `live-probe-port` are
inert strings. Arrays and objects use strict JSON, including quoted string
elements. Bare identities begin with a letter or underscore and may contain
letters, numbers, underscores, dots and hyphens. Quote other identities.

Properties end in a semicolon. Lite node statements may omit the terminator
after a prose shorthand or a closing node block; examples use semicolons for
clarity. Capability/scenario/parallel blocks do not require a trailing semicolon.
Both `scl 0.2;` and `scl "0.2";` are accepted.

Duplicate fields, unknown fields, duplicate IDs, non-finite JSON numbers, trailing
input and unsupported versions are rejected. `__scl.` identities are reserved for
compiler output. There are no executable expressions, imports, macros or includes.

## Lite authoring

A document contains one capability. It requires a `promise` and one or more
scenarios. `label` and `domain` are optional. Scenario labels are optional. Every
scenario must contain an input, an event and an outcome; every outcome must be
reachable. Node identities are unique across the entire circuit.

| Authoring | Canonical meaning |
|---|---|
| `given id "Text";` | Input |
| `when id "Text";` or `when id { responsibility "..."; }` | Event |
| `then id "Text";` or `then id { experience "..."; }` | Outcome |
| `validate id on session, coverage, time, authority;` | Validation, responsibility text and retained field identities in `variants` |
| `deny id expect no-effect;` | Event retaining `deny` and `no-effect` as declared variants |
| `permit id expect declared-effect;` | Event retaining `permit` and `declared-effect` as declared variants |
| `input`, `event`, `outcome`, `validation`, `human-approval` | Explicit node spellings in the scenario sequence |

The sequence of flow declarations is intentional authoring: consecutive flow
items acquire transition routes. Support declarations (`evidence`, `provider-port`,
`provider`, `authority`) do not acquire execution routes just because they appear
next to an event. Labels default from identities; no mechanic is inferred from
the label. `expect` and validation fields are declarations, not executed tests.

Lite generates design-context sources referencing
`declarations/scl/playground-intent.json`. That hashed context identifies the
authoring lane; it does not verify claims written in the draft. Canonical form is
required for explicit source references and product contracts across capabilities.

## Parallel paths and traces

```scl
when both-probes {
  label "Both probes";
  parallel {
    deny unmanaged-probe expect no-effect;
    permit read-only-probe expect declared-effect;
  }
  join both-results all;
}
```

This compiles to a fan-out, two independent paths and an ALL convergence. Omit
`join` to get a stable generated join ID. Put `path { ... }` around multiple
sequential nodes in one branch; nested parallel blocks are supported. Parallel
blocks require at least two nonempty paths and are limited to sixteen nesting
levels in Lite.

Each Lite scenario receives a named `<scenario-id>.flow`. The initial selection
is the first scenario. The playground selects the corresponding trace when the
scenario lens changes. Generated IDs are derived from semantic role and endpoint
identities, not labels or screen coordinates.

Canonical form can explicitly author:

```scl
trace "certification-flow" {
  step "e00";
  parallel {
    path ["e01", "e03"];
    path ["e02", "e04"];
  }
  step "e05";
  step "e06";
}
```

These IDs must already name routes. A nested `path { step ...; parallel ...; }`
is also supported. Named blocks infer scenario ownership from their first route.
`selectedTrace "certification-flow";` selects one when there are several. The
normalized carrier stores `traces` as JSON data; do not mix that property with
named blocks in one document.

The compiler rejects disconnected sequential steps, repeated edges, overlapping
parallel interiors, different fork/join boundaries, omitted branches and
cross-scenario named traces. Structured parallel requires a fan-out and an ALL
convergence. Explicit canonical any/quorum joins and selections remain available
with the existing flat trace form; they are not silently reinterpreted as an ALL
barrier. Named trace syntax is limited to twenty nesting levels.

The existing silver-ball scheduler already derives concurrent flights from
fan-out topology and waits for required arrivals. 0.2 supplies and validates the
structured authoring behind that selection. Flattening a trace for that scheduler
does not mean serial execution. Animation remains illustrative, not runtime timing.

## Meaning and visual plane

Node blocks may directly author `altitude`, `parentId`, `responsibility`,
`authorityId`, `mechanicProfile`, `experience`, `variants` and
`productIsExperience`. These normalize into one `meaning` record. A duplicate
inline and explicit meaning record is rejected. When `detail` is absent it defaults
to responsibility or experience; explicit detail remains distinct and preserved.

Altitudes, in descending order, are:
`strategy → product → capability → scenario → execution → mechanic → provider → physical`.
Containment is acyclic, belongs to one capability and cannot ascend in altitude.
These names extend semantic description, not the native execution renderer.

Planes are `primary`, `support`, `evidence`, `provider` and `observation`. They
answer where a node belongs in this view, independently of its altitude. The
current SVG grammar renders primary in its mechanic band and all other planes in
its support band. The precise plane survives in canonical data and the projection's
`semanticPlanes`; five independent visual bands are not claimed. An explicit
legacy `layer` conflicting with this mapping is rejected.

## Providers and evidence

```scl
provider candidate hook-runtime through live-probe-port;
```

This declares a provider, its port and the candidate binding. A missing port
declaration receives a named open responsibility; it is not proof that a provider
implements the responsibility. `bound` is also allowed but its operating state
remains unknown. A port without a provider becomes an open slot. Link an event
explicitly using `requires-port live-probe-port;`.

`requires evidence probe-testimony;` inside a scenario attaches evidence to its
last outcome. If undeclared, the evidence becomes GAP with a visible unresolved
finding and a closure obligation. To state the obligation precisely, declare:

```scl
evidence probe-testimony {
  basis GAP;
  plane evidence;
  closure "Execute both probes in the same exact session and bind their effects.";
}
```

Node sugar is also available in canonical and Lite blocks:

- On an outcome: `requires-evidence "proof";`
- On evidence: `establishes "outcome-id";`
- On an event: `requires-port "port-id";`

Each also accepts a JSON array of identities. References and endpoint types are
checked; these compile to evidence-attachment or dependency edges. Support edges
never become flow steps. Evidence attached to an outcome produces a persistent
**PROOF NOT ESTABLISHED** banner in the draft preview. Reaching the end of its
target animation does not certify the outcome.

Evidence basis remains DECLARED / OBSERVED / TARGET / GAP / STAGING. Drafts allow
TARGET / GAP / STAGING. CANDIDATE is provider state; BOUND is binding state;
PROVED, REJECTED and SUPERSEDED are not new evidence bases in this release. They
need separate lifecycle or proof contracts rather than an editable claim of truth.

## Debugging

Both language versions now return a structured diagnostic: code, message, repair
hint and a source location when known. Syntax errors identify the parser position;
0.2 contract errors identify the authored declaration. The playground displays a
source excerpt and **Go to line**, which focuses and selects that line. Diagnostics
use UTF-16 offsets for browser selections. Your text is preserved through errors.

The parser reports the first error to avoid cascades from incomplete input; it does
not silently repair or execute anything. Unknown 0.1 semantic locations remain
unlocated rather than inventing an exact position.

## Compatibility and production boundaries

0.1 source graphs retain their exact canonical fields, hashes and render meaning.
The shared SVG grammar, geometry engine, material plates, animation scheduler and
episode film sources are unchanged. The 0.2 renderer removes downstream-only plane
fields when using the legacy projection schema, while retaining them in exported
metadata and the canonical graph.

The larger design notes also propose live target/current/diff lenses, proof-backed
state transitions, editable diagram nodes, richer lifecycle bases and an admitted
SCL-to-capability builder. Those require further contracts and evidence; this
release does not claim them. All existing explicit canonical route families,
bounded retry laws, provider validation and native-record retention remain
available. Native runtime recurrence/cancellation animation is still a separate
profile, as documented in 0.1.

```powershell
.venv\Scripts\python.exe scripts/build_scl_studio.py
.venv\Scripts\python.exe scripts/serve_scl.py --port 8766
.venv\Scripts\python.exe scripts/scl.py declarations/scl/certification.v02.scl --output outputs/scl-02.json
.venv\Scripts\python.exe scripts/scl.py --schema --schema-version 0.2 --output outputs/scl-02-schema.json
.venv\Scripts\python.exe scripts/scl_render.py declarations/scl/certification.v02.scl --enhanced --output outputs/scl-02-preview
```

Conformance tests cover the exact proposed Lite specimen, nested parallelism,
named trace validation, source diagnostics, retained meaning, evidence gaps,
canonical round trips and 0.1 compatibility. The workbench build receipt binds
compiler inputs, examples, templates and generated outputs.

The [upgrade review](../evaluations/scl-v02-review.json) records 118 passing Python
tests, eight passing live-editor/motion tests and unchanged hashes for all 219
existing graphs, 823 scenario SVGs and sixteen native-view receipts.
