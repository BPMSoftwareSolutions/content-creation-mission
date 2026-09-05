@capability:determine-model-role-provider-switch
@root-scenario:determine-model-role-provider-switch
Feature: Determine model role provider switches

  A model-role stage may declare an ordered set of compatible model bindings
  from multiple providers and exact conditions under which the conveyor may
  switch. This capability makes that switch decision from normalized execution
  testimony, stage authority, remaining alternatives, compatibility evidence,
  privacy and effect policy, and remaining budget. Models and provider adapters
  cannot select their successor.

  Switching preserves the stage, role, responsibility, semantic request,
  context-pack digest, output contract, evidence requirements, and user-facing
  stage identity. Provider and concrete-model changes remain explicit internal
  lineage. The decision never invokes a model or mutates prior testimony.

  @scenario:determine-model-role-provider-switch
  @input:model-role-provider-switch-request
  @input-contract:determine-model-role-provider-switch-input.v1
  @event:model-role-provider-switch-decision-requested
  @event-authority:determine-model-role-provider-switch.v1
  @outcome:model-role-provider-switch-decision
  @outcome-contract:model-role-provider-switch-decision-evidence.v1
  @outcome-terminal
  Scenario: Switch after an authorized usage or capacity failure
    Given one role stage whose current provider reports an admitted quota rate-limit token-capacity or usage-limit disposition and whose ordered switch policy names a compatible eligible alternative binding
    When the model role provider switch is determined
    Then SWITCH_ELIGIBLE selects exactly the first eligible alternative and preserves stage role request context contract budget and user-facing identity with complete provider-change lineage

  @scenario:retain-current-model-role-binding-after-success
  @input:successful-model-role-stage-receipt
  @input-contract:determine-model-role-provider-switch-input.v1
  @event:successful-model-role-provider-switch-decision-requested
  @event-authority:retain-current-model-role-binding-after-success.v1
  @outcome:retain-current-model-role-binding-decision
  @outcome-contract:model-role-provider-switch-decision-evidence.v1
  @outcome-terminal
  Scenario: Do not switch after a successful stage outcome
    Given one stage receipt satisfying its output contract and closure policy
    When provider switching is evaluated
    Then RETAIN_CURRENT_BINDING is returned and no alternative model credential endpoint budget or invocation becomes eligible

  @scenario:switch-model-role-provider-after-timeout-or-unavailability
  @input:unavailable-model-role-stage-receipt
  @input-contract:determine-model-role-provider-switch-input.v1
  @event:unavailable-model-role-provider-switch-decision-requested
  @event-authority:switch-model-role-provider-after-timeout-or-unavailability.v1
  @outcome:unavailable-model-role-provider-switch-decision
  @outcome-contract:model-role-provider-switch-decision-evidence.v1
  @outcome-terminal
  Scenario: Switch after timeout or provider unavailability only when declared
    Given one timed-out or unavailable stage receipt and a switch policy explicitly admitting that disposition with a compatible remaining alternative
    When provider switching is evaluated
    Then SWITCH_ELIGIBLE selects the next authorized binding without replaying the failed provider or changing role responsibility semantic input or output contract

  @scenario:hold-unlisted-model-role-switch-condition
  @input:unlisted-model-role-switch-condition
  @input-contract:determine-model-role-provider-switch-input.v1
  @event:unlisted-model-role-provider-switch-decision-requested
  @event-authority:hold-unlisted-model-role-switch-condition.v1
  @outcome:model-role-provider-switch-not-authorized
  @outcome-contract:model-role-provider-switch-decision-evidence.v1
  @outcome-terminal
  Scenario: Refuse switching for a disposition absent from policy
    Given authentication request-rejection response-format cancellation internal-failure or other testimony not listed by the stage switch policy
    When provider switching is evaluated
    Then SWITCH_NOT_AUTHORIZED retains the original terminal disposition and no alternative model provider or adapter is made eligible

  @scenario:reject-incompatible-model-role-switch-target
  @input:incompatible-model-role-switch-target
  @input-contract:determine-model-role-provider-switch-input.v1
  @event:incompatible-model-role-switch-target-evaluation-requested
  @event-authority:reject-incompatible-model-role-switch-target.v1
  @outcome:incompatible-model-role-switch-target-findings
  @outcome-contract:model-role-provider-switch-decision-evidence.v1
  @outcome-terminal
  Scenario: Reject an alternative that cannot preserve stage semantics
    Given an alternative binding lacking the role interaction mode context capacity structured-output support tool policy output contract privacy classification data residency adapter conformance or host mechanics required by the stage
    When switch-target compatibility is evaluated
    Then the alternative is ineligible with exact compatibility findings and cannot receive stage input or credential authority

  @scenario:skip-ineligible-model-role-switch-target
  @input:model-role-switch-chain-with-ineligible-target
  @input-contract:determine-model-role-provider-switch-input.v1
  @event:model-role-switch-chain-selection-requested
  @event-authority:skip-ineligible-model-role-switch-target.v1
  @outcome:model-role-switch-chain-selection
  @outcome-contract:model-role-provider-switch-decision-evidence.v1
  @outcome-terminal
  Scenario: Select the first eligible alternative in declared order
    Given an ordered alternative list whose earlier binding is stale unauthorized unavailable or incompatible and whose later binding is completely eligible
    When switch-target selection is performed
    Then the first eligible binding in declared order is selected and every skipped binding retains an attributable non-invocation reason without model-ranked selection

  @scenario:exhaust-model-role-provider-switch-alternatives
  @input:exhausted-model-role-provider-switch-chain
  @input-contract:determine-model-role-provider-switch-input.v1
  @event:model-role-provider-switch-exhaustion-requested
  @event-authority:exhaust-model-role-provider-switch-alternatives.v1
  @outcome:model-role-provider-alternatives-exhausted
  @outcome-contract:model-role-provider-switch-decision-evidence.v1
  @outcome-terminal
  Scenario: Return one stable terminal disposition after all alternatives are exhausted
    Given a switch-eligible failure and an alternative chain with no unused eligible binding
    When provider switching is determined
    Then PROVIDER_ALTERNATIVES_EXHAUSTED preserves every attempted and skipped binding disposition in order and no undeclared provider is discovered or invoked

  @scenario:prevent-model-role-provider-switch-cycle
  @input:cyclic-or-replayed-model-role-provider-switch
  @input-contract:determine-model-role-provider-switch-input.v1
  @event:model-role-provider-switch-cycle-evaluation-requested
  @event-authority:prevent-model-role-provider-switch-cycle.v1
  @outcome:model-role-provider-switch-cycle-findings
  @outcome-contract:model-role-provider-switch-decision-evidence.v1
  @outcome-terminal
  Scenario: Prevent cycles duplicate alternatives and revisiting failed bindings
    Given switch authority containing duplicate bindings a cycle or a request to revisit a previously attempted provider model binding
    When switch-chain integrity is evaluated
    Then the cycle duplicate or replay is rejected and no binding can be invoked more times than its own attempt authority permits

  @scenario:preserve-model-role-semantics-across-provider-switch
  @input:model-role-provider-switch-semantic-comparison
  @input-contract:determine-model-role-provider-switch-input.v1
  @event:model-role-provider-switch-semantic-proof-requested
  @event-authority:preserve-model-role-semantics-across-provider-switch.v1
  @outcome:model-role-provider-switch-semantic-evidence
  @outcome-contract:model-role-provider-switch-decision-evidence.v1
  @outcome-terminal
  Scenario: Preserve role request context and output meaning across providers
    Given a proposed switch with canonical stage role responsibility request context-pack output-contract evidence-policy and non-claim digests before and after selection
    When semantic continuity is evaluated
    Then all non-provider digests remain byte-identical and only the authorized provider model adapter endpoint credential reference and attempt lineage differ

  @scenario:respect-model-role-switch-budget-and-approval
  @input:model-role-provider-switch-budget-and-approval-facts
  @input-contract:determine-model-role-provider-switch-input.v1
  @event:model-role-provider-switch-budget-and-approval-evaluation-requested
  @event-authority:respect-model-role-switch-budget-and-approval.v1
  @outcome:model-role-provider-switch-budget-and-approval-decision
  @outcome-contract:model-role-provider-switch-decision-evidence.v1
  @outcome-terminal
  Scenario: Hold switching when cost token time effect or approval authority is insufficient
    Given an otherwise compatible alternative whose invocation would exceed remaining stage or conveyor budget change effect class or require missing human approval
    When switch budget and approval eligibility are evaluated
    Then the alternative is held with exact budget effect or approval findings and no credential or network effect is authorized

  @scenario:produce-deterministic-model-role-switch-selection
  @input:equivalent-model-role-provider-switch-facts
  @input-contract:determine-model-role-provider-switch-input.v1
  @event:model-role-provider-switch-determinism-proof-requested
  @event-authority:produce-deterministic-model-role-switch-selection.v1
  @outcome:deterministic-model-role-provider-switch-evidence
  @outcome-contract:model-role-provider-switch-decision-evidence.v1
  @outcome-terminal
  Scenario: Replay equivalent switch facts to the same selection
    Given semantically equivalent stage receipts policies alternatives compatibility proofs and budgets in different serialization order
    When provider switching is determined repeatedly
    Then selection skipped-binding reasons and decision digests are byte-identical and no live latency model preference or provider response wording affects the choice

  @scenario:preserve-user-facing-stage-continuity-during-provider-switch
  @input:model-role-provider-switch-user-experience-facts
  @input-contract:determine-model-role-provider-switch-input.v1
  @event:model-role-provider-switch-user-experience-evaluation-requested
  @event-authority:preserve-user-facing-stage-continuity-during-provider-switch.v1
  @outcome:model-role-provider-switch-user-experience-evidence
  @outcome-contract:model-role-provider-switch-decision-evidence.v1
  @outcome-terminal
  Scenario: Keep one stable user-facing stage while internal providers change
    Given an authorized switch between compatible provider model bindings for one role stage and its declared progress and terminal presentation policy
    When user-facing switch disposition is derived
    Then the stage remains one continuous operation with stable role goal progress identity and output contract while internal provider-change evidence remains available for diagnostics without exposing avoidable provider churn
