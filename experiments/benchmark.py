from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
import time
import tracemalloc

import cv2
import numpy as np

from src.algorithms import (
    BaselineBicepCurlTracker,
    ProposedBicepCurlTracker,
    generate_bicep_curl_sequence,
)


RESULTS_DIR = Path(__file__).resolve().parent / "results"
CSV_PATH = RESULTS_DIR / "runtime.csv"
PLOT_PATH = RESULTS_DIR / "plots.png"


@dataclass
class BenchmarkResult:
    input_size: int
    method: str
    expected_reps: int
    predicted_reps: int
    count_error: int
    total_ms: float
    ms_per_frame: float
    peak_kb: float
    stage_changes: int
    side_switches: int


def evaluate_tracker(tracker, frames, expected_reps: int, method: str) -> BenchmarkResult:
    tracemalloc.start()
    start = time.perf_counter()
    for frame in frames:
        tracker.process(frame)
    total_ms = (time.perf_counter() - start) * 1000.0
    _, peak_bytes = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return BenchmarkResult(
        input_size=len(frames),
        method=method,
        expected_reps=expected_reps,
        predicted_reps=tracker.counter,
        count_error=abs(tracker.counter - expected_reps),
        total_ms=total_ms,
        ms_per_frame=total_ms / len(frames),
        peak_kb=peak_bytes / 1024.0,
        stage_changes=tracker.stage_changes,
        side_switches=tracker.side_switches,
    )


def write_csv(results: list[BenchmarkResult]):
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    with CSV_PATH.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=[
                "input_size",
                "method",
                "expected_reps",
                "predicted_reps",
                "count_error",
                "total_ms",
                "ms_per_frame",
                "peak_kb",
                "stage_changes",
                "side_switches",
            ],
        )
        writer.writeheader()
        for result in results:
            writer.writerow(result.__dict__)


def _draw_axes(canvas, origin, width, height, title):
    x0, y0 = origin
    cv2.rectangle(canvas, (x0 - 25, y0 - height - 55), (x0 + width + 15, y0 + 20), (255, 255, 255), -1)
    cv2.rectangle(canvas, (x0 - 25, y0 - height - 55), (x0 + width + 15, y0 + 20), (225, 230, 236), 2)
    cv2.line(canvas, (x0, y0), (x0, y0 - height), (50, 50, 50), 2)
    cv2.line(canvas, (x0, y0), (x0 + width, y0), (50, 50, 50), 2)
    cv2.putText(canvas, title, (x0, y0 - height - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (30, 30, 30), 2)


def write_plot(results: list[BenchmarkResult]):
    baseline = [r for r in results if r.method == "baseline"]
    proposed = [r for r in results if r.method == "proposed"]

    canvas = np.full((860, 1400, 3), 248, dtype=np.uint8)
    _draw_axes(canvas, (110, 390), 500, 240, "Runtime (ms/frame)")
    _draw_axes(canvas, (760, 390), 500, 240, "Count Error")
    _draw_axes(canvas, (110, 760), 500, 240, "Peak Memory (KB)")
    _draw_axes(canvas, (760, 760), 500, 240, "Side Switches")

    labels = ["1k", "10k", "100k"]
    bar_positions = [120, 270, 420]

    def draw_metric(group_a, group_b, attr, origin_x, origin_y, scale):
        for idx, pos_x in enumerate(bar_positions):
            a_val = getattr(group_a[idx], attr)
            b_val = getattr(group_b[idx], attr)
            a_h = int(min(240, a_val * scale))
            b_h = int(min(240, b_val * scale))
            cv2.rectangle(canvas, (origin_x + pos_x - 28, origin_y - a_h), (origin_x + pos_x - 4, origin_y), (72, 125, 245), -1)
            cv2.rectangle(canvas, (origin_x + pos_x + 6, origin_y - b_h), (origin_x + pos_x + 30, origin_y), (0, 180, 120), -1)
            cv2.putText(canvas, labels[idx], (origin_x + pos_x - 18, origin_y + 34), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (30, 30, 30), 2)

    runtime_scale = 240.0 / max(r.ms_per_frame for r in results)
    memory_scale = 240.0 / max(r.peak_kb for r in results)
    error_scale = 240.0 / max(1, max(r.count_error for r in results))
    switch_scale = 240.0 / max(1, max(r.side_switches for r in results))

    draw_metric(baseline, proposed, "ms_per_frame", 0, 390, runtime_scale)
    draw_metric(baseline, proposed, "count_error", 650, 390, error_scale)
    draw_metric(baseline, proposed, "peak_kb", 0, 760, memory_scale)
    draw_metric(baseline, proposed, "side_switches", 650, 760, switch_scale)

    cv2.putText(canvas, "Synthetic scaling benchmark for bicep curl tracking", (110, 55), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (20, 20, 20), 2)
    cv2.putText(canvas, "Blue = Baseline", (110, 95), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (72, 125, 245), 2)
    cv2.putText(canvas, "Green = Proposed", (340, 95), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 180, 120), 2)
    cv2.putText(canvas, "Each panel compares the same 3 input scales: 1k, 10k, 100k frames.", (110, 125), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (90, 90, 90), 2)

    cv2.imwrite(str(PLOT_PATH), canvas)


def main():
    input_sizes = [1_000, 10_000, 100_000]
    results = []

    for input_size in input_sizes:
        sequence = generate_bicep_curl_sequence(num_frames=input_size)
        results.append(
            evaluate_tracker(
                tracker=BaselineBicepCurlTracker(),
                frames=sequence.frames,
                expected_reps=sequence.expected_reps,
                method="baseline",
            )
        )
        results.append(
            evaluate_tracker(
                tracker=ProposedBicepCurlTracker(),
                frames=sequence.frames,
                expected_reps=sequence.expected_reps,
                method="proposed",
            )
        )

    write_csv(results)
    write_plot(results)

    print(f"Wrote benchmark results to {CSV_PATH}")
    print(f"Wrote benchmark plot to {PLOT_PATH}")


if __name__ == "__main__":
    main()
