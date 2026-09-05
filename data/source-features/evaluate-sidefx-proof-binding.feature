@capability:evaluate-sidefx-proof-binding
@root-scenario:evaluate-sidefx-proof-binding
Feature: Evaluate SideFX proof binding

  A SideFX semantic authority maintainer needs proof-binding evaluation to
  preserve the frozen profile's authority boundary through the admitted
  profile-governed proof-binding evaluation platform capability. Operational
  evaluation records remain distinct from provider-conformance evidence and
  from the proof-binding conformance receipts that consume those records.

  @scenario:evaluate-sidefx-proof-binding
  @input:sidefx-proof-binding-evaluation-request
  @input-contract:sidefx-proof-binding-evaluation-input.v1
  @event:sidefx-proof-binding-evaluation-requested
  @event-authority:sidefx-proof-binding-evaluation.v1
  @outcome:sidefx-proof-binding-evaluation-record
  @outcome-contract:sidefx-proof-binding-evaluation-record.v1
  @outcome-terminal
  Scenario: Evaluate one proof obligation under the frozen binding profile
    Given one pinned snapshot, the frozen SideFX proof-binding profile, and one declared proof obligation
    When explicit bindings, deterministic rules, applicability, and evidence lineage are evaluated in profile order
    Then exactly one honest obligation disposition and its lineage findings are retained without turning the operational record into a conformance receipt or admission claim

  @scenario:accept-explicit-or-deterministic-current-binding
  @input:current-proof-binding-evaluation
  @input-contract:sidefx-proof-binding-evaluation-record.v1
  @event:current-proof-binding-evaluation-requested
  @event-authority:sidefx-proof-binding-current-evaluation.v1
  @outcome:current-proof-binding-evaluation-record
  @outcome-contract:sidefx-proof-binding-evaluation-record.v1
  @outcome-terminal
  Scenario: Accept an explicit or deterministic binding with current passing evidence
    Given explicit fixture authority or a canonical-ID deterministic rule and current admitted passing evidence
    When the declared binding path is evaluated
    Then the binding is retained as BOUND and the obligation is SATISFIED without treating the result as capability admission or conformance

  @scenario:report-missing-evidence-not-observable
  @input:missing-proof-evidence-evaluation
  @input-contract:sidefx-proof-binding-evaluation-record.v1
  @event:missing-proof-evidence-evaluation-requested
  @event-authority:sidefx-proof-binding-missing-evidence-evaluation.v1
  @outcome:missing-proof-evidence-evaluation-record
  @outcome-contract:sidefx-proof-binding-evaluation-record.v1
  @outcome-terminal
  Scenario: Report missing required evidence as not observable
    Given a required proof obligation whose subject binding or evidence is absent
    When the obligation is evaluated
    Then the obligation is NOT_OBSERVABLE and no failure is inferred from absence alone

  @scenario:report-current-failure-not-satisfied
  @input:current-failing-proof-evidence-evaluation
  @input-contract:sidefx-proof-binding-evaluation-record.v1
  @event:current-failing-proof-evidence-evaluation-requested
  @event-authority:sidefx-proof-binding-current-failure-evaluation.v1
  @outcome:current-failing-proof-evidence-evaluation-record
  @outcome-contract:sidefx-proof-binding-evaluation-record.v1
  @outcome-terminal
  Scenario: Report current admitted failing evidence as not satisfied
    Given a required proof obligation with current admitted evidence that explicitly fails it
    When the obligation is evaluated after applicability and observability
    Then the obligation is NOT_SATISFIED with the current evidence lineage retained

  @scenario:report-admitted-exclusion-not-applicable
  @input:excluded-proof-obligation-evaluation
  @input-contract:sidefx-proof-binding-evaluation-record.v1
  @event:excluded-proof-obligation-evaluation-requested
  @event-authority:sidefx-proof-binding-exclusion-evaluation.v1
  @outcome:excluded-proof-obligation-evaluation-record
  @outcome-contract:sidefx-proof-binding-evaluation-record.v1
  @outcome-terminal
  Scenario: Report an admitted authority exclusion as not applicable
    Given admitted authority explicitly excludes one proof obligation
    When the obligation is evaluated
    Then the obligation is NOT_APPLICABLE before evidence absence or failure is considered

  @scenario:reject-prohibited-binding-basis
  @input:prohibited-basis-proof-binding-evaluation
  @input-contract:sidefx-proof-binding-evaluation-record.v1
  @event:prohibited-basis-proof-binding-evaluation-requested
  @event-authority:sidefx-proof-binding-prohibited-basis-evaluation.v1
  @outcome:prohibited-basis-proof-binding-evaluation-record
  @outcome-contract:sidefx-proof-binding-evaluation-record.v1
  @outcome-terminal
  Scenario: Reject proximity prose similarity and model testimony as proof basis
    Given a proposed binding justified only by directory proximity matching prose lexical similarity embedding similarity or model testimony
    When binding basis is evaluated
    Then the binding is REJECTED with its prohibited basis named and no relationship is derived

  @scenario:reject-stale-or-mixed-proof-lineage
  @input:stale-or-mixed-lineage-evaluation
  @input-contract:sidefx-proof-binding-evaluation-record.v1
  @event:stale-or-mixed-lineage-evaluation-requested
  @event-authority:sidefx-proof-binding-lineage-evaluation.v1
  @outcome:stale-or-mixed-lineage-evaluation-record
  @outcome-contract:sidefx-proof-binding-evaluation-record.v1
  @outcome-terminal
  Scenario: Reject stale or mixed snapshot lineage before evaluating proof
    Given a proposed proof path with stale evidence, inconsistent snapshot digests, or mixed fixture and projected-test lineage
    When lineage freshness and identity continuity are evaluated
    Then the invalid proof path is REJECTED and the required obligation remains NOT_OBSERVABLE unless admitted current evidence explicitly fails it

  @scenario:reproduce-proof-binding-evaluation-deterministically
  @input:reproducible-proof-binding-evaluation
  @input-contract:sidefx-proof-binding-evaluation-record.v1
  @event:reproducible-proof-binding-evaluation-requested
  @event-authority:sidefx-proof-binding-reproduction-evaluation.v1
  @outcome:reproducible-proof-binding-evaluation-record
  @outcome-contract:sidefx-proof-binding-evaluation-record.v1
  @outcome-terminal
  Scenario: Reproduce a proof-binding evaluation from pinned ordered inputs
    Given the same pinned snapshot, ordered input digest, profile version, and declared rule identities
    When the proof-binding evaluation is repeated
    Then the same obligation disposition binding disposition and ordered findings are reproducible without a model-selected basis
