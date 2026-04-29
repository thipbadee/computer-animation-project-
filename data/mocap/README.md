# Mocap Data

This folder documents the project workflow for real recorded landmark data.

## What Is Stored Here

`capture_template.csv`
- Defines the expected CSV schema for recorded arm-landmark sequences.

Potential user-generated files:
- `recorded_arm_sequence.csv`
- any other recorded CSV captured from webcam sessions

## Why Real Data Is Not Committed by Default

The repository intentionally does not include a committed human landmark recording by default because:
- landmark sequences are user-specific
- they may raise privacy concerns
- they are not necessary for reproducing the synthetic benchmark

Instead, the repository provides the capture and replay pipeline.

## Recording a Sequence

Use:

```bash
python tools/collect_mocap.py --output data/mocap/recorded_arm_sequence.csv
```

This opens the webcam, runs MediaPipe Pose, and records selected arm landmarks to a CSV file.

## Evaluating a Recorded Sequence

Use:

```bash
python experiments/evaluate_recorded_sequence.py data/mocap/recorded_arm_sequence.csv --expected-reps 10
```

This replays the saved landmark sequence through both:
- `BaselineBicepCurlTracker`
- `ProposedBicepCurlTracker`

and reports:
- predicted repetition counts
- side switches
- optional count error when `--expected-reps` is supplied

## Related Files

- `../../tools/collect_mocap.py`
- `../../experiments/evaluate_recorded_sequence.py`
- `../../src/algorithms/baseline.py`
- `../../src/algorithms/proposed.py`
