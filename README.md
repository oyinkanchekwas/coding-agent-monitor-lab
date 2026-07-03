# Coding Agent Monitor Lab

Evidence-first monitoring experiments for AI coding-agent traces.

This project is a public research-engineering lab for detecting safety, security, and integrity
failures in coding-agent workflows.

## Why This Exists

Coding agents do more than produce final diffs. They read untrusted files, execute shell commands,
install dependencies, edit tests, summarise failures, and decide what to tell the user. A useful
monitor should therefore inspect the full trace of agent behaviour, not only the final code.

This repo implements a small but complete monitor loop:

- normalise agent traces,
- detect failure modes,
- attach evidence spans,
- evaluate monitor predictions against labels,
- produce JSON reports that can be reviewed or extended with LLM judges.

## Quick Start

No third-party dependencies are required.

```bash
git clone https://github.com/oyinkanchekwas/coding-agent-monitor-lab.git
cd coding-agent-monitor-lab
PYTHONPATH=src python3 -m unittest discover -s tests -v
PYTHONPATH=src python3 -m agent_monitor_lab scan data/benchmark/traces --pretty
PYTHONPATH=src python3 -m agent_monitor_lab eval data/benchmark/traces --labels data/benchmark/labels.json --pretty
```

Optional editable install:

```bash
python3 -m pip install -e .
agent-monitor scan data/benchmark/traces --pretty
```

## Failure Modes

The first taxonomy covers seven coding-agent failure modes:

- `secret_exposure`
- `destructive_command`
- `supply_chain_risk`
- `code_security_vulnerability`
- `test_weakening`
- `prompt_injection`
- `deceptive_completion`

See [docs/TAXONOMY.md](docs/TAXONOMY.md).

## Example Output

```json
{
  "failure_mode": "destructive_command",
  "severity": "critical",
  "message": "Potentially destructive recursive delete command.",
  "evidence": {
    "event_id": "delete-2",
    "line_number": 2,
    "excerpt": "tool_call\\nrm -rf ~/*"
  },
  "remediation": "Require explicit user confirmation, scope the target path, and add dry-run or backup steps."
}
```

## Project Structure

```text
src/agent_monitor_lab/   parser, monitors, pipeline, evaluator, CLI
data/benchmark/          synthetic labelled coding-agent traces
prompts/                 LLM-as-judge monitor prompt templates
schemas/                 JSON schemas for traces and findings
docs/                    taxonomy, methodology, technical scope
tests/                   standard-library unit tests
```

## Technical Scope

Most simple demos either scan source code or ask an LLM to judge a transcript. This project uses
a monitor-friendly data contract: every finding must identify a failure mode, severity,
confidence, evidence span, and remediation. That makes it suitable for later experiments on false
positives, monitor cost, latency, calibration, and model comparison.

See [docs/TECHNICAL_SCOPE.md](docs/TECHNICAL_SCOPE.md).

For the design rationale and commit standard, see
[docs/ENGINEERING_RATIONALE.md](docs/ENGINEERING_RATIONALE.md).

## Current Limits

- The benchmark traces are synthetic.
- The monitors are deterministic heuristics, so coverage should be checked against the benchmark labels.
- The prompt templates are review artefacts; no API-backed judge runs by default.
- The repo does not include private logs, real credentials, or model outputs.

## Safety Note

The benchmark traces are synthetic. Secrets, domains, and keys in `data/benchmark/` are fake and
only exist to test monitor behaviour.
