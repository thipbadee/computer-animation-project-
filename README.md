# Real-Time Exercise Motion Tracking for Computer Animation

This repository contains a real-time pose-driven exercise tracking project built with Python, Flask, OpenCV, and MediaPipe. The project was organized for a `Computer Animation` course submission and is centered on a reproducible comparison between a simple `baseline` tracker and a more stable `proposed` tracker for bicep-curl motion analysis, while also providing a live web demo for multiple exercise modes.

## Project Summary

Project title:
- `Real-Time Exercise Motion Tracking with Confidence-Aware Temporal Filtering`

Core idea:
- Treat webcam-based exercise tracking as an articulated motion interpretation problem.
- Use pose landmarks as a lightweight skeleton.
- Convert landmark sequences into `count`, `stage`, `angle`, and `progress`.
- Compare a simple threshold-based baseline against a confidence-aware, temporally filtered proposed method.

Live exercise modes in the web app:
- `Bicep Curl`
- `Shoulder Press`
- `Dumbbell Side Lateral Raise`
- `Squat`
- `Plank`
- `High Knees`

Project split:
- `app.py`, `camera.py`, `templates/`, `static/`, and `exercises/` implement the live webcam web application.
- `src/algorithms/`, `experiments/`, and `visualization/` implement the reproducible baseline-versus-proposed benchmark pipeline used in the report.
- The comparative experiment is centered on `bicep curl` motion, while the live web app exposes six exercise modes for interactive demonstration.

## Problem Statement

The project studies real-time repetition tracking from noisy 2D pose landmarks. The main challenge is not only detecting pose landmarks, but interpreting them robustly over time while handling:

- partial occlusion
- left/right arm ambiguity
- threshold chatter near turning points
- visible frame-to-frame jitter
- live responsiveness requirements for interactive feedback

From a computer animation perspective, the system maps continuous body motion into pose states and transitions, similar to a simplified rig-and-state workflow.

## Baseline vs Proposed

Baseline:
- selects the more visible arm
- computes elbow angle directly from landmarks
- uses fixed thresholds to detect `down -> up` transitions
- has low implementation complexity
- is more sensitive to side-switch jitter and noisy turning points

Proposed:
- uses confidence-aware side selection
- keeps a short-term side lock to reduce arm flapping
- smooths elbow angle with an exponential moving average
- preserves the same public output interface as the baseline
- improves temporal stability, with a small runtime trade-off at the largest tested scale

Shared output fields:
- `count`
- `stage`
- `angle`
- `progress`

## Current Benchmark Snapshot

Run:

```bash
python src/main.py --mode benchmark
```

Latest benchmark files:
- [runtime.csv](/c:/Users/USER/Documents/computer-animation-project-/experiments/results/runtime.csv)
- [plots.png](/c:/Users/USER/Documents/computer-animation-project-/experiments/results/plots.png)

Current quantitative summary from `runtime.csv`:

- At `1,000` frames, proposed is faster: `0.006809 -> 0.005954 ms/frame` (`+12.56%`)
- At `10,000` frames, proposed is faster: `0.006103 -> 0.005409 ms/frame` (`+11.37%`)
- At `100,000` frames, proposed is slightly slower: `0.006073 -> 0.006172 ms/frame` (`-1.64%`)
- At `100,000` frames, proposed reduces peak traced memory: `0.609 -> 0.531 KB`
- At `100,000` frames, proposed reduces side-switch jitter: `3832 -> 3334`
- Repetition-count error remains `0` for both methods at all tested scales

Interpretation:
- The proposed method improves temporal stability consistently.
- The proposed method is faster at small and medium scales.
- At the largest tested scale, the added temporal logic introduces a small runtime overhead, but still improves memory usage and tracking stability.

## How to Run

Prerequisite:

```bash
pip install -r requirements.txt
```

The detailed execution paths are listed in the `Run Guide` below. In practice, most users will choose one of these modes:
- `web`: live webcam application
- `benchmark`: reproducible baseline-versus-proposed experiment
- `demo`: synthetic side-by-side video generation
- `tests`: unit-test verification
- `collect_mocap` + `evaluate_recorded_sequence`: real-data capture and replay pipeline

## Run Guide

Use the project in one of the following four ways, depending on your goal.

### 1. Live Web Demo

Purpose:
- run the real-time webcam application
- interact with the UI and switch between supported exercises

Commands:

```bash
python src/main.py --mode web
```

Then open:

```text
http://127.0.0.1:5000
```

Typical steps:
1. Start the command above.
2. Open the browser at `http://127.0.0.1:5000`.
3. Go to `/workout`.
4. Select an exercise from the right-side panel.
5. Perform the motion while watching the live overlay for `count`, `stage`, and `progress`.

