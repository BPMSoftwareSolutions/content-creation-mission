@capability:project-and-prove-semantic-carrier-graph
@root-scenario:project-and-prove-canonical-graph
Feature: Project and prove only canonical graph meaning

  Execute project-and-prove-semantic-carrier-graph from capsule-contained semantic implementation authority through a generic language resolver.

  @scenario:project-and-prove-canonical-graph
  @input:canonical-graph-proof-request
  @input-contract:semantic-carrier-graph-proof-request.v1
  @event:project-and-prove-graph-only-meaning
  @event-authority:project-and-prove-graph-only-meaning.v1
  @outcome:graph-proof-classified
  @outcome-contract:semantic-carrier-graph-proof-result.v1
  Scenario: Project and prove canonical graph
    Given one exact canonical graph after an established carrier-blackout boundary
    When the canonical graph is independently projected and proven without carrier access
    Then the graph-only proof is classified

  @scenario:return-proof-held
  @input:held-proof
  @input-contract:semantic-carrier-graph-proof-result.v1
  @event:bind-proof-held
  @event-authority:bind-proof-held.v1
  @outcome:projection-proof-held
  @outcome-contract:semantic-carrier-graph-proof-result.v1
  @outcome-terminal
  Scenario: Return proof held
    Given an incomplete or divergent graph proof
    When the proof hold receipt is bound
    Then PROJECTION_PROOF_HELD is returned

  @scenario:return-proof-passed
  @input:passed-proof
  @input-contract:semantic-carrier-graph-proof-result.v1
  @event:bind-proof-passed
  @event-authority:bind-proof-passed.v1
  @outcome:proof-passed
  @outcome-contract:semantic-carrier-graph-proof-result.v1
  @outcome-terminal
  Scenario: Return proof passed
    Given a complete graph-bound independent proof set
    When the passed proof receipt is bound
    Then PROOF_PASSED is returned
