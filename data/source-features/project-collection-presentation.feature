@capability:project-collection-presentation
@root-scenario:project-collection-presentation
Feature: Project semantic collection presentation

  # Original hand-authored source references (migration oracles only):
  # scenario-driven-architecture/tools/src/consumer-projection/providers/csharp/consumer-application-provider.ts :: renderSemanticItem collection branch
  # scenario-driven-architecture/languages/csharp/src/ScenarioKernel.Wpf/AuthorityCollectionSurface.cs :: AuthorityCollectionSurface.Render
  # scenario-driven-architecture/languages/csharp/src/ScenarioKernel.UiAuthority/UiCollectionProjector.cs :: UiCollectionProjector.Project

  A declared collection must preserve its state source, row identity, ordered
  fields, value paths, labels, empty disposition, presentation intent,
  selection intent, accessibility obligations, and lineage. Projection must not
  infer columns, cards, metrics, lineage, steps, or navigation from data shape.

  @scenario:project-collection-presentation
  @input:collection-presentation-facts
  @input-contract:project-collection-presentation-input.v1
  @event:collection-presentation-projection-requested
  @event-authority:collection-presentation-projection.v1
  @outcome:collection-presentation-projection-known
  @outcome-contract:collection-presentation-projection-evidence.v1
  @outcome-terminal
  Scenario: Preserve declared collection meaning for projection
    Given one admitted semantic collection and its ordered field, state, selection, and accessibility facts
    When semantic collection presentation is projected
    Then rows, fields, paths, order, intent, empty disposition, selection, accessibility, and lineage are preserved without inspecting legacy physical structure
