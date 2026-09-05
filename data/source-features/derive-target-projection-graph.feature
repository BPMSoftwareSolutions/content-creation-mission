@capability:derive-target-projection-graph
@root-scenario:derive-target-projection-graph
# Legacy source: scenario-driven-architecture/tools/src/capabilities/structural-model-projection/derive-target-projection-graph/provider.ts
Feature: Derive target projection graph

  A language maintainer needs to inspect exactly how target-specific
  naming, type, default, and file policy were applied to the canonical type
  graph before any code is rendered. The capability applies target
  structural projection policy without changing canonical meaning.

  Every canonical type receives one attributable target decision, and every
  target choice retains its canonical source lineage. The capability does
  not render any file — it only produces the inspectable target decisions
  rendering will use.

  @scenario:derive-target-projection-graph
  @input:canonical-graph-and-profile-facts
  @input-contract:derive-target-projection-graph-input.v1
  @event:target-projection-graph-derivation-requested
  @event-authority:target-projection-graph-derivation.v1
  @outcome:target-projection-graph-known
  @outcome-contract:target-projection-graph-evidence.v1
  @outcome-terminal
  Scenario: Apply target structural projection policy to the canonical type graph
    Given one canonical type graph and one target structural profile
    When target naming, type, default, and file policy are applied without changing canonical meaning
    Then every canonical type has one attributable target decision that retains its canonical source lineage
