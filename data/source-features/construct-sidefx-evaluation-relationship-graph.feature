@capability:construct-sidefx-evaluation-relationship-graph
@root-scenario:construct-sidefx-evaluation-relationship-graph
Feature: Construct one non-production SideFX evaluation relationship graph

  The frozen seed population is retained as one evidence object and its 106
  connector-selected member records are retained as capability objects. This
  bounded capability derives only the evidence-to-subject edges justified by
  those exact JSON pointers. It cannot infer relationships between capabilities
  or claim that frozen membership observation proves their current semantics.

  @scenario:construct-sidefx-evaluation-relationship-graph
  @input:sidefx-evaluation-relationship-graph-construction-request
  @input-contract:sidefx-evaluation-relationship-graph-construction-request.v1
  @event:sidefx-evaluation-relationship-graph-construction-requested
  @event-authority:construct-sidefx-evaluation-relationship-graph.v1
  @outcome:sidefx-semantic-relationship-graph
  @outcome-contract:sidefx-semantic-relationship-graph.v1
  @outcome-terminal
  Scenario: Relate frozen seed evidence to its selected capability subjects
    Given one snapshot and its 109-record evaluation catalog
    When the 106 connector-selected seed records are mapped in original member order
    Then 106 evidence-to-subject edges retain exact seed pointers while held artifacts remain edge-free and semantic proof remains not observable
