@capability:route-aware-consumer-execution-surface
@root-scenario:route-aware-consumer-execution-surface
Feature: Execute one route-governed consumer circuit through the narrow scenario kernel

  A governed consumer capability declares a route graph: scenario
  responsibilities, junctions with declared outcome variants, bounded-return
  recurrence authority, and terminal dispositions. The five-step scenario
  kernel executes one admitted scenario at a time and owns no route meaning.

  Route decision authority is already admitted: the route resolver decides
  which invocations are authorized next from the current route state and the
  last outcome. This capability composes that resolver; it never re-derives
  route semantics internally.

  Route-state progression establishes additional governed truth: executed
  invocation identities, established products, observed outcomes, satisfied
  route obligations, and remaining governed obligations. It never widens
  previously admitted route possibilities. Every selected invocation
  originates from the exact invocation set returned by admitted route
  resolution, and invocation-set execution monotonically reduces the
  unexecuted authorized set until closure. A completed invocation is never
  reselected unless explicit bounded-return authority permits recurrence.
  Scenario-kernel execution establishes results only; it never selects
  subsequent route authority. Bounded returns carry a strictly advanced
  semantic state, even when control revisits an earlier responsibility.
  Canonical route authority is never reconstructed from execution results:
  results update route state, authority determines continuation. Every
  recurrence carries a measurable convergence condition.

  Control may return. Meaning only advances.

  Unauthorized work is never invoked. Closed work is never re-invoked. Every
  recurrence traverses only under its bounded-return authority. The kernel
  never learns about routes, branches, recurrences, or terminals.

  @scenario:route-aware-consumer-execution-surface
  @input:route-governed-execution-request
  @input-contract:route-governed-execution-request.v1
  @event:execute-route-governed-consumer-circuit
  @event-authority:execute-route-governed-consumer-circuit.v1
  @outcome:route-governed-execution-result
  @outcome-contract:route-governed-execution-result.v1
  @outcome-terminal
  Scenario: Execute one route-governed consumer circuit
    Given one declared route authority with junctions, bounded-return recurrence, and terminals, one current route state, and one candidate invocation set
    When the circuit advances one bounded traversal by composing the admitted route resolver and invoking only its authorized set through the unchanged scenario kernel
    Then one route-governed execution result carrying the resolver's exact terminal disposition, pending surface, or rejected surface, established from the resolver disposition alone, is returned without invoking unauthorized work, without re-deriving route semantics, and without broadening the kernel

  @scenario:admit-route-governed-execution-context
  @input:route-governed-execution-request
  @input-contract:route-governed-execution-request.v1
  @event:admit-route-governed-execution-context
  @event-authority:admit-route-governed-execution-context.v1
  @outcome:admitted-route-execution-context
  @outcome-contract:admitted-route-execution-context.v1
  Scenario: Admit the route-governed execution context
    Given one declared route authority carrying junctions with exact declared variants, bounded-return recurrence authority, terminal dispositions, and one current route state
    When the route authority, the current route state, and the candidate invocation set are admitted as canonical source authority
    Then one immutable execution context fixes the route being traversed, or the context is held with exact findings

  @scenario:resolve-selected-invocation-set
  @input:admitted-route-execution-context
  @input-contract:admitted-route-execution-context.v1
  @event:resolve-selected-invocation-set
  @event-authority:resolve-selected-invocation-set.v1
  @outcome:selected-invocation-set
  @outcome-contract:selected-invocation-set.v1
  @outcome-terminal
  Scenario: Compose the admitted route resolver for the selected invocation set
    Given one admitted execution context carrying the current route state and the exact last scenario outcome when a traversal has completed
    When the admitted route resolver is composed and its exact disposition is consumed
    Then the resolver's exact disposition — NEXT_SCENARIO_AUTHORIZED, FAN_OUT_AUTHORIZED, BOUNDED_RETURN_AUTHORIZED, CONVERGENCE_PENDING, TERMINAL_REACHED, or ROUTE_REJECTED — and its exact authorized invocation set are preserved unchanged; no route semantics are re-derived internally and no invocation occurs during resolution

  @scenario:invoke-selected-scenario-set
  @input:selected-invocation-set
  @input-contract:selected-invocation-set.v1
  @event:invoke-selected-scenario-set
  @event-authority:invoke-selected-scenario-set.v1
  @outcome:selected-invocation-results
  @outcome-contract:selected-invocation-results.v1
  Scenario: Invoke the authorized scenario set through the scenario kernel
    Given one selected invocation set preserved from the route resolver disposition
    When every authorized scenario in the set, at the set's declared cardinality, is invoked through the five-step scenario kernel with no ordering imposed between independent members
    Then every kernel invocation reduces the unexecuted authorized set, each executed identity is retained with its result and lineage, no invocation outside the set is ever selected, and one selected-invocation-results carrier closes only when the unexecuted set is empty

  @scenario:resolve-next-route-state
  @input:selected-invocation-results
  @input-contract:selected-invocation-results.v1
  @event:resolve-next-route-state
  @event-authority:resolve-next-route-state.v1
  @outcome:admitted-route-execution-context
  @outcome-contract:admitted-route-execution-context.v1
  @outcome-terminal
  Scenario: Establish the next admitted route execution context and return bounded to the route resolver
    Given the selected invocation results converged from the authorized set and the declared route authority
    When the next admitted route-state snapshot is established from the converged results and the declared route topology
    Then one admitted route execution context establishes additional governed truth — executed invocation identities, established products, observed outcomes, satisfied route obligations, and remaining governed obligations — and never widens previously admitted route possibilities; the circuit returns bounded to the admitted route resolver with that context, and whether the route completes, continues, or holds is decided by the route resolver alone, never by this establishment

  @scenario:establish-route-governed-execution-result
  @input:selected-invocation-set
  @input-contract:selected-invocation-set.v1
  @event:establish-route-governed-execution-result
  @event-authority:establish-route-governed-execution-result.v1
  @outcome:route-governed-execution-result
  @outcome-contract:route-governed-execution-result.v1
  @outcome-terminal
  Scenario: Establish the route-governed execution result for terminal dispositions
    Given one route resolver disposition that terminates, holds, or rejects the route
    When the route-governed execution result is established from the resolver's exact disposition and the held surface
    Then one route-governed execution result carrying the resolver's exact terminal disposition, pending surface, or rejected surface is established for the terminal experience, never inferred from invocation outcomes
