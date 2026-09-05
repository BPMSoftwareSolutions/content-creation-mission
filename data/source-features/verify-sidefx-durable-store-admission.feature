@capability:verify-sidefx-durable-store-admission
@root-scenario:verify-sidefx-durable-store-admission
Feature: Verify SideFX durable store admission

  A SideFX semantic authority maintainer needs the durable-store law to be
  admitted by evidence rather than by assertion. The declared store documents
  are ingested through the admitted profile-governed JSON authority ingestion
  platform capability, so schema admission and canonical byte discipline are
  resolved by admitted mechanics and never by a hand-authored instrument.

  Receipt self-digest reproduction is deliberately absent: it requires canonical
  recursive-key-order JSON with member exclusion, which the admitted
  transformation vocabulary cannot express. It is admitted in Phase 1 with the
  canonical-json-byte-validation mechanic, not claimed here.

  Admission of a document is distinct from conformance of a provider. This
  capability observes that the declared law is admitted, internally
  consistent, and refuses what it claims to refuse. It makes no claim about
  any physical store provider.

  @scenario:verify-sidefx-durable-store-admission
  @input:sidefx-durable-store-admission-request
  @input-contract:sidefx-durable-store-admission-request.v1
  @event:sidefx-durable-store-admission-requested
  @event-authority:sidefx-durable-store-admission.v1
  @outcome:sidefx-durable-store-admission-record
  @outcome-contract:sidefx-durable-store-admission-receipt.v1
  @outcome-terminal
  Scenario: Observe one admission disposition for the declared durable-store law
    Given one declared durable-store document set, each document pinned by exact bytes and one declared schema, under the frozen ingestion profile
    When schema admission, canonical byte discipline, and declared agreement are evaluated in profile order
    Then exactly one admission disposition and its ordered findings are retained, without the record becoming a provider conformance claim

  @scenario:admit-declared-store-law-document
  @input:declared-store-law-document-admission
  @input-contract:sidefx-durable-store-admission-receipt.v1
  @event:declared-store-law-document-admission-requested
  @event-authority:sidefx-durable-store-document-admission.v1
  @outcome:declared-store-law-document-admission-record
  @outcome-contract:sidefx-durable-store-admission-receipt.v1
  @outcome-terminal
  Scenario: Admit a declared store document that satisfies its pinned schema
    Given one declared store document whose exact bytes reproduce its pinned source digest and whose content satisfies its pinned schema
    When the document is ingested under the declared schema binding
    Then the document is retained as ADMITTED with its exact bytes and digest, and no admission of any provider is implied

  @scenario:refuse-adversarial-store-contract-case
  @input:adversarial-store-contract-case
  @input-contract:sidefx-durable-store-admission-receipt.v1
  @event:adversarial-store-contract-case-observed
  @event-authority:sidefx-durable-store-adversarial-refusal.v1
  @outcome:adversarial-store-contract-case-record
  @outcome-contract:sidefx-durable-store-admission-receipt.v1
  @outcome-terminal
  Scenario: Refuse an adversarial store contract case with a named diagnostic
    Given one adversarial store document that forges a digest, omits pointer lineage, mints generation identity in a provider, carries credential material, or declares a mutable ledger record
    When the document is ingested under the declared schema binding
    Then the document is REJECTED with its dominant diagnostic named, and the refusal is attributed to the law it violates rather than approximated

  @scenario:agree-across-admitted-store-documents
  @input:admitted-store-document-agreement
  @input-contract:sidefx-durable-store-admission-receipt.v1
  @event:admitted-store-document-agreement-requested
  @event-authority:sidefx-durable-store-document-agreement.v1
  @outcome:admitted-store-document-agreement-record
  @outcome-contract:sidefx-durable-store-admission-receipt.v1
  @outcome-terminal
  Scenario: Require the admitted store documents to agree with one another
    Given the admitted ledger policy, scope authority, authorization authority, result profile, and the retained repository law, each ingested as exact bytes
    When declared agreement is evaluated over the ingested values
    Then the admitted artifact kinds, the declared action surface, every grant scope, the single mutating action, and the pointer key construction agree exactly, and any disagreement is reported as NOT_SATISFIED

  @scenario:report-absent-store-document-not-observable
  @input:absent-store-document-observation
  @input-contract:sidefx-durable-store-admission-receipt.v1
  @event:absent-store-document-observed
  @event-authority:sidefx-durable-store-absence-observation.v1
  @outcome:absent-store-document-observation-record
  @outcome-contract:sidefx-durable-store-admission-receipt.v1
  @outcome-terminal
  Scenario: Report an absent declared document as not observable
    Given one declared store document whose bytes or whose pinned schema cannot be observed
    When the document is evaluated
    Then the document is NOT_OBSERVABLE, no failure is inferred from absence alone, and the absence is never reported as an integrity rejection
