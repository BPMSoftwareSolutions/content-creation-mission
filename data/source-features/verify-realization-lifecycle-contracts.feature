@capability:verify-realization-lifecycle-contracts
@root-scenario:verify-realization-lifecycle-contracts
# Legacy source: scenario-driven-architecture/tools/src/capabilities/realization-planning/verify-realization-lifecycle-contracts/provider.ts
Feature: Verify realization lifecycle contracts

  A realization operator needs to review why a physical workload existed
  and confirm that evicting it retained capability availability and
  historical proof rather than erasing them. The capability verifies causal
  lineage, ordered stage evidence, immutable proof, and independently
  derived availability across content-addressed realization lifecycle
  artifacts.

  Lifecycle artifacts preserve workload-to-intent causality and keep
  registration, realization, proof, and availability lifetimes distinct;
  every lifecycle artifact verifies by digest, links to its predecessors,
  and preserves proof history after eviction. The capability does not
  create or evict any realization itself — it only verifies that the
  lifecycle artifacts already produced remain coherent.

  @scenario:verify-realization-lifecycle-contracts
  @input:content-addressed-realization-lifecycle-artifacts
  @input-contract:realization-lifecycle-fixture.v1
  @event:realization-lifecycle-contract-verification-requested
  @event-authority:realization-lifecycle-contract-verification.v1
  @outcome:realization-lifecycle-contract-coherence-known
  @outcome-contract:realization-lifecycle-contract-evidence.v1
  @outcome-terminal
  Scenario: Verify causal lineage, ordered stage evidence, immutable proof, and independently derived availability
    Given a set of content-addressed realization lifecycle artifacts
    When causal lineage, ordered stage evidence, immutable proof, and independently derived availability are verified
    Then lifecycle artifacts preserve workload-to-intent causality, keep registration, realization, proof, and availability lifetimes distinct, and every artifact verifies by digest while preserving proof history after eviction
