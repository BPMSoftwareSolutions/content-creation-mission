"""Generate scene-sized RapidAPI demo narration and one combined WAV."""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import re
import urllib.request
import wave
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from generate_gemini import api_key


ROOT = Path(__file__).resolve().parents[1]
RELEASE = ROOT / "releases" / "rapidapi-assimilation-demo"
SCRIPT = RELEASE / "voiceover.md"
AUDIO = RELEASE / "audio"
MODEL = "gemini-2.5-flash-preview-tts"
VOICE = "Kore"
INSTRUCTION = (
    "Read the following exact script in a confident, clear engineering documentary voice "
    "at approximately 140 words per minute. Do not add an introduction or any other words. "
    "Pronounce RapidAPI as Rapid A P I, Agentic as uh-JEN-tick, MCP and SDK as letter names, "
    "and YH as why aitch. The pronunciation guidance is not part of the script.\n"
)


def sha256(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def chapters() -> list[dict[str, str]]:
    text = SCRIPT.read_text(encoding="utf-8")
    matches = list(re.finditer(r"^##\s+(.+?)\s*$", text, re.MULTILINE))
    result: list[dict[str, str]] = []
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        body = " ".join(text[start:end].strip().split())
        if body:
            result.append({"id": f"{index + 1:02}", "title": match.group(1), "text": body})
    if not result:
        raise ValueError("VOICEOVER_CHAPTERS_NOT_FOUND")
    return result


def generate(chapter: dict[str, str], force_chapter: str | None = None) -> dict[str, object]:
    AUDIO.mkdir(parents=True, exist_ok=True)
    request_payload = {
        "contents": [{"parts": [{"text": INSTRUCTION + chapter["text"]}]}],
        "generationConfig": {
            "responseModalities": ["AUDIO"],
            "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": VOICE}}},
        },
    }
    request_bytes = json.dumps(request_payload, separators=(",", ":")).encode("utf-8")
    request_digest = sha256(request_bytes)
    wav_path = AUDIO / f"{chapter['id']}.wav"
    receipt_path = AUDIO / f"{chapter['id']}.receipt.json"
    if chapter["id"] != force_chapter and wav_path.is_file() and receipt_path.is_file():
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        if receipt.get("requestDigest") == request_digest and receipt.get("audioDigest") == sha256(wav_path.read_bytes()):
            return receipt

    request = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent",
        data=request_bytes,
        headers={"Content-Type": "application/json", "x-goog-api-key": api_key()},
    )
    with urllib.request.urlopen(request, timeout=180) as response:
        result = json.load(response)
    parts = result.get("candidates", [{}])[0].get("content", {}).get("parts", [])
    inline = next(
        part["inlineData"]
        for part in parts
        if part.get("inlineData", {}).get("mimeType", "").startswith("audio/")
    )
    if "rate=24000" not in inline["mimeType"]:
        raise ValueError("UNEXPECTED_AUDIO_RATE")
    pcm = base64.b64decode(inline["data"], validate=True)
    if not pcm or len(pcm) % 2:
        raise ValueError("UNUSABLE_AUDIO_PAYLOAD")
    with wave.open(str(wav_path), "wb") as output:
        output.setnchannels(1)
        output.setsampwidth(2)
        output.setframerate(24000)
        output.writeframes(pcm)
    receipt = {
        "chapterId": chapter["id"],
        "title": chapter["title"],
        "script": chapter["text"],
        "scriptDigest": sha256(chapter["text"].encode("utf-8")),
        "requestDigest": request_digest,
        "model": MODEL,
        "voice": VOICE,
        "mimeType": inline["mimeType"],
        "audioFile": wav_path.name,
        "audioDigest": sha256(wav_path.read_bytes()),
        "durationSeconds": round(len(pcm) / 48000, 3),
        "execution": "LIVE_GEMINI_TTS_IN_LOCAL_EDITORIAL_LAB",
        "humanListeningDisposition": "REQUIRED_BEFORE_FINAL_RELEASE",
    }
    receipt_path.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return receipt


def combine(receipts: list[dict[str, object]]) -> dict[str, object]:
    silence = b"\x00\x00" * 12000
    frames: list[bytes] = []
    for index, receipt in enumerate(receipts):
        with wave.open(str(AUDIO / str(receipt["audioFile"])), "rb") as source:
            properties = (source.getnchannels(), source.getsampwidth(), source.getframerate())
            if properties != (1, 2, 24000):
                raise ValueError(f"UNEXPECTED_WAV_PROPERTIES:{properties}")
            frames.append(source.readframes(source.getnframes()))
        if index + 1 < len(receipts):
            frames.append(silence)
    combined = b"".join(frames)
    output_path = RELEASE / "voiceover.wav"
    with wave.open(str(output_path), "wb") as output:
        output.setnchannels(1)
        output.setsampwidth(2)
        output.setframerate(24000)
        output.writeframes(combined)
    return {
        "file": output_path.name,
        "audioDigest": sha256(output_path.read_bytes()),
        "durationSeconds": round(len(combined) / 48000, 3),
        "sampleRate": 24000,
        "channels": 1,
        "sampleWidthBytes": 2,
        "interChapterSilenceSeconds": 0.5,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--force-chapter", choices=[f"{index:02}" for index in range(1, 7)])
    args = parser.parse_args()
    items = chapters()
    if not args.execute:
        print(f"Prepared {len(items)} chapters; pass --execute to synthesize narration.")
        return 0
    if not api_key():
        raise RuntimeError("LOC_GEMINI_API_KEY_UNAVAILABLE")
    with ThreadPoolExecutor(max_workers=2) as pool:
        receipts = list(pool.map(lambda item: generate(item, args.force_chapter), items))
    combined = combine(receipts)
    manifest = {
        "manifestType": "rapidapi-assimilation-demo-narration.v1",
        "scriptRef": "voiceover.md",
        "scriptDigest": sha256(SCRIPT.read_bytes()),
        "syntheticNarration": True,
        "model": MODEL,
        "voice": VOICE,
        "chapters": receipts,
        "combined": combined,
        "humanListeningDisposition": "REQUIRED_BEFORE_FINAL_RELEASE",
    }
    manifest_path = RELEASE / "narration-manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"NARRATION_READY {combined['durationSeconds']}s {combined['audioDigest']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
