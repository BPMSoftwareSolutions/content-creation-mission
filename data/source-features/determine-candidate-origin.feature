@capability:determine-candidate-origin
@root-scenario:determine-candidate-origin
Feature: Determine candidate origin

  As a language maintainer I want to evaluate candidate files so that I can verify whether every file is projected, hand authored, mixed, or absent before promotion.

  @scenario:determine-candidate-origin
  @input:candidate-file-and-manifest-facts
  @input-contract:determine-candidate-origin-input.v1
  @event:candidate-origin-determination-requested
  @event-authority:candidate-origin-determination.v1
  @outcome:candidate-origin-known
  @outcome-contract:candidate-origin-evidence.v1
  @outcome-terminal
  Scenario: Determine candidate origin from candidate files and manifest facts
    Given a candidate file set and manifest facts are ready for evaluation
    When candidate origin determination is requested
    Then candidate origin evidence is generated with origin classification and file counts
