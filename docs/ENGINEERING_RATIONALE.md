# Engineering Rationale

This repo is meant to keep monitor decisions inspectable.

## Why the first release is small

The first release deliberately covers a compact monitor loop: parse traces, run deterministic
monitors, attach evidence, and evaluate against labelled examples. I chose that shape because it
keeps the failure path inspectable. A larger system with agents calling agents would look more
impressive, but it would make the core claim harder to check.

## Why deterministic monitors come before LLM monitors

The project is about coding-agent monitoring, not about hiding every decision inside another model.
Deterministic monitors give a baseline that is cheap, reproducible, and easy to audit. The prompt
templates are included so LLM-as-judge experiments can be added later against a stable output
contract.

## Why every finding needs evidence

A monitor that only says "unsafe" is not very useful to an engineer. The finding schema requires
an evidence span and remediation so a reviewer can inspect the exact event and decide whether to
block, warn, or ignore.

## Why fixture tokens are clearly fake

The benchmark needs secret-exposure examples, but public repositories should not contain realistic
provider-token strings. Synthetic examples therefore use explicit `FAKE_*_DO_NOT_USE` fixture values.
The monitor still contains patterns for real credential shapes because users may scan their own
private traces locally, but the public benchmark avoids realistic secret material.

## Commit Standard

For this repo, commit messages should explain the design reason, not only the file diff.

Good commit shape:

```text
Tighten secret fixture safety

Why: the benchmark should teach secret detection without storing realistic provider-token
strings in public data.

Verification: unit tests and benchmark evaluation passed.
```
