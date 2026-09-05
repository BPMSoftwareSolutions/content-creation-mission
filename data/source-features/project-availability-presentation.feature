@capability:project-availability-presentation
@root-scenario:project-availability-presentation
Feature: Project semantic availability

  # Original hand-authored source references (migration oracles only):
  # scenario-driven-architecture/languages/csharp/src/ScenarioKernel.UiAuthority/ConsumerUiApplication.cs :: ActionAvailability.Evaluate
  # scenario-driven-architecture/languages/csharp/src/ScenarioKernel.UiAuthority/AuthorityBackedViewModel.cs :: AuthorityBackedViewModel command construction
  # scenario-driven-architecture/languages/csharp/src/ScenarioKernel.UiAuthority/AuthorityCommand.cs :: AuthorityCommand.CanExecute

  Availability is a declared predicate over admitted state, not target-owned
  command logic. Projection must preserve predicate identity, operands,
  comparison semantics, dependent interactions, unavailable disposition, and
  lineage without choosing a native enabled-state mechanism.

  @scenario:project-availability-presentation
  @input:availability-presentation-facts
  @input-contract:project-availability-presentation-input.v1
  @event:availability-presentation-projection-requested
  @event-authority:availability-presentation-projection.v1
  @outcome:availability-presentation-projection-known
  @outcome-contract:availability-presentation-projection-evidence.v1
  @outcome-terminal
  Scenario: Preserve one availability predicate for projection
    Given one admitted availability predicate and its state and interaction references
    When semantic availability is projected
    Then operands, comparison, dependents, unavailable disposition, and lineage are preserved without target-owned predicate logic
