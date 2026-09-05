@capability:author-one-scenario-candidate
@root-scenario:author-one-scenario-candidate
Feature: Author the meaning of one declared scenario

  A governed authoring conveyor holds one admitted capability meaning and one
  declared scenario identity taken from an admitted canonical feature. It needs
  the meaning of that single scenario, and nothing else.

  This capability authors scenario meaning at scenario altitude. It answers only
  what comes in, what happens, and what becomes true. Input, event, and outcome
  remain distinct fields; an outcome is never collapsed into a technical
  representation of the event that produced it.

  The scenario identity, its declared connectors, and its declared contracts are
  supplied by the admitted feature and are never invented, renamed, widened, or
  reinterpreted here. This capability does not decide which scenarios exist.

  Scenario meaning may reference a lower-altitude identity through a governed
  reference, but it never owns lower-altitude meaning. Operations,
  transformations, bindings, ports, provider identities, transports,
  serializations, runtimes, and physical mechanisms are forbidden as scenario
  meaning. Where such content appears in testimony it is returned as an exact
  altitude finding rather than silently rewritten into acceptable language.

  Model output remains untrusted testimony. Authoring one scenario candidate
  establishes no contract admission, behavioral conformance, projection, or
  promotion, and never claims acceptance.

  @scenario:author-one-scenario-candidate
  @input:bounded-scenario-meaning-request
  @input-contract:bounded-scenario-meaning-request.v1
  @event:author-one-scenario-candidate
  @event-authority:author-one-scenario-candidate.v1
  @outcome:scenario-authoring-outcome
  @outcome-contract:scenario-authoring-outcome.v1
  @outcome-terminal
  Scenario: Author one scenario candidate
    Given one admitted capability meaning and one declared scenario identity with its connectors
    When the meaning of that single scenario is authored at scenario altitude
    Then one scenario candidate carrying its input, event, outcome, responsibility, and obligation is returned as untrusted testimony without acceptance claims

  @scenario:admit-scenario-meaning-boundary
  @input:bounded-scenario-meaning-request
  @input-contract:bounded-scenario-meaning-request.v1
  @event:admit-scenario-meaning-boundary
  @event-authority:admit-scenario-meaning-boundary.v1
  @outcome:admitted-scenario-meaning-boundary
  @outcome-contract:admitted-scenario-meaning-boundary.v1
  @outcome-terminal
  Scenario: Admit the bounded scenario authoring boundary
    Given one capability meaning, one declared scenario identity, its declared connectors, and the scenario-altitude vocabulary authority
    When the identity, connector completeness, capability-meaning admission, and vocabulary authority digest are evaluated
    Then one immutable scenario authoring boundary fixes the single identity under authorship, or the boundary is held with exact findings

  @scenario:construct-scenario-meaning-request
  @input:admitted-scenario-meaning-boundary
  @input-contract:admitted-scenario-meaning-boundary.v1
  @event:construct-scenario-meaning-request
  @event-authority:construct-scenario-meaning-request.v1
  @outcome:bounded-scenario-meaning-invocation
  @outcome-contract:bounded-scenario-meaning-invocation.v1
  @outcome-terminal
  Scenario: Construct the altitude-bounded scenario meaning request
    Given one admitted scenario authoring boundary and the scenario-altitude vocabulary authority
    When the target altitude, admitted upstream meaning, permitted concepts, referable lower altitudes, forbidden ownership, and the single requested product are bound into one request
    Then one bounded invocation asks for exactly one scenario meaning and carries no obligation belonging to another scenario or another altitude

  @scenario:obtain-scenario-meaning-testimony
  @input:bounded-scenario-meaning-invocation
  @input-contract:bounded-scenario-meaning-invocation.v1
  @event:obtain-scenario-meaning-testimony
  @event-authority:obtain-scenario-meaning-testimony.v1
  @outcome:scenario-meaning-testimony
  @outcome-contract:scenario-meaning-testimony.v1
  @outcome-terminal
  Scenario: Obtain bounded scenario meaning testimony
    Given one bounded scenario meaning invocation under a declared provider authority
    When the governed request is issued once without provider substitution
    Then exact scenario meaning testimony and its request and response lineage are observed as untrusted evidence, or an attributable failure disposition is returned

  @scenario:resolve-scenario-candidate-disposition
  @input:scenario-meaning-testimony
  @input-contract:scenario-meaning-testimony.v1
  @event:resolve-scenario-candidate-disposition
  @event-authority:resolve-scenario-candidate-disposition.v1
  @outcome:scenario-authoring-outcome
  @outcome-contract:scenario-authoring-outcome.v1
  @outcome-terminal
  Scenario: Resolve the scenario candidate against its altitude
    Given one scenario meaning testimony bound to one declared scenario identity
    When declared identity preservation, input, event, and outcome completeness, and scenario-altitude concept closure are evaluated against the admitted vocabulary authority
    Then the scenario candidate is conformant, or it is held with exact findings naming each lower-altitude ownership, higher-altitude claim, and unbound concept without rewriting the testimony
