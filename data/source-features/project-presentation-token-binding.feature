@capability:project-presentation-token-binding
@root-scenario:project-presentation-token-binding
Feature: Project presentation token binding

  # Original hand-authored source references (migration oracles only):
  # scenario-driven-architecture/tools/src/consumer-projection/providers/csharp/consumer-application-provider.ts :: renderWpfWindow and realizeScalarPresentationResources
  # scenario-driven-architecture/languages/csharp/src/ScenarioKernel.UiAuthority/ConsumerUiApplication.cs :: PresentationTokens

  Presentation tokens provide declared semantic values for color, spacing,
  typography, shape, density, motion, emphasis, and state distinction.
  Projection must retain token identity, semantic role, value constraints,
  fallback policy, usage subjects, and lineage without embedding target syntax.

  @scenario:project-presentation-token-binding
  @input:presentation-token-binding-facts
  @input-contract:project-presentation-token-binding-input.v1
  @event:presentation-token-binding-projection-requested
  @event-authority:presentation-token-binding-projection.v1
  @outcome:presentation-token-binding-projection-known
  @outcome-contract:presentation-token-binding-projection-evidence.v1
  @outcome-terminal
  Scenario: Preserve semantic presentation tokens for projection
    Given admitted presentation tokens and their semantic usage references
    When presentation token binding is projected
    Then identity, role, value, constraints, fallback, subjects, and lineage are preserved without target styling syntax or invented defaults
