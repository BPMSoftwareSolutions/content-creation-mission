@capability:admit-capsule-execution-closure
@root-scenario:admit-capsule-execution-closure
Feature: Admit one capsule execution closure without expansion

  Store the capability. Project the explanation. Execute the effect.

  This capability owns the no-expansion execution closure law. Its
  input is the physical capsule bytes, the declared capsule digest, and
  the required execution entry reference list. Its outcome is
  EXECUTION_CLOSURE_ADMITTED or EXECUTION_CLOSURE_HELD. The capsule
  decodes, its digest verifies, and every entry required to execute the
  capability in memory — execution authorities, semantic
  transformations, interfaces, scenario corpus, and semantic graph — is
  present inside the capsule with verified digests. Nothing expands to
  disk.

  @scenario:admit-capsule-execution-closure
  @input:capsule-execution-closure-record
  @input-contract:capsule-execution-closure-record.v1
  @event:capsule-execution-closure-admission-requested
  @event-authority:admit-capsule-execution-closure.v1
  @outcome:capsule-execution-closure-record
  @outcome-contract:capsule-execution-closure-record.v1
  @outcome-terminal
  Scenario: Admit one capsule execution closure without expansion
    Given one physical capsule byte sequence, one declared capsule digest, and one required execution entry reference list
    When the execution closure is admitted
    Then the closure is EXECUTION_CLOSURE_ADMITTED or EXECUTION_CLOSURE_HELD with the exact holding finding, and a receipt binds capsule digest, required entries, and disposition

  @scenario:verify-closure-digest
  @input:capsule-execution-closure-record
  @input-contract:capsule-execution-closure-record.v1
  @event:closure-digest-verification-requested
  @event-authority:verify-closure-digest.v1
  @outcome:capsule-execution-closure-record
  @outcome-contract:capsule-execution-closure-record.v1
  @outcome-terminal
  Scenario: Verify the closure digest over the physical capsule
    Given one physical capsule byte sequence and one declared capsule digest
    When closure digest verification is evaluated
    Then the recomputed digest of the decoded bytes equals the declared digest, reporting CAPSULE_DIGEST_DIVERGED otherwise

  @scenario:verify-execution-entries
  @input:capsule-execution-closure-record
  @input-contract:capsule-execution-closure-record.v1
  @event:execution-entries-verification-requested
  @event-authority:verify-execution-entries.v1
  @outcome:capsule-execution-closure-record
  @outcome-contract:capsule-execution-closure-record.v1
  @outcome-terminal
  Scenario: Verify the required execution entries inside the capsule
    Given one decoded capsule manifest and one required execution entry reference list
    When execution entry verification is evaluated
    Then every required execution entry is present in the manifest with a verified digest, reporting EXECUTION_ENTRY_ABSENT or ENTRY_DIGEST_DIVERGED otherwise

  @scenario:bind-closure-receipt
  @input:capsule-execution-closure-record
  @input-contract:capsule-execution-closure-record.v1
  @event:closure-receipt-binding-requested
  @event-authority:bind-closure-receipt.v1
  @outcome:capsule-execution-closure-record
  @outcome-contract:capsule-execution-closure-record.v1
  @outcome-terminal
  Scenario: Bind one execution closure receipt
    Given one closure disposition over one physical capsule
    When the closure receipt is bound
    Then the capsule digest, required execution entries, and disposition bind into one replayable execution closure receipt
  @scenario:verify-declared-dependency-closure
  @input:capsule-execution-closure-record
  @input-contract:capsule-execution-closure-record.v1
  @event:declared-dependency-closure-verification-requested
  @event-authority:verify-declared-dependency-closure.v1
  @outcome:capsule-execution-closure-record
  @outcome-contract:capsule-execution-closure-record.v1
  @outcome-terminal
  Scenario: Resolve every declared external dependency by identity and digest
    Given one capsule carrying its declared dependencies and external tool roots, and one bounded set of dependency observations
    When the declared dependency closure is resolved
    Then every declared dependency resolves PRESENT, MISSING, or WRONG_DIGEST by its declared identity and digest, an undeclared nearby artifact never satisfies a dependency, and the closure is DEPENDENCY_CLOSURE_ADMITTED only when every declared dependency and external tool root resolves PRESENT
