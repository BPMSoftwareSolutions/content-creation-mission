@capability:manage-capability-capsule
@root-scenario:collapse-admitted-capability
Feature: Manage one capability capsule through collapse and reveal

  Store the capability once in its smallest admitted semantic form.
  Project every human-readable, executable, visual, testable, and
  target-specific representation on demand. Version the capability, not
  its redundant projections.

  Packaging preserves capability identity. Revelation exposes capability
  meaning. Realization binds capability meaning to an execution
  environment. Execution produces the effect. Those are four separate
  responsibilities; this capability owns exactly two of them: COLLAPSE
  and REVEAL, as one reversible relationship — collapse an expanded
  admitted capability into a content-addressed capsule, and reveal any
  requested representation deterministically from that capsule.

  The capsule is portable, immutable, content-addressed, self-describing,
  self-revealing, verifiable, and projectable — but never self-executing
  and never self-admitting. The language executable must not become the
  sole durable representation of the capability. Round-trip closure is
  the conformance law: reveal(package(X)) must reproduce the canonical
  capability representation of X. Every scenario admits and emits one
  shared capsule record.

  Resource selection follows declared authority, never filename
  convention. The feature entry resolves at the exact path the workspace
  authority declares. Every contract schema file named by the admitted
  contract vocabulary packs when present. A capability whose declared
  feature cannot be resolved fails closed with
  FEATURE_AUTHORITY_MISSING rather than packing a capsule without its
  meaning.

  @scenario:collapse-admitted-capability
  @input:capability-capsule-record
  @input-contract:capability-capsule-record.v1
  @event:capability-capsule-collapse-requested
  @event-authority:collapse-admitted-capability.v1
  @outcome:capability-capsule-record
  @outcome-contract:capability-capsule-record.v1
  @outcome-terminal
  Scenario: Collapse one admitted capability into a content-addressed capsule
    Given one path to an admitted capability
    When the capsule is collapsed
    Then the capability authority is observed from that path, the minimum sufficient admitted representation binds into one physical capsule whose content address is the digest of its own bytes, and the capsule is written as one .sfxcap artifact with disposition CAPSULE_PACKED

  @scenario:resolve-capsule-contract-resource-closure
  @input:capability-capsule-record
  @input-contract:capability-capsule-record.v1
  @event:capsule-contract-resource-closure-requested
  @event-authority:resolve-capsule-contract-resource-closure.v1
  @outcome:capability-capsule-record
  @outcome-contract:capability-capsule-record.v1
  @outcome-terminal
  Scenario: Resolve every catalog-declared contract schema into the capsule resource set
    Given one observed contract catalog from the admitted capability path
    When capsule contract resource closure is resolved
    Then every catalog value becomes exactly one deterministic contracts resource declaration before capability files are observed

  @scenario:reveal-capability-representation
  @input:capability-capsule-record
  @input-contract:capability-capsule-record.v1
  @event:capability-representation-revelation-requested
  @event-authority:reveal-capability-representation.v1
  @outcome:capability-capsule-record
  @outcome-contract:capability-capsule-record.v1
  @outcome-terminal
  Scenario: Reveal one requested representation deterministically
    Given one verified capsule digest and one requested representation profile from the declared representation set
    When the representation is revealed
    Then the requested view is deterministically available and bound to the same capsule digest, and an undeclared profile reports REPRESENTATION_UNDECLARED

  @scenario:prove-capsule-round-trip-closure
  @input:capability-capsule-record
  @input-contract:capability-capsule-record.v1
  @event:capability-round-trip-closure-proof-requested
  @event-authority:prove-capsule-round-trip-closure.v1
  @outcome:capability-capsule-record
  @outcome-contract:capability-capsule-record.v1
  @outcome-terminal
  Scenario: Prove reveal of package reproduces the canonical capability
    Given one expanded capability whose canonical digest is declared and one capsule collapsed from it
    When the canonical representation is revealed
    Then the revealed canonical digest equals the declared canonical digest with disposition REVEAL_PACK_CLOSED, and any mismatch reports ROUND_TRIP_OPEN

  @scenario:resolve-minimum-sufficient-representation
  @input:capability-capsule-record
  @input-contract:capability-capsule-record.v1
  @event:minimum-sufficient-representation-resolution-requested
  @event-authority:resolve-minimum-sufficient-representation.v1
  @outcome:capability-capsule-record
  @outcome-contract:capability-capsule-record.v1
  @outcome-terminal
  Scenario: Keep only the minimum sufficient admitted representation
    Given the declared authority bindings and the admitted derivable-kind list
    When sufficiency is evaluated
    Then every binding kind is admitted, no derivable representation is stored as durable authority, and a redundant representation reports REDUNDANT_REPRESENTATION_STORED

  @scenario:verify-capsule-self-description-boundary
  @input:capability-capsule-record
  @input-contract:capability-capsule-record.v1
  @event:capability-self-description-boundary-verification-requested
  @event-authority:verify-capsule-self-description-boundary.v1
  @outcome:capability-capsule-record
  @outcome-contract:capability-capsule-record.v1
  @outcome-terminal
  Scenario: Prove the capsule is self-describing but never self-admitting or self-executing
    Given the declared self-description boundary
    When the boundary is verified
    Then the capsule declares selfDescribing true, selfAdmitting false, embeddedExecutable false, and selfExecuting false, and any violation reports SELF_ADMISSION_CLAIMED

  @scenario:bind-capsule-reference
  @input:capability-capsule-record
  @input-contract:capability-capsule-record.v1
  @event:capability-capsule-reference-binding-requested
  @event-authority:bind-capsule-reference.v1
  @outcome:capability-capsule-record
  @outcome-contract:capability-capsule-record.v1
  @outcome-terminal
  Scenario: Bind the tiny pointer that versions identity and succession
    Given one packed capsule with a declared predecessor
    When the capsule reference is bound
    Then the pointer records capability identity, version, capsule digest, predecessor digest, and format version, and nothing else

  @scenario:reproduce-capsule-digest
  @input:capability-capsule-record
  @input-contract:capability-capsule-record.v1
  @event:capability-capsule-digest-reproduction-requested
  @event-authority:reproduce-capsule-digest.v1
  @outcome:capability-capsule-record
  @outcome-contract:capability-capsule-record.v1
  @outcome-terminal
  Scenario: Reproduce one content address from identical admitted inputs
    Given identical admitted inputs are collapsed in different process and discovery orders
    When the capsule digest is recomputed
    Then the content address is identical without timestamp, machine, user, or path input
