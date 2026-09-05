@capability:resolve-strategic-market-fit
@root-scenario:resolve-strategic-market-fit
Feature: Resolve one strategic market fit

  Market observes. Market intelligence interprets. Strategy governs.

  This capability owns the outside-in conclusion over admitted market
  interpretations. Its input is one set of admitted interpretation
  records, the exact strategic intent identity, market thesis identity,
  mapping authority, fit profile, evaluation window, and evidence
  cutoff. Its outcome separates evaluation from meaning:
  MARKET_FIT_EVALUATED or MARKET_FIT_EVALUATION_HELD, with
  marketFitDisposition MARKET_REINFORCES_INTENT,
  MARKET_DOES_NOT_REINFORCE_INTENT, MARKET_NOT_OBSERVABLE, or
  MARKET_NOT_APPLICABLE only when evaluated. Identity divergence holds
  evaluation; counterevidence defeats reinforcement while remaining
  retained; missing coverage remains not observable. No fit record
  authors or mutates strategy.

  @scenario:resolve-strategic-market-fit
  @input:strategic-market-fit-record
  @input-contract:strategic-market-fit-record.v1
  @event:strategic-market-fit-resolution-requested
  @event-authority:resolve-strategic-market-fit.v1
  @outcome:strategic-market-fit-record
  @outcome-contract:strategic-market-fit-record.v1
  @outcome-terminal
  Scenario: Resolve one strategic market fit
    Given one interpretation set, the exact strategic intent identity, thesis identity, mapping authority, fit profile, evaluation window, and evidence cutoff
    When strategic market fit is resolved
    Then the evaluation is MARKET_FIT_EVALUATED or MARKET_FIT_EVALUATION_HELD, and an evaluated fit carries exactly one conservative marketFitDisposition with a reproducible receipt

  @scenario:verify-fit-identity-binding
  @input:strategic-market-fit-record
  @input-contract:strategic-market-fit-record.v1
  @event:fit-identity-binding-verification-requested
  @event-authority:verify-fit-identity-binding.v1
  @outcome:strategic-market-fit-record
  @outcome-contract:strategic-market-fit-record.v1
  @outcome-terminal
  Scenario: Verify the strategic intent, thesis, mapping, and profile identities
    Given one strategic intent identity, one market thesis identity, one mapping identity, and one fit profile identity
    When identity binding verification is evaluated
    Then every identity matches its admitted digest-bound authority, reporting STRATEGIC_INTENT_IDENTITY_DIVERGED, MARKET_THESIS_UNADMITTED, STRATEGIC_MARKET_MAPPING_DIVERGED, or FIT_PROFILE_UNADMITTED otherwise

  @scenario:verify-fit-coverage-and-window
  @input:strategic-market-fit-record
  @input-contract:strategic-market-fit-record.v1
  @event:fit-coverage-window-verification-requested
  @event-authority:verify-fit-coverage-and-window.v1
  @outcome:strategic-market-fit-record
  @outcome-contract:strategic-market-fit-record.v1
  @outcome-terminal
  Scenario: Verify the expected family coverage, evaluation window, and evidence cutoff
    Given one interpretation set, one evaluation window, and one evidence cutoff
    When coverage and window verification is evaluated
    Then every expected family is covered by an admitted interpretation and the window and cutoff are declared, reporting EXPECTED_SIGNAL_FAMILY_ABSENT or EVALUATION_WINDOW_ABSENT otherwise

  @scenario:verify-fit-counterevidence-and-duplication
  @input:strategic-market-fit-record
  @input-contract:strategic-market-fit-record.v1
  @event:fit-counterevidence-duplication-verification-requested
  @event-authority:verify-fit-counterevidence-and-duplication.v1
  @outcome:strategic-market-fit-record
  @outcome-contract:strategic-market-fit-record.v1
  @outcome-terminal
  Scenario: Verify counterevidence retention and interpretation uniqueness
    Given one contradicting signal set and one interpretation set
    When counterevidence and duplication verification is evaluated
    Then counterevidence defeats reinforcement while remaining retained, and a duplicated interpretation receipt holds evaluation, reporting COUNTEREVIDENCE_PRESENT or DUPLICATE_INTERPRETATION_PRESENT otherwise

  @scenario:bind-strategic-market-fit-receipt
  @input:strategic-market-fit-record
  @input-contract:strategic-market-fit-record.v1
  @event:strategic-market-fit-receipt-binding-requested
  @event-authority:bind-strategic-market-fit-receipt.v1
  @outcome:strategic-market-fit-record
  @outcome-contract:strategic-market-fit-record.v1
  @outcome-terminal
  Scenario: Bind one strategic market fit receipt
    Given one evaluation disposition and one fit disposition over one interpretation set
    When the fit receipt is bound
    Then the thesis identity, intent digest, mapping identity, interpretation receipts, and dispositions bind into one replayable strategic market fit receipt
