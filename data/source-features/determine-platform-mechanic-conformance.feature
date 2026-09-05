@capability:determine-platform-mechanic-conformance
@root-scenario:determine-platform-mechanic-conformance
# Legacy source: scenario-driven-architecture/tools/src/capabilities/consumer-assurance/determine-platform-mechanic-conformance/provider.ts
Feature: Determine platform mechanic conformance

  A consumer needs to know which runtime can genuinely host a capability,
  not merely which runtime is declared to support it. The capability
  evaluates admitted platform providers against current toolchain proof.

  Every mandatory mechanic has current implementation and conformance
  evidence, and each active language carries complete, current mechanic
  proof. The capability does not admit the consumer capability itself — it
  only establishes which platforms are genuinely proven to host it.

  @scenario:determine-platform-mechanic-conformance
  @input:language-platform-mechanic-facts
  @input-contract:determine-platform-mechanic-conformance-input.v1
  @event:platform-mechanic-conformance-evaluation-requested
  @event-authority:platform-mechanic-conformance.v1
  @outcome:platform-mechanic-conformance-known
  @outcome-contract:platform-mechanic-conformance-evidence.v1
  @outcome-terminal
  Scenario: Evaluate admitted platform providers against current toolchain proof
    Given one set of language platform mechanic facts
    When admitted platform providers are evaluated against current toolchain proof
    Then every mandatory mechanic has current implementation and conformance evidence, and each active language carries complete current mechanic proof
