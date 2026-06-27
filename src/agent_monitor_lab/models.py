from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any


class Severity(str, Enum):
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass(frozen=True)
class TraceEvent:
    """One normalised event from a coding-agent trace."""

    event_id: str
    source: str
    line_number: int
    actor: str = "unknown"
    action: str = "message"
    content: str = ""
    command: str | None = None
    path: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def searchable_text(self) -> str:
        parts = [
            self.actor,
            self.action,
            self.content,
            self.command or "",
            self.path or "",
            " ".join(f"{k}={v}" for k, v in self.metadata.items()),
        ]
        return "\n".join(part for part in parts if part)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class EvidenceSpan:
    event_id: str
    source: str
    line_number: int
    excerpt: str
    start: int | None = None
    end: int | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class MonitorFinding:
    finding_id: str
    monitor: str
    failure_mode: str
    severity: Severity
    confidence: float
    message: str
    evidence: EvidenceSpan
    remediation: str
    tags: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["severity"] = self.severity.value
        return data


@dataclass(frozen=True)
class TraceScan:
    source: Path
    events: tuple[TraceEvent, ...]
    findings: tuple[MonitorFinding, ...]

    @property
    def trace_id(self) -> str:
        return self.source.stem

    def to_dict(self) -> dict[str, Any]:
        return {
            "trace_id": self.trace_id,
            "source": str(self.source),
            "event_count": len(self.events),
            "finding_count": len(self.findings),
            "findings": [finding.to_dict() for finding in self.findings],
        }
