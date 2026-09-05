@capability:determine-shape-conformance
@root-scenario:determine-shape-conformance
# Legacy source: scenario-driven-architecture/tools/src/capabilities/kernel-implementation-admission/determine-shape-conformance/provider.ts
Feature: Determine shape conformance

  An SDA maintainer needs to see exactly which canonical semantic objects a
  language implementation actually embodies, and which it is missing or has
  mismatched. The capability compares declared embodiments with every
  required semantic object.

  Every canonical semantic object receives an explicit shape disposition:
  present, mismatched, or explicitly missing; none disappears silently. The
  capability does not admit the implementation — it only makes every shape
  gap visible.

  @scenario:determine-shape-conformance
  @input:shape-conformance-input
  @input-contract:shape-conformance-input.v1
  @event:shape-conformance-evaluation-requested
  @event-authority:shape-conformance-evaluation.v1
  @outcome:shape-conformance-known
  @outcome-contract:shape-conformance-evidence.v1
  @outcome-terminal
  Scenario: Compare declared embodiments against every required canonical semantic object
    Given one set of declared embodiments and the required canonical semantic objects
    When declared embodiments are compared with every required semantic object
    Then every canonical semantic object has an explicit present, mismatched, or missing disposition, without an implementation admission decision being made
