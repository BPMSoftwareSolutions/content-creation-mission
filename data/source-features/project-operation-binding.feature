@capability:project-operation-binding
@root-scenario:project-operation-binding
Feature: Project declared operation binding

  # Original hand-authored source references (migration oracles only):
  # scenario-driven-architecture/languages/csharp/src/ScenarioKernel.UiAuthority/ConsumerUiApplication.cs :: UiOperation derived records
  # scenario-driven-architecture/languages/csharp/src/ScenarioKernel.UiAuthority/UiOperationExecutor.cs :: UiOperationExecutor.Execute

  Presentation may declare that a semantic event requests an admitted operation
  such as capability execution, query execution, source resolution, fixture
  selection, or cancellation. Projection must bind the request and its arguments
  to an admitted effect port without implementing the effect inside presentation.

  @scenario:project-operation-binding
  @input:declared-operation-binding-facts
  @input-contract:project-operation-binding-input.v1
  @event:declared-operation-binding-projection-requested
  @event-authority:declared-operation-binding-projection.v1
  @outcome:declared-operation-binding-projection-known
  @outcome-contract:declared-operation-binding-projection-evidence.v1
  @outcome-terminal
  Scenario: Bind a semantic event to an admitted operation port
    Given one admitted semantic event, operation declaration, argument bindings, result bindings, and effect-port identity
    When the declared operation binding is projected
    Then request, arguments, results, cancellation relationship, port, and lineage are preserved without performing the effect or inventing an execution path
