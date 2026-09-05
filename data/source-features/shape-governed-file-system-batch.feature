@capability:shape-governed-file-system-batch
@root-scenario:shape-governed-file-system-batch
@authoring-profile:pure-sda-authority-candidate.v1
Feature: Shape one governed batch of file-system mappings

  One caller declares a bounded source authority, a bounded target authority,
  an ordered set of copy or move mappings, explicit conflict policy, and proof
  requirements. This capability owns every semantic decision between that
  declaration and one attributable shaping receipt. Platform-relative path
  resolution, physical file-system observation, and mutation remain explicit
  effect responsibilities whose results are testimony; neither an effect
  provider nor a successful process exit may authorize the batch or establish
  verification.

  The complete batch is admitted and resolved before mutation. Mapping
  identities and target paths are unique. Source and target paths are relative
  to their declared roots. Absolute paths, traversal, symbolic links, missing
  sources, non-file sources, incompatible targets, and unauthorized
  replacement reject the complete batch before mutation. An existing target
  with the declared source content is a satisfied mapping and is not rewritten.
  A mapping that declares an expected source digest is rejected before mutation
  when the observed source bytes do not match it. Copy preserves its source.
  Move removes its source only as declared. Every changed mapping is
  hash-verified after the effect. Any effect or verification failure remains
  attributable and cannot be reported as complete.

  The capability authority contains no provider workspace, tool root,
  environment-specific file-system location, executable source, projection
  result, or generated acceptance flag. A provider supplies bounded facts and
  performs only an already-authorized plan. Current materialization and evidence
  publication consumers may depend on this capability without depending on the
  historical fs-shaper workspace.

  The exact admitted physical dependency is
  sda-governed-file-system-shaping-port.v2. The path-resolution scenario binds
  it with mode resolve-bounded-paths, shapePath payload.shape,
  sourceRootPath payload.sourceRootRef, targetRootPath payload.targetRootRef,
  and lineageMode retain-effect-lineage. The observation scenario binds it with
  mode observe-bounded-mappings, shapePath payload.shape,
  sourceRootPath payload.sourceRootRef, targetRootPath payload.targetRootRef,
  and lineageMode retain-effect-lineage. The execution scenario binds the same
  platform capability with mode execute-authorized-plan, planPath plan,
  sourceRootPath sourceRootRef, targetRootPath targetRootRef, and lineageMode
  retain-effect-lineage. No provider reference, provider root, nested capability
  binding, binding digest, or capability-authority digest is part of any port
  configuration.

  Canonical circuit blueprint review projection

    CAPABILITY  shape-governed-file-system-batch
       |
       v
    [delegate request]
       |
       v
    [admit declaration] -- NON_ADMISSIBLE ----------------------+
       | ADMITTED                                                |
       v                                                         |
    [resolve bounded paths] -- NON_ADMISSIBLE -------------------+
       | ADMISSIBLE                                              |
       v                                                         |
    [observe mapping facts] -- OBSERVATION_FAILED -----------+   |
       | OBSERVED                                            |   |
       v                                                     |   |
    [resolve complete plan] -- REJECTED -------------------------+
       | SATISFIED ------------------------------+            |   |
       | AUTHORIZED                              |            |   |
       v                                         |            |   |
    [execute authorized plan] -- EFFECT_FAILED --|------------+   |
       | EFFECT_OBSERVED                         |            |   |
       v                                         |            |   |
    [verify observed effect] -- NOT_VERIFIED ----|------------+   |
       | VERIFIED                                |            |   |
       v                                         v            v   v
    [issue applied or satisfied receipt]   [retain failure] [reject]

  The tagged Input/Event/Outcome geometry below is the semantic authority for
  every blueprint cell and route. The map above is only its human review
  projection and cannot introduce a second meaning.

  @scenario:shape-governed-file-system-batch
  @input:governed-file-system-shape-request
  @input-contract:governed-file-system-shape-request.v1
  @event:shape-governed-file-system-batch
  @event-authority:shape-governed-file-system-batch.v1
  @outcome:governed-file-system-shape-request-delegated
  @outcome-contract:governed-file-system-shape-request.v1
  Scenario: Delegate one declared shape into the governed circuit
    Given one declared batch shape with bounded source and target authorities, ordered mappings, policy, proof requirements, and request lineage
    When governed file-system shaping is requested
    Then the unchanged declaration enters its canonical blueprint route without a provider, mutation, verification, or completion fact being fabricated

  @scenario:admit-governed-file-system-shape-request
  @input:governed-file-system-shape-request
  @input-contract:governed-file-system-shape-request.v1
  @event:admit-governed-file-system-shape-request
  @event-authority:admit-governed-file-system-shape-request.v1
  @outcome:governed-file-system-shape-admission
  @outcome-contract:governed-file-system-shape-admission.v1
  Scenario: Admit only one complete unambiguous batch declaration
    Given one declared batch shape and the admitted shape, policy, mapping, proof, and lineage contracts
    When contract closure, authority identity, stable mapping order, unique mapping identity, unique target identity, supported copy-or-move operation, policy completeness, and proof completeness are evaluated
    Then one admission disposition preserves the exact declaration or returns stable findings and makes observation, planning, and mutation ineligible

  @scenario:resolve-bounded-file-system-mapping-paths
  @input:admitted-file-system-shape-context
  @input-contract:admitted-file-system-shape-context.v1
  @event:resolve-bounded-file-system-mapping-paths
  @event-authority:resolve-bounded-file-system-mapping-paths.v1
  @outcome:bounded-file-system-mapping-paths
  @outcome-contract:bounded-file-system-mapping-paths.v1
  Scenario: Resolve every mapping beneath its declared authority
    Given one admitted batch declaration with source and target root authorities
    When every declared source and target path is normalized and checked against its owning root
    Then one stable ordered mapping set contains only authority-relative non-traversing paths or returns exact path findings and makes observation, planning, and mutation ineligible

  @scenario:observe-file-system-mapping-facts
  @input:bounded-file-system-mapping-observation-request
  @input-contract:bounded-file-system-mapping-observation-request.v1
  @event:observe-file-system-mapping-facts
  @event-authority:observe-file-system-mapping-facts.v1
  @outcome:file-system-mapping-fact-testimony
  @outcome-contract:file-system-mapping-fact-testimony.v1
  Scenario: Observe only the bounded facts required to resolve the batch
    Given one bounded ordered mapping set and an admitted file-system observation responsibility
    When source existence, source kind, target existence, target kind, symbolic-link status, and required content hashes are observed for every mapping
    Then one lineage-bound fact set covers every declared mapping exactly once, or an attributable observation failure is retained without authorizing or performing mutation

  @scenario:resolve-complete-file-system-shape-plan
  @input:file-system-shape-resolution-context
  @input-contract:file-system-shape-resolution-context.v1
  @event:resolve-complete-file-system-shape-plan
  @event-authority:resolve-complete-file-system-shape-plan.v1
  @outcome:resolved-file-system-shape-plan
  @outcome-contract:resolved-file-system-shape-plan.v1
  Scenario: Resolve the whole batch before any mutation
    Given one admitted declaration, bounded mapping paths, and complete observed mapping facts
    When missing or non-file sources, declared source-digest mismatch, symbolic links, incompatible targets, conflict policy, content equality, copy preservation, move removal, operation order, and proof obligations are resolved
    Then one deterministic plan is either rejected with zero authorized operations, satisfied with only verified no-op mappings, or authorized with the exact ordered operations and post-effect verification obligations

  @scenario:reject-non-admissible-file-system-shape
  @input:rejected-file-system-shape-context
  @input-contract:rejected-file-system-shape-context.v1
  @event:reject-non-admissible-file-system-shape
  @event-authority:reject-non-admissible-file-system-shape.v1
  @outcome:rejected-file-system-shape-receipt
  @outcome-contract:governed-file-system-shape-result.v1
  @outcome-terminal
  Scenario: Reject the complete batch before mutation
    Given declaration, path, observation, or plan findings that make the batch non-admissible
    When the rejected route closes
    Then one receipt identifies every stable finding, zero authorized or applied operations, complete request and observation lineage, and explicit false mutation and completion claims

  @scenario:execute-authorized-file-system-shape-plan
  @input:authorized-file-system-shape-plan
  @input-contract:authorized-file-system-shape-plan.v1
  @event:execute-authorized-file-system-shape-plan
  @event-authority:execute-authorized-file-system-shape-plan.v1
  @outcome:file-system-shape-effect-testimony
  @outcome-contract:file-system-shape-effect-testimony.v1
  Scenario: Perform only the already-authorized ordered operations
    Given one authorized content-addressed plan and an admitted file-system mutation responsibility
    When the exact ordered directory, copy, move, replacement, and no-op operations are requested
    Then one lineage-bound effect testimony reports each attempted operation and observed disposition without adding, reordering, authorizing, verifying, or claiming completion for any operation

  @scenario:verify-file-system-shape-effect
  @input:file-system-shape-verification-context
  @input-contract:file-system-shape-verification-context.v1
  @event:verify-file-system-shape-effect
  @event-authority:verify-file-system-shape-effect.v1
  @outcome:verified-file-system-shape-disposition
  @outcome-contract:verified-file-system-shape-disposition.v1
  Scenario: Verify every promised mapping from observed post-effect facts
    Given one authorized plan, its effect testimony, and bounded post-effect observations
    When target content hashes, copy-source preservation, move-source absence, mapping cardinality, operation identity, order, and effect lineage are evaluated
    Then one verified disposition closes every declared mapping exactly once or returns exact non-verification findings without upgrading partial or failed testimony to success

  @scenario:retain-incomplete-file-system-shape-effect
  @input:incomplete-file-system-shape-effect-context
  @input-contract:incomplete-file-system-shape-effect-context.v1
  @event:retain-incomplete-file-system-shape-effect
  @event-authority:retain-incomplete-file-system-shape-effect.v1
  @outcome:incomplete-file-system-shape-receipt
  @outcome-contract:governed-file-system-shape-result.v1
  @outcome-terminal
  Scenario: Retain an attributable incomplete effect without a completion claim
    Given one observation, mutation, or verification failure with the last admitted plan and all available per-operation testimony
    When the incomplete route closes
    Then one receipt identifies attempted, verified, satisfied, failed, and unattempted mappings with exact findings and lineage while completion remains false

  @scenario:issue-governed-file-system-shape-receipt
  @input:verified-file-system-shape-context
  @input-contract:verified-file-system-shape-context.v1
  @event:issue-governed-file-system-shape-receipt
  @event-authority:issue-governed-file-system-shape-receipt.v1
  @outcome:governed-file-system-shape-receipt
  @outcome-contract:governed-file-system-shape-result.v1
  @outcome-terminal
  Scenario: Issue an applied or already-satisfied receipt only after proof closes
    Given one satisfied plan or one completely verified applied plan with exact mapping, operation, hash, and lineage evidence
    When terminal receipt authority is evaluated
    Then one content-addressed receipt reports SHAPE_ALREADY_SATISFIED or SHAPE_APPLIED with exact per-mapping evidence and counts while admission, projection, promotion, and downstream acceptance remain unclaimed
