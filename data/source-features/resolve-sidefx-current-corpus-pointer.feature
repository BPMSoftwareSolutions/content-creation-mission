@capability:resolve-sidefx-current-corpus-pointer
@root-scenario:resolve-sidefx-current-corpus-pointer
Feature: Resolve the current SideFX semantic corpus pointer

  The pointer is the single mutable environment fact per (estate,
  environment, corpus) scope. It is resolved before query planning, so an
  in-flight query stays pinned even when the environment advances. This
  capability is read-only: it carries no pointer-write authority and read
  consumers receive none. Every scenario admits and emits one shared
  pointer resolution record.

  @scenario:resolve-sidefx-current-corpus-pointer
  @input:sidefx-current-pointer-resolution-record
  @input-contract:sidefx-current-pointer-resolution-record.v1
  @event:sidefx-current-pointer-resolution-requested
  @event-authority:resolve-sidefx-current-corpus-pointer.v1
  @outcome:sidefx-current-pointer-resolution-record
  @outcome-contract:sidefx-current-pointer-resolution-record.v1
  @outcome-terminal
  Scenario: Resolve the pinned snapshot for the current generation
    Given one declared pointer scope and an admitted current-pointer policy
    When the pointer is resolved through the declared store port
    Then one digest-bound pointer records scope, generation, snapshot digest, and the prior generation with a complete resolution receipt

  @scenario:report-absent-pointer-scope-not-observable
  @input:sidefx-current-pointer-resolution-record
  @input-contract:sidefx-current-pointer-resolution-record.v1
  @event:absent-sidefx-pointer-scope-resolution-requested
  @event-authority:report-absent-sidefx-pointer-scope.v1
  @outcome:sidefx-current-pointer-resolution-record
  @outcome-contract:sidefx-current-pointer-resolution-record.v1
  @outcome-terminal
  Scenario: Report a scope with no admitted generation as not observable
    Given a declared scope whose pointer generation cannot be observed
    When the pointer is resolved
    Then the resolution is NOT_OBSERVABLE and no generation or snapshot is invented

  @scenario:refuse-undeclared-pointer-scope
  @input:sidefx-current-pointer-resolution-record
  @input-contract:sidefx-current-pointer-resolution-record.v1
  @event:undeclared-sidefx-pointer-scope-resolution-requested
  @event-authority:refuse-undeclared-sidefx-pointer-scope.v1
  @outcome:sidefx-current-pointer-resolution-record
  @outcome-contract:sidefx-current-pointer-resolution-record.v1
  @outcome-terminal
  Scenario: Refuse a scope outside the declared scope authority
    Given a pointer scope that the admitted scope authority does not declare
    When the pointer is resolved
    Then the resolution is REJECTED with a named scope finding and no pointer authority is exercised
