@capability:construct-sidefx-evaluation-corpus-snapshot
@root-scenario:construct-sidefx-evaluation-corpus-snapshot
Feature: Construct one non-production SideFX evaluation corpus snapshot

  This bounded evaluation capability freezes one already classified, closed,
  single-resource manifest as an immutable candidate snapshot. It preserves the
  retained ontology, repository, and canonicalization identities but does not
  classify sources, canonicalize arbitrary input, publish an artifact, move a
  current pointer, or establish Wave 1 production readiness.

  @scenario:construct-sidefx-evaluation-corpus-snapshot
  @input:sidefx-evaluation-corpus-snapshot-construction-request
  @input-contract:sidefx-evaluation-corpus-snapshot-construction-request.v1
  @event:sidefx-evaluation-corpus-snapshot-construction-requested
  @event-authority:construct-sidefx-evaluation-corpus-snapshot.v1
  @outcome:sidefx-semantic-corpus-snapshot
  @outcome-contract:sidefx-semantic-corpus-snapshot.v1
  @outcome-terminal
  Scenario: Freeze one preclassified evaluation resource as a candidate snapshot
    Given one closed single-resource evaluation manifest with a precomputed snapshot identity
    When its declared resource and lineage are assembled under the retained ontology
    Then one candidate snapshot preserves those exact facts without publication, current selection, or production eligibility
