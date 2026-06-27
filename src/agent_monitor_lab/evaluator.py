from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from agent_monitor_lab.models import TraceScan
from agent_monitor_lab.pipeline import MonitorPipeline, summarise_scans
from agent_monitor_lab.taxonomy import FAILURE_MODES


@dataclass(frozen=True)
class LabelledTrace:
    trace_id: str
    file: str
    labels: tuple[str, ...]


def load_labels(path: str | Path) -> tuple[LabelledTrace, ...]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    traces = payload.get("traces", [])
    return tuple(
        LabelledTrace(
            trace_id=str(item["trace_id"]),
            file=str(item["file"]),
            labels=tuple(sorted(item.get("labels", []))),
        )
        for item in traces
    )


def evaluate_paths(trace_root: str | Path, labels_path: str | Path, pipeline: MonitorPipeline | None = None) -> dict[str, object]:
    pipeline = pipeline or MonitorPipeline()
    trace_root = Path(trace_root)
    labelled = load_labels(labels_path)
    scans = []
    for item in labelled:
        scan = pipeline.scan_file(trace_root / item.file)
        scans.append(scan)
    return evaluate_scans(scans, labelled)


def evaluate_scans(scans: Iterable[TraceScan], labelled: Iterable[LabelledTrace]) -> dict[str, object]:
    scans_by_id = {scan.trace_id: scan for scan in scans}
    labels_by_id = {item.trace_id: set(item.labels) for item in labelled}
    all_modes = sorted(set(FAILURE_MODES) | set().union(*labels_by_id.values() or [set()]))
    per_mode = {mode: {"tp": 0, "fp": 0, "fn": 0} for mode in all_modes}
    cases: list[dict[str, object]] = []

    for trace_id, expected in labels_by_id.items():
        scan = scans_by_id[trace_id]
        predicted = {finding.failure_mode for finding in scan.findings}
        for mode in all_modes:
            if mode in expected and mode in predicted:
                per_mode[mode]["tp"] += 1
            elif mode not in expected and mode in predicted:
                per_mode[mode]["fp"] += 1
            elif mode in expected and mode not in predicted:
                per_mode[mode]["fn"] += 1
        cases.append(
            {
                "trace_id": trace_id,
                "expected": sorted(expected),
                "predicted": sorted(predicted),
                "false_negatives": sorted(expected - predicted),
                "false_positives": sorted(predicted - expected),
                "finding_count": len(scan.findings),
            }
        )

    metrics = {mode: _metric_row(counts) for mode, counts in per_mode.items()}
    micro_counts = {
        "tp": sum(row["tp"] for row in per_mode.values()),
        "fp": sum(row["fp"] for row in per_mode.values()),
        "fn": sum(row["fn"] for row in per_mode.values()),
    }
    return {
        "summary": summarise_scans(scans),
        "micro": _metric_row(micro_counts),
        "per_mode": metrics,
        "cases": cases,
    }


def _metric_row(counts: dict[str, int]) -> dict[str, float | int]:
    tp = counts["tp"]
    fp = counts["fp"]
    fn = counts["fn"]
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {
        **counts,
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
    }
