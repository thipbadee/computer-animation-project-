# Synthetic Data

This project uses synthetic landmark sequences for its reproducible scaling benchmark.

## Where the Synthetic Data Comes From

Synthetic sequences are generated on demand by:
- `../../src/algorithms/synthetic_data.py`

The benchmark script:
- `../../experiments/benchmark.py`

calls the synthetic generator at runtime rather than loading a pre-saved dataset file.

## What the Synthetic Generator Simulates

The generated sequence models a simplified bicep-curl motion using:
- a periodic elbow-angle trajectory
- additive angle noise
- left/right visibility imbalance
- temporary visibility dropouts

This design is meant to stress the tracker under controlled but imperfect conditions similar to what a real pose-estimation pipeline might produce.

## Why the Dataset Is Generated On Demand

The repository generates benchmark data at runtime because it:
- keeps the repository small
- makes the experiment fully reproducible from code
- allows the benchmark scale to be changed easily
- avoids committing large derived files that can always be regenerated

## How to Run the Synthetic Benchmark

```bash
python src/main.py --mode benchmark
```

Outputs:
- `../../experiments/results/runtime.csv`
- `../../experiments/results/plots.png`

## Current Benchmark Sizes

The benchmark currently evaluates:
- `1,000` frames
- `10,000` frames
- `100,000` frames
