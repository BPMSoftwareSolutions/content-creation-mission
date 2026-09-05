@capability:establish-human-capability-ownership-review-receipt
@root-scenario:establish-human-capability-ownership-review-receipt
Feature: Establish attributable ownership-review testimony

  An approved human ownership review must become attributable durable
  testimony without changing any exact case-level decision or allowing one
  locally held case to hold unrelated cases.

  @scenario:establish-human-capability-ownership-review-receipt
  @input:approved-human-capability-ownership-review-transcription
  @input-contract:approved-human-capability-ownership-review-transcription.v1
  @event:establish-human-capability-ownership-review-receipt
  @event-authority:establish-human-capability-ownership-review-receipt.v1
  @outcome:human-capability-ownership-review-receipt
  @outcome-contract:human-capability-ownership-review-receipt.v1
  @outcome-terminal
  Scenario: Establish one attributable durable receipt from approved review testimony
    Given one approved human ownership-review transcription with exact case-level decisions
    When the governed ownership-review receipt is established
    Then attributable durable ownership-review testimony preserves every exact case-level disposition, including every exact locally held case
