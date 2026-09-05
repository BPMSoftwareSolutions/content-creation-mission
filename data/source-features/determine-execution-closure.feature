@capability:determine-execution-closure
@root-scenario:determine-execution-closure
# Legacy source: scenario-driven-architecture/tools/src/capabilities/kernel-implementation-admission/determine-execution-closure/provider.ts
Feature: Determine execution closure

  An SDA maintainer needs to trust that observed execution testimony is
  complete: correctly ordered, gap-free, and lineage-consistent, with an
  unambiguous terminal disposition. The capability evaluates execution
  order, lineage, failure boundary, and terminal disposition from observed
  execution testimony.

  Every observed execution is either gap-free or carries a precise closure
  finding naming what is missing or inconsistent. The capability does not
  admit the implementation — it only establishes whether the testimony
  itself can be trusted.

  @scenario:determine-execution-closure
  @input:execution-closure-input
  @input-contract:execution-closure-input.v1
  @event:execution-closure-evaluation-requested
  @event-authority:execution-closure-evaluation.v1
  @outcome:execution-closure-known
  @outcome-contract:execution-closure-evidence.v1
  @outcome-terminal
  Scenario: Evaluate execution order, lineage, failure boundary, and terminal disposition
    Given one set of observed execution testimony
    When execution order, lineage, failure boundary, and terminal disposition are evaluated
    Then every observed execution is gap-free or carries a precise closure finding, and execution testimony is ordered and lineage-consistent
