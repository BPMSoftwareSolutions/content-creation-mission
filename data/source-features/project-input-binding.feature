@capability:project-input-binding
@root-scenario:project-input-binding
Feature: Project semantic input binding

  # Original hand-authored source references (migration oracles only):
  # scenario-driven-architecture/tools/src/consumer-projection/providers/csharp/consumer-application-provider.ts :: renderSemanticItem input branch
  # scenario-driven-architecture/languages/csharp/src/ScenarioKernel.Wpf/AuthorityFileInput.cs :: AuthorityFileInput

  A declared input must preserve its input intent, state relationship, label,
  placeholder, accepted value constraints, optional commit event, accessibility
  obligations, and lineage without choosing a native input type or change API.

  @scenario:project-input-binding
  @input:semantic-input-binding-facts
  @input-contract:project-input-binding-input.v1
  @event:semantic-input-binding-projection-requested
  @event-authority:semantic-input-binding-projection.v1
  @outcome:semantic-input-binding-projection-known
  @outcome-contract:semantic-input-binding-projection-evidence.v1
  @outcome-terminal
  Scenario: Preserve declared input semantics for projection
    Given one admitted semantic input and its state and event bindings
    When semantic input binding is projected
    Then its intent, value constraints, state, commit, accessibility, and lineage facts are preserved without choosing a native input implementation
