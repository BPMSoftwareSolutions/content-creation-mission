@capability:project-presentation-lifecycle
@root-scenario:project-presentation-lifecycle
Feature: Project presentation lifecycle

  # Original hand-authored source references (migration oracles only):
  # scenario-driven-architecture/languages/csharp/src/ScenarioKernel.UiAuthority/UiOperationExecutor.cs :: UiOperationExecutor.Execute
  # scenario-driven-architecture/languages/csharp/src/ScenarioKernel.UiAuthority/UiStateStore.cs :: UiStateStore
  # scenario-driven-architecture/languages/csharp/src/ScenarioKernel.UiAuthority/AuthorityBackedViewModel.cs :: AuthorityBackedViewModel.StatePropertyChanged

  Presentation lifecycle exposes declared idle, busy, cancelling, completed,
  cancelled, and failed facts and their permitted transitions. Projection must
  preserve lifecycle identities, transition causes, state patches, command
  refresh obligations, and feedback relationships without owning an operation.

  @scenario:project-presentation-lifecycle
  @input:presentation-lifecycle-facts
  @input-contract:project-presentation-lifecycle-input.v1
  @event:presentation-lifecycle-projection-requested
  @event-authority:presentation-lifecycle-projection.v1
  @outcome:presentation-lifecycle-projection-known
  @outcome-contract:presentation-lifecycle-projection-evidence.v1
  @outcome-terminal
  Scenario: Preserve declared lifecycle transitions for projection
    Given an admitted lifecycle graph and its state, operation, availability, and feedback references
    When presentation lifecycle is projected
    Then each state, transition, cause, patch, dependent refresh, and lineage fact is preserved without inventing timing, concurrency, or execution behavior
