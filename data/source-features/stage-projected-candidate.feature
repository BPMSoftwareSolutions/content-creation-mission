@capability:stage-projected-candidate
@root-scenario:stage-projected-candidate
# Legacy source: scenario-driven-architecture/tools/src/capabilities/projected-implementation-promotion/stage-projected-candidate/provider.ts
Feature: Stage projected candidate

  A language maintainer needs to inspect a freshly generated candidate
  implementation safely, with zero risk of the admitted implementation
  being touched before the candidate is proven. The capability evaluates
  that a complete plan was staged without modifying admitted bytes.

  Staging never modifies the admitted implementation; the candidate remains
  isolated outside the admitted destination until an explicit activation
  decision. The capability does not promote or activate anything — it only
  proves that staging itself was safe.

  @scenario:stage-projected-candidate
  @input:projection-plan-and-staging-facts
  @input-contract:stage-projected-candidate-input.v1
  @event:projected-candidate-staging-requested
  @event-authority:projected-candidate-staging.v1
  @outcome:projected-candidate-staged
  @outcome-contract:projected-candidate-staging-evidence.v1
  @outcome-terminal
  Scenario: Evaluate that a complete plan was staged without modifying admitted bytes
    Given one projection plan and its staging facts
    When staging is evaluated to confirm the complete plan was staged without modifying admitted bytes
    Then the admitted implementation remains unmodified and the candidate is isolated outside the admitted destination until activation
