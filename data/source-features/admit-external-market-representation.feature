@capability:admit-external-market-representation
@root-scenario:admit-external-market-representation
Feature: Admit one external market representation

  Market observes. Market intelligence interprets. Strategy governs.

  This capability owns the first step of the market evidence basis. Its
  input is one external source representation with source identity,
  representation type, captured time, content digest, acquisition
  authority, methodology, syndication declaration, licensing, and
  privacy dispositions. Its outcome is one admission disposition:
  ADMITTED_REPRESENTATION or ADMISSION_HELD. Source text is testimony
  until admitted: changed content produces a new representation
  identity, syndicated copies declare their parent series, use and
  privacy are disallowed only when declared so, and no source is
  presented as a market fact by this capability.

  @scenario:admit-external-market-representation
  @input:external-representation-receipt
  @input-contract:external-representation-receipt.v1
  @event:external-market-representation-admission-requested
  @event-authority:admit-external-market-representation.v1
  @outcome:external-representation-receipt
  @outcome-contract:external-representation-receipt.v1
  @outcome-terminal
  Scenario: Admit one external market representation
    Given one external source representation with identity, content digest, acquisition authority, methodology, syndication, licensing, and privacy declarations
    When representation admission is evaluated
    Then the representation is ADMITTED_REPRESENTATION or ADMISSION_HELD with the exact holding finding, and a receipt binds source identity, representation type, captured time, content digest, and disposition

  @scenario:verify-source-identity
  @input:external-representation-receipt
  @input-contract:external-representation-receipt.v1
  @event:source-identity-verification-requested
  @event-authority:verify-source-identity.v1
  @outcome:external-representation-receipt
  @outcome-contract:external-representation-receipt.v1
  @outcome-terminal
  Scenario: Verify the source identity and content addressing
    Given one source identity, one representation type, one captured time, and one content digest
    When source identity verification is evaluated
    Then the identity is complete and the content digest is bound, reporting SOURCE_IDENTITY_INCOMPLETE or SOURCE_REPRESENTATION_UNADMITTED otherwise

  @scenario:verify-methodology-provenance
  @input:external-representation-receipt
  @input-contract:external-representation-receipt.v1
  @event:methodology-provenance-verification-requested
  @event-authority:verify-methodology-provenance.v1
  @outcome:external-representation-receipt
  @outcome-contract:external-representation-receipt.v1
  @outcome-terminal
  Scenario: Verify the methodology provenance and acquisition authority
    Given one methodology with population, geography, observation window, and sample disposition, and one acquisition authority identity
    When methodology provenance verification is evaluated
    Then the methodology is complete and the acquisition authority is the admitted market source admission authority, reporting SOURCE_METHODOLOGY_ABSENT or SOURCE_ACQUISITION_UNADMITTED otherwise

  @scenario:verify-duplication-syndication-and-use
  @input:external-representation-receipt
  @input-contract:external-representation-receipt.v1
  @event:duplication-syndication-use-verification-requested
  @event-authority:verify-duplication-syndication-and-use.v1
  @outcome:external-representation-receipt
  @outcome-contract:external-representation-receipt.v1
  @outcome-terminal
  Scenario: Verify duplication, syndication, licensing, and privacy declarations
    Given one syndication declaration, one licensing disposition, and one privacy disposition
    When duplication syndication and use verification is evaluated
    Then a syndicated source declares its parent series, and disallowed use or privacy holds admission, reporting SOURCE_SERIES_DUPLICATED, SOURCE_USE_DISALLOWED, or SOURCE_PRIVACY_DISALLOWED otherwise

  @scenario:bind-representation-receipt
  @input:external-representation-receipt
  @input-contract:external-representation-receipt.v1
  @event:representation-receipt-binding-requested
  @event-authority:bind-representation-receipt.v1
  @outcome:external-representation-receipt
  @outcome-contract:external-representation-receipt.v1
  @outcome-terminal
  Scenario: Bind one representation receipt
    Given one admission disposition over one source representation
    When the representation receipt is bound
    Then the source identity, representation type, captured time, content digest, and disposition bind into one replayable representation receipt
