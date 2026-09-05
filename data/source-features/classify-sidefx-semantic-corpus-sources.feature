@capability:classify-sidefx-semantic-corpus-sources
@root-scenario:classify-sidefx-semantic-corpus-sources
Feature: Classify the frozen SideFX semantic corpus seed

  The complete 108-unit frozen seed population is one immutable admitted
  evidence resource. This evaluation capability retains its exact file digest,
  records all 106 connector-selected capability members as the intended
  catalog population, and attributes the projected-special and runtime members
  as excluded from canonical capability identity. It performs no ambient
  repository discovery and cannot refresh the frozen population.

  @scenario:classify-sidefx-semantic-corpus-sources
  @input:sidefx-semantic-corpus-source-classification-request
  @input-contract:sidefx-semantic-corpus-source-classification-request.v1
  @event:sidefx-semantic-corpus-source-classification-requested
  @event-authority:classify-sidefx-semantic-corpus-sources.v1
  @outcome:sidefx-semantic-source-manifest
  @outcome-contract:sidefx-semantic-source-manifest.v1
  @outcome-terminal
  Scenario: Close classification over the full frozen evaluation seed
    Given the exact frozen 108-unit seed population bytes and declared counts
    When its single evidence resource and two non-canonical member classes are recorded
    Then one CLOSED manifest preserves the seed identity and enumerates both exclusions without live observation or authority escalation
