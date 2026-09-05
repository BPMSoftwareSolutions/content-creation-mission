@capability:detect-hand-authored-code
@root-scenario:detect-hand-authored-code
Feature: Detect hand-authored code

  A capability steward needs to know when a source artifact contains executable
  mechanics that must be expressed as semantic authority and projected instead.

  The forbidden executable mechanics are branch, iteration,
  exception-handling, throw, object-construction, serialization,
  normalization, validation, fallback, retry, state-mutation, and
  meaning-hidden-in-text.

  Every supplied source artifact is classified independently. A detected
  mechanic carries attributable source evidence; an artifact without a
  detected mechanic is reported without inventing a violation. The capability
  observes and classifies only. It does not repair, move, project, or admit an
  artifact.

  @scenario:detect-hand-authored-code
  @input:source-artifacts-and-forbidden-executable-mechanics
  @input-contract:hand-authored-code-detection-input.v1
  @event:hand-authored-code-detection-requested
  @event-authority:hand-authored-code-detection-request.v1
  @outcome:hand-authored-code-detection-known
  @outcome-contract:hand-authored-code-detection-evidence.v1
  @outcome-terminal
  Scenario: Classify source artifacts by their executable mechanics
    Given source artifacts and the exact forbidden executable mechanics
    When hand-authored code detection is requested
    Then each artifact reports every detected forbidden mechanic with attributable source evidence, artifacts without detected mechanics report no violation, and the aggregate disposition reflects whether any executable mechanic was detected
