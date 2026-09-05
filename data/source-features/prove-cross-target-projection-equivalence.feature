@capability:prove-cross-target-projection-equivalence
@root-scenario:prove-cross-target-projection-equivalence
# Legacy source: scenario-driven-architecture/tools/src/capabilities/consumer-assurance/prove-cross-target-projection-equivalence/provider.ts
Feature: Prove cross-target projection equivalence

  A consumer needs to know that choosing one projected runtime target over
  another never changes what a capability means. The capability compares
  outcomes and scenario lineage across projected runtimes.

  Every fixture has an explicit equivalence disposition for every target,
  and every projected target preserves outcome and lineage. The capability
  does not run the fixtures itself — it only compares outcomes already
  produced by each target.

  @scenario:prove-cross-target-projection-equivalence
  @input:consumer-target-execution-facts
  @input-contract:prove-cross-target-projection-equivalence-input.v1
  @event:cross-target-equivalence-proof-requested
  @event-authority:consumer-cross-target-equivalence-proof.v1
  @outcome:cross-target-projection-equivalence-known
  @outcome-contract:cross-target-projection-equivalence-evidence.v1
  @outcome-terminal
  Scenario: Compare consumer outcomes and scenario lineage across projected runtimes
    Given consumer target execution facts observed across projected runtimes
    When outcomes and scenario lineage are compared across projected runtimes
    Then every fixture has an explicit equivalence disposition for every target, and every projected target preserves outcome and lineage
