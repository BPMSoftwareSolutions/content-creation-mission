@capability:operate-tooling-migration-verify
@root-scenario:operate-tooling-migration-verify
Feature: Operate the governed tooling migration verify command

  Original hand-authored source replaced by this projected command boundary:
  capabilities/tooling-migration-runtime/node/tooling-migration-operation-provider.mjs,
  especially verifyAuthoringTestimony at lines 197-248, verifyCapability at
  lines 340-373, and verify routing at lines 453-509.

  The Agentic Harness exposes this operation through a projected CLI. The
  projected scenario admits the request and invokes the pinned projected
  operate-tooling-migration-conveyor capability. Deterministic migration policy remains owned by the projected
  decide-tooling-migration capability. Model testimony cannot establish
  verification, promotion, rollback, continuation, or completion.

  @scenario:operate-tooling-migration-verify
  @input:tooling-migration-verify-request
  @input-contract:tooling-migration-verify-request.v1
  @event:operate-tooling-migration-verify
  @event-authority:operate-tooling-migration-verify.v1
  @outcome:tooling-migration-verify-evidence
  @outcome-contract:tooling-migration-verify-evidence.v1
  @outcome-terminal
  Scenario: Execute the governed tooling migration verify operation
    Given one admitted verify request and the pinned tooling migration authority
    When the projected Agentic Harness interface invokes the projected conveyor capability
    Then attributable verify evidence and an explicit interface exit disposition are returned
