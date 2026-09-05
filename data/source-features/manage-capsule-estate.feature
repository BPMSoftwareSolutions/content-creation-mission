Feature: Operate a capsule estate from bootstrap authority
  As a capsule-estate operator
  I want every estate operation to advance through explicit Scenario cells
  So that capsule authority can be verified, reconstructed, executed, projected, and migrated without hidden control flow

  Scenario: Admit one Capsule Manager command
    Given a process invocation with argv, optional stdin, and environment
    When the command-admission event occurs
    Then exactly one supported command variant is selected with its exact operands

  Scenario: Verify the capsule estate
    Given the verify command has been admitted
    When the estate is loaded, validated, and checked for collapsed durable layout
    Then capabilityCount, entryCount, and expandedCapabilityRoot are available

  Scenario: Resolve capsule dependencies and tool roots
    Given the resolve command has been admitted
    When internal bindings, external bindings, and tool roots are resolved
    Then declaredDependencies, present, toolRootsDeclared, and toolRootsPresent are available

  Scenario: List eligible capsules
    Given the list command and optional query have been admitted
    When the verified estate is filtered and projected
    Then capsules contains the matching capsule summaries

  Scenario: Inspect one capsule
    Given the inspect command and capsule identity have been admitted
    When the verified capsule is selected and described without expansion
    Then capabilityId, lineage, runtimeBindings, fixtures, and entries are available

  Scenario: Prove direct execution
    Given the direct or test command and optional selection have been admitted
    When packed runtime entries are reconstructed and their fixtures execute
    Then eligible, reconstructedEntryCount, fixtureCount, tests, passed, failed, and broken are available

  Scenario: Invoke one capability
    Given the invoke command, capsule identity, and canonical JSON input have been admitted
    When the verified and resolved runtime is reconstructed and executed
    Then disposition, outcome, and executions are available

  Scenario: Expand the capsule estate
    Given the expand command and non-durable target have been admitted
    When collision-safe entries are materialized and reconciled
    Then capabilityCount, entryCount, and targetRoot are available

  Scenario: Project the capsule estate
    Given the project command and non-durable target have been admitted
    When capabilities are ordered by dependency and projected
    Then eligible, projected, broken, and targetRoot are available

  Scenario: Prove capsule-first operation
    Given the proof command is running in an owned sterile root
    When verification, resolution, direct execution, expansion, projection, and aggregate tests complete
    Then proofType, capsuleCount, capsuleEntryCount, dependencies, directExecution, expansion, projection, proof, and broken are available

  Scenario: Run the sterile proof
    Given the sterile-proof command has been admitted against a collapsed source repository
    When an owned sterile checkout is staged, proved, and removed
    Then sterileRoot and status are available

  Scenario: Migrate the legacy capsule estate
    Given the migrate-legacy command has been admitted
    When legacy packs are discovered, runtime-closed, and durably written
    Then capabilityCount, adoptedRuntimeClosedCount, capsuleRoot, and estateManifestPath are available
