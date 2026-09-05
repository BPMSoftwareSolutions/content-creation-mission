@capability:analyze-sidefx-semantic-gaps
@root-scenario:analyze-sidefx-semantic-gaps
Feature: Report what the admitted corpus does not know

  A brain that only reports what it knows is dangerous. This capability
  enumerates the shape of the corpus's ignorance from admitted structure alone:
  ontology kinds the snapshot declares but never populates, obligations that
  remain not observable, objects carrying no attributable evidence, objects
  whose only source class is projection evidence, and sources the profile
  cannot interpret. Each gap class keeps its own subject list rather than being
  merged into one score, because the reason a gap exists determines what would
  close it. Reporting a gap is a finding about the corpus, never a defect claim
  against the subject.

  @scenario:analyze-sidefx-semantic-gaps
  @input:sidefx-gap-analysis-request
  @input-contract:sidefx-gap-analysis-request.v1
  @event:sidefx-gap-analysis-requested
  @event-authority:analyze-sidefx-semantic-gaps.v1
  @outcome:sidefx-semantic-gap-analysis
  @outcome-contract:sidefx-semantic-gap-analysis.v1
  @outcome-terminal
  Scenario: Enumerate every admitted gap class with its own subjects
    Given the pinned catalog objects, relationship graph, proof obligations, and declared ontology kinds
    When each gap class is derived from admitted structure only
    Then every observed gap class reports its own subjects and count without collapsing them into a single score
