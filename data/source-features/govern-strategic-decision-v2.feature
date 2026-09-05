@capability:govern-strategic-decision-v2
@root-scenario:govern-strategic-decision-v2
Feature: Govern one strategic decision over the admitted evidence review

  Market observes. Market intelligence interprets. Strategy governs.

  This capability owns the decision step. Its input is one admitted
  strategic review record, one accountable owner, one governance
  authorization identity, one admitted decision choice, one rationale,
  and the decision authority. Its outcome is DECISION_ADMITTED or
  DECISION_HELD. The choice belongs to governance, never to the fit
  resolver or the review projection. The allowed choices are
  CONTINUE_BOUNDED_VALIDATION, PAUSE_AND_REVIEW_COUNTEREVIDENCE,
  REQUEST_ADDITIONAL_MARKET_EVIDENCE,
  REQUEST_ADDITIONAL_INTERNAL_EVIDENCE, REVISE_STRATEGIC_THESIS, and
  RECORD_NO_ACTION. Historical decisions and evidence remain immutable;
  a successor thesis preserves its predecessor digest.

  @scenario:govern-strategic-decision-v2
  @input:strategic-decision-record-v2
  @input-contract:strategic-decision-record.v2
  @event:strategic-decision-governance-requested
  @event-authority:govern-strategic-decision-v2.v1
  @outcome:strategic-decision-record-v2
  @outcome-contract:strategic-decision-record.v2
  @outcome-terminal
  Scenario: Govern one strategic decision over the admitted evidence review
    Given one admitted strategic review record, one accountable owner, one governance authorization, one admitted choice, one rationale, and the decision authority
    When decision governance is evaluated
    Then the decision is DECISION_ADMITTED or DECISION_HELD with the exact holding finding, and a receipt binds decision identity, review receipt, choice, authorization, and disposition

  @scenario:verify-decision-review-binding
  @input:strategic-decision-record-v2
  @input-contract:strategic-decision-record.v2
  @event:decision-review-binding-verification-requested
  @event-authority:verify-decision-review-binding.v1
  @outcome:strategic-decision-record-v2
  @outcome-contract:strategic-decision-record.v2
  @outcome-terminal
  Scenario: Verify the decision review binding
    Given one strategic review receipt digest and one review disposition
    When review binding verification is evaluated
    Then the review is admitted and its receipt is bound, reporting DECISION_REVIEW_UNADMITTED otherwise

  @scenario:verify-decision-authorization
  @input:strategic-decision-record-v2
  @input-contract:strategic-decision-record.v2
  @event:decision-authorization-verification-requested
  @event-authority:verify-decision-authorization.v1
  @outcome:strategic-decision-record-v2
  @outcome-contract:strategic-decision-record.v2
  @outcome-terminal
  Scenario: Verify the decision authority, owner, and authorization identity
    Given one decision authority identity, one accountable owner, and one governance authorization identity
    When authorization verification is evaluated
    Then the decision authority is the admitted strategic decision authority, the owner is declared, and the authorization identity matches, reporting DECISION_AUTHORITY_UNADMITTED, ACCOUNTABLE_OWNER_ABSENT, or DECISION_AUTHORIZATION_ABSENT otherwise

  @scenario:verify-decision-choice-and-rationale
  @input:strategic-decision-record-v2
  @input-contract:strategic-decision-record.v2
  @event:decision-choice-rationale-verification-requested
  @event-authority:verify-decision-choice-and-rationale.v1
  @outcome:strategic-decision-record-v2
  @outcome-contract:strategic-decision-record.v2
  @outcome-terminal
  Scenario: Verify the decision choice, rationale, and effective period
    Given one admitted decision choice, one rationale, and one effective period
    When choice and rationale verification is evaluated
    Then the choice is one of the admitted choices, the rationale is declared, and the effective period is declared, reporting DECISION_CHOICE_UNADMITTED, DECISION_RATIONALE_ABSENT, or DECISION_PERIOD_ABSENT otherwise

  @scenario:bind-strategic-decision-receipt
  @input:strategic-decision-record-v2
  @input-contract:strategic-decision-record.v2
  @event:strategic-decision-receipt-binding-requested
  @event-authority:bind-strategic-decision-receipt.v1
  @outcome:strategic-decision-record-v2
  @outcome-contract:strategic-decision-record.v2
  @outcome-terminal
  Scenario: Bind one strategic decision receipt
    Given one decision disposition over one admitted review
    When the decision receipt is bound
    Then the decision identity, review receipt digest, choice, authorization identity, and disposition bind into one replayable strategic decision receipt
