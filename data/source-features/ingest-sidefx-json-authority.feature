@capability:ingest-sidefx-json-authority
@root-scenario:ingest-schema-admitted-json-authority
Feature: Ingest SideFX JSON authority

  A SideFX corpus operator needs declared JSON authority to enter an immutable
  semantic snapshot only when its exact source bytes, classification, schema,
  version, and references can be accounted for. The capability defines the
  source-authority boundary for JSON ingestion and delegates mechanics to the
  admitted profile-governed JSON ingestion platform capability.

  Exact bytes remain the source of record. Canonical JSON is limited to
  derived identity and receipt material, and neither content nor a successful
  parse may elevate evidence or testimony into canonical authority.

  @scenario:ingest-schema-admitted-json-authority
  @input:sidefx-json-authority-ingestion-request
  @input-contract:sidefx-json-authority-ingestion-request.v1
  @event:sidefx-json-authority-ingestion-requested
  @event-authority:sidefx-json-authority-ingestion-profile.v1
  @outcome:sidefx-json-authority-ingestion-receipt
  @outcome-contract:sidefx-json-authority-ingestion-receipt.v1
  @outcome-terminal
  Scenario: Retain exact bytes for schema-admitted JSON authority
    Given connector-selected canonical JSON authority with exact UTF-8 source bytes digest JSON pointer and an admitted declared schema
    When the JSON authority ingestion profile evaluates the declared source
    Then the operational receipt retains the exact bytes digest and pointer and records an admitted schema disposition under the separately bound provider-conformance authority

  @scenario:reject-malformed-or-duplicate-key-json-authority
  @input:sidefx-json-authority-ingestion-receipt
  @input-contract:sidefx-json-authority-ingestion-receipt.v1
  @event:sidefx-json-authority-ingestion-requested
  @event-authority:sidefx-json-malformed-or-duplicate-rejection.v1
  @outcome:sidefx-json-authority-ingestion-receipt
  @outcome-contract:sidefx-json-authority-ingestion-receipt.v1
  @outcome-terminal
  Scenario: Reject malformed JSON and duplicate object keys
    Given connector-selected JSON authority whose exact bytes are malformed or contain a duplicate object key
    When the JSON authority ingestion profile evaluates the declared source
    Then a JSON_PARSE_ERROR or JSON_DUPLICATE_KEY finding rejects that resource without normalization repair or inferred replacement bytes

  @scenario:hold-json-authority-with-missing-declared-schema
  @input:sidefx-json-authority-ingestion-receipt
  @input-contract:sidefx-json-authority-ingestion-receipt.v1
  @event:sidefx-json-authority-ingestion-requested
  @event-authority:sidefx-json-missing-schema-hold.v1
  @outcome:sidefx-json-authority-ingestion-receipt
  @outcome-contract:sidefx-json-authority-ingestion-receipt.v1
  @outcome-terminal
  Scenario: Hold JSON authority whose declared schema is absent
    Given connector-selected JSON authority that declares a schema unavailable from admitted scope
    When the JSON authority ingestion profile evaluates the declared source
    Then JSON_SCHEMA_MISSING is retained as a typed held finding and corpus closure remains open without treating the source as schema-admitted

  @scenario:hold-json-authority-with-unsupported-version-or-dangling-reference
  @input:sidefx-json-authority-ingestion-receipt
  @input-contract:sidefx-json-authority-ingestion-receipt.v1
  @event:sidefx-json-authority-ingestion-requested
  @event-authority:sidefx-json-version-or-reference-hold.v1
  @outcome:sidefx-json-authority-ingestion-receipt
  @outcome-contract:sidefx-json-authority-ingestion-receipt.v1
  @outcome-terminal
  Scenario: Hold JSON authority with an unsupported version or open reference
    Given connector-selected JSON authority with an unsupported declared version or a reference unavailable from admitted scope
    When the JSON authority ingestion profile evaluates the declared source
    Then JSON_VERSION_UNSUPPORTED or JSON_REFERENCE_DANGLING is retained as a typed held finding and no canonical semantic object is derived from the unresolved material

  @scenario:reject-json-source-class-escalation
  @input:sidefx-json-authority-ingestion-receipt
  @input-contract:sidefx-json-authority-ingestion-receipt.v1
  @event:sidefx-json-authority-ingestion-requested
  @event-authority:sidefx-json-source-class-escalation-rejection.v1
  @outcome:sidefx-json-authority-ingestion-receipt
  @outcome-contract:sidefx-json-authority-ingestion-receipt.v1
  @outcome-terminal
  Scenario: Reject content-based escalation from evidence or testimony to authority
    Given JSON classified as admitted evidence projection evidence or model testimony that resembles canonical authority content
    When the JSON authority ingestion profile evaluates the classification and content
    Then JSON_SOURCE_CLASS_MISMATCH rejects the escalation and the original source class remains unchanged

  @scenario:reproduce-json-authority-ingestion-deterministically
  @input:sidefx-json-authority-ingestion-receipt
  @input-contract:sidefx-json-authority-ingestion-receipt.v1
  @event:sidefx-json-authority-ingestion-reproduction-requested
  @event-authority:sidefx-json-authority-ingestion-reproduction.v1
  @outcome:sidefx-json-authority-ingestion-receipt
  @outcome-contract:sidefx-json-authority-ingestion-receipt.v1
  @outcome-terminal
  Scenario: Reproduce a JSON authority ingestion receipt from the same declared manifest
    Given the same declared manifest exact source bytes profile schema family and reference scope on two independent ingestion attempts
    When receipt material is derived under the declared canonicalization policy
    Then source digests pointers findings resource order and receipt digest must match exactly or the ingestion result remains held without a conformance claim
