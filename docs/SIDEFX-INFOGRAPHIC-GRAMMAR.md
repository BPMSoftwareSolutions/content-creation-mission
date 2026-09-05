# SideFX Infographic Grammar v1

This is the working specification for the [original brief](contract-driven%20infographic%20grammar.md).
Its machine-readable vocabulary is `declarations/infographic-grammar.v1.json`.
The projection contract is `schemas/infographic-projection.schema.json`.

**A shape has one meaning at every altitude. Evidence status never changes that meaning.**

## Primitive vocabulary

| Family | Shape | Color family | Meaning |
| --- | --- | --- | --- |
| Input | Rounded rectangle | Cool blue | Admitted incoming state or product, within the labeled scope |
| Event | Beveled rectangle | Electric cyan | A responsibility is exercised |
| Outcome | Capsule | Green / teal | Resulting product, experience, or disposition |
| Provider port | Open socket | Deep blue | A required responsibility boundary |
| Provider | Tabbed tile | Indigo | A fulfiller; attached to its port |
| Validation | Shield with check motif | Cyan-green | Named checks; the motif alone never means passed |
| Evidence | Stacked documents | White / cyan | Declaration, expectation, observed receipt, or required testimony |
| Human approval | Person inside a gate | Gold | Separate human decision authority |
| Policy / authority | Frame with a top control band | White / gold | Governing semantic authority |
| Branch | Fork junction | Neutral cyan | One guarded alternative |
| Fan-out | Radial hub | Neutral cyan | Every declared dependent receives the product |
| Convergence | Merge junction | Neutral cyan | Join under an explicit all / any / quorum policy |
| Decision / selection | Diamond | Neutral cyan | Compare alternatives and select one |
| Termination | Solid end-cap | Neutral white | No onward execution |
| Rejection / hold | Barred octagon | Amber / red | Requested effect stops; retain exact disposition and reason |

Branch, fan-out, and convergence are not interchangeable decorations. A branch
has one incoming route, guarded alternatives, and a total otherwise path. Fan-out
has one incoming route and several outgoing dependents; it does not silently claim
concurrent execution. Convergence has several incoming routes, one continuation,
and a declared join policy. A retry has a return arrow, attempt bound, exit
condition, and stop target. An unmarked line crossing is not a junction.

## Connectors are contracts

| Connector | Required meaning |
| --- | --- |
| Single arrow | Intra-capability transition |
| Double-tip arrow | Outcome → input product transfer across capability boundaries |
| Socket line | Provider → provider port; no execution implied |
| Dotted line, no arrow | Evidence supports a claim or is required to close it |
| Gold line, no arrow | Authority governs an event or decision |
| Dashed open-tip line | Declared dependency, not inferred execution or data flow |
| Return arrow | Bounded retry with an exit and terminal stop target |

A cross-capability product transfer names its product contract. The source must
be an outcome, the destination an input, and both must bind that same contract.
A required format change becomes an explicit transformation with its own input
and outcome. Similar names, shared providers, file order, and dependency lists
never establish a data-flow edge.

## Two independent visual channels

The node's family color and shape remain stable. A second channel carries the
evidence mode through an explicit colored status label. Components have no extra
enclosing boxes; only their defining primitive geometry is drawn:

- **CURRENT / DECLARED:** solid border, exact source reference. Stored expressions
  and fixture expectations remain declarations.
- **OBSERVED / RECEIPT:** solid border plus explicit observed label and an exact
  receipt. The claim cannot exceed what that receipt establishes.
- **TARGET / INTENDED:** violet TARGET label. The primitive keeps its family color;
  a target provider is still an indigo tabbed tile, without an enclosing rectangle.
- **GAP / REQUIRED:** amber GAP label and interrupted supporting connector, with
  a missing obligation and closure criterion. Required testimony is never drawn
  as an existing successful receipt.
- **HUMAN / ILLUSTRATIVE:** a labeled narrative anchor; not implementation proof.

Provider binding (`bound`, `candidate`, `open`) is separate from operating state
(`active`, `candidate`, `simulated`, `degraded`, `isolated`, `unknown`). A declared
binding does not establish live activity. Unknown stays visible.

## Reading and scale

Input → event → outcome reads left to right. The human experience sits above it;
mechanics occupy the middle; providers, evidence, states, and a legend sit below.
Long graphs use labeled rows or explicit boundaries. A presentation never hides
an alternative solely to make the diagram look simpler.

At scenario altitude, show the actual decision and responsible mechanics. At
capability altitude, enumerate every scenario and disclose the shared providers
and declared invocation relationships. At estate altitude, keep capability
boundaries and typed product ports visible. Domain clusters are labeled editorial
groupings. A curated slice must name its coverage; it must not imply a complete
estate map.

Zoom is semantic aggregation, not merely shrinking the drawing. An aggregation
retains every member ID, source reference, and evidence-mode count. Mixed evidence
cannot become a single proven badge. Expansion must recover the same members.
Responsive pages preserve diagram geometry and offer fit and full-size viewing;
they never reconnect a circuit to fit a screen.

## One contract, static and moving

An Infographic Projection Contract binds capabilities, scenarios, typed nodes,
junctions, edges, providers, source evidence, human anchors, three visual layers,
five animation beats, and explicit aggregations. The compiled artifact adds
layout coordinates. Layout is replaceable; meaning and identity are not.

The animation phases are **Establish → Activate → Execute → Resolve → Prove**.
They reveal and emphasize the same graph. Motion selects one guarded route;
fan-out may illuminate all dependents. Convergence does not resolve early.
Highlighting a required receipt never creates observed evidence. Interactive
controls expose each frame, stop after Prove, and honor reduced motion.

Every export carries a compact legend and evidence-mode label. SVG retains text,
accessible titles and stable IDs; the inspector links to source detail. The reference compiler
also exports five SVG frame states and their motion manifest. Generated bitmap
art may surround the graph, but must not invent its shapes, edges, or labels.

## Rejection rules

Compilation fails on unknown types, duplicate IDs, missing endpoints or source
bytes, stale source digests, absent claim support, unbound providers, incomplete
scenario membership, invalid junction cardinality, unbounded retries, hidden
cross-capability transitions, incompatible product ports, mixed reality on an
execution edge, and animation references outside the contract. Geometry must fit
the export canvas. Negative conformance fixtures exercise these rules.

These gates check structural truth and provenance. They do not substitute for
editorial review of whether a particular source actually supports a sentence.
The rule from `EVIDENCE-AND-INTENDED-DESIGN.md` remains in force at every altitude.

The [reference studio](../samples/infographic-grammar/index.html) contains the
symbol atlas, seven connector families, four views, source and topology
inspection, collapse/expand membership, five phase controls, exports, and a
Manim certification specimen. See the [compiler guide](INFOGRAPHIC-COMPILER.md)
for rebuild commands, library roles, tested invariants, and precise coverage.
