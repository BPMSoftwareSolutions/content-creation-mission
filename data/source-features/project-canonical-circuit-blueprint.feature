@capability:project-canonical-circuit-blueprint
@root-scenario:project-canonical-circuit-blueprint
Feature: Project one canonical circuit blueprint

  ASCII, Mermaid, every other human blueprint view, and the Markdown review
  document are deterministic projections of one canonical carrier. They are
  never authored independently and none becomes a second blueprint.

  A projection is not review-ready unless one byte-stable Markdown document
  contains the exact Mermaid source, ASCII source, C4, Observability,
  Service-Level, Provider, Evidence, replay, and digest views required for human
  review. A projection bundle without that document is held rather than handed
  to a reviewer.

  Identical lineage-bound blueprint authority, projector authority, and
  projection-profile authority must reproduce byte-identical projection source
  and digests. Observation time may be recorded in external testimony; it is
  never an input to the deterministic projection payload.

  Mermaid source determinism and rendered-image determinism are separate proof
  surfaces. This capability proves the first. It does not upgrade a candidate's
  disposition, obtain review testimony, or admit anything.

  @scenario:project-canonical-circuit-blueprint
  @input:canonical-circuit-blueprint-projection-request
  @input-contract:canonical-circuit-blueprint-projection-request.v1
  @event:project-canonical-circuit-blueprint
  @event-authority:project-canonical-circuit-blueprint.v1
  @outcome:canonical-circuit-blueprint-projection-bundle
  @outcome-contract:canonical-circuit-blueprint-projection-bundle.v2
  @outcome-terminal
  Scenario: Project every declared view from one carrier and bind its replay receipt
    Given one lineage-bound blueprint authority and the projection profiles it permits
    When the carrier is resolved, each permitted profile and declared view is projected, and replay is verified
    Then one bundle carries byte-stable source for every declared view and one complete Markdown review document with their receipt, while a missing review document holds the projection and a projection never upgrades a candidate disposition

  @scenario:resolve-canonical-circuit-blueprint
  @input:canonical-circuit-blueprint-projection-request
  @input-contract:canonical-circuit-blueprint-projection-request.v1
  @event:resolve-canonical-circuit-blueprint
  @event-authority:resolve-canonical-circuit-blueprint.v1
  @outcome:normalized-circuit-blueprint-carrier
  @outcome-contract:canonical-circuit-blueprint.v1
  Scenario: Construct one normalized carrier preserving partial order separately from ordinals
    Given a conformant lineage-bound candidate or admitted blueprint authority
    When the normalized carrier is constructed from its scenario, transition, mechanic, provider-slot, terminal, and digest authority
    Then semantic partial order is preserved separately from presentation ordinals, and a discovery order, filesystem order, or model output order is never accepted as either

  @scenario:project-canonical-circuit-blueprint-ascii
  @input:normalized-circuit-blueprint-carrier
  @input-contract:canonical-circuit-blueprint.v1
  @event:project-canonical-circuit-blueprint-ascii
  @event-authority:project-canonical-circuit-blueprint-ascii.v1
  @outcome:blueprint-ascii-source
  @outcome-contract:blueprint-projection-source.v1
  Scenario: Project ASCII source within the printable ASCII range
    Given one normalized carrier and the admitted ASCII projection profile
    When ASCII source is projected through that profile
    Then every byte lies within the printable ASCII range with the profile's declared line endings, the counted monotonic proof block is present, and no wall-clock time, machine, user, or workspace path appears in the source

  @scenario:project-canonical-circuit-blueprint-mermaid
  @input:normalized-circuit-blueprint-carrier
  @input-contract:canonical-circuit-blueprint.v1
  @event:project-canonical-circuit-blueprint-mermaid
  @event-authority:project-canonical-circuit-blueprint-mermaid.v1
  @outcome:blueprint-mermaid-source
  @outcome-contract:blueprint-projection-source.v1
  Scenario: Project Mermaid source with kind-derived shapes and correct visual channels
    Given one normalized carrier and the admitted Mermaid projection profile
    When Mermaid source is projected through that profile
    Then node shape derives from declared node kind, every edge is emitted in the visual channel its topology requires, every edge label states its topology, progress, and selecting variant, and no decision node is inserted between a scenario and its declared branches

  @scenario:project-declared-blueprint-lenses
  @input:normalized-circuit-blueprint-carrier
  @input-contract:canonical-circuit-blueprint.v1
  @event:project-declared-blueprint-lenses
  @event-authority:project-declared-blueprint-lenses.v1
  @outcome:declared-blueprint-lens-set
  @outcome-contract:blueprint-lens-set.v1
  Scenario: Project only the views the blueprint permits
    Given one normalized carrier declaring its permitted views
    When each declared view is projected from that same carrier
    Then every projected view shares the carrier's nodes, edges, identities, and digests, and a view absent from the permitted list is not emitted

  @scenario:compose-canonical-blueprint-review-document
  @input:declared-blueprint-lens-set
  @input-contract:blueprint-lens-set.v1
  @event:compose-canonical-blueprint-review-document
  @event-authority:compose-canonical-blueprint-review-document.v1
  @outcome:canonical-blueprint-review-document
  @outcome-contract:canonical-blueprint-review-document.v1
  Scenario: Compose one deterministic Markdown review document from the projected views
    Given the exact ASCII Mermaid C4 Observability Service-Level Provider Evidence replay and digest views projected from one carrier
    When the canonical review document is composed in the admitted section order with declared line endings
    Then one text markdown document embeds every exact required source and digest without invented design meaning machine paths wall-clock time or independently authored formatting

  @scenario:verify-canonical-blueprint-review-document
  @input:canonical-blueprint-review-document
  @input-contract:canonical-blueprint-review-document.v1
  @event:verify-canonical-blueprint-review-document
  @event-authority:verify-canonical-blueprint-review-document.v1
  @outcome:canonical-blueprint-review-document-disposition
  @outcome-contract:canonical-blueprint-review-document-disposition.v1
  @outcome-variants:REVIEW_DOCUMENT_COMPLETE|REVIEW_DOCUMENT_HELD
  Scenario: Hold projection when the Markdown review document is incomplete or divergent
    Given one composed Markdown review document and the exact projected source set
    When required sections embedded source bytes view digests media type and replay lineage are verified
    Then the document is REVIEW_DOCUMENT_COMPLETE only when every required view closes byte-identically and otherwise REVIEW_DOCUMENT_HELD names each missing altered duplicated or unbound section

  @scenario:verify-canonical-circuit-blueprint-replay
  @input:declared-blueprint-lens-set
  @input-contract:blueprint-lens-set.v1
  @event:verify-canonical-circuit-blueprint-replay
  @event-authority:verify-canonical-circuit-blueprint-replay.v1
  @outcome:blueprint-replay-disposition
  @outcome-contract:blueprint-replay-disposition.v1
  Scenario: Verify replay reproduces every projected surface exactly
    Given one projected bundle with its complete Markdown review document and the same lineage-bound authority inputs
    When projection is replayed and each surface and review-document digest is compared
    Then identical inputs reproduce the normalized carrier every projected source and the Markdown review document byte-identically, and any difference is reported as REPLAY_DIVERGED with the expected and observed digests

  @scenario:bind-canonical-circuit-blueprint-projection-receipt
  @input:blueprint-replay-disposition
  @input-contract:blueprint-replay-disposition.v1
  @event:bind-canonical-circuit-blueprint-projection-receipt
  @event-authority:bind-canonical-circuit-blueprint-projection-receipt.v1
  @outcome:canonical-circuit-blueprint-projection-bundle
  @outcome-contract:canonical-circuit-blueprint-projection-bundle.v2
  Scenario: Bind every projected surface to its exact authority digests
    Given one verified projection and its replay disposition
    When the receipt is bound to the carrier, projector, profile, every projected source digest, and the exact Markdown review-document digest
    Then the receipt reports PROJECTED only with a complete review document, otherwise reports REPLAY_DIVERGED or an exact holding disposition, and a bare holding disposition without a code and detail is not accepted as evidence
