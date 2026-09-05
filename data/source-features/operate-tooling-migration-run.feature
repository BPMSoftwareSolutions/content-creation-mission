@capability:operate-tooling-migration-run
@root-scenario:operate-tooling-migration-run
Feature: Operate the governed tooling migration run command

  Original hand-authored source replaced by this projected command boundary:
  capabilities/tooling-migration-runtime/node/tooling-migration-operation-provider.mjs,
  especially executeOne at lines 389-446 and stable serial run routing at
  lines 453-509.

  The Agentic Harness exposes this operation through a projected CLI. The
  projected scenario admits the request and invokes the pinned projected
  operate-tooling-migration-conveyor capability. Deterministic migration policy remains owned by the projected
  decide-tooling-migration capability. Model testimony cannot establish
  verification, promotion, rollback, continuation, or completion.

  @scenario:operate-tooling-migration-run
  @input:tooling-migration-run-request
  @input-contract:tooling-migration-run-request.v1
  @event:operate-tooling-migration-run
  @event-authority:operate-tooling-migration-run.v1
  @outcome:tooling-migration-run-evidence
  @outcome-contract:tooling-migration-run-evidence.v1
  @outcome-terminal
  Scenario: Execute the governed tooling migration run operation
    Given one admitted run request and the pinned tooling migration authority
    When the projected Agentic Harness interface invokes the projected conveyor capability
    Then attributable run evidence and an explicit interface exit disposition are returned
