@capability:admit-capability-authority
@root-scenario:evaluate-capability-authority-admission
Feature: Admit exact capability authority before capsule sealing

  Admit exact proof-complete capability authority before capsule sealing without publishing or mutating the estate.

  @scenario:evaluate-capability-authority-admission
  @input:admission-context
  @input-contract:capability-authority-admission-context.v1
  @event:admit-exact-capability-authority
  @event-authority:admit-capability-authority.v1
  @outcome:admission-classified
  @outcome-contract:capability-authority-admission-result.v1
  Scenario: Evaluate capability authority admission
    Given one exact reviewed and proof-complete target-neutral capability candidate
    When capability authority admission is evaluated against exact review and proof lineage
    Then the candidate is classified as admitted or held

  @scenario:return-admission-hold
  @input:held-classification
  @input-contract:capability-authority-admission-result.v1
  @event:bind-admission-hold
  @event-authority:bind-admission-hold.v1
  @outcome:capability-authority-held
  @outcome-contract:capability-authority-admission-result.v1
  @outcome-terminal
  Scenario: Return admission hold
    Given an exact held capability-authority admission classification
    When the held admission receipt is bound
    Then CAPABILITY_AUTHORITY_HELD is returned

  @scenario:return-admitted-authority
  @input:admitted-classification
  @input-contract:capability-authority-admission-result.v1
  @event:bind-admitted-authority
  @event-authority:bind-admitted-authority.v1
  @outcome:capability-authority-admitted
  @outcome-contract:capability-authority-admission-result.v1
  @outcome-terminal
  Scenario: Return admitted authority
    Given an exact successful capability-authority admission classification
    When the admitted authority receipt is bound
    Then CAPABILITY_AUTHORITY_ADMITTED is returned
