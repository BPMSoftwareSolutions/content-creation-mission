@capability:preserve-admitted-projection-on-incomplete-regeneration
@root-scenario:preserve-admitted-projection-on-incomplete-regeneration
# Legacy source: scenario-driven-architecture/tools/src/capabilities/projected-implementation-promotion/preserve-admitted-projection-on-incomplete-regeneration/provider.ts
Feature: Preserve admitted projection on incomplete regeneration

  A language maintainer needs to run projection fearlessly, knowing that an
  incomplete or abandoned regeneration can never lose already-admitted,
  known-good work. The capability compares admitted bytes before and after
  rollback from an incomplete regeneration.

  Previously admitted and untargeted artifacts remain byte-identical after
  rollback; every admitted byte is restored exactly. The capability does
  not attempt regeneration itself — it only verifies that rollback
  preserved what was already admitted.

  @scenario:preserve-admitted-projection-on-incomplete-regeneration
  @input:before-and-after-digest-facts
  @input-contract:preserve-admitted-projection-input.v1
  @event:incomplete-regeneration-abandonment-requested
  @event-authority:admitted-projection-preservation.v1
  @outcome:admitted-projection-preserved
  @outcome-contract:projection-preservation-evidence.v1
  @outcome-terminal
  Scenario: Verify admitted bytes survive an incomplete regeneration
    Given digest facts for admitted bytes before and after a rollback from incomplete regeneration
    When admitted bytes before and after rollback are compared
    Then previously admitted and untargeted artifacts remain byte-identical and every admitted byte is restored exactly
