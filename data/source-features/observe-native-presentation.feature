@capability:observe-native-presentation
@root-scenario:observe-native-presentation
Feature: Observe native presentation testimony

  # Original hand-authored source references (migration oracles only):
  # scenario-driven-architecture/languages/csharp/src/ScenarioKernel.Wpf.Conformance/Program.cs :: NativeWpfUiCollector
  # scenario-driven-architecture/languages/csharp/src/ScenarioKernel.UiAuthority/UiEvidenceObjects.cs :: UiPresentationTestimony and related evidence records

  Native proof must observe only declared requirements and projected lineage:
  realized semantic elements, content, state, interactions, focus,
  accessibility, adaptation, lifecycle, and composition. Observation must not
  infer semantic meaning from native structure or repair a projection.

  @scenario:observe-native-presentation
  @input:native-presentation-observation-facts
  @input-contract:observe-native-presentation-input.v1
  @event:native-presentation-observation-requested
  @event-authority:native-presentation-observation.v1
  @outcome:native-presentation-testimony-known
  @outcome-contract:native-presentation-testimony.v1
  @outcome-terminal
  Scenario: Produce requirement-bound native presentation testimony
    Given an admitted semantic presentation, projected bundle, native observation profile, and required evidence set
    When native presentation is observed
    Then testimony reports each declared requirement as observed, absent, mismatched, or not observable without inferring semantics or changing the projection
