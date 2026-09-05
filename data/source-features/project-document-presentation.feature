@capability:project-document-presentation
@root-scenario:project-document-presentation
Feature: Project semantic document presentation

  # Original hand-authored source references (migration oracles only):
  # scenario-driven-architecture/tools/src/consumer-projection/providers/csharp/consumer-application-provider.ts :: renderSemanticItem document-feedback branch
  # scenario-driven-architecture/languages/csharp/src/ScenarioKernel.Wpf/AuthorityDocumentSurface.cs :: AuthorityDocumentSurface.Render

  Document presentation must preserve admitted blocks, hierarchy, prose,
  headings, lists, links, emphasis, source lineage, sanitization obligations,
  empty disposition, and accessibility semantics without treating markup as an
  executable presentation template.

  @scenario:project-document-presentation
  @input:document-presentation-facts
  @input-contract:project-document-presentation-input.v1
  @event:document-presentation-projection-requested
  @event-authority:document-presentation-projection.v1
  @outcome:document-presentation-projection-known
  @outcome-contract:document-presentation-projection-evidence.v1
  @outcome-terminal
  Scenario: Preserve admitted document semantics for projection
    Given one admitted semantic document and its sanitization and accessibility obligations
    When semantic document presentation is projected
    Then blocks, hierarchy, content, links, emphasis, empty disposition, obligations, and lineage are preserved without executable markup or target-owned document meaning
