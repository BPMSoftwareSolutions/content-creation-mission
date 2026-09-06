# RapidAPI assimilation live demo

This package records a real, bounded proof of the reusable path:

`saved RapidAPI pages -> deterministic descriptors -> generated MCP tools -> live RapidAPI evidence -> verified Agentic Harness token`

The Python compiler and MCP calls execute in this external editorial lab. The
last stage separately verifies the capsule and estate already pushed to Agentic
Harness. Keep both lane labels visible; the local run does not fill the managed
token's open event-mechanic slot.

## Record the proof

1. Use a 1920x1080 terminal with a large monospace font. Hide notifications and
   any shell profile that prints environment variables.
2. Start a native screen recording. OBS is not installed on the current machine;
   Windows Game Bar or another native recorder is the current operator dependency.
3. From `C:\lab\repos\content-creation-mission`, run:

   ```powershell
   .\.venv\Scripts\python.exe .\scripts\run_rapidapi_assimilation_demo.py --live --pace 3.8
   ```

4. Let every stage remain readable. The script never prints the RapidAPI key or
   response bodies. At the current 60 visible lines, the 3.8-second pace matches
   the generated 3:46 review narration before live-call time. Stop the recording
   after the evidence and transcript paths appear.
5. Record [voiceover.md](voiceover.md) as scene-sized clips or one continuous WAV.
   The package also supports a synthetic review track:

   ```powershell
   .\.venv\Scripts\python.exe .\scripts\narrate_rapidapi_demo.py --execute
   ```

   Synthetic narration remains marked for human listening before release. Keep
   the screen take silent if its command-line sound is not useful.

   Run the independent recognition check after synthesis:

   ```powershell
   .\.venv\Scripts\python.exe .\scripts\review_rapidapi_narration.py
   ```
6. Layer the narration onto the capture:

   ```powershell
   .\.venv\Scripts\python.exe .\scripts\assemble_rapidapi_demo.py `
     --screen .\releases\rapidapi-assimilation-demo\capture.mp4 `
     --voiceover .\releases\rapidapi-assimilation-demo\voiceover.wav `
     --output .\releases\rapidapi-assimilation-demo\rapidapi-assimilation-demo.mp4
   ```

Use `--keep-demo-audio` only when the native take contains useful sound. The
assembler lowers that track, normalizes narration toward -16 LUFS, encodes H.264
with AAC audio, and prepares the MP4 for progressive playback.

## What the viewer should see

| Stage | Visible evidence | Claim boundary |
| --- | --- | --- |
| Input | Five real downloaded pages; runtime credential available; captured values rejected | Restricted captures stay local |
| Determinism | Two byte counts and SHA-256 digests match | Same inputs and pinned compiler environment |
| MCP projection | Four endpoint-specific tools appear | Tool shape comes from partial descriptors |
| Live calls | Yahoo returns current provider evidence; YH returns its current entitlement result | Transport and entitlement, not semantic equivalence |
| Harness | Capsule and feature hashes match the receipt; estate verification passes | Managed token retains one open mechanic slot |
| Verdict | Proven and open claims appear together | No fallback or replacement execution is implied |

`latest-evidence.json` is the machine-readable take receipt. `latest-demo-transcript.txt`
is the exact terminal text from the most recent run. Review both before recording
the final narration because live status, payload identity, and timing can change.

## Capture acceptance

- The whole terminal is legible at normal YouTube playback size.
- No notification, credential value, response body, browser profile, or unrelated
  window appears.
- The displayed compilation digests match each other.
- All four MCP tool names appear.
- Each live call displays its actual status, RapidAPI headers, body size, digest,
  and timing.
- The Harness capsule and feature checks pass, and HEAD matches `origin/main`.
- The narration says one managed mechanic slot remains open.
- The final render plays from start to finish and the narration is intelligible.
