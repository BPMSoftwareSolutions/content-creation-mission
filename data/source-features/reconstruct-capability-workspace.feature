@capability:reconstruct-capability-workspace
@root-scenario:reconstruct-capability-workspace
Feature: Reconstruct one capability workspace from its capsule entries

  Store the capability. Project the explanation. Execute the effect.

  This capability owns the explicit expansion projection. Its input is
  the verified entry set of one physical capability capsule with the
  required authority reference list. Its outcome is
  WORKSPACE_RECONSTRUCTED or RECONSTRUCTION_HELD. Every entry digest
  verifies against its embedded bytes, every required authority
  reference is covered, and no entry reference escapes the capsule
  reference space. Expansion is the disposable projection: the capsule
  remains the durable asset.

  @scenario:reconstruct-capability-workspace
  @input:capability-workspace-reconstruction-record
  @input-contract:capability-workspace-reconstruction-record.v1
  @event:capability-workspace-reconstruction-requested
  @event-authority:reconstruct-capability-workspace.v1
  @outcome:capability-workspace-reconstruction-record
  @outcome-contract:capability-workspace-reconstruction-record.v1
  @outcome-terminal
  Scenario: Reconstruct one capability workspace from its capsule entries
    Given one verified capsule entry set and one required authority reference list
    When the workspace is reconstructed
    Then the workspace is WORKSPACE_RECONSTRUCTED or RECONSTRUCTION_HELD with the exact holding finding, and a receipt binds capsule digest, entry digests, and disposition

  @scenario:verify-entry-integrity
  @input:capability-workspace-reconstruction-record
  @input-contract:capability-workspace-reconstruction-record.v1
  @event:entry-integrity-verification-requested
  @event-authority:verify-entry-integrity.v1
  @outcome:capability-workspace-reconstruction-record
  @outcome-contract:capability-workspace-reconstruction-record.v1
  @outcome-terminal
  Scenario: Verify the entry integrity and reference space
    Given one capsule entry set
    When entry integrity verification is evaluated
    Then at least one entry is declared, every entry digest equals the digest of its embedded bytes, and no entry reference contains a parent traversal, reporting WORKSPACE_ENTRIES_ABSENT, ENTRY_DIGEST_DIVERGED, or PATH_TRAVERSAL_REJECTED otherwise

  @scenario:verify-required-coverage
  @input:capability-workspace-reconstruction-record
  @input-contract:capability-workspace-reconstruction-record.v1
  @event:required-coverage-verification-requested
  @event-authority:verify-required-coverage.v1
  @outcome:capability-workspace-reconstruction-record
  @outcome-contract:capability-workspace-reconstruction-record.v1
  @outcome-terminal
  Scenario: Verify the required authority coverage
    Given one required authority reference list and one capsule entry set
    When required coverage verification is evaluated
    Then every required authority reference is covered by an entry, reporting REQUIRED_ENTRY_ABSENT otherwise

  @scenario:bind-reconstruction-receipt
  @input:capability-workspace-reconstruction-record
  @input-contract:capability-workspace-reconstruction-record.v1
  @event:reconstruction-receipt-binding-requested
  @event-authority:bind-reconstruction-receipt.v1
  @outcome:capability-workspace-reconstruction-record
  @outcome-contract:capability-workspace-reconstruction-record.v1
  @outcome-terminal
  Scenario: Bind one reconstruction receipt
    Given one reconstruction disposition over one capsule entry set
    When the reconstruction receipt is bound
    Then the capsule digest, entry digests, and disposition bind into one replayable reconstruction receipt
