@capability:retrieve-sidefx-semantic-candidates
@root-scenario:retrieve-sidefx-semantic-candidates
Feature: Retrieve semantic candidates in fixed channel order

  Retrieval returns candidates, never facts. This capability executes the three
  deterministic channels of one admitted plan in the order the query policy
  fixes: exact canonical identity first, then bounded traversal of the admitted
  relationship graph over allow-listed edge kinds and direction within the
  plan depth, then substring recall over the versioned lexical index. Exact
  identity outranks every other channel and a candidate already returned by a
  stronger channel is never repeated by a weaker one. The optional vector
  channel consumes only a full provider/model/input/index/record testimony whose
  record digest and corpus generation reproduce; disabled plans retain a null
  testimony and ignore any supplied vector data. Vector order and score belong
  to the admitted provider, while deterministic channels retain catalog order. A plan whose
  snapshot does not match the supplied generation retrieves nothing and reports
  a typed mixed-generation finding.

  @scenario:retrieve-sidefx-semantic-candidates
  @input:sidefx-semantic-candidate-retrieval-request
  @input-contract:sidefx-semantic-candidate-retrieval-request.v1
  @event:sidefx-semantic-candidate-retrieval-requested
  @event-authority:retrieve-sidefx-semantic-candidates.v1
  @outcome:sidefx-semantic-candidate-set
  @outcome-contract:sidefx-semantic-candidate-set.v1
  @outcome-terminal
  Scenario: Execute exact, graph, lexical, and optional vector channels in fixed policy order
    Given one admitted plan, the pinned identity and lexical indexes, the admitted relationship graph, and optional digest-bound vector testimony
    When the exact, graph, lexical, and enabled vector channels run in policy order within the declared depth and result limit
    Then one digest-bound candidate set carries channel-attributed candidates in catalog order and asserts no fact about them
