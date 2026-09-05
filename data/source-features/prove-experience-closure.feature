@capability:prove-experience-closure
@root-scenario:prove-experience-closure
# Legacy source: scenario-driven-architecture/tools/src/capabilities/consumer-assurance/prove-experience-closure/provider.ts
Feature: Prove experience closure

  A consumer needs to know whether a capability actually delivered its
  promised value, not merely whether its code ran. The capability evaluates
  promised experience conditions from runtime observations.

  Every promised experience condition is satisfied, unsatisfied, or not
  observable; nothing is assumed satisfied by default. The capability does
  not run the capability itself — it only evaluates already-observed
  runtime outcomes against the promised conditions.

  @scenario:prove-experience-closure
  @input:consumer-experience-observation-facts
  @input-contract:prove-experience-closure-input.v1
  @event:experience-closure-proof-requested
  @event-authority:consumer-experience-closure-proof.v1
  @outcome:experience-closure-known
  @outcome-contract:experience-closure-evidence.v1
  @outcome-terminal
  Scenario: Evaluate promised experience conditions from runtime observations
    Given consumer experience observation facts collected from runtime execution
    When promised experience conditions are evaluated from those runtime observations
    Then every promised experience condition is satisfied, unsatisfied, or explicitly not observable
