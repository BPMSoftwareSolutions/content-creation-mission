@capability:materialize-converged-candidate
@root-scenario:materialize-converged-candidate
Feature: Materialize one converged candidate into a capability workspace

  A converged candidate is bytes in a carrier. A capability is a workspace on disk.
  This capability owns the crossing, and it refuses to cross until the candidate has
  actually converged.

  Materialization is not a write. It is an admission with provenance: every artifact
  is staged, digested, ordered, and mapped from an admitted source root to an admitted
  target root before any byte moves. The governed batch shaper performs the effect;
  this capability establishes that the effect is authorized and reproducible.

  The candidate arrives claiming nothing. It does not claim acceptance, projection, or
  promotion, and materialization does not grant any of them. Materializing a workspace
  proves only that admitted bytes reached an admitted location. Whether the workspace
  projects, proves, or may be promoted remains the decision of the capabilities that
  own those questions.

  The effect boundary is the admitted artifact store: every staged byte lands beneath
  the capability's own binding directory, and a staged path escaping that root is
  refused. Existing materialization is reused where it applies.

  Required fixtures prove the materialization, not a flag. A fixture carries an
  advanced candidate with its complete artifact set; the outcome carries the ordered
  mapping — one entry per declared artifact and the canonical feature — with source
  identity, target identity, copy transformation, and the digest of the staged bytes,
  and the materializer is invoked with that mapping. A fixture carries an unconverged
  candidate; the outcome reports MATERIALIZATION_HELD and the materializer is not
  invoked. A fixture carries a staged path escaping the admitted root; the outcome
  reports OUT_OF_ROOT_STAGING and no byte is written. A fixture carries an artifact
  missing from the mapping; the outcome reports UNMAPPED_STAGED_ARTIFACT.

  @scenario:materialize-converged-candidate
  @input:candidate-materialization-record
  @input-contract:candidate-materialization-record.v1
  @event:candidate-materialization-requested
  @event-authority:materialize-converged-candidate.v1
  @outcome:candidate-materialization-record
  @outcome-contract:candidate-materialization-record.v1
  @outcome-terminal
  Scenario: Materialize one converged candidate into its capability workspace
    Given one converged candidate, its canonical feature, one admitted source root, and one admitted target root
    When the candidate is materialized
    Then every declared artifact is staged and mapped into the target workspace with disposition WORKSPACE_MATERIALIZED, and any unconverged, escaping, or unmapped candidate reports MATERIALIZATION_HELD with the exact holding finding
