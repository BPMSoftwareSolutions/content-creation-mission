@capability:bind-sidefx-semantic-query-receipt
@root-scenario:bind-sidefx-semantic-query-receipt
Feature: Bind one replayable receipt to the basis of every answer

  Every exit from the brain carries a receipt, whether it grounded or abstained.
  This capability canonicalizes the complete answer basis into one digest: the
  request, the plan, the pinned snapshot, the catalog, the relationship graph,
  every index consulted, the complete optional vector testimony, the candidate
  set, the grounded result, and the policy.
  It also checks that the receipt is honest about itself. A grounded answer must
  cite at least one exact source locator, an answer that was not found must cite
  none, and the indexes actually consulted must all be bound. A receipt that
  fails those checks is still issued, because suppressing it would hide what
  happened, but it is marked as an incomplete basis and carries the reason.

  @scenario:bind-sidefx-semantic-query-receipt
  @input:sidefx-semantic-query-receipt-binding-request
  @input-contract:sidefx-semantic-query-receipt-binding-request.v1
  @event:sidefx-semantic-query-receipt-binding-requested
  @event-authority:bind-sidefx-semantic-query-receipt.v1
  @outcome:sidefx-semantic-query-receipt
  @outcome-contract:sidefx-semantic-query-receipt.v1
  @outcome-terminal
  Scenario: Canonicalize and digest the complete basis of one answer
    Given the request, plan, snapshot, catalog, graph, index, optional vector testimony, candidate, result, and policy digests of one answer
    When the basis is checked for citation honesty and index completeness and then canonicalized
    Then one digest-bound receipt replays that exact basis and declares whether the basis was complete
