import numpy as np
from .base import Exercise
from .utils import calculate_angle

class BicepCurl(Exercise):
    def __init__(self):
        super().__init__()
        self.name = "Bicep Curl"
        # Thresholds
        self.max_angle = 160  # Down position
        self.min_angle = 35   # Up position

    def process_landmarks(self, landmarks):
        # Extract Right Arm
        shoulder_r = [
            landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
            landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y,
            landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].visibility
        ]
        elbow_r = [
            landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
            landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value].y,
            landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value].visibility
        ]
        wrist_r = [
            landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
            landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST.value].y,
            landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST.value].visibility
        ]

        # Extract Left Arm
        shoulder_l = [
            landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
            landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].y,
            landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].visibility
        ]
        elbow_l = [
            landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
            landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].y,
            landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].visibility
        ]
        wrist_l = [
            landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value].x,
            landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value].y,
            landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value].visibility
        ]

        # Calculate Angles
        angle_r = calculate_angle(shoulder_r[:2], elbow_r[:2], wrist_r[:2])
        angle_l = calculate_angle(shoulder_l[:2], elbow_l[:2], wrist_l[:2])

        # Active Arm Logic (Visibility)
        vis_r = (shoulder_r[2] + elbow_r[2] + wrist_r[2]) / 3
        vis_l = (shoulder_l[2] + elbow_l[2] + wrist_l[2]) / 3

        active_angle = angle_l
        draw_l = True
        draw_r = False

        if vis_r > vis_l and vis_r > 0.3:
            active_angle = angle_r
            draw_l = False
            draw_r = True
        elif vis_l < 0.3 and vis_r < 0.3:
            draw_l = False
            draw_r = False

        # Counter Logic
        if active_angle > self.max_angle:
            self.stage = "down"
        if active_angle < self.min_angle and self.stage == 'down':
            self.stage = "up"
            self.counter += 1

        # Gauge Logic (160 -> 0%, 35 -> 100%)
        per = np.interp(active_angle, (self.min_angle, self.max_angle), (100, 0))
        bar = np.interp(active_angle, (self.min_angle, self.max_angle), (150, 400))

        return {
            'active_angle': active_angle,
            'percentage': per,
            'bar_height': bar,
            'stage': self.stage,
            'counter': self.counter,
            'left_elbow': elbow_l[:2],
            'right_elbow': elbow_r[:2],
            'draw_left': draw_l,
            'draw_right': draw_r
        }
