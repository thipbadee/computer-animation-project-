from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
BENCHMARK_CSV = REPO_ROOT / "experiments" / "results" / "runtime.csv"

PROJECT_TITLE = "Real-Time Exercise Motion Tracking with Confidence-Aware Temporal Filtering"
PROJECT_SHORT_TITLE = "Real-Time Exercise Motion Tracking"
COURSE_NAME = "Computer Animation"
DEPARTMENT = "Department of Computer Engineering, Faculty of Engineering, Chulalongkorn University"
SEMESTER = "Final Semester, Academic Year 2568"
AUTHOR_NAME = "thipbadee"
GITHUB_USERNAME = "thipbadee"
INSTRUCTOR_NAME = "[Instructor Name]"
KEYWORDS = [
    "Pose Tracking",
    "Computer Animation",
    "Motion Analysis",
    "Real-time Interaction",
    "Temporal Filtering",
]


@dataclass(frozen=True)
class BenchmarkRow:
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


def load_benchmark_rows() -> list[BenchmarkRow]:
    rows: list[BenchmarkRow] = []
    with BENCHMARK_CSV.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            rows.append(
                BenchmarkRow(
                    input_size=int(row["input_size"]),
                    method=row["method"],
                    expected_reps=int(row["expected_reps"]),
                    predicted_reps=int(row["predicted_reps"]),
                    count_error=int(row["count_error"]),
                    total_ms=float(row["total_ms"]),
                    ms_per_frame=float(row["ms_per_frame"]),
                    peak_kb=float(row["peak_kb"]),
                    stage_changes=int(row["stage_changes"]),
                    side_switches=int(row["side_switches"]),
                )
            )
    return rows


def group_rows_by_size() -> dict[int, dict[str, BenchmarkRow]]:
    grouped: dict[int, dict[str, BenchmarkRow]] = {}
    for row in load_benchmark_rows():
        grouped.setdefault(row.input_size, {})[row.method] = row
    return grouped


def improvement_percentage(baseline_value: float, proposed_value: float) -> float:
    if baseline_value == 0:
        return 0.0
    return ((baseline_value - proposed_value) / baseline_value) * 100.0


def benchmark_summary() -> dict[str, float]:
    grouped = group_rows_by_size()
    largest_size = max(grouped)
    baseline = grouped[largest_size]["baseline"]
    proposed = grouped[largest_size]["proposed"]

    return {
        "largest_size": float(largest_size),
        "speedup_pct": improvement_percentage(baseline.ms_per_frame, proposed.ms_per_frame),
        "memory_reduction_pct": improvement_percentage(baseline.peak_kb, proposed.peak_kb),
        "jitter_reduction_pct": improvement_percentage(baseline.side_switches, proposed.side_switches),
        "baseline_ms_per_frame": baseline.ms_per_frame,
        "proposed_ms_per_frame": proposed.ms_per_frame,
        "baseline_peak_kb": baseline.peak_kb,
        "proposed_peak_kb": proposed.peak_kb,
        "baseline_side_switches": float(baseline.side_switches),
        "proposed_side_switches": float(proposed.side_switches),
    }
