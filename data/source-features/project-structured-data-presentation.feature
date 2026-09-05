@capability:project-structured-data-presentation
@root-scenario:project-structured-data-presentation
Feature: Project structured data presentation

  # Original hand-authored source references (migration oracles only):
  # scenario-driven-architecture/tools/src/consumer-projection/providers/csharp/consumer-application-provider.ts :: renderSemanticItem structured-feedback branch
  # scenario-driven-architecture/languages/csharp/src/ScenarioKernel.Wpf/AuthorityStructuredSurface.cs :: AuthorityStructuredSurface.Render

  Structured data presentation must be driven by declared semantic groups,
  ordered fields, labels, value paths, emphasis, relationships, empty
  disposition, and accessibility facts rather than by inspecting object shape or
  applying target-owned formatting conventions.

  @scenario:project-structured-data-presentation
  @input:structured-data-presentation-facts
  @input-contract:project-structured-data-presentation-input.v1
  @event:structured-data-presentation-projection-requested
  @event-authority:structured-data-presentation-projection.v1
  @outcome:structured-data-presentation-projection-known
  @outcome-contract:structured-data-presentation-projection-evidence.v1
  @outcome-terminal
  Scenario: Preserve declared structured-data meaning for projection
    Given admitted structured-data groups, fields, relationships, empty disposition, and accessibility obligations
    When structured data presentation is projected
    Then grouping, order, labels, paths, emphasis, relationships, empty disposition, accessibility, and lineage are preserved without inferring meaning from data keys
