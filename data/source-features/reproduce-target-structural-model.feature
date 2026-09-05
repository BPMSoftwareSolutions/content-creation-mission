@capability:reproduce-target-structural-model
@root-scenario:reproduce-target-structural-model
# Legacy source: scenario-driven-architecture/tools/src/capabilities/structural-model-projection/reproduce-target-structural-model/provider.ts
Feature: Reproduce target structural model

  A language maintainer needs to regenerate the target structural model
  deterministically, without semantic drift: identical input must always
  produce identical plan bytes. The capability renders an admitted target
  projection graph into an in-memory target projection plan.

  Every target-projection node has an embodiment, every profile-declared
  type is represented exactly once, and identical input produces identical
  plan bytes. The capability does not write any file to disk — it only
  renders the in-memory plan later steps will consume.

  @scenario:reproduce-target-structural-model
  @input:reproduce-structural-model-input
  @input-contract:reproduce-structural-model-input.v1
  @event:target-structural-model-reproduction-requested
  @event-authority:structural-model-reproduction.v1
  @outcome:target-structural-model-plan-known
  @outcome-contract:structural-projection-plan-evidence.v1
  @outcome-terminal
  Scenario: Render an admitted target projection graph into a deterministic in-memory plan
    Given one admitted target projection graph
    When the target projection graph is rendered into an in-memory target projection plan
    Then every profile-declared type is represented exactly once with a deterministic embodiment, and identical input produces identical plan bytes
