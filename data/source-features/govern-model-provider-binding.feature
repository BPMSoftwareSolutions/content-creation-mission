@capability:govern-model-provider-binding
@root-scenario:govern-model-provider-binding
Feature: Govern model provider bindings

  # Legacy oracles:
  # generic-llm-connector/authority/provider-authority.schema.v1.json
  # generic-llm-connector/src/obtains-model-response/resolves-provider-authority.ts
  # generic-llm-connector/src/obtains-model-response/resolves-model-alias.ts
  # generic-llm-connector/src/obtains-model-response/invokes-provider-adapter.ts

  This capability admits credential-free provider authority and a projected
  adapter registry, then resolves exactly the provider and model named by an
  admitted request. Its execution objective includes every successful,
  unresolved, incompatible, ambiguous, stale, and unauthorized binding case.

  A binding preserves provider identity and kind, concrete model identity,
  interaction-mode support, endpoint policy, credential reference name,
  request-projection and testimony-normalization capability identities, host
  coverage, and source digests. It never carries credential values, executable
  module paths, implicit defaults, fallback order, or substitution authority.

  @scenario:govern-model-provider-binding
  @input:model-provider-binding-governance-request
  @input-contract:govern-model-provider-binding-input.v1
  @event:model-provider-binding-governance-requested
  @event-authority:govern-model-provider-binding.v1
  @outcome:governed-model-provider-binding
  @outcome-contract:governed-model-provider-binding-evidence.v1
  @outcome-terminal
  Scenario: Resolve one fully governed provider binding
    Given one admitted model request, one valid provider authority, one complete projected adapter registry, and a deterministic authoring profile
    When the requested provider and model binding is governed
    Then one credential-free digest-bound binding preserves the exact provider, model, mode, endpoint, credential reference, adapter capabilities, host coverage, and authority lineage

  @scenario:resolve-distinct-model-bindings-across-providers
  @input:multi-provider-model-binding-set-request
  @input-contract:govern-model-provider-binding-input.v1
  @event:multi-provider-model-binding-set-requested
  @event-authority:resolve-distinct-model-bindings-across-providers.v1
  @outcome:governed-multi-provider-model-binding-set
  @outcome-contract:governed-model-provider-binding-evidence.v1
  @outcome-terminal
  Scenario: Resolve multiple models from multiple providers independently
    Given an ordered set of stage binding requests naming different provider authorities and concrete-model aliases with complete adapter and host coverage
    When every requested provider model binding is governed independently
    Then one stable binding per stage preserves its distinct provider model endpoint credential reference adapter and digests without coalescing roles, introducing cross-provider fallback, or treating one provider as substitute for another

  @scenario:reject-invalid-model-provider-authority
  @input:invalid-model-provider-authority
  @input-contract:govern-model-provider-binding-input.v1
  @event:model-provider-binding-governance-requested
  @event-authority:reject-invalid-model-provider-authority.v1
  @outcome:invalid-model-provider-authority-findings
  @outcome-contract:governed-model-provider-binding-evidence.v1
  @outcome-terminal
  Scenario: Reject malformed or incomplete provider authority
    Given provider authority with a missing identity, unsupported kind, incomplete endpoint policy, invalid credential reference, empty alias set, or inconsistent capability declaration
    When the provider authority is evaluated
    Then stable pointer-bound findings identify every invalid field and no provider binding, credential access, adapter load, or network effect occurs

  @scenario:reject-credential-bearing-model-provider-authority
  @input:credential-bearing-model-provider-authority
  @input-contract:govern-model-provider-binding-input.v1
  @event:model-provider-binding-governance-requested
  @event-authority:reject-credential-bearing-model-provider-authority.v1
  @outcome:credential-bearing-provider-authority-rejection
  @outcome-contract:governed-model-provider-binding-evidence.v1
  @outcome-terminal
  Scenario: Reject provider authority containing credential material
    Given provider authority containing an API key, token, secret-bearing URL, embedded authorization header, or credential value instead of a reference name
    When provider authority is evaluated
    Then the authority is rejected without reproducing, hashing, logging, indexing, or persisting the credential material

  @scenario:reject-ambiguous-model-provider-authority
  @input:ambiguous-model-provider-authority
  @input-contract:govern-model-provider-binding-input.v1
  @event:model-provider-binding-governance-requested
  @event-authority:reject-ambiguous-model-provider-authority.v1
  @outcome:ambiguous-model-provider-authority-findings
  @outcome-contract:governed-model-provider-binding-evidence.v1
  @outcome-terminal
  Scenario: Reject duplicate provider alias or adapter identities
    Given provider authorities or adapter bindings with duplicate or conflicting provider IDs, alias mappings, adapter IDs, provider kinds, or projected capability bindings
    When binding authority cardinality is evaluated
    Then every ambiguity is named in stable identity order and no arbitrary provider, model, or adapter is selected

  @scenario:hold-unknown-model-provider-authority
  @input:unknown-model-provider-binding-request
  @input-contract:govern-model-provider-binding-input.v1
  @event:model-provider-binding-governance-requested
  @event-authority:hold-unknown-model-provider-authority.v1
  @outcome:model-provider-authority-not-found
  @outcome-contract:governed-model-provider-binding-evidence.v1
  @outcome-terminal
  Scenario: Hold a request naming an unknown provider authority
    Given an admitted model request whose provider authority identity has no exact admitted match
    When the provider binding is resolved
    Then PROVIDER_AUTHORITY_NOT_FOUND is returned without defaulting, fallback, adapter invocation, credential access, or network effects

  @scenario:hold-unresolved-model-alias
  @input:unresolved-model-alias-binding-request
  @input-contract:govern-model-provider-binding-input.v1
  @event:model-provider-binding-governance-requested
  @event-authority:hold-unresolved-model-alias.v1
  @outcome:model-alias-not-found
  @outcome-contract:governed-model-provider-binding-evidence.v1
  @outcome-terminal
  Scenario: Hold a request naming an unmapped model alias
    Given an admitted request and exact provider authority with no mapping for the declared model alias
    When the model binding is resolved
    Then MODEL_ALIAS_NOT_FOUND is returned without guessing a model, following a latest alias, substituting a provider, or invoking an adapter

  @scenario:hold-unsupported-model-interaction-mode
  @input:unsupported-model-interaction-binding-request
  @input-contract:govern-model-provider-binding-input.v1
  @event:model-provider-binding-governance-requested
  @event-authority:hold-unsupported-model-interaction-mode.v1
  @outcome:model-interaction-mode-not-supported
  @outcome-contract:governed-model-provider-binding-evidence.v1
  @outcome-terminal
  Scenario: Hold a provider model that does not support the requested interaction
    Given an admitted request whose interaction mode is absent from the resolved model or provider capability declaration
    When provider model compatibility is evaluated
    Then INTERACTION_MODE_NOT_SUPPORTED is returned with the exact incompatible identities and no adapter or provider is invoked

  @scenario:reject-unprojected-model-provider-adapter
  @input:unprojected-model-provider-adapter-binding
  @input-contract:govern-model-provider-binding-input.v1
  @event:model-provider-binding-governance-requested
  @event-authority:reject-unprojected-model-provider-adapter.v1
  @outcome:unprojected-model-provider-adapter-findings
  @outcome-contract:governed-model-provider-binding-evidence.v1
  @outcome-terminal
  Scenario: Reject an authority naming an absent or handwritten adapter
    Given provider authority whose adapter has no admitted projected request-mapping and testimony-normalization capability with conformance evidence
    When adapter eligibility is evaluated
    Then the missing projected responsibility is named and no repository-relative source module or handwritten fallback is loaded

  @scenario:reject-incompatible-model-provider-adapter
  @input:incompatible-model-provider-adapter-binding
  @input-contract:govern-model-provider-binding-input.v1
  @event:model-provider-binding-governance-requested
  @event-authority:reject-incompatible-model-provider-adapter.v1
  @outcome:incompatible-model-provider-adapter-findings
  @outcome-contract:governed-model-provider-binding-evidence.v1
  @outcome-terminal
  Scenario: Reject an adapter whose provider kind contradicts authority
    Given an admitted adapter identity whose declared provider kind or supported mode differs from the provider authority or resolved model
    When adapter compatibility is evaluated
    Then the contradictory identities are returned as exact findings and no differently typed adapter is invoked

  @scenario:reject-divergent-model-adapter-host-coverage
  @input:divergent-model-adapter-host-coverage
  @input-contract:govern-model-provider-binding-input.v1
  @event:model-provider-binding-governance-requested
  @event-authority:reject-divergent-model-adapter-host-coverage.v1
  @outcome:divergent-model-adapter-host-findings
  @outcome-contract:governed-model-provider-binding-evidence.v1
  @outcome-terminal
  Scenario: Reject adapter coverage that differs across projected hosts
    Given an adapter registry whose provider support differs across declared CLI, projected consumer, or MCP host profiles
    When required host coverage is evaluated
    Then every missing or divergent host binding is named and no interface may advertise unavailable provider support

  @scenario:reject-stale-or-mutable-model-provider-binding
  @input:stale-or-mutable-model-provider-binding
  @input-contract:govern-model-provider-binding-input.v1
  @event:model-provider-binding-governance-requested
  @event-authority:reject-stale-or-mutable-model-provider-binding.v1
  @outcome:stale-or-mutable-model-provider-binding-findings
  @outcome-contract:governed-model-provider-binding-evidence.v1
  @outcome-terminal
  Scenario: Reject stale digests or mutable model mappings
    Given provider, model, registry, or policy facts whose observed digest differs from authority or whose model mapping is mutable under the deterministic profile
    When binding freshness and reproducibility are evaluated
    Then exact drift or mutability findings are returned and no stale or floating binding is admitted

  @scenario:reject-unauthorized-model-provider-endpoint
  @input:unauthorized-model-provider-endpoint-binding
  @input-contract:govern-model-provider-binding-input.v1
  @event:model-provider-binding-governance-requested
  @event-authority:reject-unauthorized-model-provider-endpoint.v1
  @outcome:unauthorized-model-provider-endpoint-findings
  @outcome-contract:governed-model-provider-binding-evidence.v1
  @outcome-terminal
  Scenario: Reject an endpoint outside declared provider policy
    Given provider authority whose explicit endpoint is malformed, credential-bearing, uses a forbidden scheme, or is outside the admitted host allowlist
    When endpoint authority is evaluated
    Then exact endpoint findings are returned without resolving DNS, opening a connection, or revealing credential material
