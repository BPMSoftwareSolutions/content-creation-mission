# SideFX Circuit Language 0.1

Status: **implemented content-lab candidate specification**. This version is not an admitted SideFX language authority or a runtime. It establishes a repeatable inspection and design boundary. Its source brief is [SideFX Circuit Language](sidefx-circuit-language%20(SCL).md), retained unchanged.

## What works now

An exact frozen capability snapshot can be revealed as SCL, validated, exported as canonical JSON, and projected into a scenario infographic. A draft can be edited as SCL and projected by the same renderer. The renderer, material plates, port geometry and silver-ball scheduler are reused from the episode system.

The estate audit covers **219 capabilities and 823 scenarios**, across **118 v1, 85 v2 and 16 v3** execution plans. The v3 plans retain **4,992 native cells and 5,498 native edges**. Every native record retains its original JSON pointer and verified bytes. No provider expression is executed or reverse engineered into invented graph edges.

This is frozen corpus coverage, not a claim about a newer live estate. The generation digest is in every reveal and the [coverage report](../evaluations/scl-coverage.json). The [render verification](../evaluations/scl-estate-verification.json) records each scenario SVG and native neighborhood checks.

Before this work, four curated infographic contracts were compiled by a generic renderer. The inventory of 219 capabilities was not automatic circuit wiring. Automatic revelation now exists; editorial approval and full native execution animation remain separate gates.

**203 legacy plans do not supply native canonical graphs. Twelve scenario declarations do not have an exact matching plan scenario.** Their feature-backed boundary views remain available with `SCENARIO_PLAN_UNRESOLVED`; no missing mechanic is fabricated. See the [authoring gap register](../evaluations/scl-authoring-gaps.json). A separate [current estate byte check](../evaluations/scl-current-estate.json) verifies all 219 current capsule hashes and confirms that the current manifest matches this frozen generation.

**48 capsules also carry a separate `canonical-circuit-blueprint.v1`.** These are retained as exact blueprint records, including source authority, responsibility/state nodes, topology, semantic progress, observability and projection authorities. They are available in the source inspector. This carrier needs its own qualified visual profile; it is not flattened into the runtime graph. “No native canonical graph” refers specifically to the runtime plan, not the absence of design testimony elsewhere in the capsule.

Three stored blueprint candidates reference undeclared junction identities: `generate-executable-capability-scaffold`, `provision-capability-artifacts`, and `resolve-estate-dependency-closure`. They explicitly retain a review/admission requirement. SCL reports `BLUEPRINT_UNRESOLVED_ENDPOINTS`, preserves their original admission state, and invents no junction to repair the picture. Source retention is not blueprint conformance.

## Authority and representations

```text
Existing capsule testimony ── reveal ──┐
                                      ├─ SCL candidate graph ── named lens ── infographic
Authored SCL ── parse and validate ────┘

SCL candidate ── design testimony ── managed blueprint adapter / review / admission
```

The native canonical graph in a capsule remains its source authority. The local SCL graph is a content-addressed candidate or source projection, never a replacement for that authority. Coordinates, material, camera position, timing and SVG are downstream projections. Changing these cannot change source meaning.

Three surfaces have distinct fidelity:

| Surface | Meaning |
|---|---|
| Scenario lens | Input → event → outcome, with declared identities and contracts. A boundary summary, not a simulation of the native graph. |
| Canonical SCL | Typed nodes, junctions, routes, scopes, sources, meanings, provider bindings, findings and a separately selected illustrative trace. Lossless text/JSON round trip. |
| Expanded native inspection | Exact source records and a navigable native topology neighborhood. Records retain ports, variants, configurations, authorities, recurrence and binding references. |

The brief's Lite conversational syntax, visual editing that changes SCL, C4 projection, and admitted SCL-to-capsule compilation are future profiles. They are not claimed by this implementation.

## Concrete syntax

SCL is UTF-8. Keywords are case sensitive. Comments begin with `//`. Property values use strict JSON; statements end in `;`. Identity strings use JSON escaping. There are no executable expressions, includes, macros, shell escapes or network imports. Strings that look like code remain inert strings.

```ebnf
document     = 'scl', '"0.1"', ';', 'circuit', json-string, '{', item*, '}' ;
item         = property | declaration ;
property     = keyword, json-value, ';' ;
declaration  = type-keyword, [json-string], '{', property*, '}' ;
```

The parser rejects trailing input, duplicate properties, duplicate JSON keys, non-finite numbers, unknown properties and unsupported versions. Model validation supplies the exact allowed properties for each declaration. [JSON Schema](../schemas/sidefx-circuit.v0.1.schema.json) is generated from the same strict models used by the compiler.

