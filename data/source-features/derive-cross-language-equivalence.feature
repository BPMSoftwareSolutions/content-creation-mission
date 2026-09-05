@capability:derive-cross-language-equivalence
@root-scenario:derive-cross-language-equivalence
# Legacy source: scenario-driven-architecture/tools/src/capabilities/conformance-evidence-publication/derive-cross-language-equivalence/provider.ts
Feature: Derive cross-language equivalence

  A release consumer needs to know exactly where different language
  embodiments of the same capability agree or diverge, fixture by fixture.
  The capability compares each canonical fixture disposition across
  languages.

  Every shared fixture has an explicit per-language equivalence result, and
  the resulting matrix contains every fixture and every targeted language.
  The capability does not run any fixture itself — it only compares
  dispositions already observed.

  @scenario:derive-cross-language-equivalence
  @input:cross-language-equivalence-input
  @input-contract:cross-language-equivalence-input.v1
  @event:cross-language-equivalence-derivation-requested
  @event-authority:cross-language-equivalence-derivation.v1
  @outcome:cross-language-equivalence-known
  @outcome-contract:cross-language-equivalence-evidence.v1
  @outcome-terminal
  Scenario: Compare each canonical fixture disposition across languages
    Given one set of canonical fixture dispositions observed across languages
    When each canonical fixture disposition is compared across languages
    Then every shared fixture has an explicit per-language equivalence result and the equivalence matrix contains every fixture and targeted language
