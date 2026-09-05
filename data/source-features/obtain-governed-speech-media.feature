@capability:obtain-governed-speech-media
@root-scenario:obtain-governed-speech-media
Feature: Obtain governed speech media from the bound narration provider

  The narration capability declares the semantic requirement
  generate-speech-audio. This capability realizes it: one authorized
  narration generation request in, one attributable speech media testimony
  out, through the bound speech provider.

  The provider is replaceable. This capability declares what speech media
  must be produced — an audio modality with decodable bytes — and what
  testimony the provider must return. The endpoint, model identity, wire
  protocol, and voice realization are realization authority bound beneath
  it, never semantics declared here. A different admitted provider
  satisfying the same contract is a rebinding, not a new capability.

  Speech generation descends into one declared speech generation slot. The
  slot is provider-neutral here: what realizes it is bound beneath this
  capability.

  The boundary fails closed and is never collapsed. A provider that returns
  no audio modality has produced no speech media and is held as absent
  modality. An empty or undecodable payload is held as unusable rather than
  materialized as silence. Only a decodable audio payload with its provider
  identity, request and response hashes, attempt count, and timing becomes
  speech media testimony.

  Model output remains untrusted testimony. Obtaining speech media
  establishes no admission, no fidelity claim, and no artifact existence.

  @scenario:obtain-governed-speech-media
  @input:authorized-narration-generation-request
  @input-contract:authorized-narration-generation-request.v1
  @event:obtain-governed-speech-media
  @event-authority:obtain-governed-speech-media.v1
  @outcome:narration-media-testimony
  @outcome-contract:narration-media-testimony.v1
  @outcome-variants:NARRATION_MEDIA_RETURNED|PROVIDER_MODALITY_ABSENT|PROVIDER_PAYLOAD_UNUSABLE
  @outcome-terminal
  Scenario: Obtain one attributable speech media testimony
    Given one authorized narration generation request and the admitted speech provider realization bound beneath this capability
    When the provider is invoked under its declared attempt authority
    Then one media testimony retains provider identity, request and response hashes, attempt count, and timing alongside the returned audio payload; a response carrying no audio modality is held as absent modality; and an empty or undecodable payload is held as unusable rather than materialized as silence

  @scenario:project-speech-generation-request
  @input:authorized-narration-generation-request
  @input-contract:authorized-narration-generation-request.v1
  @event:project-speech-generation-request
  @event-authority:project-speech-generation-request.v1
  @outcome:speech-generation-invocation
  @outcome-contract:speech-generation-invocation.v1
  Scenario: Project the authorized request into the bound speech provider wire request
    Given one authorized narration generation request and the admitted provider protocol adapter for the bound provider
    When the provider-neutral request is projected into the provider wire request
    Then the exact wire request carries the narration text, the declared voice and performance profile, and the audio response modality, without credential bytes and without provider-specific schema knowledge leaking into the caller

  @scenario:observe-governed-speech-exchange
  @input:speech-generation-invocation
  @input-contract:speech-generation-invocation.v1
  @event:observe-governed-speech-exchange
  @event-authority:observe-governed-speech-exchange.v1
  @outcome:speech-provider-observation
  @outcome-contract:speech-provider-observation.v1
  Scenario: Observe one governed speech exchange
    Given one projected speech generation invocation under the declared provider authority
    When the governed exchange is performed once under the declared attempt authority
    Then one observation carries the raw provider response with its audio payload or its exact failure disposition, request and response hashes, provider identity, and timing, and no retry or substitution occurs beyond the declared attempt authority
