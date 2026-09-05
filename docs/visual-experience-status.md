# Visual experience projection: execution status

## Current implementation

The external Python content lab is now implemented. See [README](../README.md).
It processes the full capsule manifest using read-only inputs. The latest
machine-readable results are [pipeline report](../evaluations/pipeline-report.json)
and [replay report](../evaluations/replay-report.json). Earlier token and pilot
notes below describe historical work, not the current implementation boundary.

2026-09-05. Source intent: [intent.md](intent.md).

Correction following user review: the content mission is **active**. The earlier
claim that token-provider gaps blocked the mission was too broad. The intent
places the eventual capability family downstream of content experiments; it does
not require a new managed capability before editorial work can begin.

An [eight-scenario editorial collection](../declarations/governed-routing.visual-experiences.v1.json)
and [60-second storyboard](governed-routing-storyboard.md) now cover the complete
`resolve-governed-scenario-route` feature document. They cite its exact file hash
and retain source-scenario locators. This is direct source-based editorial work,
not a SourceFacts inventory, managed retrieval receipt or admitted projection.
No rendered images or films are claimed. The token evidence below remains valid
for the separate automation attempt.

## Delivered token

- Feature: `C:/lab/repos/agentic-harness/features/resolve-scenario-visual-experience.feature`
- Capsule: `C:/lab/repos/agentic-harness/provisioning/resolve-scenario-visual-experience-9930ee80e76af0a9.sfxcap`
- Platform receipt: `C:/lab/repos/agentic-harness/provisioning/resolve-scenario-visual-experience-9930ee80e76af0a9.placement.receipt.json`
- Feature digest: `sha256:721af24109c6377de6af176477c25ed4c7534843dab44f0c0c1cc3b9d6901662`
- Capsule digest, independently checked against file bytes: `sha256:9930ee80e76af0a901fb311671b91744e00254334e3ec4833e2f5a8f3cebfd21`
- Actual state: `PROVISIONED_EXECUTABLE_WITH_OPEN_SLOTS`.
- Structural proof: `PASS`; scenario geometry: `PASS`; capsule entries: 9.
- Exact-token invocation: `terminated`, `PROVIDER_REQUIRED`.

The feature is candidate semantic testimony. The token is not managed or published.
The five open event mechanics are resolution, source qualification, taxonomy
classification, inventory coverage accounting and sequence qualification. No
product provider is bound. Structural validity does not prove these behaviors.

Replay from the Harness root:

```powershell
'{"requestType":"execute-provisioned-capability.v1"}' | npm run --silent capsule:invoke-provisioned -- provisioning/resolve-scenario-visual-experience-9930ee80e76af0a9.sfxcap
```

## Evidence and limits

Harness baseline HEAD was `a9cfe26c326e5e929859e7040e3217d89073bddb`.
Estate manifest SHA-256 was
`0b02db7ee691898d499cb9046737dce3f7c34aa8e1e3d6ca4908afeb823fb802`.
Estate verification reported 219 capabilities, 6,926 entries and no expanded
durable capability root. Dependency resolution reported 70/70 present and zero
external tool roots. These are estate measurements, not scenario counts or a
receipt-bearing semantic inventory.

The inspected `resolve-sidefx-capability-precedents` capsule was
`sha256:3bc141364a196cdce26ed97adf782dae4e57ae671224e1873ef589d886f56ecf`.
Its request schema at
`authority/sidefx-semantic-brain/capabilities/resolve-sidefx-capability-precedents/contracts/sidefx-capability-precedent-request.schema.json`
requires `evaluationBoundary: NON_PRODUCTION_WAVE4_AUTHORING_MEMORY` and fixed
snapshot/index digests. It cannot substantiate a current-estate precedent request.
It was not invoked with fabricated or stale source evidence. This finding is
specific to that inspected boundary; it does not assert that every possible
retrieval capability is absent.

The provisioner emits a `LINEAR_PIPELINE` motif linking all five scenario IDs,
including the hold scenario. That is generated provisional topology, not an
approved success path or a source-supported film sequence. Before functional
execution, the topology must represent source qualification before resolution
and keep holds separate from successful resolution. Generated capsule bytes
must not be hand-edited to repair this.

## Declaration requirements

Each eventual declaration must retain capability and scenario identity, exact
capsule and authority digests, frozen generation, retrieval receipt, and source
locators. Its three experiences contain:

| Experience | Required meaning |
| --- | --- |
| Input | Given state, source-supported actors/environment, visible information |
| Event | When action, perceived change, semantic focus |
| Outcome | Then experience and observable conditions, including rejection or failure when promised |

Every semantic claim needs a source locator. Unspecified actors, environments,
dependencies and semantic altitude remain unresolved. A chosen visual metaphor
is explicitly creative interpretation and cannot manufacture a canonical fact.
Classification records the taxonomy version, candidate families and rationale,
including ambiguous and unclassified results. Rendering style and provider
configuration remain separate from scenario semantics.

The intent's 17 initial candidate families are admission, resolution,
transformation, composition, projection, observation, comparison, validation,
recovery, routing, convergence, rejection, publication, retrieval, extraction,
execution and human approval. They are seed hypotheses, not discovered estate
clusters. No population counts or statistical classifications are claimed.

## Separate automation follow-up

For automated admitted projection, establish a current-generation receipt-bearing scenario inventory and resolve
real providers for the token's five event responsibilities through the admitted
toolchain. Correct provisional topology through its governed producer. Do not
replace these boundaries with ad hoc SourceFacts extraction or hand-authored code.

Once those boundaries close, execute a bounded pilot containing a normal outcome,
a rejection/hold and a source-supported transition. Require claim-level lineage,
separate alternative branches and complete resolved/held coverage before scaling
to the full inventory. Image-provider selection and visual experiments follow
those declarations. The intent's illustrative provider-continuity example is not
evidence of an actual current-estate scenario.

Existing unrelated Harness changes were preserved. This mission directory has no
Git repository; these notes are local artifacts. No commit, push or managed
publication was performed in the token-provisioning lane.
