import tempfile
import unittest
from pathlib import Path

from agent_monitor_lab.parser import parse_trace_file


class ParserTests(unittest.TestCase):
    def test_parse_jsonl_and_plain_lines(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "trace.jsonl"
            path.write_text(
                '{"id":"one","actor":"agent","action":"message","content":"hello"}\n'
                "plain fallback line\n",
                encoding="utf-8",
            )

            events = parse_trace_file(path)

        self.assertEqual(len(events), 2)
        self.assertEqual(events[0].event_id, "one")
        self.assertEqual(events[1].content, "plain fallback line")
        self.assertEqual(events[1].line_number, 2)


if __name__ == "__main__":
    unittest.main()

