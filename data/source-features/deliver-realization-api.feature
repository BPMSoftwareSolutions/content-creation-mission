@capability:deliver-realization-api
@root-scenario:deliver-realization-api
Feature: Deliver the SideFX realization API over loopback HTTP

  A local consumer receives the authority-declared SideFX realization API on
  loopback only. The authority owns methods, paths, carriers, dispositions,
  and server defaults. HTTP delivery owns protocol carriers and disposable
  request state only; capsule operations and realization meaning remain bound
  to their admitted capabilities.

  Remote capsule retrieval, snapshot publication, pointer advancement,
  credential handling, authentication inference, and durable projection state
  are not admitted.

  @scenario:deliver-realization-api
  @input:realization-api-delivery-request
  @input-contract:realization-api-delivery-request.v1
  @event:realization-api-delivery-requested
  @event-authority:deliver-realization-api.v1
  @outcome:realization-api-delivery-result
  @outcome-contract:realization-api-delivery-result.v1
  @outcome-terminal
  Scenario: Start the admitted loopback realization API
    Given the sidefx-realization-api authority at version 0.1.0 with host 127.0.0.1, its admitted port, and exactly six declared operations
    When HTTP delivery is requested
    Then one loopback server starts, only authority-declared method and path pairs are routed, JSON request bodies are bounded, and JSON responses use exact status and error carriers

  @scenario:discover-realization-api-capabilities
  @input:realization-api-delivery-request
  @input-contract:realization-api-delivery-request.v1
  @event:realization-api-capability-discovery-requested
  @event-authority:discover-realization-api-capabilities.v1
  @outcome:realization-api-delivery-result
  @outcome-contract:realization-api-delivery-result.v1
  @outcome-terminal
  Scenario: List and inspect capsules through declared GET routes
    Given an optional case-insensitive query or an exact capability identity
    When GET /capabilities or GET /capabilities/:capabilityId is requested
    Then the request delegates to the bound capsule discovery operation and returns stable content-addressed capsule metadata or the exact not-found representation

  @scenario:plan-realization-api-target
  @input:realization-api-delivery-request
  @input-contract:realization-api-delivery-request.v1
  @event:realization-api-plan-requested
  @event-authority:plan-realization-api-target.v1
  @outcome:realization-api-delivery-result
  @outcome-contract:realization-api-delivery-result.v1
  @outcome-terminal
  Scenario: Plan a capability realization for one target profile
    Given a capability identity and a target operating system from windows, macos, or linux with architecture x64 or arm64
    When POST /realization-plans is requested
    Then the verified capsule, dependencies, host profile, required providers, projection eligibility, requested experience, activation, and collapsed durable layout bind into one process-local plan with disposition REALIZATION_PLANNABLE or REALIZATION_TARGET_UNAVAILABLE

  @scenario:project-realization-api-capability
  @input:realization-api-delivery-request
  @input-contract:realization-api-delivery-request.v1
  @event:realization-api-projection-requested
  @event-authority:project-realization-api-capability.v1
  @outcome:realization-api-delivery-result
  @outcome-contract:realization-api-delivery-result.v1
  @outcome-terminal
  Scenario: Project one planned capability into an owned disposable root
    Given a plannable realization plan bound to the local host target
    When POST /projections is requested
    Then an ownership-marked realization root is created beside the repository, the estate is expanded and projected there, selected direct execution is proven, and a receipt binds capsule, authority, target, runtime, provider, projection, conformance, and artifact digests

  @scenario:observe-realization-api-projection
  @input:realization-api-delivery-request
  @input-contract:realization-api-delivery-request.v1
  @event:realization-api-projection-observation-requested
  @event-authority:observe-realization-api-projection.v1
  @outcome:realization-api-delivery-result
  @outcome-contract:realization-api-delivery-result.v1
  @outcome-terminal
  Scenario: Read process-local projection status and receipt
    Given one projection identity known to the running delivery instance
    When GET /projections/:projectionId or GET /projections/:projectionId/receipt is requested
    Then PROJECTING, COMPLETE, or FAILED status is returned and a receipt is returned only after completion, while unknown identities and unavailable receipts use their exact governed representations

  @scenario:dispose-realization-api-roots
  @input:realization-api-delivery-request
  @input-contract:realization-api-delivery-request.v1
  @event:realization-api-disposal-requested
  @event-authority:dispose-realization-api-roots.v1
  @outcome:realization-api-delivery-result
  @outcome-contract:realization-api-delivery-result.v1
  @outcome-terminal
  Scenario: Remove only realization roots owned by this API
    Given process-local realization roots and sibling directories that may not belong to this server
    When startup sweeping or graceful shutdown occurs
    Then only directories beside the repository whose names and exact ownership markers prove API ownership are removed and every unowned path remains untouched
