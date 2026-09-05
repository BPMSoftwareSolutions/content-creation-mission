@capability:resolve-sidefx-capability-precedents
@root-scenario:resolve-sidefx-capability-precedents
Feature: Ground authoring precedents in four separate classes

  Before anything new is authored, the brain must say what already exists.
  This capability compiles one ordinary discovery plan through the admitted
  knowledge resolver and then classifies its grounded results into four
  independent precedent classes: semantic, structural, proof, and execution.
  The classes never merge. Each result keeps its own per-channel counts for
  exact identity, graph, and lexical evidence, the exact features that selected
  it, and the limits that bound its applicability, so a reader can always see
  why a precedent was offered. There is no single similarity scalar to hide
  behind, and a class with nothing admitted behind it returns empty rather than
  reaching for a weaker signal.

  @scenario:resolve-sidefx-capability-precedents
  @input:sidefx-capability-precedent-request
  @input-contract:sidefx-capability-precedent-request.v1
  @event:sidefx-capability-precedent-requested
  @event-authority:resolve-sidefx-capability-precedents.v1
  @outcome:sidefx-semantic-precedent-set
  @outcome-contract:sidefx-semantic-precedent-set.v1
  @outcome-terminal
  Scenario: Classify grounded discovery results into four precedent classes
    Given a declared authoring intent, the pinned corpus generation, and the admitted query policy allowances
    When one discovery plan is resolved and its results are classified by semantic, structural, proof, and execution evidence
    Then each class keeps its own results, per-channel counts, selected features, applicability limits, and query receipt
