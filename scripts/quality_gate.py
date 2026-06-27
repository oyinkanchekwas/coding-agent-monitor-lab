from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKIP_PARTS = {".git", "__pycache__", ".pytest_cache", "reports"}
TEXT_SUFFIXES = {".md", ".py", ".json", ".jsonl", ".toml", ".txt", ".yml", ".yaml", ""}
ALLOW_SPELLING_RULE_FILES = {"scripts/quality_gate.py"}

US_SPELLINGS = {
    "behavior": "behaviour",
    "artifact": "artefact",
    "normalize": "normalise",
    "normalized": "normalised",
    "summarize": "summarise",
    "analyze": "analyse",
    "analyzer": "analyser",
    "optimization": "optimisation",
    "prioritize": "prioritise",
    "specialized": "specialised",
}

REALISTIC_SECRET_PATTERNS = [
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bghp_[A-Za-z0-9_]{20,}\b"),
]

ALLOW_SECRET_PATTERN_FILES = {
    "src/agent_monitor_lab/monitors.py",
}


def main() -> int:
    errors: list[str] = []
    for path in iter_text_files():
        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8")
        lower = text.lower()
        if rel not in ALLOW_SPELLING_RULE_FILES:
            for bad, good in US_SPELLINGS.items():
                if bad in lower:
                    errors.append(f"{rel}: use British English: {bad!r} -> {good!r}")
        if rel not in ALLOW_SECRET_PATTERN_FILES:
            for pattern in REALISTIC_SECRET_PATTERNS:
                if pattern.search(text):
                    errors.append(f"{rel}: realistic secret-shaped string found; use FAKE_*_DO_NOT_USE")
    if errors:
        sys.stderr.write("\n".join(errors) + "\n")
        return 1
    print("Quality gate passed.")
    return 0


def iter_text_files() -> list[Path]:
    paths: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_PARTS for part in path.parts):
            continue
        if path.suffix in TEXT_SUFFIXES:
            paths.append(path)
    return sorted(paths)


if __name__ == "__main__":
    raise SystemExit(main())
