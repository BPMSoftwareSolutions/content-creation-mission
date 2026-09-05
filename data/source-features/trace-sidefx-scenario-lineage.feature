@capability:trace-sidefx-scenario-lineage
@root-scenario:trace-sidefx-scenario-lineage
Feature: Trace the admitted lineage of one semantic subject

  A lineage answer is only as good as the edges the corpus actually admits.
  This capability owns no retrieval of its own: it compiles an ordinary lineage
  plan, hands it to the admitted knowledge resolver under a pinned binding
  digest, and then shapes the grounded hops into a lineage record. Each hop
  keeps its retrieval channel, its grounding disposition, the evidence
  relationships attributable to it, and its exact source reference. When the
  requested pattern names edge kinds the admitted graph does not carry, the
  lineage is reported LINEAGE_NOT_OBSERVABLE with the reason attached, rather
  than as an empty success or an inferred path.

  @scenario:trace-sidefx-scenario-lineage
  @input:sidefx-scenario-lineage-request
  @input-contract:sidefx-scenario-lineage-request.v1
  @event:sidefx-scenario-lineage-requested
  @event-authority:trace-sidefx-scenario-lineage.v1
  @outcome:sidefx-semantic-scenario-lineage
  @outcome-contract:sidefx-semantic-scenario-lineage.v1
  @outcome-terminal
  Scenario: Compile a lineage plan and shape its grounded hops
    Given one lineage subject, the pinned corpus generation, and the admitted query policy allowances
    When the plan is resolved through the admitted knowledge resolver and its grounded results are shaped into hops
    Then the lineage is observed with attributable hops and a receipt, or reported not observable with its reason
