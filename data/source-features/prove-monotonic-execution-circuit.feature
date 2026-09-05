@capability:prove-monotonic-execution-circuit
@root-scenario:evaluate-execution-level-monotonicity
Feature: Prove the execution circuit is monotonic at every semantic altitude

  Fractal Monotonicity Law: every expandable execution unit MUST either
  terminate in its declared outcome or decompose into a bounded, declared
  child circuit whose admitted paths converge through explicit exits to
  that outcome. Monotonic conformance MUST be independently evaluable at
  every semantic altitude and MUST compose upward from child execution
  cells to the root capability.

  This capability consumes the materialized canonical graph — not the
  rendered plan — and evaluates the same question at every altitude:
  scenario, operation, mechanic, provider. Did the unit terminate, narrow
  or advance the admitted state, or explicitly decompose into children
  that collectively do so?

  Two honest tiers. Structural monotonicity is provable from the graph
  itself: every child belongs to a declared parent, every decomposition
  declares entry and exit cells, every exit has an explicit return, every
  branch group is exhaustive and exclusive, every recurrence is explicitly
  bounded, every edge resolves to declared endpoints, every cell is
  reachable from the root, and terminal cells cannot continue. Semantic
  monotonicity — that the resulting state actually narrows or advances the
  obligation — requires declared progression authority and is reported
  SEMANTIC_MONOTONICITY_NOT_DECLARED rather than guessed when absent.

  Findings carry detail only where proof fails. Every scenario admits and
  emits one shared monotonicity record.

  @scenario:evaluate-execution-level-monotonicity
  @input:execution-circuit-monotonicity-record
  @input-contract:execution-circuit-monotonicity-record.v1
  @event:execution-level-monotonicity-evaluation-requested
  @event-authority:evaluate-execution-level-monotonicity.v1
  @outcome:execution-circuit-monotonicity-record
  @outcome-contract:execution-circuit-monotonicity-record.v1
  @outcome-terminal
  Scenario: Evaluate one monotonic disposition per semantic altitude
    Given one materialized canonical graph digest and its declared cells, edges, decompositions, and branch groups
    When every altitude is evaluated against the structural invariant
    Then one level record per altitude carries cells, evaluated, and disposition, and the overall disposition is MONOTONIC_CIRCUIT or NON_MONOTONIC with named findings

  @scenario:prove-decomposition-boundary-closure
  @input:execution-circuit-monotonicity-record
  @input-contract:execution-circuit-monotonicity-record.v1
  @event:decomposition-boundary-closure-proof-requested
  @event-authority:prove-decomposition-boundary-closure.v1
  @outcome:execution-circuit-monotonicity-record
  @outcome-contract:execution-circuit-monotonicity-record.v1
  @outcome-terminal
  Scenario: Prove every decomposition closes back onto its parent
    Given the declared decompositions with parent, entry, and exit cells
    When each decomposition boundary is evaluated
    Then every entry and exit resolves to a declared cell, every exit has an explicit return edge to its parent, and any boundary that fails to close is reported as a named finding

  @scenario:compose-child-dispositions-upward
  @input:execution-circuit-monotonicity-record
  @input-contract:execution-circuit-monotonicity-record.v1
  @event:child-disposition-composition-requested
  @event-authority:compose-child-dispositions-upward.v1
  @outcome:execution-circuit-monotonicity-record
  @outcome-contract:execution-circuit-monotonicity-record.v1
  @outcome-terminal
  Scenario: Compose child dispositions upward to the root
    Given one altitude whose children each declare a monotonic disposition
    When the parent disposition is composed
    Then the parent is MONOTONIC exactly when every child is MONOTONIC and the parent boundary is closed, and evidence contracts upward from mechanic to operation to scenario to capability

  @scenario:report-semantic-monotonicity-not-declared
  @input:execution-circuit-monotonicity-record
  @input-contract:execution-circuit-monotonicity-record.v1
  @event:semantic-monotonicity-evaluation-requested
  @event-authority:report-semantic-monotonicity-tier.v1
  @outcome:execution-circuit-monotonicity-record
  @outcome-contract:execution-circuit-monotonicity-record.v1
  @outcome-terminal
  Scenario: Report the semantic tier honestly
    Given declared progression rules that may be present or absent
    When the semantic tier is evaluated
    Then the record reports STRUCTURALLY_MONOTONIC with SEMANTIC_MONOTONICITY_NOT_DECLARED when no progression authority is declared, and never claims semantic advancement from topology alone

  @scenario:bind-monotonic-circuit-receipt
  @input:execution-circuit-monotonicity-record
  @input-contract:execution-circuit-monotonicity-record.v1
  @event:monotonic-circuit-receipt-binding-requested
  @event-authority:bind-monotonic-circuit-receipt.v1
  @outcome:execution-circuit-monotonicity-record
  @outcome-contract:execution-circuit-monotonicity-record.v1
  @outcome-terminal
  Scenario: Bind a replayable receipt over the proof basis
    Given one completed monotonicity evaluation
    When the receipt is bound
    Then the canonical graph digest, level records, dispositions, and findings bind into one replayable receipt that claims no semantic advancement beyond what is declared
