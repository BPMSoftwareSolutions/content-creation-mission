@capability:derive-target-execution-graph
@root-scenario:derive-target-execution-graph
# Legacy source: scenario-driven-architecture/tools/src/capabilities/execution-vector-projection/derive-target-execution-graph/provider.ts
Feature: Derive target execution graph

  A language maintainer needs to inspect exactly how target-specific async,
  cancellation, exception, and delegation mechanics were applied to the
  canonical execution graph before any code is rendered. The capability
  applies target execution mechanics to the canonical graph without
  changing canonical meaning.

  Every canonical execution node receives one attributable target-policy
  disposition, and every target mechanic retains its canonical step
  lineage. The capability does not render any file — it only produces the
  inspectable target execution decisions rendering will use.

  @scenario:derive-target-execution-graph
  @input:canonical-execution-and-profile-facts
  @input-contract:derive-target-execution-graph-input.v1
  @event:target-execution-graph-derivation-requested
  @event-authority:target-execution-graph-derivation.v1
  @outcome:target-execution-graph-known
  @outcome-contract:target-execution-graph-evidence.v1
  @outcome-terminal
  Scenario: Apply target execution mechanics to the canonical graph without changing canonical meaning
    Given one canonical execution graph and one target execution profile
    When target async, cancellation, exception, and delegation mechanics are applied without changing canonical meaning
    Then every canonical execution node has one attributable target-policy disposition that retains its canonical step lineage
