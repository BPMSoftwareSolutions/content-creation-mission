@capability:author-one-scenario-solution
@root-scenario:author-one-scenario-solution
Feature: Author the solution for one admitted scenario

  A governed authoring conveyor holds one admitted scenario candidate whose
  input, event, and outcome meaning is already fixed. It needs the semantic
  solution that establishes that declared outcome, and nothing else.

  This capability authors solution meaning at execution altitude. It answers
  only which semantic operations, transformations, and binding requirements
  close the scenario it was given. The scenario meaning is upstream authority
  here: it is consumed, never restated, widened, narrowed, or reinterpreted.

  A solution decomposes responsibility. It may declare operations,
  transformations, projections, branches, and the port requirements an
  operation depends on, and it may reference a provider identity through a
  governed reference. It never owns provider selection or physical mechanism.
  Concrete provider names, endpoints, credentials, transports, containers,
  sockets, and runtime mechanics are forbidden as solution meaning.

  A solution that cannot be established from the admitted scenario outcome is
  held with exact findings. Absent authority is never invented to make a
  scenario appear closed, and no operation is proposed whose outcome the
  declared scenario does not require.

  A governed response whose structured content cannot be admitted is an
  attributable representation finding, never an execution abort. Ambiguous
  provider testimony is never silently curated: unadmissible structured
  content is reported exactly with its raw response digest, request digest,
  provider identity, attempt identity, finish reason, representation
  disposition, and the exact admission defect, and no testimony is repaired
  or dropped without that finding.

  Model output remains untrusted testimony. Authoring one scenario solution
  establishes no contract admission, behavioral conformance, projection, or
  promotion, and never claims acceptance.

  @scenario:author-one-scenario-solution
  @input:bounded-scenario-solution-request
  @input-contract:bounded-scenario-solution-request.v1
  @event:author-one-scenario-solution
  @event-authority:author-one-scenario-solution.v1
  @outcome:solution-authoring-outcome
  @outcome-contract:solution-authoring-outcome.v2
  @outcome-terminal
  Scenario: Author one scenario solution candidate
    Given one admitted scenario candidate with fixed input, event, and outcome meaning
    When the semantic solution that establishes that declared outcome is authored at execution altitude
    Then one scenario solution candidate carrying its execution authority, operations, transformations, and port requirements, or one attributable finding disposition, is returned as untrusted testimony without acceptance claims

  @scenario:admit-scenario-solution-boundary
  @input:bounded-scenario-solution-request
  @input-contract:bounded-scenario-solution-request.v1
  @event:admit-scenario-solution-boundary
  @event-authority:admit-scenario-solution-boundary.v1
  @outcome:admitted-scenario-solution-boundary
  @outcome-contract:admitted-scenario-solution-boundary.v1
  @outcome-terminal
  Scenario: Admit the bounded scenario solution boundary
    Given one admitted scenario candidate, its declared outcome obligation, and the execution-altitude vocabulary authority
    When scenario candidate admission, outcome obligation completeness, and vocabulary authority digest are evaluated
    Then one immutable solution authoring boundary fixes the single scenario being closed, or the boundary is held with exact findings

  @scenario:construct-scenario-solution-request
  @input:admitted-scenario-solution-boundary
  @input-contract:admitted-scenario-solution-boundary.v1
  @event:construct-scenario-solution-request
  @event-authority:construct-scenario-solution-request.v1
  @outcome:bounded-scenario-solution-invocation
  @outcome-contract:bounded-scenario-solution-invocation.v1
  @outcome-terminal
  Scenario: Construct the altitude-bounded scenario solution request
    Given one admitted solution authoring boundary and the execution-altitude vocabulary authority
    When the target altitude, admitted scenario meaning, permitted concepts, referable lower altitudes, forbidden ownership, and the single requested product are bound into one request
    Then one bounded invocation asks for exactly one scenario solution and carries no obligation to author scenario meaning, provider selection, or physical mechanism

  @scenario:obtain-scenario-solution-testimony
  @input:bounded-scenario-solution-invocation
  @input-contract:bounded-scenario-solution-invocation.v1
  @event:obtain-scenario-solution-testimony
  @event-authority:obtain-scenario-solution-testimony.v1
  @outcome:solution-authoring-outcome
  @outcome-contract:solution-authoring-outcome.v2
  @outcome-terminal
  Scenario: Obtain bounded scenario solution testimony
    Given one bounded scenario solution invocation under a declared provider authority, and the returned provider testimony carrying its raw response digest when the governed exchange returns
    When the governed request is issued once without provider substitution and the returned structured content is admitted against the declared response shape
    Then exact scenario solution testimony and its request and response lineage are observed as untrusted evidence, or an attributable failure disposition is returned — including an exact representation finding carrying the raw response digest, request digest, provider identity, attempt identity, finish reason, and the admitted invocation identity when the returned structured content cannot be admitted, never an execution abort and never a silently repaired or dropped payload
