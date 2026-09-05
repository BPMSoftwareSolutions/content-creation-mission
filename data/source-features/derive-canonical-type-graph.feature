@capability:derive-canonical-type-graph
@root-scenario:derive-canonical-type-graph
# Legacy source: scenario-driven-architecture/tools/src/capabilities/structural-model-projection/derive-canonical-type-graph/provider.ts
Feature: Derive canonical type graph

  A projector author needs one target-neutral structural meaning resolved
  from every reachable canonical schema reference before any target-specific
  naming or type policy is applied. The capability resolves every reachable
  schema reference into target-neutral structural meaning.

  Every reachable type and reference is represented or explicitly rejected
  before target policy is considered, and the resulting graph contains no
  target mechanics. The capability does not apply any target-specific
  naming, type, or file policy — it only establishes the one complete
  structural meaning every language projector works from.

  @scenario:derive-canonical-type-graph
  @input:canonical-schema-facts
  @input-contract:derive-canonical-type-graph-input.v1
  @event:canonical-type-graph-derivation-requested
  @event-authority:canonical-type-graph-derivation.v1
  @outcome:canonical-type-graph-known
  @outcome-contract:canonical-type-graph-evidence.v1
  @outcome-terminal
  Scenario: Resolve every reachable schema reference into a target-neutral type graph
    Given one set of canonical schema facts
    When every reachable schema reference is resolved into target-neutral structural meaning
    Then every reachable type and reference is represented or explicitly rejected, and the resulting graph contains no target mechanics
