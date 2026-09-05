@capability:prove-domain-isolation
@root-scenario:prove-domain-isolation
# Legacy source: scenario-driven-architecture/tools/src/capabilities/consumer-assurance/prove-domain-isolation/provider.ts
Feature: Prove domain isolation

  A consumer needs to trust that SDA's reusable platform tooling remains
  domain-neutral and has not quietly absorbed one consumer's vocabulary or
  business rules. The capability detects external consumer vocabulary
  embedded in reusable platform tooling.

  No external domain term or rule is embedded in SDA mechanics; tooling and
  generic fixtures remain domain-neutral. The capability does not remove or
  repair a violation itself — it only makes any domain leakage visible.

  @scenario:prove-domain-isolation
  @input:consumer-tooling-source-facts
  @input-contract:prove-domain-isolation-input.v1
  @event:domain-isolation-proof-requested
  @event-authority:consumer-domain-isolation-proof.v1
  @outcome:domain-isolation-known
  @outcome-contract:domain-isolation-evidence.v1
  @outcome-terminal
  Scenario: Detect external consumer vocabulary embedded in reusable platform tooling
    Given the source facts for consumer tooling and generic platform fixtures
    When external consumer vocabulary is detected in reusable platform tooling
    Then no external domain term or rule is found embedded in SDA mechanics, or every violation found is named precisely
