@capability:project-flow-composition
@root-scenario:project-flow-composition
Feature: Project flow composition

  # Original hand-authored source references (migration oracles only):
  # scenario-driven-architecture/tools/src/consumer-projection/providers/csharp/consumer-application-provider.ts :: renderWpfWindow
  # scenario-driven-architecture/languages/csharp/src/ScenarioKernel.Wpf/V3PlanEmbodiment.cs :: V3PlanEmbodiment.Materialize.Node

  A portable flow-composition fact retains axis, direction, wrapping, child
  nodes, semantic elements, ordering, visibility, mechanic binding, and source
  lineage without selecting a target container.

  @scenario:project-flow-composition
  @input:flow-composition-projection-facts
  @input-contract:project-flow-composition-input.v1
  @event:flow-composition-projection-requested
  @event-authority:flow-composition-projection.v1
  @outcome:flow-composition-projection-known
  @outcome-contract:flow-composition-projection-evidence.v1
  @outcome-terminal
  Scenario: Preserve flow mechanics for projection
    Given one admitted flow-composition instruction and its resolved capability binding
    When flow composition is projected
    Then axis, direction, wrapping, children, elements, order, visibility, mechanic, and lineage are preserved without a language container decision
