"""Compare RapidAPI demo narration with its script using independent recognition."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from faster_whisper import WhisperModel


ROOT = Path(__file__).resolve().parents[1]
RELEASE = ROOT / "releases" / "rapidapi-assimilation-demo"


def digest(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def words(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+(?:'[a-z0-9]+)?", text.casefold().replace("’", "'"))


def edit_distance(expected: list[str], observed: list[str]) -> int:
    previous = list(range(len(observed) + 1))
    for row, expected_word in enumerate(expected, start=1):
        current = [row]
        for column, observed_word in enumerate(observed, start=1):
            current.append(
                min(
                    current[-1] + 1,
                    previous[column] + 1,
                    previous[column - 1] + (expected_word != observed_word),
                )
            )
        previous = current
    return previous[-1]


def main() -> int:
    manifest_path = RELEASE / "narration-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    model = WhisperModel(
        "base.en",
        device="cpu",
        compute_type="int8",
        cpu_threads=8,
        download_root=str(ROOT / ".tools" / "whisper"),
    )
    reviews = []
    for chapter in manifest["chapters"]:
        audio = RELEASE / "audio" / chapter["audioFile"]
        segments, _ = model.transcribe(
            str(audio),
            language="en",
            word_timestamps=True,
            vad_filter=True,
            condition_on_previous_text=False,
        )
        recognized = " ".join(segment.text.strip() for segment in segments).strip()
        expected_words = words(chapter["script"])
        recognized_words = words(recognized)
        distance = edit_distance(expected_words, recognized_words)
        reviews.append(
            {
                "chapterId": chapter["chapterId"],
                "audioDigest": digest(audio),
                "expectedWordCount": len(expected_words),
                "recognizedWordCount": len(recognized_words),
                "wordEditDistance": distance,
                "wordErrorRate": round(distance / max(1, len(expected_words)), 4),
                "recognizedText": recognized,
            }
        )
        print(f"CHAPTER {chapter['chapterId']} WER {reviews[-1]['wordErrorRate']:.2%}", flush=True)
    output = {
        "reviewType": "INDEPENDENT_BASE_EN_RECOGNITION",
        "method": "faster-whisper base.en recognition compared with the exact voiceover script",
        "humanListeningClaim": False,
        "chapters": reviews,
        "maximumWordErrorRate": max(review["wordErrorRate"] for review in reviews),
        "humanListeningDisposition": "REQUIRED_BEFORE_FINAL_RELEASE",
    }
    (RELEASE / "narration-review.json").write_text(
        json.dumps(output, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
