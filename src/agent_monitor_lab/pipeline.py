from __future__ import annotations

from pathlib import Path
from typing import Iterable

from agent_monitor_lab.models import MonitorFinding, Severity, TraceScan
from agent_monitor_lab.monitors import DEFAULT_MONITORS, BaseMonitor
from agent_monitor_lab.parser import iter_trace_files, parse_trace_file


class MonitorPipeline:
    """Two-stage monitor pipeline for coding-agent traces.

    The current implementation uses deterministic monitors for both triage and
    evidence extraction. Prompt templates in prompts/ show where LLM judges can
    be added without changing the output contract.
    """

    def __init__(self, monitors: Iterable[BaseMonitor] = DEFAULT_MONITORS) -> None:
        self.monitors = tuple(monitors)

    def scan_file(self, path: str | Path) -> TraceScan:
        source = Path(path)
        events = parse_trace_file(source)
        findings: list[MonitorFinding] = []
        for monitor in self.monitors:
            findings.extend(monitor.scan(events))
        return TraceScan(source=source, events=events, findings=tuple(_dedupe_and_sort(findings)))

    def scan_paths(self, paths: Iterable[str | Path]) -> tuple[TraceScan, ...]:
        return tuple(self.scan_file(path) for path in iter_trace_files(paths))


def default_pipeline() -> MonitorPipeline:
    return MonitorPipeline()


def summarise_scans(scans: Iterable[TraceScan]) -> dict[str, object]:
    scans = tuple(scans)
    findings = [finding for scan in scans for finding in scan.findings]
    by_mode: dict[str, int] = {}
    by_severity: dict[str, int] = {}
    for finding in findings:
        by_mode[finding.failure_mode] = by_mode.get(finding.failure_mode, 0) + 1
        by_severity[finding.severity.value] = by_severity.get(finding.severity.value, 0) + 1
    return {
        "trace_count": len(scans),
        "event_count": sum(len(scan.events) for scan in scans),
        "finding_count": len(findings),
        "by_failure_mode": dict(sorted(by_mode.items())),
        "by_severity": _ordered_severity_counts(by_severity),
    }


def _dedupe_and_sort(findings: Iterable[MonitorFinding]) -> list[MonitorFinding]:
    seen: set[str] = set()
    unique: list[MonitorFinding] = []
    for finding in findings:
        if finding.finding_id in seen:
            continue
        seen.add(finding.finding_id)
        unique.append(finding)
    return sorted(unique, key=lambda item: (_severity_sort_key(item.severity), item.failure_mode, item.finding_id), reverse=True)


def _severity_sort_key(severity: Severity) -> int:
    return {
        Severity.CRITICAL: 4,
        Severity.HIGH: 3,
        Severity.MEDIUM: 2,
        Severity.LOW: 1,
        Severity.INFO: 0,
    }[severity]


def _ordered_severity_counts(counts: dict[str, int]) -> dict[str, int]:
    order = ["critical", "high", "medium", "low", "info"]
    return {severity: counts[severity] for severity in order if severity in counts}
