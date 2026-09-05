@capability:operate-tooling-migration-promote
@root-scenario:operate-tooling-migration-promote
Feature: Operate the governed tooling migration promote command

  Original hand-authored source replaced by this projected command boundary:
  capabilities/tooling-migration-runtime/node/tooling-migration-operation-provider.mjs,
  especially replaceBindingDocument and promoteBindingTransaction at lines
  269-298 and promotion routing at lines 453-509.

  The Agentic Harness exposes this operation through a projected CLI. The
  projected scenario admits the request and invokes the pinned projected
  operate-tooling-migration-conveyor capability. Deterministic migration policy remains owned by the projected
  decide-tooling-migration capability. Model testimony cannot establish
  verification, promotion, rollback, continuation, or completion.

  @scenario:operate-tooling-migration-promote
  @input:tooling-migration-promote-request
  @input-contract:tooling-migration-promote-request.v1
  @event:operate-tooling-migration-promote
  @event-authority:operate-tooling-migration-promote.v1
  @outcome:tooling-migration-promote-evidence
  @outcome-contract:tooling-migration-promote-evidence.v1
  @outcome-terminal
  Scenario: Execute the governed tooling migration promote operation
    Given one admitted promote request and the pinned tooling migration authority
    When the projected Agentic Harness interface invokes the projected conveyor capability
    Then attributable promote evidence and an explicit interface exit disposition are returned
