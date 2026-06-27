from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

from agent_monitor_lab.models import TraceEvent


def iter_trace_files(paths: Iterable[str | Path]) -> list[Path]:
    files: list[Path] = []
    for item in paths:
        path = Path(item)
        if path.is_dir():
            files.extend(sorted(child for child in path.rglob("*") if child.suffix in {".jsonl", ".txt", ".log"}))
        elif path.exists():
            files.append(path)
    return sorted(dict.fromkeys(files))


def parse_trace_file(path: str | Path) -> tuple[TraceEvent, ...]:
    trace_path = Path(path)
    events: list[TraceEvent] = []
    with trace_path.open("r", encoding="utf-8") as handle:
        for line_number, raw_line in enumerate(handle, start=1):
            line = raw_line.strip()
            if not line:
                continue
            events.append(_parse_line(line, trace_path, line_number))
    return tuple(events)


def _parse_line(line: str, source: Path, line_number: int) -> TraceEvent:
    try:
        payload = json.loads(line)
    except json.JSONDecodeError:
        payload = {"content": line, "actor": "unknown", "action": "message"}

    if not isinstance(payload, dict):
        payload = {"content": str(payload), "actor": "unknown", "action": "message"}

    metadata = _metadata_without_core(payload)
    event_id = str(payload.get("id") or payload.get("event_id") or f"{source.stem}:{line_number}")
    return TraceEvent(
        event_id=event_id,
        source=str(source),
        line_number=line_number,
        actor=str(payload.get("actor", "unknown")),
        action=str(payload.get("action", "message")),
        content=str(payload.get("content", "")),
        command=_optional_string(payload.get("command")),
        path=_optional_string(payload.get("path")),
        metadata=metadata,
    )


def _optional_string(value: Any) -> str | None:
    if value is None:
        return None
    return str(value)


def _metadata_without_core(payload: dict[str, Any]) -> dict[str, Any]:
    core = {"id", "event_id", "actor", "action", "content", "command", "path"}
    return {key: value for key, value in payload.items() if key not in core}

