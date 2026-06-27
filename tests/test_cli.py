import json
import tempfile
import unittest
from pathlib import Path

from agent_monitor_lab.cli import main


ROOT = Path(__file__).resolve().parents[1]


class CliTests(unittest.TestCase):
    def test_scan_writes_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "scan.json"
            code = main(["scan", str(ROOT / "data/benchmark/traces/hardcoded_secret.jsonl"), "--out", str(out)])
            payload = json.loads(out.read_text(encoding="utf-8"))

        self.assertEqual(code, 0)
        self.assertEqual(payload["summary"]["trace_count"], 1)
        self.assertEqual(payload["summary"]["finding_count"], 1)


if __name__ == "__main__":
    unittest.main()

