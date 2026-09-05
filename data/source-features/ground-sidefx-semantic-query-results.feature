@capability:ground-sidefx-semantic-query-results
@root-scenario:ground-sidefx-semantic-query-results
Feature: Ground retrieved candidates against admitted authority and evidence

  A candidate becomes an answer only here. This capability resolves every
  retrieved candidate against the pinned object catalog and the admitted
  relationship graph, and gives each one exactly one grounding disposition.
  Only canonical authority and admitted evidence ground a result. Projection
  evidence proves embodiment and is refused as meaning. An unsupported source
  and an unresolvable candidate are named as such rather than dropped. When the
  plan requires evidence and none is attributable, the result is NOT_OBSERVABLE:
  missing proof is never collapsed into failed proof. The overall answer
  abstains with INSUFFICIENT_AUTHORITY when nothing grounds, reports NOT_FOUND
  when nothing was retrieved, and returns QUERY_REJECTED when retrieval itself
  was refused.

  @scenario:ground-sidefx-semantic-query-results
  @input:sidefx-semantic-grounding-request
  @input-contract:sidefx-semantic-grounding-request.v1
  @event:sidefx-semantic-grounding-requested
  @event-authority:ground-sidefx-semantic-query-results.v1
  @outcome:sidefx-semantic-grounded-result
  @outcome-contract:sidefx-semantic-grounded-result.v1
  @outcome-terminal
  Scenario: Resolve candidates into grounded results or a typed abstention
    Given one candidate set, the pinned catalog objects, and the admitted relationship graph
    When each candidate is resolved for canonical identity, source class, and attributable evidence
    Then every candidate carries exactly one grounding disposition and the answer grounds or abstains without inventing authority
