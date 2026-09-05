@capability:deliver-capsule-estate-cli
@root-scenario:deliver-capsule-estate-cli
@lifecycle:REVISION_V2
Feature: Deliver capsule estate operations through one portable command carrier

  Developers and agents use one stable JSON command surface while capsule
  meaning remains owned by operate-capsule-estate. The delivery capability owns
  only command and standard-stream carriers, canonical operation-request
  construction, projected capability invocation, result rendering, and exact
  usage failures.

  Every request carries its caller-authorized repository root explicitly. No
  checkout path, scratch root, tool root, or machine identity is embedded in
  feature, blueprint, capability, capsule, or bootstrap authority. Commands
  requiring structured values receive JSON carriers rather than relying on
  unadmitted text splitting.

  @scenario:deliver-capsule-estate-cli
  @input:capsule-estate-cli-delivery-request
  @input-contract:capsule-estate-cli-delivery-request.v2
  @event:capsule-estate-cli-delivery-requested
  @event-authority:deliver-capsule-estate-cli.v2
  @outcome:capsule-estate-cli-delivery-result
  @outcome-contract:capsule-estate-cli-delivery-result.v2
  @outcome-variants:DELIVERED|REQUEST_REJECTED
  @outcome-terminal
  Scenario: Translate and deliver one admitted capsule command
    Given a caller-authorized repository root and a command for verify, resolve, list, inspect, invoke, expand, project, test, direct, proof, or sterile-proof
    When command-line delivery is requested
    Then exactly one canonical capsule-estate-operation-request.v2 is invoked and its canonical result is rendered as JSON, or an exact attributable rejection is returned

  @scenario:bind-capsule-cli-arguments
  @input:capsule-estate-cli-delivery-request
  @input-contract:capsule-estate-cli-delivery-request.v2
  @event:capsule-estate-cli-argument-binding-requested
  @event-authority:bind-capsule-cli-arguments.v2
  @outcome:capsule-estate-cli-binding-result
  @outcome-contract:capsule-estate-cli-binding-result.v2
  @outcome-variants:REQUEST_BOUND|REQUEST_REJECTED
  Scenario: Bind command fields without changing operation meaning
    Given a command carrier containing only the declared repository root, query, capability identity, capability input, target root, disposable parent root, capability identities, or fixture identities needed by that command
    When command fields are bound
    Then verify, resolve, list, inspect, invoke, expand, project, direct proof, capsule-first proof, and sterile proof receive only their capsule-estate-operation-request.v2 fields and test and direct are aliases of prove-direct-execution

  @scenario:reject-unadmitted-capsule-cli-request
  @input:capsule-estate-cli-binding-result
  @input-contract:capsule-estate-cli-binding-result.v2
  @event:capsule-estate-cli-rejection-requested
  @event-authority:reject-unadmitted-capsule-cli-request.v2
  @outcome:capsule-estate-cli-delivery-result
  @outcome-contract:capsule-estate-cli-delivery-result.v2
  @outcome-variants:REQUEST_REJECTED
  @outcome-terminal
  Scenario: Reject missing or unadmitted command carriers
    Given a missing repository root, missing command-required field, malformed structured value, unknown command, or failed projected operation
    When command delivery is attempted
    Then no alternate operation or local path is inferred and the exact usage, contract, structured-value, or projected-operation finding is returned with a failed process disposition
