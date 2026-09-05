@capability:admit-kernel-specification
@root-scenario:admit-kernel-specification
# Legacy source: scenario-driven-architecture/tools/src/capabilities/kernel-implementation-admission/admit-kernel-specification/provider.ts
Feature: Admit kernel specification

  An SDA maintainer needs to know whether the canonical kernel specification
  is itself structurally valid before any implementation is judged against
  it. The capability validates the canonical kernel specification against
  its admitted schema.

  Every specification requirement is either admitted or identified as a
  specific gap; the specification carries one explicit schema-admission
  disposition. The capability does not evaluate any language implementation
  — it only establishes whether the specification being implemented is
  itself sound.

  @scenario:admit-kernel-specification
  @input:kernel-specification-admission-input
  @input-contract:kernel-specification-admission-input.v1
  @event:kernel-specification-admission-requested
  @event-authority:kernel-specification-admission.v1
  @outcome:kernel-specification-admission-known
  @outcome-contract:kernel-specification-admission-evidence.v1
  @outcome-terminal
  Scenario: Validate the canonical kernel specification against its admitted schema
    Given one canonical kernel specification and its admitted schema
    When the canonical kernel specification is validated against its admitted schema
    Then the specification carries one explicit schema-admission disposition naming every admitted or identified requirement, without evaluating any language implementation
