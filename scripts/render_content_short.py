"""Render the vertical contract projection for the narration content product."""
import array
import hashlib
import json
import math
import subprocess
import wave
from pathlib import Path

import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "samples/narration-continuity"
W, H, FPS, DURATION = 720, 1280, 24, 30
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
FONT = "C:/Windows/Fonts/segoeui.ttf"
BOLD = "C:/Windows/Fonts/segoeuib.ttf"
WHITE, MUTED, CYAN, AMBER, RED = "#f4f3ee", "#9fb0bc", "#6edfdc", "#edbc77", "#ed8776"


def load_json(path):
    return json.loads(path.read_bytes())


def font(size, bold=False):
    return ImageFont.truetype(BOLD if bold else FONT, size)


def label(draw, xy, value, size=28, color=WHITE, bold=False):
    draw.text(xy, value, font=font(size, bold), fill=color, spacing=8)


def cover(image, size, anchor=0.68):
    ratio = max(size[0] / image.width, size[1] / image.height)
    resized = image.resize((round(image.width * ratio), round(image.height * ratio)), Image.Resampling.LANCZOS)
    left = round((resized.width - size[0]) * anchor)
    top = (resized.height - size[1]) // 2
    return resized.crop((left, top, left + size[0], top + size[1]))


jobs = load_json(OUT / "generation-manifest.json")
receipts = {}
for receipt_path in (ROOT / "outputs/generated").glob("*.json"):
    receipt = load_json(receipt_path)
    if receipt.get("status") == "GENERATED":
        receipts[receipt["jobId"]] = receipt

stills = []
shot_evidence = []
for job in jobs:
    receipt = receipts[job["id"]]
    asset = receipt["images"][0]
    source = ROOT / "outputs/generated" / asset["path"]
    if hashlib.sha256(source.read_bytes()).hexdigest() != asset["sha256"]:
        raise ValueError("IMAGE_DIGEST_MISMATCH")
    stills.append(Image.open(source).convert("RGB"))
    shot_evidence.append({"shot": job["shot"]["id"], "jobId": job["id"], "imageDigest": asset["sha256"]})

demo = load_json(OUT / "demo.receipt.json")
with wave.open(str(OUT / "finished-narration.wav"), "rb") as wav:
    samples = array.array("h", wav.readframes(wav.getnframes()))
