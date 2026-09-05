@capability:operate-tooling-migration-conveyor
@root-scenario:operate-tooling-migration-conveyor
Feature: Operate the tooling migration conveyor from declared capability authority

  Together with the separately projected operate-tooling-migration-inventory
  capability, this capability replaces the complete hand-authored
  implementation formerly located at capabilities/tooling-migration-runtime/
  node/tooling-migration-operation-provider.mjs. That deleted source path is
  retained here only as the historical responsibility map. No executable
  binding to its operation-specific native port remains in the active circuit.

  The conveyor is a projected semantic composition. It may invoke only pinned
  projected capability bindings and generic admitted effect capabilities. It
  must never bind an operation-specific native provider, dynamically import an
  executable provider, embed executable source in authority, infer migration
  semantics from repository layout, or delegate any part of this responsibility
  back to tooling-migration-operation-provider.mjs.

  Tooling migration proof state is authority-projected. The declared proof
  authority names every governed capability, scenario responsibility, feature,
  workspace, physical projection digest, fixture authority, active binding,
  target-conformance result, oracle-equivalence result, and gate result that may
  participate. The checked-in physical projections are the durable receipts;
  an ignored model response or runtime evidence file cannot be required to
  resolve VERIFIED or PROMOTED meaning. Adding or changing proof state is an
  authority change suitable for later database storage.

  The replacement circuit invokes projected capabilities for bounded repository
  observation and deterministic migration decisions. The remaining mechanics
  are semantic transformations over the declared proof authority: they select a
  proof, construct its operation plan, retain its physical-projection evidence,
  and shape the public outcome. Every nested binding and capability-authority
  digest is pinned in version-controlled semantic authority. Only projected
  deterministic decision authority may determine evidence disposition or
  finalize a run.

  This feature covers the original source responsibilities as follows:
  - lines 16-153: declared authority observation, digest lineage, and invocation
    of the projected decide-tooling-migration capability;
  - lines 155-196: authority-projected inventory construction and classification;
  - lines 197-268: immutable authoring-testimony verification and bounded target
    projection/execution planning;
  - lines 269-339: one-binding replacement, full-gate evaluation, exact rollback,
    and frozen operational-oracle comparison;
  - lines 340-446: complete verification, deterministic disposition, and durable
    evidence publication;
  - lines 447-509: selected-operation routing and stable serial run finalization.

  @scenario:operate-tooling-migration-conveyor
  @input:tooling-migration-operation-request
  @input-contract:tooling-migration-operation-request.v1
  @event:operate-tooling-migration-conveyor
  @event-authority:operate-tooling-migration-conveyor.v1
  @outcome:tooling-migration-operation-request-delegated
  @outcome-contract:tooling-migration-operation-context.v1
  Scenario: Delegate one admitted tooling migration operation
    Given one verify, promote, or run request and the pinned tooling migration proof authority
    When the projected conveyor is invoked
    Then one immutable operation context preserves the request, operation identity, authority reference, and request lineage without executing an effect or claiming a migration disposition

  @scenario:observe-declared-tooling-migration-authority
  @input:tooling-migration-operation-context
  @input-contract:tooling-migration-operation-context.v1
  @event:observe-declared-tooling-migration-authority
  @event-authority:observe-declared-tooling-migration-authority.v1
  @outcome:observed-tooling-migration-authority
  @outcome-contract:observed-tooling-migration-authority.v1
  Scenario: Observe the exact declared migration registry
    Given one immutable operation context and a pinned projected observe-governed-repository binding
    When the declared migration registry bytes and digest are observed once
    Then the exact registry testimony, explicit absence findings, and nested execution lineage are retained without enumerating folders, interpreting physical structure, or fabricating an inventory entry

  @scenario:construct-declared-tooling-migration-operation-plan
  @input:observed-tooling-migration-authority
  @input-contract:observed-tooling-migration-authority.v1
  @event:construct-declared-tooling-migration-operation-plan
  @event-authority:construct-declared-tooling-migration-operation-plan.v1
  @outcome:declared-tooling-migration-operation-plan
  @outcome-contract:declared-tooling-migration-operation-plan.v1
  Scenario: Resolve the complete bounded projected-capability composition
    Given an observed declared registry and one admitted operation request
    When the semantic plan transformation selects the declared physical projection proofs and constructs the exact decision request
    Then one stable bounded proof plan names only declared projected capability receipts, target results, binding identities, gate results, and evidence policy without embedding executable source or an operation-specific native provider

  @scenario:execute-declared-tooling-migration-operation-plan
  @input:declared-tooling-migration-operation-plan
  @input-contract:declared-tooling-migration-operation-plan.v1
  @event:execute-declared-tooling-migration-operation-plan
  @event-authority:execute-declared-tooling-migration-operation-plan.v1
  @outcome:observed-tooling-migration-operation
  @outcome-contract:observed-tooling-migration-operation.v1
  Scenario: Execute only the declared projected capability transactions
    Given one stable bounded proof plan backed by checked-in physical projections
    When the semantic execution transformation retains the declared proof results
    Then complete projection, target, oracle, binding, and gate testimony is retained without rerunning an ignored authoring artifact or invoking undeclared work

  @scenario:resolve-tooling-migration-operation-disposition
  @input:observed-tooling-migration-operation
  @input-contract:observed-tooling-migration-operation.v1
  @event:resolve-tooling-migration-operation-disposition
  @event-authority:resolve-tooling-migration-operation-disposition.v1
  @outcome:resolved-tooling-migration-operation
  @outcome-contract:resolved-tooling-migration-operation.v1
  Scenario: Derive the terminal operation and interface dispositions
    Given complete declared operation testimony and nested effect lineage
    When the pinned projected decide-tooling-migration capability evaluates inventory classification, verification, gate, continuation, evidence, and final-run decisions applicable to the operation
    Then the exact INVENTORIED, VERIFIED, PROMOTED, REJECTED, COMPLETED, or COMPLETED_WITH_REJECTIONS disposition and ZERO or NONZERO interface exit disposition are returned without accepting model testimony or effect self-assertion as authority

  @scenario:publish-declared-tooling-migration-operation-evidence
  @input:resolved-tooling-migration-operation
  @input-contract:resolved-tooling-migration-operation.v1
  @event:publish-declared-tooling-migration-operation-evidence
  @event-authority:publish-declared-tooling-migration-operation-evidence.v1
  @outcome:tooling-migration-operation-evidence
  @outcome-contract:tooling-migration-operation-evidence.v1
  @outcome-terminal
  Scenario: Publish the version-controlled and bounded operation evidence
    Given one resolved operation with complete authority, child-capability, effect, equality, rollback, and decision lineage
    When the semantic publication transformation materializes the declared evidence envelope
    Then the public operation outcome is returned with unchanged dispositions, and projected capability workspaces remain the physical conformance receipts without relying on an ignored artifact as proof
