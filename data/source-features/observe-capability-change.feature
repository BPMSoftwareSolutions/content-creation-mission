@capability:observe-capability-change
@root-scenario:observe-capability-change
Feature: Observe one governed capability change

  An engineer or agent can ask for the current meaning and progress of a
  capability change at any point without mutating it. Observation resolves the
  authoritative state, permitted mutation boundary, proof impact, evidence,
  findings, and next legitimate action from the change set and its receipts.

  Status never infers completion from activity testimony, confuses a candidate
  with admitted authority, or repairs missing state. Missing, divergent, or
  inaccessible evidence remains visible as an exact observation finding.

  @scenario:observe-capability-change
  @input:capability-change-status-request
  @input-contract:capability-change-status-request.v1
  @event:capability-change-status-requested
  @event-authority:observe-capability-change.v1
  @outcome:capability-change-status
  @outcome-contract:capability-change-status.v1
  @outcome-terminal
  Scenario: Observe the authoritative status of one change
    Given one change identity or one current governed change context
    When capability change status is requested
    Then one read-only status reports identity, reason, root capability, baseline, mutation set, impact proof set, state, stage, evidence, findings, admitted-authority relationship, and authorized next action

  @scenario:resolve-capability-change-state
  @input:capability-change-status-request
  @input-contract:capability-change-status-request.v1
  @event:capability-change-state-resolution-requested
  @event-authority:resolve-capability-change-state.v1
  @outcome:capability-change-state
  @outcome-contract:capability-change-state.v1
  @outcome-terminal
  Scenario: Resolve state only from authoritative receipts
    Given one change set and any opening, sealing, publication, rejection, or recovery receipts bound to it
    When the current state is resolved
    Then exactly one OPEN, SEALED, PUBLISHED, or REJECTED state and its current stage are derived from closed receipt lineage without testimony declaring its own success

  @scenario:resolve-capability-change-next-action
  @input:capability-change-state
  @input-contract:capability-change-state.v1
  @event:capability-change-next-action-resolution-requested
  @event-authority:resolve-capability-change-next-action.v1
  @outcome:capability-change-next-action
  @outcome-contract:capability-change-next-action.v1
  @outcome-terminal
  Scenario: Resolve the next legitimate action from state and findings
    Given one authoritative change state, its mutation boundary, current findings, and admitted lifecycle policy
    When the next legitimate action is resolved
    Then the result names only an action authorized in the current state or reports that no action is authorized without widening scope or mutation permission

  @scenario:represent-capability-change-evidence
  @input:capability-change-state
  @input-contract:capability-change-state.v1
  @event:capability-change-evidence-representation-requested
  @event-authority:represent-capability-change-evidence.v1
  @outcome:capability-change-evidence-view
  @outcome-contract:capability-change-evidence-view.v1
  @outcome-terminal
  Scenario: Represent parallel authoring and proof evidence without conflating them
    Given retained authoring testimony, semantic and blueprint deltas, conformance, fixtures, impact proofs, Cross-Apply, capsule proof, and publication receipts
    When change evidence is represented
    Then each evidence stream retains its authority, disposition, digest, and relationship to the current state without activity testimony becoming admission evidence

  @scenario:hold-unobservable-capability-change
  @input:capability-change-observation-findings
  @input-contract:capability-change-observation-findings.v1
  @event:capability-change-observation-disposition-requested
  @event-authority:hold-unobservable-capability-change.v1
  @outcome:held-capability-change-observation
  @outcome-contract:held-capability-change-observation.v1
  @outcome-terminal
  Scenario: Report missing or divergent change evidence exactly
    Given an unknown change identity, missing authoritative state, divergent receipt lineage, or inaccessible evidence
    When the observation disposition is resolved
    Then STATUS_HELD returns exact findings without mutating the change, selecting a replacement state, or hiding the last verified admitted-authority relationship

