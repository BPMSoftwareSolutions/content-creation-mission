@capability:resolve-scenario-reinforcing-fit
@root-scenario:resolve-scenario-reinforcing-fit
Feature: Resolve one scenario reinforcing fit signal

  Execution testifies. Interpretation evaluates. Governance decides.

  This capability owns the first step of the meaning-return circuit. Its
  input is one admitted scenario outcome receipt, the capability's
  declared intent, and one governed fit relation from the domain
  vocabulary authority. Its outcome is one domain-language fit signal.
  The dispositions are conservative and exact: REINFORCES,
  DOES_NOT_REINFORCE, NOT_OBSERVABLE, or NOT_APPLICABLE. A fit signal
  never changes configuration, never re-pins bindings, and never
  self-reinforces: it is forward-looking validation for product,
  portfolio, and strategy responsibilities downstream. Evidence may be
  technical; the reinforcing meaning must resolve into the governed
  vocabulary of the consuming semantic altitude.

  @scenario:resolve-scenario-reinforcing-fit
  @input:scenario-reinforcing-fit-record
  @input-contract:scenario-reinforcing-fit-record.v1
  @event:scenario-reinforcing-fit-resolution-requested
  @event-authority:resolve-scenario-reinforcing-fit.v1
  @outcome:scenario-reinforcing-fit-record
  @outcome-contract:scenario-reinforcing-fit-record.v1
  @outcome-terminal
  Scenario: Resolve one scenario reinforcing fit signal
    Given one admitted scenario outcome receipt, one declared capability intent, and one governed fit relation
    When the reinforcing fit of the observed outcome is resolved
    Then one domain-language fit signal is available with disposition REINFORCES, DOES_NOT_REINFORCE, NOT_OBSERVABLE, or NOT_APPLICABLE, and the signal changes nothing

  @scenario:admit-outcome-receipt
  @input:scenario-reinforcing-fit-record
  @input-contract:scenario-reinforcing-fit-record.v1
  @event:outcome-receipt-admission-requested
  @event-authority:admit-outcome-receipt.v1
  @outcome:scenario-reinforcing-fit-record
  @outcome-contract:scenario-reinforcing-fit-record.v1
  @outcome-terminal
  Scenario: Admit the outcome receipt against the observed outcome identity
    Given one outcome receipt digest, one observed outcome identity, and one observed outcome digest
    When receipt admission is evaluated
    Then the receipt is bound and the observed outcome digest matches the expected outcome digest, reporting RECEIPT_NOT_BOUND or OUTCOME_DIVERGED otherwise

  @scenario:evaluate-declared-fit-relation
  @input:scenario-reinforcing-fit-record
  @input-contract:scenario-reinforcing-fit-record.v1
  @event:declared-fit-relation-evaluation-requested
  @event-authority:evaluate-declared-fit-relation.v1
  @outcome:scenario-reinforcing-fit-record
  @outcome-contract:scenario-reinforcing-fit-record.v1
  @outcome-terminal
  Scenario: Evaluate the declared fit relation over the observed outcome
    Given one declared fit relation with a technical condition and one observed condition outcome
    When the fit relation is evaluated
    Then the technical condition observation and the outcome match determine reinforcement, reporting CONDITION_NOT_OBSERVED otherwise

  @scenario:project-domain-fit-statement
  @input:scenario-reinforcing-fit-record
  @input-contract:scenario-reinforcing-fit-record.v1
  @event:domain-fit-statement-projection-requested
  @event-authority:project-domain-fit-statement.v1
  @outcome:scenario-reinforcing-fit-record
  @outcome-contract:scenario-reinforcing-fit-record.v1
  @outcome-terminal
  Scenario: Project the domain fit statement under the admitted mapping
    Given one admitted fit relation from the domain vocabulary authority and one scenario identity
    When domain statement projection is evaluated
    Then the domain statement is present under an admitted mapping that applies to the scenario, reporting MAPPING_NOT_ADMITTED, MAPPING_SCOPE_NOT_APPLICABLE, or DOMAIN_STATEMENT_ABSENT otherwise

  @scenario:bind-fit-signal-receipt
  @input:scenario-reinforcing-fit-record
  @input-contract:scenario-reinforcing-fit-record.v1
  @event:fit-signal-receipt-binding-requested
  @event-authority:bind-fit-signal-receipt.v1
  @outcome:scenario-reinforcing-fit-record
  @outcome-contract:scenario-reinforcing-fit-record.v1
  @outcome-terminal
  Scenario: Bind one fit signal receipt
    Given one resolved fit signal with disposition and domain statement
    When the signal receipt is bound
    Then the capability identity, scenario identity, observed outcome identity, outcome receipt digest, fit authority, domain statement, and disposition bind into one replayable fit signal receipt
