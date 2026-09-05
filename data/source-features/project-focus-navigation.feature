@capability:project-focus-navigation
@root-scenario:project-focus-navigation
Feature: Project focus and navigation semantics

  # Original hand-authored source references (migration oracles only):
  # scenario-driven-architecture/tools/src/consumer-projection/providers/csharp/consumer-application-provider.ts :: renderSemanticItem and renderWpfWindow
  # scenario-driven-architecture/languages/csharp/src/ScenarioKernel.Wpf/V3PlanEmbodiment.cs :: V3PlanEmbodiment.Materialize event bindings

  Focus and navigation must preserve declared entry, sequence, grouping,
  destinations, restoration, activation relationships, visibility constraints,
  and accessibility obligations without selecting a focus manager, route API,
  or native traversal order.

  @scenario:project-focus-navigation
  @input:focus-navigation-facts
  @input-contract:project-focus-navigation-input.v1
  @event:focus-navigation-projection-requested
  @event-authority:focus-navigation-projection.v1
  @outcome:focus-navigation-projection-known
  @outcome-contract:focus-navigation-projection-evidence.v1
  @outcome-terminal
  Scenario: Preserve focus and navigation meaning for projection
    Given admitted focus order, navigation destinations, restoration rules, and accessibility obligations
    When focus and navigation semantics are projected
    Then entry, sequence, groups, destinations, restoration, activation, visibility, obligations, and lineage are preserved without a target traversal decision
