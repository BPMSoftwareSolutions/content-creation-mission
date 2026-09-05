# Gemini generation strategy

Provider documentation checked 2026-09-05:
[Google image-generation guide](https://ai.google.dev/gemini-api/docs/generate-content/image-generation).
It lists `gemini-3.1-flash-image` for general work and `gemini-3-pro-image`
for demanding visual tasks. Recipes choose the former for triptychs, square
posts and vertical drafts, and the latter for covers, heroes and infographics.
Model availability is account-dependent and can change; override it explicitly.

The runner uses REST generateContent with text/image response modalities and
imageConfig.aspectRatio. Live generation now succeeds for the eight-scenario
pilot using gemini-3-pro-image, confirmed through the authenticated model list.

Review a small family-stratified sample first. Select one concrete Examples row
for an outline and one branch for a final image; preserve all alternatives in
the durable spec. Retain the unmodified source spec beside reviewed refinements.
Begin with one request, compare its result with every outcome constraint, then
increase the bounded limit. Grouped JSONL files are preparation artifacts; they
are not automatically submitted to Google's asynchronous Batch service.

Use an approved style reference consistently across related scenes. The current
runner accepts local PNG/JPEG references with --reference; multi-turn editing
remains a future extension. Preserve reference file hashes and
permission information when adding inlineData parts. Never let a style reference
replace the source semantics. Brand profile remains proposed until supplied.

HTTP 429 and selected 5xx errors retry at most three times after the first
attempt. Authentication, invalid payloads, no-image results and uncertain network
outcomes stop for diagnosis. There is no automatic model substitution. Resume
skips only outputs whose saved image hashes still match.

Evaluate source fidelity, negative constraints, separation of alternatives,
legible labels, aspect ratio, consistent object identities and usable composition.
Reject any image that depicts an unauthorized effect, invents source facts or
turns a pending outcome into success. Structural preparation checks are automatic;
semantic and visual review is human work until an evaluator is separately proven.
