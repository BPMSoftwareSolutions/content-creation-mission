@capability:resolve-registered-realization-plan
@root-scenario:resolve-registered-realization-plan
# Legacy source: scenario-driven-architecture/tools/src/capabilities/realization-planning/resolve-registered-realization-plan/provider.ts
Feature: Resolve registered realization plan

  A realization operator needs to use friendly, registry-backed authority
  selectors without ever losing exact digest lineage. The capability
  resolves admitted aliases to immutable digests and invokes deterministic
  plan construction.

  Every requested authority selector resolves exactly once and is
  digest-pinned before planning proceeds; resolution evidence identifies
  the alias or digest and the exact immutable digest selected for every
  authority. The capability does not construct the plan's provider
  decisions itself — it only resolves selectors to pinned authority and
  delegates to deterministic plan construction.

  @scenario:resolve-registered-realization-plan
  @input:registry-backed-realization-plan-request
  @input-contract:registry-backed-realization-plan-request.v1
  @event:registered-realization-plan-requested
  @event-authority:registered-realization-plan-resolution.v1
  @outcome:registered-realization-plan-known
  @outcome-contract:registry-backed-realization-plan-evidence.v1
  @outcome-terminal
  Scenario: Resolve registry-backed selectors to pinned authority before constructing a plan
    Given one registry-backed realization plan request naming admitted selectors
    When admitted aliases are resolved to immutable digests and deterministic plan construction is invoked
    Then every requested authority selector resolves exactly once and is digest-pinned before planning, with resolution evidence naming the alias and its selected digest
