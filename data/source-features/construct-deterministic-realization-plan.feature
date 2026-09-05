@capability:construct-deterministic-realization-plan
@root-scenario:construct-deterministic-realization-plan
# Legacy source: scenario-driven-architecture/tools/src/capabilities/realization-planning/construct-deterministic-realization-plan/provider.ts
Feature: Construct deterministic realization plan

  A realization operator needs to review the exact authority and provider
  decisions a realization would make before any target is ever changed. The
  capability validates immutable authority and resolves exactly one
  admitted provider for every target responsibility.

  Planning produces one content-addressed plan from pinned authority, or
  blocks with explicit governed findings, without mutating any target;
  every requested target and responsibility has exactly one admitted
  provider binding, and the plan digest covers every selected authority.
  The capability does not apply the plan or touch any target — it only
  produces the reviewable plan or the reason it cannot yet be produced.

  @scenario:construct-deterministic-realization-plan
  @input:admitted-realization-planning-authority
  @input-contract:construct-deterministic-realization-plan-input.v1
  @event:deterministic-realization-plan-requested
  @event-authority:deterministic-realization-plan-construction.v1
  @outcome:realization-plan-compilation-known
  @outcome-contract:realization-plan-compilation-evidence.v1
  @outcome-terminal
  Scenario: Resolve admitted authority into one content-addressed realization plan without changing a target
    Given admitted immutable realization planning authority
    When that authority is validated and exactly one admitted provider is resolved for every target responsibility
    Then planning produces one content-addressed plan from pinned authority, or blocks with explicit governed findings, and no target is mutated
