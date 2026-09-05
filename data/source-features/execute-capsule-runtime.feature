@capability:execute-capsule-runtime
@root-scenario:execute-capsule-runtime
Feature: Execute one admitted capability from its capsule without expansion

  Store the capability. Project the explanation. Execute the effect — from the
  capsule itself.

  A customer installs and runs capabilities, not expanded repositories. The
  expanded workspace is an authoring and inspection projection; it is disposable
  and MUST NOT be required for ordinary capability execution. This capability
  owns the loader closure: open the capsule, verify it, decode the execution
  authorities, port bindings, and semantic transformations in memory, execute
  the declared scenario, and report what was observed.

  No workspace is written. No projected execution plan is read from any
  repository. The only admitted input is the capsule byte sequence and one
  scenario input. If the capability folder does not exist, execution still
  closes.

  A capsule carries meaning, not providers. It is self-describing and
  self-revealing but never self-admitting and never self-executing: this
  capability admits only pure authority transformations from capsule bindings,
  and refuses any binding that would reach outside the capsule for an effect.
  Admission remains the consuming authority's decision; this capability reports
  execution facts and never promotes them into acceptance.

  Every scenario admits and emits one shared capsule runtime record.

  @scenario:execute-capsule-runtime
  @input:capsule-runtime-record
  @input-contract:capsule-runtime-record.v1
  @event:capsule-runtime-execution-requested
  @event-authority:execute-capsule-runtime.v1
  @outcome:capsule-runtime-record
  @outcome-contract:capsule-runtime-record.v1
  @outcome-terminal
  Scenario: Execute one capability from capsule bytes with no expansion
    Given one physical capsule byte sequence and one scenario input
    When the capsule runtime is executed
    Then the declared root scenario runs wholly in memory and the outcome binds with disposition CAPSULE_EXECUTION_ESTABLISHED, no workspace is written, no projected execution plan is read, and any failure reports CAPSULE_EXECUTION_HELD with the exact holding finding

  @scenario:admit-capsule-runtime-integrity
  @input:capsule-runtime-record
  @input-contract:capsule-runtime-record.v1
  @event:capsule-runtime-integrity-admission-requested
  @event-authority:admit-capsule-runtime-integrity.v1
  @outcome:capsule-runtime-record
  @outcome-contract:capsule-runtime-record.v1
  @outcome-terminal
  Scenario: Trust no capsule entry before its own digest reproduces
    Given one capsule byte sequence and one declared capsule digest
    When capsule integrity is admitted
    Then the recomputed capsule digest equals the declared digest and every entry digest reproduces from that entry's own bytes, reporting CAPSULE_DIGEST_DIVERGED or CAPSULE_ENTRY_DIGEST_DIVERGED otherwise

  @scenario:resolve-capsule-execution-authority
  @input:capsule-runtime-record
  @input-contract:capsule-runtime-record.v1
  @event:capsule-execution-authority-resolution-requested
  @event-authority:resolve-capsule-execution-authority.v1
  @outcome:capsule-runtime-record
  @outcome-contract:capsule-runtime-record.v1
  @outcome-terminal
  Scenario: Resolve the execution circuit from capsule entries alone
    Given one admitted capsule
    When the execution authority is resolved
    Then the root scenario identity, execution authorities, port bindings, and semantic transformations are bound from capsule entries alone, and a missing required entry reports REQUIRED_CAPSULE_ENTRY_MISSING

  @scenario:refuse-capsule-effect-boundary
  @input:capsule-runtime-record
  @input-contract:capsule-runtime-record.v1
  @event:capsule-effect-boundary-refusal-requested
  @event-authority:refuse-capsule-effect-boundary.v1
  @outcome:capsule-runtime-record
  @outcome-contract:capsule-runtime-record.v1
  @outcome-terminal
  Scenario: Refuse any binding that reaches outside the capsule
    Given one resolved capsule execution circuit
    When the effect boundary is verified
    Then every invoked port binding is a pure authority transformation, and any other platform capability reports CAPSULE_EFFECT_PORT_NOT_ADMITTED before the effect occurs

  @scenario:observe-capsule-execution-trace
  @input:capsule-runtime-record
  @input-contract:capsule-runtime-record.v1
  @event:capsule-execution-trace-observation-requested
  @event-authority:observe-capsule-execution-trace.v1
  @outcome:capsule-runtime-record
  @outcome-contract:capsule-runtime-record.v1
  @outcome-terminal
  Scenario: Observe every step the capsule executed
    Given one capsule execution
    When the execution trace is observed
    Then each step records its owning scenario, operation kind, invoked reference, and transformation identity in declared order, and the observed step count equals the executed operation count

  @scenario:bind-capsule-runtime-receipt
  @input:capsule-runtime-record
  @input-contract:capsule-runtime-record.v1
  @event:capsule-runtime-receipt-binding-requested
  @event-authority:bind-capsule-runtime-receipt.v1
  @outcome:capsule-runtime-record
  @outcome-contract:capsule-runtime-record.v1
  @outcome-terminal
  Scenario: Bind one replayable capsule runtime receipt
    Given one capsule execution disposition
    When the capsule runtime receipt is bound
    Then the capsule digest, root scenario identity, scenario input digest, outcome digest, step count, and disposition bind into one replayable receipt, and the receipt is reproducible without timestamp, machine, user, or path input
