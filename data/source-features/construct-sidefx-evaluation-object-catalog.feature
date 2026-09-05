@capability:construct-sidefx-evaluation-object-catalog
@root-scenario:construct-sidefx-evaluation-object-catalog
Feature: Construct one non-production SideFX evaluation object catalog

  This bounded capability derives one root CONFORMANCE_EVIDENCE record for the
  exact frozen seed file and one held CAPABILITY record for each of the
  106 connector-selected members and one held ARTIFACT record for each of the
  two non-canonical members in the frozen seed population. Every record
  points to the exact seed-file bytes and its /members/<index> evidence pointer.
  It does not reinterpret the seed evidence as canonical feature authority and
  does not claim the general selector, canonical JSON, reduction, or authority-
  resolution mechanics required by the production derivation capability.

  @scenario:construct-sidefx-evaluation-object-catalog
  @input:sidefx-evaluation-object-catalog-construction-request
  @input-contract:sidefx-evaluation-object-catalog-construction-request.v1
  @event:sidefx-evaluation-object-catalog-construction-requested
  @event-authority:construct-sidefx-evaluation-object-catalog.v1
  @outcome:sidefx-semantic-object-catalog
  @outcome-contract:sidefx-semantic-object-catalog.v1
  @outcome-terminal
  Scenario: Derive the full frozen connector-selected evaluation catalog
    Given one evaluation snapshot and all 108 frozen seed members in declared order
    When the 106 connector-selected members are mapped to held capability records
    Then one ordered 109-record catalog retains the seed root, exact byte and pointer lineage, and no claim of current conformance
