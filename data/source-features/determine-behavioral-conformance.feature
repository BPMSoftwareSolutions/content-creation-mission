@capability:determine-behavioral-conformance
@root-scenario:determine-behavioral-conformance
# Legacy source: scenario-driven-architecture/tools/src/capabilities/kernel-implementation-admission/determine-behavioral-conformance/provider.ts
Feature: Determine behavioral conformance

  An SDA maintainer needs to know whether a language implementation's
  claimed semantics actually run, not merely whether they are declared. The
  capability evaluates the admitted real-toolchain observation collected for
  one language against the required fixture corpus.

  Every required fixture receives attributable behavior evidence or an
  explicit observation gap; the language corpus run is satisfied,
  unsatisfied, or not observable. The capability does not invoke the
  toolchain itself and does not admit the implementation — it only evaluates
  observations already collected.

  @scenario:determine-behavioral-conformance
  @input:behavioral-conformance-input
  @input-contract:behavioral-conformance-input.v1
  @event:behavioral-conformance-evaluation-requested
  @event-authority:behavioral-conformance-evaluation.v1
  @outcome:behavioral-conformance-known
  @outcome-contract:behavioral-conformance-evidence.v1
  @outcome-terminal
  Scenario: Evaluate the admitted real-toolchain observation for one language
    Given one admitted real-toolchain observation collected for one language
    When the admitted observation is evaluated against the required fixture corpus
    Then every required fixture has attributable behavior evidence or an explicit observation gap, and the language corpus run is satisfied, unsatisfied, or not observable
