from __future__ import annotations

from .baseline import BaselineBicepCurlTracker
from .common import PoseFrame, TrackingState, calculate_angle, mean_visibility
from src.data_structures import ExponentialAngleFilter


class ProposedBicepCurlTracker(BaselineBicepCurlTracker):
    """
    Proposed method:
    - confidence-aware side selection
    - short-term side lock to prevent arm flapping
    - temporal smoothing on the elbow angle
    - wider hysteresis for more stable stage transitions
    """

    def __init__(
        self,
        down_threshold: float = 150.0,
        up_threshold: float = 50.0,
        visibility_threshold: float = 0.25,
        side_lock_frames: int = 18,
        smoothing_alpha: float = 0.28,
    ):
        super().__init__(
            down_threshold=down_threshold,
            up_threshold=up_threshold,
            visibility_threshold=visibility_threshold,
        )
        self.side_lock_frames = side_lock_frames
        self.filter = ExponentialAngleFilter(alpha=smoothing_alpha)
        self.locked_side = None
        self.lock_frames_left = 0

    def reset(self):
        super().reset()
        self.filter.reset()
        self.locked_side = None
        self.lock_frames_left = 0

    def _arm_score(self, shoulder, elbow, wrist):
        visibility = mean_visibility(shoulder, elbow, wrist)
        angle = calculate_angle(shoulder, elbow, wrist)
        centered_bonus = 1.0 - min(abs(elbow.x - 0.5) * 1.5, 1.0)
        return angle, (visibility * 0.75) + (centered_bonus * 0.25), visibility

    def _score_side(self, frame: PoseFrame, side: str):
        if side == "left":
            return self._arm_score(frame.left_shoulder, frame.left_elbow, frame.left_wrist)
        return self._arm_score(frame.right_shoulder, frame.right_elbow, frame.right_wrist)

    def _select_side(self, frame: PoseFrame):
        if self.locked_side in {"left", "right"} and self.lock_frames_left > 0:
            locked_angle, _, locked_vis = self._score_side(frame, self.locked_side)
            if locked_vis >= self.visibility_threshold:
                self.lock_frames_left -= 1
                return self.locked_side, locked_angle, locked_vis

        left_angle, left_score, left_vis = self._score_side(frame, "left")
        right_angle, right_score, right_vis = self._score_side(frame, "right")

        if left_vis < self.visibility_threshold and right_vis < self.visibility_threshold:
            return self.locked_side, None, max(left_vis, right_vis)

        if right_score > left_score + 0.05:
            self.locked_side = "right"
            self.lock_frames_left = self.side_lock_frames
            return "right", right_angle, right_vis

        self.locked_side = "left"
        self.lock_frames_left = self.side_lock_frames
        return "left", left_angle, left_vis

    def process(self, frame: PoseFrame) -> TrackingState:
        previous_stage = self.stage
        previous_side = self.active_side

        side, raw_angle, confidence = self._select_side(frame)
        filtered_angle = self.filter.update(raw_angle)

        self.active_side = side
        self.active_angle = filtered_angle

        if side is not None and previous_side is not None and side != previous_side:
            self.side_switches += 1

        if filtered_angle is not None:
            if filtered_angle >= self.down_threshold:
                self.stage = "down"
            elif filtered_angle <= self.up_threshold and self.stage == "down":
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
