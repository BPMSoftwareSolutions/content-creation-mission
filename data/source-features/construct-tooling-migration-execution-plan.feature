@capability:construct-tooling-migration-execution-plan
@root-scenario:construct-tooling-migration-execution-plan
Feature: Construct a controlled tooling migration execution plan

  An SDA maintainer submits one admitted tooling migration request for
  inventory, verification, promotion, or a serial migration run. The request
  identifies the governed migration authority, selected capabilities,
  required projection targets, and full-gate policy, but it does not prescribe
  executable source or bypass any acceptance authority.

  The capability constructs the complete ordered work plan that the current
  tooling migration conveyor performs. Every policy decision is delegated to
  the already projected decide-tooling-migration capability. Repository
  observation, projection, target execution, legacy-oracle comparison, atomic
  binding replacement, full-gate execution, rollback, and evidence publication
  remain explicit effect-capability dependencies that execute outside this
  pure planning boundary.

  Verification must complete before promotion can begin. A promotion plan
  retains the exact prior binding, evaluates the full-gate receipt through the
  decision capability, restores the prior binding on rejection, and publishes
  terminal evidence. A run plan orders capabilities deterministically and
  promotes them serially so one decision is complete before the next begins.

  The returned plan is candidate execution authority. It does not claim that
  any effect ran, any candidate passed acceptance, any binding was promoted,
  or the handwritten conveyor is already replaceable.

  @scenario:construct-tooling-migration-execution-plan
  @input:controlled-tooling-migration-request
  @input-contract:controlled-tooling-migration-request.v1
  @event:construct-tooling-migration-execution-plan
  @event-authority:construct-tooling-migration-execution-plan.v1
  @outcome:tooling-migration-execution-plan-known
  @outcome-contract:tooling-migration-execution-plan.v1
  @outcome-terminal
  Scenario: Construct the ordered work for one controlled tooling migration request
    Given one admitted inventory, verify, promote, or serial run request with governed migration authority and effect-capability bindings
    When a tooling migration execution plan is requested
    Then deterministic ordered work, rollback policy, dependency authority, and non-claim evidence are returned without executing or promoting the migration
