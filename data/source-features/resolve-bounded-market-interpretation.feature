@capability:resolve-bounded-market-interpretation
@root-scenario:resolve-bounded-market-interpretation
Feature: Resolve one bounded market interpretation

  Market observes. Market intelligence interprets. Strategy governs.

  This capability owns the bounded statement step of the market
  evidence basis. Its input is one candidate interpretation bound to an
  established market pattern under the admitted interpretation profile.
  Its outcome is INTERPRETATION_ADMITTED or INTERPRETATION_HELD. An
  interpretation without an established pattern is held, the statement
  must stay inside the bounded statement form, forbidden claim terms
  such as prevalence, causality, market size, or buying intent are
  rejected, and limitations must be declared. Interpretations never
  select a strategy or offering.

  @scenario:resolve-bounded-market-interpretation
  @input:market-interpretation-record
  @input-contract:market-interpretation-record.v1
  @event:bounded-market-interpretation-resolution-requested
  @event-authority:resolve-bounded-market-interpretation.v1
  @outcome:market-interpretation-record
  @outcome-contract:market-interpretation-record.v1
  @outcome-terminal
  Scenario: Resolve one bounded market interpretation
    Given one candidate interpretation bound to one market pattern, one bounded statement, declared limitations, and the admitted interpretation profile
    When interpretation resolution is evaluated
    Then the interpretation is INTERPRETATION_ADMITTED or INTERPRETATION_HELD with the exact holding finding, and a receipt binds interpretation identity, pattern receipt, statement, and disposition

  @scenario:verify-pattern-binding
  @input:market-interpretation-record
  @input-contract:market-interpretation-record.v1
  @event:interpretation-pattern-binding-verification-requested
  @event-authority:verify-interpretation-pattern-binding.v1
  @outcome:market-interpretation-record
  @outcome-contract:market-interpretation-record.v1
  @outcome-terminal
  Scenario: Verify the interpretation pattern binding
    Given one pattern receipt digest and one pattern disposition
    When pattern binding verification is evaluated
    Then the pattern is established and its receipt is bound, reporting MARKET_PATTERN_NOT_ESTABLISHED otherwise

  @scenario:verify-bounded-statement
  @input:market-interpretation-record
  @input-contract:market-interpretation-record.v1
  @event:bounded-statement-verification-requested
  @event-authority:verify-bounded-statement.v1
  @outcome:market-interpretation-record
  @outcome-contract:market-interpretation-record.v1
  @outcome-terminal
  Scenario: Verify the bounded statement against the interpretation profile
    Given one bounded statement and the admitted interpretation profile
    When statement bound verification is evaluated
    Then the statement is present and contains no forbidden claim term, reporting INTERPRETATION_STATEMENT_ABSENT or FORBIDDEN_CLAIM_PRESENT otherwise

  @scenario:verify-interpretation-limitations
  @input:market-interpretation-record
  @input-contract:market-interpretation-record.v1
  @event:interpretation-limitations-verification-requested
  @event-authority:verify-interpretation-limitations.v1
  @outcome:market-interpretation-record
  @outcome-contract:market-interpretation-record.v1
  @outcome-terminal
  Scenario: Verify the interpretation limitations and profile admission
    Given one limitations statement and one interpretation profile identity
    When limitations and profile verification is evaluated
    Then the limitations are declared and the profile is the admitted market interpretation profile, reporting INTERPRETATION_LIMITATIONS_ABSENT or INTERPRETATION_PROFILE_UNADMITTED otherwise

  @scenario:bind-market-interpretation-receipt
  @input:market-interpretation-record
  @input-contract:market-interpretation-record.v1
  @event:market-interpretation-receipt-binding-requested
  @event-authority:bind-market-interpretation-receipt.v1
  @outcome:market-interpretation-record
  @outcome-contract:market-interpretation-record.v1
  @outcome-terminal
  Scenario: Bind one market interpretation receipt
    Given one interpretation disposition over one candidate interpretation
    When the interpretation receipt is bound
    Then the interpretation identity, pattern receipt digest, bounded statement, and disposition bind into one replayable market interpretation receipt
