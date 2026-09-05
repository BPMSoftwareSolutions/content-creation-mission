# Capability Content Contract

Every capability is a content product. Its meaning is authored once in a
`capability-content.v1` contract and projected into media without asking each
surface to reinvent the story.

The contract binds audience, human problem, input/event/outcome experience,
persistent entities, mechanics, claims, exact evidence, emotional arc, permitted
surfaces, and the structure of each projection. Claims distinguish four kinds of
truth:

- `CAPSULE_DECLARATION` records what verified capsule authority declares.
- `OBSERVED_LOCAL_DEMO` records what an inspectable local run produced.
- `EDITORIAL_STAGING` records the fictional human world used to make the experience
  visible.
- `TARGET_DESIGN` records the intended capability experience and architecture.
  It remains visually distinct from present implementation evidence. The gap
  between current proof and the target becomes an engineering improvement brief.

See `docs/EVIDENCE-AND-INTENDED-DESIGN.md` for the cross-surface rule.

An `EDITORIALLY_REVIEWED` contract must have substantive direction and evidence.
A `NEEDS_DIRECTION` contract remains a source-bound inventory record and cannot be
compiled into finished media.

The first complete package permits nine surfaces: video, short, thumbnail, article,
infographic, training, demo, landing page, and evidence story. Each surface names
the claim and evidence IDs it may project. Provider bindings may change; those IDs
keep meaning and proof stable.

`scripts/compile_content_products.py` validates the whole 219-contract estate before
compilation. For reviewed contracts it also resolves every evidence path and checks
its SHA-256 digest. The product manifest at
`outputs/capability-content-products.json` records every emitted surface and digest.
Its v2 `products` mapping binds each capability to its exact contract digest and
nine surface artifacts. Product manifests under `outputs/content-products/` are
rejected if a contract, surface permission, or artifact has changed.

The compiler must fail when a surface invents a claim, references unknown evidence,
uses changed evidence bytes, or appears outside the contract's permission set. A
render is a replaceable realization. The contract is the content authority.
