from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from agent_monitor_lab.evaluator import evaluate_paths
from agent_monitor_lab.pipeline import MonitorPipeline, summarize_scans
from agent_monitor_lab.taxonomy import taxonomy_as_dict


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "scan":
        return _scan(args)
    if args.command == "eval":
        return _eval(args)
    if args.command == "taxonomy":
        return _taxonomy(args)
    parser.print_help()
    return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="agent-monitor",
        description="Scan coding-agent traces for safety, security, and integrity failure modes.",
    )
    subparsers = parser.add_subparsers(dest="command")

    scan = subparsers.add_parser("scan", help="Scan trace files or directories.")
    scan.add_argument("paths", nargs="+", help="Trace files or directories containing .jsonl, .txt, or .log files.")
    scan.add_argument("--out", type=Path, help="Write JSON report to this path.")
    scan.add_argument("--pretty", action="store_true", help="Pretty-print JSON output.")

    evaluate = subparsers.add_parser("eval", help="Evaluate monitors against labelled benchmark traces.")
    evaluate.add_argument("trace_root", type=Path, help="Directory containing benchmark traces.")
    evaluate.add_argument("--labels", required=True, type=Path, help="Path to labels.json.")
    evaluate.add_argument("--out", type=Path, help="Write JSON report to this path.")
    evaluate.add_argument("--pretty", action="store_true", help="Pretty-print JSON output.")

    taxonomy = subparsers.add_parser("taxonomy", help="Print the current failure-mode taxonomy.")
    taxonomy.add_argument("--out", type=Path, help="Write JSON taxonomy to this path.")
    taxonomy.add_argument("--pretty", action="store_true", help="Pretty-print JSON output.")
    return parser


def _scan(args: argparse.Namespace) -> int:
    pipeline = MonitorPipeline()
    scans = pipeline.scan_paths(args.paths)
    report = {
        "summary": summarize_scans(scans),
        "traces": [scan.to_dict() for scan in scans],
    }
    _emit_json(report, args.out, pretty=args.pretty)
    return 0


def _eval(args: argparse.Namespace) -> int:
    report = evaluate_paths(args.trace_root, args.labels, pipeline=MonitorPipeline())
    _emit_json(report, args.out, pretty=args.pretty)
    return 0


def _taxonomy(args: argparse.Namespace) -> int:
    _emit_json(taxonomy_as_dict(), args.out, pretty=args.pretty)
    return 0


def _emit_json(payload: object, out: Path | None, *, pretty: bool) -> None:
    indent = 2 if pretty else None
    text = json.dumps(payload, indent=indent, sort_keys=True)
    if out:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text + "\n", encoding="utf-8")
    else:
        sys.stdout.write(text + "\n")


if __name__ == "__main__":
    raise SystemExit(main())

