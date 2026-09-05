@capability:analyze-sidefx-semantic-impact
@root-scenario:analyze-sidefx-semantic-impact
Feature: Report only attributable downstream semantic impact

  Impact is a graph question, not a license to infer dependencies from prose,
  directory proximity, lexical similarity, or model testimony. This capability
  owns no retrieval engine. It compiles an ordinary IMPACT request against one
  allow-listed graph pattern, resolves it through the pinned Wave 2 knowledge
  capability, removes the starting subject from the result set, and reports
  only grounded downstream subjects. If the admitted graph carries no such
  relationship path, impact is NOT_OBSERVABLE and the query receipt is retained.

  @scenario:analyze-sidefx-semantic-impact
  @input:sidefx-impact-analysis-request
  @input-contract:sidefx-impact-analysis-request.v1
  @event:sidefx-impact-analysis-requested
  @event-authority:analyze-sidefx-semantic-impact.v1
  @outcome:sidefx-semantic-impact-analysis
  @outcome-contract:sidefx-semantic-impact-analysis.v1
  @outcome-terminal
  Scenario: Resolve downstream impact through an admitted graph plan
    Given one semantic subject, the pinned corpus generation, and the admitted query policy allowances
    When its downstream impact plan is resolved through the admitted knowledge capability
    Then only attributable grounded downstream subjects are reported, or impact remains not observable with a receipt
