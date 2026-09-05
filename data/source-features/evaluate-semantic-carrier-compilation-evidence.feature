@capability:evaluate-semantic-carrier-compilation-evidence
@root-scenario:evaluate-semantic-carrier-compilation
Feature: Adjudicate independently manufactured semantic carrier compilation evidence

  One extracted canonical graph and its independently manufactured proof set are adjudicated without evaluator evidence manufacture; ordinary subjects become review-ready or held, while evaluator replacement alone is diverted to independent adjudication.

  @scenario:evaluate-semantic-carrier-compilation
  @input:semantic-carrier-compilation-evaluation-request
  @input-contract:semantic-carrier-compilation-evaluation-request.v1
  @event:adjudicate-semantic-carrier-compilation-evidence
  @event-authority:adjudicate-semantic-carrier-compilation-evidence.v1
  @outcome:semantic-carrier-compilation-evaluation-classified
  @outcome-contract:semantic-carrier-compilation-evaluation-stage.v1
  Scenario: Evaluate semantic carrier compilation
    Given one graph-bound validator and extraction lineage plus a complete independently manufactured proof set
    When the supplied evidence is adjudicated without evaluator evidence manufacture
    Then evaluation is classified for ordinary review, hold, or evaluator-replacement independent adjudication

  @scenario:return-evaluation-held
  @input:held-evaluation-stage
  @input-contract:semantic-carrier-compilation-evaluation-stage.v1
  @event:return-evaluation-held
  @event-authority:return-evaluation-held.v1
  @outcome:semantic-carrier-compilation-evaluation-held
  @outcome-contract:semantic-carrier-compilation-evaluation-result.v1
  @outcome-terminal
  Scenario: Return evaluation held
    Given ordered attributable evidence, lineage, blackout, or independence findings
    When the evaluation-held receipt is returned
    Then EVALUATION_HELD is returned with ordered attributable findings

  @scenario:return-review-ready-evaluation
  @input:review-ready-evaluation-stage
  @input-contract:semantic-carrier-compilation-evaluation-stage.v1
  @event:return-review-ready-evaluation
  @event-authority:return-review-ready-evaluation.v1
  @outcome:semantic-carrier-compilation-review-ready
  @outcome-contract:semantic-carrier-compilation-evaluation-result.v1
  @outcome-terminal
  Scenario: Return review-ready evaluation
    Given complete passing independent evidence for a non-evaluator-replacement subject
    When the ordinary-subject review-ready receipt is returned
    Then REVIEW_READY_NON_EVALUATOR_SUBJECT is returned

  @scenario:return-evaluator-replacement-for-independent-adjudication
  @input:evaluator-replacement-evaluation-stage
  @input-contract:semantic-carrier-compilation-evaluation-stage.v1
  @event:return-evaluator-replacement-for-independent-adjudication
  @event-authority:return-evaluator-replacement-for-independent-adjudication.v1
  @outcome:evaluator-replacement-independent-adjudication-required
  @outcome-contract:semantic-carrier-compilation-evaluation-result.v1
  @outcome-terminal
  Scenario: Return evaluator replacement for independent adjudication
    Given complete passing independent evidence for an evaluator-replacement subject
    When the evaluator-replacement receipt is returned for independent adjudication
    Then EVALUATOR_REPLACEMENT_REQUIRES_INDEPENDENT_ADJUDICATION is returned