### 2. Reproducible Benchmark

Purpose:
- compare the `baseline` and `proposed` methods on synthetic bicep-curl sequences
- regenerate the runtime and stability numbers used in the report

Command:

```bash
python src/main.py --mode benchmark
```

Outputs:
- `experiments/results/runtime.csv`
- `experiments/results/plots.png`

Typical steps:
1. Run the benchmark command.
2. Wait for the benchmark to finish.
3. Open `runtime.csv` for numeric results.
4. Open `plots.png` for the summary figure used in the report and presentation.

### 3. Synthetic Demo Video

Purpose:
- generate a side-by-side visual comparison between `baseline` and `proposed`
- produce a reproducible demo artifact without requiring a live camera

Command:

```bash
python src/main.py --mode demo
```

Output:
- `demo/synthetic_bicep_curl.mp4`

Typical steps:
1. Run the demo command.
2. Open `demo/synthetic_bicep_curl.mp4`.
3. Use the video as supporting evidence in the report or slide deck.

### 4. Real-Data Capture and Replay

Purpose:
- record a real webcam landmark sequence
- replay the saved sequence through the `baseline` and `proposed` bicep-curl trackers

Step 1: record a sequence

```bash
python tools/collect_mocap.py --output data/mocap/recorded_arm_sequence.csv
```

How to record:
1. Stand so the camera can clearly see your shoulder, elbow, and wrist.
2. Perform the `Bicep Curl` exercise.
3. Complete the intended number of repetitions, such as `10`.
4. Press `q` to stop recording.

Step 2: evaluate the recorded sequence

```bash
python experiments/evaluate_recorded_sequence.py data/mocap/recorded_arm_sequence.csv --expected-reps 10
```

What this reports:
- predicted repetition count for `baseline`
- predicted repetition count for `proposed`
- side switches for both methods
- count error, if `--expected-reps` is supplied

Important note:
- the current real-data evaluation pipeline is designed for `Bicep Curl`
- other live exercise modes in the Flask app are not yet supported by `evaluate_recorded_sequence.py`

### 5. Unit Tests

Purpose:
- verify that the benchmark-side tracking logic still behaves as expected

Command:

```bash
python -m unittest tests.test_simulation
```

### Recommended Execution Order

For a quick product demo:
1. `pip install -r requirements.txt`
2. `python src/main.py --mode web`

For report regeneration:
1. `python src/main.py --mode benchmark`
2. `python src/main.py --mode demo`
3. `python scripts/generate_submission_assets.py`
4. `python scripts/generate_report_docx.py`
5. `python scripts/generate_presentation.py`

For real-data evaluation:
1. `python tools/collect_mocap.py --output data/mocap/recorded_arm_sequence.csv`
2. `python experiments/evaluate_recorded_sequence.py data/mocap/recorded_arm_sequence.csv --expected-reps 10`

## Live Web Application

Main pages:
- `/`: landing page with project entry links
- `/workout`: live workout dashboard with webcam stream, exercise selector, and reference guide
- `/how-to-use`: usage instructions and setup checklist

Streaming and control endpoints:
- `/video_feed`: MJPEG webcam stream with pose overlay
- `/set_exercise`: POST endpoint that switches the current exercise and resets its state
- `/current_exercise`: returns the currently selected exercise name as JSON
- `/reset_counter`: POST endpoint that clears the active exercise state

What appears on the live overlay:
- current exercise name
- repetition count or elapsed time, depending on the mode
- current stage such as `up`, `down`, `hold`, `adjust`, or `left up`
- pose landmarks drawn on the webcam frame
- progress gauge derived from the active motion angle or posture score

Web-app execution flow:
1. `app.py` serves the HTML pages and JSON endpoints.
2. `camera.py` opens the webcam, runs MediaPipe Pose, and dispatches landmarks to the currently selected exercise class.
3. The exercise module in `exercises/` converts landmarks into UI fields such as `counter`, `stage`, `active_angle`, and `percentage`.
4. The processed frame is streamed back to `/video_feed` and rendered inside `templates/workout.html`.

## Supported Exercise Logic

The live application includes six exercise analyzers. They do not all use the same kinematic signal:

- `Bicep Curl`: tracks elbow flexion/extension and counts `down -> up` transitions.
- `Shoulder Press`: tracks arm extension overhead and counts `down -> up` presses.
- `Dumbbell Side Lateral Raise`: tracks shoulder abduction angle while requiring the elbow to stay sufficiently extended.
- `Squat`: tracks knee angle to estimate squat depth and counts return-to-stand transitions.
- `Plank`: does not count repetitions; it estimates posture quality and accumulates valid hold time.
- `High Knees`: does not use a joint angle directly; it tracks alternating knee-lift height and counts steps with a switch-timing guard.

