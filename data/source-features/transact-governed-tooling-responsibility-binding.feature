@capability:transact-governed-tooling-responsibility-binding
@root-scenario:transact-governed-tooling-responsibility-binding
Feature: Transact one governed tooling responsibility binding

  A downstream consumer supplies one verified replacement request naming one
  governed responsibility binding, its projected provider identity, immutable
  prior binding bytes, and one governed full-gate authority. The consumer
  receives attributable transaction evidence that either retains the staged
  binding after successful gate testimony or restores the exact prior bytes
  after rejected gate testimony.

  This capability owns neither candidate verification nor promotion policy.
  Deterministic migration decision authority remains responsible for deciding
  whether the supplied evidence permits a transaction and for interpreting the
  returned disposition. The capability does not decide that a candidate is
  verified, invent a gate result, choose a replacement, mutate more than one
  binding, or claim promotion.

  Binding preservation, staging, gate observation, retention, and restoration
  are explicit governed effect responsibilities. Pure authority may resolve a
  bounded request, but it cannot fabricate prior bytes, write receipts, gate
  exits, hashes, or rollback evidence. Missing authority, a selected binding
  mismatch, prior-byte mismatch, unsafe path, staging failure, unreadable
  receipt, or rejected gate returns attributable evidence.

  @scenario:transact-governed-tooling-responsibility-binding
  @input:governed-tooling-binding-transaction-request
  @input-contract:governed-tooling-binding-transaction-request.v1
  @event:transact-governed-tooling-responsibility-binding
  @event-authority:transact-governed-tooling-responsibility-binding.v1
  @outcome:governed-tooling-binding-transaction-request-delegated
  @outcome-contract:governed-tooling-binding-transaction-request.v1
  Scenario: Delegate one governed responsibility-binding transaction
    Given one declared responsibility binding, projected replacement identity, immutable prior binding bytes, and governed full-gate authority
    When a downstream consumer requests the declared binding transaction composition
    Then the unchanged request is delegated with its authority lineage and no binding or gate fact is fabricated

  @scenario:resolve-governed-tooling-binding-transaction-scope
  @input:governed-tooling-binding-transaction-request
  @input-contract:governed-tooling-binding-transaction-request.v1
  @event:resolve-governed-tooling-binding-transaction-scope
  @event-authority:resolve-governed-tooling-binding-transaction-scope.v1
  @outcome:bounded-governed-tooling-binding-transaction-context
  @outcome-contract:bounded-governed-tooling-binding-transaction-context.v1
  Scenario: Resolve exactly one authorized binding transaction
    Given one declared selected responsibility, pinned binding authority, exact prior bytes, projected replacement, and full-gate authority
    When the transaction scope and immutable before-state are resolved
    Then one bounded context identifies exactly one eligible binding and its complete rollback material, or an attributable rejection is returned before mutation

  @scenario:stage-governed-tooling-responsibility-binding
  @input:bounded-governed-tooling-binding-transaction-context
  @input-contract:bounded-governed-tooling-binding-transaction-context.v1
  @event:stage-governed-tooling-responsibility-binding
  @event-authority:stage-governed-tooling-responsibility-binding.v1
  @outcome:staged-governed-tooling-binding-observation
  @outcome-contract:staged-governed-tooling-binding-observation.v1
  Scenario: Preserve and stage only the selected binding
    Given one bounded transaction context with exact prior binding bytes
    When the admitted binding-transaction effect preserves those bytes and stages the declared projected replacement
    Then attributable preservation and staging receipts identify one changed responsibility and every unchanged binding, or exact prior bytes remain active with an attributable staging rejection

  @scenario:observe-governed-tooling-binding-full-gate
  @input:staged-governed-tooling-binding-observation
  @input-contract:staged-governed-tooling-binding-observation.v1
  @event:observe-governed-tooling-binding-full-gate
  @event-authority:observe-governed-tooling-binding-full-gate.v1
  @outcome:governed-tooling-binding-gate-observation
  @outcome-contract:governed-tooling-binding-gate-observation.v1
  Scenario: Observe the declared full gate against the staged binding
    Given one attributable staged-binding observation and one governed full-gate authority
    When the admitted full-gate execution effect is invoked once against the staged binding
    Then an attributable exit receipt and complete execution lineage are returned without interpreting the gate as candidate verification or promotion

  @scenario:complete-governed-tooling-binding-transaction
  @input:governed-tooling-binding-gate-observation
  @input-contract:governed-tooling-binding-gate-observation.v1
  @event:complete-governed-tooling-binding-transaction
  @event-authority:complete-governed-tooling-binding-transaction.v1
  @outcome:governed-tooling-binding-transaction-evidence
  @outcome-contract:governed-tooling-binding-transaction-evidence.v1
  @outcome-terminal
  Scenario: Retain or restore exact binding bytes from gate testimony
    Given one staged binding observation, immutable prior bytes, and attributable full-gate testimony
    When the admitted binding-transaction effect retains the staged replacement only after zero gate exit or restores the exact prior bytes after any rejected gate
    Then durable transaction evidence reports RETAINED or RESTORED, exact before and after byte hashes, one selected responsibility, and complete effect lineage without claiming promotion
