.PHONY: test scan eval taxonomy

test:
	PYTHONPATH=src python3 -m unittest discover -s tests -v

scan:
	PYTHONPATH=src python3 -m agent_monitor_lab scan data/benchmark/traces --out reports/sample_findings.json

eval:
	PYTHONPATH=src python3 -m agent_monitor_lab eval data/benchmark/traces --labels data/benchmark/labels.json --out reports/sample_eval.json

taxonomy:
	PYTHONPATH=src python3 -m agent_monitor_lab taxonomy

quality:
	PYTHONPATH=src python3 scripts/quality_gate.py
