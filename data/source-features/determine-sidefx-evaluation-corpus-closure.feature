@capability:determine-sidefx-evaluation-corpus-closure
@root-scenario:determine-sidefx-evaluation-corpus-closure
Feature: Determine non-production SideFX evaluation corpus closure

  This capability applies the retained closure law to one digest-bound
  evaluation snapshot, object catalog, relationship graph, and the three
  required input-receipt identities. The bounded fixture binds the exact Wave 0
  Gherkin, JSON-authority, and proof-binding receipts to one lineage-consistent
  evaluation generation. It issues no current selection and makes no production
  closure claim.

  @scenario:determine-sidefx-evaluation-corpus-closure
  @input:sidefx-evaluation-corpus-closure-request
  @input-contract:sidefx-evaluation-corpus-closure-request.v1
  @event:sidefx-evaluation-corpus-closure-requested
  @event-authority:determine-sidefx-evaluation-corpus-closure.v1
  @outcome:sidefx-semantic-corpus-closure
  @outcome-contract:sidefx-semantic-corpus-closure.v1
  @outcome-terminal
  Scenario: Close one lineage-consistent non-production evaluation corpus
    Given one lineage-consistent evaluation snapshot catalog and graph with all three exact Wave 0 receipt bindings
    When the retained closure checks and receipt dispositions are evaluated
    Then CORPUS_CLOSED is returned with four satisfied checks and no findings without issuing current selection
