@capability:verify-capability-authoring-lineage
@root-scenario:verify-capability-authoring-lineage
Feature: Verify capability authoring lineage

  A downstream consumer supplies one declared capability-authoring lineage and
  the governed locations of its immutable author request, model response,
  canonical feature, and complete candidate source bundle. The consumer
  receives deterministic lineage evidence showing whether the observed bytes,
  hashes, identities, attempt authority, feature wording, and artifact envelope
  agree with the declaration.

  This capability verifies provenance only. Model testimony remains untrusted,
  and a lineage match does not claim source admission, projection, behavioral
  conformance, equivalence, promotion, or acceptance. Repository access is
  delegated to the projected governed-repository observation capability;
  lineage comparison is declarative and does not mutate the observed evidence.

  Every rejection is attributable to one declared connector. Missing or
  additional source artifacts, request or response hash mismatches, provider or
  model identity drift, unauthorized attempt counts, structured-candidate hash
  mismatches, canonical-feature wording drift, and workbench-to-candidate hash
  mismatches remain distinct findings. Prior observations and complete nested
  execution lineage are retained in both MATCHED and REJECTED outcomes.

  @scenario:verify-capability-authoring-lineage
  @input:capability-authoring-lineage-verification-request
  @input-contract:capability-authoring-lineage-verification-request.v1
  @event:verify-capability-authoring-lineage
  @event-authority:verify-capability-authoring-lineage.v1
  @outcome:capability-authoring-lineage-verification-request-delegated
  @outcome-contract:capability-authoring-lineage-verification-request.v1
  Scenario: Delegate one capability authoring-lineage verification
    Given one declared authoring lineage and governed references for its immutable request, response, feature, workbench, and candidate bundle
    When a downstream consumer requests the declared authoring-lineage verification composition
    Then the unchanged request is delegated with its declaration lineage and no provenance, acceptance, or promotion claim is fabricated

  @scenario:resolve-capability-authoring-lineage-scope
  @input:capability-authoring-lineage-verification-request
  @input-contract:capability-authoring-lineage-verification-request.v1
  @event:resolve-capability-authoring-lineage-scope
  @event-authority:resolve-capability-authoring-lineage-scope.v1
  @outcome:bounded-capability-authoring-lineage-context
  @outcome-contract:bounded-capability-authoring-lineage-context.v1
  Scenario: Resolve the exact declared authoring evidence scope
    Given one verification request with fixed provider, model, attempt, feature, artifact-slot, and hash identities
    When the declared evidence connectors and expected artifact envelope are resolved
    Then one bounded context identifies every required observation and expected value in stable semantic identity order, or an attributable declaration finding is returned before evidence observation

  @scenario:observe-capability-authoring-lineage-evidence
  @input:bounded-capability-authoring-lineage-context
  @input-contract:bounded-capability-authoring-lineage-context.v1
  @event:observe-capability-authoring-lineage-evidence
  @event-authority:observe-capability-authoring-lineage-evidence.v1
  @outcome:observed-capability-authoring-lineage-evidence
  @outcome-contract:observed-capability-authoring-lineage-evidence.v1
  Scenario: Observe immutable authoring evidence through the governed repository capability
    Given one bounded lineage context and one pinned projected governed-repository observation binding
    When the request, response, feature, workbench artifacts, and candidate artifacts are observed without mutation
    Then exact bytes, digests, stable identities, attributable observation findings, and complete nested execution lineage are retained without interpreting model testimony as acceptance

  @scenario:compare-capability-authoring-lineage-evidence
  @input:observed-capability-authoring-lineage-evidence
  @input-contract:observed-capability-authoring-lineage-evidence.v1
  @event:compare-capability-authoring-lineage-evidence
  @event-authority:compare-capability-authoring-lineage-evidence.v1
  @outcome:capability-authoring-lineage-evidence
  @outcome-contract:capability-authoring-lineage-evidence.v1
  @outcome-terminal
  Scenario: Return a deterministic authoring-lineage disposition
    Given the declared authoring lineage and complete immutable observations in stable semantic identity order
    When request, response, provider, model, attempt, structured-candidate, feature-wording, artifact-envelope, and workbench-to-candidate equality obligations are compared
    Then MATCHED is returned only when every declared connector agrees, otherwise REJECTED is returned with the first attributable finding and all prior evidence, without claiming capability acceptance or changing any source artifact
