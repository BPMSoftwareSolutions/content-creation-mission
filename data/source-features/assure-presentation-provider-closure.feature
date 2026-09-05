@capability:assure-presentation-provider-closure
@root-scenario:assure-presentation-provider-closure
Feature: Assure complete presentation provider closure

  # Original hand-authored source references (migration oracles only):
  # scenario-driven-architecture/tools/src/interfaces/ui-parity/evaluate.ts :: UI parity closure evaluation
  # scenario-driven-architecture/tools/src/consumer-projection/proof/mechanical-sterility-evaluator.ts :: evaluateMechanicalSterility
  # scenario-driven-architecture/languages/csharp/src/ScenarioKernel.Wpf/UiStructuralContract.cs :: UiStructuralContract.Emit

  Provider closure requires one admitted semantic source, database round-trip
  identity, clean regeneration, projected-only executable origin, complete
  native proof, exact oracle equivalence, active binding cutover, and absence of
  handwritten or target-specific migration mechanics from the active path.

  @scenario:assure-presentation-provider-closure
  @input:presentation-provider-closure-facts
  @input-contract:assure-presentation-provider-closure-input.v1
  @event:presentation-provider-closure-assurance-requested
  @event-authority:presentation-provider-closure-assurance.v1
  @outcome:presentation-provider-closure-known
  @outcome-contract:presentation-provider-closure-evidence.v1
  @outcome-terminal
  Scenario: Decide whether a semantic presentation provider completely replaces its oracle
    Given admitted semantic authority, database round-trip evidence, regeneration evidence, projection lineage, native testimony, oracle comparison, binding evidence, and active dependency evidence
    When presentation provider closure is assured
    Then closure is proven only when every requirement passes and no handwritten provider or target-specific migration executable remains active
