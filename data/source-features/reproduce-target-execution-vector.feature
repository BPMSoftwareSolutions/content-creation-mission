@capability:reproduce-target-execution-vector
@root-scenario:reproduce-target-execution-vector
# Legacy source: scenario-driven-architecture/tools/src/capabilities/execution-vector-projection/reproduce-target-execution-vector/provider.ts
Feature: Reproduce target execution vector

  A language maintainer needs to regenerate the target execution circuit
  deterministically: identical input must always yield identical bytes. The
  capability renders an in-memory execution projection plan from the target
  execution graph without invoking any toolchain.

  Every target execution node has a deterministic embodiment, and the plan
  carries unique paths, stable bytes, digests, and source lineage. The
  capability does not write any file to disk or invoke a compiler — it only
  renders the in-memory plan those steps will later consume.

  @scenario:reproduce-target-execution-vector
  @input:target-execution-graph
  @input-contract:reproduce-target-execution-vector-input.v1
  @event:target-execution-vector-reproduction-requested
  @event-authority:target-execution-vector-reproduction.v1
  @outcome:target-execution-vector-plan-known
  @outcome-contract:execution-projection-plan-evidence.v1
  @outcome-terminal
  Scenario: Render a deterministic in-memory execution projection plan
    Given one target execution graph
    When an in-memory execution projection plan is rendered without invoking a toolchain
    Then every target execution node has a deterministic embodiment with a unique path, stable bytes, digest, and source lineage, and identical input yields identical bytes
