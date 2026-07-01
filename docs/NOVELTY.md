# Novelty Positioning

This repo is not trying to be a full static analyser, a SIEM product, or a generic LLM judge.
The contribution is a compact research lab for coding-agent monitor design.

## What Is Distinctive

- **Trace-native monitoring**: inputs are agent events, tool calls, edits, and messages rather than only source files.
- **Evidence-first findings**: every alert carries a line-linked excerpt and remediation.
- **Agent-specific taxonomy**: labels include test weakening, deceptive completion, and prompt injection alongside security risks.
- **Hierarchical monitor scaffold**: cheap deterministic monitors establish a first-pass triage layer; prompt templates define deeper adjudication.
- **Benchmark-first repo layout**: synthetic labelled traces and metrics are included from the first commit.

## Research Hypotheses

1. Coding-agent monitors should evaluate behaviour traces, not only final diffs.
2. Evidence-span output will reduce false-positive review cost compared with label-only monitor judgments.
3. A small taxonomy with high-actionability labels is more useful than a large taxonomy that reviewers cannot apply consistently.
4. Hybrid monitors can improve the cost/latency frontier: deterministic triage first, LLM adjudication second.

## Evaluation Boundaries

- The included traces are synthetic and should be treated as benchmark fixtures, not evidence of deployment performance.
- The deterministic monitors are a first-pass triage layer, not a complete safety system.
- Prompt templates are included for review and reproducibility; no API-backed judge runs by default.
- Any future real-trace work needs consent, redaction, provenance notes, and disagreement tracking before it belongs in the public repo.
