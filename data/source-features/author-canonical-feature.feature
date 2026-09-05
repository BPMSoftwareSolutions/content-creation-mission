@capability:author-canonical-feature
@root-scenario:author-canonical-feature
Feature: Author a canonical feature from governed planning testimony

  Feature authoring participates in the same governed circuit as feature
  execution. A model may propose bounded language for one declared capability,
  but it cannot mint semantic identities, write source authority, invoke a
  projector, or declare an executable capability admitted. Contract admission
  fixes every identity before candidate language is rendered. Artifact
  materialization is atomic and produces digest-bearing testimony. Published
  artifact references are repository-relative, so the same testimony remains
  portable across workspaces. Projection remains a separate governed
  responsibility performed by the existing SDA consumer-capability compilation
  scenarios.

  The authored source bundle contains no executable body. It contains canonical
  Gherkin, contracts, semantic execution authority, fixtures, interface
  bindings, and projection intent. Every executable consumer must be reproduced
  from that bundle and retain source, projection, execution, and model lineage.

  @scenario:author-canonical-feature
  @input:governed-feature-authoring-context
  @input-contract:governed-feature-authoring-context.v1
  @event:materialize-admitted-feature-source
  @event-authority:materialize-admitted-feature-source.v1
  @outcome:governed-feature-authoring-testimony
  @outcome-contract:governed-feature-authoring-testimony.v1
  @outcome-terminal
  Scenario: Materialize one admitted feature source workspace
    Given bounded feature intent and schema-conformant planning testimony for declared semantic identities
    When the candidate declaration is admitted and its canonical source artifacts are atomically materialized
    Then a complete digest-bearing feature workspace with repository-relative artifact references and a separate projection request are observable without any handwritten executable body