Canonical files start like this:

```scl
scl "0.1";
circuit "boundary-certification" {
  title "Prove both sides of the boundary.";
  promise "An operator can trust the exact admitted scope.";
  status "DRAFT";
  // capability, scenario and source declarations establish scope and evidence.
  // Typed input, event, outcome, junction and route declarations follow.
}
```

The excerpt is introductory, not a complete valid circuit. The complete runnable authoring examples are [two-sided certification](../declarations/scl/scenario-target.scl) and [one decision](../declarations/scl/scenario-current.scl).

An input is authored as `input "request" { ... }`; an event as `event "resolve" { ... }`; a route as `route "request-to-resolve" { source "request"; target "resolve"; type "transition"; ... }`. The keywords supply the node type and identities supply stable references. Properties can be reordered without changing meaning; declaration-list order is preserved because source order may matter.

## Semantic core

| Declaration | Responsibility |
|---|---|
| `capability` | Identity, label, domain, scenario membership, coverage and sources. |
| `scenario` | Exact capability owner, input/event/outcome membership and source references. |
| `input`, `event`, `outcome` | The scenario triad. Input/output contracts are distinct from human experience. |
| `meaning` | A node's semantic altitude, parent, responsibility, authority, mechanic profile, experience and variants. |
| `provider-port`, `provider`, `binding` | Required responsibility, candidate or bound fulfiller, and explicitly unknown/declared/observed operating state. |
| `validation`, `human-approval`, `authority`, `evidence` | Validation boundary, human decision, governing authority and evidence object. |
| `branch`, `decision`, `fan-out`, `convergence`, `termination`, `rejection` | Typed control junctions. These are not interchangeable glyphs. |
| `route` | Typed relationship between exact endpoints. |
| `source` | Repository-relative snapshot, SHA-256, encoding, JSON pointer and evidence mode. |
| `record` | Exact native cell, route, operation, mechanic, provider, policy or blueprint data. |
| `finding` | Named unresolved fact with an explicit closure obligation. |

There are four semantic altitudes: scenario, execution, mechanic and provider. A child cannot point upward through containment or belong to a different capability. Containment must be acyclic. Nested mechanics at the same altitude are permitted. Semantic descent is not inferred from screen position.

Mechanics are **identities and versioned profiles**, not a new keyword for each provider operation. `mechanicProfile` identifies the proposed responsibility profile. Imported records retain exact `nativeType`, authority identities and full configurations through verified references. An unknown profile stays inspectable and requires a supported adapter before it may become execution animation or an executable blueprint.

## Route laws

| Draft route family | Required semantics |
|---|---|
| `transition` | Declared progress inside a capability; never evidence of a live effect. |
| `product-transfer` | Outcome to input, with the identical contract identity on both endpoints and the edge. Cross-capability flow requires this family. |
| `provider-binding` | Provider to provider port; cannot substitute for authority or execution flow. |
| `authority` | Starts at an authority node. |
| `evidence-attachment` | Has an evidence endpoint; cannot be traversed as execution. |
| `dependency` | A requirement relation, not an inferred dispatch or product transfer. |
| `retry` | Bounded return: maximum attempts, exit condition, explicit terminal stop and an existing forward path. |

The ordinary flow graph must be acyclic. Only explicit bounded retry edges can return. Terminal and rejection nodes cannot continue. Every outcome must be reachable from an input. Unknown endpoints, mixed reality flows, untyped splits and untyped merges fail validation.

Selection requires one incoming edge, at least two alternatives, a rule, distinct guards and exactly one `otherwise`. Guards are labels/declared conditions, not evaluated programs. A trace may select only one alternative. A fan-out requires all its output branches in a selected trace.

Convergence requires an explicit policy. Let `n` be the number of distinct incoming edges:

- `all`: release requires `n` arrivals.
- `any`: release requires at least one arrival.
- `quorum`: release requires `q` arrivals, with `1 ≤ q ≤ n`.

This validates topology and illustrative trace coverage. It does **not** prove runtime correlation, freshness, cancellation of late arrivals, idempotency or evidence identity. These remain obligations of an admitted execution profile; a silver ball is never their proof.

## Native profile coverage

The adapter recognizes the exact `consumer-execution-embodiment-plan.v1`, `.v2` and `.v3` discriminators. It selects runtime plans through the capsule's exact `planEntryRef`, verifies entry identities and digests, and binds one frozen manifest generation. Multiple target plans require explicit resolution; they are not silently merged.

