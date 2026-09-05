@capability:project-strategic-evidence-review
@root-scenario:project-strategic-evidence-review
Feature: Project one read-only strategic evidence review

  Market observes. Market intelligence interprets. Strategy governs.

  This capability owns the joining of the two evidence planes. Its
  input is the exact strategic intent and market thesis identities, the
  admitted external market fit record, the admitted internal strategic
  interpretation record, and the review profile. Its outcome is one
  read-only review record. The review preserves both planes
  independently, retains limitations, counterevidence, evidence
  windows, and review due time, and emits no decision: decisionEmitted
  is always false. No composite score exists. An operational choice
  requires separate accountable authorization.

  @scenario:project-strategic-evidence-review
  @input:strategic-review-record
  @input-contract:strategic-review-record.v1
  @event:strategic-evidence-review-projection-requested
  @event-authority:project-strategic-evidence-review.v1
  @outcome:strategic-review-record
  @outcome-contract:strategic-review-record.v1
  @outcome-terminal
  Scenario: Project one read-only strategic evidence review
    Given the exact strategic intent and market thesis identities, one admitted external market fit record, one admitted internal strategic interpretation record, and the review profile
    When the evidence review is projected
    Then the review is REVIEW_ADMITTED or REVIEW_HELD, preserves both planes independently, retains limitations and divergences, and emits no decision

  @scenario:verify-review-identity-binding
  @input:strategic-review-record
  @input-contract:strategic-review-record.v1
  @event:review-identity-binding-verification-requested
  @event-authority:verify-review-identity-binding.v1
  @outcome:strategic-review-record
  @outcome-contract:strategic-review-record.v1
  @outcome-terminal
  Scenario: Verify the review identity binding
    Given one strategic intent identity, one market thesis identity, and one review profile identity
    When identity binding verification is evaluated
    Then every identity matches its admitted authority, reporting STRATEGIC_INTENT_IDENTITY_DIVERGED, MARKET_THESIS_UNADMITTED, or REVIEW_PROFILE_UNADMITTED otherwise

  @scenario:verify-evidence-plane-binding
  @input:strategic-review-record
  @input-contract:strategic-review-record.v1
  @event:evidence-plane-binding-verification-requested
  @event-authority:verify-evidence-plane-binding.v1
  @outcome:strategic-review-record
  @outcome-contract:strategic-review-record.v1
  @outcome-terminal
  Scenario: Verify the external and internal evidence plane bindings
    Given one external market fit record and one internal strategic interpretation record
    When evidence plane binding verification is evaluated
    Then both records carry their receipt digests and dispositions, and competitive differentiation remains NOT_PROVIDED, reporting EXTERNAL_EVIDENCE_UNBOUND, INTERNAL_EVIDENCE_UNBOUND, or DIFFERENTIATION_RECORD_UNBOUND otherwise

  @scenario:verify-review-preservation-law
  @input:strategic-review-record
  @input-contract:strategic-review-record.v1
  @event:review-preservation-law-verification-requested
  @event-authority:verify-review-preservation-law.v1
  @outcome:strategic-review-record
  @outcome-contract:strategic-review-record.v1
  @outcome-terminal
  Scenario: Verify the review preservation and decision prohibition law
    Given one limitations statement, one review due time, and one decision emission claim
    When the preservation law is verified
    Then limitations and review due time are declared, divergences are retained, and any decision emission claim is rejected, reporting REVIEW_LIMITATIONS_ABSENT, REVIEW_DUE_ABSENT, or DECISION_EMISSION_PROHIBITED otherwise

  @scenario:bind-strategic-review-receipt
  @input:strategic-review-record
  @input-contract:strategic-review-record.v1
  @event:strategic-review-receipt-binding-requested
  @event-authority:bind-strategic-review-receipt.v1
  @outcome:strategic-review-record
  @outcome-contract:strategic-review-record.v1
  @outcome-terminal
  Scenario: Bind one strategic review receipt
    Given one review disposition over two evidence plane records
    When the review receipt is bound
    Then the review identity, intent digest, external market fit receipt digest, internal interpretation receipt digest, decision emission flag, and disposition bind into one replayable strategic review receipt
