import numpy as np

from .base import Exercise
from .utils import calculate_angle


class Squat(Exercise):
    def __init__(self):
        super().__init__()
        self.name = "Squat"
        self.stand_angle = 170
        self.bottom_angle = 90

    def _joint(self, landmarks, joint):
        point = landmarks[getattr(self.mp_pose.PoseLandmark, joint).value]
        return [point.x, point.y, point.visibility]

    def process_landmarks(self, landmarks):
        hip_r = self._joint(landmarks, "RIGHT_HIP")
        knee_r = self._joint(landmarks, "RIGHT_KNEE")
        ankle_r = self._joint(landmarks, "RIGHT_ANKLE")

        hip_l = self._joint(landmarks, "LEFT_HIP")
        knee_l = self._joint(landmarks, "LEFT_KNEE")
        ankle_l = self._joint(landmarks, "LEFT_ANKLE")

        knee_angle_r = calculate_angle(hip_r[:2], knee_r[:2], ankle_r[:2])
        knee_angle_l = calculate_angle(hip_l[:2], knee_l[:2], ankle_l[:2])

        vis_r = (hip_r[2] + knee_r[2] + ankle_r[2]) / 3
        vis_l = (hip_l[2] + knee_l[2] + ankle_l[2]) / 3

        active_angle = knee_angle_l
        draw_l = True
        draw_r = False

        if vis_r > vis_l and vis_r > 0.3:
            active_angle = knee_angle_r
            draw_l = False
            draw_r = True
        elif vis_l < 0.3 and vis_r < 0.3:
            draw_l = False
            draw_r = False

        # State machine for squat depth using the knee DOF of the leg chain.
        if active_angle > self.stand_angle and self.stage == "down":
            self.stage = "up"
            self.counter += 1
        elif active_angle > self.stand_angle:
            self.stage = "up"
        elif active_angle < self.bottom_angle and self.stage == "up":
            self.stage = "down"

        # Match bicep curl style:
        # standing tall (large knee angle) -> 0%
        # deep squat (small knee angle) -> 100%
        per = np.interp(active_angle, (self.bottom_angle, self.stand_angle), (100, 0))
        per = float(np.clip(per, 0, 100))
        bar = np.interp(active_angle, (self.bottom_angle, self.stand_angle), (150, 400))

        return {
            "active_angle": active_angle,
            "percentage": per,
            "bar_height": bar,
            "stage": self.stage,
            "counter": self.counter,
            "left_elbow": knee_l[:2],
            "right_elbow": knee_r[:2],
            "draw_left": draw_l,
            "draw_right": draw_r,
        }
