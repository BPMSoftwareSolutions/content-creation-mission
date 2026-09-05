@capability:project-activation-binding
@root-scenario:project-activation-binding
Feature: Project activation binding

  # Original hand-authored source references (migration oracles only):
  # scenario-driven-architecture/tools/src/consumer-projection/providers/csharp/consumer-application-provider.ts :: renderSemanticItem action branch
  # scenario-driven-architecture/languages/csharp/src/ScenarioKernel.UiAuthority/UiActionDispatcher.cs :: UiActionDispatcher.Dispatch
  # scenario-driven-architecture/languages/csharp/src/ScenarioKernel.UiAuthority/AuthorityCommand.cs :: AuthorityCommand

  A presentation capability needs one portable activation fact that retains the
  declared semantic element, semantic event, trigger, mechanic, availability
  reference, and source lineage without choosing a callback or command API.

  @scenario:project-activation-binding
  @input:activation-binding-projection-facts
  @input-contract:project-activation-binding-input.v1
  @event:activation-binding-projection-requested
  @event-authority:activation-binding-projection.v1
  @outcome:activation-binding-projection-known
  @outcome-contract:activation-binding-projection-evidence.v1
  @outcome-terminal
  Scenario: Preserve activation semantics for projection
    Given one admitted activation instruction and its resolved capability binding
    When activation binding is projected
    Then its element, event, trigger, availability, mechanic, and lineage facts are preserved without a language callback decision
