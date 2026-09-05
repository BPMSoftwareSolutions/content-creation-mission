@capability:observe-language-behavior
@root-scenario:observe-language-behavior
# Legacy source: scenario-driven-architecture/tools/src/capabilities/conformance-evidence-publication/observe-language-behavior/provider.ts
Feature: Observe language behavior

  An SDA maintainer needs every language's real test suite invoked and its
  results captured attributably, so a failing implementation can never be
  confused with a missing toolchain. The capability invokes the real
  language suite and captures attributable results for each targeted
  language.

  Every targeted language produces evidence or an explicit NOT_OBSERVABLE
  reason, and each observation distinguishes implementation failure from
  environment absence. The capability does not evaluate conformance itself
  — it only produces the attributable observation later evaluation depends
  on.

  @scenario:observe-language-behavior
  @input:language-behavior-observation-input
  @input-contract:language-behavior-observation-input.v1
  @event:language-behavior-observation-requested
  @event-authority:language-behavior-observation.v1
  @outcome:language-behavior-observation-known
  @outcome-contract:language-behavior-observation-evidence.v1
  @outcome-terminal
  Scenario: Invoke the real language suite and capture attributable results
    Given one targeted language and its real test suite
    When the real language suite is invoked and its results are captured attributably
    Then every targeted language produces evidence or an explicit NOT_OBSERVABLE reason that distinguishes implementation failure from environment absence
