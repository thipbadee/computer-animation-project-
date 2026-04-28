# AI Gymnastics Tracker 🏋️‍♂️🤖

A Real-Time AI Pose Estimation system built with Python, OpenCV, and Mediapipe.
Our tracker uses webcam input to count your repetitions automatically and gives you a visual progress gauge to ensure you hit the full range of motion!

---

## ✨ Features
- ⚡ **Real-time Tracking:** Low-latency pose detection using Mediapipe.
- 💪 **Multi-Exercise Support:** Toggle between **Bicep Curls**, **Shoulder Press**, **Dumbbell Side Lateral Raise**, **Squat**, **Plank**, and **High Knees**.
- 📊 **Visual Gauge:** A dynamic progress bar (0-100%) that tracks your form.
- 🔢 **Automatic Counting:** Intelligently counts reps based on defined angle thresholds.

---

## 🛠️ Getting Started (For Collaborators)

### Prerequisites
- Python 3.12

### 1. Clone & Setup
```bash
git clone https://github.com/thipbadee/computer-animation-project-.git
cd computer-animation-project-

# Setup Virtual Environment
py -3.12 -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install Dependencies
pip install -r requirements.txt
```

### 2. Run the Web Tracker
```bash
python app.py
```

### 3. Open the Dashboard
Open your web browser (Chrome, Safari, Edge) and go to:
```text
http://127.0.0.1:5000
```

---

## 🎮 Controls & Interface
Everything is now controlled via a sleek web interface!
- **Exercise Mode:** Click the buttons on the dashboard to switch between all supported exercises, including **Dumbbell Side Lateral Raise**.
- **Reset:** Click the "Reset Counter" button safely from your browser.
- **Positioning:** Stand back so your upper body (shoulders to wrists) is visible in the web stream.

---

## 📂 Project Structure
```text
.
├── app.py                  # Flask Web Server & API endpoints
├── camera.py               # VideoCamera class handling OpenCV & Mediapipe
├── exercises/              # Folder containing logic for specific exercises
│   ├── __init__.py         # Package exports
│   ├── base.py             # The Exercise base class (interface)
│   ├── bicep_curl.py       # Logic for tracking Bicep Curls
│   ├── shoulder_press.py   # Logic for tracking Shoulder Presses
│   └── utils.py            # Utility functions (e.g. calculate_angle)
├── static/
│   └── style.css           # Premium Dark Mode Glassmorphism UI
├── templates/
│   └── index.html          # Main HTML Dashboard
├── requirements.txt        # Project dependencies (Flask added)
├── .gitignore              # Git ignore rules for Python & IDEs
└── README.md               # You are here!
```

---

## ⚙️ Exercise Logic
| Exercise | Down Threshold | Up Threshold | Logic |
| :--- | :--- | :--- | :--- |
| **Bicep Curls** | Angle > 160° | Angle < 35° | Tracks the most bent arm |
| **Shoulder Press** | Angle < 70° | Angle > 160° | Tracks the most extended arm |
| **Dumbbell Side Lateral Raise** | Shoulder angle < 28° | Shoulder angle > 78° | Tracks the clearest arm while keeping the elbow mostly extended |

---

## ❓ Troubleshooting
- **Camera Not Opening:** If you get a "Camera index out of range" error, check `camera.py` at line 9. `self.video = cv2.VideoCapture(0)` is the default. If you have multiple cameras, try changing `0` to `1` or `2`.
- **Low FPS:** Ensure your laptop is plugged in and check that no other app is using the camera.

---

## 🤝 Contributing
Feel free to add new exercises! We use a clean, modular structure so you don't have to touch the main camera logic. To add a new exercise (e.g. Squats):

1. **Create a new file** in the `exercises/` folder (e.g., `exercises/squat.py`).
2. **Inherit from the `Exercise` base class** and implement the `process_landmarks(self, landmarks)` method. Check out `bicep_curl.py` for inspiration!
3. **Return the UI dictionary** at the end of your method (containing `active_angle`, `stage`, `counter`, `percentage`, etc.)
4. **Register your exercise** by importing it into `camera.py` and adding it to the `self.exercises_dict` around line 17:
   ```python
   from exercises import BicepCurl, ShoulderPress, Squat
   self.exercises_dict = {
       'Bicep Curl': BicepCurl(),
       'Shoulder Press': ShoulderPress(),
       'Squat': Squat()
   }
   ```
5. Update `templates/index.html` to add a new button for your exercise.
6. Run `python app.py` and toggle to your brand new exercise on the web dashboard!
