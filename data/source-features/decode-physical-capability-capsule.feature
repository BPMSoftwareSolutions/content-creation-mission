@capability:decode-physical-capability-capsule
@root-scenario:decode-physical-capability-capsule
Feature: Decode one physical capability capsule

  Store the capability. Project the explanation. Execute the effect.

  This capability owns the physical admission of a `.sfxcap` capsule.
  Its input is the raw capsule bytes, the declared capsule digest, and
  the capsule format identity. Its outcome is
  PHYSICAL_CAPSULE_DECODED or DECODE_HELD. The bytes decode, the
  recomputed digest must equal the declared digest, the format is the
  admitted capsule pack format, the manifest declares its entries, and
  every entry digest verifies against its embedded bytes. Nothing is
  expanded to disk: decoding is the in-memory bridge between the
  physical capsule and the semantic revelation protocol.

  @scenario:decode-physical-capability-capsule
  @input:physical-capsule-decode-record
  @input-contract:physical-capsule-decode-record.v1
  @event:physical-capsule-decode-requested
  @event-authority:decode-physical-capability-capsule.v1
  @outcome:physical-capsule-decode-record
  @outcome-contract:physical-capsule-decode-record.v1
  @outcome-terminal
  Scenario: Decode one physical capability capsule
    Given one capsule byte sequence, one declared capsule digest, and one capsule format identity
    When the physical capsule is decoded
    Then the capsule is PHYSICAL_CAPSULE_DECODED or DECODE_HELD with the exact holding finding, and a receipt binds the capsule digest, format, and disposition

  @scenario:verify-capsule-bytes-and-format
  @input:physical-capsule-decode-record
  @input-contract:physical-capsule-decode-record.v1
  @event:capsule-bytes-format-verification-requested
  @event-authority:verify-capsule-bytes-and-format.v1
  @outcome:physical-capsule-decode-record
  @outcome-contract:physical-capsule-decode-record.v1
  @outcome-terminal
  Scenario: Verify the capsule bytes and format identity
    Given one capsule byte sequence and one capsule format identity
    When bytes and format verification is evaluated
    Then the bytes are present and the format is the admitted capsule pack format, reporting CAPSULE_BYTES_ABSENT or CAPSULE_FORMAT_UNDECLARED otherwise

  @scenario:verify-capsule-digest
  @input:physical-capsule-decode-record
  @input-contract:physical-capsule-decode-record.v1
  @event:capsule-digest-verification-requested
  @event-authority:verify-capsule-digest.v1
  @outcome:physical-capsule-decode-record
  @outcome-contract:physical-capsule-decode-record.v1
  @outcome-terminal
  Scenario: Verify the capsule digest over the decoded bytes
    Given one capsule byte sequence and one declared capsule digest
    When digest verification is evaluated
    Then the recomputed digest of the decoded bytes equals the declared digest, reporting CAPSULE_DIGEST_DIVERGED otherwise

  @scenario:verify-capsule-manifest-entries
  @input:physical-capsule-decode-record
  @input-contract:physical-capsule-decode-record.v1
  @event:capsule-manifest-entries-verification-requested
  @event-authority:verify-capsule-manifest-entries.v1
  @outcome:physical-capsule-decode-record
  @outcome-contract:physical-capsule-decode-record.v1
  @outcome-terminal
  Scenario: Verify the capsule manifest and entry digests
    Given one decoded capsule manifest with entries and embedded entry bytes
    When manifest and entry verification is evaluated
    Then the manifest declares at least one entry and every entry digest equals the digest of its embedded bytes, reporting CAPSULE_MANIFEST_OPEN or CAPSULE_ENTRY_DIGEST_DIVERGED otherwise

  @scenario:bind-decode-receipt
  @input:physical-capsule-decode-record
  @input-contract:physical-capsule-decode-record.v1
  @event:decode-receipt-binding-requested
  @event-authority:bind-decode-receipt.v1
  @outcome:physical-capsule-decode-record
  @outcome-contract:physical-capsule-decode-record.v1
  @outcome-terminal
  Scenario: Bind one decode receipt
    Given one decode disposition over one physical capsule
    When the decode receipt is bound
    Then the capsule digest, format identity, and disposition bind into one replayable decode receipt
