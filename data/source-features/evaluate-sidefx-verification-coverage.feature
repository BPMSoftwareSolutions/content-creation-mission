@capability:evaluate-sidefx-verification-coverage
@root-scenario:evaluate-sidefx-verification-coverage
Feature: Evaluate declared proof obligations into four honest states

  Coverage is where a semantic brain is most tempted to lie. This capability
  recomputes every declared proof obligation from the admitted graph under the
  coverage policy and gives each one exactly one of four dispositions. The
  governing distinction is that evidence attesting corpus membership is not
  evidence that an obligation was verified: an edge derived by a membership
  rule leaves the obligation NOT_OBSERVABLE, and only an edge derived by a
  declared closing rule can make it SATISFIED. Absence never becomes
  NOT_SATISFIED, and NOT_SATISFIED never appears without admitted evidence that
  explicitly fails. Each obligation carries the reason for its state, so a
  reader can tell missing proof from failed proof. If a recomputed disposition
  disagrees with the one the admitted graph declares, that is a reported
  finding and the whole evaluation is rejected, never a silent correction.

  @scenario:evaluate-sidefx-verification-coverage
  @input:sidefx-verification-coverage-request
  @input-contract:sidefx-verification-coverage-request.v1
  @event:sidefx-verification-coverage-requested
  @event-authority:evaluate-sidefx-verification-coverage.v1
  @outcome:sidefx-semantic-verification-coverage
  @outcome-contract:sidefx-semantic-verification-coverage.v1
  @outcome-terminal
  Scenario: Recompute every obligation into exactly one honest disposition
    Given the admitted proof obligations, the relationship graph, the catalog subjects, and the digest-bound coverage policy
    When each obligation is recomputed in policy order against its basis relationships and their derivation rules
    Then every obligation carries one disposition and one reason, missing proof stays NOT_OBSERVABLE, and any disagreement with the declared disposition rejects the evaluation
