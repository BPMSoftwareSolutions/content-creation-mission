@capability:project-accessibility-binding
@root-scenario:project-accessibility-binding
Feature: Project accessibility binding

  # Original hand-authored source references (migration oracles only):
  # scenario-driven-architecture/tools/src/consumer-projection/providers/csharp/consumer-application-provider.ts :: accessibilityName and renderSemanticItem
  # scenario-driven-architecture/languages/csharp/src/ScenarioKernel.Wpf/V3PlanEmbodiment.cs :: V3PlanEmbodiment.Materialize.Element

  Accessibility obligations are semantic requirements for names,
  descriptions, roles, operability, relationships, announcements, focus order,
  and state exposure. Projection must preserve each obligation and its subject
  without selecting or inventing a target accessibility API.

  @scenario:project-accessibility-binding
  @input:accessibility-binding-facts
  @input-contract:project-accessibility-binding-input.v1
  @event:accessibility-binding-projection-requested
  @event-authority:accessibility-binding-projection.v1
  @outcome:accessibility-binding-projection-known
  @outcome-contract:accessibility-binding-projection-evidence.v1
  @outcome-terminal
  Scenario: Preserve accessibility obligations for projection
    Given admitted accessibility obligations and their semantic subjects
    When accessibility binding is projected
    Then obligation kind, subject, value source, priority, relationships, required observation, and lineage are preserved without a target accessibility decision
