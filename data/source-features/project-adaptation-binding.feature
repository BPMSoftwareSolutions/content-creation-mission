@capability:project-adaptation-binding
@root-scenario:project-adaptation-binding
Feature: Project semantic adaptation

  # Original hand-authored source references (migration oracles only):
  # scenario-driven-architecture/tools/src/consumer-projection/providers/csharp/consumer-application-provider.ts :: renderWpfWindow
  # scenario-driven-architecture/languages/csharp/src/ScenarioKernel.UiAuthority/ConsumerUiApplication.cs :: AdaptationProfile.SelectContext

  Adaptation must preserve declared contexts, predicates, grouping, ordering,
  visibility, composition changes, invariant references, priorities, and
  lineage without measuring a target or choosing a target layout mechanism.

  @scenario:project-adaptation-binding
  @input:adaptation-binding-facts
  @input-contract:project-adaptation-binding-input.v1
  @event:adaptation-binding-projection-requested
  @event-authority:adaptation-binding-projection.v1
  @outcome:adaptation-binding-projection-known
  @outcome-contract:adaptation-binding-projection-evidence.v1
  @outcome-terminal
  Scenario: Preserve declared adaptation rules for projection
    Given admitted adaptation contexts, operations, priorities, and invariants
    When semantic adaptation is projected
    Then predicates, grouping, order, visibility, composition, invariants, priority, and lineage are preserved without a target layout decision
