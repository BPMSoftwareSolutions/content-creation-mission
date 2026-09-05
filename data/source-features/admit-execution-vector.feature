@capability:admit-execution-vector
@root-scenario:admit-execution-vector
# Legacy source: scenario-driven-architecture/tools/src/capabilities/kernel-implementation-admission/admit-execution-vector/provider.ts
Feature: Admit execution vector

  An SDA maintainer needs to know that the canonical execution vector and its
  declared step ordering are themselves structurally valid before any
  language implementation is judged against them. The capability validates
  the canonical execution vector and its declared ordering against its
  admitted schema.

  Every declared step and ordering constraint is admitted, or the gap is
  identified precisely; the canonical execution vector carries one explicit
  schema-admission disposition. The capability does not evaluate any
  language implementation — it only establishes that the execution law
  being implemented is itself sound.

  @scenario:admit-execution-vector
  @input:execution-vector-admission-input
  @input-contract:execution-vector-admission-input.v1
  @event:execution-vector-admission-requested
  @event-authority:execution-vector-admission.v1
  @outcome:execution-vector-admission-known
  @outcome-contract:execution-vector-admission-evidence.v1
  @outcome-terminal
  Scenario: Validate the canonical execution vector and its declared ordering
    Given one canonical execution vector and its declared step ordering
    When the canonical execution vector and its declared ordering are validated against its admitted schema
    Then every declared step and ordering constraint is admitted or identified as a precise gap, without evaluating any language implementation
