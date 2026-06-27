# Novelty Positioning

This repo is not trying to be a full static analyzer, a SIEM product, or a generic LLM judge.
The contribution is a compact research lab for coding-agent monitor design.

## What Is Distinctive

- **Trace-native monitoring**: inputs are agent events, tool calls, edits, and messages rather than only source files.
- **Evidence-first findings**: every alert carries a line-linked excerpt and remediation.
- **Agent-specific taxonomy**: labels include test weakening, deceptive completion, and prompt injection alongside security risks.
- **Hierarchical monitor scaffold**: cheap deterministic monitors establish a first-pass triage layer; prompt templates define deeper adjudication.
- **Benchmark-first repo layout**: synthetic labelled traces and metrics are included from the first commit.

## Research Hypotheses

1. Coding-agent monitors should evaluate behavior traces, not only final diffs.
2. Evidence-span output will reduce false-positive review cost compared with label-only monitor judgments.
3. A small taxonomy with high-actionability labels is more useful than a large taxonomy that reviewers cannot apply consistently.
4. Hybrid monitors can improve the cost/latency frontier: deterministic triage first, LLM adjudication second.

## Near-Term Extensions

- Add real anonymized traces from Codex, Claude Code, or Cursor sessions.
- Add LLM-as-judge adapters with structured outputs.
- Fine-tune a small open model on the benchmark format.
- Add red-team generators that mutate benign traces into adversarial variants.
- Track monitor calibration, abstention, and reviewer disagreement.

