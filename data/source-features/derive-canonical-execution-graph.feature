@capability:derive-canonical-execution-graph
@root-scenario:derive-canonical-execution-graph
# Legacy source: scenario-driven-architecture/tools/src/capabilities/execution-vector-projection/derive-canonical-execution-graph/provider.ts
Feature: Derive canonical execution graph

  A projector author needs one target-neutral representation of the
  kernel's canonical steps, dependencies, and failure paths before any
  language-specific projection policy is applied. The capability resolves
  canonical steps, dependencies, and failure paths into target-neutral
  execution meaning.

  Every execution step and dependency is represented in the graph before any
  target policy is considered, including every ordered step and failure
  boundary. The capability does not apply any target-specific mechanic — it
  only establishes the one execution meaning every language projector
  shares.

  @scenario:derive-canonical-execution-graph
  @input:execution-vector-facts
  @input-contract:derive-canonical-execution-graph-input.v1
  @event:canonical-execution-graph-derivation-requested
  @event-authority:canonical-execution-graph-derivation.v1
  @outcome:canonical-execution-graph-known
  @outcome-contract:canonical-execution-graph-evidence.v1
  @outcome-terminal
  Scenario: Resolve canonical execution facts into one target-neutral execution graph
    Given one set of canonical execution vector facts
    When canonical steps, dependencies, and failure paths are resolved into target-neutral execution meaning
    Then the graph represents every ordered step, dependency, and failure boundary before any target policy is applied
