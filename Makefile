PYTHON ?= python
.PHONY: help requirements audit test notebook
help:
	@echo "requirements  Install core notebook dependencies"
	@echo "audit         Recalculate metrics from original saved confusion matrices"
	@echo "test          Run standard-library regression checks"
	@echo "notebook      Open JupyterLab (input data required to train)"
requirements:
	$(PYTHON) -m pip install -r requirements.txt
audit:
	$(PYTHON) scripts/summarize_saved_results.py
test:
	$(PYTHON) -m unittest discover -s tests -v
notebook:
	$(PYTHON) -m jupyterlab
