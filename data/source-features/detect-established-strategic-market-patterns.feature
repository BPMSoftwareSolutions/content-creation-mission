@capability:detect-established-strategic-market-patterns
@root-scenario:detect-established-strategic-market-patterns
Feature: Detect one established strategic market pattern

  Market observes. Market intelligence interprets. Strategy governs.

  This capability owns longitudinal and independence-aware pattern
  detection. Its input is one candidate pattern over admitted market
  signals: expected signal families, supporting and contradicting
  signal receipts, independence groups, and observation windows. Its
  outcome is PATTERN_ESTABLISHED or PATTERN_NOT_ESTABLISHED. A single
  window is never established, coverage of every expected family is
  required, independence groups must represent distinct source series,
  duplicated signals are rejected, and contradicting evidence is
  retained alongside supporting evidence.

  @scenario:detect-established-strategic-market-patterns
  @input:market-pattern-record
  @input-contract:market-pattern-record.v1
  @event:strategic-market-pattern-detection-requested
  @event-authority:detect-established-strategic-market-patterns.v1
  @outcome:market-pattern-record
  @outcome-contract:market-pattern-record.v1
  @outcome-terminal
  Scenario: Detect one established strategic market pattern
    Given one candidate pattern with expected families, supporting and contradicting signals, independence groups, and windows
    When pattern detection is evaluated
    Then the pattern is PATTERN_ESTABLISHED or PATTERN_NOT_ESTABLISHED with the exact holding finding, and a receipt binds pattern identity, profile, signal identities, and disposition

  @scenario:verify-pattern-coverage
  @input:market-pattern-record
  @input-contract:market-pattern-record.v1
  @event:pattern-coverage-verification-requested
  @event-authority:verify-pattern-coverage.v1
  @outcome:market-pattern-record
  @outcome-contract:market-pattern-record.v1
  @outcome-terminal
  Scenario: Verify the expected family coverage
    Given one expected signal family set and one supporting signal set
    When coverage verification is evaluated
    Then every expected family is covered by an admitted supporting signal, reporting EXPECTED_SIGNAL_FAMILY_ABSENT otherwise

  @scenario:verify-pattern-independence
  @input:market-pattern-record
  @input-contract:market-pattern-record.v1
  @event:pattern-independence-verification-requested
  @event-authority:verify-pattern-independence.v1
  @outcome:market-pattern-record
  @outcome-contract:market-pattern-record.v1
  @outcome-terminal
  Scenario: Verify the independence groups and signal uniqueness
    Given one independence group set and one supporting signal set
    When independence verification is evaluated
    Then at least two distinct source series groups are declared and no signal receipt is duplicated, reporting INDEPENDENCE_GROUPS_UNDECLARED or SIGNAL_DUPLICATED otherwise

  @scenario:verify-pattern-temporality-and-contradiction
  @input:market-pattern-record
  @input-contract:market-pattern-record.v1
  @event:pattern-temporality-contradiction-verification-requested
  @event-authority:verify-pattern-temporality-and-contradiction.v1
  @outcome:market-pattern-record
  @outcome-contract:market-pattern-record.v1
  @outcome-terminal
  Scenario: Verify the temporal windows and retained contradiction
    Given one supporting signal set with observation windows and one contradicting signal set
    When temporality and contradiction verification is evaluated
    Then at least two distinct windows corroborate, and any contradicting signal defeats establishment while remaining retained, reporting SINGLE_WINDOW_NOT_ESTABLISHED or COUNTEREVIDENCE_PRESENT otherwise

  @scenario:bind-market-pattern-receipt
  @input:market-pattern-record
  @input-contract:market-pattern-record.v1
  @event:market-pattern-receipt-binding-requested
  @event-authority:bind-market-pattern-receipt.v1
  @outcome:market-pattern-record
  @outcome-contract:market-pattern-record.v1
  @outcome-terminal
  Scenario: Bind one market pattern receipt
    Given one pattern disposition over one candidate market pattern
    When the pattern receipt is bound
    Then the pattern identity, supporting and contradicting signal identities, and disposition bind into one replayable market pattern receipt
