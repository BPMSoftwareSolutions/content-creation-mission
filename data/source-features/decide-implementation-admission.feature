@capability:decide-implementation-admission
@root-scenario:decide-implementation-admission
# Legacy source: scenario-driven-architecture/tools/src/capabilities/kernel-implementation-admission/decide-implementation-admission/provider.ts
Feature: Decide implementation admission

  An SDA maintainer needs one final, honest admission verdict for a language
  implementation, derived from the complete evidence set produced by the
  other kernel-implementation-admission evaluators, with no failed or
  unobservable obligation hidden or silently dropped. The capability derives
  that verdict from one complete evidence set.

  Every required obligation participates exactly once in the verdict, and
  the verdict preserves the distinction between a failure and an
  unobservable gap. The capability does not re-evaluate authority, shape,
  execution, or behavioral conformance itself — it only composes their
  evidence into one explained verdict.

  @scenario:decide-implementation-admission
  @input:implementation-admission-input
  @input-contract:implementation-admission-input.v1
  @event:implementation-admission-decision-requested
  @event-authority:implementation-admission-decision.v1
  @outcome:implementation-admission-known
  @outcome-contract:implementation-admission-evidence.v1
  @outcome-terminal
  Scenario: Derive one explained admission verdict without hiding failed or unobservable obligations
    Given one complete evidence set covering every required implementation obligation
    When admission is derived from that evidence set without suppressing any failure or gap
    Then every required obligation participates exactly once in the verdict, and the verdict distinguishes a failed obligation from an unobservable one
