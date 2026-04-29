from __future__ import annotations

from .common import PoseFrame, TrackingState, calculate_angle, mean_visibility


class BaselineBicepCurlTracker:
    """
    Fixed-threshold baseline similar to a classic webcam rep counter.
    It selects the more visible arm and makes decisions from the raw angle only.
    """

    def __init__(
        self,
        down_threshold: float = 160.0,
        up_threshold: float = 35.0,
        visibility_threshold: float = 0.30,
    ):
        self.down_threshold = down_threshold
        self.up_threshold = up_threshold
        self.visibility_threshold = visibility_threshold
        self.counter = 0
        self.stage = None
        self.active_side = None
        self.active_angle = None
        self.stage_changes = 0
        self.side_switches = 0

    def reset(self):
        self.counter = 0
        self.stage = None
        self.active_side = None
        self.active_angle = None
        self.stage_changes = 0
        self.side_switches = 0

    def _select_side(self, frame: PoseFrame):
        right_vis = mean_visibility(frame.right_shoulder, frame.right_elbow, frame.right_wrist)
        left_vis = mean_visibility(frame.left_shoulder, frame.left_elbow, frame.left_wrist)

        if right_vis < self.visibility_threshold and left_vis < self.visibility_threshold:
            return None, None, max(left_vis, right_vis)

        if right_vis > left_vis:
            angle = calculate_angle(frame.right_shoulder, frame.right_elbow, frame.right_wrist)
            return "right", angle, right_vis

        angle = calculate_angle(frame.left_shoulder, frame.left_elbow, frame.left_wrist)
        return "left", angle, left_vis

    def process(self, frame: PoseFrame) -> TrackingState:
        previous_stage = self.stage
        previous_side = self.active_side

        side, angle, confidence = self._select_side(frame)
        self.active_side = side
        self.active_angle = angle

        if side is not None and previous_side is not None and side != previous_side:
            self.side_switches += 1

        if angle is not None:
            if angle > self.down_threshold:
                self.stage = "down"
            elif angle < self.up_threshold and self.stage == "down":
                self.stage = "up"
                self.counter += 1

        if self.stage != previous_stage and self.stage is not None:
            self.stage_changes += 1

        return TrackingState(
            counter=self.counter,
            stage=self.stage,
            active_side=self.active_side,
            active_angle=self.active_angle,
            confidence=confidence,
        )
