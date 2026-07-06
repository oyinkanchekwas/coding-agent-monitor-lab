# Methodology

The project uses an evidence-first monitoring design.

## Pipeline

1. Normalise coding-agent logs into trace events.
2. Run fast pattern monitors for high-precision triage.
3. Attach evidence spans to every finding.
4. Evaluate predicted failure modes against trace-level labels.
5. Use prompt templates for slower LLM adjudication where deterministic evidence is ambiguous.

The current repo ships deterministic monitors so the benchmark can run without API keys.
The prompt templates in `prompts/` provide the same output contract for LLM-as-judge review.

## Metrics

The evaluator reports:

- micro precision, recall, and F1,
- per-mode precision, recall, and F1,
- false positives and false negatives by trace,
- finding counts and severity counts.

This is deliberately closer to an empirical research harness than a product demo.
The metrics make monitor changes measurable.

## Design Assumptions

- Coding-agent traces are mixed-trust artefacts. User prompts, issue bodies, repository files,
  tool output, and web content can all contain malicious or misleading instructions.
- Monitoring output must be auditable. A finding without an evidence span is not actionable.
- Hierarchical monitoring keeps slower review focused on suspicious events.
