@capability:project-openapi-description
@root-scenario:project-openapi-description
# Legacy source: scenario-driven-architecture/tools/src/capabilities/api-interface-projection/project-openapi-description/provider.ts
Feature: Project bounded OpenAPI description

  An API product maintainer needs one stable, source-attributable OpenAPI
  description to review before hosting, SDK generation, or publication ever
  happens. The capability verifies the operation graph, contracts, and
  content-addressed OpenAPI profile, rejects unsupported schema shapes, and
  derives one deterministic in-memory OpenAPI description.

  Every admitted graph operation, contract, response, scope, and `x-sda`
  lineage field has one attributable OpenAPI embodiment, and the resulting
  OpenAPI 3.1.2 document is content addressed, complete, and contains no
  deployment server authority. The capability does not host, publish, or
  generate any SDK — it only projects the reviewable description those
  steps would later consume.

  @scenario:project-openapi-description
  @input:admitted-operation-graph-contracts-and-openapi-profile
  @input-contract:project-openapi-description-input.v1
  @event:openapi-description-projection-requested
  @event-authority:openapi-description-projection.v1
  @outcome:openapi-description-known
  @outcome-contract:openapi-projection-evidence.v1
  @outcome-terminal
  Scenario: Project one deterministic bounded OpenAPI description from the admitted operation graph
    Given one admitted operation graph, its contracts, and a content-addressed OpenAPI profile
    When the graph, contracts, and profile are verified, unsupported schema shapes are rejected, and one deterministic in-memory OpenAPI description is derived
    Then every admitted operation, contract, response, scope, and lineage field has one attributable OpenAPI embodiment, and the document contains no deployment server authority
