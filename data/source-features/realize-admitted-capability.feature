@capability:realize-admitted-capability
@root-scenario:realize-admitted-capability
Feature: Realize one admitted capability capsule for one environment

  Packaging preserves capability identity. Revelation exposes capability
  meaning. Realization binds capability meaning to an execution
  environment. Execution produces the effect.

  This capability owns realization. Its input is a verified capability
  capsule, an admitted target environment profile, and the available
  provider catalog. Its outcome is one conforming runnable realization —
  which may require zero code generation: verify the capsule, resolve the
  required providers, bind them to the declared graph, load the graph, and
  the capability is runnable in this environment.

  The realization test is never "did we produce an executable file." It
  is: can the realization admit scenario inputs, execute the declared
  graph, resolve required providers, establish declared outcomes, emit
  required testimony, pass its scenario corpus, and preserve canonical
  graph identity. Identity separates cleanly: the capability digest is
  always the same while the realization digest differs by environment.
  Every scenario admits and emits one shared realization record.

  @scenario:realize-admitted-capability
  @input:capability-realization-record
  @input-contract:capability-realization-record.v1
  @event:capability-realization-requested
  @event-authority:realize-admitted-capability.v1
  @outcome:capability-realization-record
  @outcome-contract:capability-realization-record.v1
  @outcome-terminal
  Scenario: Realize one capsule in one environment
    Given one verified capsule digest, one admitted environment profile, and the available provider catalog
    When the capability is realized
    Then one realization record binds the resolved providers, the bound graph, the preserved canonical identity, and the conformance disposition

  @scenario:resolve-required-providers
  @input:capability-realization-record
  @input-contract:capability-realization-record.v1
  @event:required-provider-resolution-requested
  @event-authority:resolve-required-providers.v1
  @outcome:capability-realization-record
  @outcome-contract:capability-realization-record.v1
  @outcome-terminal
  Scenario: Resolve every required provider against the available catalog
    Given the capsule's required providers and the available provider catalog for the declared target
    When providers are resolved
    Then every required provider resolves to an available admitted provider, and an unresolved provider reports PROVIDER_NOT_AVAILABLE

  @scenario:bind-providers-to-graph
  @input:capability-realization-record
  @input-contract:capability-realization-record.v1
  @event:provider-graph-binding-requested
  @event-authority:bind-providers-to-graph.v1
  @outcome:capability-realization-record
  @outcome-contract:capability-realization-record.v1
  @outcome-terminal
  Scenario: Bind every resolved provider to its declared graph slot
    Given the resolved providers and their declared slots
    When providers are bound
    Then every slot carries one binding digest, and a slot without a provider reports PROVIDER_SLOT_UNBOUND

  @scenario:preserve-canonical-graph-identity
  @input:capability-realization-record
  @input-contract:capability-realization-record.v1
  @event:canonical-graph-identity-preservation-requested
  @event-authority:preserve-canonical-graph-identity.v1
  @outcome:capability-realization-record
  @outcome-contract:capability-realization-record.v1
  @outcome-terminal
  Scenario: Prove the realization preserves canonical graph identity
    Given the capsule's canonical graph digest and the realized graph digest
    When identity preservation is evaluated
    Then the realized digest equals the canonical digest while the realization digest differs by environment, and a diverged canonical digest reports CANONICAL_IDENTITY_DIVERGED

  @scenario:prove-realization-conformant
  @input:capability-realization-record
  @input-contract:capability-realization-record.v1
  @event:realization-conformance-proof-requested
  @event-authority:prove-realization-conformant.v1
  @outcome:capability-realization-record
  @outcome-contract:capability-realization-record.v1
  @outcome-terminal
  Scenario: Prove the seven realization conformance dimensions
    Given the declared realization dimensions
    When conformance is evaluated
    Then input admission, graph execution, provider resolution, outcome establishment, testimony emission, scenario corpus passage, and canonical identity preservation are each reported, and the realization is CAPABILITY_REALIZATION_CONFORMANT only when every dimension passes
