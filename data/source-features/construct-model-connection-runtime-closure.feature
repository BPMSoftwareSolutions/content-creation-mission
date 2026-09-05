@capability:construct-model-connection-runtime-closure
@root-scenario:construct-model-connection-runtime-closure
Feature: Construct model connection runtime closures

  # Legacy dependencies:
  # sibling scenario-driven-architecture checkout
  # sibling generic-llm-connector checkout
  # connector-local tsx loading of TypeScript source

  This capability constructs and proves the complete content-addressed runtime
  closure needed by a projected model connection. Its objective covers a valid
  closure, explicit external-host obligations, sibling and absolute path
  rejection, source-loader and development-dependency rejection, package
  pinning, artifact cardinality, digest integrity, and target-host coverage.

  The closure contains projected executable mechanics, admitted configuration,
  schemas, protocol profiles, packages, and stable logical paths. Operating
  system processes, target runtimes, credential stores, clocks, entropy, DNS,
  TLS, sockets, and remote providers remain classified external substrates.
  Existing publication capabilities retain sole write authority.

  @scenario:construct-model-connection-runtime-closure
  @input:model-connection-runtime-closure-request
  @input-contract:construct-model-connection-runtime-closure-input.v1
  @event:model-connection-runtime-closure-construction-requested
  @event-authority:construct-model-connection-runtime-closure.v1
  @outcome:model-connection-runtime-closure
  @outcome-contract:model-connection-runtime-closure-evidence.v1
  @outcome-terminal
  Scenario: Construct one complete self-contained projected runtime closure
    Given admitted model connection capabilities, provider and adapter authority, projection plans, exact packages, schemas, configuration, host profiles, policies, and conformance evidence
    When the model connection runtime closure is constructed
    Then every bundled artifact and external host obligation has one stable identity, classification, path where applicable, origin, and digest without sibling imports, development loaders, package installation, publication, execution, or credential disclosure

  @scenario:classify-model-connection-external-substrates
  @input:model-connection-external-substrate-facts
  @input-contract:construct-model-connection-runtime-closure-input.v1
  @event:model-connection-external-substrate-classification-requested
  @event-authority:classify-model-connection-external-substrates.v1
  @outcome:model-connection-external-substrate-classification
  @outcome-contract:model-connection-runtime-closure-evidence.v1
  @outcome-terminal
  Scenario: Distinguish projected artifacts from irreducible host substrates
    Given runtime dependency facts for processes, language runtimes, credential stores, clocks, entropy, network stacks, provider services, packages, schemas, configuration, and projected mechanics
    When each dependency is classified
    Then every item is classified exactly once as bundled authority or an admitted external obligation and no physical substrate is falsely represented as projected semantic content

  @scenario:reject-sibling-repository-runtime-dependency
  @input:sibling-repository-runtime-dependency
  @input-contract:construct-model-connection-runtime-closure-input.v1
  @event:sibling-repository-runtime-closure-requested
  @event-authority:reject-sibling-repository-runtime-dependency.v1
  @outcome:sibling-repository-runtime-dependency-findings
  @outcome-contract:model-connection-runtime-closure-evidence.v1
  @outcome-terminal
  Scenario: Reject runtime reliance on sibling repository layout
    Given a planned runtime importing SDA, connector, configuration, schemas, packages, or source through a sibling checkout or repository-relative path
    When runtime dependency closure is evaluated
    Then every sibling assumption is named with its importing artifact and no environment-specific repository layout is admitted

  @scenario:reject-unsafe-runtime-path
  @input:unsafe-model-connection-runtime-path
  @input-contract:construct-model-connection-runtime-closure-input.v1
  @event:unsafe-model-connection-runtime-path-observed
  @event-authority:reject-unsafe-runtime-path.v1
  @outcome:unsafe-runtime-path-findings
  @outcome-contract:model-connection-runtime-closure-evidence.v1
  @outcome-terminal
  Scenario: Reject absolute traversal symlink and duplicate logical paths
    Given planned runtime artifacts containing an absolute path, root escape, traversal segment, symlink escape, case-colliding path, or duplicate logical destination
    When governed placement and path cardinality are evaluated
    Then each unsafe or ambiguous path is returned as an exact finding and no artifact plan is repaired, published, or executed

  @scenario:reject-runtime-source-loader-dependency
  @input:model-connection-runtime-source-loader-dependency
  @input-contract:construct-model-connection-runtime-closure-input.v1
  @event:model-connection-runtime-source-loader-observed
  @event-authority:reject-runtime-source-loader-dependency.v1
  @outcome:runtime-source-loader-dependency-findings
  @outcome-contract:model-connection-runtime-closure-evidence.v1
  @outcome-terminal
  Scenario: Reject runtime compilation or dynamic loading of source
    Given a closure requiring tsx, ts-node, a compiler, development-only transpilation, dynamic TypeScript import, source-tree evaluation, or equivalent runtime source loading
    When executable-origin and loader closure are evaluated
    Then every source-loader dependency is named and only preprojected executable mechanics remain eligible

  @scenario:reject-undeclared-or-mutable-runtime-package
  @input:undeclared-or-mutable-runtime-package
  @input-contract:construct-model-connection-runtime-closure-input.v1
  @event:runtime-package-closure-requested
  @event-authority:reject-undeclared-or-mutable-runtime-package.v1
  @outcome:runtime-package-closure-findings
  @outcome-contract:model-connection-runtime-closure-evidence.v1
  @outcome-terminal
  Scenario: Reject missing development-only or unpinned package authority
    Given a runtime import whose package is undeclared, omitted from production closure, available only as a development dependency, versioned by a mutable range, or missing integrity evidence
    When package authority is closed
    Then exact package findings are returned and no ambient node_modules lookup, installation, version selection, or network package resolution occurs

  @scenario:reject-incomplete-runtime-artifact-set
  @input:incomplete-model-connection-runtime-artifacts
  @input-contract:construct-model-connection-runtime-closure-input.v1
  @event:runtime-artifact-cardinality-evaluation-requested
  @event-authority:reject-incomplete-runtime-artifact-set.v1
  @outcome:runtime-artifact-cardinality-findings
  @outcome-contract:model-connection-runtime-closure-evidence.v1
  @outcome-terminal
  Scenario: Reject missing extra duplicate or unoriginated runtime artifacts
    Given a runtime plan with a required artifact missing, an undeclared extra artifact, duplicate logical identity, unsupported target artifact, or artifact lacking projected origin
    When artifact-set cardinality and origin are evaluated
    Then every missing, extra, duplicate, unsupported, or unoriginated artifact is named and no partial closure is reported

  @scenario:reject-runtime-digest-drift
  @input:drifted-model-connection-runtime-artifacts
  @input-contract:construct-model-connection-runtime-closure-input.v1
  @event:runtime-digest-closure-requested
  @event-authority:reject-runtime-digest-drift.v1
  @outcome:runtime-digest-drift-findings
  @outcome-contract:model-connection-runtime-closure-evidence.v1
  @outcome-terminal
  Scenario: Reject bytes that differ from manifest projection or package authority
    Given projected executable, configuration, schema, protocol, package, provider, adapter, policy, or conformance bytes whose observed digest differs from the runtime manifest
    When content-addressed integrity is evaluated
    Then every drifted identity and expected and observed digest are returned without rewriting bytes, updating authority, or weakening the proof

  @scenario:reject-incomplete-model-connection-host-coverage
  @input:incomplete-model-connection-host-coverage
  @input-contract:construct-model-connection-runtime-closure-input.v1
  @event:model-connection-host-coverage-evaluation-requested
  @event-authority:reject-incomplete-model-connection-host-coverage.v1
  @outcome:model-connection-host-coverage-findings
  @outcome-contract:model-connection-runtime-closure-evidence.v1
  @outcome-terminal
  Scenario: Reject a target host lacking required runtime or effect mechanics
    Given declared CLI, projected consumer, or MCP target hosts with missing runtime version support, adapter coverage, credential port, HTTP port, schema admission, cancellation, hashing, clock, identity, or evidence delivery mechanics
    When hostability is evaluated
    Then each missing host obligation is named and no unsupported target is included in the closed runtime manifest
