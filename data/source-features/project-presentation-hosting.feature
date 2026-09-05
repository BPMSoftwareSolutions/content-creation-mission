@capability:project-presentation-hosting
@root-scenario:project-presentation-hosting
Feature: Project presentation hosting

  # Original hand-authored source references (migration oracles only):
  # scenario-driven-architecture/tools/src/consumer-projection/providers/csharp/consumer-application-provider.ts :: renderWpfApp, renderWpfWindow, and renderWpfProject
  # scenario-driven-architecture/languages/csharp/src/ScenarioKernel.UiAuthority/ConsumerUiApplication.cs :: UiView and UiRegion

  A presentation host declares root views, title and identity facts, startup
  view, lifecycle relationships, sizing constraints, resource references,
  accessibility context, and packaging requirements. Projection must not add
  shell content, navigation, chrome, or behavior absent from authority.

  @scenario:project-presentation-hosting
  @input:presentation-hosting-facts
  @input-contract:project-presentation-hosting-input.v1
  @event:presentation-hosting-projection-requested
  @event-authority:presentation-hosting-projection.v1
  @outcome:presentation-hosting-projection-known
  @outcome-contract:presentation-hosting-projection-evidence.v1
  @outcome-terminal
  Scenario: Preserve declared host requirements for projection
    Given admitted host identity, root views, startup, lifecycle, size, resources, accessibility, and packaging requirements
    When presentation hosting is projected
    Then every host fact and lineage reference is preserved without invented shell content or target-owned application behavior
