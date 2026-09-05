@capability:admit-canonical-circuit-blueprint
@root-scenario:admit-canonical-circuit-blueprint
Feature: Admit one canonical circuit blueprint

  Admission is the only step that converts a blueprint candidate into immutable
  authority eligible to guide fabrication. Everything reaching it is testimony:
  conformance evidence, geometry proof, projection receipts, and human review
  are each consumed as inputs to a decision none of them can make alone.

  This capability requires deterministic conformance, a geometry proof, and one
  current approved review receipt, and proves that the reviewed digests still
  match the candidate authority. A successful projection, a green gate, or a
  zero exit code does not establish eligibility.

  Once admitted, the blueprint becomes the fixed map every later authoring
  request, integration, closure decision, human view, and proof obligation must
  resolve from by digest.

  @scenario:admit-canonical-circuit-blueprint
  @input:canonical-blueprint-admission-request
  @input-contract:canonical-blueprint-admission-request.v1
  @event:admit-canonical-circuit-blueprint
  @event-authority:admit-canonical-circuit-blueprint.v1
  @outcome:admitted-canonical-circuit-blueprint
  @outcome-contract:admitted-canonical-circuit-blueprint.v1
  @outcome-terminal
  Scenario: Emit immutable blueprint authority only when every admission obligation closes
    Given one blueprint candidate with its conformance evidence, geometry proof, and review receipt
    When each required obligation is resolved and the reviewed digests are compared with the candidate authority
    Then immutable blueprint authority with a stable digest is emitted only when every obligation closes, and otherwise an exact rejection naming the unmet obligation is returned

  @scenario:require-blueprint-conformance-evidence
  @input:canonical-blueprint-admission-request
  @input-contract:canonical-blueprint-admission-request.v1
  @event:require-blueprint-conformance-evidence
  @event-authority:require-blueprint-conformance-evidence.v1
  @outcome:conformance-obligation-disposition
  @outcome-contract:blueprint-admission-obligation-disposition.v1
  Scenario: Require conformance evidence bound to this candidate digest
    Given one admission request naming a candidate and its conformance evidence
    When the evidence is resolved and its bound digest is compared with the candidate
    Then evidence carrying findings, evidence bound to a different digest, and absent evidence are each unmet obligations

  @scenario:require-blueprint-geometry-proof
  @input:canonical-blueprint-admission-request
  @input-contract:canonical-blueprint-admission-request.v1
  @event:require-blueprint-geometry-proof
  @event-authority:require-blueprint-geometry-proof.v1
  @outcome:geometry-obligation-disposition
  @outcome-contract:blueprint-admission-obligation-disposition.v1
  Scenario: Require a conforming geometry proof bound to this candidate digest
    Given one admission request naming a candidate and its geometry proof
    When the proof is resolved and its counted summary and disposition are inspected
    Then a holding disposition, a summary whose totals do not reconcile, and a proof bound to a different digest are each unmet obligations

  @scenario:require-current-approved-review-receipt
  @input:canonical-blueprint-admission-request
  @input-contract:canonical-blueprint-admission-request.v1
  @event:require-current-approved-review-receipt
  @event-authority:require-current-approved-review-receipt.v1
  @outcome:review-obligation-disposition
  @outcome-contract:blueprint-admission-obligation-disposition.v1
  Scenario: Require one current approved review receipt whose digests still match
    Given one admission request naming a candidate and its review receipt
    When the receipt disposition is resolved and every reviewed digest is compared with the current candidate authority
    Then a hold or reject disposition, a receipt whose reviewed digests no longer match, and an absent receipt are each unmet obligations, and no assurance profile waives this requirement

  @scenario:emit-immutable-blueprint-authority
  @input:canonical-blueprint-admission-request
  @input-contract:canonical-blueprint-admission-request.v1
  @event:emit-immutable-blueprint-authority
  @event-authority:emit-immutable-blueprint-authority.v1
  @outcome:admitted-canonical-circuit-blueprint
  @outcome-contract:admitted-canonical-circuit-blueprint.v1
  Scenario: Emit the fixed map every later authoring request must resolve from
    Given every admission obligation resolved as met for one candidate
    When the candidate disposition is advanced to ADMITTED and its authority digest is bound
    Then immutable blueprint authority is emitted with a stable digest, and its emission claims no fabrication, projection, or capability admission of its own
