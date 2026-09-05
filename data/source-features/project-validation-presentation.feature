@capability:project-validation-presentation
@root-scenario:project-validation-presentation
Feature: Project validation presentation

  # Original hand-authored source references (migration oracles only):
  # scenario-driven-architecture/languages/csharp/src/ScenarioKernel.UiAuthority/ConsumerUiApplication.cs :: UiValidationRule
  # scenario-driven-architecture/languages/csharp/src/ScenarioKernel.UiAuthority/UiOperationExecutor.cs :: UiOperationExecutor.ExecuteCapability

  A declared validation rule must preserve its state reference, rule identity,
  parameters, message, evaluation phase, blocking disposition, feedback target,
  and lineage. Projection must not embed validation meaning in a native control.

  @scenario:project-validation-presentation
  @input:validation-presentation-facts
  @input-contract:project-validation-presentation-input.v1
  @event:validation-presentation-projection-requested
  @event-authority:validation-presentation-projection.v1
  @outcome:validation-presentation-projection-known
  @outcome-contract:validation-presentation-projection-evidence.v1
  @outcome-terminal
  Scenario: Preserve validation semantics and feedback obligations
    Given admitted validation facts and their state and feedback references
    When validation presentation is projected
    Then rule, parameters, phase, blocking disposition, message, target, and lineage are preserved without selecting a language validator or native error surface
