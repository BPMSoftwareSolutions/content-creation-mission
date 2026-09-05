@capability:operate-capsule-estate
@root-scenario:operate-capsule-estate
@lifecycle:REVISION_V2
Feature: Operate the SideFX capsule estate

  A clean checkout contains an admitted bootstrap and a capsule-only durable
  estate. The estate authority binds each capability identity to one immutable
  capsule digest and binds every capsule entry to its exact byte digest.

  This capability owns verification, dependency resolution, discovery,
  inspection, capsule-carried execution, reconstruction, projection, direct
  fixture proof, capsule-first proof, and sterile-checkout proof. It never
  accepts the durable repository as an expansion or projection target, never
  trusts an undeclared dependency or tool root, and never treats an expanded
  capability workspace as required durable state.

  Capsule-estate behavior is capability authority. It is realized only through
  admitted caller-authorized external-root observation, semantic transformation,
  exact-byte digest, artifact materialization, disposable-root lifecycle,
  consumer projection, and projected-application execution mechanics. It must
  not require a capsule-estate-specific provider in any language runtime.
  The caller supplies the current repository root as runtime authority; no
  machine path, scratch root, or checkout location is embedded in durable
  feature, blueprint, capability, capsule, or bootstrap authority.

  @scenario:operate-capsule-estate
  @input:capsule-estate-operation-request
  @input-contract:capsule-estate-operation-request.v2
  @event:capsule-estate-operation-requested
  @event-authority:operate-capsule-estate.v2
  @outcome:capsule-estate-operation-result
  @outcome-contract:capsule-estate-operation-result.v2
  @outcome-variants:VERIFIED|RESOLVED|LISTED|INSPECTED|INVOKED|DIRECT_EXECUTION_PROVED|EXPANDED|PROJECTED|CAPSULE_FIRST_PROVED|STERILE_CHECKOUT_PROVED|REQUEST_REJECTED
  @outcome-terminal
  Scenario: Dispatch one admitted capsule estate operation
    Given one operation from verify, resolve, list, inspect, invoke, expand, project, prove-direct-execution, prove-capsule-first, or prove-sterile-checkout with a caller-authorized repository root and its other required arguments
    When the capsule estate operation is requested
    Then exactly the named operation is performed through its admitted scenario and its canonical result or exact failed obligation is returned with attributable lineage

  @scenario:verify-capsule-estate
  @input:capsule-estate-operation-request
  @input-contract:capsule-estate-operation-request.v2
  @event:capsule-estate-verification-requested
  @event-authority:verify-capsule-estate.v2
  @outcome:capsule-estate-operation-result
  @outcome-contract:capsule-estate-operation-result.v2
  @outcome-variants:VERIFIED|REQUEST_REJECTED
  @outcome-terminal
  Scenario: Verify the complete capsule-only estate
    Given a verify operation and a governed repository root containing the bootstrap manifest and capsule-estate manifest
    And bounded external-root observation returns the exact bytes and SHA-256 digest of both manifests without changing the repository
    And semantic authority parses those observed manifests and derives the stable declared resource set for every capsule and every bootstrap entry
    When verification is requested
    Then bounded external-root observation returns the exact bytes and SHA-256 digest of every derived resource without directory enumeration or undeclared fallback
    And exact decoded-byte digest mechanics reproduce every capsule entry digest without UTF-8 coercion
    And semantic authority compares manifest counts, bootstrap and interface digests, capsule digests, authority digests, runtime bindings, dependency bindings, and declared tool roots
    And semantic authority proves the expanded capability root is absent from durable repository authority
    And the canonical verified result is returned or the exact failed obligation is returned with attributable lineage

  @scenario:resolve-capsule-estate-dependencies
  @input:capsule-estate-operation-request
  @input-contract:capsule-estate-operation-request.v2
  @event:capsule-estate-dependency-resolution-requested
  @event-authority:resolve-capsule-estate-dependencies.v2
  @outcome:capsule-estate-operation-result
  @outcome-contract:capsule-estate-operation-result.v2
  @outcome-variants:RESOLVED|REQUEST_REJECTED
  @outcome-terminal
  Scenario: Resolve only declared capsule dependencies and tool roots
    Given verified capsule entries containing declared capability bindings and external tool roots
    When dependency resolution is requested
    Then every dependency identity, binding digest, capability authority digest, and declared tool root is present and exact without directory-name inference or undeclared fallback

  @scenario:discover-and-inspect-capsules
  @input:capsule-estate-operation-request
  @input-contract:capsule-estate-operation-request.v2
  @event:capsule-estate-discovery-requested
  @event-authority:discover-and-inspect-capsules.v2
  @outcome:capsule-estate-operation-result
  @outcome-contract:capsule-estate-operation-result.v2
  @outcome-variants:LISTED|INSPECTED|REQUEST_REJECTED
  @outcome-terminal
  Scenario: List and inspect admitted capsules
    Given a verified estate and an optional case-insensitive identity query or one exact capability identity
    When capsule discovery or inspection is requested
    Then stable identity, lineage, target, runtime, dependency, fixture, and content-addressed entry metadata are returned and an absent identity fails as CAPSULE_NOT_FOUND

  @scenario:execute-capsule-carried-capabilities
  @input:capsule-estate-operation-request
  @input-contract:capsule-estate-operation-request.v2
  @event:capsule-carried-execution-requested
  @event-authority:execute-capsule-carried-capabilities.v2
  @outcome:capsule-estate-operation-result
  @outcome-contract:capsule-estate-operation-result.v2
  @outcome-variants:INVOKED|DIRECT_EXECUTION_PROVED|REQUEST_REJECTED
  @outcome-terminal
  Scenario: Invoke one capsule or prove selected fixtures directly
    Given one verified capsule runtime binding and either a canonical input or an optional set of capability identities
    When invocation or direct fixture proof is requested
    Then runtime entries are reconstructed into an ownership-marked disposable execution root
    And execution uses exact digest-bound projected application authority
    And fixture observations and outcomes are compared exactly
    And the disposable root is removed only through marker-bound release with post-effect absence proof

  @scenario:reconstruct-and-project-capsule-estate
  @input:capsule-estate-operation-request
  @input-contract:capsule-estate-operation-request.v2
  @event:capsule-estate-reconstruction-requested
  @event-authority:reconstruct-and-project-capsule-estate.v2
  @outcome:capsule-estate-operation-result
  @outcome-contract:capsule-estate-operation-result.v2
  @outcome-variants:EXPANDED|PROJECTED|REQUEST_REJECTED
  @outcome-terminal
  Scenario: Reconstruct and project into an explicitly selected disposable root
    Given a verified estate and a caller-authorized target root outside the durable repository
    When expansion or projection is requested
    Then canonical entry paths and shared authority are reconstructed from exact capsule bytes
    And every eligible capability is projected through the admitted consumer projector with exact authority-digest binding
    And progress remains observable
    And no source or projected capability folder is written into the durable repository

  @scenario:prove-capsule-first-checkout-closure
  @input:capsule-estate-operation-request
  @input-contract:capsule-estate-operation-request.v2
  @event:capsule-first-checkout-proof-requested
  @event-authority:prove-capsule-first-checkout-closure.v2
  @outcome:capsule-estate-operation-result
  @outcome-contract:capsule-estate-operation-result.v2
  @outcome-variants:CAPSULE_FIRST_PROVED|STERILE_CHECKOUT_PROVED|REQUEST_REJECTED
  @outcome-terminal
  Scenario: Prove capsule-first closure from an owned sterile checkout
    Given only the admitted bootstrap roots and capsule estate copied into an ownership-marked sterile root
    When capsule-first or sterile-checkout proof is requested
    Then verification, resolution, shared-authority reconstruction, direct execution, full expansion, full projection, and the aggregate conformance corpus complete with zero broken obligations
    And the owned sterile root is removed only after every required proof result is retained with attributable lineage
