@capability:establish-capsule-first-repository-closure
@root-scenario:establish-capsule-first-repository-closure
Feature: Establish capsule-first repository closure

  Capsule-First Repository Law: once a capability has proven capsule closure,
  its expanded workspace is a disposable realization and MUST NOT be required
  as durable repository state. A clean checkout containing only the admitted
  bootstrap and capsule estate must be sufficient to verify, resolve, execute,
  and when necessary reconstruct every eligible capability.

  The capsule manager and language resolvers produce one deterministic proof
  receipt from the admitted bootstrap and capsule estate. This capability does
  not implement those mechanics again. It admits or holds that receipt by
  evaluating the exact estate, dependency, execution, reconstruction,
  projection, and proof counts bound to the two manifest digests.

  The current admitted transition bar is 173 verified capsules carrying 5,753
  entries, 33 of 33 dependencies and 2 of 2 external tool roots present, 173
  directly executable runtimes carrying 926 fixtures and passing 1,099 of
  1,099 direct tests, 173 reconstructable and projectable workspaces carrying
  2,269 reconstructed entries, a 6 of 6 pre-proof, a 473 of 473 sterile
  generated aggregate, and zero broken, skipped, todo, or attributable
  findings. The source repository compatibility gate remains 481 of 481; its
  eight legacy repository checks are not part of the sterile generated estate.

  No success switch is accepted. CAPSULE_FIRST_REPOSITORY_CLOSED is derived
  only from the structured proof facts. Any mismatch returns
  CAPSULE_FIRST_REPOSITORY_HELD and preserves the findings. This capability
  authorizes a separate repository transition; it performs no deletion.

  @scenario:establish-capsule-first-repository-closure
  @input:capsule-first-repository-closure-request
  @input-contract:capsule-first-repository-closure-request.v1
  @event:capsule-first-repository-closure-requested
  @event-authority:establish-capsule-first-repository-closure.v1
  @outcome:capsule-first-repository-closure-evidence
  @outcome-contract:capsule-first-repository-closure-evidence.v1
  @outcome-terminal
  Scenario: Admit the deterministic capsule-first proof receipt
    Given one capsule-first sterile-checkout proof receipt bound to the admitted bootstrap and capsule estate manifest digests
    When semantic authority evaluates every required count and zero-failure obligation
    Then CAPSULE_FIRST_REPOSITORY_CLOSED is returned only when the complete current transition bar is proven, otherwise CAPSULE_FIRST_REPOSITORY_HELD retains the exact findings
