@capability:discover-language-bindings
@root-scenario:discover-language-bindings
# Legacy source: scenario-driven-architecture/tools/src/capabilities/workspace-governance/discover-language-bindings/provider.ts
Feature: Discover language bindings

  An SDA maintainer needs one authoritative inventory of every language
  binding manifest declared in the workspace before any obligation or
  conformance question can be asked about them. The capability enumerates
  every declared language binding manifest in the workspace.

  Every discoverable manifest is represented exactly once, with its language
  and source path. The capability does not classify a binding's obligation
  or evaluate its conformance — it only establishes the complete inventory
  those later steps depend on.

  @scenario:discover-language-bindings
  @input:language-binding-discovery-input
  @input-contract:language-binding-discovery-input.v1
  @event:language-binding-discovery-requested
  @event-authority:language-binding-discovery.v1
  @outcome:language-binding-inventory-known
  @outcome-contract:language-binding-discovery-evidence.v1
  @outcome-terminal
  Scenario: Enumerate every declared language binding manifest in the workspace
    Given one workspace containing declared language binding manifests
    When every declared language binding manifest in the workspace is enumerated
    Then every discoverable manifest is represented exactly once with its language and source lineage, without evaluating its obligation or conformance
