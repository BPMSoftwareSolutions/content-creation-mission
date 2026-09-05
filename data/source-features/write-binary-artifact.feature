@capability:write-binary-artifact
@root-scenario:write-binary-artifact
@lifecycle:CANDIDATE_SUCCESSOR_V7
Feature: Write binary artifact from the exact parent carrier through the admitted bounded filesystem store

  As a governed artifact producer
  I want the successor parent-supplied complete WAV carrier delivered as encoding=base64
  So that invalid requests are rejected before effects, write outcomes return as evidence, and accepted bytes are independently read back

  @scenario:write-binary-artifact
  @input:binary-artifact-write-request
  @input-contract:binary-artifact-write-request.v1
  @event:materialize-governed-artifact
  @event-authority:materialize-governed-artifact.v1
  @outcome:binary-artifact-write-outcome
  @outcome-contract:binary-artifact-write-outcome.v2
  Scenario: Write and verify the successor parent-produced complete WAV request
    Given the successor parent request {contractId: binary-artifact-write-request.v1, payload: {encoding: base64, bytesBase64: complete WAV carrier}}
    When pre-effect validation accepts the carrier and the admitted sda-filesystem-artifact-store.v1 stages a bounded write and atomically renames it
    Then derive a bounded destination from the decoded-byte SHA-256, read the destination bytes, and require byte length and SHA-256 equality before SUCCEEDED

  @scenario:validate-binary-artifact-write-request
  @input:binary-artifact-write-request
  @input-contract:binary-artifact-write-request.v1
  @event:validate-binary-artifact-write-request
  @event-authority:validate-binary-artifact-write-request.v1
  @outcome:binary-artifact-write-validation
  @outcome-contract:binary-artifact-write-validation.v1
  @outcome-variants:ACCEPTED|REJECTED
  Scenario: Validate the request before any physical effect
    Given a request whose encoding, base64 syntax, bounded destination safety, and collision policy can be checked without writing
    When the pre-effect validation boundary evaluates the request
    Then ACCEPTED proceeds to the provider or REJECTED terminates without filesystem descent

  @scenario:observe-binary-artifact-write-result
  @input:binary-artifact-write-observation
  @input-contract:binary-artifact-write-observation.v1
  @event:observe-binary-artifact-write-result
  @event-authority:observe-binary-artifact-write-result.v1
  @outcome:binary-artifact-write-result
  @outcome-contract:binary-artifact-write-result.v1
  @outcome-variants:WRITE_ESTABLISHED|WRITE_FAILED|HELD
  Scenario: Observe the bounded filesystem write result before read-back
    Given one admitted filesystem write attempt and its bounded write receipt
    When the write effect returns to the capability evidence boundary
    Then WRITE_ESTABLISHED alone may descend to read-back, while WRITE_FAILED or HELD terminate locally

  @scenario:verify-binary-artifact-readback
  @input:binary-artifact-readback-observation
  @input-contract:binary-artifact-readback-observation.v2
  @event:verify-binary-artifact-readback
  @event-authority:verify-binary-artifact-readback.v1
  @outcome:binary-artifact-write-outcome
  @outcome-contract:binary-artifact-write-outcome.v2
  @outcome-variants:SUCCEEDED|HELD
  Scenario: Verify one physical artifact read-back
    Given one bounded write effect and one physical byte read-back observation
    When decoded-byte length and SHA-256 are compared with the candidate expectation
    Then SUCCEEDED or HELD is selected by the declared read-back evidence
