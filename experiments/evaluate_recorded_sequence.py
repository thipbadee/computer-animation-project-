from __future__ import annotations

import argparse
import csv
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.algorithms import BaselineBicepCurlTracker, ProposedBicepCurlTracker
from src.algorithms.common import Joint2D, PoseFrame


def _joint(row: dict[str, str], prefix: str) -> Joint2D:
    return Joint2D(
        x=float(row[f"{prefix}_x"]),
        y=float(row[f"{prefix}_y"]),
        visibility=float(row[f"{prefix}_visibility"]),
    )


def load_pose_frames(csv_path: Path) -> list[PoseFrame]:
    frames: list[PoseFrame] = []
    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            frames.append(
                PoseFrame(
                    left_shoulder=_joint(row, "left_shoulder"),
                    left_elbow=_joint(row, "left_elbow"),
                    left_wrist=_joint(row, "left_wrist"),
                    right_shoulder=_joint(row, "right_shoulder"),
                    right_elbow=_joint(row, "right_elbow"),
                    right_wrist=_joint(row, "right_wrist"),
                )
            )
    return frames


def main():
    parser = argparse.ArgumentParser(description="Evaluate a recorded mocap CSV with baseline and proposed bicep curl trackers.")
    parser.add_argument("csv_path")
    parser.add_argument("--expected-reps", type=int, default=None)
    args = parser.parse_args()

    csv_path = Path(args.csv_path)
    frames = load_pose_frames(csv_path)
    baseline = BaselineBicepCurlTracker()
    proposed = ProposedBicepCurlTracker()

    for frame in frames:
        baseline.process(frame)
        proposed.process(frame)

    print(f"Sequence: {csv_path}")
    print(f"Frames: {len(frames)}")
    print(f"Baseline reps: {baseline.counter} | side switches: {baseline.side_switches}")
    print(f"Proposed reps: {proposed.counter} | side switches: {proposed.side_switches}")
    if args.expected_reps is not None:
        print(f"Baseline count error: {abs(baseline.counter - args.expected_reps)}")
        print(f"Proposed count error: {abs(proposed.counter - args.expected_reps)}")


if __name__ == "__main__":
    main()
