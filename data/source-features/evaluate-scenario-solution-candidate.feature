@capability:evaluate-scenario-solution-candidate
@root-scenario:evaluate-scenario-solution-candidate
Feature: Evaluate one scenario solution candidate

  A scenario solution candidate is untrusted testimony. It becomes a scenario
  solution only when every part of it is shown to close the scenario it claims
  to close, using only admitted meaning.

  This capability evaluates one candidate against the scenario it serves and the
  rules that governed its authoring.

  The resulting ScenarioSolution becomes input to composition.

  A candidate that names an identity, mechanic, or capability the authority does
  not admit is held with exact findings rather than repaired.

  @scenario:evaluate-scenario-solution-candidate
  @input:scenario-solution-candidate-evaluation-request
  @input-contract:scenario-solution-candidate-evaluation-request.v1
  @event:evaluate-scenario-solution-candidate
  @event-authority:evaluate-scenario-solution-candidate.v1
  @outcome:evaluated-scenario-solution
  @outcome-contract:evaluated-scenario-solution.v1
  @outcome-terminal
  Scenario: Evaluate one scenario solution candidate
    Given one scenario solution candidate, the scenario candidate it claims to close, and the profile that governed its authoring
    When identity, mechanics, operations, transformations, and platform capability identities are evaluated against admitted authority
    Then the candidate is admitted as one scenario solution, or it is held with exact ordered findings

  @scenario:admit-solution-evaluation-boundary
  @input:scenario-solution-candidate-evaluation-request
  @input-contract:scenario-solution-candidate-evaluation-request.v1
  @event:admit-solution-evaluation-boundary
  @event-authority:admit-solution-evaluation-boundary.v1
  @outcome:admitted-solution-evaluation-boundary
  @outcome-contract:admitted-solution-evaluation-boundary.v1
  @outcome-terminal
  Scenario: Admit the candidate and the authority it is evaluated against
    Given one scenario solution candidate, one scenario candidate, and one authoring profile
    When the candidate, the scenario it claims, and the governing profile are observed without model, network, or clock access
    Then one immutable evaluation boundary fixes what is being evaluated and what it is evaluated against, or the boundary is held with exact findings

  @scenario:evaluate-declared-solution-identities
  @input:admitted-solution-evaluation-boundary
  @input-contract:admitted-solution-evaluation-boundary.v1
  @event:evaluate-declared-solution-identities
  @event-authority:evaluate-declared-solution-identities.v1
  @outcome:evaluated-solution-identities
  @outcome-contract:evaluated-solution-identities.v1
  @outcome-terminal
  Scenario: Evaluate every identity the candidate names
    Given one admitted evaluation boundary carrying the permitted mechanics and permitted platform capability identities
    When the scenario identity, every port platform capability identity, and every transformation operation are compared with admitted authority
    Then each unadmitted identity is named exactly as a finding, and no unadmitted identity is silently accepted or replaced

  @scenario:resolve-scenario-solution-admission
  @input:evaluated-solution-identities
  @input-contract:evaluated-solution-identities.v1
  @event:resolve-scenario-solution-admission
  @event-authority:resolve-scenario-solution-admission.v1
  @outcome:evaluated-scenario-solution
  @outcome-contract:evaluated-scenario-solution.v1
  @outcome-terminal
  Scenario: Resolve whether the candidate closes its scenario
    Given the evaluated identities and the declared outcome the scenario requires
    When completeness of execution authority, operations, and transformations is resolved together with every identity finding
    Then the candidate is SCENARIO_SOLUTION_ADMITTED and becomes one scenario solution, or it is SCENARIO_SOLUTION_HELD carrying every finding in stable order
