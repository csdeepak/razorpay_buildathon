.PHONY: help setup test eval demo demo-benign decide progress

help:
	@echo "razorpay_buildathon (Warden) — available commands:"
	@echo "  make setup        Install dependencies"
	@echo "  make test         Run the test suite"
	@echo "  make demo         Run the attack scenario (matches submission/demo-script.md)"
	@echo "  make demo-benign  Run the benign scenario, for contrast"
	@echo "  make eval         Run the adversarial evaluation harness (Day 11+, see eval/)"
	@echo "  make decide       Reminder to log a new decision — see docs/decisions/"
	@echo "  make progress     Show the current progress tracker"

setup:
	pip install -r requirements.txt

test:
	pytest -q

demo:
	python -m src.cli --scenario attack

demo-benign:
	python -m src.cli --scenario benign

eval:
	@echo "No evaluation harness yet — starts Day 11. See eval/README.md."
	@exit 1

decide:
	@echo "Invented or locked something? Use the /new-decision Claude Code command,"
	@echo "or copy the template in docs/decisions/README.md by hand."

progress:
	@cat docs/progress-tracker.md
