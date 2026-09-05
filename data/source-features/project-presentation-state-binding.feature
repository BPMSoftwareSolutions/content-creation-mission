@capability:project-presentation-state-binding
@root-scenario:project-presentation-state-binding
Feature: Project presentation state binding

  # Original hand-authored source references (migration oracles only):
  # scenario-driven-architecture/languages/csharp/src/ScenarioKernel.UiAuthority/ConsumerUiApplication.cs :: UiStateBinding
  # scenario-driven-architecture/languages/csharp/src/ScenarioKernel.UiAuthority/UiStateStore.cs :: UiStateStore
  # scenario-driven-architecture/languages/csharp/src/ScenarioKernel.UiAuthority/AuthorityBackedViewModel.cs :: AuthorityBackedViewModel.StatePropertyChanged

  Presentation state must remain a declared relationship between a semantic
  state identity, its source role, optional value path, initial value, update
  direction, and dependent presentation facts. Projection must not invent an
  observable property, storage object, notification API, or default state.

  @scenario:project-presentation-state-binding
  @input:presentation-state-binding-facts
  @input-contract:project-presentation-state-binding-input.v1
  @event:presentation-state-binding-projection-requested
  @event-authority:presentation-state-binding-projection.v1
  @outcome:presentation-state-binding-projection-known
  @outcome-contract:presentation-state-binding-projection-evidence.v1
  @outcome-terminal
  Scenario: Preserve declared state relationships for projection
    Given admitted state bindings and their semantic consumers
    When presentation state binding is projected
    Then source, path, initial value, direction, dependents, and lineage are preserved without selecting a language state or notification mechanism