| Source feature | Implemented projection | Execution animation |
|---|---|---|
| Scenario input/event/outcome | Automatic SideFX scenario infographic | Only an explicitly authored supported trace |
| Legacy invoke-port, invoke-scenario, project-state | Exact operation and mechanic records | Not synthesized from operation list order |
| Native cells and provider slots | Exact records and native neighborhood lens | Requires native motion profile |
| Separate canonical blueprint carrier | Exact complete blueprint record, checked node/edge identities | Requires blueprint visual and motion profiles |
| `sequence`, `selection`, `transition` | Exact native endpoints, kind and selecting variant | Requires native motion profile |
| `return`, `bounded_return`, `altitude_descent` | Exact endpoints, including outcome-to-outcome returns | Requires native motion profile |
| `recurrence`, `cancellation` | Preserved kind, group, authority and source configuration | Requires bounds/correlation/cancellation profile |
| Provider expression operations | Preserved through exact configuration references | Never evaluated by the content lab |
| Unsupported future version/kind | Explicit finding or rejected adaptation | Held |

The native view shows the selected cell, immediate children and neighbors, with a maximum of twelve visible cells. Its receipt lists visible identities and counts omitted cells/edges. Focus another cell to inspect further. A neighborhood is not advertised as the whole graph. All records remain in the exported SCL, regardless of lens.

## Evidence, admission and compatibility

Evidence modes remain distinct: DECLARED, OBSERVED, TARGET, GAP and STAGING. Authored drafts may use only TARGET, GAP or STAGING entities. GAP requires closure and cannot carry execution flow. An active provider requires OBSERVED evidence and a bound slot. An open slot cannot have a fictitious provider.

Hash verification proves exact bytes and provenance references, not the truth of every statement in those bytes. Source revelation is reproduced from the frozen capsule snapshots; scenario narration and native records are not promoted to observed effects. Editorial readiness requires claim review, human experience direction, source scope review and explicit trace selection.

Version 0.1 does not silently upgrade documents. A new keyword, native adapter or execution meaning requires a new supported profile and conformance cases. Unknown fields fail closed. Opaque native records are retained without semantic reclassification. Canonical graph hashes use UTF-8 JSON with sorted object keys, compact separators and preserved arrays; the format is local and versioned, not a claim of RFC 8785 conformance.

Existing episode contracts and films remain unchanged. SCL exports can feed the infographic production stage after review. The existing episode build's exact artifact and receipt bindings still govern inclusion in a film; the workbench does not automatically insert unreviewed drafts.

## Run it

```powershell
# Reveal one capability, or every capability in the frozen corpus.
.venv\Scripts\python.exe scripts/reveal_scl.py interlock-agent-operation
.venv\Scripts\python.exe scripts/reveal_scl.py --all

# Validate authored language; export its canonical candidate.
.venv\Scripts\python.exe scripts/scl.py declarations/scl/scenario-target.scl --output outputs/scl-candidate.json

# Render with the established material grammar.
.venv\Scripts\python.exe scripts/scl_render.py declarations/scl/scenario-target.scl --enhanced --output outputs/scl-preview

# Rebuild and open the editing workbench.
.venv\Scripts\python.exe scripts/build_scl_studio.py
.venv\Scripts\python.exe scripts/serve_scl.py --port 8766
# http://127.0.0.1:8766/samples/scl/index.html

# Reproduce and measure every scenario infographic.
.venv\Scripts\python.exe scripts/verify_scl_estate.py
.venv\Scripts\python.exe -m unittest discover -s scripts -p test_scl.py -v

# Export design testimony for a future governed adapter; does not invoke admission.
.venv\Scripts\python.exe scripts/scl.py declarations/scl/scenario-target.scl --handoff --output outputs/scl-blueprint-testimony.json
```

The preview service accepts bounded JSON requests on loopback, checks Host and Origin, and renders data. It cannot dispatch capabilities or run user-provided code. Generated graphs are not executable code in Agentic Harness; this implementation lives entirely in the separately authorized content lab.

## Engineering runway

The next platform boundary is an **admitted SCL-to-canonical-blueprint adapter**. It must resolve exact current managed contracts; distinguish first admission from revision; bind predecessor identity; resolve contract compatibility and monotonic progress; obtain provider completeness and mechanic feasibility; and preserve review, proof and publication gates. The local handoff is testimony only.

Native execution animation also needs explicit profile laws for recurring iterations, correlation identities, competing selections, cancellation and return boundaries. Those laws must be proved against source topology and trace evidence before native mechanics get animated. Their absence never authorizes replacing a native edge with a visually convenient sequence.
