import time

import numpy as np

from .base import Exercise


class HighKnees(Exercise):
    def __init__(self):
        super().__init__()
        self.name = "High Knees"
        self.up_threshold = 0.08
        self.down_threshold = 0.03
        self.min_switch_interval = 0.18
        self.last_switch_time = 0.0
        self.last_up_side = None
        self.awaiting_down = False

    def reset(self):
        super().reset()
        self.last_switch_time = 0.0
        self.last_up_side = None
        self.awaiting_down = False

    def _joint(self, landmarks, joint):
        point = landmarks[getattr(self.mp_pose.PoseLandmark, joint).value]
        return [point.x, point.y, point.visibility]

    def process_landmarks(self, landmarks):
        hip_r = self._joint(landmarks, "RIGHT_HIP")
        knee_r = self._joint(landmarks, "RIGHT_KNEE")
        hip_l = self._joint(landmarks, "LEFT_HIP")
        knee_l = self._joint(landmarks, "LEFT_KNEE")

        left_lift = hip_l[1] - knee_l[1]
        right_lift = hip_r[1] - knee_r[1]
        left_visible = (hip_l[2] + knee_l[2]) / 2 > 0.3
        right_visible = (hip_r[2] + knee_r[2]) / 2 > 0.3

        active_angle = 0.0
        draw_left = False
        draw_right = False
        stage = "reset"

        if left_visible and (not right_visible or left_lift >= right_lift):
            active_angle = left_lift * 1000
            draw_left = True
        elif right_visible:
            active_angle = right_lift * 1000
            draw_right = True

        current_time = time.monotonic()
        left_up = left_visible and left_lift > self.up_threshold and left_lift > right_lift + 0.015
        right_up = right_visible and right_lift > self.up_threshold and right_lift > left_lift + 0.015
        neutral_phase = left_lift < self.down_threshold and right_lift < self.down_threshold

        if neutral_phase:
            self.awaiting_down = False
            stage = "reset"
        elif left_up:
            stage = "left up"
            if (
                self.last_up_side != "left"
                and not self.awaiting_down
                and current_time - self.last_switch_time >= self.min_switch_interval
            ):
                self.counter += 1
                self.last_up_side = "left"
                self.last_switch_time = current_time
                self.awaiting_down = True
        elif right_up:
            stage = "right up"
            if (
                self.last_up_side != "right"
                and not self.awaiting_down
                and current_time - self.last_switch_time >= self.min_switch_interval
            ):
                self.counter += 1
                self.last_up_side = "right"
                self.last_switch_time = current_time
                self.awaiting_down = True
        else:
            stage = "switch"

        max_lift = max(left_lift, right_lift, 0.0)
        per = np.interp(max_lift, (0.0, self.up_threshold), (0, 100))
        per = float(np.clip(per, 0, 100))
        bar = np.interp(per, (0, 100), (400, 150))

        self.stage = stage

        return {
            "active_angle": active_angle,
            "percentage": per,
            "bar_height": bar,
            "stage": self.stage,
            "counter": self.counter,
            "display_label": "STEPS",
            "display_value": str(int(self.counter)),
            "left_elbow": knee_l[:2],
            "right_elbow": knee_r[:2],
            "draw_left": draw_left,
            "draw_right": draw_right,
        }
