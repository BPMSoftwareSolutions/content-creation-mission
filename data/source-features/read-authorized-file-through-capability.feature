@capability:read-authorized-file-through-capability
@root-scenario:read-authorized-file-through-capability
@lifecycle:FIRST_ADMISSION
Feature: Preserve every authorized-file outcome through one exact capability dependency

  A caller supplies one digest-bound relative path. The capability delegates that
  exact request to the published read-authorized-file capability, retains nested
  execution lineage, and returns the dependency outcome without reinterpretation.

  @scenario:read-authorized-file-through-capability
  @input:authorized-file-read-request
  @input-contract:authorized-file-read-request.v1
  @event:invoke-authorized-file-read-dependency
  @event-authority:invoke-authorized-file-read-dependency.v1
  @outcome:authorized-file-read-outcome
  @outcome-contract:authorized-file-read-outcome.v2
  @outcome-variants:READ_ESTABLISHED|EMPTY_FILE_ESTABLISHED|FILE_NOT_FOUND|READ_DENIED
  @outcome-terminal
  Scenario: Resolve one authorized-file read through the exact published dependency
    Given one relative file reference and expected SHA-256 accepted by the dependency input contract
    When the exact published read-authorized-file capability is invoked through its digest-bound projected binding
    Then return its non-empty, empty, missing, or denied outcome unchanged
    And retain attributable nested execution lineage for the dependency invocation
