from __future__ import annotations

from dataclasses import dataclass
import math
import random

from .common import Joint2D, PoseFrame


@dataclass(frozen=True)
class SyntheticSequence:
    frames: list[PoseFrame]
    expected_reps: int
    ground_truth_angles: list[float]


def _build_arm(anchor_x: float, mirror: int, angle_deg: float, visibility: float):
    shoulder = Joint2D(anchor_x, 0.34, visibility)
    elbow = Joint2D(anchor_x, 0.54, visibility)
    theta = math.radians(angle_deg)
    forearm_length = 0.18
    wrist = Joint2D(
        elbow.x + (mirror * math.sin(theta) * forearm_length),
        elbow.y - (math.cos(theta) * forearm_length),
        visibility,
    )
    return shoulder, elbow, wrist


def generate_bicep_curl_sequence(
    num_frames: int,
    frames_per_rep: int = 50,
    noise_std_deg: float = 6.0,
    seed: int = 7,
) -> SyntheticSequence:
    rng = random.Random(seed)
    cycles = max(1, num_frames // frames_per_rep)
    frames = []
    angles = []

    for frame_idx in range(num_frames):
        phase = (2.0 * math.pi * frame_idx) / frames_per_rep
        clean_angle = 100.0 + 70.0 * math.cos(phase)
        noisy_angle = max(20.0, min(175.0, clean_angle + rng.gauss(0.0, noise_std_deg)))

        left_visibility = 0.85
        right_visibility = 0.85

        if (frame_idx // 30) % 2 == 0:
            left_visibility = 0.95
            right_visibility = 0.42
        else:
            left_visibility = 0.42
            right_visibility = 0.95

        if frame_idx % 120 in range(90, 100):
            left_visibility *= 0.18
        if frame_idx % 150 in range(65, 78):
            right_visibility *= 0.18

        left_arm = _build_arm(0.38, -1, noisy_angle, left_visibility)
        right_arm = _build_arm(0.62, 1, noisy_angle + rng.gauss(0.0, 2.0), right_visibility)
        frames.append(
            PoseFrame(
                left_shoulder=left_arm[0],
                left_elbow=left_arm[1],
                left_wrist=left_arm[2],
                right_shoulder=right_arm[0],
                right_elbow=right_arm[1],
                right_wrist=right_arm[2],
            )
        )
        angles.append(clean_angle)

    return SyntheticSequence(
        frames=frames,
        expected_reps=cycles,
        ground_truth_angles=angles,
    )
