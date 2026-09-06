"""Layer a finished voiceover onto a native RapidAPI demo screen capture."""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path


def command_output(command: list[str]) -> str:
    return subprocess.run(command, check=True, capture_output=True, text=True).stdout


def has_audio(ffprobe: str, path: Path) -> bool:
    payload = json.loads(
        command_output(
            [
                ffprobe,
                "-v",
                "error",
                "-select_streams",
                "a",
                "-show_entries",
                "stream=index",
                "-of",
                "json",
                str(path),
            ]
        )
    )
    return bool(payload.get("streams"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--screen", type=Path, required=True, help="Native screen recording.")
    parser.add_argument("--voiceover", type=Path, required=True, help="Final WAV voiceover.")
    parser.add_argument("--output", type=Path, required=True, help="Rendered MP4.")
    parser.add_argument(
        "--keep-demo-audio",
        action="store_true",
        help="Retain screen-capture audio quietly beneath the voiceover.",
    )
    args = parser.parse_args()

    for path in (args.screen, args.voiceover):
        if not path.is_file():
            raise FileNotFoundError(path)
    ffmpeg = shutil.which("ffmpeg")
    ffprobe = shutil.which("ffprobe")
    if not ffmpeg or not ffprobe:
        raise RuntimeError("FFMPEG_AND_FFPROBE_REQUIRED")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    screen_has_audio = has_audio(ffprobe, args.screen)
    command = [ffmpeg, "-y", "-i", str(args.screen), "-i", str(args.voiceover)]
    if args.keep_demo_audio and screen_has_audio:
        command += [
            "-filter_complex",
            "[0:a]volume=0.18[demo];[1:a]loudnorm=I=-16:LRA=11:TP=-1.5[voice];"
            "[demo][voice]amix=inputs=2:duration=longest:dropout_transition=2[a]",
            "-map",
            "0:v:0",
            "-map",
            "[a]",
        ]
    else:
        command += [
            "-filter_complex",
            "[1:a]loudnorm=I=-16:LRA=11:TP=-1.5,apad[a]",
            "-map",
            "0:v:0",
            "-map",
            "[a]",
        ]
    command += [
        "-c:v",
        "libx264",
        "-preset",
        "slow",
        "-crf",
        "18",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-ar",
        "48000",
        "-movflags",
        "+faststart",
        "-shortest",
        str(args.output),
    ]
    subprocess.run(command, check=True)
    print(args.output.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
