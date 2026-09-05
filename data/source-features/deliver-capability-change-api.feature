@capability:deliver-capability-change-api
@root-scenario:deliver-capability-change-api
Feature: Deliver capability change management through the SideFX API

  An authorized local consumer uses declared change-management resources while
  open, seal, publish, and observe capabilities retain all lifecycle meaning.
  API delivery owns protocol carriers, route selection, bounded request state,
  response representation, and exact protocol failures only.

  The API never reimplements the change circuit, infers authorization, stores
  credentials in change authority, or reports an operation as complete before
  the bound capability returns its governed disposition.

  @scenario:deliver-capability-change-api
  @input:capability-change-api-delivery-request
  @input-contract:capability-change-api-delivery-request.v1
  @event:capability-change-api-delivery-requested
  @event-authority:deliver-capability-change-api.v1
  @outcome:capability-change-api-delivery-result
  @outcome-contract:capability-change-api-delivery-result.v1
  @outcome-terminal
  Scenario: Deliver the declared change management API
    Given admitted route authority and bindings to open, seal, publish, and observe capability change operations
    When API delivery is requested
    Then only declared method and resource pairs accept bounded carriers and delegate to the exact bound capability operation

  @scenario:open-capability-change-through-api
  @input:capability-change-api-operation-request
  @input-contract:capability-change-api-operation-request.v1
  @event:capability-change-api-open-requested
  @event-authority:open-capability-change-through-api.v1
  @outcome:capability-change-api-operation-result
  @outcome-contract:capability-change-api-operation-result.v1
  @outcome-terminal
  Scenario: Open a change through the declared collection resource
    Given one bounded capability identity and reason reference
    When the declared change collection creation operation is requested
    Then the request delegates to open-capability-change and returns the governed OPEN or held representation without API-owned lifecycle meaning

  @scenario:transition-capability-change-through-api
  @input:capability-change-api-operation-request
  @input-contract:capability-change-api-operation-request.v1
  @event:capability-change-api-transition-requested
  @event-authority:transition-capability-change-through-api.v1
  @outcome:capability-change-api-operation-result
  @outcome-contract:capability-change-api-operation-result.v1
  @outcome-terminal
  Scenario: Seal or publish a change through declared transition resources
    Given one exact change identity and one declared seal or publish transition
    When the transition resource is requested
    Then the request delegates only to seal-capability-change or publish-capability-change and preserves its governed disposition and evidence

  @scenario:observe-capability-change-through-api
  @input:capability-change-api-operation-request
  @input-contract:capability-change-api-operation-request.v1
  @event:capability-change-api-status-requested
  @event-authority:observe-capability-change-through-api.v1
  @outcome:capability-change-api-operation-result
  @outcome-contract:capability-change-api-operation-result.v1
  @outcome-terminal
  Scenario: Observe a change through its declared resource
    Given one exact change identity
    When the declared change status resource is requested
    Then the request delegates to observe-capability-change and returns its read-only governed status without creating mutable API authority

  @scenario:represent-capability-change-api-failure
  @input:capability-change-api-failure
  @input-contract:capability-change-api-failure.v1
  @event:capability-change-api-failure-representation-requested
  @event-authority:represent-capability-change-api-failure.v1
  @outcome:capability-change-api-delivery-result
  @outcome-contract:capability-change-api-delivery-result.v1
  @outcome-terminal
  Scenario: Represent protocol and governed failures distinctly
    Given an undeclared route, malformed carrier, unknown change, unauthorized effect, or held capability operation
    When the API failure is represented
    Then the exact protocol or governed disposition and evidence are returned without retry, fallback, inferred mutation, or server-owned semantic repair

