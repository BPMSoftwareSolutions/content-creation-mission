@capability:adapt-job-market-intelligence-evidence
@root-scenario:adapt-job-market-intelligence-evidence
Feature: Adapt one Job Market Intelligence evidence record

  Market observes. Market intelligence interprets. Strategy governs.

  This capability owns the typed entry point for Job Market
  Intelligence records into the SideFX market evidence plane. Its
  input is one JMI record reference, its admitted record type, its
  content digest, the adapter authority, and the observation window.
  Its outcome is ADAPTED_EVIDENCE_BINDING or ADAPTATION_HELD. The
  adapter binds the JMI identity and digest as a typed reference; it
  never copies untyped JSON into market evidence and never treats the
  referenced JMI content as admitted SideFX evidence by itself.

  @scenario:adapt-job-market-intelligence-evidence
  @input:job-market-intelligence-adapter-record
  @input-contract:job-market-intelligence-adapter-record.v1
  @event:job-market-intelligence-adaptation-requested
  @event-authority:adapt-job-market-intelligence-evidence.v1
  @outcome:job-market-intelligence-adapter-record
  @outcome-contract:job-market-intelligence-adapter-record.v1
  @outcome-terminal
  Scenario: Adapt one Job Market Intelligence evidence record
    Given one JMI record reference, one admitted JMI record type, one content digest, one adapter authority identity, and one observation window
    When the JMI evidence adaptation is evaluated
    Then the adaptation is ADAPTED_EVIDENCE_BINDING or ADAPTATION_HELD with the exact holding finding, and a receipt binds the JMI record reference, type, digest, and disposition

  @scenario:verify-jmi-record-binding
  @input:job-market-intelligence-adapter-record
  @input-contract:job-market-intelligence-adapter-record.v1
  @event:jmi-record-binding-verification-requested
  @event-authority:verify-jmi-record-binding.v1
  @outcome:job-market-intelligence-adapter-record
  @outcome-contract:job-market-intelligence-adapter-record.v1
  @outcome-terminal
  Scenario: Verify the JMI record binding
    Given one JMI record reference and one JMI content digest
    When record binding verification is evaluated
    Then the reference and the content digest are declared, reporting JMI_RECORD_UNBOUND otherwise

  @scenario:verify-jmi-type-admission
  @input:job-market-intelligence-adapter-record
  @input-contract:job-market-intelligence-adapter-record.v1
  @event:jmi-type-admission-verification-requested
  @event-authority:verify-jmi-type-admission.v1
  @outcome:job-market-intelligence-adapter-record
  @outcome-contract:job-market-intelligence-adapter-record.v1
  @outcome-terminal
  Scenario: Verify the JMI record type against the admitted adapter vocabulary
    Given one JMI record type and one adapter authority identity
    When type admission verification is evaluated
    Then the type is one of the admitted JMI record types under the adapter authority, reporting JMI_RECORD_TYPE_UNADMITTED or ADAPTER_AUTHORITY_UNADMITTED otherwise

  @scenario:bind-jmi-adapter-receipt
  @input:job-market-intelligence-adapter-record
  @input-contract:job-market-intelligence-adapter-record.v1
  @event:jmi-adapter-receipt-binding-requested
  @event-authority:bind-jmi-adapter-receipt.v1
  @outcome:job-market-intelligence-adapter-record
  @outcome-contract:job-market-intelligence-adapter-record.v1
  @outcome-terminal
  Scenario: Bind one JMI adapter receipt
    Given one adaptation disposition over one JMI record reference
    When the adapter receipt is bound
    Then the JMI record reference, record type, content digest, and disposition bind into one replayable JMI adapter receipt
