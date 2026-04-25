import time
import numpy as np

from .base import Exercise
from .utils import calculate_angle


class Plank(Exercise):
    def __init__(self):
        super().__init__()
        self.name = "Plank"
        self.hold_start_time = None
        self.elapsed_time = 0.0
        self.last_valid_time = None

    def reset(self):
        super().reset()
        self.hold_start_time = None
        self.elapsed_time = 0.0
        self.last_valid_time = None

    def _joint(self, landmarks, joint):
        point = landmarks[getattr(self.mp_pose.PoseLandmark, joint).value]
        return [point.x, point.y, point.visibility]

    def process_landmarks(self, landmarks):
        shoulder_r = self._joint(landmarks, "RIGHT_SHOULDER")
        elbow_r = self._joint(landmarks, "RIGHT_ELBOW")
        hip_r = self._joint(landmarks, "RIGHT_HIP")
        ankle_r = self._joint(landmarks, "RIGHT_ANKLE")

        shoulder_l = self._joint(landmarks, "LEFT_SHOULDER")
        elbow_l = self._joint(landmarks, "LEFT_ELBOW")
        hip_l = self._joint(landmarks, "LEFT_HIP")
        ankle_l = self._joint(landmarks, "LEFT_ANKLE")

        vis_r = (shoulder_r[2] + elbow_r[2] + hip_r[2] + ankle_r[2]) / 4
        vis_l = (shoulder_l[2] + elbow_l[2] + hip_l[2] + ankle_l[2]) / 4

        active_shoulder = shoulder_l
        active_elbow = elbow_l
        active_hip = hip_l
        active_ankle = ankle_l
        draw_l = True
        draw_r = False

        if vis_r > vis_l and vis_r > 0.25:
            active_shoulder = shoulder_r
            active_elbow = elbow_r
            active_hip = hip_r
            active_ankle = ankle_r
            draw_l = False
            draw_r = True
        elif vis_l < 0.25 and vis_r < 0.25:
            draw_l = False
            draw_r = False

        spine_angle = calculate_angle(
            active_shoulder[:2],
            active_hip[:2],
            active_ankle[:2]
        )

        support_angle = calculate_angle(
            active_shoulder[:2],
            active_elbow[:2],
            active_hip[:2]
        )

        shoulder_stack = abs(active_shoulder[0] - active_elbow[0])

        # เพิ่มตัวนี้: เช็กว่าลำตัวไหล่-สะโพกขนานพื้นไหม
        torso_y_diff = abs(active_shoulder[1] - active_hip[1])
        torso_x_diff = abs(active_shoulder[0] - active_hip[0])
        torso_slope = torso_y_diff / max(torso_x_diff, 0.001)

        spine_error = abs(180 - spine_angle)
        support_error = abs(90 - support_angle)
        stack_error = min(shoulder_stack / 0.20, 1.0) * 100
        torso_error = min(torso_slope / 0.35, 1.0) * 100

        posture_error = min(
            (spine_error * 1.5) +
            (support_error * 0.5) +
            (stack_error * 0.4) +
            (torso_error * 0.7),
            100
        )

        posture_score = float(np.clip(100 - posture_error, 0, 100))

        # รูป 2 จะเข้าเงื่อนไขนี้ เพราะลำตัวชัน / ยกอกสูงเกิน
        is_chest_lifted = torso_slope > 0.38 or torso_y_diff > 0.13

        is_collapsed = (
            spine_error > 45 or
            shoulder_stack > 0.30 or
            is_chest_lifted
        )

        valid_posture = (
            spine_error < 35 and
            support_error < 90 and
            shoulder_stack < 0.24 and
            torso_slope < 0.38 and
            torso_y_diff < 0.13 and
            max(vis_l, vis_r) > 0.25
        )

        now = time.monotonic()

        if valid_posture:
            if self.hold_start_time is None:
                self.hold_start_time = now - self.elapsed_time

            self.last_valid_time = now
            self.elapsed_time = now - self.hold_start_time
            self.counter = self.elapsed_time
            self.stage = "hold"

        else:
            if is_collapsed:
                self.hold_start_time = None
                self.elapsed_time = 0.0
                self.counter = 0.0
                self.stage = "adjust"

            elif self.last_valid_time is not None and now - self.last_valid_time < 0.5:
                self.counter = self.elapsed_time
                self.stage = "hold"

            else:
                self.hold_start_time = None
                self.elapsed_time = 0.0
                self.counter = 0.0
                self.stage = "adjust"

        return {
            "active_angle": spine_angle,
            "percentage": posture_score,
            "bar_height": np.interp(posture_score, (0, 100), (400, 150)),
            "stage": self.stage,
            "counter": self.counter,
            "display_label": "TIME",
            "display_value": f"{self.counter:0.1f}s",
            "left_elbow": elbow_l[:2],
            "right_elbow": elbow_r[:2],
            "draw_left": draw_l,
            "draw_right": draw_r,
        }