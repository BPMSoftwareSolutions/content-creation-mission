@capability:project-source-selection-presentation
@root-scenario:project-source-selection-presentation
Feature: Project source selection presentation

  # Original hand-authored source references (migration oracles only):
  # scenario-driven-architecture/languages/csharp/src/ScenarioKernel.Wpf/AuthorityFileInput.cs :: AuthorityFileInput.SelectFile
  # scenario-driven-architecture/languages/csharp/src/ScenarioKernel.UiAuthority/UiOperationExecutor.cs :: UiOperationExecutor.ResolveInput

  Source selection presentation declares a source role, accepted media facts,
  multiplicity, state binding, commit event, consent copy, and source-acquisition
  port. Projection must not open, read, decode, upload, or otherwise acquire a
  source inside the presentation capability.

  @scenario:project-source-selection-presentation
  @input:source-selection-presentation-facts
  @input-contract:project-source-selection-presentation-input.v1
  @event:source-selection-presentation-projection-requested
  @event-authority:source-selection-presentation-projection.v1
  @outcome:source-selection-presentation-projection-known
  @outcome-contract:source-selection-presentation-projection-evidence.v1
  @outcome-terminal
  Scenario: Bind source selection intent to an admitted acquisition port
    Given admitted source-selection intent, media constraints, state and event bindings, and a source-acquisition port
    When source selection presentation is projected
    Then role, constraints, multiplicity, state, consent, commit, port, and lineage are preserved without acquiring or interpreting source bytes
