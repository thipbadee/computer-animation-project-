import numpy as np

from .base import Exercise
from .utils import calculate_angle


class DumbbellSideLateralRaise(Exercise):
    def __init__(self):
        super().__init__()
        self.name = "Dumbbell Side Lateral Raise"
        self.raise_angle = 78
        self.lower_angle = 28
        self.min_elbow_extension = 135

    def _joint(self, landmarks, joint):
        point = landmarks[getattr(self.mp_pose.PoseLandmark, joint).value]
        return [point.x, point.y, point.visibility]

    def process_landmarks(self, landmarks):
        shoulder_r = self._joint(landmarks, "RIGHT_SHOULDER")
        elbow_r = self._joint(landmarks, "RIGHT_ELBOW")
        wrist_r = self._joint(landmarks, "RIGHT_WRIST")
        hip_r = self._joint(landmarks, "RIGHT_HIP")

        shoulder_l = self._joint(landmarks, "LEFT_SHOULDER")
        elbow_l = self._joint(landmarks, "LEFT_ELBOW")
        wrist_l = self._joint(landmarks, "LEFT_WRIST")
        hip_l = self._joint(landmarks, "LEFT_HIP")

        raise_angle_r = calculate_angle(hip_r[:2], shoulder_r[:2], elbow_r[:2])
        raise_angle_l = calculate_angle(hip_l[:2], shoulder_l[:2], elbow_l[:2])

        elbow_angle_r = calculate_angle(shoulder_r[:2], elbow_r[:2], wrist_r[:2])
        elbow_angle_l = calculate_angle(shoulder_l[:2], elbow_l[:2], wrist_l[:2])

        vis_r = (shoulder_r[2] + elbow_r[2] + wrist_r[2] + hip_r[2]) / 4
        vis_l = (shoulder_l[2] + elbow_l[2] + wrist_l[2] + hip_l[2]) / 4

        active_raise_angle = raise_angle_l
        active_elbow_angle = elbow_angle_l
        anchor_l = shoulder_l[:2]
        anchor_r = shoulder_r[:2]
        draw_l = True
        draw_r = False

        if vis_r > vis_l and vis_r > 0.3:
            active_raise_angle = raise_angle_r
            active_elbow_angle = elbow_angle_r
            draw_l = False
            draw_r = True
        elif vis_l < 0.3 and vis_r < 0.3:
            draw_l = False
            draw_r = False

        arms_ready = active_elbow_angle >= self.min_elbow_extension

        if active_raise_angle <= self.lower_angle and arms_ready:
            self.stage = "down"
        if active_raise_angle >= self.raise_angle and self.stage == "down" and arms_ready:
            self.stage = "up"
            self.counter += 1

        per = np.interp(active_raise_angle, (self.lower_angle, self.raise_angle), (0, 100))
        per = float(np.clip(per, 0, 100))
        bar = np.interp(active_raise_angle, (self.lower_angle, self.raise_angle), (400, 150))

        return {
            "active_angle": active_raise_angle,
            "percentage": per,
            "bar_height": bar,
            "stage": self.stage,
            "counter": self.counter,
            "left_elbow": anchor_l,
            "right_elbow": anchor_r,
            "draw_left": draw_l,
            "draw_right": draw_r,
        }
