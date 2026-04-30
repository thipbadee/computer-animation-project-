import cv2
import numpy as np
import mediapipe as mp
from exercises import (
    BicepCurl,
    DumbbellSideLateralRaise,
    HighKnees,
    Plank,
    ShoulderPress,
    Squat,
)

class VideoCamera(object):
    def __init__(self):
        # Open the webcam
        self.video = cv2.VideoCapture(0)
        
        # Mediapipe pose setup
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.mp_drawing = mp.solutions.drawing_utils
        
        # Exercises Setup
        self.exercises_dict = {
            'Bicep Curl': BicepCurl(),
            'Shoulder Press': ShoulderPress(),
            'Dumbbell Side Lateral Raise': DumbbellSideLateralRaise(),
            'Squat': Squat(),
            'Plank': Plank(),
            'High Knees': HighKnees()
        }
        self.current_exercise_name = 'Bicep Curl'
        self.current_exercise = self.exercises_dict[self.current_exercise_name]

    def __del__(self):
        self.video.release()
        
    def set_exercise(self, exercise_name):
        if exercise_name in self.exercises_dict:
            self.current_exercise_name = exercise_name
            self.current_exercise = self.exercises_dict[exercise_name]
            self.reset_counter()

    def reset_counter(self):
        self.current_exercise.reset()

    def get_current_exercise_name(self):
        return self.current_exercise_name

    def get_frame(self):
        success, frame = self.video.read()
        if not success:
            return None

        # Present the webcam feed in a non-mirrored orientation on the web UI.
        frame = cv2.flip(frame, 1)

        # ReColor Image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        
        # Make Detection
        results = self.pose.process(image)

        # Recoloring Back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        ui_data = {}
        if results.pose_landmarks:
            try:
                landmarks = results.pose_landmarks.landmark
                ui_data = self.current_exercise.process_landmarks(landmarks)
                
                # Visualize Active Angle on the frame directly (optional, since we'll draw it below)
                if ui_data.get('draw_left'):
                    cv2.putText(image, str(int(ui_data['active_angle'])),
                                tuple(np.multiply(ui_data['left_elbow'], [640, 480]).astype(int)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                elif ui_data.get('draw_right'):
                    cv2.putText(image, str(int(ui_data['active_angle'])),
                                tuple(np.multiply(ui_data['right_elbow'], [640, 480]).astype(int)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                
                # Render Detections
                self.mp_drawing.draw_landmarks(
                    image,
                    results.pose_landmarks,
                    self.mp_pose.POSE_CONNECTIONS,
                    self.mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                    self.mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                )

            except Exception as e:
                pass
        
        # -----------------------------------------
        # Modern Minimal UI Overlay
        # -----------------------------------------
        
        # Helper function to draw rounded rectangles with transparency
        def draw_glass_pill(img, pt1, pt2, color, alpha=0.5):
            overlay = img.copy()
            # Draw rounded rectangle (approximate with circles and rects)
            r = 15 # radius
            x1, y1 = pt1
            x2, y2 = pt2
            cv2.rectangle(overlay, (x1+r, y1), (x2-r, y2), color, -1)
            cv2.rectangle(overlay, (x1, y1+r), (x2, y2-r), color, -1)
            cv2.circle(overlay, (x1+r, y1+r), r, color, -1)
            cv2.circle(overlay, (x2-r, y1+r), r, color, -1)
            cv2.circle(overlay, (x1+r, y2-r), r, color, -1)
            cv2.circle(overlay, (x2-r, y2-r), r, color, -1)
            cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)

        bg_color = (20, 20, 20) # Dark gray glass
        
        # 1. Exercise Name Pill (Top Left)
        draw_glass_pill(image, (20, 20), (360, 70), bg_color, 0.6)
        exercise_name = self.current_exercise.name.upper()
        name_scale = 0.55 if len(exercise_name) > 22 else 0.8
        cv2.putText(image, exercise_name, (40, 52),
                    cv2.FONT_HERSHEY_SIMPLEX, name_scale, (255, 255, 255), 2, cv2.LINE_AA)

        # 2. Reps & Stage Box (Top Right)
        draw_glass_pill(image, (420, 20), (620, 85), bg_color, 0.6)
        
        # Reps
        value_label = ui_data.get('display_label', 'REPS')
        value_text = ui_data.get('display_value', str(ui_data.get('counter', self.current_exercise.counter)))
        cv2.putText(image, value_label, (440, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1, cv2.LINE_AA)
        cv2.putText(image, value_text, (440, 75), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 136), 2, cv2.LINE_AA)
        
        # Stage
        cv2.putText(image, 'STAGE', (520, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1, cv2.LINE_AA)
        stage_str = str(ui_data.get('stage', self.current_exercise.stage or '-')).upper()
        stage_color = (0, 255, 136) if 'UP' in stage_str or stage_str == 'HOLD' else (255, 100, 100)
        cv2.putText(image, stage_str, (520, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.8, stage_color, 2, cv2.LINE_AA)

        # 3. Minimal Modern Gauge (Bottom Right)
        if 'percentage' in ui_data and 'bar_height' in ui_data:
            # We map the 150-400 bar to a smaller, sleeker bar: 250 to 450
            bar_mapped = np.interp(ui_data['percentage'], (0, 100), (420, 250))
            
            # Background track
            cv2.rectangle(image, (590, 250), (600, 420), (50, 50, 50), -1)
            # Filled progress
            cv2.rectangle(image, (590, int(bar_mapped)), (600, 420), (0, 255, 136), -1)
            # Text
            cv2.putText(image, f"{int(ui_data['percentage'])}%", (540, 440), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 136), 1, cv2.LINE_AA)

        # Encode frame to JPEG
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
