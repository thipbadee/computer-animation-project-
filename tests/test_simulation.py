from __future__ import annotations

import unittest

from src.algorithms import (
    BaselineBicepCurlTracker,
    ProposedBicepCurlTracker,
    generate_bicep_curl_sequence,
)


class BicepCurlBenchmarkTests(unittest.TestCase):
    def test_proposed_matches_expected_reps_on_synthetic_sequence(self):
        sequence = generate_bicep_curl_sequence(num_frames=1_000, seed=13)
        tracker = ProposedBicepCurlTracker()

        for frame in sequence.frames:
            tracker.process(frame)

        self.assertEqual(tracker.counter, sequence.expected_reps)

    def test_proposed_has_no_more_count_error_than_baseline(self):
        sequence = generate_bicep_curl_sequence(num_frames=1_000, seed=21)
        baseline = BaselineBicepCurlTracker()
        proposed = ProposedBicepCurlTracker()

        for frame in sequence.frames:
            baseline.process(frame)
            proposed.process(frame)

        baseline_error = abs(baseline.counter - sequence.expected_reps)
        proposed_error = abs(proposed.counter - sequence.expected_reps)
        self.assertLessEqual(proposed_error, baseline_error)

    def test_proposed_reduces_side_switching_jitter(self):
        sequence = generate_bicep_curl_sequence(num_frames=2_000, seed=5)
        baseline = BaselineBicepCurlTracker()
        proposed = ProposedBicepCurlTracker()

        for frame in sequence.frames:
            baseline.process(frame)
            proposed.process(frame)

        self.assertLess(proposed.side_switches, baseline.side_switches)


if __name__ == "__main__":
    unittest.main()
