@capability:provision-capability-artifacts
@root-scenario:provision-capability-artifacts
Feature: Decide which observed artifacts enter the content-addressed capability estate

  Provisioning has been performed by a hand-written script since the estate began.
  That script does seven things, and only two of them are effects: it walks a
  directory tree, and it writes bytes. The other five are decisions - admitting a
  batch request, screening artifacts against a secret policy, classifying each
  artifact by its declared extension, resolving what provisioning disposition each
  one earns, and binding the manifest entries that record them. Those five are what
  this capability owns.

  It owns no walk and no scan. The observed artifact set is presented to it, and
  each artifact arrives carrying the policy screen already applied. That is not a
  convenience: the admitted transformation vocabulary has no pattern matching, so a
  capability claiming to screen bytes would be claiming something it cannot perform.
  Screening is testimony. Deciding what that testimony means is governance.

  An artifact carrying any policy finding is rejected unless the batch request
  declares an explicit allowance naming that artifact and that rule. An allowance
  naming no finding is itself a finding, because a blanket allowance is how a secret
  enters an estate that believes it screens.

  Classification is declared, never inferred. An artifact whose extension is absent
  from the declared catalog is rejected rather than guessed at, because a guessed
  media type is how an unreviewable byte acquires a respectable name.

  Coverage is proven. Every artifact the batch selected is either provisioned with a
  content-addressed entry or rejected with a named reason. An artifact that is
  neither is a hole in the account the estate keeps of itself.

  Absence is never normalized. A batch presenting no observed artifacts has not
  provisioned an empty set; it has failed to present its observations.

  @scenario:provision-capability-artifacts
  @input:provisioning-request
  @input-contract:capability-provisioning-request.v1
  @event:provision-capability-artifacts
  @event-authority:provision-capability-artifacts.v1
  @outcome:provisioning-decision
  @outcome-contract:capability-provisioning-decision.v1
  @outcome-terminal
  Scenario: Return one exact provisioning decision for one presented batch
    Given one admitted batch request and the observed artifacts it selected
    When the batch is provisioned
    Then one decision binds every provisioned entry, every rejection, and the exact coverage of the selection
    And PROVISIONED is returned only when every observed artifact was either provisioned or explicitly rejected

  @scenario:admit-provisioning-batch-request
  @input:provisioning-inputs
  @input-contract:provisioning-carrier.v1
  @event:admit-provisioning-batch-request
  @event-authority:admit-provisioning-batch-request.v1
  @outcome:admitted-request
  @outcome-contract:provisioning-carrier.v1
  Scenario: Admit the batch request before observing anything about its artifacts
    Given one batch request declaring its zone, its source node and its selections
    When the request is admitted
    Then the batch identity, zone and selection set are bound exactly as declared
    And a batch declaring no selection returns PROVISIONING_SELECTION_UNDECLARED
    And a batch presenting no observed artifact returns PROVISIONING_OBSERVATION_ABSENT rather than an empty provisioned set

  @scenario:screen-observed-artifacts-against-policy
  @input:provisioning-inputs
  @input-contract:provisioning-carrier.v1
  @event:screen-observed-artifacts-against-policy
  @event-authority:screen-observed-artifacts-against-policy.v1
  @outcome:screened-artifacts
  @outcome-contract:provisioning-carrier.v1
  Scenario: Reject any artifact whose supplied screen carries a finding
    Given observed artifacts each carrying the policy screen already applied to their bytes
    When the screen testimony is admitted
    Then every artifact carrying a policy finding is rejected with the rule that rejected it
    And an artifact whose screen was never applied returns POLICY_SCREEN_NOT_APPLIED rather than passing unscreened
    And a declared allowance naming no specific finding returns POLICY_ALLOWANCE_UNBOUNDED, because a blanket allowance is not an exception

  @scenario:classify-artifact-by-declared-extension
  @input:provisioning-inputs
  @input-contract:provisioning-carrier.v1
  @event:classify-artifact-by-declared-extension
  @event-authority:classify-artifact-by-declared-extension.v1
  @outcome:classified-artifacts
  @outcome-contract:provisioning-carrier.v1
  Scenario: Classify each artifact from the declared catalog rather than inferring it
    Given one declared artifact catalog binding each extension to its type, language and media type
    When the observed artifacts are classified
    Then every artifact carries the exact artifact type, language and media type its extension declares
    And an extension absent from the declared catalog returns ARTIFACT_EXTENSION_UNDECLARED rather than a guessed classification

  @scenario:resolve-artifact-provisioning-disposition
  @input:provisioning-inputs
  @input-contract:provisioning-carrier.v1
  @event:resolve-artifact-provisioning-disposition
  @event-authority:resolve-artifact-provisioning-disposition.v1
  @outcome:dispositioned-artifacts
  @outcome-contract:provisioning-carrier.v1
  Scenario: Resolve what provisioning disposition each artifact earns
    Given classified artifacts and the refinement state each one is declared to hold
    When the dispositions are resolved
    Then a non-script artifact is DURABLY_PROVISIONED
    And a script that has been scenario-shaped is SEMANTIC_EXTRACTION_PENDING, and one that has not is SCENARIO_SHAPING_PENDING, because a provisioned script is preserved evidence and never a discharged responsibility

  @scenario:bind-provisioning-manifest-entries
  @input:provisioning-inputs
  @input-contract:provisioning-carrier.v1
  @event:bind-provisioning-manifest-entries
  @event-authority:bind-provisioning-manifest-entries.v1
  @outcome:manifest-entries
  @outcome-contract:provisioning-carrier.v1
  Scenario: Bind one content-addressed entry for every provisioned artifact
    Given dispositioned artifacts and the digests observed for their bytes
    When the manifest entries are bound
    Then every entry names its source digest, its byte length, its content-addressed repository path and the sources that observed it
    And two observations of identical bytes bind one entry carrying both observed sources, never two entries
    And an entry whose observed digest does not match its declared digest returns PROVISIONED_DIGEST_DIVERGED

  @scenario:close-provisioning-coverage
  @input:provisioning-inputs
  @input-contract:provisioning-carrier.v1
  @event:close-provisioning-coverage
  @event-authority:close-provisioning-coverage.v1
  @outcome:coverage-ledger
  @outcome-contract:provisioning-carrier.v1
  Scenario: Prove every selected artifact was accounted for
    Given the observed artifact set and the entries and rejections resolved from it
    When coverage is closed
    Then the ledger reports every observed artifact, its entry or its rejection, and any artifact left unaccounted
    And an unaccounted artifact holds the batch rather than reporting it provisioned
