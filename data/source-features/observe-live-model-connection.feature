@capability:observe-live-model-connection
@root-scenario:observe-live-model-connection
Feature: Observe explicitly authorized live model connections

  # Legacy oracle: generic-llm-connector CLI live obtainment

  This capability performs one opt-in live smoke observation for one explicitly
  governed provider and concrete model. Its objective covers successful
  connectivity, missing authorization, open conformance or runtime proof,
  unavailable credentials, denied endpoints, provider and transport failure,
  provider/model drift, attempt and substitution limits, and the rule that live
  testimony cannot change deterministic conformance or promotion.

  A multi-model conveyor may invoke this capability independently for model
  bindings from different providers. Each observation remains isolated and
  attributable to exactly one role-ready binding.

  @scenario:observe-live-model-connection
  @input:live-model-connection-observation-request
  @input-contract:observe-live-model-connection-input.v1
  @event:live-model-connection-observation-requested
  @event-authority:observe-live-model-connection.v1
  @outcome:live-model-connection-observation
  @outcome-contract:live-model-connection-observation-evidence.v1
  @outcome-terminal
  Scenario: Observe one successful live provider and model binding
    Given explicit effect authorization, one small admitted smoke request, one exact provider and concrete model binding, proven runtime and conformance, allowed endpoint, available credential, one attempt, and a fresh run identity
    When the live model connection is observed
    Then a credential-free MODEL_RESPONSE_OBTAINED receipt retains provider, concrete model, request and response hashes, timing, usage when available, attempt count, and effect lineage as non-gating testimony

  @scenario:reject-unauthorized-live-model-connection
  @input:unauthorized-live-model-connection-request
  @input-contract:observe-live-model-connection-input.v1
  @event:unauthorized-live-model-connection-observation-requested
  @event-authority:reject-unauthorized-live-model-connection.v1
  @outcome:unauthorized-live-model-connection-rejection
  @outcome-contract:live-model-connection-observation-evidence.v1
  @outcome-terminal
  Scenario: Reject live observation without explicit effect authority
    Given a smoke request lacking authorization for its root, provider, concrete model, endpoint, credential reference, cost scope, or fresh run identity
    When live observation prerequisites are evaluated
    Then the request is rejected before credential or network effects and every missing authority is named without widening scope or selecting defaults

  @scenario:hold-unproven-live-model-runtime-or-conformance
  @input:unproven-live-model-runtime-or-conformance
  @input-contract:observe-live-model-connection-input.v1
  @event:unproven-live-model-connection-observation-requested
  @event-authority:hold-unproven-live-model-runtime-or-conformance.v1
  @outcome:unproven-live-model-connection-held
  @outcome-contract:live-model-connection-observation-evidence.v1
  @outcome-terminal
  Scenario: Hold live observation when runtime or deterministic conformance is open
    Given a model binding with missing, stale, failed, or incomplete runtime-closure or deterministic conformance evidence
    When live observation eligibility is evaluated
    Then the observation is held with exact prerequisite findings and live success cannot be used to bypass the open proof

  @scenario:hold-live-model-connection-with-unavailable-credential
  @input:live-model-connection-with-unavailable-credential
  @input-contract:observe-live-model-connection-input.v1
  @event:live-model-connection-with-unavailable-credential-requested
  @event-authority:hold-live-model-connection-with-unavailable-credential.v1
  @outcome:live-model-credential-unavailable
  @outcome-contract:live-model-connection-observation-evidence.v1
  @outcome-terminal
  Scenario: Retain credential unavailability without contacting the provider
    Given an otherwise eligible live request whose exact authorized credential reference is missing, empty, expired, or unavailable
    When credential binding is attempted
    Then PROVIDER_AUTHENTICATION_FAILED and secret-free lineage are retained with zero network exchanges and no alternative credential or provider is tried

  @scenario:reject-live-model-endpoint-outside-policy
  @input:live-model-endpoint-outside-policy
  @input-contract:observe-live-model-connection-input.v1
  @event:out-of-policy-live-model-endpoint-requested
  @event-authority:reject-live-model-endpoint-outside-policy.v1
  @outcome:out-of-policy-live-model-endpoint-rejection
  @outcome-contract:live-model-connection-observation-evidence.v1
  @outcome-terminal
  Scenario: Reject live endpoints that differ from governed binding
    Given an otherwise eligible request whose endpoint is malformed, credential-bearing, outside the allowlist, or differs from the provider binding
    When endpoint authority is evaluated
    Then the request is rejected before DNS or connection effects and no redirect, alternate host, or provider default is followed

  @scenario:retain-live-model-provider-failure
  @input:failed-live-model-provider-observation
  @input-contract:observe-live-model-connection-input.v1
  @event:failed-live-model-provider-observation-requested
  @event-authority:retain-live-model-provider-failure.v1
  @outcome:live-model-provider-failure-observation
  @outcome-contract:live-model-connection-observation-evidence.v1
  @outcome-terminal
  Scenario: Retain authentication timeout unavailable rejection and format failures
    Given one authorized live attempt returning a provider authentication, timeout, unavailable, request-rejection, content-policy, refusal, truncation, malformed-body, or response-format failure
    When the live observation is normalized
    Then the exact governed disposition, provider-native safe facts, hashes, timing, usage when available, and lineage are retained without retry, repair, substitution, or acceptance claims

  @scenario:hold-live-model-identity-drift
  @input:drifted-live-model-identity-observation
  @input-contract:observe-live-model-connection-input.v1
  @event:live-model-identity-drift-evaluation-requested
  @event-authority:hold-live-model-identity-drift.v1
  @outcome:live-model-identity-drift-findings
  @outcome-contract:live-model-connection-observation-evidence.v1
  @outcome-terminal
  Scenario: Hold a response attributed to an unexpected provider or model
    Given a live exchange whose observed provider, concrete model, endpoint, adapter, or authority digest differs from the requested binding
    When response attribution is evaluated
    Then exact identity drift is retained and the response is not reassigned to the requested role, accepted as conformant, or used by a dependent stage

  @scenario:prove-single-attempt-live-model-observation
  @input:live-model-attempt-count-observation
  @input-contract:observe-live-model-connection-input.v1
  @event:single-attempt-live-model-observation-proof-requested
  @event-authority:prove-single-attempt-live-model-observation.v1
  @outcome:single-attempt-live-model-observation-evidence
  @outcome-contract:live-model-connection-observation-evidence.v1
  @outcome-terminal
  Scenario: Prove no hidden retry fallback or provider substitution occurred
    Given successful and failed live smoke observations authorized for exactly one provider model and one attempt
    When invocation count and binding lineage are evaluated
    Then exactly zero or one authorized attempt is attributable and no alternate model, provider, endpoint, credential, or adapter was tried

  @scenario:prove-live-model-testimony-is-non-gating
  @input:live-model-observation-and-gate-state
  @input-contract:observe-live-model-connection-input.v1
  @event:live-model-testimony-authority-proof-requested
  @event-authority:prove-live-model-testimony-is-non-gating.v1
  @outcome:live-model-testimony-non-gating-evidence
  @outcome-contract:live-model-connection-observation-evidence.v1
  @outcome-terminal
  Scenario: Prove live success and failure cannot mutate deterministic authority
    Given a retained live observation and prior compiler, runtime, conformance, candidate, oracle, provider-binding, and promotion state
    When live testimony authority is evaluated
    Then all prior deterministic state remains byte-identical and the live observation can inform availability only without admitting semantics, closing conformance, changing roles, or promoting a provider
