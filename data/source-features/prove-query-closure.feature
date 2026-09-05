@capability:prove-query-closure
@root-scenario:prove-query-closure
# Legacy source: scenario-driven-architecture/tools/src/capabilities/consumer-assurance/prove-query-closure/provider.ts
Feature: Prove query closure

  A consumer needs to know that every promised inspectable question a
  capability claims to answer is actually answerable from observed
  behavior. The capability evaluates implemented queries against fixture
  observations.

  Every implemented query is observed with a satisfying fixture result, or
  is explicitly unproven. The capability does not implement or run the
  queries itself — it only evaluates whether already-implemented queries
  are backed by observation.

  @scenario:prove-query-closure
  @input:consumer-query-observation-facts
  @input-contract:prove-query-closure-input.v1
  @event:query-closure-proof-requested
  @event-authority:consumer-query-closure-proof.v1
  @outcome:query-closure-known
  @outcome-contract:query-closure-evidence.v1
  @outcome-terminal
  Scenario: Evaluate implemented consumer queries against fixture observations
    Given consumer query observation facts collected from fixtures
    When implemented queries are evaluated against fixture observations
    Then every implemented query is observed with a satisfying fixture result, or is explicitly unproven
