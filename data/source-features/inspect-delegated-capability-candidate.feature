@capability:inspect-delegated-capability-candidate
@root-scenario:inspect-delegated-capability-candidate
Feature: Inspect one delegated capability candidate before source materialization

  A downstream authoring circuit supplies immutable canonical feature bytes,
  immutable structured candidate testimony, and the fixed eleven-slot
  authoring profile. This capability deterministically derives the complete
  feature identity set and checks whether the opaque candidate strings form a
  closed declarative SDA source bundle. It does not author, repair, replace,
  materialize, project, accept, or promote candidate content.

  The inspection boundary turns a model-produced opaque-string limitation into
  attributable machine evidence. Every declared capability, scenario, input,
  event, outcome, input-contract, outcome-contract, terminal marker, artifact
  slot, and non-claim is retained in stable order. Every string is parsed as
  JSON before any artifact-specific check. A failure identifies the first
  bounded location while retaining all prior observations and hashes.

  Candidate-slot conformance is deliberately narrower than ordinary SDA source
  admission. It establishes only that the exact eleven testimony strings are
  parseable, feature-derived, archetype-shaped, contract-closed, fixture-shaped,
  cross-file closed, and non-claiming enough to submit unchanged to ordinary
  source admission. Ordinary SDA admission, projection, behavioral conformance,
  acceptance, and promotion remain separate authorities.

  @scenario:inspect-delegated-capability-candidate
  @input:delegated-capability-candidate-inspection-request
  @input-contract:delegated-capability-candidate-inspection-request.v1
  @event:inspect-delegated-capability-candidate
  @event-authority:inspect-delegated-capability-candidate.v1
  @outcome:candidate-slot-admission-evidence
  @outcome-contract:candidate-slot-admission-evidence.v1
  Scenario: Return deterministic candidate-slot inspection evidence
    Given one immutable canonical feature, one immutable structured candidate response, and one fixed eleven-slot profile
    When feature-derived identities and every candidate slot are inspected through declared deterministic authorities
    Then CONFORMS_FOR_SOURCE_SUBMISSION or REJECTED is returned with exact findings, hashes, and retained evidence without an authoring, source-admission, projection, acceptance, or promotion claim

  @scenario:observe-delegated-candidate-inspection-inputs
  @input:delegated-capability-candidate-inspection-request
  @input-contract:delegated-capability-candidate-inspection-request.v1
  @event:observe-delegated-candidate-inspection-inputs
  @event-authority:observe-delegated-candidate-inspection-inputs.v1
  @outcome:observed-delegated-candidate-inspection-inputs
  @outcome-contract:observed-delegated-candidate-inspection-inputs.v1
  Scenario: Observe immutable feature, response, and profile evidence
    Given governed repository references for one feature, one normalized model response, and one fixed profile authority
    When their exact bytes, digests, and declared logical names are observed without mutation
    Then immutable observed evidence and attributable observation findings are retained in stable declared order

  @scenario:derive-feature-derived-candidate-slot-scope
  @input:observed-delegated-candidate-inspection-inputs
  @input-contract:observed-delegated-candidate-inspection-inputs.v1
  @event:derive-feature-derived-candidate-slot-scope
  @event-authority:derive-feature-derived-candidate-slot-scope.v1
  @outcome:feature-derived-candidate-slot-scope
  @outcome-contract:feature-derived-candidate-slot-scope.v1
  Scenario: Freeze identities and required candidate surface
    Given immutable feature annotations and the fixed eleven logical artifact slots
    When every declared semantic identity and unique carrier contract identity is extracted in annotation order
    Then one bounded scope fixes the expected slots, artifact archetypes, contract-bundle mappings, feature connectors, fixture rules, cross-file references, and required non-claims

  @scenario:inspect-declarative-candidate-artifact-slots
  @input:feature-derived-candidate-slot-scope
  @input-contract:feature-derived-candidate-slot-scope.v1
  @event:inspect-declarative-candidate-artifact-slots
  @event-authority:inspect-declarative-candidate-artifact-slots.v1
  @outcome:inspected-declarative-candidate-artifact-slots
  @outcome-contract:inspected-declarative-candidate-artifact-slots.v1
  Scenario: Parse and inspect all fixed candidate artifacts
    Given one bounded feature-derived scope and eleven immutable candidate artifact strings
    When every slot is parsed as JSON and inspected against its admitted SDA artifact-specific root archetype
    Then exact parse, executable-content, identity, contract-catalog, schema-bundle, authority-reference, fixture, and non-claim findings are retained without changing a candidate byte

  @scenario:resolve-declarative-candidate-slot-disposition
  @input:inspected-declarative-candidate-artifact-slots
  @input-contract:inspected-declarative-candidate-artifact-slots.v1
  @event:resolve-declarative-candidate-slot-disposition
  @event-authority:resolve-declarative-candidate-slot-disposition.v1
  @outcome:candidate-slot-admission-evidence
  @outcome-contract:candidate-slot-admission-evidence.v1
  @outcome-terminal
  Scenario: Resolve submission readiness without accepting the candidate
    Given complete immutable observations and deterministic slot findings
    When artifact envelope, JSON parsing, feature identity preservation, contract closure, admitted archetype shape, cross-file closure, fixture closure, and non-claims are evaluated in fixed order
    Then CONFORMS_FOR_SOURCE_SUBMISSION is returned only when every inspection obligation passes, otherwise REJECTED identifies the first attributable finding and the complete inspection evidence remains available to bounded curation or regeneration
