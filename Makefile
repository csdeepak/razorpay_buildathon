.PHONY: help setup test eval demo decide progress

help:
	@echo "razorpay_buildathon — available commands:"
	@echo "  make setup     Install dependencies (wired up once the stack is chosen, Day 6+)"
	@echo "  make test      Run the test suite (wired up once src/ exists)"
	@echo "  make eval      Run the adversarial evaluation harness (Day 11+, see eval/)"
	@echo "  make demo      Run the demo scenario (Day 13+, must match submission/demo-script.md)"
	@echo "  make decide    Reminder to log a new decision — see docs/decisions/"
	@echo "  make progress  Show the current progress tracker"

setup:
	@echo "No stack chosen yet — record the choice as an ADR in docs/decisions/, then wire this target."
	@exit 1

test:
	@echo "No source yet — src/ is empty until the Day 5 problem lock. See docs/progress-tracker.md."
	@exit 1

eval:
	@echo "No evaluation harness yet — starts Day 11. See eval/README.md."
	@exit 1

demo:
	@echo "No demo yet — write submission/demo-script.md at the Day 5 lock before building this."
	@exit 1

decide:
	@echo "Invented or locked something? Use the /new-decision Claude Code command,"
	@echo "or copy the template in docs/decisions/README.md by hand."

progress:
	@cat docs/progress-tracker.md
