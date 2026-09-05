@capability:execute-capsule-direct
@root-scenario:execute-capsule-direct
Feature: Execute one capability directly from its physical capsule

  Store the capability. Project the explanation. Execute the effect.

  This capability owns the final product law: a capsule executes
  without expansion. Its input is the physical capsule bytes, the
  declared capsule digest, the declared projected binding identity,
  and one scenario input. Its outcome is DIRECT_EXECUTION_ESTABLISHED
  or DIRECT_EXECUTION_HELD. The capsule decodes in memory, its digest
  verifies, its capability authority digest equals the admitted
  projected binding authority, the binding executes the scenario
  input, and the observed outcome must equal the declared expected
  disposition. No workspace is written and no expanded representation
  is required for ordinary execution.

  @scenario:execute-capsule-direct
  @input:capsule-direct-execution-record
  @input-contract:capsule-direct-execution-record.v1
  @event:capsule-direct-execution-requested
  @event-authority:execute-capsule-direct.v1
  @outcome:capsule-direct-execution-record
  @outcome-contract:capsule-direct-execution-record.v1
  @outcome-terminal
  Scenario: Execute one capability directly from its physical capsule
    Given one physical capsule byte sequence, one declared capsule digest, one declared projected binding identity, and one scenario input
    When the capsule is executed directly
    Then the execution is DIRECT_EXECUTION_ESTABLISHED or DIRECT_EXECUTION_HELD with the exact holding finding, and a receipt binds capsule digest, binding digest, scenario input digest, evidence disposition, and disposition

  @scenario:verify-capsule-gate
  @input:capsule-direct-execution-record
  @input-contract:capsule-direct-execution-record.v1
  @event:capsule-gate-verification-requested
  @event-authority:verify-capsule-gate.v1
  @outcome:capsule-direct-execution-record
  @outcome-contract:capsule-direct-execution-record.v1
  @outcome-terminal
  Scenario: Verify the capsule digest and binding authority gate
    Given one physical capsule byte sequence, one declared capsule digest, and one declared projected binding authority digest
    When the capsule gate is verified
    Then the recomputed capsule digest equals the declared digest and the capsule capability authority digest equals the declared binding authority digest, reporting CAPSULE_DIGEST_DIVERGED or BINDING_AUTHORITY_DIVERGED otherwise

  @scenario:admit-direct-execution-evidence
  @input:capsule-direct-execution-record
  @input-contract:capsule-direct-execution-record.v1
  @event:direct-execution-evidence-admission-requested
  @event-authority:admit-direct-execution-evidence.v1
  @outcome:capsule-direct-execution-record
  @outcome-contract:capsule-direct-execution-record.v1
  @outcome-terminal
  Scenario: Admit the direct execution evidence
    Given one direct execution evidence record and one declared expected outcome disposition
    When the evidence is admitted
    Then the observed evidence disposition equals the declared expected outcome disposition, reporting OUTCOME_NOT_ESTABLISHED otherwise

  @scenario:bind-direct-execution-receipt
  @input:capsule-direct-execution-record
  @input-contract:capsule-direct-execution-record.v1
  @event:direct-execution-receipt-binding-requested
  @event-authority:bind-direct-execution-receipt.v1
  @outcome:capsule-direct-execution-record
  @outcome-contract:capsule-direct-execution-record.v1
  @outcome-terminal
  Scenario: Bind one direct execution receipt
    Given one direct execution disposition over one capsule execution
    When the direct execution receipt is bound
    Then the capsule digest, binding digest, scenario input digest, evidence disposition, and disposition bind into one replayable direct execution receipt
