@capability:verify-capability-scenario-outcomes
@root-scenario:verify-capability-scenario-outcomes
Feature: Verify one capability scenario corpus through the standard test harness

  Scenarios declare what must be proven. One reusable harness knows how to
  prove it. The standard SDA test harness consumes the admitted capability,
  its canonical execution graph, and its declared scenario verification
  vectors — test data, not generated test code — and proves every declared
  scenario outcome obligation or reports otherwise.

  A verification vector is the declared unit of proof: scenario identity,
  fixture input, expected disposition, and expected outcome. The universal
  algorithm never varies: resolve the scenario, admit the fixture input,
  execute the circuit, admit the observed outcome, evaluate declared
  assertions, verify the expected disposition, verify execution topology,
  verify monotonicity, and record testimony.

  Proof bindings must be declared or deterministically derived from
  canonical references, never inferred from proximity. A scenario that
  exists without a required vector is PROOF_BINDING_MISSING, never silently
  tested. Branches and recurrence are tested as declared vectors — required
  paths, not brute-force exploration. Every scenario admits and emits one
  shared verification record.

  @scenario:verify-capability-scenario-outcomes
  @input:capability-scenario-verification-record
  @input-contract:capability-scenario-verification-record.v1
  @event:capability-scenario-corpus-verification-requested
  @event-authority:verify-capability-scenario-outcomes.v1
  @outcome:capability-scenario-verification-record
  @outcome-contract:capability-scenario-verification-record.v1
  @outcome-terminal
  Scenario: Verify the declared scenario corpus against the standard harness law
    Given one admitted capability identity, its canonical graph digest, and its declared verification vectors
    When the corpus is verified through the universal algorithm
    Then every required scenario outcome is proven or explicitly reported otherwise, and the aggregate disposition is CAPABILITY_SCENARIO_CORPUS_CONFORMANT only when every scenario result passes and coverage closes

  @scenario:resolve-scenario-proof-bindings
  @input:capability-scenario-verification-record
  @input-contract:capability-scenario-verification-record.v1
  @event:scenario-proof-binding-resolution-requested
  @event-authority:resolve-scenario-proof-bindings.v1
  @outcome:capability-scenario-verification-record
  @outcome-contract:capability-scenario-verification-record.v1
  @outcome-terminal
  Scenario: Resolve every required scenario to its declared proof bindings
    Given one declared required-scenario list and the verification vectors
    When proof bindings are resolved
    Then every required scenario has at least one declared vector, and a scenario without one reports PROOF_BINDING_MISSING rather than silently counting as tested

  @scenario:verify-branch-and-recurrence-coverage
  @input:capability-scenario-verification-record
  @input-contract:capability-scenario-verification-record.v1
  @event:branch-and-recurrence-coverage-verification-requested
  @event-authority:verify-branch-and-recurrence-coverage.v1
  @outcome:capability-scenario-verification-record
  @outcome-contract:capability-scenario-verification-record.v1
  @outcome-terminal
  Scenario: Prove every declared branch and recurrence path is covered by a vector
    Given declared required verification paths for branches and recurrence profiles
    When coverage is evaluated against the declared vectors
    Then every required path has a matching vector, coverage is reported per declared path, and an uncovered path is a named finding

  @scenario:prove-integrated-circuit-conformance
  @input:capability-scenario-verification-record
  @input-contract:capability-scenario-verification-record.v1
  @event:integrated-circuit-conformance-proof-requested
  @event-authority:prove-integrated-circuit-conformance.v1
  @outcome:capability-scenario-verification-record
  @outcome-contract:capability-scenario-verification-record.v1
  @outcome-terminal
  Scenario: Prove every vector declares its admitted route through the root circuit
    Given the declared vectors with expected dispositions and routes
    When integrated circuit conformance is evaluated
    Then every vector declares an admitted path from the root, and a vector without one reports INTEGRATED_PATH_NOT_DECLARED — a scenario may pass locally while failing its transition, and both are required

  @scenario:aggregate-scenario-testimony
  @input:capability-scenario-verification-record
  @input-contract:capability-scenario-verification-record.v1
  @event:scenario-testimony-aggregation-requested
  @event-authority:aggregate-scenario-testimony.v1
  @outcome:capability-scenario-verification-record
  @outcome-contract:capability-scenario-verification-record.v1
  @outcome-terminal
  Scenario: Aggregate scenario results upward into one receipt
    Given completed per-scenario results and coverage dispositions
    When testimony is aggregated
    Then scenario coverage, vector execution, assertion evaluation, monotonicity, and the final disposition bind into one replayable receipt
