# Technical Scope

This repo is a compact research lab for coding-agent monitor design. It focuses on trace review,
evidence spans, and benchmarkable findings rather than full static analysis or production SIEM
workflows.

## Project Shape

- **Trace-native monitoring**: inputs are agent events, tool calls, edits, and messages rather than only source files.
- **Evidence-first findings**: every alert carries a line-linked excerpt and remediation.
- **Agent-specific taxonomy**: labels include test weakening, deceptive completion, and prompt injection alongside security risks.
- **Hierarchical monitor scaffold**: cheap deterministic monitors establish a first-pass triage layer; prompt templates define deeper adjudication.
- **Benchmark fixtures**: synthetic labelled traces and metrics are included for repeatable local evaluation.

## Evaluation Questions

1. Can coding-agent monitors catch risky behaviour from traces rather than final diffs alone?
2. Do evidence spans make false positives easier to review?
3. Which labels are actionable enough for a small monitor taxonomy?
4. Where does deterministic triage work well, and where would slower adjudication help?

## Evaluation Boundaries

- The included traces are synthetic and should be treated as benchmark fixtures, not evidence of deployment performance.
- The deterministic monitors are a first-pass triage layer, not a complete safety system.
- Prompt templates are included for review and reproducibility; no API-backed judge runs by default.
- Real-trace datasets are outside this release unless consent, redaction, provenance notes, and
  disagreement tracking are handled first.
