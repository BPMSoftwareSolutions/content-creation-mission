@capability:compare-projected-tooling-migration-oracle
@root-scenario:compare-projected-tooling-migration-oracle
Feature: Compare projected tooling migration behavior with a frozen operational oracle

  A downstream consumer supplies one projected tooling-migration observation,
  declared portable fixtures, and one frozen legacy operational oracle that is
  bound to byte-identical repository state. The consumer receives attributable
  equality evidence for the declared observations only. The capability does
  not decide verification, promotion, rollback policy, inventory state, or
  continuation of a migration run.

  The frozen oracle is an explicit governed effect responsibility. Its
  repository root, declared legacy provider and obligation evaluator, closed
  manifest of every declared relevant resource with relative path, byte digest,
  and explicit absence marker, fixture identities, and expected rollback facts
  are resolved before observation. An optional repository revision identity is
  retained as evidence only and never substitutes for the manifest bytes. Pure
  comparison may evaluate the returned facts, but it may not fabricate
  projected outcomes, oracle outcomes, obligation dispositions, repository
  equality, or rollback restoration facts.

  Equality evidence is not an acceptance claim. A mismatch is retained with
  the first attributable connector and every prior observation; it neither
  changes the frozen oracle or fixture authority nor decides whether a
  candidate is verified, promoted, or rolled back. A reported rollback fact is
  attributable only to preserved prior-binding bytes and an observed restored
  binding digest.

  @scenario:compare-projected-tooling-migration-oracle
  @input:projected-tooling-migration-oracle-comparison-request
  @input-contract:projected-tooling-migration-oracle-comparison-request.v1
  @event:compare-projected-tooling-migration-oracle
  @event-authority:compare-projected-tooling-migration-oracle.v1
  @outcome:projected-tooling-migration-oracle-comparison-request-delegated
  @outcome-contract:projected-tooling-migration-oracle-comparison-request.v1
  Scenario: Delegate one bounded projected-to-oracle comparison
    Given one lineage-bound projected target observation, declared fixture scope, and frozen operational oracle declaration
    When a downstream consumer requests the declared projected-to-oracle comparison composition
    Then the unchanged request is delegated with immutable lineage and no equality, acceptance, verification, promotion, or rollback fact is fabricated

  @scenario:resolve-projected-tooling-migration-oracle-comparison-scope
  @input:projected-tooling-migration-oracle-comparison-request
  @input-contract:projected-tooling-migration-oracle-comparison-request.v1
  @event:resolve-projected-tooling-migration-oracle-comparison-scope
  @event-authority:resolve-projected-tooling-migration-oracle-comparison-scope.v1
  @outcome:bounded-governed-repository-observation-context
  @outcome-contract:bounded-governed-repository-observation-context.v1
  Scenario: Resolve the byte-identical frozen-oracle scope
    Given one declared projected observation, fixture authority, legacy provider oracle, independent obligation oracle, and a closed frozen repository-state manifest of every relevant relative path, byte digest, and explicit absence marker
    When the declared repository-state manifest, optional repository revision evidence, fixture identities, projected observations, oracle connectors, and optional prior-binding restoration facts are resolved in stable identity order
    Then one bounded governed repository observation context identifies only authorized facts and expected equality obligations, or an attributable declaration rejection is returned before oracle observation

  @scenario:observe-frozen-tooling-migration-operational-oracle
  @input:bounded-governed-repository-observation-context
  @input-contract:bounded-governed-repository-observation-context.v1
  @event:observe-frozen-tooling-migration-operational-oracle
  @event-authority:observe-frozen-tooling-migration-operational-oracle.v1
  @outcome:governed-repository-observation
  @outcome-contract:governed-repository-observation.v1
  Scenario: Observe the frozen legacy operational oracle from the declared repository state
    Given one bounded governed repository observation context and one admitted repository-observation effect capability
    When every declared fixture is observed against the byte-identical legacy provider and independent obligation evaluator
    Then declared repository-state manifest byte and digest evidence, optional repository revision evidence, per-fixture oracle outcomes, obligation dispositions, attributable unavailable-or-drift findings, optional restored-binding byte equality facts, and complete effect lineage are returned without changing the oracle, fixture authority, or provider binding

  @scenario:compare-projected-tooling-migration-oracle-observations
  @input:governed-repository-observation
  @input-contract:governed-repository-observation.v1
  @event:compare-projected-tooling-migration-oracle-observations
  @event-authority:compare-projected-tooling-migration-oracle-observations.v1
  @outcome:tooling-migration-oracle-equivalence-evidence
  @outcome-contract:tooling-migration-oracle-equivalence-evidence.v1
  @outcome-terminal
  Scenario: Return attributable equality evidence without deciding migration policy
    Given complete projected target observations and governed repository observations for the same declared closed repository-state manifest and fixture identities
    When projected outcome hashes, obligation dispositions, every declared manifest relative path, byte digest, and absence marker, and declared rollback restoration equality facts are compared in stable fixture identity order
    Then EQUIVALENT is returned only when every declared comparison agrees, otherwise MISMATCHED is returned with the first attributable connector and all prior facts, without accepting a candidate or deciding verification, promotion, rollback, or continuation
