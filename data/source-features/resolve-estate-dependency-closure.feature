@capability:resolve-estate-dependency-closure
@root-scenario:resolve-estate-dependency-closure
Feature: Resolve whether every admitted capability in the estate can still be executed

  An estate can verify clean, pass its entire test suite, and be unable to execute
  a single capability. That is not hypothetical. It happened here: repairing one
  capability changed its application binding, every capsule that pinned the old
  binding digest became unresolvable, and nothing in the repository noticed.
  Capsule verification confirmed that each capsule matched its own recorded bytes,
  which was true and irrelevant. The tests exercised transformations directly and
  never resolved the estate. Both gates were green over a broken estate.

  The missing gate is closure. A capability is executable only if every dependency
  it declares resolves to an admitted capsule whose application binding still
  canonicalizes to the digest the dependent pinned, and whose capability authority
  still matches the digest its execution plan recorded. Each capsule being
  internally consistent proves nothing about whether the graph they form holds.

  Closure is computed, never assumed. Every declared dependency is resolved to a
  target, every target binding is recanonicalized and rehashed, and every pin is
  compared against what was recomputed. A pin that matches by name and diverges by
  digest is exactly the failure that hid here, so name agreement is never accepted
  as resolution.

  Resolution is pure. It consumes the estate inventory it is given: capsules,
  their declared dependencies, their application bindings and their recorded
  digests. It reads no filesystem and admits nothing. What it returns is the
  disposition the estate is actually in.

  Absence is never normalized. An estate presenting no capsules has not thereby
  achieved closure; it has failed to present an estate, and that is a finding.
  Closure reports RESOLVED only when every declared dependency of every presented
  capsule resolved and matched.

  @scenario:resolve-estate-dependency-closure
  @input:closure-request
  @input-contract:estate-dependency-closure-request.v1
  @event:resolve-estate-dependency-closure
  @event-authority:resolve-estate-dependency-closure.v1
  @outcome:closure
  @outcome-contract:estate-dependency-closure.v1
  @outcome-terminal
  Scenario: Return the exact executability disposition of one presented estate
    Given one estate inventory carrying every admitted capsule, its declared dependencies and its application binding
    When the dependency closure is resolved
    Then one closure binds every resolved dependency, every recomputed digest, and every divergence found
    And RESOLVED is returned only when no declared dependency is unresolved and no pin diverges

  @scenario:resolve-declared-dependencies
  @input:closure-inputs
  @input-contract:estate-closure-carrier.v1
  @event:resolve-declared-dependencies
  @event-authority:resolve-declared-dependencies.v1
  @outcome:declared
  @outcome-contract:estate-closure-carrier.v1
  Scenario: Resolve every declared dependency to an admitted target
    Given one estate inventory whose capsules declare dependencies by binding reference
    When the declared dependencies are resolved
    Then every declared dependency names the admitted capsule it resolved to
    And a dependency naming no admitted capsule returns DEPENDENCY_TARGET_UNRESOLVED

  @scenario:recompute-binding-digests
  @input:closure-inputs
  @input-contract:estate-closure-carrier.v1
  @event:recompute-binding-digests
  @event-authority:recompute-binding-digests.v1
  @outcome:recomputed
  @outcome-contract:estate-closure-carrier.v1
  Scenario: Recompute each target binding rather than trusting its recorded digest
    Given one resolved dependency set carrying each target application binding
    When the binding digests are recomputed
    Then every target binding is canonicalized and hashed to the digest it currently produces
    And a target presenting no application binding returns TARGET_BINDING_ABSENT rather than a recomputed digest over nothing

  @scenario:detect-stale-pins
  @input:closure-inputs
  @input-contract:estate-closure-carrier.v1
  @event:detect-stale-pins
  @event-authority:detect-stale-pins.v1
  @outcome:stale
  @outcome-contract:estate-closure-carrier.v1
  Scenario: Compare every pin against what was recomputed
    Given one dependency set carrying both the pinned digests and the recomputed digests
    When the pins are compared
    Then every pin whose digest diverges from the recomputed digest is reported with both values
    And a dependency that resolves by name while diverging by digest returns DEPENDENCY_PIN_STALE, because name agreement is not resolution

  @scenario:close-execution-resolvability
  @input:closure-inputs
  @input-contract:estate-closure-carrier.v1
  @event:close-execution-resolvability
  @event-authority:close-execution-resolvability.v1
  @outcome:resolvability
  @outcome-contract:estate-closure-carrier.v1
  Scenario: Close over the whole graph rather than each capsule alone
    Given one dependency graph and the divergences found within it
    When execution resolvability is closed
    Then every capsule reachable from a divergent binding is reported as unexecutable, not only the capsule that changed
    And an estate presenting no capsules returns ESTATE_INVENTORY_ABSENT rather than an empty closure reported as RESOLVED
