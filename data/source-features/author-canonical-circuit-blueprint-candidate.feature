@capability:author-canonical-circuit-blueprint-candidate
@root-scenario:author-canonical-circuit-blueprint-candidate
@lifecycle:REVISION
Feature: Author one canonical circuit blueprint candidate from exact governed design testimony

  A design authority supplies one governed canonical feature reference, a bounded
  set of exact admitted precedent testimony, and one explicit blueprint design
  testimony object. The capability resolves the exact feature bytes and declared
  root identities, verifies every precedent content digest, verifies that the
  proposed design preserves those identities and authorities, and constructs one
  canonical candidate with a deterministic authority digest.

  The successful result is one complete canonical-circuit-blueprint.v1 carrier
  with sourceAuthority.disposition CANDIDATE. It is not conformance, geometry,
  review, approval, admission, fabrication, or publication authority. Missing
  feature authority, divergent precedent bytes, malformed design testimony,
  incomplete lineage, and proposed feature identity drift are returned as exact
  attributable rejection evidence.

  This capability contains no subject-specific topology, scenario, provider,
  dependency, or outcome knowledge. The Level 4 build-level4-design.mjs provision
  is retained only as a behavioral oracle: its exact approved design becomes the
  golden testimony vector used to prove this generic revision.

  @scenario:author-canonical-circuit-blueprint-candidate
  @input:canonical-blueprint-design-request
  @input-contract:canonical-blueprint-design-request.v2
  @event:author-canonical-circuit-blueprint-candidate
  @event-authority:author-canonical-circuit-blueprint-candidate.v2
  @outcome:canonical-blueprint-authoring-result
  @outcome-contract:canonical-blueprint-authoring-result.v2
  @outcome-variants:BLUEPRINT_CANDIDATE_AUTHORED|FEATURE_AUTHORITY_REJECTED|PRECEDENT_AUTHORITY_REJECTED|DESIGN_TESTIMONY_REJECTED|CANDIDATE_LINEAGE_REJECTED
  @outcome-terminal
  Scenario: Author one lineage-bound candidate without claiming admission
    Given one governed feature reference, exact admitted precedent testimony, and one explicit blueprint design testimony object
    When feature bytes and identities are resolved, precedent bytes are verified, design testimony is bound, and candidate identity is derived
    Then return one complete CANDIDATE carrier with exact lineage and deterministic authority identity or attributable rejection evidence without claiming conformance, review, approval, admission, fabrication, or publication

  @scenario:resolve-exact-feature-authority
  @input:canonical-blueprint-design-request
  @input-contract:canonical-blueprint-design-request.v2
  @event:resolve-exact-feature-authority
  @event-authority:resolve-exact-feature-authority.v2
  @outcome:exact-feature-authority
  @outcome-contract:canonical-blueprint-authoring-intermediate.v2
  Scenario: Resolve exact feature bytes and root identities
    Given one feature reference bounded to the governed Harness and platform roots
    When the admitted canonical feature resolver observes and parses it
    Then exact source bytes, source reference, capability identity, root Input, Event, Outcome, and contract identities are returned or exact feature rejection evidence is retained

  @scenario:bind-admitted-blueprint-precedents
  @input:exact-feature-authority
  @input-contract:canonical-blueprint-authoring-intermediate.v2
  @event:bind-admitted-blueprint-precedents
  @event-authority:bind-admitted-blueprint-precedents.v2
  @outcome:admitted-blueprint-design-context
  @outcome-contract:canonical-blueprint-authoring-intermediate.v2
  Scenario: Bind exact admitted precedent testimony
    Given resolved feature authority and an ordered set of precedent authority identities, content, digest bases, and ADMITTED dispositions
    When each content digest is derived and compared with its declared digest
    Then the exact ordered precedent set is bound only when every digest matches, or PRECEDENT_AUTHORITY_REJECTED identifies the divergent authority before candidate construction

  @scenario:bind-blueprint-design-testimony
  @input:admitted-blueprint-design-context
  @input-contract:canonical-blueprint-authoring-intermediate.v2
  @event:bind-blueprint-design-testimony
  @event-authority:bind-blueprint-design-testimony.v2
  @outcome:blueprint-candidate-testimony
  @outcome-contract:canonical-blueprint-authoring-intermediate.v2
  Scenario: Bind explicit design testimony without treating it as authority
    Given exact feature authority, verified precedent testimony, and one complete blueprint design testimony object
    When the proposed capability identity, CANDIDATE disposition, feature authority reference, precedent lineage, nodes, edges, mappings, service levels, and projection authorities are evaluated
    Then the testimony proceeds unchanged only when every required identity and lineage member closes, or DESIGN_TESTIMONY_REJECTED identifies the first unresolved obligation

  @scenario:bind-blueprint-candidate-lineage
  @input:blueprint-candidate-testimony
  @input-contract:canonical-blueprint-authoring-intermediate.v2
  @event:bind-blueprint-candidate-lineage
  @event-authority:bind-blueprint-candidate-lineage.v2
  @outcome:canonical-blueprint-authoring-result
  @outcome-contract:canonical-blueprint-authoring-result.v2
  @outcome-variants:BLUEPRINT_CANDIDATE_AUTHORED|CANDIDATE_LINEAGE_REJECTED
  @outcome-terminal
  Scenario: Derive candidate identity only after exact lineage closes
    Given one verified design testimony object, exact feature authority, and verified precedents
    When canonical blueprint authority material is assembled without an authority digest and hashed
    Then the candidate is returned with that deterministic authority digest, or CANDIDATE_LINEAGE_REJECTED identifies the unresolved identity without altering testimony
