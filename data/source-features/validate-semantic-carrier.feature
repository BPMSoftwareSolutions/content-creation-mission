@capability:validate-semantic-carrier
@root-scenario:validate-carrier-source
Feature: Validate a Scenario Semantic Carrier

  A carrier receives a deterministic conformant or rejected disposition with explicit findings.

  @scenario:validate-carrier-source
  @input:semantic-carrier-source
  @input-contract:semantic-carrier-source.v1
  @event:validate-semantic-carrier
  @event-authority:validate-semantic-carrier.v1
  @outcome:carrier-validation-classified
  @outcome-contract:carrier-validation-result.v1
  Scenario: Validate carrier source
    Given Scenario Semantic Carrier source bytes
    When the carrier is parsed and validated without executing it
    Then the carrier has an exact validation classification

  @scenario:return-conformant-carrier
  @input:conformant-validation-result
  @input-contract:carrier-validation-result.v1
  @event:bind-conformant-receipt
  @event-authority:bind-conformant-receipt.v1
  @outcome:carrier-conformant
  @outcome-contract:carrier-conformance.v1
  @outcome-terminal
  Scenario: Return conformant carrier
    Given validation evidence with no findings
    When the conformant receipt is bound
    Then the CONFORMANT receipt is returned

  @scenario:return-carrier-rejection
  @input:rejected-validation-result
  @input-contract:carrier-validation-result.v1
  @event:bind-rejected-receipt
  @event-authority:bind-rejected-receipt.v1
  @outcome:carrier-rejected
  @outcome-contract:carrier-conformance.v1
  @outcome-terminal
  Scenario: Return carrier rejection
    Given validation evidence with one or more findings
    When the rejected receipt is bound
    Then the CARRIER_NOT_CONFORMANT receipt is returned

