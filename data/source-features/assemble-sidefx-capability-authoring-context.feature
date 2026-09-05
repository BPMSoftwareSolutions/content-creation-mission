@capability:assemble-sidefx-capability-authoring-context
@root-scenario:assemble-sidefx-capability-authoring-context
Feature: Assemble the smallest sufficient authoring context

  A context pack is a promise about what an author was allowed to see. This
  capability assembles one from admitted items only, under a fixed budget in
  both item count and size, and binds every item to its exact source locator,
  its content digest, and its citation label. Whatever the budget removes is
  recorded as an explicit omission rather than silently dropped, and whatever
  was excluded from consideration is carried through as a declared exclusion.
  A pack that would exceed its size budget, or that is missing a purpose the
  stage requires, is HELD with the reason attached: an incomplete pack is never
  emitted as though it were sufficient.

  @scenario:assemble-sidefx-capability-authoring-context
  @input:sidefx-authoring-context-request
  @input-contract:sidefx-authoring-context-request.v1
  @event:sidefx-authoring-context-requested
  @event-authority:assemble-sidefx-capability-authoring-context.v1
  @outcome:sidefx-capability-authoring-context-pack
  @outcome-contract:sidefx-capability-authoring-context-pack.v1
  @outcome-terminal
  Scenario: Bind a budgeted, cited, digest-bound pack or hold it
    Given admitted candidate items, declared exclusions, required purposes, and a fixed item and size budget
    When items are admitted in declared order until the budget is reached and the required purposes are checked
    Then one digest-bound pack cites every item and lists every omission, or the pack is HELD with the reason it could not be assembled
