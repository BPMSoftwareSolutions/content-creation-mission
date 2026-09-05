@capability:prove-canonical-blueprint-geometry
@root-scenario:prove-canonical-blueprint-geometry
Feature: Prove canonical blueprint geometry

  The canonical blueprint is a typed semantic graph. Branching, fan-out,
  convergence, delegation, termination, and monotonic advancement are explicit
  graph semantics, never properties inferred from implementation control flow,
  node adjacency, or projection ordinal.

  This capability proves those obligations by traversal, before projection and
  before review. It is separate from candidate inspection because its
  obligations are graph-wide rather than field-local, and separate from the
  carrier contract because JSON Schema cannot express them at all.

  A counted monotonic summary is the proof surface. The capability does not
  repair geometry, project any view, or admit anything.

  @scenario:prove-canonical-blueprint-geometry
  @input:canonical-blueprint-geometry-proof-request
  @input-contract:canonical-blueprint-geometry-proof-request.v1
  @event:prove-canonical-blueprint-geometry
  @event-authority:prove-canonical-blueprint-geometry.v1
  @outcome:canonical-blueprint-geometry-proof
  @outcome-contract:canonical-blueprint-geometry-proof.v1
  @outcome-terminal
  Scenario: Prove typed geometry and monotonic advancement for one blueprint
    Given one canonical circuit blueprint carrier
    When node kinds, orthogonal edge semantics, branch coverage, fan-out joint requirement, convergence completeness, and monotonic advancement are each proven by traversal
    Then one geometry proof carries the counted monotonic summary and a CONFORMS or exact holding disposition, with no repair applied and no admission claimed

  @scenario:prove-typed-node-coverage
  @input:canonical-blueprint-geometry-proof-request
  @input-contract:canonical-blueprint-geometry-proof-request.v1
  @event:prove-typed-node-coverage
  @event-authority:prove-typed-node-coverage.v1
  @outcome:typed-node-disposition
  @outcome-contract:blueprint-geometry-disposition.v1
  Scenario: Prove every node carries a declared kind consistent with its shape obligations
    Given one carrier whose nodes declare kind and altitude
    When each node kind is checked against the obligations that kind carries
    Then an untyped node is a holding disposition, a junction declaring fewer than two variants is a holding disposition, and a convergence node without a complete required-product set is a holding disposition

  @scenario:prove-orthogonal-edge-semantics
  @input:canonical-blueprint-geometry-proof-request
  @input-contract:canonical-blueprint-geometry-proof-request.v1
  @event:prove-orthogonal-edge-semantics
  @event-authority:prove-orthogonal-edge-semantics.v1
  @outcome:edge-semantics-disposition
  @outcome-contract:blueprint-geometry-disposition.v1
  Scenario: Prove every edge carries one topology and its applicable dimensions
    Given one carrier whose edges declare topology, contract relation, progress, and selecting variant
    When each edge is checked for exactly one topological role and the dimensions applicable to that role
    Then a collapsed dimension, an untyped edge, an executable transition without a progress disposition, and a contract edge without a contract relation are each holding dispositions

  @scenario:prove-branch-and-fan-out-distinction
  @input:canonical-blueprint-geometry-proof-request
  @input-contract:canonical-blueprint-geometry-proof-request.v1
  @event:prove-branch-and-fan-out-distinction
  @event-authority:prove-branch-and-fan-out-distinction.v1
  @outcome:branch-fan-out-disposition
  @outcome-contract:blueprint-geometry-disposition.v1
  Scenario: Prove branch routes, fan-out sets, and convergence sets remain distinct
    Given one carrier declaring branch junctions, fan-out sets, and convergence nodes
    When every declared variant is traced to a route, every fan-out member is checked for joint requirement, and every convergence requirement set is checked for completeness
    Then an unrouted variant, a fan-out member that is not jointly required, and alternative routes into a shared node presented as convergence are each holding dispositions

  @scenario:prove-monotonic-advancement
  @input:canonical-blueprint-geometry-proof-request
  @input-contract:canonical-blueprint-geometry-proof-request.v1
  @event:prove-monotonic-advancement
  @event-authority:prove-monotonic-advancement.v1
  @outcome:monotonic-advancement-disposition
  @outcome-contract:blueprint-geometry-disposition.v1
  Scenario: Prove every forward transition advances and every route terminates
    Given one carrier whose edges declare progress dispositions and bounded returns
    When each forward transition is checked for advancement and each route is traversed to a declared terminal
    Then unexplained state widening, an undeclared back edge, a bounded return without a declared bound, and a route that reaches no declared terminal are each holding dispositions

  @scenario:bind-counted-monotonic-summary
  @input:canonical-blueprint-geometry-proof-request
  @input-contract:canonical-blueprint-geometry-proof-request.v1
  @event:bind-counted-monotonic-summary
  @event-authority:bind-counted-monotonic-summary.v1
  @outcome:canonical-blueprint-geometry-proof
  @outcome-contract:canonical-blueprint-geometry-proof.v1
  Scenario: Bind the counted monotonic summary to the blueprint digest
    Given every geometry disposition produced for one carrier
    When the counted summary is composed and bound to the carrier digest
    Then the summary reports semantic states, executable forward transitions, totals by topology and progress, declared branch, fan-out, and convergence sets, terminal paths, undeclared back edges, and unexplained widening, and reconciles its totals before reporting CONFORMS
