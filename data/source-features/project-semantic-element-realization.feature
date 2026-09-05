@capability:project-semantic-element-realization
@root-scenario:project-semantic-element-realization
Feature: Project semantic element realization

  # Original hand-authored source references (migration oracles only):
  # scenario-driven-architecture/tools/src/consumer-projection/providers/csharp/consumer-application-provider.ts :: renderSemanticItem
  # scenario-driven-architecture/languages/csharp/src/ScenarioKernel.Wpf/V3PlanEmbodiment.cs :: V3PlanEmbodiment.Materialize.Element

  One declared semantic element must retain its kind, role, content
  indirection, state references, event references, mechanic binding, and source
  lineage before a language or native presentation type is selected.

  @scenario:project-semantic-element-realization
  @input:semantic-element-realization-facts
  @input-contract:project-semantic-element-realization-input.v1
  @event:semantic-element-realization-projection-requested
  @event-authority:semantic-element-realization-projection.v1
  @outcome:semantic-element-realization-projection-known
  @outcome-contract:semantic-element-realization-projection-evidence.v1
  @outcome-terminal
  Scenario: Preserve one semantic element for projection
    Given one admitted semantic element instruction and its resolved capability binding
    When semantic element realization is projected
    Then its kind, role, content, state, event, mechanic, and lineage facts are preserved without a language or native-type decision
