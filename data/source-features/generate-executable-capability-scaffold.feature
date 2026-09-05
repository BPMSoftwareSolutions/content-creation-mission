@capability:generate-executable-capability-scaffold
@root-scenario:generate-executable-capability-scaffold
Feature: Generate an executable capability scaffold from an admitted design

  An admitted capability design already fixes one Input, one Event, and one
  Outcome. Every capability that executes that circuit does so through the same
  ordered execution shell. Rediscovering that shell for each new capability is
  wasted authoring entropy and is the pressure that produces disposable scripts.

  This capability generates the standard execution shell for one admitted design
  and enumerates exactly what remains unresolved: which mechanics, which
  capability dependencies, which providers, and which evidence obligations. It
  then resolves those slots against the supplied admitted estate and emits the
  next bounded authoring obligation.

  The generation is pure. It consumes the exact declarative carrier bytes it is
  given plus a supplied estate inventory and mechanic catalog. It reads no
  filesystem, invokes no provider, performs no external effect, authors no
  capability, admits no authority, and repairs no blueprint. A scaffold is
  testimony about what remains to be resolved; it is never itself an admission.

  The execution shell carries no business meaning. Its steps are drawn from a
  fixed admitted vocabulary of admit, validate, resolve, invoke, bind, observe,
  and return. A shell step naming a domain term is a defect, not a shortcut,
  because a shell that knows the domain has stopped being reusable and has
  started being an implementation.

  A slot is resolved only against the supplied admitted estate. A capability
  that is absent is reported NOT_FOUND with its exact identity so it can become
  the next bounded authoring obligation. Absence is never normalized to zero
  findings, and a missing inventory is never read as an empty inventory.

  Scaffold completeness is proportional to design completeness. A request
  carrying only a scenario set earns the standard shell and nothing more. A
  request carrying an admitted canonical blueprint earns everything that
  blueprint already fixes: the ordinals, the altitudes, the per-edge binding
  authority, the observability the design declared, the service level it
  promised, and the projection authorities it already named. Rediscovering any
  of those is not thoroughness, it is a second opinion about a settled design.

  A blueprint is conditioning, never suggestion. When one is supplied, the
  scenarios, terminals, routes and slots are read from it rather than from the
  loose fields of the request, and any loose field that contradicts it is a
  finding rather than an override. The scaffold emits no competing circuit in
  that case: it binds the admitted blueprint by digest and returns an embodiment
  receipt, because two circuits carrying two digests for one capability is a
  lineage divergence rather than a richer scaffold.

  Embodiment is proven, never assumed. Every cell, edge, terminal and declared
  slot of the conditioning blueprint must appear in the generated structure, and
  the generated structure must add none of its own. A scaffold that quietly
  introduces executable topology the design never declared has authored
  architecture, which is the one thing this capability exists to refuse.

  Scaffolding closes when every declared slot carries an explicit disposition
  and the same request reproduces byte-identical scaffold evidence.

  @scenario:generate-executable-capability-scaffold
  @input:executable-scaffold-request
  @input-contract:executable-scaffold-request.v1
  @event:generate-executable-capability-scaffold
  @event-authority:generate-executable-capability-scaffold.v1
  @outcome:executable-capability-scaffold
  @outcome-contract:executable-capability-scaffold.v1
  @outcome-terminal
  Scenario: Return one exact scaffold for one admitted design
    Given one admitted capability design carrier and one supplied admitted estate inventory
    When the executable scaffold is generated
    Then one scaffold binds the exact carrier digest, the standard execution shell, every declared slot with its disposition, and the next bounded authoring obligation
    And the scaffold is SCAFFOLD_READY only when no declared slot remains unresolved

  @scenario:generate-standard-execution-shell
  @input:executable-scaffold-request
  @input-contract:executable-scaffold-request.v1
  @event:generate-standard-execution-shell
  @event-authority:generate-standard-execution-shell.v1
  @outcome:standard-execution-shell
  @outcome-contract:scaffold-derivation-carrier.v1
  Scenario: Generate the same ordered execution shell for every capability
    Given any admitted capability design carrier
    When the standard execution shell is generated
    Then the shell carries the same ordered steps for every capability regardless of its domain
    And the shell is marked GENERATED rather than resolved, because a shell is not an execution

  @scenario:reject-business-meaning-in-execution-shell
  @input:executable-scaffold-request
  @input-contract:executable-scaffold-request.v1
  @event:reject-business-meaning-in-execution-shell
  @event-authority:reject-business-meaning-in-execution-shell.v1
  @outcome:shell-vocabulary-disposition
  @outcome-contract:scaffold-derivation-carrier.v1
  Scenario: Keep domain meaning out of the reusable shell
    Given a generated execution shell
    When the shell vocabulary is qualified
    Then every step identity is drawn from the fixed admitted shell vocabulary
    And any step carrying capability-specific or domain-specific meaning returns SHELL_VOCABULARY_ESCAPED

  @scenario:derive-mechanic-slots-from-circuit
  @input:scaffold-derivation-inputs
  @input-contract:scaffold-derivation-carrier.v1
  @event:derive-mechanic-slots-from-circuit
  @event-authority:derive-mechanic-slots-from-circuit.v1
  @outcome:mechanic-slot-set
  @outcome-contract:scaffold-derivation-carrier.v1
  Scenario: Derive required mechanics from the declared circuit
    Given one admitted capability design carrier
    When mechanic slots are derived
    Then every mechanic the declared circuit requires appears exactly once as a slot
    And a mechanic is never invented for a responsibility the circuit does not declare

  @scenario:derive-capability-slots-from-dependencies
  @input:scaffold-derivation-inputs
  @input-contract:scaffold-derivation-carrier.v1
  @event:derive-capability-slots-from-dependencies
  @event-authority:derive-capability-slots-from-dependencies.v1
  @outcome:capability-slot-set
  @outcome-contract:scaffold-derivation-carrier.v1
  Scenario: Derive required capability dependencies from the declared circuit
    Given one admitted capability design carrier
    When capability slots are derived
    Then every capability the circuit delegates to appears exactly once as a slot
    And a delegated responsibility is never silently absorbed into the shell

  @scenario:derive-provider-slots-from-altitude-descents
  @input:scaffold-derivation-inputs
  @input-contract:scaffold-derivation-carrier.v1
  @event:derive-provider-slots-from-altitude-descents
  @event-authority:derive-provider-slots-from-altitude-descents.v1
  @outcome:provider-slot-set
  @outcome-contract:scaffold-derivation-carrier.v1
  Scenario: Derive provider slots only where the circuit descends altitude
    Given one admitted capability design carrier
    When provider slots are derived
    Then every declared provider-slot node and every altitude descent yields exactly one provider slot
    And a provider-free circuit yields zero provider slots rather than an unproven absence

  @scenario:derive-evidence-obligations-from-outcomes
  @input:scaffold-derivation-inputs
  @input-contract:scaffold-derivation-carrier.v1
  @event:derive-evidence-obligations-from-outcomes
  @event-authority:derive-evidence-obligations-from-outcomes.v1
  @outcome:evidence-obligation-set
  @outcome-contract:scaffold-derivation-carrier.v1
  Scenario: Derive evidence obligations from declared outcomes
    Given one admitted capability design carrier
    When evidence obligations are derived
    Then every terminal disposition carries one evidence obligation
    And an outcome without an evidence obligation returns EVIDENCE_OBLIGATION_MISSING

  @scenario:resolve-slots-against-admitted-estate
  @input:scaffold-derivation-inputs
  @input-contract:scaffold-derivation-carrier.v1
  @event:resolve-slots-against-admitted-estate
  @event-authority:resolve-slots-against-admitted-estate.v1
  @outcome:slot-resolution-set
  @outcome-contract:scaffold-derivation-carrier.v1
  Scenario: Resolve every slot against the supplied admitted estate
    Given one derived slot set and one supplied admitted estate inventory
    When the slots are resolved
    Then every slot carries FOUND or NOT_FOUND against the exact supplied inventory
    And a missing or unsupplied inventory returns ESTATE_INVENTORY_UNSUPPLIED rather than resolving every slot as absent

  @scenario:emit-next-bounded-authoring-obligation
  @input:scaffold-derivation-inputs
  @input-contract:scaffold-derivation-carrier.v1
  @event:emit-next-bounded-authoring-obligation
  @event-authority:emit-next-bounded-authoring-obligation.v1
  @outcome:authoring-work-queue
  @outcome-contract:scaffold-derivation-carrier.v1
  Scenario: Emit the next bounded authoring obligation
    Given one resolved slot set carrying at least one NOT_FOUND slot
    When the authoring work queue is emitted
    Then the queue names each unresolved slot as its own bounded authoring obligation
    And a fully resolved slot set emits an empty queue rather than inventing work

  @scenario:replay-scaffold-generation
  @input:scaffold-derivation-inputs
  @input-contract:scaffold-derivation-carrier.v1
  @event:replay-scaffold-generation
  @event-authority:replay-scaffold-generation.v1
  @outcome:scaffold-replay-disposition
  @outcome-contract:scaffold-derivation-carrier.v1
  Scenario: Require byte-identical replay without self-issued correctness
    Given one frozen scaffold request
    When the scaffold is generated twice
    Then both products are byte-identical
    And a divergent replay returns SCAFFOLD_REPLAY_DIVERGED rather than the later product

  @scenario:derive-blueprint-carrier-from-declared-scenarios
  @input:scaffold-derivation-inputs
  @input-contract:scaffold-derivation-carrier.v1
  @event:derive-blueprint-carrier-from-declared-scenarios
  @event-authority:derive-blueprint-carrier-from-declared-scenarios.v1
  @outcome:derived-blueprint-carrier
  @outcome-contract:scaffold-derivation-carrier.v1
  Scenario: Bind declared topology and never invent design
    Given the declared scenario set of one reviewed feature
    When the blueprint carrier is bound
    Then every declared scenario becomes exactly one responsibility node and every declared terminal disposition becomes one terminal node
    And the routes, variants, convergence and semantic precedence are taken only from the declared topology supplied with the request
    And a request carrying no declared topology returns BLUEPRINT_TOPOLOGY_NOT_DECLARED and emits no circuit, because topology is designed meaning and a convenient default geometry would let implementation mechanics author architecture
    And an archetype instantiation whose geometry differs from the admitted archetype returns ARCHETYPE_TOPOLOGY_MUTATED, because instantiating an archetype may bind identities and configuration but may never add, remove or rewire a node, an edge, a branch, a convergence, a precedence or a terminal
    And a topology that must change beyond its archetype returns ARCHETYPE_NO_LONGER_FITS and belongs to the design resolver rather than to this scaffold
    And the emitted carrier records where its topology came from, as an archetype instantiation, an archetype composition, or a design resolver candidate
    And the emitted carrier is always a candidate requiring conformance and human blueprint admission, never an admitted design
    And a request conditioned on a supplied canonical blueprint emits no carrier at all and binds that blueprint by its own digest, because emitting a second circuit for one capability is a lineage divergence rather than a derivation

  @scenario:emit-mechanical-authoring-artifacts
  @input:scaffold-derivation-inputs
  @input-contract:scaffold-derivation-carrier.v1
  @event:emit-mechanical-authoring-artifacts
  @event-authority:emit-mechanical-authoring-artifacts.v1
  @outcome:mechanical-artifact-set
  @outcome-contract:scaffold-derivation-carrier.v1
  Scenario: Emit every artifact that is a pure function of the reviewed feature
    Given one derived canonical circuit and its declared contracts
    When the mechanical authoring artifacts are emitted
    Then the capability authority, blueprint carrier, interface authority, execution authorities, contract catalog and contract skeletons are emitted complete
    And each emitted artifact is derived only from the reviewed feature, never from an assumption about the domain

  @scenario:preserve-semantic-transformation-as-unresolved
  @input:scaffold-derivation-inputs
  @input-contract:scaffold-derivation-carrier.v1
  @event:preserve-semantic-transformation-as-unresolved
  @event-authority:preserve-semantic-transformation-as-unresolved.v1
  @outcome:unresolved-semantic-cells
  @outcome-contract:scaffold-derivation-carrier.v1
  Scenario: Never generate the meaning the capability exists to express
    Given one emitted artifact set
    When the semantic transformation artifact is emitted
    Then it carries one unresolved cell for the root transformation and one preserving cell for each remaining scenario
    And an emitted transformation that claims a resolved root cell returns SEMANTIC_MEANING_FABRICATED, because a scaffold that writes meaning has stopped being a scaffold
    And each emitted transformation carries only the identity and expression the admitted transformation schema permits, with the unresolved marker carried beside the transformation set rather than inside a transformation, because an artifact that cannot pass projection validation was never a usable scaffold

  @scenario:condition-scaffold-on-admitted-blueprint
  @input:scaffold-derivation-inputs
  @input-contract:scaffold-derivation-carrier.v1
  @event:condition-scaffold-on-admitted-blueprint
  @event-authority:condition-scaffold-on-admitted-blueprint.v1
  @outcome:blueprint-conditioning
  @outcome-contract:scaffold-derivation-carrier.v1
  Scenario: Read the design from the blueprint rather than from loose request fields
    Given one supplied canonical circuit blueprint and the loose scenario, terminal, topology and slot fields of the same request
    When the scaffold is conditioned
    Then the scenarios, terminals, routes, variants, convergence, ordinals, altitudes, observability, binding authority, service level and projection authorities are read from the blueprint
    And a loose request field contradicting the blueprint returns BLUEPRINT_CONDITIONING_CONTRADICTED naming the field, because a disassembled design re-entered by hand is a claim to be checked and never an override
    And a supplied blueprint carrying no authority digest returns BLUEPRINT_DIGEST_UNBOUND rather than being conditioned on anonymously
    And a supplied blueprint that is a candidate rather than admitted still conditions the scaffold but is recorded as CANDIDATE_CONDITIONED, because scaffolding an unadmitted design is permitted while pretending it was admitted is not

  @scenario:prove-blueprint-embodiment
  @input:scaffold-derivation-inputs
  @input-contract:scaffold-derivation-carrier.v1
  @event:prove-blueprint-embodiment
  @event-authority:prove-blueprint-embodiment.v1
  @outcome:embodiment-receipt
  @outcome-contract:scaffold-derivation-carrier.v1
  Scenario: Prove the generated structure embodies the conditioning design exactly
    Given one conditioning blueprint and the structure generated from it
    When embodiment is proven
    Then the receipt reports every declared cell, edge, terminal and slot together with the generated element that embodies it
    And a declared element with no generated counterpart returns BLUEPRINT_CELL_UNEMBODIED naming it
    And generated executable topology with no declared counterpart returns UNDECLARED_EXECUTABLE_TOPOLOGY naming it, because a scaffold may realize a design and may never extend one

  @scenario:resolve-scaffold-completeness-level
  @input:scaffold-derivation-inputs
  @input-contract:scaffold-derivation-carrier.v1
  @event:resolve-scaffold-completeness-level
  @event-authority:resolve-scaffold-completeness-level.v1
  @outcome:completeness-level
  @outcome-contract:scaffold-derivation-carrier.v1
  Scenario: Report how much of the design the scaffold was actually given
    Given one request and whatever design authority it supplied
    When the completeness level is resolved
    Then a request carrying only scenarios reports SCENARIO_ONLY, one carrying resolved topology reports TOPOLOGY_RESOLVED, one carrying contracts and ports reports INTERFACES_RESOLVED, and one carrying required capabilities and mechanics reports COMPOSITION_RESOLVED
    And the level reported is the highest one the supplied authority actually satisfies, never the level the request claims
    And the level is reported alongside the unresolved authoring obligations, so the caller can see what remains and what supplying a richer blueprint would have saved
