@capability:seal-capability-change
@root-scenario:seal-capability-change
Feature: Seal one proven capability change

  An engineer or agent seals an OPEN capability change only after its bounded
  candidate closes the reviewed intent and every declared impact obligation.
  Sealing inspects the semantic delta, rejects undeclared architectural
  mutation, proves the candidate and impacted estate, and binds one immutable
  candidate capsule and seal receipt to the change set.

  A failed proof never leaves a half-sealed change. The candidate remains
  isolated and repairable under the original mutation boundary, while the
  admitted estate remains unchanged.

  @scenario:seal-capability-change
  @input:capability-change-set
  @input-contract:capability-change-set.v1
  @event:capability-change-sealing-requested
  @event-authority:seal-capability-change.v1
  @outcome:sealed-capability-change-set
  @outcome-contract:sealed-capability-change-set.v1
  @outcome-terminal
  Scenario: Seal one change only after complete closure
    Given one OPEN capability change set with bounded candidate authority and retained baseline lineage
    When capability change sealing is requested
    Then the change becomes SEALED with its before and after capsule identities, semantic and blueprint deltas, complete proof receipts, and authorized next action, or remains OPEN with exact findings and no half-sealed candidate

  @scenario:inspect-capability-change-delta
  @input:capability-change-set
  @input-contract:capability-change-set.v1
  @event:capability-change-delta-inspection-requested
  @event-authority:inspect-capability-change-delta.v1
  @outcome:capability-change-delta
  @outcome-contract:capability-change-delta.v1
  @outcome-terminal
  Scenario: Inspect the candidate delta against the mutation boundary
    Given one OPEN change set, its baseline authority, and its candidate authority
    When the semantic, blueprint, contract, dependency, mechanic, and kernel deltas are inspected
    Then every changed fact is classified and bound to an authorized mutation or an UNDECLARED_ARCHITECTURAL_MUTATION finding is returned before proof or collapse

  @scenario:prove-capability-change-closure
  @input:capability-change-delta
  @input-contract:capability-change-delta.v1
  @event:capability-change-closure-proof-requested
  @event-authority:prove-capability-change-closure.v1
  @outcome:capability-change-proof
  @outcome-contract:capability-change-proof.v1
  @outcome-terminal
  Scenario: Prove the candidate and every impacted obligation
    Given one authorized delta, the mutation set, the impact proof set, and the admitted proof policy
    When capability change closure is proven
    Then conformance, scenario fixtures, impacted capability proofs, contract compatibility, blueprint closure, Cross-Apply, observability obligations, sterility, and reconstruction either all pass with bound receipts or the exact failed obligations are returned

  @scenario:collapse-sealed-capability-change
  @input:capability-change-proof
  @input-contract:capability-change-proof.v1
  @event:sealed-capability-change-collapse-requested
  @event-authority:collapse-sealed-capability-change.v1
  @outcome:sealed-capability-change-candidate
  @outcome-contract:sealed-capability-change-candidate.v1
  @outcome-terminal
  Scenario: Collapse only a completely proven candidate
    Given one candidate whose complete change proof passes and whose lineage still binds the OPEN baseline
    When the sealed candidate is collapsed
    Then exact candidate capsule bytes, content digest, integrity proof, reconstruction proof, semantic delta, and seal receipt are bound without changing admitted authority

  @scenario:hold-unsealable-capability-change
  @input:capability-change-sealing-findings
  @input-contract:capability-change-sealing-findings.v1
  @event:capability-change-sealing-disposition-requested
  @event-authority:hold-unsealable-capability-change.v1
  @outcome:held-capability-change-seal
  @outcome-contract:held-capability-change-seal.v1
  @outcome-terminal
  Scenario: Retain an open repairable change after any seal failure
    Given an ineligible state, lineage divergence, undeclared mutation, failed proof, incomplete collapse, or digest divergence
    When the sealing disposition is resolved
    Then the change remains OPEN under its original isolation and mutation boundary with SEALING_HELD and exact findings, while admitted authority remains unchanged

