@capability:generate-governed-narration
@root-scenario:generate-governed-narration
Feature: Generate governed narration

  An admitted presentation scene graph carries narration intent: what must be
  said, in what order, at what altitude, and on whose authority. Nothing in the
  estate can turn that intent into sound. This capability realizes it as an
  attributable audio artifact that physically exists and can be played.

  Narration is spoken authority. Every assertion the narration voices must trace
  to the admitted authority or evidence reference that grounds it. An assertion
  the scene graph does not ground is a grounding finding, not a sentence the
  provider is free to invent.

  The public boundary is the responsibility itself: one admitted presentation
  scene graph in, one narration asset out. Nothing between them is a caller's
  concern, and no adapter stands between this capability and the narration
  responsibility it supplies. A consumer that must first translate its scene
  graph into some other request shape has been handed a different capability
  than the one it needed.

  The provider is replaceable. This capability declares what narration must be
  produced from the scene graph and what testimony the provider must return. The
  endpoint, model identity, response modality, wire protocol, and voice
  realization are realization authority bound beneath it, never semantics
  declared here. A different admitted provider satisfying the same contract is a
  rebinding, not a new capability.

  Narration crosses two physical boundaries, and the design admits both rather
  than hiding them inside ordinary responsibilities. Generating speech descends
  into a declared narration generation slot; writing audio descends into a
  declared binary artifact materialization slot. Both slots are provider-neutral
  here: what realizes them is bound beneath this capability, and a capability
  that declares no such descent could never emit a byte while still appearing
  well formed.

  Three boundaries fail closed and are never collapsed into one another. A
  provider that returns no audio modality, an empty payload, or an undecodable
  one has produced no narration, and the request is held with attributable
  provider testimony rather than completed with silence. A payload that is
  perfectly valid but cannot be written leaves no artifact at all, and that is
  held as failed materialization. Separately again, bytes that do reach storage
  but whose digest, provider lineage, or grounding cannot be established are not
  governed narration: a file existing is not an asset being admitted, and such an
  artifact is returned as an unattributable-artifact finding. Nothing existing and
  something existing unattributably are different states of the world.

  Proof of this capability requires an actual audio artifact. Testimony that the
  circuit ran, over no bytes, proves a projection rather than narration.

  This capability does not compose video, select scenes, author narration text,
  admit the scene graph it consumes, or claim that the narration is faithful to
  the meaning it describes. Fidelity is evaluated elsewhere against the admitted
  authority.

  @scenario:generate-governed-narration
  @input:presentation-scene-graph
  @input-contract:presentation-scene-graph.v1
  @event:generate-governed-narration
  @event-authority:generate-governed-narration.v1
  @outcome:video-narration-asset
  @outcome-contract:video-narration-asset.v1
  Scenario: Turn one admitted presentation scene graph into one narration asset
    Given one admitted presentation scene graph carrying the narration intent and performance profile that govern it
    When narration is realized for that scene graph
    Then exactly one narration asset is returned for it, or exact held or rejection evidence naming the boundary that stopped it, and no narration is claimed for a scene graph the capability was not given

  @scenario:resolve-narration-generation-authority
  @input:presentation-scene-graph
  @input-contract:presentation-scene-graph.v1
  @event:resolve-narration-generation-authority
  @event-authority:resolve-narration-generation-authority.v1
  @outcome:authorized-narration-generation-request
  @outcome-contract:authorized-narration-generation-request.v1
  @outcome-variants:NARRATION_AUTHORITY_RESOLVED|NARRATION_INTENT_UNGROUNDED
  Scenario: Resolve the narration authority that grounds every assertion
    Given one admitted presentation scene graph and the admitted authority it binds its narration intent to
    When each declared assertion is resolved against that authority
    Then one authorized request carries the exact scene-graph digest, performance intent, and every assertion bound to the authority or evidence reference grounding it, and an assertion without such a reference holds generation as ungrounded narration intent rather than delegating it to the provider

  @scenario:invoke-governed-narration-provider
  @input:authorized-narration-generation-request
  @input-contract:authorized-narration-generation-request.v1
  @event:invoke-governed-narration-provider
  @event-authority:invoke-governed-narration-provider.v1
  @outcome:narration-media-testimony
  @outcome-contract:narration-media-testimony.v1
  @outcome-variants:NARRATION_MEDIA_RETURNED|PROVIDER_MODALITY_ABSENT|PROVIDER_PAYLOAD_UNUSABLE
  Scenario: Invoke the bound narration provider for one authorized request
    Given one authorized narration generation request and the admitted provider realization bound beneath this capability
    When the provider is invoked under its declared attempt authority
    Then one media testimony retains provider identity, request and response hashes, attempt count, and timing alongside the returned audio payload; a response carrying no audio modality is held as absent modality; and an empty or undecodable payload is held as unusable rather than materialized as silence

  @scenario:materialize-narration-artifact
  @input:narration-media-testimony
  @input-contract:narration-media-testimony.v1
  @event:materialize-narration-artifact
  @event-authority:materialize-narration-artifact.v1
  @outcome:attributable-narration-artifact
  @outcome-contract:attributable-narration-artifact.v1
  @outcome-variants:NARRATION_ARTIFACT_MATERIALIZED|ARTIFACT_MATERIALIZATION_FAILED|ARTIFACT_LINEAGE_UNATTRIBUTABLE
  Scenario: Materialize the returned payload as physical audio bytes
    Given one media testimony carrying a decodable audio payload
    When the payload is decoded and written through the declared binary artifact materialization slot
    Then one artifact record carries the physical location, byte length, and content digest of audio that exists on disk, together with the provider lineage and scene-graph digest that produced it; a valid payload the store cannot write leaves no artifact and holds materialization as failed; and bytes that do exist but whose digest, provider lineage, or grounding cannot be established are returned as an unattributable artifact rather than reported as narration

  @scenario:admit-governed-narration-asset
  @input:attributable-narration-artifact
  @input-contract:attributable-narration-artifact.v1
  @event:admit-governed-narration-asset
  @event-authority:admit-governed-narration-asset.v1
  @outcome:video-narration-asset
  @outcome-contract:video-narration-asset.v1
  @outcome-variants:NARRATION_ASSET_ADMITTED|NARRATION_ASSET_REJECTED
  @outcome-terminal
  Scenario: Admit exactly one narration asset from the attributable artifact
    Given one attributable narration artifact and the declared narration asset contract
    When admission is resolved over the artifact, its grounding, and its lineage
    Then exactly one narration asset is established carrying the audio location, digest, duration profile, grounded assertion set, and provider lineage, and an artifact failing its declared contract is returned as exact rejection evidence without establishing an asset
