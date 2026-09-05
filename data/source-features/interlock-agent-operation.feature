@capability:interlock-agent-operation
@root-scenario:interlock-agent-operation
@lifecycle:FIRST_ADMISSION
Feature: Govern one agent session through an admitted hook interlock

  An operator gives an agent an assigned task. Before the agent performs that
  task, this capability establishes an exact session-scoped hook boundary,
  proves that the same live boundary both denies an unmanaged probe and allows
  a declared read-only probe, and thereafter adjudicates every supported covered
  local tool call. The declarative governed-run skill tells the agent how to use
  this capability; the skill never carries or substitutes executable governance.

  Activation is not certification. Certification joins evidence only from one
  activation, harness session, workspace, ordered time boundary, adapter digest,
  daemon digest, policy digest, and durable capability-authority digest. Test,
  falsification, stale, cross-session, and cross-workspace receipts cannot
  satisfy a production certification.

  Production failure is closed. An unavailable adjudicator, malformed hook
  request, malformed response, unsupported local effect surface, incomplete
  adapter coverage, configuration conflict, or identity divergence holds the
  operation. A harness that cannot attach the exact hook to its current session
  returns a concrete relaunch requirement and does not claim governance.

  The governed agent cannot lower its own mode, grant itself a bypass, replace
  the hook, or mutate operator policy. Those controls cross a separately
  authenticated operator boundary. Existing harness configuration is strictly
  parsed, atomically merged without deleting unrelated settings, and restored
  from an exact pre-change digest when rollback is required.

  The claim is intentionally bounded. Certification covers only the local tool
  surfaces the detected harness is proven to route through its declared hook.
  Hosted and specialized paths outside that route are reported as uncovered and
  never silently included. This capability does not prove an operating-system
  filesystem, process, credential, or network effect boundary.

  @scenario:interlock-agent-operation
  @input:agent-interlock-operation-request
  @input-contract:agent-interlock-operation-request.v1
  @event:interlock-agent-operation
  @event-authority:interlock-agent-operation.v1
  @outcome:agent-interlock-operation-outcome
  @outcome-contract:agent-interlock-operation-outcome.v1
  @outcome-variants:ACTIVATION_READY|CERTIFICATION_ESTABLISHED|OPERATION_ADJUDICATED|OPERATOR_ACTION_APPLIED|GOVERNANCE_HELD
  @outcome-terminal
  Scenario: Govern one requested agent operation without widening its authority
    Given one contract-admitted activation, certification, adjudication, or authenticated operator-control request
    When the request is bound to exact live governance identities and routed to its declared operation
    Then return its exact ready, established, adjudicated, applied, or held outcome without treating activation, configuration, or an agent report as proof

  @scenario:admit-agent-interlock-request
  @input:agent-interlock-operation-request
  @input-contract:agent-interlock-operation-request.v1
  @event:admit-agent-interlock-request
  @event-authority:admit-agent-interlock-request.v1
  @outcome:admitted-agent-interlock-request
  @outcome-contract:admitted-agent-interlock-request.v1
  @outcome-variants:ACTIVATION_REQUEST_ADMITTED|CERTIFICATION_REQUEST_ADMITTED|ADJUDICATION_REQUEST_ADMITTED|CONTROL_REQUEST_ADMITTED|GOVERNANCE_HELD
  Scenario: Admit only a complete request at the caller's authority altitude
    Given one request naming its operation, harness, session, workspace, requested mode, authority lineage, and evidence domain
    When shape, identity, mode, caller authority, and operation applicability are evaluated
    Then admit the exact activation, certification, adjudication, or control request variant or hold it with an attributable code before any configuration, policy, process, or receipt state changes

  @scenario:activate-agent-interlock
  @input:admitted-agent-interlock-activation-request
  @input-contract:admitted-agent-interlock-activation-request.v1
  @event:activate-agent-interlock
  @event-authority:activate-agent-interlock.v1
  @outcome:agent-interlock-activation-outcome
  @outcome-contract:agent-interlock-activation-outcome.v1
  @outcome-variants:ATTACHED_IN_SESSION|RELAUNCH_REQUIRED|ACTIVATION_HELD
  Scenario: Establish one identity-bound fail-closed hook boundary
    Given one admitted production activation request for ENFORCE or LOCKDOWN and one detected supported harness
    When the admitted runtime resolves complete supported local-tool coverage, binds live adapter, daemon, policy, and capability identities, and atomically attaches or stages the exact hook configuration
    Then return ATTACHED_IN_SESSION with a one-use probe nonce, RELAUNCH_REQUIRED with a concrete governed launch instruction, or ACTIVATION_HELD with no governance claim and no destructive configuration change

  @scenario:certify-live-agent-interlock
  @input:agent-interlock-certification-request
  @input-contract:agent-interlock-certification-request.v1
  @event:certify-live-agent-interlock
  @event-authority:certify-live-agent-interlock.v1
  @outcome:agent-interlock-certification-outcome
  @outcome-contract:agent-interlock-certification-outcome.v1
  @outcome-variants:GOVERNANCE_PROVEN|GOVERNANCE_NOT_ACTIVE|GOVERNANCE_BLOCKS_EVERYTHING|GOVERNANCE_NOT_ENFORCING|GOVERNANCE_UNREACHABLE|GOVERNANCE_IDENTITY_MISMATCH|GOVERNANCE_UNVERIFIED_ALLOW_PATH
  Scenario: Certify only a two-sided probe from the same live activation
    Given one certification request carrying the one-use nonce and exact activation identity
    When production receipts are resolved in order for one denied nonce-bearing real tool call and one allowed declared read-only real tool call
    Then return GOVERNANCE_PROVEN only when every session, workspace, activation, hook, daemon, policy, capability-authority, time, and evidence-domain identity matches, or return the exact non-proven disposition

  @scenario:adjudicate-covered-agent-tool-call
  @input:covered-agent-tool-call
  @input-contract:covered-agent-tool-call.v1
  @event:adjudicate-covered-agent-tool-call
  @event-authority:adjudicate-covered-agent-tool-call.v1
  @outcome:agent-tool-call-disposition
  @outcome-contract:agent-tool-call-disposition.v1
  @outcome-variants:ALLOW|USE_CAPABILITY|PROVIDE_CAPABILITY_INTENT|PROVISION_CAPABILITY|OPERATOR_REQUIRED|GOVERNANCE_HELD
  Scenario: Return the next legal operation for one covered tool call
    Given one hook-observed local tool call bound to a proven live activation and its exact structured input
    When the operation, intent, capability admission, scope, mode, and authority altitude are adjudicated
    Then allow the call, require an exact admitted capability, request capability intent, require provisioning, require the operator, or hold fail-closed with a corrective instruction and immutable production receipt

  @scenario:protect-agent-interlock-control-plane
  @input:agent-interlock-control-request
  @input-contract:agent-interlock-control-request.v1
  @event:protect-agent-interlock-control-plane
  @event-authority:protect-agent-interlock-control-plane.v1
  @outcome:agent-interlock-control-outcome
  @outcome-contract:agent-interlock-control-outcome.v1
  @outcome-variants:OPERATOR_ACTION_APPLIED|OPERATOR_AUTHORITY_REQUIRED|CONTROL_REQUEST_REJECTED
  Scenario: Separate operator policy authority from the governed agent channel
    Given one request to change mode, grant a bounded bypass, repair attachment, or restore configuration
    When authenticated operator authority, target session, scope, duration, and reason are verified independently of agent-supplied identity
    Then apply and receipt the exact bounded operator action or reject it without weakening any active session boundary

  @scenario:hold-untrusted-or-uncovered-agent-operation
  @input:untrusted-agent-operation
  @input-contract:untrusted-agent-operation.v1
  @event:hold-untrusted-or-uncovered-agent-operation
  @event-authority:hold-untrusted-or-uncovered-agent-operation.v1
  @outcome:governance-hold
  @outcome-contract:governance-hold.v1
  @outcome-variants:MALFORMED_HOOK_INPUT|ADJUDICATOR_UNAVAILABLE|MALFORMED_ADJUDICATOR_RESPONSE|UNSUPPORTED_HARNESS|UNSUPPORTED_LOCAL_TOOL_SURFACE|INCOMPLETE_COVERAGE|CONFIGURATION_CONFLICT|GOVERNANCE_IDENTITY_MISMATCH
  @outcome-terminal
  Scenario: Fail closed without overstating the hook boundary
    Given malformed, unavailable, divergent, unsupported, or incompletely covered governance testimony
    When the capability cannot prove one exact legal operation through the declared hook surface
    Then deny the local operation with the exact hold code, retain attributable evidence, and make no operating-system or uncovered-surface enforcement claim
