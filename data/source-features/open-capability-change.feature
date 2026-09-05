@capability:open-capability-change
@root-scenario:open-capability-change
Feature: Open one governed capability change

  An engineer or agent starts from one capability identity and one bounded
  reason for change. The opened change fixes its exact origin, separates
  the smallest authorized mutation set from the wider impact proof set, and
  establishes an isolated authoring boundary before any candidate authority
  may change.

  A change is one of exactly two kinds. A revision opens against an admitted
  capsule. A first admission opens against a capability identity that has no
  admitted capsule, where the reviewed canonical feature and its approved
  canonical blueprint are the authority the authoring boundary is established
  from. First admission is its own legitimate input condition, not a tolerated
  missing baseline: no capsule digest is fabricated, no baseline artefact is
  copied, and a feature is never presented as a capsule.

  Opening never mutates admitted authority, silently authorizes related
  capabilities, or treats dependency impact as co-change permission. If the
  change kind, origin, reason, or mutation boundary cannot be resolved
  exactly, the change is held without a partial change set.

  @scenario:open-capability-change
  @input:capability-change-open-request
  @input-contract:capability-change-open-request.v1
  @event:capability-change-opening-requested
  @event-authority:open-capability-change.v1
  @outcome:capability-change-set
  @outcome-contract:capability-change-set.v1
  @outcome-terminal
  Scenario: Open one governed change from admitted authority
    Given one root capability identity and one bounded reason for change
    When capability change opening is requested
    Then one OPEN change set binds its identity, reason, resolved change kind and origin, mutation set, impact proof set, authoring boundary, evidence stream, and authorized next action, or exact held findings are returned without changing admitted authority

  @scenario:resolve-capability-change-kind
  @input:capability-change-open-request
  @input-contract:capability-change-open-request.v1
  @event:capability-change-kind-resolution-requested
  @event-authority:resolve-capability-change-kind.v1
  @outcome:capability-change-kind
  @outcome-contract:capability-change-kind.v1
  @outcome-variants:REVISION|FIRST_ADMISSION|CHANGE_KIND_UNRESOLVED
  @outcome-terminal
  Scenario: Resolve which kind of change is being opened
    Given one root capability identity and the current admitted estate and repository testimony
    When the change kind is resolved
    Then the change is REVISION when an admitted capsule exists for that exact identity and FIRST_ADMISSION when none does, and an identity whose admitted presence cannot be observed exactly is returned as exact held findings rather than assumed to be either kind

  @scenario:resolve-capability-change-baseline
  @input:capability-change-kind
  @input-contract:capability-change-kind.v1
  @event:capability-change-baseline-resolution-requested
  @event-authority:resolve-capability-change-baseline.v1
  @outcome:capability-change-origin
  @outcome-contract:capability-change-origin.v1
  @outcome-terminal
  Scenario: Resolve the exact admitted baseline of a revision
    Given one root capability identity resolved as a revision and the current admitted estate and repository testimony
    When its change baseline is resolved
    Then the origin binds the admitted capsule, authority, blueprint, dependency, and repository identities without inferring a missing or ambiguous identity

  @scenario:resolve-first-admission-authority
  @input:capability-change-kind
  @input-contract:capability-change-kind.v1
  @event:first-admission-authority-resolution-requested
  @event-authority:resolve-first-admission-authority.v1
  @outcome:capability-change-origin
  @outcome-contract:capability-change-origin.v1
  @outcome-terminal
  Scenario: Resolve the reviewed authority a first admission opens against
    Given one capability identity resolved as a first admission, its reviewed canonical feature, and the approved canonical blueprint governing that feature
    When the first-admission authority is resolved
    Then the origin binds the exact feature bytes, blueprint authority digest, carrier digest, reviewer-authority digest, and approved review-boundary digest and declares that no admitted capsule exists for that identity, and an admitted capsule that unexpectedly exists, a blueprint that does not govern that feature, or an absent, unapproved, superseded, or digest-divergent review is returned as exact held findings

  @scenario:resolve-capability-change-impact
  @input:capability-change-origin
  @input-contract:capability-change-origin.v1
  @event:capability-change-impact-resolution-requested
  @event-authority:resolve-capability-change-impact.v1
  @outcome:capability-change-impact
  @outcome-contract:capability-change-impact.v1
  @outcome-terminal
  Scenario: Separate authorized mutation from required proof
    Given one resolved change origin and the admitted semantic dependency graph reachable from it
    When change impact is resolved
    Then the mutation set contains only explicitly authorized capabilities while the impact proof set contains every affected capability, route, contract, and experience that must be reproven

  @scenario:establish-capability-change-authoring-boundary
  @input:capability-change-impact
  @input-contract:capability-change-impact.v1
  @event:capability-change-authoring-boundary-requested
  @event-authority:establish-capability-change-authoring-boundary.v1
  @outcome:capability-change-authoring-boundary
  @outcome-contract:capability-change-authoring-boundary.v1
  @outcome-variants:BOUNDARY_ESTABLISHED|BOUNDARY_UNAVAILABLE
  @outcome-terminal
  Scenario: Establish an isolated bounded authoring experience
    Given one exact change origin, mutation set, and impact proof set
    When the authoring boundary is established
    Then candidate authority is isolated from admitted authority, only the mutation set is writable, every dependency and proof subject remains immutable, and the admitted mainline remains unchanged, where a revision boundary carries the admitted baseline capsule into isolation and a first-admission boundary is bounded by the approved blueprint alone without copying, fabricating, or substituting any baseline artefact

  @scenario:hold-unopenable-capability-change
  @input:capability-change-opening-findings
  @input-contract:capability-change-opening-findings.v1
  @event:capability-change-opening-disposition-requested
  @event-authority:hold-unopenable-capability-change.v1
  @outcome:held-capability-change
  @outcome-contract:held-capability-change.v1
  @outcome-terminal
  Scenario: Hold a change whose boundary cannot be established exactly
    Given an unresolvable change kind, missing admitted authority, an unresolved reason, divergent origin testimony, an ambiguous mutation set, or an unavailable isolation effect
    When the opening disposition is resolved
    Then the change reports OPENING_HELD with exact findings and no partial change set, candidate mutation, or admitted-authority change

