from __future__ import annotations

from dataclasses import dataclass
import math


@dataclass(frozen=True)
class Joint2D:
    x: float
    y: float
    visibility: float = 1.0


@dataclass(frozen=True)
class PoseFrame:
    left_shoulder: Joint2D
    left_elbow: Joint2D
    left_wrist: Joint2D
    right_shoulder: Joint2D
    right_elbow: Joint2D
    right_wrist: Joint2D


@dataclass
class TrackingState:
    counter: int
    stage: str | None
    active_side: str | None
    active_angle: float | None
    confidence: float


def calculate_angle(a: Joint2D, b: Joint2D, c: Joint2D) -> float:
    radians = math.atan2(c.y - b.y, c.x - b.x) - math.atan2(a.y - b.y, a.x - b.x)
    angle = abs(math.degrees(radians))
    if angle > 180.0:
        angle = 360.0 - angle
    return angle


def mean_visibility(*joints: Joint2D) -> float:
    return sum(j.visibility for j in joints) / len(joints)
