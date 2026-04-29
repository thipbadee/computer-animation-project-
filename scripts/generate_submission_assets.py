from __future__ import annotations

from pathlib import Path
import textwrap

import cv2
from PIL import Image, ImageDraw, ImageFont


REPO_ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = REPO_ROOT / "report" / "assets"
DEMO_VIDEO = REPO_ROOT / "demo" / "synthetic_bicep_curl.mp4"
WORKFLOW_PATH = ASSET_DIR / "workflow.png"
DEMO_STRIP_PATH = ASSET_DIR / "demo_strip.png"


def _font(size: int, bold: bool = False):
    candidates = [
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/calibrib.ttf" if bold else "C:/Windows/Fonts/calibri.ttf",
    ]
    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default()


def _wrap_text(draw: ImageDraw.ImageDraw, text: str, font, max_width: int) -> str:
    words = text.split()
    lines: list[str] = []
    current = ""

    for word in words:
        candidate = word if not current else f"{current} {word}"
        bbox = draw.textbbox((0, 0), candidate, font=font)
        if (bbox[2] - bbox[0]) <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word

    if current:
        lines.append(current)

    return "\n".join(lines)


def build_workflow_image():
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    image = Image.new("RGB", (2300, 560), (250, 252, 255))
    draw = ImageDraw.Draw(image)

    title_font = _font(42, bold=True)
    body_font = _font(24, bold=True)
    small_font = _font(21)

    draw.text((55, 25), "System Workflow for Real-Time Exercise Motion Tracking", fill=(20, 20, 20), font=title_font)

    boxes = [
        ("Webcam Input", "Capture RGB frames from a live camera or recorded sequence."),
        ("Pose Estimation", "Infer 2D landmarks using MediaPipe Pose for the visible body joints."),
        ("Baseline / Proposed", "Convert landmarks to joint angles and temporal states for rep tracking."),
        ("Metrics", "Measure runtime, memory, repetition count error, and side-switch jitter."),
        ("Visualization", "Render overlay UI, side-by-side demo, plots, and report figures."),
    ]

    x = 45
    y = 140
    w = 395
    h = 300
    gap = 52
    for index, (heading, description) in enumerate(boxes):
        draw.rounded_rectangle((x, y, x + w, y + h), radius=28, outline=(37, 99, 235), width=4, fill=(230, 240, 255))
        draw.text((x + 24, y + 24), heading, fill=(27, 64, 147), font=body_font)

        wrapped = _wrap_text(draw, description, small_font, max_width=w - 48)
        draw.multiline_text((x + 24, y + 88), wrapped, fill=(40, 40, 40), font=small_font, spacing=10)

        if index < len(boxes) - 1:
            arrow_x = x + w + 12
            center_y = y + h // 2
            draw.line((arrow_x, center_y, arrow_x + gap - 22, center_y), fill=(37, 99, 235), width=8)
            draw.polygon(
                [
                    (arrow_x + gap - 22, center_y),
                    (arrow_x + gap - 52, center_y - 20),
                    (arrow_x + gap - 52, center_y + 20),
                ],
                fill=(37, 99, 235),
            )
        x += w + gap

    image.save(WORKFLOW_PATH)


def build_demo_strip():
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    capture = cv2.VideoCapture(str(DEMO_VIDEO))
    if not capture.isOpened():
        raise RuntimeError(f"Unable to open demo video: {DEMO_VIDEO}")

    frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT)) or 1
    sample_indices = [int(frame_count * ratio) for ratio in (0.10, 0.35, 0.60, 0.85)]
    frames = []

    for index in sample_indices:
        capture.set(cv2.CAP_PROP_POS_FRAMES, index)
        ok, frame = capture.read()
        if not ok:
            continue
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_frame = Image.fromarray(frame).resize((440, 152))
        frames.append(pil_frame)

    capture.release()

    if not frames:
        raise RuntimeError("No frames could be extracted from the demo video.")

    strip = Image.new("RGB", (frames[0].width * len(frames), frames[0].height + 42), (255, 255, 255))
    draw = ImageDraw.Draw(strip)
    title_font = _font(24, bold=True)
    draw.text((20, 10), "Synthetic side-by-side demo frames (baseline vs proposed)", fill=(25, 25, 25), font=title_font)

    x = 0
    for frame in frames:
        strip.paste(frame, (x, 42))
        x += frame.width

    strip.save(DEMO_STRIP_PATH)


def main():
    build_workflow_image()
    build_demo_strip()
    print(f"Wrote {WORKFLOW_PATH}")
    print(f"Wrote {DEMO_STRIP_PATH}")


if __name__ == "__main__":
    main()
