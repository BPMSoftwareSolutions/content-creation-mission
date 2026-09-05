@capability:project-feedback-presentation
@root-scenario:project-feedback-presentation
Feature: Project semantic feedback

  # Original hand-authored source references (migration oracles only):
  # scenario-driven-architecture/tools/src/consumer-projection/providers/csharp/consumer-application-provider.ts :: renderSemanticItem feedback branch
  # scenario-driven-architecture/languages/csharp/src/ScenarioKernel.UiAuthority/ConsumerUiApplication.cs :: UiFeedback
  # scenario-driven-architecture/languages/csharp/src/ScenarioKernel.UiAuthority/UiStateStore.cs :: UiStateStore feedback state

  Feedback must retain its semantic intent, presentation intent, state source,
  label, importance, accessibility announcement, visibility conditions, and
  lineage without selecting a native status, error, result, or document surface.

  @scenario:project-feedback-presentation
  @input:feedback-presentation-facts
  @input-contract:project-feedback-presentation-input.v1
  @event:feedback-presentation-projection-requested
  @event-authority:feedback-presentation-projection.v1
  @outcome:feedback-presentation-projection-known
  @outcome-contract:feedback-presentation-projection-evidence.v1
  @outcome-terminal
  Scenario: Preserve feedback meaning for projection
    Given one admitted feedback declaration and its state and accessibility references
    When semantic feedback is projected
    Then intent, state, copy, importance, visibility, announcement, and lineage are preserved without a native feedback implementation
