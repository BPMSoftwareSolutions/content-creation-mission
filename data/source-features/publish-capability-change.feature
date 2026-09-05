@capability:publish-capability-change
@root-scenario:publish-capability-change
Feature: Publish one sealed capability change to mainline

  A publisher admits one SEALED capability change only through a fail-closed
  mainline transaction. Publication refreshes current authority, compares it
  with the sealed baseline, re-resolves impact, reproves compatible movement,
  admits the exact candidate capsule, and binds repository lineage to the
  admitted change.

  Publication never invents a semantic merge. Incompatible baseline movement,
  failed mainline proof, incomplete admission, or failed lineage publication
  leaves the previous admitted estate current and the sealed candidate intact.

  @scenario:publish-capability-change
  @input:sealed-capability-change-set
  @input-contract:sealed-capability-change-set.v1
  @event:capability-change-publication-requested
  @event-authority:publish-capability-change.v1
  @outcome:published-capability-change-set
  @outcome-contract:published-capability-change-set.v1
  @outcome-terminal
  Scenario: Publish one sealed change through a governed mainline transaction
    Given one SEALED capability change with an exact candidate capsule, proof, baseline, and publication authority
    When capability change publication is requested
    Then the exact candidate becomes admitted, mainline proof and repository lineage close, and the change becomes PUBLISHED with a publication receipt, or the prior admitted estate remains current with exact held findings

  @scenario:revalidate-capability-change-baseline
  @input:sealed-capability-change-set
  @input-contract:sealed-capability-change-set.v1
  @event:capability-change-baseline-revalidation-requested
  @event-authority:revalidate-capability-change-baseline.v1
  @outcome:capability-change-baseline-revalidation
  @outcome-contract:capability-change-baseline-revalidation.v1
  @outcome-terminal
  Scenario: Compare the sealed baseline with current mainline authority
    Given one sealed baseline and the current admitted capsule, authority, blueprint, dependency, and repository identities
    When baseline compatibility is revalidated
    Then unchanged authority proceeds, compatible movement produces a bounded reproof requirement, and incompatible movement reports BASELINE_MOVED with CHANGE_REVALIDATION_REQUIRED without inferring a merge

  @scenario:reprove-capability-change-on-mainline
  @input:capability-change-baseline-revalidation
  @input-contract:capability-change-baseline-revalidation.v1
  @event:capability-change-mainline-proof-requested
  @event-authority:reprove-capability-change-on-mainline.v1
  @outcome:capability-change-mainline-proof
  @outcome-contract:capability-change-mainline-proof.v1
  @outcome-terminal
  Scenario: Re-resolve impact and prove the candidate against current mainline
    Given one unchanged or compatibly moved baseline and one exact sealed candidate
    When semantic impact and the full mainline proof are resolved again
    Then every current dependency, route, contract, experience, capsule, and repository obligation either passes with a current receipt or publication is held before admission

  @scenario:admit-and-record-capability-change
  @input:capability-change-mainline-proof
  @input-contract:capability-change-mainline-proof.v1
  @event:capability-change-admission-transaction-requested
  @event-authority:admit-and-record-capability-change.v1
  @outcome:capability-change-publication-receipt
  @outcome-contract:capability-change-publication-receipt.v1
  @outcome-terminal
  Scenario: Admit the candidate and bind architectural lineage atomically
    Given one exact sealed capsule with a current passing mainline proof and authorized publication effect
    When admission and repository lineage publication are transacted
    Then the new admitted capsule, previous capsule, change identity, reason reference, blueprint digest, proof receipt digest, repository identity, and publication disposition bind into one durable receipt

  @scenario:restore-prior-capability-change-admission
  @input:capability-change-publication-failure
  @input-contract:capability-change-publication-failure.v1
  @event:capability-change-publication-recovery-requested
  @event-authority:restore-prior-capability-change-admission.v1
  @outcome:held-capability-change-publication
  @outcome-contract:held-capability-change-publication.v1
  @outcome-terminal
  Scenario: Preserve the exact prior admission after publication failure
    Given any failed baseline revalidation, mainline proof, capsule admission, lineage publication, or resulting-state verification
    When publication recovery is resolved
    Then the exact prior admitted estate remains current, the sealed candidate remains available for revalidation, and PUBLISHING_HELD reports the failed boundary without a partial published state

