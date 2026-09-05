@capability:observe-projected-target-execution
@root-scenario:observe-projected-target-execution
Feature: Observe projected capability execution on governed targets

  A downstream consumer supplies one lineage-bound projected capability,
  declared target fixture suites, and a governed target-execution authority.
  The consumer receives attributable execution observations for only the
  declared targets, commands, and fixtures. The capability does not decide
  admission, equivalence, verification, promotion, or repository policy.

  Target execution is an explicit governed effect responsibility. Pure
  transformations may resolve a bounded execution request, but they never
  fabricate projection receipts, command exits, fixture outcomes, or target
  dispositions. Missing projections, undeclared targets or fixtures, an
  authority mismatch, unavailable target runtime, and execution failure return
  attributable evidence without changing generated artifacts.

  @scenario:observe-projected-target-execution
  @input:projected-target-execution-request
  @input-contract:projected-target-execution-request.v1
  @event:observe-projected-target-execution
  @event-authority:observe-projected-target-execution.v1
  @outcome:projected-target-execution-request-delegated
  @outcome-contract:projected-target-execution-request.v1
  Scenario: Delegate one governed projected-target execution observation
    Given one declared projected capability, target execution authority, and bounded target fixture scope
    When a downstream consumer requests the declared target execution composition
    Then the unchanged request is delegated with its immutable lineage and no target execution fact is fabricated

  @scenario:resolve-governed-target-execution-scope
  @input:projected-target-execution-request
  @input-contract:projected-target-execution-request.v1
  @event:resolve-governed-target-execution-scope
  @event-authority:resolve-governed-target-execution-scope.v1
  @outcome:bounded-projected-target-execution-context
  @outcome-contract:bounded-projected-target-execution-context.v1
  Scenario: Resolve the exact authorized target execution scope
    Given one projected target-execution request with declared projection receipts, target identities, fixture references, and execution authority
    When the declared targets, fixture suites, projected application references, and immutable lineage are resolved
    Then one bounded target execution context identifies only authorized target work, or an attributable rejection is returned before target execution

  @scenario:observe-bounded-projected-target-execution
  @input:bounded-projected-target-execution-context
  @input-contract:bounded-projected-target-execution-context.v1
  @event:observe-bounded-projected-target-execution
  @event-authority:observe-bounded-projected-target-execution.v1
  @outcome:projected-target-execution-observation
  @outcome-contract:projected-target-execution-observation.v1
  @outcome-terminal
  Scenario: Return target fixture observations without editing projected output
    Given one bounded target execution context and one admitted target-execution effect capability
    When every declared target fixture suite is invoked in stable target and fixture identity order
    Then projection receipts, target command receipts, fixture results, target dispositions, generated-artifact-unchanged evidence, and complete effect lineage are returned without admission, equivalence, verification, promotion, or generated-artifact mutation
