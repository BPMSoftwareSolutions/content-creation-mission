@capability:advance-sidefx-current-corpus-pointer
@root-scenario:advance-sidefx-current-corpus-pointer
Feature: Advance the current SideFX semantic corpus pointer strictly

  Pointer advancement is the one mutation in the architecture and carries
  the strictest authority boundary. The compare-and-swap receives the
  complete expected-current and authority-supplied proposed-next pointer
  states and pins both the expected generation and the expected snapshot
  digest. The store realizes compare plus atomic replace only; generation
  identity is never calculated by any store provider. Every scenario admits
  and emits one shared pointer advancement record.

  @scenario:advance-sidefx-current-corpus-pointer
  @input:sidefx-current-pointer-advancement-record
  @input-contract:sidefx-current-pointer-advancement-record.v1
  @event:sidefx-current-pointer-advancement-requested
  @event-authority:advance-sidefx-current-corpus-pointer.v1
  @outcome:sidefx-current-pointer-advancement-record
  @outcome-contract:sidefx-current-pointer-advancement-record.v1
  @outcome-terminal
  Scenario: Advance the pointer only when expected state matches exactly
    Given a closed snapshot candidate, the complete expected-current pointer state, and the authority-supplied proposed-next pointer state for one declared scope
    When the current corpus pointer is advanced
    Then exactly the proposed next generation is established or the observed winner is reported without mutation, and generation identity remains authority-owned

  @scenario:report-pointer-conflict-without-mutation
  @input:sidefx-current-pointer-advancement-record
  @input-contract:sidefx-current-pointer-advancement-record.v1
  @event:sidefx-current-pointer-conflict-observed
  @event-authority:report-sidefx-current-pointer-conflict.v1
  @outcome:sidefx-current-pointer-advancement-record
  @outcome-contract:sidefx-current-pointer-advancement-record.v1
  @outcome-terminal
  Scenario: Report the observed winner when expected state is stale
    Given an expected state that no longer matches the current pointer
    When the advance is attempted
    Then the observed winning generation and snapshot are reported and no state changes

  @scenario:refuse-open-pointer-advancement
  @input:sidefx-current-pointer-advancement-record
  @input-contract:sidefx-current-pointer-advancement-record.v1
  @event:open-sidefx-pointer-advancement-requested
  @event-authority:refuse-open-sidefx-pointer-advancement.v1
  @outcome:sidefx-current-pointer-advancement-record
  @outcome-contract:sidefx-current-pointer-advancement-record.v1
  @outcome-terminal
  Scenario: Refuse an advancement without a closed candidate snapshot
    Given a candidate that is missing, corrupted, open, rejected, or bound to a stale closure receipt
    When the pointer advancement is requested
    Then the current pointer is unchanged and every missing, stale, or rejected subject is returned as a named finding
