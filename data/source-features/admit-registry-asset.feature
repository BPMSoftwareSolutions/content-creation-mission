@capability:admit-registry-asset
@root-scenario:admit-registry-asset
Feature: Admit one reusable vocabulary asset into its registry

  Scenario archetypes are the reusable design vocabulary. Mechanic profiles are
  the reusable execution vocabulary. Provider connections are the reusable
  physical vocabulary. Each is a governed asset, not a template, and each is
  admitted through one circuit so that three registries never become three piles
  of admission mechanics.

  Admission is pure. It consumes the exact asset bytes it is given plus a
  supplied registry inventory and a supplied set of referenced authorities. It
  reads no filesystem, resolves nothing by convention, and admits nothing on the
  strength of a name.

  The separation between the three vocabularies is the property this capability
  exists to defend. A mechanic profile that declares scenario topology has taken
  design authority. A provider connection that declares topology or owns mechanic
  meaning has taken both design and execution authority. Either is an authority
  inversion and returns a finding rather than an admission.

  A scenario archetype must declare its topology and must declare that topology
  immutable under instantiation. An archetype whose geometry may be rewritten by
  its own parameters is a topology generator wearing a template's name.

  A referenced authority that is not admitted cannot be relied upon, and an asset
  is never admitted on unadmitted references. Human admission disposition is
  required and is never inferred from the absence of findings.

  Admission closes when identity is unique, the recomputed digest matches the
  claimed digest exactly, kind conformance passes, references are admitted, a
  human has approved, and the same request reproduces byte-identical evidence.

  @scenario:admit-registry-asset
  @input:registry-asset-admission-request
  @input-contract:registry-asset-admission-request.v1
  @event:admit-registry-asset
  @event-authority:admit-registry-asset.v1
  @outcome:registry-asset-admission-receipt
  @outcome-contract:registry-asset-admission-receipt.v1
  @outcome-terminal
  Scenario: Return one exact admission disposition for one vocabulary asset
    Given one candidate registry asset and its supplied registry inventory
    When the asset is admitted
    Then one receipt binds the asset kind, the recomputed identity and digest, the kind conformance, and the admission disposition
    And ADMITTED is returned only when identity, digest, conformance, references and human approval all close

  @scenario:recompute-asset-identity
  @input:registry-asset-admission-request
  @input-contract:registry-asset-admission-request.v1
  @event:recompute-asset-identity
  @event-authority:recompute-asset-identity.v1
  @outcome:recomputed-asset-identity
  @outcome-contract:registry-admission-carrier.v1
  Scenario: Recompute identity from the exact bytes rather than trusting the claim
    Given one candidate asset carrying a claimed digest
    When the identity is recomputed
    Then the digest is recomputed from the exact supplied bytes
    And a claimed digest that differs from the recomputed digest returns ASSET_DIGEST_DIVERGED

  @scenario:reject-colliding-asset-identity
  @input:registry-asset-admission-request
  @input-contract:registry-asset-admission-request.v1
  @event:reject-colliding-asset-identity
  @event-authority:reject-colliding-asset-identity.v1
  @outcome:identity-collision-disposition
  @outcome-contract:registry-admission-carrier.v1
  Scenario: Refuse to shadow an already admitted identity
    Given one supplied registry inventory
    When the candidate identity is compared
    Then an identity already present in the registry returns ASSET_IDENTITY_COLLIDES
    And an unsupplied registry inventory returns REGISTRY_INVENTORY_UNSUPPLIED rather than treating every identity as unique

  @scenario:conform-scenario-archetype
  @input:registry-admission-inputs
  @input-contract:registry-admission-carrier.v1
  @event:conform-scenario-archetype
  @event-authority:conform-scenario-archetype.v1
  @outcome:archetype-conformance
  @outcome-contract:registry-admission-carrier.v1
  Scenario: Require a scenario archetype to declare immutable topology
    Given one candidate scenario archetype
    When archetype conformance is evaluated
    Then the archetype declares its nodes, its edges and its terminal dispositions
    And an archetype that does not declare nodes, edges, branch geometry, convergence geometry, semantic precedence and terminal structure immutable under instantiation returns ARCHETYPE_GEOMETRY_NOT_IMMUTABLE

  @scenario:conform-mechanic-profile
  @input:registry-admission-inputs
  @input-contract:registry-admission-carrier.v1
  @event:conform-mechanic-profile
  @event-authority:conform-mechanic-profile.v1
  @outcome:profile-conformance
  @outcome-contract:registry-admission-carrier.v1
  Scenario: Require a mechanic profile to declare execution without design
    Given one candidate mechanic profile
    When profile conformance is evaluated
    Then the profile declares its required mechanics and its provider requirements
    And a profile declaring scenario topology returns MECHANIC_PROFILE_DECLARES_TOPOLOGY

  @scenario:conform-provider-connection
  @input:registry-admission-inputs
  @input-contract:registry-admission-carrier.v1
  @event:conform-provider-connection
  @event-authority:conform-provider-connection.v1
  @outcome:connection-conformance
  @outcome-contract:registry-admission-carrier.v1
  Scenario: Require a provider connection to declare realization without meaning
    Given one candidate provider connection
    When connection conformance is evaluated
    Then the connection declares which mechanic requirements it satisfies and the bounds it satisfies them under
    And a connection declaring scenario topology returns PROVIDER_CONNECTION_DECLARES_TOPOLOGY

  @scenario:preserve-vocabulary-separation
  @input:registry-admission-inputs
  @input-contract:registry-admission-carrier.v1
  @event:preserve-vocabulary-separation
  @event-authority:preserve-vocabulary-separation.v1
  @outcome:vocabulary-separation-disposition
  @outcome-contract:registry-admission-carrier.v1
  Scenario: Keep each vocabulary inside its own authority
    Given one candidate asset of any kind
    When vocabulary separation is evaluated
    Then design, execution and physical vocabulary remain in their own registries
    And an asset claiming an authority belonging to another vocabulary returns VOCABULARY_AUTHORITY_INVERTED, because a provider that names the circuit has stopped being a provider

  @scenario:require-admitted-referenced-authority
  @input:registry-admission-inputs
  @input-contract:registry-admission-carrier.v1
  @event:require-admitted-referenced-authority
  @event-authority:require-admitted-referenced-authority.v1
  @outcome:reference-admission-disposition
  @outcome-contract:registry-admission-carrier.v1
  Scenario: Never admit an asset on unadmitted references
    Given one candidate asset referencing other authorities
    When the references are evaluated
    Then every referenced authority is admitted and exact
    And any unadmitted reference returns REFERENCED_AUTHORITY_UNADMITTED

  @scenario:require-human-admission-disposition
  @input:registry-admission-inputs
  @input-contract:registry-admission-carrier.v1
  @event:require-human-admission-disposition
  @event-authority:require-human-admission-disposition.v1
  @outcome:human-disposition
  @outcome-contract:registry-admission-carrier.v1
  Scenario: Require an explicit human disposition
    Given one candidate asset that has closed every deterministic gate
    When the human disposition is evaluated
    Then admission proceeds only on an explicit APPROVE
    And an absent, held or rejected disposition returns HUMAN_ADMISSION_NOT_APPROVED, because zero findings is not approval

  @scenario:replay-registry-admission
  @input:registry-admission-inputs
  @input-contract:registry-admission-carrier.v1
  @event:replay-registry-admission
  @event-authority:replay-registry-admission.v1
  @outcome:admission-replay-disposition
  @outcome-contract:registry-admission-carrier.v1
  Scenario: Require byte-identical replay without self-issued correctness
    Given one frozen admission request
    When the asset is admitted twice
    Then both receipts are byte-identical
    And a divergent replay returns REGISTRY_ADMISSION_REPLAY_DIVERGED rather than the later receipt
