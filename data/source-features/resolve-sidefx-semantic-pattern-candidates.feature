@capability:resolve-sidefx-semantic-pattern-candidates
@root-scenario:resolve-sidefx-semantic-pattern-candidates
Feature: Offer admitted patterns as candidates, never as admissions

  A pattern is a suggestion with boundaries, not a decision. This capability
  matches a requested subject kind and relationship kinds against explicitly
  admitted, digest-bound patterns, and returns only those whose declared
  applicability actually covers the request. Every candidate carries its own
  applicability conditions, its explicit limits, and its exact source locator,
  and every candidate declares that no automatic admission is claimed. When no
  admitted pattern covers the request the answer is NOT_FOUND, and when no
  pattern authority was supplied at all the answer is INSUFFICIENT_AUTHORITY;
  the two are never confused with each other.

  @scenario:resolve-sidefx-semantic-pattern-candidates
  @input:sidefx-pattern-candidate-request
  @input-contract:sidefx-pattern-candidate-request.v1
  @event:sidefx-pattern-candidate-requested
  @event-authority:resolve-sidefx-semantic-pattern-candidates.v1
  @outcome:sidefx-semantic-pattern-candidate-set
  @outcome-contract:sidefx-semantic-pattern-candidate-set.v1
  @outcome-terminal
  Scenario: Match admitted patterns and keep their applicability boundaries
    Given digest-bound admitted patterns, a requested subject kind, and requested relationship kinds
    When each pattern is checked for declared subject-kind and relationship-kind coverage
    Then covering patterns are returned as candidates with explicit limits and no admission claim, and absence is distinguished from missing authority
