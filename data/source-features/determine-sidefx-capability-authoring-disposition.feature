@capability:determine-sidefx-capability-authoring-disposition
@root-scenario:determine-sidefx-capability-authoring-disposition
Feature: Prefer reuse, composition, and profile before new identity

  New identity is the most expensive semantic act, so it is the last one this
  capability will reach for. The decision walks a fixed ladder: reuse an
  admitted identity, else compose admitted objects, else profile an admitted
  pattern, and only then author something new. AUTHOR_NEW is permitted only
  when nothing above it closes the request and the novel semantic delta, the
  required proof obligations, and the required source authorities are all
  explicitly declared. When those requirements are incomplete the decision is
  HELD rather than defaulted downward into new identity, and an unbound policy
  is HELD too. Every outcome states the reason it was reached and binds a
  decision receipt.

  @scenario:determine-sidefx-capability-authoring-disposition
  @input:sidefx-authoring-disposition-request
  @input-contract:sidefx-authoring-disposition-request.v1
  @event:sidefx-authoring-disposition-requested
  @event-authority:determine-sidefx-capability-authoring-disposition.v1
  @outcome:sidefx-capability-authoring-disposition
  @outcome-contract:sidefx-capability-authoring-disposition.v1
  @outcome-terminal
  Scenario: Walk the reuse-first ladder and hold rather than default to new identity
    Given a classified precedent set, pattern candidates, declared composables, and the digest-bound authoring policy
    When reuse, composition, profile, and new identity are considered in that fixed order
    Then the earliest closing disposition is returned with its reason and receipt, and an unjustified new identity is HELD instead
