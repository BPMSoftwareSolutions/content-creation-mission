@capability:observe-governed-repository
@root-scenario:observe-governed-repository
Feature: Observe a governed repository

  A downstream consumer supplies one governed repository-observation request
  containing an admitted repository root, an observation authority reference,
  and a bounded set of declared resources. The consumer receives canonical
  repository facts sufficient for downstream evaluation without acquiring
  authority to interpret those facts or change the repository.

  The capability observes only declared resources and semantic identities. It
  returns stable resource ordering, presence or absence, exact bytes and
  digests when requested, and complete observation lineage. It does not make
  migration decisions, validate or accept a candidate, execute a resource,
  mutate repository state, or claim that any downstream policy has passed.

  Repository access is an explicit governed effect responsibility. Pure
  transformations may resolve the bounded observation context, but they may
  not fabricate repository facts. Traversal outside the admitted root,
  undeclared resources, escaped links, unreadable authorities, and identity or
  digest mismatches terminate with attributable evidence.

  @scenario:observe-governed-repository
  @input:governed-repository-observation-request
  @input-contract:governed-repository-observation-request.v1
  @event:observe-governed-repository
  @event-authority:observe-governed-repository.v1
  @outcome:governed-repository-observation-request-delegated
  @outcome-contract:governed-repository-observation-request.v1
  Scenario: Delegate one governed repository observation
    Given one admitted repository root, observation authority reference, and bounded resource scope
    When a downstream consumer requests the declared repository observation composition
    Then the unchanged request is delegated with its authority lineage and no repository fact is fabricated

  @scenario:resolve-governed-repository-observation-scope
  @input:governed-repository-observation-request
  @input-contract:governed-repository-observation-request.v1
  @event:resolve-governed-repository-observation-scope
  @event-authority:resolve-governed-repository-observation-scope.v1
  @outcome:bounded-governed-repository-observation-context
  @outcome-contract:bounded-governed-repository-observation-context.v1
  Scenario: Resolve the exact authorized observation scope
    Given one governed repository-observation request and one admitted observation authority
    When the admitted root, declared resources, requested fact forms, and stable semantic identity order are resolved
    Then one bounded observation context identifies only authorized resources and facts, or an attributable rejection is returned before repository access

  @scenario:observe-bounded-governed-repository-facts
  @input:bounded-governed-repository-observation-context
  @input-contract:bounded-governed-repository-observation-context.v1
  @event:observe-bounded-governed-repository-facts
  @event-authority:observe-bounded-governed-repository-facts.v1
  @outcome:governed-repository-observation
  @outcome-contract:governed-repository-observation.v1
  @outcome-terminal
  Scenario: Return canonical repository facts without mutation
    Given one bounded observation context and one admitted repository-observation effect capability
    When every declared resource is observed in stable semantic identity order
    Then canonical presence facts, requested bytes and digests, sorted identities, attributable rejections, and complete effect lineage are returned without repository mutation or downstream decisions
