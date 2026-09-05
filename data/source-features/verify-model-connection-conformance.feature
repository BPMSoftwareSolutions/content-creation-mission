@capability:verify-model-connection-conformance
@root-scenario:verify-model-connection-conformance
Feature: Verify model connection conformance

  # Legacy oracles:
  # generic-llm-connector/tests/acceptance
  # generic-llm-connector/tests/conformance
  # generic-llm-connector/tests/adapters
  # scenario-driven-architecture/languages/typescript/runtimes/node/generic-llm-connector-port.conformance.test.mjs

  This capability verifies every admitted provider adapter and every projected
  host path with portable deterministic fixtures. Its execution objective
  covers complete conformance, provider and adapter coverage, protocol request
  mapping, provider testimony normalization, attempts and receipts, secret
  exclusion, host equivalence, runtime closure, and test isolation from live
  credentials, networks, clocks, entropy, and provider availability.

  Live testimony cannot make a failed deterministic partition pass.

  @scenario:verify-model-connection-conformance
  @input:model-connection-conformance-request
  @input-contract:verify-model-connection-conformance-input.v1
  @event:model-connection-conformance-verification-requested
  @event-authority:verify-model-connection-conformance.v1
  @outcome:model-connection-conformance
  @outcome-contract:model-connection-conformance-evidence.v1
  @outcome-terminal
  Scenario: Prove all declared adapters and hosts against every fixture partition
    Given admitted provider and adapter authority, a proven runtime closure, projected fake credential and HTTP effects, deterministic clock identity and hash testimony, and complete portable fixtures
    When model connection conformance is verified
    Then every request, binding, protocol, response, failure, attempt, receipt, secret-exclusion, and host-equivalence partition passes with exact evidence and no live effect

  @scenario:reject-incomplete-model-provider-conformance-coverage
  @input:incomplete-model-provider-conformance-coverage
  @input-contract:verify-model-connection-conformance-input.v1
  @event:model-provider-conformance-coverage-verification-requested
  @event-authority:reject-incomplete-model-provider-conformance-coverage.v1
  @outcome:model-provider-conformance-coverage-findings
  @outcome-contract:model-connection-conformance-evidence.v1
  @outcome-terminal
  Scenario: Fail when a declared provider adapter mode or host lacks fixtures
    Given provider and adapter authority with a provider kind, interaction mode, response format, failure disposition, or projected host absent from the fixture matrix
    When conformance coverage is evaluated
    Then every uncovered provider adapter mode format disposition and host is named and no partial suite is reported as conformant

  @scenario:detect-model-protocol-request-projection-divergence
  @input:model-protocol-request-projection-fixtures
  @input-contract:verify-model-connection-conformance-input.v1
  @event:model-protocol-request-projection-verification-requested
  @event-authority:detect-model-protocol-request-projection-divergence.v1
  @outcome:model-protocol-request-projection-findings
  @outcome-contract:model-connection-conformance-evidence.v1
  @outcome-terminal
  Scenario: Detect incorrect provider wire projection
    Given text and structured requests covering roles, ordering, model target, temperature, token bound, response schema, endpoint, headers, body, timeout, and credential injection boundaries
    When each projected provider request is compared with its frozen adapter oracle
    Then every byte or semantic mismatch is attributable to provider adapter and field without changing the oracle or accepting provider-specific mechanics upstream

  @scenario:detect-model-provider-testimony-normalization-divergence
  @input:model-provider-testimony-normalization-fixtures
  @input-contract:verify-model-connection-conformance-input.v1
  @event:model-provider-testimony-normalization-verification-requested
  @event-authority:detect-model-provider-testimony-normalization-divergence.v1
  @outcome:model-provider-testimony-normalization-findings
  @outcome-contract:model-connection-conformance-evidence.v1
  @outcome-terminal
  Scenario: Detect incorrect success error refusal truncation or malformed-body mapping
    Given provider fixtures for text, structured output, usage, request IDs, authentication, timeout, unavailability, rate limiting, content filtering, refusal, truncation, invalid JSON, schema violation, and unparseable bodies
    When provider testimony is normalized
    Then exact canonical disposition content retention and safe native evidence equal the frozen oracle or each divergence is named without leaking invalid content

  @scenario:detect-model-attempt-and-receipt-divergence
  @input:model-attempt-and-receipt-conformance-fixtures
  @input-contract:verify-model-connection-conformance-input.v1
  @event:model-attempt-and-receipt-conformance-verification-requested
  @event-authority:detect-model-attempt-and-receipt-divergence.v1
  @outcome:model-attempt-and-receipt-conformance-findings
  @outcome-contract:model-connection-conformance-evidence.v1
  @outcome-terminal
  Scenario: Detect hidden retries incorrect continuation and incomplete receipts
    Given fixtures for one attempt, transient continuation, non-transient stop, exhausted authority, missing continuation rule, no substitution, cancellation, every disposition, and each evidence-policy variant
    When attempt and receipt behavior is verified
    Then invocation counts, ordered testimony, stable hashes, exit dispositions, exit codes, optional evidence, and every-path receipts equal authority or exact mismatches are returned

  @scenario:detect-model-connection-secret-leakage
  @input:model-connection-secret-exclusion-fixtures
  @input-contract:verify-model-connection-conformance-input.v1
  @event:model-connection-secret-exclusion-verification-requested
  @event-authority:detect-model-connection-secret-leakage.v1
  @outcome:model-connection-secret-leakage-findings
  @outcome-contract:model-connection-conformance-evidence.v1
  @outcome-terminal
  Scenario: Detect credentials crossing any model connection boundary
    Given canary secret fixtures exercised through requests, authorities, bindings, wire projection, transport, failures, logs, hashes, receipts, MCP content, retrieval units, and durable evidence
    When secret exclusion is verified
    Then no canary appears outside the fake credential effect provider or an exact surface and artifact finding is returned without reproducing the secret value

  @scenario:detect-model-connection-host-divergence
  @input:model-connection-host-equivalence-fixtures
  @input-contract:verify-model-connection-conformance-input.v1
  @event:model-connection-host-equivalence-verification-requested
  @event-authority:detect-model-connection-host-divergence.v1
  @outcome:model-connection-host-equivalence-findings
  @outcome-contract:model-connection-conformance-evidence.v1
  @outcome-terminal
  Scenario: Detect CLI projected consumer and MCP semantic divergence
    Given equivalent fixture requests executed through every declared interface host against the same projected capability and fake effects
    When carrier, disposition, evidence meaning, lineage, and non-claims are compared
    Then all hosts are semantically equivalent or each divergent host and field is named without treating transport shape as semantic authority

  @scenario:reject-unclosed-model-connection-runtime
  @input:unclosed-model-connection-runtime-conformance-request
  @input-contract:verify-model-connection-conformance-input.v1
  @event:model-connection-runtime-conformance-verification-requested
  @event-authority:reject-unclosed-model-connection-runtime.v1
  @outcome:unclosed-model-connection-runtime-findings
  @outcome-contract:model-connection-conformance-evidence.v1
  @outcome-terminal
  Scenario: Refuse conformance when runtime self-containment is open
    Given a runtime closure with a sibling import, source loader, development-only or mutable package, missing artifact, digest drift, unsafe path, or missing host obligation
    When model connection conformance is requested
    Then verification is held with the runtime-closure findings and no fixture result can override missing deployment authority

  @scenario:reject-nondeterministic-or-live-conformance-fixture
  @input:nondeterministic-or-live-model-conformance-fixture
  @input-contract:verify-model-connection-conformance-input.v1
  @event:model-conformance-fixture-isolation-verification-requested
  @event-authority:reject-nondeterministic-or-live-conformance-fixture.v1
  @outcome:model-conformance-fixture-isolation-findings
  @outcome-contract:model-connection-conformance-evidence.v1
  @outcome-terminal
  Scenario: Reject fixtures requiring real secrets networks clocks entropy or providers
    Given a conformance fixture that reads a live credential, contacts DNS or a remote endpoint, uses unbound wall time or randomness, or depends on provider availability
    When deterministic fixture isolation is evaluated
    Then the fixture is rejected with its undeclared effect and no live success or failure is accepted as deterministic conformance evidence
