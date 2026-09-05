@capability:materialize-authorized-file-batch
@root-scenario:materialize-authorized-file-batch
@lifecycle:FIRST_ADMISSION
Feature: Materialize one authorized batch of exact file bytes

  A caller supplies one disposable external-root authority and a non-empty ordered
  batch of content-addressed file mappings. The capability derives one canonical
  authorized plan, delegates exactly that plan to an admitted generic filesystem
  mechanic, and returns bounded post-effect testimony for every mapping.

  The capability is domain-neutral. It knows nothing about capsules, expansion,
  Reveal, repositories, projectors, or any consumer-specific layout. It neither
  discovers a destination nor grants authority to one. The caller supplies the
  target root, relative target paths, exact base64 bytes, expected SHA-256 digests,
  and per-target existence policy.

  Absolute paths, traversal, symbolic-link crossings, malformed or divergent byte
  testimony, duplicate or colliding targets, incompatible existing targets, and
  post-effect digest divergence fail closed. The complete batch is validated before
  the target root is created or any file is written. Repeating an exact authorized
  request is idempotent only where allow-exact-match is explicitly declared.

  Success reports file paths, byte lengths, content hashes, per-mapping results,
  and effect lineage without returning encoded content bytes. REQUEST_REJECTED and
  EFFECT_FAILED remain distinct from EFFECT_OBSERVED and never claim completion.

  @scenario:materialize-authorized-file-batch
  @input:authorized-file-batch-materialization-request
  @input-contract:authorized-file-batch-materialization-request.v1
  @event:materialize-authorized-file-batch
  @event-authority:materialize-authorized-file-batch.v1
  @outcome:authorized-file-batch-materialization-outcome
  @outcome-contract:authorized-file-batch-materialization-outcome.v1
  @outcome-variants:EFFECT_OBSERVED|REQUEST_REJECTED|EFFECT_FAILED
  @outcome-terminal
  Scenario: Materialize one authorized exact-byte batch
    Given one caller-authorized disposable external root and one non-empty ordered batch of exact content-addressed file mappings
    When a canonical plan is derived, the admitted external-root materialization mechanic is invoked once, and its bounded testimony is projected
    Then return EFFECT_OBSERVED, REQUEST_REJECTED, or EFFECT_FAILED with exact per-mapping evidence and no encoded content bytes

  @scenario:derive-authorized-file-batch-plan
  @input:authorized-file-batch-materialization-request
  @input-contract:authorized-file-batch-materialization-request.v1
  @event:derive-authorized-file-batch-plan
  @event-authority:derive-authorized-file-batch-plan.v1
  @outcome:authorized-file-batch-materialization-plan
  @outcome-contract:authorized-file-batch-materialization-plan.v1
  @outcome-variants:PLAN_AUTHORIZED
  Scenario: Derive one canonical content-addressed plan
    Given one contract-admitted request containing a target-root reference, ordered mappings, exact encoded bytes, declared hashes, existence policy, and request lineage
    When the provider request, ordered operations, and canonical plan identity are derived
    Then return one AUTHORIZED content-addressed plan and bounded provider request without claiming any filesystem effect

  @scenario:materialize-authorized-file-batch-effect
  @input:authorized-file-batch-materialization-plan
  @input-contract:authorized-file-batch-materialization-plan.v1
  @event:materialize-authorized-file-batch-effect
  @event-authority:materialize-authorized-file-batch-effect.v1
  @outcome:authorized-file-batch-materialization-effect
  @outcome-contract:authorized-file-batch-materialization-effect.v1
  @outcome-variants:EFFECT_OBSERVED|REQUEST_REJECTED|EFFECT_FAILED
  Scenario: Execute only the authorized plan at the caller root
    Given one authorized plan and one caller-supplied external-root reference
    When the admitted governed external-root batch materialization mechanic is invoked exactly once
    Then return bounded per-operation effect testimony and post-effect hashes without returning encoded content bytes or adding semantic authorization

  @scenario:project-authorized-file-batch-outcome
  @input:authorized-file-batch-materialization-effect
  @input-contract:authorized-file-batch-materialization-effect.v1
  @event:project-authorized-file-batch-outcome
  @event-authority:project-authorized-file-batch-outcome.v1
  @outcome:authorized-file-batch-materialization-outcome
  @outcome-contract:authorized-file-batch-materialization-outcome.v1
  @outcome-variants:EFFECT_OBSERVED|REQUEST_REJECTED|EFFECT_FAILED
  @outcome-terminal
  Scenario: Project bounded materialization testimony
    Given one exact provider testimony with plan, operation, failure, and effect lineage evidence
    When consumer-facing outcome authority is projected
    Then preserve the terminal disposition and bounded evidence while excluding encoded content bytes and any capsule, repository, or downstream completion claim
