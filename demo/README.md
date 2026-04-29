# Demo

This folder contains demonstration artifacts for the project.

## Available Demo Modes

Live web demo:

```bash
python src/main.py --mode web
```

This starts the Flask application and streams the webcam-driven tracking UI to:

```text
http://127.0.0.1:5000
```

Main web pages:
- `/`: landing page
- `/workout`: live dashboard
- `/how-to-use`: setup and usage guide

Live dashboard features:
- webcam stream with pose landmarks and status overlay
- exercise selector for six supported exercises
- reset button for the active exercise state
- reference image and short movement instructions

Synthetic video demo:

```bash
python src/main.py --mode demo
```

This generates:
- `demo/synthetic_bicep_curl.mp4`

## What the Generated Video Shows

The synthetic demo video is a side-by-side comparison between:
- the `baseline` tracker
- the `proposed` tracker

It visualizes:
- a synthetic bicep-curl motion sequence
- the selected active side
- current repetition count
- current stage
- angle estimate
- confidence estimate

Scope note:
- The generated video covers the `bicep curl` benchmark pipeline only.
- The live Flask app supports additional exercise modes implemented under `exercises/`.

## Why This Demo Exists

The synthetic video is useful because it:
- provides a reproducible visual artifact without requiring a live camera
- supports the report and slide deck with side-by-side visual evidence
- makes it easier to discuss temporal stability and active-side behavior

## Related Files

- `../visualization/animate_results.py`: demo generator
- `../app.py`: Flask entry point
- `../camera.py`: live webcam and overlay pipeline
- `../report/assets/demo_strip.png`: sampled frames used in the report/presentation
