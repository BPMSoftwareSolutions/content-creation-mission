@capability:construct-model-role-conveyor-plan
@root-scenario:construct-model-role-conveyor-plan
Feature: Construct model role conveyor plans

  # Existing role oracles:
  # agentic-harness/features/converge-projectable-capability-candidate.feature
  # agentic-harness/docs/self-authoring-handoff-roadmap.md

  This capability constructs the complete deterministic plan for a conveyor in
  which multiple models from multiple providers perform different declared
  roles and responsibilities. Each stage fixes its stage and role identities,
  responsibility and capability binding, primary provider and concrete-model
  binding, compatible ordered alternatives and exact switch conditions,
  admitted inputs, context-pack authority, output contract, dependency edges,
  effect class, approval, attempt and substitution policy, budget, evidence
  requirements, and non-claims before any model is invoked.

  Author, reviewer, correction-advisor, summarizer, or future roles are data in
  admitted role authority rather than hard-coded provider behavior. A provider
  assigned to one role is not fallback authority for another role.

  @scenario:construct-model-role-conveyor-plan
  @input:model-role-conveyor-planning-request
  @input-contract:construct-model-role-conveyor-plan-input.v1
  @event:model-role-conveyor-plan-construction-requested
  @event-authority:construct-model-role-conveyor-plan.v1
  @outcome:model-role-conveyor-plan
  @outcome-contract:model-role-conveyor-plan-evidence.v1
  @outcome-terminal
  Scenario: Construct a closed ordered multi-model multi-provider role plan
    Given admitted pipeline objectives, role and responsibility authority, distinct governed provider model bindings, stage contracts, context authority, dependency edges, effect policy, budgets, and non-claims
    When the model role conveyor plan is constructed
    Then every stage has one complete content-addressed role responsibility primary and alternative provider-model context contract switch effect budget and lineage binding in deterministic eligible order without invoking a model

  @scenario:plan-distinct-models-from-one-provider
  @input:single-provider-multiple-model-role-plan-request
  @input-contract:construct-model-role-conveyor-plan-input.v1
  @event:single-provider-multiple-model-role-plan-requested
  @event-authority:plan-distinct-models-from-one-provider.v1
  @outcome:single-provider-multiple-model-role-plan
  @outcome-contract:model-role-conveyor-plan-evidence.v1
  @outcome-terminal
  Scenario: Assign different concrete models from one provider to different roles
    Given multiple stage roles whose admitted bindings name one provider authority and different concrete models with compatible adapter coverage
    When role-stage bindings are planned
    Then each role retains its own concrete model policy context and receipt identity without collapsing the models into one provider default

  @scenario:plan-distinct-models-across-providers
  @input:multiple-provider-model-role-plan-request
  @input-contract:construct-model-role-conveyor-plan-input.v1
  @event:multiple-provider-model-role-plan-requested
  @event-authority:plan-distinct-models-across-providers.v1
  @outcome:multiple-provider-model-role-plan
  @outcome-contract:model-role-conveyor-plan-evidence.v1
  @outcome-terminal
  Scenario: Assign stage roles to models governed by different providers
    Given multiple stage roles with independently admitted bindings to models from different provider authorities and compatible stage contracts
    When the multi-provider role plan is constructed
    Then each stage retains its exact provider model adapter endpoint credential reference and policy binding without implicit fallback cross-provider substitution or shared-provider assumptions while separately declared switch authority remains explicit

  @scenario:plan-model-role-provider-switch-chain
  @input:model-role-provider-switch-chain-plan-request
  @input-contract:construct-model-role-conveyor-plan-input.v1
  @event:model-role-provider-switch-chain-plan-requested
  @event-authority:plan-model-role-provider-switch-chain.v1
  @outcome:model-role-provider-switch-chain-plan
  @outcome-contract:model-role-conveyor-plan-evidence.v1
  @outcome-terminal
  Scenario: Plan compatible ordered alternatives and exact provider-switch conditions
    Given one role stage with a primary model binding and alternatives from one or more providers plus declared usage quota rate-limit timeout availability and other switch conditions
    When its provider-switch chain is planned
    Then every alternative has stable order compatibility proof independent credential and endpoint authority per-binding attempts and shared role request context output-contract and user-facing stage identity without invoking any provider

  @scenario:reject-invalid-model-role-provider-switch-chain
  @input:invalid-model-role-provider-switch-chain
  @input-contract:construct-model-role-conveyor-plan-input.v1
  @event:invalid-model-role-provider-switch-chain-evaluation-requested
  @event-authority:reject-invalid-model-role-provider-switch-chain.v1
  @outcome:invalid-model-role-provider-switch-chain-findings
  @outcome-contract:model-role-conveyor-plan-evidence.v1
  @outcome-terminal
  Scenario: Reject undeclared incompatible cyclic duplicate or unbounded switch authority
    Given a switch chain with no exact trigger condition an unknown or incompatible alternative duplicate or cyclic binding implicit provider discovery unlimited switches missing per-binding attempts or changed role request context contract privacy or effect policy
    When switch-chain closure is evaluated
    Then every invalid condition binding edge policy and bound is named and no implicit fallback or model-selected alternative is added

  @scenario:plan-stable-model-role-conveyor-presentation
  @input:model-role-conveyor-presentation-plan-request
  @input-contract:construct-model-role-conveyor-plan-input.v1
  @event:model-role-conveyor-presentation-plan-requested
  @event-authority:plan-stable-model-role-conveyor-presentation.v1
  @outcome:model-role-conveyor-presentation-plan
  @outcome-contract:model-role-conveyor-plan-evidence.v1
  @outcome-terminal
  Scenario: Plan one stable user-facing stage across retries and provider switches
    Given pipeline presentation authority declaring operation stage progress hold terminal and diagnostic visibility for roles with attempts and provider-switch chains
    When the conveyor presentation plan is constructed
    Then each role exposes one stable user-facing stage identity and coherent progress semantics while attempts provider changes and native errors remain attributable diagnostics without generating duplicate user operations

  @scenario:plan-deterministic-model-role-dependency-order
  @input:model-role-dependency-graph-planning-request
  @input-contract:construct-model-role-conveyor-plan-input.v1
  @event:model-role-dependency-order-planning-requested
  @event-authority:plan-deterministic-model-role-dependency-order.v1
  @outcome:ordered-model-role-dependency-plan
  @outcome-contract:model-role-conveyor-plan-evidence.v1
  @outcome-terminal
  Scenario: Order dependent and independent model stages deterministically
    Given an acyclic role-stage dependency graph containing serial dependencies and independently eligible stages
    When stage eligibility and order are derived
    Then dependencies precede consumers and ties use one declared stable ordering rule without model-selected sequencing or nondeterministic concurrency

  @scenario:preserve-model-role-plan-canonical-identity
  @input:semantically-equivalent-model-role-plan-requests
  @input-contract:construct-model-role-conveyor-plan-input.v1
  @event:model-role-plan-canonical-identity-proof-requested
  @event-authority:preserve-model-role-plan-canonical-identity.v1
  @outcome:model-role-plan-canonical-identity-evidence
  @outcome-contract:model-role-conveyor-plan-evidence.v1
  @outcome-terminal
  Scenario: Produce stable plan bytes independent of input serialization order
    Given semantically equivalent role plan facts in different object order and facts differing in at least one stage authority value
    When their canonical plans are constructed
    Then equivalent facts produce byte-identical plan digests and any changed role responsibility provider model contract edge policy or budget changes the plan digest

  @scenario:reject-incomplete-model-role-stage-authority
  @input:incomplete-model-role-stage-authority
  @input-contract:construct-model-role-conveyor-plan-input.v1
  @event:incomplete-model-role-stage-plan-requested
  @event-authority:reject-incomplete-model-role-stage-authority.v1
  @outcome:incomplete-model-role-stage-findings
  @outcome-contract:model-role-conveyor-plan-evidence.v1
  @outcome-terminal
  Scenario: Reject stages missing identity role responsibility or binding authority
    Given a stage lacking a unique stage ID role ID responsibility capability provider model binding or evidence identity
    When stage authority completeness is evaluated
    Then every missing or duplicate identity is named and no partial or inferred stage is added to the conveyor plan

  @scenario:reject-stale-or-unknown-model-role-binding
  @input:stale-or-unknown-model-role-binding
  @input-contract:construct-model-role-conveyor-plan-input.v1
  @event:stale-or-unknown-model-role-plan-requested
  @event-authority:reject-stale-or-unknown-model-role-binding.v1
  @outcome:stale-or-unknown-model-role-binding-findings
  @outcome-contract:model-role-conveyor-plan-evidence.v1
  @outcome-terminal
  Scenario: Reject stage bindings that are absent stale or incompatible
    Given a stage naming an unknown role responsibility capability provider model adapter or a binding whose digest or supported interaction mode no longer matches authority
    When stage binding closure is evaluated
    Then each unresolved stale or incompatible identity is returned and no default role model provider or adapter is selected

  @scenario:reject-model-role-contract-or-context-mismatch
  @input:model-role-contract-or-context-mismatch
  @input-contract:construct-model-role-conveyor-plan-input.v1
  @event:model-role-contract-and-context-plan-requested
  @event-authority:reject-model-role-contract-or-context-mismatch.v1
  @outcome:model-role-contract-or-context-findings
  @outcome-contract:model-role-conveyor-plan-evidence.v1
  @outcome-terminal
  Scenario: Reject inputs outputs or context outside role authority
    Given a stage whose input reference output contract context-pack class root scope or source authority is missing incompatible forbidden or broader than its role permits
    When stage data authority is closed
    Then every contract context and scope mismatch is named without widening access copying unrelated testimony or allowing free-form model context selection

  @scenario:reject-cyclic-or-unreachable-model-role-stage
  @input:invalid-model-role-dependency-graph
  @input-contract:construct-model-role-conveyor-plan-input.v1
  @event:model-role-dependency-graph-plan-requested
  @event-authority:reject-cyclic-or-unreachable-model-role-stage.v1
  @outcome:invalid-model-role-dependency-findings
  @outcome-contract:model-role-conveyor-plan-evidence.v1
  @outcome-terminal
  Scenario: Reject cycles dangling edges unreachable stages and ambiguous joins
    Given a role-stage graph with a dependency cycle unknown predecessor dangling output unreachable stage ambiguous join or missing terminal path
    When graph closure is evaluated
    Then every structural finding is returned in stable stage order and no model is allowed to repair or reinterpret the pipeline graph

  @scenario:reject-model-role-authority-escalation
  @input:model-role-authority-escalation-plan
  @input-contract:construct-model-role-conveyor-plan-input.v1
  @event:model-role-authority-escalation-evaluation-requested
  @event-authority:reject-model-role-authority-escalation.v1
  @outcome:model-role-authority-escalation-findings
  @outcome-contract:model-role-conveyor-plan-evidence.v1
  @outcome-terminal
  Scenario: Reject roles claiming another role or deterministic gate responsibility
    Given a stage role claiming provider selection pipeline planning candidate admission code projection oracle change approval conformance promotion or another role responsibility outside its authority
    When role separation and non-claims are evaluated
    Then every excess responsibility is rejected and model testimony remains unable to grant itself or another model execution or acceptance authority

  @scenario:reject-incomplete-model-role-effect-and-budget-policy
  @input:incomplete-model-role-effect-and-budget-policy
  @input-contract:construct-model-role-conveyor-plan-input.v1
  @event:model-role-effect-and-budget-plan-requested
  @event-authority:reject-incomplete-model-role-effect-and-budget-policy.v1
  @outcome:model-role-effect-and-budget-policy-findings
  @outcome-contract:model-role-conveyor-plan-evidence.v1
  @outcome-terminal
  Scenario: Reject stages without closed attempts substitution effects approvals or budgets
    Given a model stage missing attempt authority continuation and substitution declarations effect class approval law token or cost budget timeout cancellation scope or evidence policy
    When execution policy closure is evaluated
    Then each missing policy is named and no implicit retry fallback approval budget or effect authority is added

  @scenario:enforce-distinct-model-role-separation-policy
  @input:model-role-separation-policy-plan
  @input-contract:construct-model-role-conveyor-plan-input.v1
  @event:model-role-separation-policy-evaluation-requested
  @event-authority:enforce-distinct-model-role-separation-policy.v1
  @outcome:model-role-separation-policy-evidence
  @outcome-contract:model-role-conveyor-plan-evidence.v1
  @outcome-terminal
  Scenario: Enforce required provider or model independence between roles
    Given role authority requiring selected stages such as author and reviewer to use distinct model bindings providers context or invocation identities
    When physical and semantic role separation is evaluated
    Then the plan preserves every required distinction or returns exact coalescence findings without silently reusing one model session binding or context for incompatible roles
