@capability:promote-proven-implementation
@root-scenario:promote-proven-implementation
# Legacy source: scenario-driven-architecture/tools/src/capabilities/projected-implementation-promotion/promote-proven-implementation/provider.ts
Feature: Promote proven implementation

  A language maintainer needs to adopt a proven generated implementation
  confidently, with an atomic activation and a manifest that names exactly
  what was promoted. The capability evaluates atomic activation and exact
  manifest publication for a proven plan.

  Publication is atomic, and the committed manifest names every promoted
  digest exactly. The capability does not prove the candidate itself — it
  only evaluates whether promotion of an already-proven candidate was
  performed atomically and manifested exactly.

  @scenario:promote-proven-implementation
  @input:proven-plan-and-transaction-facts
  @input-contract:promote-proven-implementation-input.v1
  @event:proven-implementation-promotion-requested
  @event-authority:proven-implementation-promotion.v1
  @outcome:proven-implementation-promoted
  @outcome-contract:promotion-evidence.v1
  @outcome-terminal
  Scenario: Evaluate atomic activation and exact manifest publication for a proven plan
    Given one proven plan and its promotion transaction facts
    When atomic activation and exact manifest publication are evaluated
    Then publication is atomic and the committed manifest names every promoted digest exactly
