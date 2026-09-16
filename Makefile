PYTHON ?= python3

.PHONY: preflight install

preflight:
	$(PYTHON) scripts/preflight.py

install:
	$(PYTHON) -m pip install -r requirements.txt
