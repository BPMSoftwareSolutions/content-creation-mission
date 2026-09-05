@capability:govern-strategic-decision
@root-scenario:govern-strategic-decision
Feature: Record one separately authorized strategic decision

  Evidence informs. Interpretation evaluates. Accountable governance decides.

  This capability records a decision selected by an admitted governance
  authorization. It never infers a decision from an interpretation. It binds
  the exact interpretation, authorization, rationale, effective period,
  review date, and predecessor without mutating evidence or history.
  Conformance fixtures use authorization scope CONFORMANCE_FIXTURE and do not
  constitute real organizational decisions.

  @scenario:govern-strategic-decision
  @input:strategic-decision-record
  @input-contract:strategic-decision-record.v1
  @event:strategic-decision-recording-requested
  @event-authority:govern-strategic-decision.v1
  @outcome:strategic-decision-record
  @outcome-contract:strategic-decision-record.v1
  @outcome-terminal
  Scenario: Record one separately authorized strategic decision
    Given one admitted interpretation, decision authority, and governance authorization
    When the authorized strategic decision is recorded
    Then the governance-selected disposition is bound with rationale, review, lineage, and one receipt without mutating evidence or history

  @scenario:admit-strategic-decision-authorization
  @input:strategic-decision-record
  @input-contract:strategic-decision-record.v1
  @event:strategic-decision-authorization-admission-requested
  @event-authority:admit-strategic-decision-authorization.v1
  @outcome:strategic-decision-record
  @outcome-contract:strategic-decision-record.v1
  @outcome-terminal
  Scenario: Admit the interpretation and governance authorization
    Given one interpretation reference, authority, requested decision, and governance authorization
    When decision recording admission is evaluated
    Then interpretation, strategic identity, accountable body, authorized choice, time, and no-automation laws are reported

  @scenario:bind-strategic-decision-lineage
  @input:strategic-decision-record
  @input-contract:strategic-decision-record.v1
  @event:strategic-decision-lineage-requested
  @event-authority:bind-strategic-decision-lineage.v1
  @outcome:strategic-decision-record
  @outcome-contract:strategic-decision-record.v1
  @outcome-terminal
  Scenario: Bind immutable decision lineage
    Given one current decision and an optional predecessor receipt
    When strategic decision lineage is bound
    Then the predecessor is retained, historical mutation remains prohibited, and strategy change requires re-evaluation

  @scenario:bind-strategic-decision-receipt
  @input:strategic-decision-record
  @input-contract:strategic-decision-record.v1
  @event:strategic-decision-receipt-requested
  @event-authority:bind-strategic-decision-receipt.v1
  @outcome:strategic-decision-record
  @outcome-contract:strategic-decision-record.v1
  @outcome-terminal
  Scenario: Bind one strategic decision receipt
    Given the exact authority, interpretation, authorization, selected decision, rationale, time, review, and lineage
    When the strategic decision receipt is bound
    Then equivalent governed inputs reproduce one receipt even when recording is held

