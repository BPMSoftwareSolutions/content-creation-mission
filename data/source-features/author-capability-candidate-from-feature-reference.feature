@capability:author-capability-candidate-from-feature-reference
@root-scenario:author-capability-candidate-from-feature-reference
Feature: Author a capability candidate under approved canonical blueprint authority

  A harness operator supplies one canonical feature reference and the approved
  canonical blueprint that governs it. The Agentic Harness resolves and
  observes the referenced feature, binds the current digest-bound blueprint
  review, resolves the blueprint cell ledger, selects exactly one eligible
  cell, and invokes the admitted projectable-candidate authoring capability for
  that cell alone.

  The blueprint is authority during authoring, not lineage attached beside it.
  A model proposes meaning inside one selected cell. It never selects scenario
  inventory, topology, routes, connectors, altitudes, artifact ownership,
  mechanics, provider slots, or proof obligations, and it is never asked to
  author a capability whole. Every request, response, retained fragment, and
  result carries the same feature bytes, blueprint digest, reviewer-authority
  digest, review-boundary digest, and selected cell identity.

  Authoring without an approved blueprint is rejected rather than degraded to
  feature-only authoring. A stale, unapproved, superseded, or digest-divergent
  review is rejected. A cell already closed, absent from the blueprint, or
  requested by a caller against the ledger is rejected. Authoring never
  advances the ledger on a rejected or held cell.

  Having no eligible cell is an observation about selection. Having every
  required cell closed is a statement about completion. The circuit never
  derives the second from the first: authoring completion is established only
  from proven closure of every required cell, and an absence of eligible cells
  while required cells remain open is held as blocked, never reported as
  completion.

  Feature resolution and byte observation are explicit filesystem effects.
  Annotation resolution and ledger derivation are deterministic platform
  mechanics. Candidate authoring remains owned by the separately projected
  author-tooling-capability-candidate capability. This capability does not
  author companion authority itself, handwrite executable source, admit a
  blueprint, conduct a review, or claim admission, behavioral conformance,
  projection, promotion, or acceptance.

  @scenario:author-capability-candidate-from-feature-reference
  @input:blueprint-bound-capability-authoring-request
  @input-contract:blueprint-bound-capability-authoring-request.v1
  @event:author-capability-candidate-from-feature-reference
  @event-authority:author-capability-candidate-from-feature-reference.v1
  @outcome:blueprint-bound-capability-authoring-result
  @outcome-contract:blueprint-bound-capability-authoring-result.v1
  @outcome-terminal
  Scenario: Author one selected blueprint cell under approved blueprint authority
    Given one governed canonical feature reference and the approved canonical blueprint that governs it
    When the feature is resolved, the blueprint review is bound, one eligible cell is selected, and the admitted candidate-authoring capability is invoked for that cell
    Then either one projectable cell candidate carrying the exact feature, blueprint, review, and cell identities or exact authoring rejection evidence is returned, with no claim of admission, projection, promotion, review, or handwritten executable code

  @scenario:resolve-canonical-feature-authoring-input
  @input:blueprint-bound-capability-authoring-request
  @input-contract:blueprint-bound-capability-authoring-request.v1
  @event:resolve-canonical-feature-authoring-input
  @event-authority:resolve-canonical-feature-authoring-input.v1
  @outcome:canonical-capability-feature
  @outcome-contract:canonical-capability-feature.v1
  @outcome-terminal
  Scenario: Resolve one canonical feature reference
    Given one feature path or capability identity within the governed harness roots
    When the reference is resolved, observed, and its declared root connectors are parsed
    Then one immutable canonical capability feature contains the exact source bytes, source reference, and declared root semantic identities

  @scenario:bind-approved-blueprint-authority
  @input:canonical-capability-feature
  @input-contract:canonical-capability-feature.v1
  @event:bind-approved-blueprint-authority
  @event-authority:bind-approved-blueprint-authority.v1
  @outcome:bound-blueprint-authoring-authority
  @outcome-contract:bound-blueprint-authoring-authority.v1
  @outcome-terminal
  Scenario: Bind the approved blueprint and its current digest-bound review
    Given one immutable canonical capability feature and one canonical blueprint with its reviewer-authority, review-boundary, and approval testimony
    When the blueprint is bound to the feature and its review is verified
    Then one bound authority carries the exact feature bytes, blueprint digest, carrier digest, reviewer-authority digest, and review-boundary digest, and an absent, unapproved, superseded, or digest-divergent review is returned as exact rejection evidence rather than authorizing feature-only authoring

  @scenario:resolve-blueprint-cell-ledger
  @input:bound-blueprint-authoring-authority
  @input-contract:bound-blueprint-authoring-authority.v1
  @event:resolve-blueprint-cell-ledger
  @event-authority:resolve-blueprint-cell-ledger.v1
  @outcome:blueprint-cell-ledger
  @outcome-contract:blueprint-cell-ledger.v1
  @outcome-terminal
  Scenario: Derive the cell ledger from the bound blueprint
    Given one bound blueprint authoring authority and the retained authoring evidence for its blueprint digest
    When the ledger is derived from the blueprint cells and their retained closure decisions
    Then every blueprint cell appears exactly once with its identity, dependency position, and closure state, the ledger is derived only from the bound blueprint digest and retained evidence, and a ledger that does not account for every blueprint cell is returned as exact rejection evidence

  @scenario:select-one-eligible-blueprint-cell
  @input:blueprint-cell-ledger
  @input-contract:blueprint-cell-ledger.v1
  @event:select-one-eligible-blueprint-cell
  @event-authority:select-one-eligible-blueprint-cell.v1
  @outcome:selected-blueprint-cell
  @outcome-contract:selected-blueprint-cell.v1
  @outcome-variants:CELL_SELECTED|ALL_BLUEPRINT_CELLS_CLOSED|BLUEPRINT_AUTHORING_BLOCKED|CELL_SELECTION_REJECTED
  @outcome-terminal
  Scenario: Establish exactly one declared selection disposition
    Given one blueprint cell ledger and the declared cell eligibility order
    When the next authoring step is selected against that ledger
    Then exactly one declared disposition is established: one cell is selected by deterministic order over the ledger; or every required cell is proven closed, which alone establishes authoring completion and is never inferred from an absence of eligible cells; or no cell is eligible while required cells remain open, which is held as blocked authoring rather than reported as completion; or a cell that is already closed, absent from the bound blueprint, or requested by a caller against the ledger is returned as exact rejection evidence

  @scenario:invoke-projectable-capability-candidate-author
  @input:selected-blueprint-cell
  @input-contract:selected-blueprint-cell.v1
  @event:invoke-projectable-capability-candidate-author
  @event-authority:invoke-projectable-capability-candidate-author.v1
  @outcome:blueprint-bound-capability-authoring-result
  @outcome-contract:blueprint-bound-capability-authoring-result.v1
  @outcome-terminal
  Scenario: Invoke the admitted candidate author for that cell alone
    Given one selected blueprint cell carrying its bound feature, blueprint, and review identities
    When the projected author-tooling-capability-candidate capability is invoked for that cell
    Then its projectable source candidate or exact authoring rejection evidence is returned unchanged with the same feature, blueprint, review, and cell identities, no fabrication surface outside the selected cell is produced, and the ledger is never advanced on a rejected or held cell

  @scenario:verify-blueprint-authoring-lineage
  @input:blueprint-bound-capability-authoring-result
  @input-contract:blueprint-bound-capability-authoring-result.v1
  @event:verify-blueprint-authoring-lineage
  @event-authority:verify-blueprint-authoring-lineage.v1
  @outcome:verified-blueprint-authoring-lineage
  @outcome-contract:verified-blueprint-authoring-lineage.v1
  @outcome-variants:LINEAGE_VERIFIED|BLUEPRINT_DID_NOT_CONSTRAIN|NOT_ON_SELECTED_ROUTE
  @outcome-terminal
  Scenario: Prove the blueprint survived into the authored result
    Given one authoring result and the bound feature, blueprint, review, and selected-cell identities the request carried
    When the result lineage is verified against those exact identities
    Then the result is returned only when the bound blueprint measurably constrained it, a result whose content is unchanged by the bound blueprint, whose identities drifted, or whose fabrication surface exceeds the selected cell is returned as exact rejection evidence, and a route that authored no cell candidate claims nothing about lineage rather than asserting either verification or violation
