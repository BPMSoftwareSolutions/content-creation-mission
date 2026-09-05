@capability:resolve-capability-reinforcing-fit
@root-scenario:resolve-capability-reinforcing-fit
Feature: Resolve one capability reinforcing fit snapshot

  Execution testifies. Interpretation evaluates. Governance decides.

  This capability owns the capability-level aggregation of the
  meaning-return circuit. Its input is one capability identity with its
  declared intent and a set of admitted scenario fit signals. Its
  outcome is one capability fit snapshot with conservative dispositions:
  CAPABILITY_REINFORCED, CAPABILITY_NOT_REINFORCED,
  CAPABILITY_FIT_NOT_OBSERVABLE, or CAPABILITY_FIT_NOT_APPLICABLE. The
  snapshot is a signal, not a decision: it changes nothing, and a single
  unobservable or non-reinforcing signal keeps the whole capability from
  being declared reinforced.

  @scenario:resolve-capability-reinforcing-fit
  @input:capability-reinforcing-fit-record
  @input-contract:capability-reinforcing-fit-record.v1
  @event:capability-reinforcing-fit-resolution-requested
  @event-authority:resolve-capability-reinforcing-fit.v1
  @outcome:capability-reinforcing-fit-record
  @outcome-contract:capability-reinforcing-fit-record.v1
  @outcome-terminal
  Scenario: Resolve one capability reinforcing fit snapshot
    Given one capability identity, its declared intent, and a set of admitted scenario fit signals
    When the capability fit aggregate is resolved
    Then one capability fit snapshot is available with disposition CAPABILITY_REINFORCED, CAPABILITY_NOT_REINFORCED, CAPABILITY_FIT_NOT_OBSERVABLE, or CAPABILITY_FIT_NOT_APPLICABLE, and the snapshot changes nothing

  @scenario:admit-scenario-fit-signals
  @input:capability-reinforcing-fit-record
  @input-contract:capability-reinforcing-fit-record.v1
  @event:scenario-fit-signal-admission-requested
  @event-authority:admit-scenario-fit-signals.v1
  @outcome:capability-reinforcing-fit-record
  @outcome-contract:capability-reinforcing-fit-record.v1
  @outcome-terminal
  Scenario: Admit the scenario fit signals against the expected scenarios
    Given one set of scenario fit signals and one set of expected scenario identities
    When signal admission is evaluated
    Then every expected scenario is covered by an admitted signal, reporting SIGNAL_COVERAGE_INCOMPLETE otherwise

  @scenario:evaluate-capability-fit-aggregate
  @input:capability-reinforcing-fit-record
  @input-contract:capability-reinforcing-fit-record.v1
  @event:capability-fit-aggregate-evaluation-requested
  @event-authority:evaluate-capability-fit-aggregate.v1
  @outcome:capability-reinforcing-fit-record
  @outcome-contract:capability-reinforcing-fit-record.v1
  @outcome-terminal
  Scenario: Evaluate the capability fit aggregate over the admitted signals
    Given one set of admitted scenario fit signals bound to one capability identity
    When the aggregate is evaluated
    Then all reinforcing signals yield CAPABILITY_REINFORCED, any non-reinforcing signal yields CAPABILITY_NOT_REINFORCED, any unobservable signal yields CAPABILITY_FIT_NOT_OBSERVABLE, and any scope mismatch yields CAPABILITY_FIT_NOT_APPLICABLE

  @scenario:bind-capability-fit-snapshot
  @input:capability-reinforcing-fit-record
  @input-contract:capability-reinforcing-fit-record.v1
  @event:capability-fit-snapshot-binding-requested
  @event-authority:bind-capability-fit-snapshot.v1
  @outcome:capability-reinforcing-fit-record
  @outcome-contract:capability-reinforcing-fit-record.v1
  @outcome-terminal
  Scenario: Bind one capability fit snapshot
    Given one resolved capability fit snapshot with disposition and signal digests
    When the snapshot is bound
    Then the capability identity, every admitted fit signal digest, and the disposition bind into one replayable capability fit snapshot receipt
