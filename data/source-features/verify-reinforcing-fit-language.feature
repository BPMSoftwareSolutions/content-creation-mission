@capability:verify-reinforcing-fit-language
@root-scenario:verify-reinforcing-fit-language
Feature: Verify one reinforcing fit statement stays inside its semantic altitude

  Evidence may be technical. Reinforcing meaning must resolve into the
  vocabulary of the semantic altitude consuming it.

  This capability owns the semantic altitude law for reinforcing fit
  statements. Its input is one resolved fit signal with its domain
  statement, its consuming altitude, and the domain vocabulary
  authority that governs it. Its outcome is one language conformance
  disposition: SEMANTIC_ALTITUDE_CONFORMANT, LANGUAGE_LEAKAGE, or
  NOT_OBSERVABLE. Technical terms such as http, sql, kafka, json,
  class, function, adapter, serializer, pod, and container are rejected
  unless they are part of the governed vocabulary at the consuming
  altitude. The statement is never rewritten: leakage is reported, and
  remediation belongs to the declaring authority.

  @scenario:verify-reinforcing-fit-language
  @input:reinforcing-fit-language-record
  @input-contract:reinforcing-fit-language-record.v1
  @event:reinforcing-fit-language-verification-requested
  @event-authority:verify-reinforcing-fit-language.v1
  @outcome:reinforcing-fit-language-record
  @outcome-contract:reinforcing-fit-language-record.v1
  @outcome-terminal
  Scenario: Verify one reinforcing fit statement stays inside its semantic altitude
    Given one resolved fit signal with domain statement, consuming altitude, and domain vocabulary authority
    When language conformance is evaluated
    Then the statement is SEMANTIC_ALTITUDE_CONFORMANT or reports LANGUAGE_LEAKAGE with the exact leaked terms, and the statement is never rewritten

  @scenario:admit-fit-signal-evidence
  @input:reinforcing-fit-language-record
  @input-contract:reinforcing-fit-language-record.v1
  @event:fit-signal-evidence-admission-requested
  @event-authority:admit-fit-signal-evidence.v1
  @outcome:reinforcing-fit-language-record
  @outcome-contract:reinforcing-fit-language-record.v1
  @outcome-terminal
  Scenario: Admit the fit signal evidence
    Given one fit signal digest and one domain statement
    When signal evidence admission is evaluated
    Then the signal digest and the domain statement are present, reporting SIGNAL_NOT_BOUND or DOMAIN_STATEMENT_ABSENT otherwise

  @scenario:evaluate-altitude-vocabulary-binding
  @input:reinforcing-fit-language-record
  @input-contract:reinforcing-fit-language-record.v1
  @event:altitude-vocabulary-binding-evaluation-requested
  @event-authority:evaluate-altitude-vocabulary-binding.v1
  @outcome:reinforcing-fit-language-record
  @outcome-contract:reinforcing-fit-language-record.v1
  @outcome-terminal
  Scenario: Evaluate the altitude and vocabulary binding
    Given one consuming altitude and one domain vocabulary authority identity
    When altitude vocabulary binding is evaluated
    Then the vocabulary authority is the admitted domain vocabulary and the consuming altitude is a meaning altitude, reporting VOCABULARY_NOT_ADMITTED or ALTITUDE_NOT_COVERED otherwise

  @scenario:scan-forbidden-terminology
  @input:reinforcing-fit-language-record
  @input-contract:reinforcing-fit-language-record.v1
  @event:forbidden-terminology-scan-requested
  @event-authority:scan-forbidden-terminology.v1
  @outcome:reinforcing-fit-language-record
  @outcome-contract:reinforcing-fit-language-record.v1
  @outcome-terminal
  Scenario: Scan the domain statement for forbidden technical terminology
    Given one domain statement and the forbidden technical term list of the domain vocabulary
    When the statement is scanned
    Then no forbidden technical term appears in the statement, and every leaked term is reported exactly

  @scenario:bind-language-conformance-receipt
  @input:reinforcing-fit-language-record
  @input-contract:reinforcing-fit-language-record.v1
  @event:language-conformance-receipt-binding-requested
  @event-authority:bind-language-conformance-receipt.v1
  @outcome:reinforcing-fit-language-record
  @outcome-contract:reinforcing-fit-language-record.v1
  @outcome-terminal
  Scenario: Bind one language conformance receipt
    Given one language conformance disposition over one fit signal
    When the conformance receipt is bound
    Then the fit signal digest, vocabulary authority identity, consuming altitude, domain statement, and disposition bind into one replayable language conformance receipt
