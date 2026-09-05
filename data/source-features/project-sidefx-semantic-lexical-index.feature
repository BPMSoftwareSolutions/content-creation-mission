@capability:project-sidefx-semantic-lexical-index
@root-scenario:project-sidefx-semantic-lexical-index
Feature: Project the deterministic lexical index from the closed corpus

  Lexical recall is the third retrieval channel and the weakest one. It may
  only propose candidates. This capability projects a rebuildable lexical index
  over the single allowed canonical text field of the admitted Wave 1 catalog,
  under a versioned profile that declares exactly what it can and cannot do:
  whole-field retention, substring containment over exact bytes, no case
  folding, no stemming, no scoring, and admitted catalog ordinal for order.
  The profile records its own limitations rather than implying capabilities the
  admitted transformation vocabulary does not provide.

  @scenario:project-sidefx-semantic-lexical-index
  @input:sidefx-semantic-lexical-index-projection-request
  @input-contract:sidefx-semantic-lexical-index-projection-request.v1
  @event:sidefx-semantic-lexical-index-projection-requested
  @event-authority:project-sidefx-semantic-lexical-index.v1
  @outcome:sidefx-semantic-lexical-index
  @outcome-contract:sidefx-semantic-lexical-index.v1
  @outcome-terminal
  Scenario: Project a profile-bound lexical index over the allowed text field
    Given the closed catalog subjects, the versioned lexical profile, and the declared snapshot and catalog digests
    When each allowed search representation is retained whole against its catalog ordinal and the index and receipt digests are derived
    Then one digest-bound lexical index carries recall material only and claims no score, rank, authority, or relationship
