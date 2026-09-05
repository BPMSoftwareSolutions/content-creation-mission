@capability:govern-authoring-convergence
@root-scenario:govern-authoring-convergence
Feature: Govern one authoring convergence round deterministically

  An authoring model proposes meaning. It must never be asked to decide what the
  machine already knows exactly. This capability owns everything mechanically
  decidable about a capability candidate, so probabilistic review never spends a
  token deciding whether an operator exists.

  Every rule here was derived from the admitted estate by the same method: observe a
  pattern, search for counterexamples, prove causality with a fixed baseline probe,
  and only then state the invariant. Prevalence alone is not law.

  The governing distinction is closure, not cardinality. Six required ports and six
  declared bindings prove nothing if the six identities do not resolve to each other.
  Coverage counts. Closure resolves.

  A round emits bounded findings, never a verdict of "try again". Each finding names
  the artifact, the authority pointer, the rule, what was observed, what was expected,
  and the constraint any repair must honour. Repair is therefore a narrowing problem
  rather than a regeneration problem, and admitted authority is preserved untouched.

  An invented operator is not a failure. It is REPAIRABLE. Only a session that cannot
  legitimately make another move is BLOCKED. Every scenario admits and emits one
  shared authoring convergence record.

  @scenario:govern-authoring-convergence
  @input:authoring-convergence-record
  @input-contract:authoring-convergence-record.v1
  @event:authoring-convergence-round-requested
  @event-authority:govern-authoring-convergence.v1
  @outcome:authoring-convergence-record
  @outcome-contract:authoring-convergence-record.v1
  @outcome-terminal
  Scenario: Govern one deterministic convergence round over a candidate
    Given one capability candidate, its declared scenario identities, and the round history already admitted
    When the convergence round is governed
    Then every deterministic conformance rule is evaluated, the findings bind into one normalized finding set, and the round disposition is ADVANCED, REPAIRABLE, or BLOCKED

  @scenario:evaluate-expression-operator-conformance
  @input:authoring-convergence-record
  @input-contract:authoring-convergence-record.v1
  @event:expression-operator-conformance-evaluation-requested
  @event-authority:evaluate-expression-operator-conformance.v1
  @outcome:authoring-convergence-record
  @outcome-contract:authoring-convergence-record.v1
  @outcome-terminal
  Scenario: Admit only declared operators carrying their declared operands
    Given the admitted operator vocabulary and the candidate semantic transformations
    When operator conformance is evaluated
    Then every expression node names an admitted operator and carries only that operator's declared operand keys, reporting UNKNOWN_OPERATOR or UNKNOWN_OPERAND_KEY with the offending authority pointer otherwise

  @scenario:evaluate-scenario-edge-realization
  @input:authoring-convergence-record
  @input-contract:authoring-convergence-record.v1
  @event:scenario-edge-realization-evaluation-requested
  @event-authority:evaluate-scenario-edge-realization.v1
  @outcome:authoring-convergence-record
  @outcome-contract:authoring-convergence-record.v1
  @outcome-terminal
  Scenario: Give one semantic edge exactly one realization
    Given the candidate execution authorities and its declared semantic graph transitions
    When edge realization is evaluated
    Then a capability composing scenarios through invoke-scenario declares no transitions and a capability declaring transitions composes no scenarios, reporting DUPLICATE_EDGE_REALIZATION otherwise

  @scenario:evaluate-port-binding-closure
  @input:authoring-convergence-record
  @input-contract:authoring-convergence-record.v1
  @event:port-binding-closure-evaluation-requested
  @event-authority:evaluate-port-binding-closure.v1
  @outcome:authoring-convergence-record
  @outcome-contract:authoring-convergence-record.v1
  @outcome-terminal
  Scenario: Resolve every required port identity to exactly one declared binding
    Given the candidate execution authorities and its declared port bindings
    When port binding closure is evaluated
    Then every invoke-port operation resolves to exactly one declared port binding, reporting UNBOUND_REQUIRED_PORT when none resolves and AMBIGUOUS_PORT_BINDING when more than one does, and equal counts never establish closure

  @scenario:evaluate-execution-authority-closure
  @input:authoring-convergence-record
  @input-contract:authoring-convergence-record.v1
  @event:execution-authority-closure-evaluation-requested
  @event-authority:evaluate-execution-authority-closure.v1
  @outcome:authoring-convergence-record
  @outcome-contract:authoring-convergence-record.v1
  @outcome-terminal
  Scenario: Resolve every declared scenario to exactly one execution authority
    Given the declared scenario identities and the candidate execution authorities
    When execution authority closure is evaluated
    Then every declared scenario resolves to exactly one owning execution authority, reporting SCENARIO_WITHOUT_EXECUTION_AUTHORITY or AMBIGUOUS_EXECUTION_AUTHORITY otherwise

  @scenario:evaluate-observed-sequence-closure
  @input:authoring-convergence-record
  @input-contract:authoring-convergence-record.v1
  @event:observed-sequence-closure-evaluation-requested
  @event-authority:evaluate-observed-sequence-closure.v1
  @outcome:authoring-convergence-record
  @outcome-contract:authoring-convergence-record.v1
  @outcome-terminal
  Scenario: Expect only the sequence the realization style can observe
    Given the candidate proof corpus and the realization style the capability declares
    When observed sequence closure is evaluated
    Then a capability composing through invoke-scenario expects its root scenario alone as the observed sequence and terminal scenario, reporting OBSERVED_SEQUENCE_NOT_CLOSED or TERMINAL_SCENARIO_NOT_CLOSED otherwise

  @scenario:evaluate-literal-discriminator-conformance
  @input:authoring-convergence-record
  @input-contract:authoring-convergence-record.v1
  @event:literal-discriminator-conformance-evaluation-requested
  @event-authority:evaluate-literal-discriminator-conformance.v1
  @outcome:authoring-convergence-record
  @outcome-contract:authoring-convergence-record.v1
  @outcome-terminal
  Scenario: Keep literal data opaque to expression interpretation
    Given the observed expression nodes carrying literal discriminator pointers
    When literal discriminator conformance is evaluated
    Then every data position beneath a literal carrying an expression-shaped discriminator reports UNESCAPED_EXPRESSION_DISCRIMINATOR_IN_LITERAL with the offending pointer, and literal data without an expression-shaped discriminator reports nothing

  @scenario:bind-normalized-authoring-findings
  @input:authoring-convergence-record
  @input-contract:authoring-convergence-record.v1
  @event:normalized-authoring-finding-binding-requested
  @event-authority:bind-normalized-authoring-findings.v1
  @outcome:authoring-convergence-record
  @outcome-contract:authoring-convergence-record.v1
  @outcome-terminal
  Scenario: Bind every finding into one bounded repair surface
    Given the findings each conformance evaluation produced
    When the findings are bound
    Then each finding records its rule identity, artifact, authority pointer, observed value, expected value, and repair constraint, and the repair surface names only the artifacts carrying findings

  @scenario:resolve-convergence-disposition
  @input:authoring-convergence-record
  @input-contract:authoring-convergence-record.v1
  @event:convergence-disposition-resolution-requested
  @event-authority:resolve-convergence-disposition.v1
  @outcome:authoring-convergence-record
  @outcome-contract:authoring-convergence-record.v1
  @outcome-terminal
  Scenario: Resolve the round disposition from admitted gate state alone
    Given the bound findings and the finding digest of the preceding round
    When the convergence disposition is resolved
    Then an empty finding set resolves ADVANCED, a narrowing actionable finding set resolves REPAIRABLE, and a finding set identical to the preceding round resolves BLOCKED with CONVERGENCE_NOT_NARROWING, so no orchestration may report advancement while any required gate holds a finding
