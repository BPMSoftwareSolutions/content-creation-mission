@capability:prove-cross-apply-ui-parity
@root-scenario:prove-cross-apply-ui-parity
# Legacy source: scenario-driven-architecture/tools/src/capabilities/consumer-assurance/prove-cross-apply-ui-parity/provider.ts
Feature: Prove cross-apply UI parity

  A consumer needs to know that choosing one admitted UI framework over
  another never re-authors interface meaning or changes the promised
  experience. The capability compares digest-bound semantic and
  presentation testimony plus native wiring across admitted UI embodiments.

  Every UI embodiment preserves the same authority, shared test vectors,
  semantic and presentation testimony, native wiring, and projected-only
  origin; the same immutable UI authority closes an equivalent experience
  through every admitted embodiment it is proven against. The capability
  does not render or wire any embodiment itself — it only compares
  testimony each embodiment already produced.

  @scenario:prove-cross-apply-ui-parity
  @input:ui-authority-interaction-presentation-and-wiring-facts
  @input-contract:prove-cross-apply-ui-parity-input.v1
  @event:cross-apply-ui-parity-proof-requested
  @event-authority:consumer-cross-apply-ui-parity-proof.v1
  @outcome:cross-apply-ui-parity-known
  @outcome-contract:consumer-ui-parity-evidence.v1
  @outcome-terminal
  Scenario: Compare semantic and presentation testimony across admitted UI embodiments
    Given UI authority, interaction, presentation, and native wiring facts collected across admitted embodiments
    When digest-bound semantic and presentation testimony plus native wiring are compared across those embodiments
    Then every UI embodiment preserves the same authority, vectors, testimony, native wiring, and projected-only origin, with an equivalent experience closed under the same immutable UI authority
