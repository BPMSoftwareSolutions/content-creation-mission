@capability:publish-sidefx-evidence-receipt
@root-scenario:publish-sidefx-evidence-receipt
Feature: Publish one admitted SideFX evidence receipt to the durable store

  An admitted evidence receipt is published to the content-addressed durable
  store by exact digest. Publication verifies the digest before any write,
  republishing the exact bytes is idempotent and reports ALREADY_PRESENT, an
  occupied address with different bytes is REJECTED without overwrite, and
  publication binds terminal publication testimony that never requires its
  own publication. Every scenario admits and emits one shared publication
  record, so the circuit passes the record through unchanged except for the
  evidence fields each scenario is responsible for.

  @scenario:publish-sidefx-evidence-receipt
  @input:sidefx-evidence-receipt-publication-record
  @input-contract:sidefx-evidence-receipt-publication-record.v1
  @event:sidefx-evidence-receipt-publication-requested
  @event-authority:publish-sidefx-evidence-receipt.v1
  @outcome:sidefx-evidence-receipt-publication-record
  @outcome-contract:sidefx-evidence-receipt-publication-record.v1
  @outcome-terminal
  Scenario: Publish one admitted receipt at its exact content address
    Given one admitted receipt document, its exact bytes, and one expected digest
    When the receipt is published through the declared store port under one declared scope
    Then the exact bytes are retained once or matched idempotently with terminal publication testimony, and no admission, grounding, or pointer claim is made

  @scenario:republish-sidefx-evidence-receipt-idempotently
  @input:sidefx-evidence-receipt-publication-record
  @input-contract:sidefx-evidence-receipt-publication-record.v1
  @event:sidefx-evidence-receipt-republication-requested
  @event-authority:republish-sidefx-evidence-receipt.v1
  @outcome:sidefx-evidence-receipt-publication-record
  @outcome-contract:sidefx-evidence-receipt-publication-record.v1
  @outcome-terminal
  Scenario: Report an idempotent exact republish without another write
    Given the same receipt bytes are published again at the same content address
    When publication is evaluated through the declared store port
    Then the disposition is ALREADY_PRESENT and the stored bytes are unchanged

  @scenario:reject-conflicting-sidefx-evidence-receipt-publication
  @input:sidefx-evidence-receipt-publication-record
  @input-contract:sidefx-evidence-receipt-publication-record.v1
  @event:conflicting-sidefx-evidence-receipt-publication-requested
  @event-authority:reject-sidefx-evidence-receipt-publication-conflict.v1
  @outcome:sidefx-evidence-receipt-publication-record
  @outcome-contract:sidefx-evidence-receipt-publication-record.v1
  @outcome-terminal
  Scenario: Refuse an unverified digest or an occupied-address conflict before any write
    Given supplied bytes fail to reproduce the expected digest or the content address is occupied by different bytes
    When publication admission is evaluated
    Then the publication is REJECTED with one named finding and no partial artifact or overwrite occurs

  @scenario:bind-terminal-sidefx-publication-testimony
  @input:sidefx-evidence-receipt-publication-record
  @input-contract:sidefx-evidence-receipt-publication-record.v1
  @event:sidefx-publication-testimony-binding-requested
  @event-authority:bind-sidefx-publication-testimony.v1
  @outcome:sidefx-evidence-receipt-publication-record
  @outcome-contract:sidefx-evidence-receipt-publication-record.v1
  @outcome-terminal
  Scenario: Bind terminal publication testimony outside the receipt digest basis
    Given one successful publication
    When publication testimony is bound through the ledger relation
    Then the testimony is terminal, declares recursivePublicationRequired false, and never enters the semantic receipt digest basis
