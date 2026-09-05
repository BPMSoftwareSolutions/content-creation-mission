@capability:publish-implementation-evidence
@root-scenario:publish-implementation-evidence
# Legacy source: scenario-driven-architecture/tools/src/capabilities/conformance-evidence-publication/publish-implementation-evidence/provider.ts
Feature: Publish implementation evidence

  A release consumer needs one inspectable, current admission record for a
  language implementation, not a scattered set of intermediate evaluations.
  The capability constructs a versioned implementation evidence artifact
  from one coherent evidence set.

  The published artifact carries complete source, input, environment,
  disposition, timestamp, and digest lineage. The capability does not
  evaluate any conformance itself — it only publishes the already-produced
  evidence as one coherent, versioned artifact.

  @scenario:publish-implementation-evidence
  @input:implementation-evidence-publication-input
  @input-contract:implementation-evidence-publication-input.v1
  @event:implementation-evidence-publication-requested
  @event-authority:implementation-evidence-publication.v1
  @outcome:implementation-evidence-publication-known
  @outcome-contract:published-implementation-evidence.v1
  @outcome-terminal
  Scenario: Construct one versioned implementation evidence artifact from a coherent evidence set
    Given one coherent evidence set covering a language implementation
    When a versioned implementation evidence artifact is constructed from that evidence set
    Then the published artifact carries complete source, input, environment, disposition, time, and digest lineage
