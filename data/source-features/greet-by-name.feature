@capability:greet-by-name
@root-scenario:greet-by-name
Feature: Construct a greeting from one name input

  A caller supplies one admitted name and receives one deterministic personalized greeting without an external effect.

  @scenario:greet-by-name
  @input:personal-greeting-request
  @input-contract:personal-greeting-request.v1
  @event:greet-by-name
  @event-authority:greet-by-name.v1
  @outcome:personal-greeting
  @outcome-contract:personal-greeting.v1
  @outcome-terminal
  Scenario: Greet a caller by name
    Given one admitted non-empty person name
    When a personalized greeting is requested
    Then the exact greeting Hello, {name}! is returned without an external effect
