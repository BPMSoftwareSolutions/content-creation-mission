@capability:construct-capability-author-delegate-request
@root-scenario:construct-capability-author-delegate-request
Feature: Construct a governed capability-author delegate request

  A downstream consumer supplies one reviewed canonical capability feature and
  one bounded authoring-profile identity. The Agentic Harness derives the
  complete closed model-request authority needed to ask an admitted authoring
  model for exactly eleven projectable SDA candidate artifacts.

  The consumer does not hand-author a delegate JSON document. Capability,
  scenario, input, event, outcome, and contract identities come from the
  admitted feature. Artifact slots, filenames, admitted authority archetypes,
  transformation vocabulary, response non-claims, Gemini provider authority,
  temperature zero, one-attempt authority, no-substitution policy, and evidence
  capture policy come from the governed authoring profile.

  The resulting delegate request is both returned as an admitted carrier for
  the next harness operation and published beneath a fresh governed live-request
  destination derived from its unique run identity with its exact byte hash.
  Existing destinations are rejected; a concurrent request cannot replace an
  earlier request. Construction and publication do not call
  the model, accept candidate content, project an executable, or promote a
  capability. Repeating the same feature and profile produces byte-identical
  delegate request content apart from an explicitly supplied unique run ID.

  @scenario:construct-capability-author-delegate-request
  @input:capability-author-delegate-construction-request
  @input-contract:capability-author-delegate-construction-request.v1
  @event:construct-capability-author-delegate-request
  @event-authority:construct-capability-author-delegate-request.v1
  @outcome:capability-author-delegate-construction-request-delegated
  @outcome-contract:capability-author-delegate-construction-request.v1
  Scenario: Delegate one reviewed feature into request construction
    Given one reviewed canonical feature reference, one governed authoring-profile identity, and one unique run identity
    When the downstream consumer requests a governed capability-author delegate
    Then the unchanged construction request is delegated without authoring candidate content or invoking a model

  @scenario:observe-delegate-canonical-feature
  @input:capability-author-delegate-construction-request
  @input-contract:capability-author-delegate-construction-request.v1
  @event:observe-delegate-canonical-feature
  @event-authority:observe-delegate-canonical-feature.v1
  @outcome:observed-delegate-canonical-feature
  @outcome-contract:observed-delegate-canonical-feature.v1
  Scenario: Observe the reviewed feature without mutation
    Given one governed feature reference and one pinned projected repository-observation binding
    When the canonical feature bytes and digest are observed
    Then the exact unchanged feature evidence and nested observation lineage are retained for canonical feature admission

  @scenario:resolve-delegate-authoring-profile
  @input:observed-delegate-canonical-feature
  @input-contract:observed-delegate-canonical-feature.v1
  @event:resolve-delegate-authoring-profile
  @event-authority:resolve-delegate-authoring-profile.v1
  @outcome:bounded-capability-author-delegate-profile
  @outcome-contract:bounded-capability-author-delegate-profile.v1
  Scenario: Derive the closed authoring profile from canonical connectors
    Given admitted feature bytes with declared semantic connectors and one governed authoring-profile identity
    When canonical identities, eleven fixed artifact slots, SDA archetypes, permitted transformation operations, response non-claims, and provider policies are resolved
    Then one bounded profile fixes the entire model-request surface without model-selected identities, filenames, providers, attempts, or executable mechanics

  @scenario:assemble-capability-author-delegate-request
  @input:bounded-capability-author-delegate-profile
  @input-contract:bounded-capability-author-delegate-profile.v1
  @event:assemble-capability-author-delegate-request
  @event-authority:assemble-capability-author-delegate-request.v1
  @outcome:governed-capability-author-delegate-request
  @outcome-contract:governed-capability-author-delegate-request.v1
  Scenario: Assemble the connector-ready delegate request deterministically
    Given one bounded authoring profile with fixed feature identities, artifact slots, archetypes, provider policy, response schema, and evidence policy
    When the generic-connector model request is assembled as canonical JSON
    Then one schema-valid Gemini delegate request with temperature zero, exactly one authorized attempt, no provider substitution, eleven named string slots, and explicit non-claims is returned without invoking the provider

  @scenario:publish-capability-author-delegate-request
  @input:governed-capability-author-delegate-request
  @input-contract:governed-capability-author-delegate-request.v1
  @event:publish-capability-author-delegate-request
  @event-authority:publish-capability-author-delegate-request.v1
  @outcome:published-capability-author-delegate-request
  @outcome-contract:published-capability-author-delegate-request.v1
  @outcome-terminal
  Scenario: Publish and forward the delegate request atomically
    Given one connector-ready delegate request, one fresh governed live-request destination derived from its unique run identity, and the next model-obtainment operation
    When the exact canonical request bytes are published through admitted artifact storage
    Then the request carrier, distinct immutable logical request reference, byte hash, publication lineage, and next-operation input are returned together, or an existing destination or failed publication is rejected without reporting a partial delegate file
