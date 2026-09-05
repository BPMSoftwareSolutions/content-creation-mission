@capability:audit-controlled-tooling-migration-batch
@root-scenario:audit-controlled-tooling-migration-batch
Feature: Audit a controlled tooling migration batch

  A downstream consumer supplies one governed Agentic Harness root and between
  one and five unique capability identities. The capability observes the
  declared migration authority, current inventory, per-capability durable
  promotion evidence, and SDA provider-binding authority through admitted
  repository-observation ports. It returns one stable audit result per supplied
  capability without mutating authority or promoting any candidate.

  A capability passes only when inventory reports PROMOTED, migration authority
  contains the identity, durable evidence reports PROMOTED with VERIFIED
  verification and a zero full-gate exit, Gemini authoring testimony is BOUND
  with exactly one attempt and all declared testimony hashes agree, and the
  active responsibility binding exactly matches the declared projected
  replacement using projected-consumer-runtime-v2. The requested audit set
  must also contain every capability that the current inventory labels
  PROMOTED, so an ungoverned metadata-only promotion cannot remain outside the
  durable evidence audit. Missing, malformed, stale,
  mismatched, duplicated, empty, or over-limit input is retained as attributable
  audit failure evidence.

  The execution authority must transform the requested identities into one
  closed resource declaration, invoke
  `sda-governed-repository-observation-port.v1`, decode every returned
  `exactBytes` value with `base64-decode-utf8`, parse each JSON document with
  `parse-json`, and evaluate the audit conditions through authority-driven
  transformations. A pure transformation port must not stand in for repository
  observation.

  @scenario:audit-controlled-tooling-migration-batch
  @input:controlled-tooling-migration-batch-audit-request
  @input-contract:controlled-tooling-migration-batch-audit-request.v1
  @event:audit-controlled-tooling-migration-batch
  @event-authority:audit-controlled-tooling-migration-batch.v1
  @outcome:controlled-tooling-migration-batch-audit-evidence
  @outcome-contract:controlled-tooling-migration-batch-audit-evidence.v1
  @outcome-terminal
  Scenario: Return bounded migration audit evidence
    Given one governed harness root and one to five unique migration capability identities
    When inventory, migration authority, durable promotion evidence, testimony bindings, and active SDA provider bindings are observed and compared in stable capability identity order
    Then AUDIT_PASSED is returned only when every capability satisfies every declared condition, otherwise AUDIT_FAILED is returned with per-capability attributable failures and no repository mutation
