@capability:determine-projected-shape-equivalence
@root-scenario:determine-projected-shape-equivalence
# Legacy source: scenario-driven-architecture/tools/src/capabilities/structural-model-projection/determine-projected-shape-equivalence/provider.ts
Feature: Determine projected shape equivalence

  A language maintainer needs to see exactly where generated and admitted
  structure differ, independently of file layout. The capability compares
  semantic member shape between the projection plan and the admitted
  implementation.

  Every canonical type present in either the plan or the admitted source
  has an explicit MATCH, MISMATCH, HAND_WRITTEN_ONLY, or GENERATED_ONLY
  disposition. The capability does not regenerate or repair anything — it
  only makes shape drift visible.

  @scenario:determine-projected-shape-equivalence
  @input:determine-shape-equivalence-input
  @input-contract:determine-shape-equivalence-input.v1
  @event:projected-shape-equivalence-evaluation-requested
  @event-authority:projected-shape-equivalence-evaluation.v1
  @outcome:projected-shape-equivalence-known
  @outcome-contract:projected-shape-evidence.v1
  @outcome-terminal
  Scenario: Compare projected and admitted structural shape independently of file layout
    Given one target projection plan and one admitted implementation
    When semantic member shape is compared between the projection plan and the admitted implementation, independently of file layout
    Then every type name present in either side has an explicit MATCH, MISMATCH, HAND_WRITTEN_ONLY, or GENERATED_ONLY disposition
