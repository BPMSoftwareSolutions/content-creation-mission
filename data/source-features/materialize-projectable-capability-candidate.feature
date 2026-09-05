@capability:materialize-projectable-capability-candidate
@root-scenario:materialize-projectable-capability-candidate
Feature: Materialize one admitted projectable capability candidate

  A downstream authoring circuit has already admitted one canonical feature
  and the complete bounded set of eleven companion SDA source artifacts. The
  candidate contents, logical names, byte digests, semantic identities, and
  destination policy are immutable before publication begins.

  Publication invokes the governed SDA capability
  `shape-governed-file-system-batch` with one bounded source root and one fresh
  destination root. That capability resolves the complete mapping set before
  mutation, rejects any existing target, verifies every declared source-byte
  digest and copied target hash, and writes the workspace authority last as the
  commit marker. No provider-workspace or FS Shaper checkout participates. An
  interrupted publication therefore cannot present a partial fresh destination
  as source-admissible.

  This capability does not author or repair candidate content and cannot claim
  source admission, projection, behavioral acceptance, or promotion. It only
  materializes the unchanged admitted bundle through the governed SDA shaping
  capability and reports the observed paths, hashes, and nested execution
  lineage. Executable source remains the responsibility of ordinary SDA
  projection after publication.

  @scenario:materialize-projectable-capability-candidate
  @input:admitted-projectable-capability-candidate
  @input-contract:admitted-projectable-capability-candidate.v1
  @event:materialize-projectable-capability-candidate
  @event-authority:materialize-projectable-capability-candidate.v1
  @outcome:materialized-projectable-capability-candidate
  @outcome-contract:materialized-projectable-capability-candidate.v1
  @outcome-terminal
  Scenario: Publish one complete candidate to a fresh governed destination
    Given one admitted canonical feature and exactly eleven immutable companion artifacts with fixed logical names and byte digests
    When `shape-governed-file-system-batch` authorizes the complete fresh-destination shape, verifies every declared source-byte digest and copied target hash, and publishes the final workspace authority last
    Then one complete digest-bearing candidate workspace is observable with publication lineage and no claim of admission, projection, acceptance, or promotion
