@capability:project-sidefx-semantic-identity-index
@root-scenario:project-sidefx-semantic-identity-index
Feature: Project the exact semantic identity index from the closed corpus

  Wave 2 deterministic retrieval begins with exact canonical identity. This
  capability projects a rebuildable identity index over the admitted Wave 1
  object catalog, binding every entry to its immutable snapshot, its catalog
  digest, and its catalog ordinal. The ordinal is the admitted deterministic
  order of the catalog itself, so retrieval never needs a comparator to make
  results stable. The index carries identity only. It adds no relationship, no
  evidence, and no authority that the catalog did not already admit, and it is
  rejected outright when its derived digests do not match the declared bindings.

  @scenario:project-sidefx-semantic-identity-index
  @input:sidefx-semantic-identity-index-projection-request
  @input-contract:sidefx-semantic-identity-index-projection-request.v1
  @event:sidefx-semantic-identity-index-projection-requested
  @event-authority:project-sidefx-semantic-identity-index.v1
  @outcome:sidefx-semantic-identity-index
  @outcome-contract:sidefx-semantic-identity-index.v1
  @outcome-terminal
  Scenario: Project a digest-bound identity index over the closed catalog
    Given the closed 109-object catalog subjects and their declared snapshot and catalog digests
    When each subject is bound to its catalog ordinal and the index and receipt digests are derived
    Then one digest-bound identity index preserves catalog order and admits no authority the catalog did not declare
