@capability:prove-mechanical-sterility
@root-scenario:prove-mechanical-sterility
# Legacy source: scenario-driven-architecture/tools/src/capabilities/consumer-assurance/prove-mechanical-sterility/provider.ts
Feature: Prove mechanical sterility

  A consumer needs to know that generated code has not silently acquired
  hidden domain meaning. The capability inspects projected executable seams
  for unauthorized mechanics.

  Every projected artifact is mechanical, or carries a precise violation
  naming what was found; projected executable seams contain no hidden
  domain mechanics. The capability does not repair or reject a publication
  itself — it only makes hidden mechanics visible wherever they exist.

  @scenario:prove-mechanical-sterility
  @input:projected-artifacts-and-sterility-rules
  @input-contract:prove-mechanical-sterility-input.v1
  @event:mechanical-sterility-proof-requested
  @event-authority:consumer-mechanical-sterility-proof.v1
  @outcome:mechanical-sterility-known
  @outcome-contract:mechanical-sterility-evidence.v1
  @outcome-terminal
  Scenario: Inspect projected executable seams for unauthorized mechanics
    Given a set of projected artifacts and the admitted sterility rules
    When projected executable seams are inspected for unauthorized mechanics
    Then every projected artifact is mechanical or carries a precise violation, and no hidden domain mechanic remains undetected