This distinction matters when reading the code:
- `exercises/` contains the real-time multi-exercise logic used by the Flask app.
- `src/algorithms/` contains the research-style baseline/proposed comparison used for the benchmark, report, and synthetic demo video.

## Real-Data Workflow

Record a landmark sequence from webcam input:

```bash
python tools/collect_mocap.py --output data/mocap/recorded_arm_sequence.csv
```

Replay and evaluate the recorded sequence:

```bash
python experiments/evaluate_recorded_sequence.py data/mocap/recorded_arm_sequence.csv --expected-reps 10
```

This workflow exists so the repository supports both:
- reproducible synthetic benchmarking
- optional real-data evaluation without embedding private user motion files in the repository

Recorded CSV schema:
- Each row stores frame-level 2D landmarks and visibility values for shoulder, elbow, and wrist joints on both sides.
- The replay script uses this schema to reconstruct the same arm-state sequence for offline evaluation.

## Submission Artifacts

Recommended submission documents:
- [report.docx](/c:/Users/USER/Documents/computer-animation-project-/report/report.docx)
- [presentation.pptx](/c:/Users/USER/Documents/computer-animation-project-/report/presentation.pptx)

Supporting submission assets:
- [workflow.png](/c:/Users/USER/Documents/computer-animation-project-/report/assets/workflow.png)
- [plots.png](/c:/Users/USER/Documents/computer-animation-project-/experiments/results/plots.png)
- [demo_strip.png](/c:/Users/USER/Documents/computer-animation-project-/report/assets/demo_strip.png)
- [synthetic_bicep_curl.mp4](/c:/Users/USER/Documents/computer-animation-project-/demo/synthetic_bicep_curl.mp4)

The `report/` folder now contains only the current submission documents and their supporting assets.

## Repository Structure

```text
computer-animation-project-/
|-- README.md
|-- app.py
|-- camera.py
|-- requirements.txt
|-- exercises/
|-- templates/
|-- static/
|-- src/
|   |-- main.py
|   |-- algorithms/
|   `-- data_structures/
|-- experiments/
|   |-- benchmark.py
|   |-- evaluate_recorded_sequence.py
|   `-- results/
|-- visualization/
|-- tools/
|-- tests/
|-- data/
|   |-- synthetic/
|   `-- mocap/
|-- demo/
|-- scripts/
`-- report/
```

## Important Paths

Application files:
- `app.py`: Flask routes and page serving
- `camera.py`: webcam capture, MediaPipe inference, and live overlay pipeline
- `exercises/`: exercise-specific real-time tracking logic
- `templates/`: landing page, workout dashboard, and how-to-use page
- `static/`: stylesheet for the web interface

Benchmark files:
- `src/algorithms/baseline.py`
- `src/algorithms/proposed.py`
- `src/algorithms/synthetic_data.py`
- `experiments/benchmark.py`

Visualization files:
- `visualization/animate_results.py`
- `experiments/results/plots.png`
- `demo/synthetic_bicep_curl.mp4`

Real-data tools:
- `tools/collect_mocap.py`
- `experiments/evaluate_recorded_sequence.py`

Document-generation scripts:
- `scripts/generate_submission_assets.py`
- `scripts/generate_report_docx.py`
- `scripts/generate_presentation.py`

## Regenerating Documents and Figures

Regenerate report/supporting assets:

```bash
python src/main.py --mode benchmark
python src/main.py --mode demo
python scripts/generate_submission_assets.py
python scripts/generate_report_docx.py
python scripts/generate_presentation.py
```

Run the commands in this order so:
- `runtime.csv` and `plots.png` are refreshed before document generation
- `demo/synthetic_bicep_curl.mp4` exists before `demo_strip.png` is extracted

## Notes and Limitations

- The benchmark is centered on a representative motion primitive (`bicep curl`) rather than every live exercise mode.
- The live Flask demo and the benchmark pipeline are related but separate subsystems; changes in one do not automatically update the other unless the corresponding scripts are rerun.
- `synthetic_data.py` generates benchmark data on demand and does not store a large committed dataset.
- Real webcam landmark CSV files are intentionally not committed by default due to privacy concerns.
- The current document set still contains an instructor-name placeholder if that value has not yet been filled in manually.

## Recommended Final Submission Checklist

- Confirm the final report file is `report/report.docx`
- Confirm the final presentation file is `report/presentation.pptx`
- Include `experiments/results/runtime.csv` and `experiments/results/plots.png`
- Include `demo/synthetic_bicep_curl.mp4`
- Include source code folders and `requirements.txt`
- Exclude `venv/` unless specifically requested
