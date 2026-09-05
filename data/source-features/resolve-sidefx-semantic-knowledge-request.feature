@capability:resolve-sidefx-semantic-knowledge-request
@root-scenario:resolve-sidefx-semantic-knowledge-request
Feature: Resolve one semantic knowledge request end to end

  This is the read-only root of the SideFX brain. It owns no semantics of its
  own. It composes the admitted planning, optional deterministic vector-index,
  retrieval, grounding, and receipt capabilities in governed order under pinned
  binding and authority digests. The vector provider is invoked only when the
  plan enables its channel, and its complete provider/model/input/index/record
  testimony survives into both the candidate set and replay receipt. When the
  plan is rejected, vector indexing, retrieval, and grounding are skipped rather
  than run against an invalid plan, and the request still exits with a receipt
  that records QUERY_REJECTED. Every exit therefore carries a replayable
  receipt, whether the brain answered or abstained. No model provider or
  handwritten consumer runtime participates in any step.

  @scenario:resolve-sidefx-semantic-knowledge-request
  @input:sidefx-semantic-knowledge-request
  @input-contract:sidefx-semantic-knowledge-request.v1
  @event:sidefx-semantic-knowledge-requested
  @event-authority:resolve-sidefx-semantic-knowledge-request.v1
  @outcome:sidefx-semantic-knowledge-outcome
  @outcome-contract:sidefx-semantic-knowledge-outcome.v1
  @outcome-terminal
  Scenario: Compose planning, retrieval, grounding, and receipt into one answer
    Given one typed knowledge request, the pinned corpus generation, and the admitted query policy allowances
    When planning, optional vector recall, retrieval, grounding, and receipt binding run in governed order under pinned binding digests
    Then one grounded answer or typed abstention is returned with a replayable receipt and no model invocation
