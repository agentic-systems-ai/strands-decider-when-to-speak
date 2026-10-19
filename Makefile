PY ?= .venv/Scripts/python.exe
DECIDER_MODEL ?= StrandsAgents/strands-decider-2B-qwen3.5-v1-2610
DECIDER_PORT ?= 8099
DEVICE ?= cuda

.PHONY: setup serve smoke test dataset ollama-check pilot data eval-dev eval-test agent demo

setup:            ## venv + deps (CUDA torch on Windows/Linux)
	uv venv --python 3.12 .venv
	uv pip install --python $(PY) -e ".[decider,app,eval,dev]"
	uv pip install --python $(PY) --reinstall torch --index-url https://download.pytorch.org/whl/cu128

serve:            ## Decider server on localhost only
	.venv/Scripts/strands-decider serve $(DECIDER_MODEL) --port $(DECIDER_PORT) --device $(DEVICE)

smoke:            ## hand-written windows through the 7 questions
	$(PY) scripts/m0_smoke.py --url http://127.0.0.1:$(DECIDER_PORT)

test:
	$(PY) -m pytest -q

dataset:          ## prebuilt eval set: data/authored/*.md -> meetings + dev/test windows
	$(PY) scripts/build_dataset.py

ollama-check:     ## is the local LLM up? (LLM_PROVIDER=ollama, the default)
	curl -s $${OLLAMA_HOST:-http://127.0.0.1:11434}/api/tags

pilot:            ## simulator (online generation): 3 meetings to read
	$(PY) scripts/gen_meetings.py --pilot --workers 3

data:             ## simulator (online generation): 48-meeting grid (cached LLM calls)
	$(PY) scripts/gen_meetings.py --grid --workers 6

eval-dev:         ## Decider + LLM baseline on dev, charts
	$(PY) scripts/eval_decider.py predict --split dev --backend decider
	$(PY) scripts/eval_decider.py predict --split dev --backend judge --limit 600
	$(PY) scripts/eval_decider.py report --split dev

eval-test:
	$(PY) scripts/eval_decider.py predict --split test --backend decider
	$(PY) scripts/eval_decider.py report --split test --backend decider

agent:            ## headless agent over test meetings
	$(PY) scripts/run_agent.py --split test

demo:             ## demo UI on http://127.0.0.1:8080 (needs `make serve` running)
	$(PY) -m when_to_speak.app --port 8080
