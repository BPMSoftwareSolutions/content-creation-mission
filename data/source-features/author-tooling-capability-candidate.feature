@capability:author-tooling-capability-candidate
@root-scenario:author-tooling-capability-candidate
Feature: Convergently author an SDA capability candidate from canonical source authority

  A downstream consumer describes one desired capability as canonical Gherkin
  with declared scenario, input, event, outcome, and contract connectors, bound
  to one approved capability-authoring blueprint and one selected blueprint
  cell. The consumer does not supply an implementation or language-specific
  source code.

  The authoring capability uses the admitted feature, the approved blueprint
  identity, and the selected cell as its semantic boundary, and may obtain
  bounded model testimony for exactly one authoring work unit at a time. Every
  required companion artifact is authored as atomic, independently
  schema-bound testimony and composed into canonical projectable SDA source
  authority by deterministic assembly.

  Convergence is owned by the harness, not by the model. The circuit selects
  work, constrains context, validates testimony, classifies defects, authorizes
  repair from admitted attempt authority, preserves closed authority, and
  proves closure before any candidate is assembled. Probabilistic authoring may
  fail locally; the harness must converge globally.

  The harness never spends probabilistic intelligence discovering a
  deterministic defect. Before any model invocation, a deterministic
  authorability preflight proves the selected work unit ready, and every
  preflight failure holds the circuit and reports the exact finding without
  invoking the model. When a condition covered by a readiness proof changes,
  the proof expires: a provider switch or a semantic repair re-proves the work
  unit before any further model invocation.

  Mechanical repair is authorized only when exactly one authority-preserving
  repair exists. Zero repairs are reported as not mechanically repairable and
  more than one as ambiguous; neither may be repaired mechanically. Any
  ambiguous correction is semantic repair carried back to the model with the
  original testimony immutable and the exact finding and allowed mutation
  surface declared. Every successful attempt reduces the unresolved semantic
  surface. Closed work is never regenerated without explicit change authority.
  Work-unit recurrence is authorized only while the ledger proves work
  remains, every recurrence closes at least one unit, and recurrence ends when
  the ledger itself proves all work closed.

  Model output remains candidate testimony. Authoring a candidate does not
  establish contract admission, behavioral conformance, projection success, or
  promotion. Those dispositions remain owned by independent SDA authorities.

  The root scenario composes eighteen monotonic supporting scenarios. Each
  supporting scenario consumes the immutable outcome of the preceding
  scenario, appends its own evidence and lineage, and cannot reinterpret or
  replace facts that have already been admitted.

  @scenario:author-tooling-capability-candidate
  @input:capability-authoring-context
  @input-contract:capability-authoring-context.v1
  @event:author-capability-candidate
  @event-authority:author-capability-candidate.v1
  @outcome:projectable-capability-authoring-result
  @outcome-contract:projectable-capability-authoring-result.v2
  @outcome-terminal
  Scenario: Convergently author one projectable capability candidate
    Given one canonical capability authoring context containing a canonical feature, one approved blueprint identity, and one selected blueprint cell
    When the downstream consumer requests a declarative SDA capability candidate
    Then either a self-contained projectable source bundle with complete convergence lineage and closure proof, or exact classified findings with complete immutable attempt testimony and no authorized retry, or a held disposition reporting the exact ineligible surface, is returned without handwritten executable code or claims of acceptance

  @scenario:admit-capability-authoring-context
  @input:capability-authoring-context
  @input-contract:capability-authoring-context.v1
  @event:admit-capability-authoring-context
  @event-authority:admit-capability-authoring-context.v1
  @outcome:admitted-capability-authoring-context
  @outcome-contract:admitted-capability-authoring-context.v1
  Scenario: Admit the capability authoring context
    Given one submitted authoring context containing the canonical feature, one approved blueprint identity, one selected blueprint cell, and existing admitted authority
    When the feature, the blueprint binding, and the selected cell are admitted as canonical source authority
    Then immutable admitted authoring context and its source lineage are available to the authoring circuit

  @scenario:resolve-capability-authoring-profile
  @input:admitted-capability-authoring-context
  @input-contract:admitted-capability-authoring-context.v1
  @event:resolve-capability-authoring-profile
  @event-authority:resolve-capability-authoring-profile.v1
  @outcome:bounded-capability-authoring-profile
  @outcome-contract:bounded-capability-authoring-profile.v2
  Scenario: Resolve the bounded capability authoring profile and attempt authority
    Given immutable admitted authoring context and its declared semantic connectors
    When the required SDA source artifacts, archetypes, permissible ontology vocabulary, and admitted authoring attempt authority are resolved
    Then a bounded authoring profile fixes the complete declarative candidate surface, the required artifact catalog, and the attempt authority — maximum authoring attempts, maximum repair attempts, provider switch policy, repairable finding classes, retryable provider findings, immutable closed-work policy, and terminal disposition policy — without introducing implementation authority

  @scenario:initialize-artifact-authoring-ledger
  @input:bounded-capability-authoring-profile
  @input-contract:bounded-capability-authoring-profile.v2
  @event:initialize-artifact-authoring-ledger
  @event-authority:initialize-artifact-authoring-ledger.v1
  @outcome:artifact-authoring-ledger
  @outcome-contract:artifact-authoring-ledger.v1
  Scenario: Initialize the artifact authoring ledger
    Given one bounded authoring profile naming its exact required companion-artifact catalog
    When one artifact authoring ledger is derived from the profile catalog alone
    Then every required artifact is carried with its required flag, schema authority, dependencies, and pending status, and no artifact is admitted as closed

  @scenario:select-next-eligible-artifact-fragment
  @input:artifact-authoring-ledger
  @input-contract:artifact-authoring-ledger.v1
  @event:select-next-eligible-artifact-fragment
  @event-authority:select-next-eligible-artifact-fragment.v1
  @outcome:eligible-artifact-authoring-work-unit
  @outcome-contract:eligible-artifact-authoring-work-unit.v1
  @outcome-terminal
  Scenario: Select the next eligible artifact or fragment work unit
    Given one artifact authoring ledger with admitted dependency and closure state
    When one work unit is selected from ledger status and dependency state alone
    Then either one eligible artifact or fragment work unit is selected, or the circuit returns held when work remains and no unit is eligible, reporting the exact ineligible surface

  @scenario:prove-authoring-work-unit-readiness
  @input:eligible-artifact-authoring-work-unit
  @input-contract:eligible-artifact-authoring-work-unit.v1
  @event:prove-authoring-work-unit-readiness
  @event-authority:prove-authoring-work-unit-readiness.v1
  @outcome:authoring-work-unit-readiness-proof
  @outcome-contract:authoring-work-unit-readiness-proof.v1
  Scenario: Prove the selected work unit is authoring-ready before any model invocation
    Given one eligible artifact or fragment work unit with its current attempt context, its admitted authoring profile, and the admitted preflight rule set
    When the deterministic authorability preflight evaluates authority closure, authorized mutation scope, representation safety, schema round-trip, provider compatibility, work-unit size and depth limits, dependency closure, and repair and retry authority
    Then either the work unit is proven authoring-ready with the readiness proof carrying the exact work unit, its disposition, findings, and lineage, or one exact preflight finding — representation unsafe, schema unsatisfiable, context incomplete, provider incompatible, dependency unresolved, mutation scope divergent, or work unit too broad — is reported and no model invocation is authorized

  @scenario:construct-bounded-authoring-envelope
  @input:authoring-work-unit-readiness-proof
  @input-contract:authoring-work-unit-readiness-proof.v1
  @event:construct-bounded-authoring-envelope
  @event-authority:construct-bounded-authoring-envelope.v1
  @outcome:bounded-authoring-envelope
  @outcome-contract:bounded-authoring-envelope.v1
  Scenario: Construct the bounded authoring envelope for one work unit
    Given one authoring-ready work unit carried by its readiness proof with disposition, findings, and lineage, plus the exact current attempt finding when this construction is a repair or provider-switch attempt
    When one bounded authoring envelope is constructed for exactly one work unit with the smallest legal response schema compiled for that work unit
    Then the envelope carries the exact declared capability, scenario, input, input contract, event, event authority, outcome, and outcome contract identities, the unit meaning, incoming and outgoing obligations, permitted dependencies, provider slot, applicable schemas and vocabulary, already-closed referenced fragments, and the constraint to author only this unit

  @scenario:obtain-authoring-testimony
  @input:bounded-authoring-envelope
  @input-contract:bounded-authoring-envelope.v1
  @event:obtain-authoring-testimony
  @event-authority:obtain-authoring-testimony.v1
  @outcome:governed-authoring-testimony
  @outcome-contract:governed-authoring-testimony.v1
  Scenario: Obtain bounded authoring testimony
    Given one bounded authoring envelope bound to one declared work unit whose schema round-trip and provider compatibility are proven
    When bounded structured testimony is requested for the single selected work unit
    Then one governed response containing bounded structured testimony and its provider lineage is observed as untrusted testimony

  @scenario:prepare-authoring-testimony-for-admission
  @input:authoring-testimony-source
  @input-contract:authoring-testimony-source.v1
  @event:prepare-authoring-testimony-for-admission
  @event-authority:prepare-authoring-testimony-for-admission.v1
  @outcome:authoring-testimony-for-admission
  @outcome-contract:authoring-testimony-for-admission.v1
  Scenario: Prepare the common testimony admission carrier
    Given one governed testimony response or one mechanically repaired testimony with its source identity for one declared work unit
    When the testimony is prepared into the common admission carrier
    Then the admission carrier carries the source kind, source digest, work unit identity, attempt identity, and the applicable provider identity or repair authority, without altering any testimony byte

  @scenario:admit-structured-authoring-testimony
  @input:authoring-testimony-for-admission
  @input-contract:authoring-testimony-for-admission.v1
  @event:admit-structured-authoring-testimony
  @event-authority:admit-structured-authoring-testimony.v1
  @outcome:authoring-testimony-admission-result
  @outcome-contract:authoring-testimony-admission-result.v1
  Scenario: Admit structured authoring testimony
    Given one prepared testimony admission carrier holding either the governed testimony response or the mechanically repaired testimony with its source identity and lineage for one declared work unit
    When every JSON authority fragment is admitted as a nested structured object, every genuinely textual fragment as text content, and every fragment is independently bound to its declared schema
    Then either admitted atomic testimony or exact representation-defect findings carrying the raw testimony digest, work unit identity, and attempt identity are available for classification, never as a platform exception; failed admission produces findings and never admitted authority; no content is repaired or assembled without classification

  @scenario:classify-authoring-testimony
  @input:authoring-testimony-admission-result
  @input-contract:authoring-testimony-admission-result.v1
  @event:classify-authoring-testimony
  @event-authority:classify-authoring-testimony.v1
  @outcome:classified-authoring-findings
  @outcome-contract:classified-authoring-findings.v1
  Scenario: Classify authoring testimony findings
    Given one authoring testimony admission result carrying either admitted atomic testimony or exact representation-defect findings
    When the admission result is classified against the admitted defect classes
    Then findings are classified as conforming, representation defect, schema defect, vocabulary defect, reference defect, local semantic defect, cross-artifact conflict, scope overreach, missing required product, provider failure, or broadly unusable, and the class alone determines what may happen next

  @scenario:establish-conforming-authoring-work-unit
  @input:classified-authoring-findings
  @input-contract:classified-authoring-findings.v1
  @event:establish-conforming-authoring-work-unit
  @event-authority:establish-conforming-authoring-work-unit.v1
  @outcome:conforming-authoring-work-unit
  @outcome-contract:conforming-authoring-work-unit.v1
  Scenario: Establish the conforming authoring work unit
    Given one classified authoring result whose disposition is conforming and which carries the admitted work unit with its admitted fragment digests and lineage
    When the conforming work unit is established as the integration subject
    Then the conforming work unit carries the exact work unit identity, its admitted fragment digests, disposition, and lineage for integration

  @scenario:resolve-mechanical-repair-uniqueness
  @input:classified-authoring-findings
  @input-contract:classified-authoring-findings.v1
  @event:resolve-mechanical-repair-uniqueness
  @event-authority:resolve-mechanical-repair-uniqueness.v1
  @outcome:mechanical-repair-resolution
  @outcome-contract:mechanical-repair-resolution.v1
  Scenario: Resolve mechanical repair uniqueness
    Given classified findings, including admitted representation-defect findings, on one declared work unit
    When the number of authority-preserving mechanical repairs is resolved
    Then mechanical repair is authorized only when exactly one authority-preserving repair exists, zero is reported as not mechanically repairable, and more than one is reported as ambiguous with neither repaired mechanically

  @scenario:apply-unique-mechanical-repair
  @input:mechanical-repair-resolution
  @input-contract:mechanical-repair-resolution.v1
  @event:apply-unique-mechanical-repair
  @event-authority:apply-unique-mechanical-repair.v1
  @outcome:mechanically-repaired-testimony
  @outcome-contract:mechanically-repaired-testimony.v1
  Scenario: Apply the unique mechanical repair
    Given one mechanical repair resolution authorizing exactly one authority-preserving repair on one declared work unit
    When the unique repair is applied to exactly the affected fragment
    Then the repaired testimony is returned for re-admission through the same deterministic admission and classification gate, and no other fragment is altered

  @scenario:integrate-conforming-authoring-work-unit
  @input:conforming-authoring-work-unit
  @input-contract:conforming-authoring-work-unit.v1
  @event:integrate-conforming-authoring-work-unit
  @event-authority:integrate-conforming-authoring-work-unit.v1
  @outcome:artifact-authoring-ledger
  @outcome-contract:artifact-authoring-ledger.v1
  Scenario: Integrate one conforming authoring work unit
    Given one conforming classification result carrying the admitted work unit, its admitted fragment digests, disposition, and lineage
    When the work unit is integrated into the artifact authoring ledger with its admitted fragment digests
    Then the unit is closed, closed work is immutable and is never regenerated without explicit change authority, and every successful attempt reduces the unresolved semantic surface

  @scenario:authorize-authoring-attempt
  @input:classified-authoring-findings
  @input-contract:classified-authoring-findings.v1
  @event:authorize-authoring-attempt
  @event-authority:authorize-authoring-attempt.v1
  @outcome:authorized-authoring-attempt
  @outcome-contract:authorized-authoring-attempt.v1
  @outcome-terminal
  Scenario: Authorize the next authoring attempt from admitted attempt authority
    Given non-conforming classified findings on one declared work unit
    When the admitted attempt authority is applied to the attempt record alone
    Then either one bounded retry, one provider switch, one bounded repair, or terminal rejection is authorized by authority alone, the model never authorizes its own attempt, and every attempt is retained as immutable testimony with its request digest, response digest, and findings

  @scenario:repair-authoring-work-unit
  @input:authorized-authoring-attempt
  @input-contract:authorized-authoring-attempt.v1
  @event:repair-authoring-work-unit
  @event-authority:repair-authoring-work-unit.v1
  @outcome:bounded-authoring-repair-request
  @outcome-contract:bounded-authoring-repair-request.v1
  Scenario: Repair one declared authoring work unit
    Given one authorized bounded repair for one declared work unit
    When one bounded repair request is constructed for exactly the affected fragment
    Then the repair request carries the original immutable testimony, the exact finding, and the exact allowed mutation surface, and closed neighboring authority stays immutable

  @scenario:assemble-canonical-authority-artifacts
  @input:artifact-authoring-ledger
  @input-contract:artifact-authoring-ledger.v1
  @event:assemble-canonical-authority-artifacts
  @event-authority:assemble-canonical-authority-artifacts.v1
  @outcome:projectable-capability-candidate
  @outcome-contract:projectable-capability-candidate.v1
  Scenario: Assemble the canonical authority artifacts
    Given one artifact authoring ledger with every required artifact closed
    When closed atomic testimony is composed by deterministic ordering and identity rules into the canonical declarative artifacts
    Then one self-contained projectable SDA source bundle and accumulated authoring lineage are available for closure proof without altering any admitted fact

  @scenario:prove-candidate-authoring-closure
  @input:projectable-capability-candidate
  @input-contract:projectable-capability-candidate.v1
  @event:prove-candidate-authoring-closure
  @event-authority:prove-candidate-authoring-closure.v1
  @outcome:projectable-capability-authoring-result
  @outcome-contract:projectable-capability-authoring-result.v2
  @outcome-terminal
  Scenario: Prove whole-candidate authoring closure
    Given one assembled projectable capability candidate
    When whole-candidate conformance, blueprint lineage proof, cross-artifact reference proof, and dependency closure are evaluated
    Then the candidate is eligible for independent admission only after every closure proof passes, and a cross-artifact defect reopens only the affected ledger units for bounded repair
