@capability:bind-canonical-blueprint-review
@root-scenario:bind-canonical-blueprint-review
Feature: Bind one canonical blueprint review

  Before capability authority is admitted for collapse, a designated human must
  receive the deterministic projections and return approve, hold, or reject
  testimony. Designated human blueprint approval is a permanent, universal
  admission obligation, not a temporary assurance profile.

  The human decision occurs at the SideFX experience boundary. The provisioning
  circuit must durably pause after it publishes the exact review boundary and may
  resume only after the designated reviewer supplies testimony against that
  boundary. This capability does not simulate or invoke a human provider. It
  consumes the submitted testimony and deterministically validates, binds, and
  receipts it.

  Neither the person nor the interface self-admits the capability. An APPROVE
  receipt satisfies only the design-review obligation consumed by deterministic
  admission alongside contract, identity, lineage, closure, and proof gates. A
  HOLD or REJECT is valid review testimony and also receives a digest-bound
  receipt; it does not become a malformed-request failure.

  @scenario:bind-canonical-blueprint-review
  @input:canonical-blueprint-review-binding-request
  @input-contract:canonical-blueprint-review-binding-request.v2
  @event:bind-canonical-blueprint-review
  @event-authority:bind-canonical-blueprint-review.v1
  @outcome:canonical-blueprint-review-receipt
  @outcome-contract:canonical-blueprint-review-receipt.v2
  @outcome-terminal
  Scenario: Bind submitted human review testimony to the exact review boundary
    Given one projected blueprint bundle, its projection receipt, and submitted designated-reviewer testimony
    When the review boundary and testimony are admitted, the disposition is bound, and digest closure is verified
    Then one review receipt carries the reviewer authority, every reviewed surface digest, and an approve, hold, or reject disposition, without admitting the capability

  @scenario:admit-blueprint-review-boundary
  @input:canonical-blueprint-review-binding-request
  @input-contract:canonical-blueprint-review-binding-request.v2
  @event:admit-blueprint-review-boundary
  @event-authority:admit-blueprint-review-boundary.v1
  @outcome:blueprint-review-boundary-admission
  @outcome-contract:blueprint-review-boundary-admission.v2
  @outcome-variants:REVIEW_BOUNDARY_ADMITTED|REVIEW_BOUNDARY_REJECTED
  Scenario: Admit only a complete and current review boundary
    Given one binding request carrying the exact blueprint, projection-receipt, and review-boundary bytes plus their claimed digests and a designated reviewer authority
    When every byte digest is recomputed, each JSON carrier is parsed without exception, and the claimed boundary is resolved against the carried blueprint and projection receipt
    Then a complete byte-closed boundary is admitted, while malformed bytes, a digest mismatch, a missing required view, an uncarried digest, or an absent designated reviewer authority is rejected before submitted testimony is read

  @scenario:admit-human-blueprint-review-testimony
  @input:admitted-blueprint-review-boundary
  @input-contract:admitted-blueprint-review-boundary.v2
  @event:admit-human-blueprint-review-testimony
  @event-authority:admit-human-blueprint-review-testimony.v1
  @outcome:human-blueprint-review-testimony-admission
  @outcome-contract:human-blueprint-review-testimony-admission.v2
  @outcome-variants:HUMAN_REVIEW_TESTIMONY_ADMITTED|HUMAN_REVIEW_TESTIMONY_REJECTED
  Scenario: Admit only testimony supplied by the designated reviewer for the exact boundary
    Given one admitted review boundary and the testimony submitted with its binding request
    When reviewer authority, presented surface digests, disposition, and required findings are validated
    Then exact approve, hold, or reject testimony is admitted immutably, while mismatched reviewer authority, changed surfaces, an undeclared disposition, or hold or reject testimony without exact findings is rejected

  @scenario:bind-blueprint-review-disposition
  @input:admitted-human-blueprint-review-testimony
  @input-contract:admitted-human-blueprint-review-testimony.v2
  @event:bind-blueprint-review-disposition
  @event-authority:bind-blueprint-review-disposition.v1
  @outcome:blueprint-review-disposition-binding
  @outcome-contract:blueprint-review-disposition-binding.v2
  @outcome-variants:REVIEW_DISPOSITION_BOUND|REVIEW_DISPOSITION_REJECTED
  Scenario: Bind the exact valid decision without changing its meaning
    Given admitted human review testimony for one exact boundary
    When its decision is bound to the reviewed authority and surface digests
    Then approve, hold, or reject is preserved exactly, and contradictory or incomplete binding testimony is rejected rather than repaired

  @scenario:verify-blueprint-review-digest-closure
  @input:bound-blueprint-review-disposition
  @input-contract:bound-blueprint-review-disposition.v2
  @event:verify-blueprint-review-digest-closure
  @event-authority:verify-blueprint-review-digest-closure.v1
  @outcome:canonical-blueprint-review-receipt
  @outcome-contract:canonical-blueprint-review-receipt.v2
  @outcome-variants:REVIEW_RECEIPT_BOUND|REVIEW_DIGEST_CLOSURE_REJECTED
  Scenario: Emit a receipt only while every submitted digest closes against the admitted byte boundary
    Given one bound review disposition whose admitted boundary retains the exact blueprint, projection-receipt, and review-boundary bytes
    When every bound digest is compared with the recomputed byte digests and parsed authority fields retained by that admitted boundary
    Then a receipt is emitted only while every digest matches the admitted bytes, and any blueprint, boundary, view, or projection-profile mismatch rejects closure and requires re-projection and re-review; later admission independently compares the receipt with current governed authority

