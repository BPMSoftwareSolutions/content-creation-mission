# Episode 1 — YouTube release

Destination: [SideFX @SideFX-b4](https://www.youtube.com/@SideFX-b4).

**Title:** AI Agents Can Act. Who Gives Them Authority? | SideFX Episode 1

Use `episode-01.mp4` (reviewed 1080p edition), `thumbnail.jpg`, `description.txt`, and `captions.srt` or `captions.vtt`. The caption formats contain the same authored timing and text; sentence timing is approximate. `release.json` preserves file hashes, exact sources, chapters, and observed upload state. A null video URL means no upload has been verified.

The audience is engineers, operators, and architects. Category: Education. English. Not made for kids. Disclose altered/synthetic content: the episode uses realistic fictional AI-generated human scenes and synthetic narration. No paid promotion or sponsorship claim has been added. Keep YouTube's copyright and processing results visible before publication.

The first two description lines establish the dilemma. Ten chapter markers come from the authored film timeline, rounded to whole seconds. The landing page contains the same film and a public evidence guide. The site URL must be accessible to viewers before releasing the description that links to it.

`pinned-comment.txt` is ready for the release discussion. Publishing the video does not mean that this comment has been posted. The new wisdom pilot's reserved prompts, answers, and learner records are excluded from all upload and public site assets.

## Complete the release

1. Upload to the confirmed SideFX channel; verify the account before selecting files. Avoid duplicate uploads: inspect channel drafts/content if an attempt has an uncertain outcome.
2. Apply title, description, thumbnail, English captions, audience setting and synthetic-content disclosure. Review processing and copyright results.
3. Publish the video to the public audience requested for this market release; record the actual URL and state in `release.json` only after YouTube confirms it.
4. Update the landing page's discussion link with that verified URL; rebuild its public assets and deploy. Post the prepared discussion comment if authorized.
5. Inspect actual reach, click-through rate, average view duration, retention around the current/target explanation, and substantive comments after release. These are distribution and audience signals, not validated learning outcomes. No automatic monitoring or publishing schedule has been created.

Rebuild the upload assets from the repository root with `.venv/Scripts/python.exe scripts/prepare_youtube_release.py`. This verifies the film against the existing review and all five evidence bindings before copying. Site source lives in the separate `release-site` checkout; publishing it does not publish this repository or the private pilot materials.
