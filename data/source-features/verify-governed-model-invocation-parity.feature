@capability:verify-governed-model-invocation-parity
@root-scenario:verify-governed-model-invocation-parity
Feature: Verify governed model invocation parity

  Capabilities that invoke the same governed model capability under the same
  admitted invocation profile must not each reinvent the terms of that
  invocation.

  This capability compares the declared invocations of two or more capabilities
  against the admitted invocation authority they share.

  What each capability asks the model is its own product and may differ. How the
  invocation is governed may not.

  A divergence is reported as an exact finding before any external effect
  occurs, rather than discovered by invoking a provider.

  @scenario:verify-governed-model-invocation-parity
  @input:governed-model-invocation-parity-request
  @input-contract:governed-model-invocation-parity-request.v1
  @event:verify-governed-model-invocation-parity
  @event-authority:verify-governed-model-invocation-parity.v1
  @outcome:governed-model-invocation-parity-evidence
  @outcome-contract:governed-model-invocation-parity-evidence.v1
  @outcome-terminal
  Scenario: Verify that every declared invocation shares one governed contract
    Given two or more declared model invocations and the admitted invocation authority they share
    When every governed term of each invocation is compared with the admitted authority and with the other invocations
    Then invocation parity is proven, or it is violated with one exact finding for each diverging term

  @scenario:admit-declared-model-invocations
  @input:governed-model-invocation-parity-request
  @input-contract:governed-model-invocation-parity-request.v1
  @event:admit-declared-model-invocations
  @event-authority:admit-declared-model-invocations.v1
  @outcome:admitted-declared-model-invocations
  @outcome-contract:admitted-declared-model-invocations.v1
  @outcome-terminal
  Scenario: Admit the invocations being compared
    Given the declared invocations of two or more capabilities and one admitted invocation authority
    When each declaring capability, its invocation binding, and the shared authority are observed without model, network, or clock access
    Then the invocations are admitted for comparison, or comparison is held when any invocation or the shared authority cannot be observed

  @scenario:compare-governed-invocation-terms
  @input:admitted-declared-model-invocations
  @input-contract:admitted-declared-model-invocations.v1
  @event:compare-governed-invocation-terms
  @event-authority:compare-governed-invocation-terms.v1
  @outcome:compared-governed-invocation-terms
  @outcome-contract:compared-governed-invocation-terms.v1
  @outcome-terminal
  Scenario: Compare every term that may not vary by caller
    Given the admitted invocations and the governed terms the shared authority fixes
    When provider authority, fallback authority, credential reference, response policy, execution policy, evidence policy, timeout, result mode, model role binding, required carrier, and invocation port identity and digests are compared across every invocation
    Then each diverging term is named exactly with the capabilities that disagree, and terms the authority permits to vary by caller are excluded from comparison

  @scenario:resolve-invocation-parity-disposition
  @input:compared-governed-invocation-terms
  @input-contract:compared-governed-invocation-terms.v1
  @event:resolve-invocation-parity-disposition
  @event-authority:resolve-invocation-parity-disposition.v1
  @outcome:governed-model-invocation-parity-evidence
  @outcome-contract:governed-model-invocation-parity-evidence.v1
  @outcome-terminal
  Scenario: Resolve whether invocation parity holds
    Given every compared term and its divergences
    When the divergences are resolved in stable term order
    Then parity is INVOCATION_PARITY_CONFORMS with no findings, or INVOCATION_PARITY_VIOLATED carrying one finding per diverging term
