@capability:construct-sidefx-semantic-query-plan
@root-scenario:construct-sidefx-semantic-query-plan
Feature: Compile a typed request into one allow-listed semantic query plan

  The query plan is the provider-neutral intermediate representation of the
  SideFX brain. It is not SQL, Cypher, search syntax, or vector-store syntax,
  and no provider may widen it. This capability compiles a typed request into
  exactly one immutable plan after checking it against the digest-bound query
  policy: the mode must be admitted, the graph pattern must be allow-listed,
  every requested relationship kind and the subject kind must belong to that
  pattern, and depth, result limit, and lexical term count must stay inside
  their declared ceilings. A request that fails any check is rejected as a
  typed finding. It is never silently narrowed into a plan that would answer a
  different question.

  @scenario:construct-sidefx-semantic-query-plan
  @input:sidefx-semantic-query-plan-construction-request
  @input-contract:sidefx-semantic-query-plan-construction-request.v1
  @event:sidefx-semantic-query-plan-construction-requested
  @event-authority:construct-sidefx-semantic-query-plan.v1
  @outcome:sidefx-semantic-query-plan-construction-outcome
  @outcome-contract:sidefx-semantic-query-plan-construction-outcome.v1
  @outcome-terminal
  Scenario: Compile an admitted request into one digest-bound plan or reject it
    Given a typed semantic request, a pinned snapshot, and the digest-bound query policy allowances
    When the mode, graph pattern, subject kind, relationship kinds, depth, limit, and lexical term count are checked against those allowances
    Then either one digest-bound provider-neutral plan is constructed or the request is rejected as a typed finding without narrowing it
