import unittest
from pathlib import Path

from agent_monitor_lab.evaluator import evaluate_paths


ROOT = Path(__file__).resolve().parents[1]


class EvaluatorTests(unittest.TestCase):
    def test_benchmark_micro_recall_is_high(self) -> None:
        report = evaluate_paths(
            ROOT / "data/benchmark/traces",
            ROOT / "data/benchmark/labels.json",
        )

        self.assertGreaterEqual(report["micro"]["recall"], 0.9)
        self.assertEqual(report["cases"][-1]["trace_id"], "benign_refactor")


if __name__ == "__main__":
    unittest.main()

