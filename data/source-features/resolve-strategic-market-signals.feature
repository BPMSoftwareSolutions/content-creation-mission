@capability:resolve-strategic-market-signals
@root-scenario:resolve-strategic-market-signals
Feature: Resolve one strategic market signal

  Market observes. Market intelligence interprets. Strategy governs.

  This capability owns signal derivation over admitted market facts.
  Its input is one candidate signal in one of the four first thesis
  signal families, bound to admitted market fact identities and
  declared source series. Its outcome is SIGNAL_ADMITTED or
  SIGNAL_HELD. Every signal retains its evidence fact identities and
  source series, declares its observation window and limitations, and
  cannot establish prevalence, causality, market size, or buying
  intent.

  @scenario:resolve-strategic-market-signals
  @input:market-signal-record
  @input-contract:market-signal-record.v1
  @event:strategic-market-signal-resolution-requested
  @event-authority:resolve-strategic-market-signals.v1
  @outcome:market-signal-record
  @outcome-contract:market-signal-record.v1
  @outcome-terminal
  Scenario: Resolve one strategic market signal
    Given one candidate market signal with evidence fact identities, signal family, source series, observation window, and limitations
    When signal resolution is evaluated
    Then the signal is SIGNAL_ADMITTED or SIGNAL_HELD with the exact holding finding, and a receipt binds signal identity, family, evidence facts, and disposition

  @scenario:verify-signal-fact-bindings
  @input:market-signal-record
  @input-contract:market-signal-record.v1
  @event:signal-fact-binding-verification-requested
  @event-authority:verify-signal-fact-bindings.v1
  @outcome:market-signal-record
  @outcome-contract:market-signal-record.v1
  @outcome-terminal
  Scenario: Verify the signal fact bindings
    Given one evidence fact identity list
    When fact binding verification is evaluated
    Then at least one admitted market fact identity is bound and every identity is declared, reporting MARKET_SIGNAL_LINEAGE_OPEN otherwise

  @scenario:verify-signal-family-admission
  @input:market-signal-record
  @input-contract:market-signal-record.v1
  @event:signal-family-admission-verification-requested
  @event-authority:verify-signal-family-admission.v1
  @outcome:market-signal-record
  @outcome-contract:market-signal-record.v1
  @outcome-terminal
  Scenario: Verify the signal family against the admitted signal vocabulary
    Given one signal family identifier and one admitted signal vocabulary identity
    When family admission is evaluated
    Then the family is one of the four first thesis families under the admitted signal vocabulary, reporting SIGNAL_FAMILY_UNADMITTED otherwise

  @scenario:verify-independence-and-window
  @input:market-signal-record
  @input-contract:market-signal-record.v1
  @event:signal-independence-window-verification-requested
  @event-authority:verify-independence-and-window.v1
  @outcome:market-signal-record
  @outcome-contract:market-signal-record.v1
  @outcome-terminal
  Scenario: Verify the declared source series, observation window, and limitations
    Given one source series list, one observation window, and one limitations statement
    When independence and window verification is evaluated
    Then at least one source series is declared, the observation window is declared, and the limitations are declared, reporting SOURCE_SERIES_UNDECLARED, OBSERVATION_WINDOW_ABSENT, or SIGNAL_LIMITATIONS_ABSENT otherwise

  @scenario:bind-market-signal-receipt
  @input:market-signal-record
  @input-contract:market-signal-record.v1
  @event:market-signal-receipt-binding-requested
  @event-authority:bind-market-signal-receipt.v1
  @outcome:market-signal-record
  @outcome-contract:market-signal-record.v1
  @outcome-terminal
  Scenario: Bind one market signal receipt
    Given one signal disposition over one candidate market signal
    When the signal receipt is bound
    Then the signal identity, signal family, evidence fact identities, and disposition bind into one replayable market signal receipt
