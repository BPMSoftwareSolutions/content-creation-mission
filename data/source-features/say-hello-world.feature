@capability:say-hello-world
@root-scenario:say-hello-world
Feature: Say the canonical Hello World greeting

  A caller with no domain input must receive one exact deterministic greeting.

  @scenario:say-hello-world
  @input:hello-world-request
  @input-contract:hello-world-request.v1
  @event:say-hello-world
  @event-authority:say-hello-world.v1
  @outcome:hello-world-greeting
  @outcome-contract:hello-world-greeting.v1
  @outcome-terminal
  Scenario: Say Hello World without domain input
    Given no domain input
    When the canonical Hello World greeting is requested
    Then the exact greeting is Hello, World!
