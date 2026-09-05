@capability:verify-governed-placement
@root-scenario:verify-governed-placement
# Legacy source: scenario-driven-architecture/tools/src/capabilities/workspace-governance/verify-governed-placement/provider.ts
Feature: Verify governed placement

  An SDA maintainer needs to trust that canonical fixtures, expectations,
  and language claims remain on their governed side of the workspace, and
  that every fixture-to-expectation reference actually resolves. The
  capability evaluates governed document placement and
  fixture-to-expectation reference integrity.

  Every governed document is correctly placed and paired, or carries an
  explicit finding naming the violation. The capability does not move or
  repair anything — it only makes placement and reference violations
  visible.

  @scenario:verify-governed-placement
  @input:governed-placement-input
  @input-contract:governed-placement-input.v1
  @event:governed-placement-verification-requested
  @event-authority:governed-placement-verification.v1
  @outcome:governed-placement-conformance-known
  @outcome-contract:governed-placement-evidence.v1
  @outcome-terminal
  Scenario: Evaluate governed document placement and fixture-to-expectation reference integrity
    Given one workspace containing governed fixtures, expectations, and language claims
    When governed document placement and fixture-to-expectation reference integrity are evaluated
    Then every governed document is correctly placed and paired or carries an explicit finding, and every reference either resolves or is named as broken
