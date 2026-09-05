@capability:publish-bounded-tooling-migration-evidence
@root-scenario:publish-bounded-tooling-migration-evidence
Feature: Publish bounded tooling migration evidence

  A downstream consumer supplies one terminal tooling-migration observation
  with complete declared lineage and an admitted evidence-publication
  authority. The consumer receives a destination reference, content digest,
  operation disposition, and interface exit disposition for the exact
  published observation. The capability does not decide admission,
  equivalence, verification, promotion, rollback policy, or acceptance.

  Evidence publication is an explicit governed effect responsibility executed
  through the SDA capability `shape-governed-file-system-batch`. The
  declared observation, evidence envelope, immutable run-or-evidence identity,
  fresh destination, reject-existing policy, and required lineage references
  are resolved before materialization. Versioning is governed only by the
  declared run-or-evidence identity and never by overwrite or append. The
  effect capability may publish only the declared bounded evidence and may
  report publication only from its observed nested receipt; pure
  transformations may not fabricate a destination, digest, exit disposition,
  or acceptance fact. No provider-workspace or FS Shaper checkout participates.

  Publication preserves rather than upgrades meaning. It carries observed
  rejection, rollback, equality, and execution facts with their declared
  connectors. A complete publication never changes an incoming disposition to
  accepted, and a failed or partial materialization returns attributable
  publication evidence without reporting completion.

  @scenario:publish-bounded-tooling-migration-evidence
  @input:bounded-tooling-migration-evidence-publication-request
  @input-contract:bounded-tooling-migration-evidence-publication-request.v1
  @event:publish-bounded-tooling-migration-evidence
  @event-authority:publish-bounded-tooling-migration-evidence.v1
  @outcome:bounded-tooling-migration-evidence-publication-request-delegated
  @outcome-contract:bounded-tooling-migration-evidence-publication-request.v1
  Scenario: Delegate one bounded tooling-migration evidence publication
    Given one declared terminal tooling-migration observation, bounded evidence destination, and publication authority
    When a downstream consumer requests the declared evidence-publication composition
    Then the unchanged request is delegated with complete lineage and no publication, acceptance, or migration-policy fact is fabricated

  @scenario:resolve-bounded-tooling-migration-evidence-publication-scope
  @input:bounded-tooling-migration-evidence-publication-request
  @input-contract:bounded-tooling-migration-evidence-publication-request.v1
  @event:resolve-bounded-tooling-migration-evidence-publication-scope
  @event-authority:resolve-bounded-tooling-migration-evidence-publication-scope.v1
  @outcome:bounded-tooling-migration-evidence-publication-context
  @outcome-contract:bounded-tooling-migration-evidence-publication-context.v1
  Scenario: Resolve the exact evidence envelope before publication
    Given one declared terminal observation with operation disposition, interface exit disposition, lineage connectors, immutable run-or-evidence identity, and an admitted fresh-destination reject-existing policy
    When the declared evidence fields, required equality or rollback facts, run-or-evidence identity, fresh destination, reject-existing policy, and stable evidence ordering are resolved
    Then one bounded publication context identifies only the publishable observation and required evidence envelope, or an attributable declaration rejection is returned before materialization

  @scenario:materialize-bounded-tooling-migration-evidence
  @input:bounded-tooling-migration-evidence-publication-context
  @input-contract:bounded-tooling-migration-evidence-publication-context.v1
  @event:materialize-bounded-tooling-migration-evidence
  @event-authority:materialize-bounded-tooling-migration-evidence.v1
  @outcome:published-bounded-tooling-migration-evidence
  @outcome-contract:published-bounded-tooling-migration-evidence.v1
  @outcome-terminal
  Scenario: Return an observed atomic evidence-publication receipt
    Given one bounded publication context and the governed SDA capability `shape-governed-file-system-batch`
    When that capability materializes the exact declared evidence envelope at its fresh immutable run-evidence destination under the admitted reject-existing policy
    Then an observed artifact digest, destination reference, unchanged operation disposition, unchanged interface exit disposition, attributable equality and rollback facts, and complete effect lineage are returned only after complete publication, otherwise an attributable incomplete-publication observation is returned without an acceptance claim or completion report
