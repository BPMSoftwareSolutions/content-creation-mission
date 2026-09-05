@capability:read-authorized-file
@root-scenario:read-authorized-file
@lifecycle:REVISION_V2
Feature: Resolve every authorized-file read partition through one admitted provider boundary

  A caller supplies one digest-bound path beneath the provider-authorized root.
  The capability preserves the established exact-byte result and distinguishes
  an existing empty file, an absent file, and an attributable denied read.

  @scenario:read-authorized-file
  @input:authorized-file-read-request
  @input-contract:authorized-file-read-request.v1
  @event:read-authorized-file
  @event-authority:read-authorized-file.v2
  @outcome:authorized-file-read-outcome
  @outcome-contract:authorized-file-read-outcome.v2
  @outcome-variants:READ_ESTABLISHED|EMPTY_FILE_ESTABLISHED|FILE_NOT_FOUND|READ_DENIED
  @outcome-terminal
  Scenario: Resolve one authorized-file read into exactly one terminal partition
    Given one relative file reference and expected SHA-256 at the provider-authorized root boundary
    When the admitted bounded filesystem observation provider observes that exact path
    Then return exact bytes for a non-empty file, establish an existing empty file, report an absent file, or return attributable denial findings
