@capability:bind-model-testimony-evidence
@root-scenario:bind-model-testimony-evidence
Feature: Bind immutable model testimony to deterministic evidence

  A downstream consumer supplies governed references to one exact model request
  and one exact model response. The capability observes their bytes through an
  admitted file-observation port, validates that the response is obtained from
  Gemini in exactly one attempt and contains one structured candidate object,
  and returns content digests plus retained provider lineage. It never obtains
  a new model response, alters testimony, accepts a candidate, or writes code.

  Missing files, malformed JSON, a non-obtained disposition, a non-Gemini
  provider, an attempt count other than one, or a missing structured value are
  returned as attributable rejection evidence. Candidate hashing uses the
  canonical compact JSON serialization of the structured value. Request and
  response hashing uses the exact observed bytes.

  The execution authority must first transform the input into a bounded
  `sda-governed-repository-observation-port.v1` request for exactly the two
  declared resources, then decode each returned `exactBytes` value with the
  admitted `base64-decode-utf8` transformation, parse the response with
  `parse-json`, serialize `result.structuredValue` with `json-stringify`, and
  hash that serialization with `sha256`. A pure transformation port must not
  stand in for repository observation.

  @scenario:bind-model-testimony-evidence
  @input:model-testimony-binding-request
  @input-contract:model-testimony-binding-request.v1
  @event:bind-model-testimony-evidence
  @event-authority:bind-model-testimony-evidence.v1
  @outcome:model-testimony-binding-evidence
  @outcome-contract:model-testimony-binding-evidence.v1
  @outcome-terminal
  Scenario: Return digest-bound testimony evidence
    Given governed request and response references with exact observed bytes
    When the response structure, Gemini provider identity, and one-attempt proof are validated
    Then request, response, and structured-candidate hashes plus provider, model, invocation, and attempt lineage are returned, or attributable rejection evidence is returned without accepting the candidate
