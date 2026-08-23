.PHONY: help setup test eval eval-smoke demo demo-benign demo-live fixture decide progress

help:
	@echo "razorpay_buildathon (Warden) — available commands:"
	@echo "  make setup        Install dependencies"
	@echo "  make test         Run the test suite"
	@echo "  make demo         Run the attack scenario (matches submission/demo-script.md)"
	@echo "  make demo-benign  Run the benign scenario, for contrast"
	@echo "  make demo-live    Same, against Razorpay's REAL test-mode API (needs keys + PAYMENT_ID)"
	@echo "  make fixture      Mint the captured test payment demo-live needs"
	@echo "  make eval-smoke   3 case-runs, verifies eval wiring (needs ANTHROPIC_API_KEY)"
	@echo "  make eval         Full adversarial corpus -- COSTS MONEY, read docs/eval-budget.md"
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

fixture:
	python scripts/checkout_fixture.py

# Requires RAZORPAY_KEY_ID/SECRET in .env and a captured payment id:
#   make fixture   -> pay it in the browser -> make demo-live PAYMENT_ID=pay_...
demo-live:
	@test -n "$(PAYMENT_ID)" || (echo "usage: make demo-live PAYMENT_ID=pay_..." && exit 2)
	python -m src.cli --scenario benign --rail razorpay --payment-id $(PAYMENT_ID)

eval-smoke:
	python -m eval.run --smoke

eval:
	@echo "The full corpus is 38 cases x N seeds against a paid model."
	@echo "Recorded results are already in docs/eval-findings.md and eval/runs/ --"
	@echo "only re-run if the corpus or the system under test actually changed."
	@echo "Costs real money. Read docs/eval-budget.md first, then run e.g.:"
	@echo ""
	@echo "  python -m eval.run --model claude-haiku-4-5 --seeds 5"
	@echo "  python -m eval.run --model gemini-3.6-flash --classes denial --limit 3"
	@echo ""
	@echo "Calibrate with --sample N (stratified), never --limit N (prefix)."
	@echo "See docs/eval-findings.md Finding 16 for why that distinction cost 19%."

decide:
	@echo "Invented or locked something? Use the /new-decision Claude Code command,"
	@echo "or copy the template in docs/decisions/README.md by hand."

progress:
	@cat docs/progress-tracker.md
