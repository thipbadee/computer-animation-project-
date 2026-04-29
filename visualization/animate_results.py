from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np

from src.algorithms import (
    BaselineBicepCurlTracker,
    ProposedBicepCurlTracker,
    generate_bicep_curl_sequence,
)


OUTPUT_PATH = Path(__file__).resolve().parents[1] / "demo" / "synthetic_bicep_curl.mp4"


def _to_px(point, width=520, height=360):
    return int(point.x * width), int(point.y * height)


def _draw_arm(panel, frame, side: str, color):
    if side == "left":
        shoulder, elbow, wrist = frame.left_shoulder, frame.left_elbow, frame.left_wrist
    else:
        shoulder, elbow, wrist = frame.right_shoulder, frame.right_elbow, frame.right_wrist

    pts = [_to_px(shoulder), _to_px(elbow), _to_px(wrist)]
    cv2.line(panel, pts[0], pts[1], color, 4)
    cv2.line(panel, pts[1], pts[2], color, 4)
    for pt in pts:
        cv2.circle(panel, pt, 6, color, -1)


def _draw_panel(title, tracker_state, frame, color):
    panel = np.full((360, 520, 3), 245, dtype=np.uint8)
    cv2.putText(panel, title, (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (20, 20, 20), 2)
    if tracker_state.active_side is not None:
        _draw_arm(panel, frame, tracker_state.active_side, color)
    cv2.putText(panel, f"Reps: {tracker_state.counter}", (20, 310), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (30, 30, 30), 2)
    cv2.putText(panel, f"Stage: {tracker_state.stage or '-'}", (20, 340), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (30, 30, 30), 2)
    angle_text = "-" if tracker_state.active_angle is None else f"{tracker_state.active_angle:0.1f}"
    cv2.putText(panel, f"Angle: {angle_text}", (260, 310), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (30, 30, 30), 2)
    cv2.putText(panel, f"Conf: {tracker_state.confidence:0.2f}", (260, 340), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (30, 30, 30), 2)
    return panel


def main():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    sequence = generate_bicep_curl_sequence(num_frames=240, seed=11)
    baseline = BaselineBicepCurlTracker()
    proposed = ProposedBicepCurlTracker()

    writer = cv2.VideoWriter(
        str(OUTPUT_PATH),
        cv2.VideoWriter_fourcc(*"mp4v"),
        24.0,
        (1040, 360),
    )

    for frame in sequence.frames:
        baseline_state = baseline.process(frame)
        proposed_state = proposed.process(frame)
        left = _draw_panel("Baseline", baseline_state, frame, (72, 125, 245))
        right = _draw_panel("Proposed", proposed_state, frame, (0, 180, 120))
        writer.write(np.hstack([left, right]))

    writer.release()
    print(f"Wrote demo animation to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
