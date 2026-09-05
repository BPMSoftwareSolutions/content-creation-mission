@capability:project-semantic-presentation-layer
@root-scenario:project-semantic-presentation-layer
Feature: Project a complete semantic presentation layer

  # Original hand-authored source references (migration oracles only):
  # scenario-driven-architecture/tools/src/consumer-projection/providers/csharp/consumer-application-provider.ts :: CSharpConsumerApplicationProvider.project
  # scenario-driven-architecture/languages/csharp/src/ScenarioKernel.Wpf/V3PlanEmbodiment.cs :: V3PlanEmbodiment.Materialize

  A complete presentation layer must be reproducible from admitted semantic
  presentation authority, a closed embodiment plan, resolved capability
  bindings, a language resolution, and a data-only target profile. The
  projection composes bounded presentation capabilities without reopening
  meaning, embedding executable source in authority, or depending on a legacy
  presentation provider.

  @scenario:project-semantic-presentation-layer
  @input:semantic-presentation-layer-projection-facts
  @input-contract:project-semantic-presentation-layer-input.v1
  @event:semantic-presentation-layer-projection-requested
  @event-authority:semantic-presentation-layer-projection.v1
  @outcome:semantic-presentation-layer-projection-known
  @outcome-contract:semantic-presentation-layer-projection-evidence.v1
  @outcome-terminal
  Scenario: Compose one complete presentation layer from admitted semantics
    Given one closed semantic presentation and every required admitted presentation capability binding
    When the semantic presentation layer is projected for one resolved language and target profile
    Then one lineage-bound disposable native bundle is known with no missing mechanic, invented meaning, executable authority, or legacy-provider dependency