peaks = []
for index in range(56):
    part = samples[len(samples) * index // 56:len(samples) * (index + 1) // 56]
    peaks.append(max(0.04, max(abs(value) for value in part) / 32768))

titles = [
    ("HER CUT IS READY.", "The voice provider is not."),
    ("KEEP THE SCRIPT.", "The creative request stays intact."),
    ("CHECK THE ROUTE.", "A unavailable · B text only · C audio"),
    ("MAKE IT REAL.", "Response → file → verified digest"),
    ("NOW SHE CAN HEAR IT.", "A playable narration returns."),
    ("THE PROVIDER CHANGED.", "The story stayed hers."),
]


def render_frame(second):
    scene = min(5, int(second // 5))
    local = (second % 5) / 5
    source = stills[scene]
    # The full-width frame keeps the human action legible; the cropped backdrop supplies vertical depth.
    background = cover(source, (W, H), 0.70).convert("RGBA")
    wash = Image.new("RGBA", (W, H), (3, 12, 20, 174))
    image = Image.alpha_composite(background, wash)
    frame = ImageOps.fit(source, (W - 72, 364), method=Image.Resampling.LANCZOS)
    zoom = 1 + 0.018 * local
    frame = frame.resize((round(frame.width * zoom), round(frame.height * zoom)), Image.Resampling.BICUBIC)
    frame = frame.crop(((frame.width - (W - 72)) // 2, (frame.height - 364) // 2, (frame.width + (W - 72)) // 2, (frame.height + 364) // 2))
    image.alpha_composite(frame.convert("RGBA"), (36, 92))
    layer = Image.new("RGBA", (W, H))
    draw = ImageDraw.Draw(layer)
    draw.rounded_rectangle((35, 91, W - 35, 457), radius=16, outline=(110, 223, 220, 120), width=2)
    label(draw, (36, 32), "S I D E F X", 18, CYAN, True)
    label(draw, (548, 35), "SHORT", 14, MUTED, True)
    label(draw, (40, 518), titles[scene][0], 45, WHITE, True)
    label(draw, (40, 585), titles[scene][1], 25, MUTED)
    if scene == 2:
        y = 710
        states = [("A", "UNAVAILABLE", RED), ("B", "TEXT ONLY", AMBER), ("C", "AUDIO SELECTED", CYAN)]
        for idx, (provider, state, color) in enumerate(states):
            yy = y + idx * 105
            draw.rounded_rectangle((40, yy, 680, yy + 76), radius=12, fill=(10, 28, 39, 230), outline=color, width=2)
            label(draw, (62, yy + 16), provider, 28, color, True)
            label(draw, (118, yy + 20), state, 20, color, True)
    elif scene == 3:
        steps = [("01", "MATERIALIZE"), ("02", "HASH"), ("03", "CONNECT EVIDENCE")]
        for idx, (number, value) in enumerate(steps):
            yy = 704 + idx * 100
            label(draw, (42, yy), number, 18, CYAN, True)
            draw.line((92, yy + 15, 150, yy + 15), fill=CYAN, width=2)
            label(draw, (174, yy - 5), value, 23, WHITE, True)
    elif scene >= 4:
        y = 770
        for idx, peak in enumerate(peaks):
            x = 42 + idx * 11
            height = peak * 92
            draw.line((x, y - height, x, y + height), fill=CYAN, width=5)
        label(draw, (42, 900), f"ACTUAL OUTPUT · {demo['asset']['durationSeconds']:.2f}s", 18, CYAN, True)
        label(draw, (42, 936), demo["asset"]["audioDigest"][:24], 16, MUTED)
    else:
        label(draw, (40, 742), "INPUT", 17, AMBER, True)
        label(draw, (40, 790), "A marked script.\nAn edit waiting.\nNo usable narration.", 31, WHITE)
    phase = ["INPUT", "INPUT", "EVENT", "EVENT", "OUTCOME", "OUTCOME"][scene]
    label(draw, (40, 1183), phase + "  /  HUMAN EXPERIENCE", 15, MUTED, True)
    draw.line((40, 1230, 680, 1230), fill=(102, 140, 152, 80), width=3)
    draw.line((40, 1230, 40 + 640 * second / DURATION, 1230), fill=CYAN, width=4)
    return Image.alpha_composite(image, layer).convert("RGB")


def render():
    silent = OUT / "content-short-silent.mp4"
    command = [FFMPEG, "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
               "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-an", "-c:v", "libx264", "-preset", "fast",
               "-crf", "20", "-pix_fmt", "yuv420p", str(silent)]
    process = subprocess.Popen(command, stdin=subprocess.PIPE)
    for index in range(DURATION * FPS):
        process.stdin.write(render_frame(index / FPS).tobytes())
    process.stdin.close()
    if process.wait():
        raise ValueError("SHORT_RENDER_FAILED")
    output = OUT / "the-story-stays-hers-short.mp4"
    subprocess.run([FFMPEG, "-hide_banner", "-loglevel", "error", "-y", "-i", str(silent),
                    "-i", str(OUT / "short-voiceover.wav"), "-i", str(OUT / "finished-narration.wav"),
                    "-i", str(OUT / "original-bed.wav"), "-filter_complex",
                    "[1:a]apad[v];[2:a]adelay=21500|21500,apad[n];[3:a]volume=0.45[b];[v][n][b]amix=inputs=3:duration=longest:normalize=0,alimiter=limit=0.95[a]",
                    "-map", "0:v", "-map", "[a]", "-t", str(DURATION), "-c:v", "copy", "-c:a", "aac", "-b:a", "160k",
                    "-movflags", "+faststart", str(output)], check=True)
    receipt = {"projection": "short", "contract": "declarations/capability-content/generate-governed-narration.json",
               "format": "720x1280 H264 AAC", "durationSeconds": DURATION, "fps": FPS,
               "actualDemoAudioStartsAtSeconds": 21.5, "shotEvidence": shot_evidence,
               "videoDigest": hashlib.sha256(output.read_bytes()).hexdigest(),
               "scope": "Vertical editorial projection using the same fictional producer, generated short voiceover, and actual local-demo narration."}
    (OUT / "content-short.receipt.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print("SHORT COMPLETE", receipt["videoDigest"])


if __name__ == "__main__":
    render()
