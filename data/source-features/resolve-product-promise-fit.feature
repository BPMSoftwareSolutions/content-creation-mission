@capability:resolve-product-promise-fit
@root-scenario:resolve-product-promise-fit
Feature: Resolve one product promise fit snapshot

  Execution testifies. Interpretation evaluates. Governance decides.

  This capability owns the product-level evaluation of the meaning-return
  circuit. Its input is one admitted product promise, its strategic-intent
  binding, one admitted expected capability set, real capability fit
  snapshots, admitted product-capability mappings, one conservative aggregate
  profile, and a bounded evaluation window. Its outcome separates evaluation
  admission from semantic fit. Invalid, incomplete, duplicate, held, stale, or
  identity-divergent input holds evaluation and yields no product fit meaning.
  Valid evaluation yields PRODUCT_REINFORCED, PRODUCT_NOT_REINFORCED,
  PRODUCT_FIT_NOT_OBSERVABLE, or PRODUCT_FIT_NOT_APPLICABLE. The snapshot is
  evidence, not interpretation or decision, and changes nothing.

  @scenario:resolve-product-promise-fit
  @input:product-promise-fit-record
  @input-contract:product-promise-fit-record.v1
  @event:product-promise-fit-resolution-requested
  @event-authority:resolve-product-promise-fit.v1
  @outcome:product-promise-fit-record
  @outcome-contract:product-promise-fit-record.v1
  @outcome-terminal
  Scenario: Resolve one product promise fit snapshot
    Given one admitted product promise, expected capability set, capability fit snapshot set, product-capability mapping set, aggregate profile, and evaluation window
    When product promise fit is resolved
    Then evaluation is PRODUCT_FIT_EVALUATED with one conservative product fit disposition or PRODUCT_FIT_EVALUATION_HELD with no product fit meaning, one replayable snapshot receipt is available, and nothing changes

  @scenario:admit-product-fit-inputs
  @input:product-promise-fit-record
  @input-contract:product-promise-fit-record.v1
  @event:product-fit-input-admission-requested
  @event-authority:admit-product-fit-inputs.v1
  @outcome:product-promise-fit-record
  @outcome-contract:product-promise-fit-record.v1
  @outcome-terminal
  Scenario: Admit the product fit authorities and capability evidence
    Given one product promise and strategic binding, one expected capability set, capability snapshots, mappings, profile, window, and cutoff
    When product fit input admission is evaluated
    Then identities, digests, expected coverage, duplicate absence, mapping admission and effectiveness, and capability snapshot validity are reported without assigning fit meaning to held input

  @scenario:evaluate-product-fit-aggregate
  @input:product-promise-fit-record
  @input-contract:product-promise-fit-record.v1
  @event:product-fit-aggregate-evaluation-requested
  @event-authority:evaluate-product-fit-aggregate.v1
  @outcome:product-promise-fit-record
  @outcome-contract:product-promise-fit-record.v1
  @outcome-terminal
  Scenario: Evaluate the conservative product fit aggregate
    Given one admitted complete capability snapshot vector under one conservative product aggregate profile
    When the product fit aggregate is evaluated
    Then no applicable evidence yields PRODUCT_FIT_NOT_APPLICABLE, counterevidence yields PRODUCT_NOT_REINFORCED, otherwise missing evidence yields PRODUCT_FIT_NOT_OBSERVABLE, and only complete reinforcing evidence yields PRODUCT_REINFORCED

  @scenario:bind-product-fit-snapshot
  @input:product-promise-fit-record
  @input-contract:product-promise-fit-record.v1
  @event:product-fit-snapshot-binding-requested
  @event-authority:bind-product-fit-snapshot.v1
  @outcome:product-promise-fit-record
  @outcome-contract:product-promise-fit-record.v1
  @outcome-terminal
  Scenario: Bind one product fit snapshot
    Given one product fit evaluation with exact authority, capability snapshot, mapping, window, cutoff, and disposition evidence
    When the product fit snapshot is bound
    Then the complete provenance vector binds into one reproducible product fit snapshot digest even when evaluation is held
