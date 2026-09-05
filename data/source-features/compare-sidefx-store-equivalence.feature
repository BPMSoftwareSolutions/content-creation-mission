@capability:compare-sidefx-store-equivalence
@root-scenario:compare-sidefx-store-equivalence
Feature: Compare SideFX store equivalence across providers

  The same pinned snapshot must produce byte-identical semantic results and
  semantic receipts whether the store behind the port is artifact-backed or
  database-backed. Store realization testimony differs by design, is
  retained in full, is bound to the receipt through the ledger REALIZED_BY
  edge, and is compared for integrity — never for equality. Disabling one
  provider must leave deterministic results unchanged. Every scenario
  admits and emits one shared equivalence comparison record.

  @scenario:compare-sidefx-store-equivalence
  @input:sidefx-store-equivalence-comparison-record
  @input-contract:sidefx-store-equivalence-comparison-record.v1
  @event:sidefx-store-equivalence-comparison-requested
  @event-authority:compare-sidefx-store-equivalence.v1
  @outcome:sidefx-store-equivalence-comparison-record
  @outcome-contract:sidefx-store-equivalence-comparison-record.v1
  @outcome-terminal
  Scenario: Require byte-identical semantic results and receipts across providers
    Given the same pinned snapshot and one declared query partition executed against both providers
    When semantic outcomes and semantic receipts are compared
    Then results and receipts are byte-identical and every provider's store realization testimony is retained and integrity-compared

  @scenario:retain-provider-testimony-outside-semantic-basis
  @input:sidefx-store-equivalence-comparison-record
  @input-contract:sidefx-store-equivalence-comparison-record.v1
  @event:sidefx-store-testimony-retention-observed
  @event-authority:retain-sidefx-store-testimony.v1
  @outcome:sidefx-store-equivalence-comparison-record
  @outcome-contract:sidefx-store-equivalence-comparison-record.v1
  @outcome-terminal
  Scenario: Bind provider testimony through the ledger relation without contaminating identity
    Given two provider testimonies for the same semantic receipt
    When equivalence is compared
    Then each testimony is bound through REALIZED_BY edges outside the semantic digest basis and neither provider identity enters the semantic receipt subject

  @scenario:report-unavailable-provider-not-observable
  @input:sidefx-store-equivalence-comparison-record
  @input-contract:sidefx-store-equivalence-comparison-record.v1
  @event:sidefx-store-provider-unavailability-observed
  @event-authority:report-sidefx-store-provider-unavailability.v1
  @outcome:sidefx-store-equivalence-comparison-record
  @outcome-contract:sidefx-store-equivalence-comparison-record.v1
  @outcome-terminal
  Scenario: Report an unavailable provider as not observable without weakening equivalence
    Given a declared provider that cannot be observed during the comparison
    When equivalence is evaluated
    Then the partition is NOT_OBSERVABLE and the other provider's results are never treated as equivalent evidence
