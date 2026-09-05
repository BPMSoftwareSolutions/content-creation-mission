@capability:realize-node-execute-bounded-process
@root-scenario:realize-node-execute-bounded-process
Feature: Realize the admitted bounded-process mechanic on Node

  The Node projection target realizes the already admitted
  execute-bounded-process mechanic without creating capability meaning in the
  runtime. The provider executes one authority-selected executable without a
  shell, inside an admitted working root, with explicit time and output bounds.
  It returns digest-bound process testimony and never treats a zero exit as
  capability acceptance.

  @scenario:realize-node-execute-bounded-process
  @input:bounded-process-execution-request
  @input-contract:mechanic:execute-bounded-process:input.v1
  @event:execute-bounded-process
  @event-authority:execute-bounded-process.v1
  @outcome:bounded-process-execution-testimony
  @outcome-contract:mechanic:execute-bounded-process:outcome.v1
  @outcome-terminal
  Scenario: Execute one admitted process and bind bounded testimony
    Given an admitted executable, arguments, working directory, timeout, and output bound
    When Node spawns the executable without a shell and observes its bounded completion
    Then digest-bound stdout and stderr testimony identifies exactly one terminal disposition without claiming capability acceptance

  @scenario:admit-bounded-process-execution-request
  @input:bounded-process-execution-request
  @input-contract:mechanic:execute-bounded-process:input.v1
  @event:admit-bounded-process-execution-request
  @event-authority:admit-bounded-process-execution-request.v1
  @outcome:bounded-process-request-disposition
  @outcome-contract:bounded-process-request-disposition.v1
  Scenario: Reject an unbounded or unauthorised process request before effects
    Given a candidate bounded-process request
    When executable authority, arguments, root containment, timeout, and output bounds are validated
    Then the request becomes REQUEST_ADMITTED or REQUEST_REJECTED and a rejected request performs no process effect

  @scenario:invoke-node-child-process
  @input:admitted-bounded-process-request
  @input-contract:admitted-bounded-process-request.v1
  @event:invoke-node-child-process
  @event-authority:node-child-process-spawn.v1
  @outcome:raw-bounded-process-observation
  @outcome-contract:raw-bounded-process-observation.v1
  Scenario: Spawn one process without a command shell
    Given one admitted request rooted inside the projected application boundary
    When node child_process spawn is invoked with shell false and bounded pipes
    Then one completion, error, timeout, cancellation, or output-limit observation returns and all listeners settle exactly once

  @scenario:bind-bounded-process-execution-testimony
  @input:raw-bounded-process-observation
  @input-contract:raw-bounded-process-observation.v1
  @event:bind-bounded-process-execution-testimony
  @event-authority:bind-bounded-process-execution-testimony.v1
  @outcome:bounded-process-execution-testimony
  @outcome-contract:mechanic:execute-bounded-process:outcome.v1
  @outcome-terminal
  Scenario: Bind process evidence without upgrading it to semantic success
    Given one raw bounded process observation
    When executable, argument, output, exit, signal, timeout, and effect-lineage testimony is bound
    Then the outcome is EXITED_ZERO, EXITED_NONZERO, TIMED_OUT, RUNTIME_UNAVAILABLE, OUTPUT_LIMIT_EXCEEDED, or CANCELLED and acceptance remains NOT_CLAIMED
