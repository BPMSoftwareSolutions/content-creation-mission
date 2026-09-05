@capability:deliver-capability-change-cli
@root-scenario:deliver-capability-change-cli
Feature: Deliver capability change management through one command line

  Engineers and agents use one stable `sidefx change` command surface while
  open, seal, publish, and observe capabilities retain all lifecycle meaning.
  Command-line delivery owns only argument and standard-stream carriers,
  canonical operation request construction, capability invocation, result
  rendering, and exact usage failures.

  The command line never recreates change orchestration, chooses a mutation
  set, infers proof success, performs an undeclared merge, or edits admitted
  authority directly.

  @scenario:deliver-capability-change-cli
  @input:capability-change-cli-request
  @input-contract:capability-change-cli-request.v1
  @event:capability-change-cli-delivery-requested
  @event-authority:deliver-capability-change-cli.v1
  @outcome:capability-change-cli-result
  @outcome-contract:capability-change-cli-result.v1
  @outcome-terminal
  Scenario: Deliver one admitted capability change command
    Given arguments for open, seal, publish, or status and admitted bindings to the corresponding capability change operations
    When command-line delivery is requested
    Then the exact canonical operation request is invoked and only its governed result is rendered through the declared standard carriers

  @scenario:bind-capability-change-cli-command
  @input:capability-change-cli-request
  @input-contract:capability-change-cli-request.v1
  @event:capability-change-cli-command-binding-requested
  @event-authority:bind-capability-change-cli-command.v1
  @outcome:capability-change-operation-request
  @outcome-contract:capability-change-operation-request.v1
  @outcome-terminal
  Scenario: Bind the four public verbs without changing their meaning
    Given `sidefx change open` with a capability and reason reference, or seal, publish, or status with a governed change context
    When command arguments are bound
    Then one request targets only open-capability-change, seal-capability-change, publish-capability-change, or observe-capability-change with the declared carrier fields

  @scenario:render-capability-change-cli-status
  @input:capability-change-status
  @input-contract:capability-change-status.v1
  @event:capability-change-cli-status-rendering-requested
  @event-authority:render-capability-change-cli-status.v1
  @outcome:capability-change-cli-result
  @outcome-contract:capability-change-cli-result.v1
  @outcome-terminal
  Scenario: Render concise status without becoming status authority
    Given one governed capability change status
    When command-line status is rendered
    Then change identity, root capability, baseline, reason, mutation set, impact proof set, current stage, findings, mainline relationship, and authorized next action preserve the governed status exactly

  @scenario:reject-unadmitted-capability-change-cli-request
  @input:capability-change-cli-request
  @input-contract:capability-change-cli-request.v1
  @event:capability-change-cli-rejection-requested
  @event-authority:reject-unadmitted-capability-change-cli-request.v1
  @outcome:capability-change-cli-result
  @outcome-contract:capability-change-cli-result.v1
  @outcome-terminal
  Scenario: Reject missing malformed or unknown command carriers
    Given a missing capability identity, missing reason reference, missing governed change context, malformed carrier, unknown verb, or failed projected operation
    When command-line delivery is attempted
    Then no alternate operation is inferred and the exact usage, admission, or governed-operation failure is rendered with a failed process disposition

