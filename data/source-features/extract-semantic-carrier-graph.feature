@capability:extract-semantic-carrier-graph
@root-scenario:extract-canonical-carrier-graph
Feature: Extract a canonical graph from a validated Scenario Semantic Carrier

  One validated Scenario Semantic Carrier becomes one canonical graph and exact extraction receipt before carrier blackout, or one attributable held disposition.

  @scenario:extract-canonical-carrier-graph
  @input:validated-semantic-carrier-request
  @input-contract:semantic-carrier-extraction-request.v1
  @event:extract-canonical-carrier-graph
  @event-authority:extract-canonical-carrier-graph.v1
  @outcome:carrier-graph-extraction-classified
  @outcome-contract:semantic-carrier-extraction-stage.v1
  Scenario: Extract canonical carrier graph
    Given exact unchanged carrier bytes and their exact conformant validator PASS receipt
    When one canonical graph is extracted from the validated bytes and carrier blackout is established
    Then graph extraction is classified without projecting or evaluating downstream meaning

  @scenario:return-extracted-graph
  @input:extracted-graph-stage
  @input-contract:semantic-carrier-extraction-stage.v1
  @event:return-extracted-graph
  @event-authority:return-extracted-graph.v1
  @outcome:canonical-carrier-graph-extracted
  @outcome-contract:semantic-carrier-extraction-result.v1
  @outcome-terminal
  Scenario: Return extracted graph
    Given one canonical graph and exact extraction lineage with blackout established
    When the extracted graph receipt is returned
    Then EXTRACTED is returned with carrier blackout established

  @scenario:return-extraction-held
  @input:held-extraction-stage
  @input-contract:semantic-carrier-extraction-stage.v1
  @event:return-extraction-held
  @event-authority:return-extraction-held.v1
  @outcome:semantic-carrier-extraction-held
  @outcome-contract:semantic-carrier-extraction-result.v1
  @outcome-terminal
  Scenario: Return extraction held
    Given attributable validator-receipt, carrier-binding, graph-canonicalization, or blackout findings
    When the extraction-held receipt is returned
    Then EXTRACTION_HELD is returned with ordered attributable findings

