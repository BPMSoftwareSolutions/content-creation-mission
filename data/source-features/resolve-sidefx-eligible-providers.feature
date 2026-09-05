@capability:resolve-sidefx-eligible-providers
@root-scenario:resolve-sidefx-eligible-providers
Feature: Resolve eligible providers from explicit binding evidence only

  A provider is eligible only when admitted authority says so. This capability
  evaluates declared provider bindings against the requested platform
  capability and projection target, and admits one only when its binding is
  ADMITTED, its conformance receipt carries an admitted disposition, and the
  binding itself declares the requested target. Every returned provider cites
  its exact binding reference and digest, provider authority reference and
  digest, profile and policy bindings, and conformance receipt reference and
  digest. A provider that is admitted and conformant but
  declares no projection target is not quietly assumed to support it: the
  result is NOT_OBSERVABLE and the missing declaration is reported as a finding
  against the estate.

  @scenario:resolve-sidefx-eligible-providers
  @input:sidefx-provider-resolution-request
  @input-contract:sidefx-provider-resolution-request.v1
  @event:sidefx-provider-resolution-requested
  @event-authority:resolve-sidefx-eligible-providers.v1
  @outcome:sidefx-semantic-provider-resolution
  @outcome-contract:sidefx-semantic-provider-resolution.v1
  @outcome-terminal
  Scenario: Admit only providers whose binding, conformance, and target are declared
    Given declared provider bindings, a requested platform capability, a requested target, and the admitted conformant dispositions
    When each binding is checked for capability match, admission, conformance evidence, and declared target
    Then eligible providers cite exact binding, profile, policy, authority, and conformance evidence and every other provider is NOT_OBSERVABLE, INELIGIBLE, or NOT_APPLICABLE with its reason
