@capability:verify-admitted-capability-lifecycle
@root-scenario:verify-admitted-capability-lifecycle
Feature: Verify one admitted capability through its portable lifecycle

  Packaging preserves capability identity. Revelation exposes capability
  meaning. Realization binds capability meaning to an execution
  environment. Execution produces the effect. Verification proves the
  chain.

  This capability owns the composition proof. Its input embeds the five
  real upstream records exactly as the upstream capabilities emitted
  them: the capsule record, the realization record, the execution
  record, the monotonicity record, and the scenario verification record.
  Its outcome is one lifecycle disposition over the upstream laws:
  packing is closed, the capsule round trip is closed, the realization
  preserves the canonical graph identity, the realization binds the
  capsule digest and the execution binds the realization digest, the
  execution is established, and the monotonicity and scenario outcome
  proofs bind the same canonical graph and capability identity. No
  digest domain is conflated; lineage is verified against the upstream
  record fields themselves.

  @scenario:verify-admitted-capability-lifecycle
  @input:capability-lifecycle-proof-record
  @input-contract:capability-lifecycle-proof-record.v1
  @event:capability-lifecycle-verification-requested
  @event-authority:verify-admitted-capability-lifecycle.v1
  @outcome:capability-lifecycle-proof-record
  @outcome-contract:capability-lifecycle-proof-record.v1
  @outcome-terminal
  Scenario: Verify one admitted capability through its portable lifecycle
    Given the five upstream lifecycle records for one admitted capability
    When lifecycle verification is evaluated over the upstream law dispositions
    Then the lifecycle conforms or reports LIFECYCLE_HELD with the typed divergence, and the lifecycle receipt binds capability identity, realization, execution, and disposition

  @scenario:verify-capability-identity-preservation
  @input:capability-lifecycle-proof-record
  @input-contract:capability-lifecycle-proof-record.v1
  @event:capability-identity-preservation-verification-requested
  @event-authority:verify-capability-identity-preservation.v1
  @outcome:capability-lifecycle-proof-record
  @outcome-contract:capability-lifecycle-proof-record.v1
  @outcome-terminal
  Scenario: Verify capability identity preservation across the lifecycle
    Given one realization record with a realized graph digest and a canonical graph digest
    When identity preservation is evaluated
    Then the realized graph digest equals the canonical graph digest, and any divergence reports CANONICAL_IDENTITY_DIVERGED

  @scenario:verify-capsule-round-trip
  @input:capability-lifecycle-proof-record
  @input-contract:capability-lifecycle-proof-record.v1
  @event:capsule-round-trip-verification-requested
  @event-authority:verify-capsule-round-trip.v1
  @outcome:capability-lifecycle-proof-record
  @outcome-contract:capability-lifecycle-proof-record.v1
  @outcome-terminal
  Scenario: Verify the capsule packing and round trip closed
    Given one capsule record with a packing disposition and a round trip disposition
    When packing and round trip closure are evaluated
    Then packing is CAPSULE_PACKED and the round trip is REVEAL_PACK_CLOSED, reporting PACKING_OPEN or ROUND_TRIP_OPEN otherwise

  @scenario:verify-execution-preservation
  @input:capability-lifecycle-proof-record
  @input-contract:capability-lifecycle-proof-record.v1
  @event:execution-preservation-verification-requested
  @event-authority:verify-execution-preservation.v1
  @outcome:capability-lifecycle-proof-record
  @outcome-contract:capability-lifecycle-proof-record.v1
  @outcome-terminal
  Scenario: Verify lineage binding and established execution
    Given one capsule record, one realization record, and one execution record
    When lineage binding and execution establishment are evaluated
    Then the realization binds the capsule digest and the execution binds the realization digest with the effect established, reporting LINEAGE_BINDING_DIVERGED or EXECUTION_NOT_ESTABLISHED otherwise

  @scenario:verify-monotonicity-proof-binding
  @input:capability-lifecycle-proof-record
  @input-contract:capability-lifecycle-proof-record.v1
  @event:monotonicity-proof-binding-verification-requested
  @event-authority:verify-monotonicity-proof-binding.v1
  @outcome:capability-lifecycle-proof-record
  @outcome-contract:capability-lifecycle-proof-record.v1
  @outcome-terminal
  Scenario: Verify the monotonicity proof binds the same canonical graph
    Given one monotonicity record and one realization record
    When monotonicity proof binding is evaluated
    Then the monotonicity disposition is MONOTONIC_CIRCUIT and its canonical graph digest equals the realization canonical graph digest, reporting MONOTONICITY_PROOF_UNBOUND otherwise

  @scenario:verify-scenario-outcome-proof-binding
  @input:capability-lifecycle-proof-record
  @input-contract:capability-lifecycle-proof-record.v1
  @event:scenario-outcome-proof-binding-verification-requested
  @event-authority:verify-scenario-outcome-proof-binding.v1
  @outcome:capability-lifecycle-proof-record
  @outcome-contract:capability-lifecycle-proof-record.v1
  @outcome-terminal
  Scenario: Verify the scenario outcome proof binds the same capability identity
    Given one scenario verification record, one capsule record, and one realization record
    When scenario outcome proof binding is evaluated
    Then the scenario verification disposition is CAPABILITY_SCENARIO_CORPUS_CONFORMANT with the capsule capability identity and the realization canonical graph digest, reporting SCENARIO_OUTCOME_PROOF_UNBOUND otherwise
