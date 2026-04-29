from __future__ import annotations

import argparse
import csv
from pathlib import Path
import time

import cv2
import mediapipe as mp


ARM_JOINTS = [
    "LEFT_SHOULDER",
    "LEFT_ELBOW",
    "LEFT_WRIST",
    "RIGHT_SHOULDER",
    "RIGHT_ELBOW",
    "RIGHT_WRIST",
]


def build_header() -> list[str]:
    header = ["frame_id", "timestamp_sec"]
    for joint in ARM_JOINTS:
        lower = joint.lower()
        header.extend([f"{lower}_x", f"{lower}_y", f"{lower}_visibility"])
    return header


def extract_row(landmarks, pose_landmark_enum, frame_id: int, start_time: float) -> list[float]:
    row = [frame_id, time.monotonic() - start_time]
    for joint in ARM_JOINTS:
        point = landmarks[getattr(pose_landmark_enum, joint).value]
        row.extend([point.x, point.y, point.visibility])
    return row


def main():
    parser = argparse.ArgumentParser(description="Record a simple arm-landmark mocap CSV from webcam input.")
    parser.add_argument("--output", default="data/mocap/recorded_arm_sequence.csv")
    parser.add_argument("--camera-index", type=int, default=0)
    parser.add_argument("--max-frames", type=int, default=0, help="0 means unlimited until q is pressed.")
    args = parser.parse_args()

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    pose_api = mp.solutions.pose
    drawing = mp.solutions.drawing_utils
    capture = cv2.VideoCapture(args.camera_index)
    if not capture.isOpened():
        raise RuntimeError(f"Unable to open camera index {args.camera_index}")

    pose = pose_api.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(build_header())

        frame_id = 0
        start_time = time.monotonic()

        while True:
            ok, frame = capture.read()
            if not ok:
                break

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = pose.process(rgb)

            if result.pose_landmarks:
                writer.writerow(extract_row(result.pose_landmarks.landmark, pose_api.PoseLandmark, frame_id, start_time))
                drawing.draw_landmarks(frame, result.pose_landmarks, pose_api.POSE_CONNECTIONS)

            cv2.putText(frame, "Press q to stop recording", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 136), 2)
            cv2.imshow("Mocap Recorder", frame)
            frame_id += 1

            if (args.max_frames and frame_id >= args.max_frames) or (cv2.waitKey(1) & 0xFF == ord("q")):
                break

    pose.close()
    capture.release()
    cv2.destroyAllWindows()
    print(f"Saved mocap CSV to {output_path}")


if __name__ == "__main__":
    main()
