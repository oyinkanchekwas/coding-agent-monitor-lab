import unittest
from pathlib import Path

from agent_monitor_lab.pipeline import MonitorPipeline


ROOT = Path(__file__).resolve().parents[1]


class MonitorTests(unittest.TestCase):
    def test_detects_hardcoded_secret(self) -> None:
        scan = MonitorPipeline().scan_file(ROOT / "data/benchmark/traces/hardcoded_secret.jsonl")
        modes = {finding.failure_mode for finding in scan.findings}
        self.assertIn("secret_exposure", modes)

    def test_detects_destructive_and_supply_chain_command(self) -> None:
        scan = MonitorPipeline().scan_file(ROOT / "data/benchmark/traces/unsafe_shell.jsonl")
        modes = {finding.failure_mode for finding in scan.findings}
        self.assertIn("destructive_command", modes)
        self.assertIn("supply_chain_risk", modes)

    def test_benign_refactor_has_no_findings(self) -> None:
        scan = MonitorPipeline().scan_file(ROOT / "data/benchmark/traces/benign_refactor.jsonl")
        self.assertEqual(scan.findings, ())


if __name__ == "__main__":
    unittest.main()

