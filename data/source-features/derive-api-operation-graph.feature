@capability:derive-api-operation-graph
@root-scenario:derive-api-operation-graph
# Legacy source: scenario-driven-architecture/tools/src/capabilities/api-interface-projection/derive-api-operation-graph/provider.ts
Feature: Derive API operation graph

  An API product maintainer needs to review the complete semantic API
  surface before any OpenAPI, hosting, or SDK mechanic is introduced. The
  capability verifies content-addressed interface and contract authority,
  resolves every scenario binding, and derives one deterministic,
  target-neutral operation graph.

  Every operation has one unique route, resolved request and response
  contracts, and exact capability-scenario lineage; the graph carries
  `x-sda` lineage and one verified graph digest. The capability does not
  project any transport format — it only establishes the semantic surface
  transport projection will later consume.

  @scenario:derive-api-operation-graph
  @input:admitted-api-interface-capability-and-contract-authority
  @input-contract:derive-api-operation-graph-input.v1
  @event:api-operation-graph-derivation-requested
  @event-authority:api-operation-graph-derivation.v1
  @outcome:api-operation-graph-known
  @outcome-contract:api-operation-graph-evidence.v1
  @outcome-terminal
  Scenario: Derive one deterministic target-neutral API operation graph from admitted authority
    Given admitted API interface, capability, and contract authority
    When content-addressed interface and contract authority are verified, every scenario binding is resolved, and one deterministic target-neutral operation graph is derived
    Then every operation has one unique route, resolved request and response contracts, and exact capability-scenario lineage, with one verified graph digest and no transport projection performed
