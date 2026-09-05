@capability:execute-admitted-capability
@root-scenario:execute-admitted-capability
Feature: Execute one admitted capability realization for one scenario input

  Packaging preserves capability identity. Revelation exposes capability
  meaning. Realization binds capability meaning to an execution
  environment. Execution produces the effect.

  This capability owns execution — the last link. Its input is one
  conforming capability realization and one scenario input. Its outcome
  is the established effect or a governed disposition: the input admits
  against the declared scenario contract, the declared graph executes,
  the outcome admits against the declared outcome contract, testimony is
  emitted bound to the realization digest, and the execution receipt is
  replayable. Execution never claims more than the realization declared.
  Every scenario admits and emits one shared execution record.

  @scenario:execute-admitted-capability
  @input:capability-execution-record
  @input-contract:capability-execution-record.v1
  @event:capability-execution-requested
  @event-authority:execute-admitted-capability.v1
  @outcome:capability-execution-record
  @outcome-contract:capability-execution-record.v1
  @outcome-terminal
  Scenario: Execute one realization for one scenario input
    Given one conforming realization digest, one scenario identity, and one scenario input
    When the capability is executed
    Then the effect is established or a governed disposition is returned, and the execution receipt binds realization, scenario, input, outcome, and disposition

  @scenario:admit-scenario-input
  @input:capability-execution-record
  @input-contract:capability-execution-record.v1
  @event:scenario-input-admission-requested
  @event-authority:admit-scenario-input.v1
  @outcome:capability-execution-record
  @outcome-contract:capability-execution-record.v1
  @outcome-terminal
  Scenario: Admit the scenario input against the declared contract
    Given one scenario input and the realization's declared input contract
    When input admission is evaluated
    Then the input is admitted or rejected with INPUT_ADMISSION_REJECTED, and a rejected input never reaches execution

  @scenario:execute-declared-graph
  @input:capability-execution-record
  @input-contract:capability-execution-record.v1
  @event:declared-graph-execution-requested
  @event-authority:execute-declared-graph.v1
  @outcome:capability-execution-record
  @outcome-contract:capability-execution-record.v1
  @outcome-terminal
  Scenario: Execute the declared graph for the admitted input
    Given one admitted input and the realization's declared graph
    When the graph is executed
    Then execution is reported as completed or failed with EXECUTION_FAILED, and a failed execution never produces an outcome claim

  @scenario:admit-outcome-and-emit-testimony
  @input:capability-execution-record
  @input-contract:capability-execution-record.v1
  @event:outcome-admission-and-testimony-emission-requested
  @event-authority:admit-outcome-and-emit-testimony.v1
  @outcome:capability-execution-record
  @outcome-contract:capability-execution-record.v1
  @outcome-terminal
  Scenario: Admit the observed outcome and emit bound testimony
    Given one observed outcome and the realization's declared outcome contract
    When outcome admission and testimony emission are evaluated
    Then the outcome admits or reports OUTCOME_ADMISSION_REJECTED, and testimony is bound to the realization digest without claiming more than the realization declared

  @scenario:bind-execution-receipt
  @input:capability-execution-record
  @input-contract:capability-execution-record.v1
  @event:execution-receipt-binding-requested
  @event-authority:bind-execution-receipt.v1
  @outcome:capability-execution-record
  @outcome-contract:capability-execution-record.v1
  @outcome-terminal
  Scenario: Bind one replayable execution receipt
    Given one completed execution with disposition and outcome
    When the receipt is bound
    Then the realization digest, scenario identity, input digest, outcome digest, and disposition bind into one replayable receipt
