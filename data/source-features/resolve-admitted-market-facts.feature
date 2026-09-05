@capability:resolve-admitted-market-facts
@root-scenario:resolve-admitted-market-facts
Feature: Resolve one admitted market fact

  Market observes. Market intelligence interprets. Strategy governs.

  This capability owns the second step of the market evidence basis.
  Its input is one candidate market fact bound to one admitted external
  representation receipt and one fact type from the admitted market fact
  vocabulary. Its outcome is FACT_ADMITTED or FACT_HELD. No source text
  is a fact without deterministic admission: the lineage must traverse
  to an admitted representation, the fact type must be admitted, the
  provenance must be complete, and no forbidden inference predicate may
  appear. Facts never claim prevalence, causality, market size, or
  buying intent.

  @scenario:resolve-admitted-market-facts
  @input:market-fact-record
  @input-contract:market-fact-record.v1
  @event:market-fact-resolution-requested
  @event-authority:resolve-admitted-market-facts.v1
  @outcome:market-fact-record
  @outcome-contract:market-fact-record.v1
  @outcome-terminal
  Scenario: Resolve one admitted market fact
    Given one candidate market fact with representation lineage, fact type, provenance, and bounded predicate
    When fact resolution is evaluated
    Then the fact is FACT_ADMITTED or FACT_HELD with the exact holding finding, and a receipt binds fact identity, type, evidence reference, and disposition

  @scenario:verify-fact-lineage
  @input:market-fact-record
  @input-contract:market-fact-record.v1
  @event:fact-lineage-verification-requested
  @event-authority:verify-fact-lineage.v1
  @outcome:market-fact-record
  @outcome-contract:market-fact-record.v1
  @outcome-terminal
  Scenario: Verify the fact lineage against an admitted representation
    Given one representation receipt digest and one representation admission disposition
    When fact lineage verification is evaluated
    Then the representation is admitted and bound, reporting MARKET_FACT_LINEAGE_OPEN otherwise

  @scenario:verify-fact-type-admission
  @input:market-fact-record
  @input-contract:market-fact-record.v1
  @event:fact-type-admission-verification-requested
  @event-authority:verify-fact-type-admission.v1
  @outcome:market-fact-record
  @outcome-contract:market-fact-record.v1
  @outcome-terminal
  Scenario: Verify the fact type against the admitted market fact vocabulary
    Given one fact type identifier and one admitted market fact vocabulary identity
    When fact type admission is evaluated
    Then the fact type is admitted by the market fact vocabulary, reporting FACT_TYPE_UNADMITTED otherwise

  @scenario:verify-fact-provenance-and-bounds
  @input:market-fact-record
  @input-contract:market-fact-record.v1
  @event:fact-provenance-bounds-verification-requested
  @event-authority:verify-fact-provenance-and-bounds.v1
  @outcome:market-fact-record
  @outcome-contract:market-fact-record.v1
  @outcome-terminal
  Scenario: Verify the fact provenance and bounded predicate
    Given one population, geography, observation window, and bounded predicate statement
    When provenance and bounds verification is evaluated
    Then the provenance is complete and the bounded predicate contains no forbidden inference term, reporting FACT_PROVENANCE_INCOMPLETE or FORBIDDEN_INFERENCE_PRESENT otherwise

  @scenario:bind-market-fact-receipt
  @input:market-fact-record
  @input-contract:market-fact-record.v1
  @event:market-fact-receipt-binding-requested
  @event-authority:bind-market-fact-receipt.v1
  @outcome:market-fact-record
  @outcome-contract:market-fact-record.v1
  @outcome-terminal
  Scenario: Bind one market fact receipt
    Given one fact disposition over one candidate market fact
    When the fact receipt is bound
    Then the fact identity, fact type, representation receipt digest, and disposition bind into one replayable market fact receipt
