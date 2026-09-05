@capability:verify-sidefx-evidence-ledger-integrity
@root-scenario:verify-sidefx-evidence-ledger-integrity
Feature: Verify SideFX evidence ledger integrity

  The evidence ledger is append-only and digest-addressed. Verification
  re-checks a stored receipt by its exact digest, distinguishes absence
  from integrity failure, traverses the wave receipt chain by source and
  receipt digests, and reports generation gaps without inferring failure.
  A digest that fails to recompute is INTEGRITY_REJECTED evidence of a
  false integrity claim; it is never reported as absence. Every scenario
  admits and emits one shared ledger verification record.

  @scenario:verify-sidefx-evidence-ledger-integrity
  @input:sidefx-ledger-integrity-verification-record
  @input-contract:sidefx-ledger-integrity-verification-record.v1
  @event:sidefx-ledger-integrity-verification-requested
  @event-authority:verify-sidefx-evidence-ledger-integrity.v1
  @outcome:sidefx-ledger-integrity-verification-record
  @outcome-contract:sidefx-ledger-integrity-verification-record.v1
  @outcome-terminal
  Scenario: Verify one stored receipt by digest with a three-way disposition
    Given one receipt digest and the declared ledger policy
    When the stored receipt is re-verified
    Then the disposition is exactly one of VERIFIED, INTEGRITY_REJECTED, or NOT_OBSERVABLE, and absence is never reported as integrity failure

  @scenario:traverse-sidefx-receipt-chain-by-digest
  @input:sidefx-ledger-integrity-verification-record
  @input-contract:sidefx-ledger-integrity-verification-record.v1
  @event:sidefx-receipt-chain-traversal-requested
  @event-authority:traverse-sidefx-receipt-chain.v1
  @outcome:sidefx-ledger-integrity-verification-record
  @outcome-contract:sidefx-ledger-integrity-verification-record.v1
  @outcome-terminal
  Scenario: Traverse the receipt chain by source and receipt digests
    Given one admitted receipt whose predecessor bindings are declared
    When the chain is traversed through the ledger
    Then every link verifies by its own digest or the traversal stops with a typed disposition naming the first failing link

  @scenario:report-ledger-generation-gap-without-inferring-failure
  @input:sidefx-ledger-integrity-verification-record
  @input-contract:sidefx-ledger-integrity-verification-record.v1
  @event:sidefx-ledger-generation-gap-observed
  @event-authority:report-sidefx-ledger-generation-gap.v1
  @outcome:sidefx-ledger-integrity-verification-record
  @outcome-contract:sidefx-ledger-integrity-verification-record.v1
  @outcome-terminal
  Scenario: Report a generation gap as an observation, never a failure
    Given ledger records whose generation chain has a gap
    When ledger integrity is verified
    Then the gap is reported as a typed finding and no later record is marked failed because of it
