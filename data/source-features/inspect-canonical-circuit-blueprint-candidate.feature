@capability:inspect-canonical-circuit-blueprint-candidate
@root-scenario:inspect-canonical-circuit-blueprint-candidate
Feature: Inspect one canonical circuit blueprint candidate

  A blueprint candidate is untrusted testimony. Before it may be projected for
  human review it must survive deterministic inspection that names exactly what
  is wrong rather than reporting a summary adjective.

  Schema validity is not blueprint validity. The carrier contract constrains
  shape and locally decidable field applicability; this capability owns the
  graph-wide obligations that require traversal, plus the declared-field support
  and coverage rules the carrier cannot express.

  A valid monotonic graph is not an adequate design. A candidate can traverse
  cleanly while omitting every case its feature obliges it to represent: no
  rejection route, no hold terminal, no boundary where an effect must cross.
  Coverage is therefore inspected against the obligations the feature and the
  declared design-partition ledger fix, not against the candidate's own
  internal consistency.

  Inspection consumes more than the candidate. The request carries the candidate
  carrier, the exact feature authority the candidate must honor, the admitted
  precedents available at its altitude, and the independently approved
  design-partition ledger. It also carries the exact qualification request for
  qualify-provider-candidate-completeness. Before any design inspection reads
  the request, this capability invokes that exact admitted managed capability
  through its digest-bound application binding and retains the nested execution
  lineage. The returned receipt must bind the candidate's recomputed blueprint
  digest, report CONFORMS or a proven NOT_APPLICABLE with no findings, and prove
  byte-identical replay. A missing qualification request, failed dependency
  invocation, held, digest-divergent, finding-bearing, or replay-divergent
  outcome rejects the request. Every inspection reads that same admitted
  carrier, so no inspection silently acquires a fact the request did not supply,
  and the composed record carries the exact dependency-produced completeness
  receipt and every disposition to the binder rather than leaving the binder to
  re-derive them from the carrier.

  That inspection has one honest limit, and the limit is structural rather than
  incidental. Coverage can be proven only against a partition ledger that was
  declared and approved independently. Semantic edge cases cannot be
  deterministically discovered from prose, so model testimony may propose the
  ledger, but the ledger's completeness is a human review obligation held
  outside this capability, and a ledger arriving without independent approval is
  rejected rather than trusted. A blueprint never defines its own test and then
  passes it.

  Findings are stable identities, not sentences. Each finding names one exact
  code against the exact node, edge, set, field, or obligation it is against, so
  a consumer can act on the code rather than parse prose. Three vocabularies are
  declared by contract and none may be reported outside it: the request
  rejection codes, the coverage obligation codes, and the record rejection
  codes. Rejection is never reported as incompleteness: a ledger that is present
  but unapproved is rejected, not partially accepted.

  Returning evidence is not the same as conforming. An evidence record carrying
  findings means the inspection completed and reported them; only an empty
  finding list reports the candidate as conformant. Findings therefore need no
  terminal route of their own.

  Design coverage proven here, before OPEN, does not establish execution
  coverage. Whether the authored capability actually satisfies every declared
  partition remains the separate runtime obligation of
  verify-capability-scenario-outcomes during PROVE. Both are required and
  neither substitutes for the other.

  This capability does not repair the candidate, upgrade its disposition,
  project any view, obtain review testimony, author, complete, or approve the
  partition ledger, or admit anything. It reports conformance evidence and
  nothing else.

  @scenario:inspect-canonical-circuit-blueprint-candidate
  @input:canonical-blueprint-inspection-request
  @input-contract:canonical-blueprint-inspection-request.v1
  @event:inspect-canonical-circuit-blueprint-candidate
  @event-authority:inspect-canonical-circuit-blueprint-candidate.v1
  @outcome:canonical-blueprint-conformance-evidence
  @outcome-contract:canonical-blueprint-conformance-evidence.v1
  @outcome-terminal
  Scenario: Report exact conformance evidence for one blueprint candidate
    Given one inspection request presenting the candidate, its feature authority, the admitted precedents, the design-partition ledger, and the exact provider-candidate completeness qualification request
    When the request is validated, the digest-bound qualifier capability is invoked, its returned receipt is admitted, and an accepted request is inspected for semantic precedence, cell geometry, declared field support, feature obligation and partition coverage, and observability and service-level coverage
    Then every inspected obligation carries an explicit conformant or exact finding disposition, a rejected request returns its exact rejection code without any inspection reading it, the exact dependency-produced provider-candidate completeness receipt and nested execution lineage are preserved in the evidence, and the candidate disposition is never upgraded

  @scenario:validate-blueprint-inspection-request
  @input:canonical-blueprint-inspection-request
  @input-contract:canonical-blueprint-inspection-request.v1
  @event:validate-blueprint-inspection-request
  @event-authority:validate-blueprint-inspection-request.v1
  @outcome:blueprint-inspection-request-validation
  @outcome-contract:blueprint-inspection-request-validation.v1
  @outcome-variants:INSPECTION_REQUEST_ACCEPTED|INSPECTION_REQUEST_REJECTED
  Scenario: Accept or reject one inspection request before any inspection reads it
    Given one inspection request presenting a candidate carrier, a feature authority, admitted precedents, a design-partition ledger, and one provider-candidate completeness qualification request
    When each presented part is resolved against the exact digests it claims, the ledger's independent approval is verified, the qualification request is bound to the candidate's recomputed blueprint digest, and the exact admitted qualifier capability returns its digest-bound outcome with retained nested execution lineage
    Then an accepted request carries every part and the dependency-produced receipt bound to their exact digests, and a request whose candidate, feature authority, or precedents are absent or digest-divergent, whose ledger is absent or present without independent approval, whose qualification request is missing or candidate-divergent, whose qualifier dependency cannot be resolved exactly, or whose returned receipt is held, digest-divergent, finding-bearing, or replay-divergent is rejected by its exact declared code rather than treated as incomplete, repaired, self-attested, or passed to any design inspection

  @scenario:inspect-semantic-precedence
  @input:canonical-blueprint-inspection-request
  @input-contract:canonical-blueprint-inspection-request.v1
  @event:inspect-semantic-precedence
  @event-authority:inspect-semantic-precedence.v1
  @outcome:semantic-precedence-disposition
  @outcome-contract:blueprint-inspection-disposition.v1
  Scenario: Reject absent, ambiguous, or undeclared-cyclic semantic precedence
    Given one inspection request whose candidate declares semantic precedence and presentation ordinals
    When the required partial order is resolved and every cycle is compared with the declared bounded returns
    Then absent, ambiguous, or undeclared-cyclic precedence is a finding, independent siblings are not required to carry an arbitrary total order, and a presentation ordinal is never accepted as execution precedence

  @scenario:inspect-altitude-appropriate-cell-geometry
  @input:canonical-blueprint-inspection-request
  @input-contract:canonical-blueprint-inspection-request.v1
  @event:inspect-altitude-appropriate-cell-geometry
  @event-authority:inspect-altitude-appropriate-cell-geometry.v1
  @outcome:cell-geometry-disposition
  @outcome-contract:blueprint-inspection-disposition.v1
  Scenario: Reject missing or altitude-inappropriate cell geometry
    Given one inspection request whose candidate nodes declare their kind and altitude
    When each cell's three declared positions are inspected against its altitude
    Then a missing position is a finding, and a lower-altitude cell that claims a promised experience it cannot own is a finding

  @scenario:inspect-declared-field-support
  @input:canonical-blueprint-inspection-request
  @input-contract:canonical-blueprint-inspection-request.v1
  @event:inspect-declared-field-support
  @event-authority:inspect-declared-field-support.v1
  @outcome:declared-field-disposition
  @outcome-contract:blueprint-inspection-disposition.v1
  Scenario: Reject a declared field the active circuit cannot consume
    Given one inspection request whose candidate declares structural, observability, and service-level fields
    When each declared field is resolved against the decisions the active circuit can actually consume
    Then an unsupported field, an authority drift, and a duplicate ownership of an upstream fact are each findings, and no declared field is ignored as decorative or prompt-only context

  @scenario:inspect-feature-obligation-and-partition-coverage
  @input:canonical-blueprint-inspection-request
  @input-contract:canonical-blueprint-inspection-request.v1
  @event:inspect-feature-obligation-and-partition-coverage
  @event-authority:inspect-feature-obligation-and-partition-coverage.v1
  @outcome:coverage-obligation-disposition
  @outcome-contract:blueprint-inspection-disposition.v1
  Scenario: Reject a candidate that omits an obligation its feature and partition ledger declare
    Given one inspection request carrying exact feature and candidate digests, the admitted precedents, and the approved partition ledger naming required outcomes, rejection and hold cases, contract boundaries, effect boundaries, and proof obligations
    When every declared obligation is resolved against the nodes, routes, variants, terminals, provider slots, and contracts the candidate actually declares
    Then a feature scenario no cell preserves is FEATURE_SCENARIO_UNMAPPED, a declared outcome no route reaches is DECLARED_OUTCOME_UNROUTED, a rejection or hold case the circuit cannot represent is REJECTION_PATH_UNREPRESENTED, a required effect boundary crossing no provider slot is REQUIRED_EFFECT_BOUNDARY_UNMAPPED, a contract boundary no cell declares is CONTRACT_BOUNDARY_UNMAPPED, a proof obligation bound to no partition is PROOF_PARTITION_UNBOUND, and a blueprint claim the feature does not support is BLUEPRINT_CLAIM_UNSUPPORTED_BY_FEATURE, each named against the exact obligation and the artifact that omits it, and a candidate that is a valid monotonic graph is never reported conformant merely because it traverses cleanly

  @scenario:inspect-observability-and-service-level-coverage
  @input:canonical-blueprint-inspection-request
  @input-contract:canonical-blueprint-inspection-request.v1
  @event:inspect-observability-and-service-level-coverage
  @event-authority:inspect-observability-and-service-level-coverage.v1
  @outcome:coverage-disposition
  @outcome-contract:blueprint-inspection-disposition.v1
  Scenario: Reject incomplete observability or invalid service-level binding
    Given one inspection request whose candidate declares executable cells, indicators, objectives, and boundaries
    When observability coverage and every indicator, objective, and boundary binding are inspected
    Then an executable cell without sufficient observability authority, an indicator derived from non-admitted testimony, an objective without an exact target and window, an inferred child allocation, and a boundary without a declared service boundary are each findings

  @scenario:bind-blueprint-conformance-disposition
  @input:blueprint-inspection-record
  @input-contract:blueprint-inspection-record.v1
  @event:bind-blueprint-conformance-disposition
  @event-authority:bind-blueprint-conformance-disposition.v1
  @outcome:canonical-blueprint-conformance-evidence
  @outcome-contract:canonical-blueprint-conformance-evidence.v1
  Scenario: Bind every inspected obligation to one exact disposition
    Given one inspection record carrying the candidate digest, the exact dependency-produced provider-candidate completeness receipt and nested execution lineage, and the semantic precedence, cell geometry, declared field, obligation and partition coverage, and observability and service-level dispositions produced for it
    When the dispositions are composed into conformance evidence bound to that candidate digest
    Then the evidence preserves that exact completeness receipt and nested execution lineage, names each finding by its declared code against the exact node, edge, set, field, or obligation it is against, marks every design inspection NOT_INSPECTED when request validation or qualifier admission rejects the request, rejects a record missing or contradicting any declared accepted-request disposition by its exact declared code rather than composing a subset, reports findings as completed inspection evidence rather than candidate conformance, and reports an empty finding list as conformant without claiming review or admission
