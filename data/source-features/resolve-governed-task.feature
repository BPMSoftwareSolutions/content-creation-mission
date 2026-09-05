@capability:resolve-governed-task
@root-scenario:resolve-governed-task
Feature: Resolve a governed task through an agentic circuit

  Agentic planning and provider execution participate in the same governed
  scenario circuit as every other capability mechanic. A planner proposes one
  bounded next responsibility, but its proposal is testimony rather than
  execution authority. Tool visibility does not grant authorization, physical
  success does not admit an outcome, and an admitted outcome does not realize
  the promised experience until its obligation closes. Budget, tool, policy,
  approval, testimony, outcome, obligation, experience, and lineage
  dispositions remain canonical and inspectable regardless of which model,
  tool provider, interface profile, or language projection participates.

  The model may vary its wording or candidate path. The circuit does not make
  probabilistic prose deterministic; it makes the authority digest, admitted
  tool surface, approval law, execution budget, transition law, evidence
  requirements, outcome contract, obligation, and promised experience
  deterministic. MCP, conversational, HTTP, CLI, and SDK delivery are
  interface projections over this authority, never alternate semantic owners.

  @scenario:resolve-governed-task
  @input:governed-agent-execution-context
  @input-contract:governed-agent-execution-context.v1
  @event:resolve-governed-agent-step
  @event-authority:resolve-governed-agent-step.v1
  @outcome:governed-agent-execution-testimony
  @outcome-contract:governed-agent-execution-testimony.v1
  @outcome-terminal
  Scenario: Resolve a governed task through one admitted tool
    Given an admitted task, candidate planning testimony, and bounded execution context
    When the next responsible action is admitted and its candidate outcome is evaluated
    Then the requested experience is realized or one governed non-fulfillment disposition is observable with complete execution lineage
