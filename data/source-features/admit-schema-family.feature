@capability:admit-schema-family
@root-scenario:admit-schema-family
# Legacy source: scenario-driven-architecture/tools/src/capabilities/kernel-implementation-admission/admit-schema-family/provider.ts
Feature: Admit schema family

  An SDA maintainer needs to know that the complete canonical schema family
  compiles cleanly under its declared dialect before any contract built from
  it is trusted. The capability compiles every canonical schema and resolves
  every reference between them.

  Every canonical schema and reference resolves under the declared dialect,
  or the compilation gap is identified precisely. The capability does not
  admit any implementation or specification — it only establishes that the
  schema family itself is internally coherent.

  @scenario:admit-schema-family
  @input:schema-family-admission-input
  @input-contract:schema-family-admission-input.v1
  @event:schema-family-admission-requested
  @event-authority:schema-family-admission.v1
  @outcome:schema-family-admission-known
  @outcome-contract:schema-family-admission-evidence.v1
  @outcome-terminal
  Scenario: Compile the canonical schema family and resolve every reference
    Given one canonical schema family and its declared dialect
    When every canonical schema is compiled and every reference between them is resolved
    Then every canonical schema and reference resolves under the declared dialect or carries a precise unresolved finding, without admitting any implementation
