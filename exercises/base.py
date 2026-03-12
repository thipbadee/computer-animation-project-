import numpy as np
import mediapipe as mp

class Exercise:
    """
    Base class for all exercises.
    """
    def __init__(self):
        self.name = "Unknown Exercise"
        self.counter = 0
        self.stage = None
        self.mp_pose = mp.solutions.pose
        
    def reset(self):
        self.counter = 0
        self.stage = None

    def process_landmarks(self, landmarks):
        """
        Process the raw landmarks from mediapipe and return the UI update dictionary.
        This method must be implemented by subclasses.
        Returns:
            dict: {
                'active_angle': float,
                'percentage': float,
                'bar_height': float,
                'stage': str,
                'counter': int,
                'left_coords': tuple, 
                'right_coords': tuple,
                'draw_left': bool,
                'draw_right': bool
            }
        """
        raise NotImplementedError("Subclasses must implement process_landmarks()")
