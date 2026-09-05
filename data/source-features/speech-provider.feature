@capability:speech-provider
@root-scenario:speech-provider-exchange
Feature: Realize one governed speech provider exchange through explicit candidate effect envelopes

  This candidate explicitly constructs the admitted credential-binding and governed-HTTP
  input envelopes and returns the raw providerExchangeResponse seam expected by the
  obtain-governed-speech-media consumer. The audio adapter, OpenAI profile, local requester authorization, audio normalization, and binary identity remain typed candidate divergences.

  @scenario:speech-provider-exchange
  @input:speech-generation-invocation
  @input-contract:speech-generation-invocation.v2
  @event:speech-provider-exchange
  @event-authority:speech-provider-exchange.v3
  @outcome:speech-provider-exchange-response
  @outcome-contract:speech-provider-exchange-response.v2
  @outcome-variants:SPEECH_EXCHANGE_RETURNED|PROVIDER_MODALITY_ABSENT|PROVIDER_PAYLOAD_UNUSABLE|PROVIDER_INVOCATION_FAILED|CREDENTIAL_MISSING|CREDENTIAL_UNAUTHORIZED
  @outcome-terminal
  Scenario: Perform one bounded speech provider exchange through explicit governed effect envelopes
    Given one speech generation invocation with audio response modality and maximumAttempts equal to one
    When the audio adapter emits a credential-binding request and complete governed HTTP request template, the credential effect returns an opaque binding disposition, only CREDENTIAL_BOUND receives a bound HTTP envelope, and one governed HTTP exchange returns exact byte testimony
    Then the provider returns candidate identity, modality, attempt count, timing, audioPayload, physical responseBodyHash, boundedBytes, responseBodyBytesBase64, content type, findings, and terminal disposition; retry and substitution remain forbidden
