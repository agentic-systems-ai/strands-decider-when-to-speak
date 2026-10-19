# Verified APIs

Checked on 2026-10-13 by reading the installed source, not the blog. Versions:
`strands-decider 0.1.0`, `strands-agents 1.60.0`, `torch 2.11.0+cu128`, `transformers 5.19.0`,
Windows 11 native (no WSL), RTX 3060 12 GB.

## Strands Decider

| Item | Finding | Source |
|---|---|---|
| Install | `pip install strands-decider`. It pulls in a **CPU** torch on Windows; reinstall torch from the `cu128` index for the GPU. | install log |
| Load call | `StrandsDeciderModel.load(path)` in `strands_decider.modeling`. For serving, use `strands_decider.infer.load_engine(checkpoint, device=...)`, which returns a `SystemOneEngine` with `.evaluate(SystemOneRequest)` / `.ask(state, {name: Question})` | `modeling.py`, `infer.py` |
| Question types | pydantic models in `strands_decider.schema`: `NoulQuestion(instructions, criteria={"true":..,"false":..})`, `ChoiceQuestion(instructions, criteria={label: desc})` (2–255 options), `ScoreQuestion(instructions, criteria=[ascending levels])` (2–10). **There is no `Decider.noul(...)` in the package**; that helper is in `examples/strands/_client.py` only. | `schema.py` |
| HTTP server | `strands-decider serve <ckpt> --port N --device cuda`. Binds `127.0.0.1`, single worker, no auth. `GET /health`, `POST /v1/systemone` | `server.py`, `cli.py` |
| Request | `{"state": str or JSON, "questions": {"<key>": {"type": "noul", "instructions": "...", "criteria": {...}}}, "model": "..."}` | `schema.py` |
| Response | `{"model", "answers": {"<key>": ...}, "usage": {"input_tokens", "output_tokens"}, "latency_ms"}`. Noul: `{"type":"noul","noul": P(true)}` (no confidence field). Choice: `{"choice", "probabilities", "confidence"}`. Score: `{"score" (expected level), "legend", "probabilities" keyed by level index, "confidence"}` | `schema.py`, `infer.py` |
| Choice `confidence` | **Normalized** max-probability `(N·p_max − 1)/(N − 1)`, not p_max. Our adapter reports `Decision.confidence = p(top option)` for every type and keeps the full `probs`, so thresholds mean the same thing for noul and choice. | `schema.derive_confidence` |
| Several questions, one state | **Yes, batched.** The state is encoded once (KV cache), then all question suffixes run in one batched forward (up to 32 per chunk). With 1 question, the prefix path is skipped. | `infer.SystemOneEngine.evaluate` |
| Several states, one call | **No.** One state per request, and the server is single-worker. `DeciderClient.ask_many` loops and sets `last_batch_path="loop"`. | `schema.SystemOneRequest`, `server.py` |
| Truncation | The question gets first claim on the window. The state is cut from the right to fit `max_length`. Keep states small. | `infer._fit` |
| Checkpoints | `StrandsAgents/strands-decider-2B-hobson-v19`, `-2B-hobson-v21`, **`-2B-qwen3.5-v1-2610` (newest 2B; JevBench 0.779 vs v19's 0.723, Brier 0.280 vs 0.342)**, plus Gemma 4 E2B/E4B/12B/26B. We default to `2B-qwen3.5-v1-2610` (env `DECIDER_MODEL_ID`). The checkpoint is a LoRA adapter plus head; the base torso downloads on first load. | HF API, upstream README |

## Strands Agents interventions (`strands.interventions`)

| Item | Finding |
|---|---|
| Handler | `class X(InterventionHandler)` with a `name` attribute; override any of `before_invocation`, `before_tool_call`, `after_tool_call`, `before_model_call`, `after_model_call`. Sync or async. `on_error` property: `"throw"` (default) / `"proceed"` / `"deny"`. |
| Wiring | `Agent(interventions=[handler, ...])`. Handlers run in order; `Deny` short-circuits. |
| Actions | `Proceed(reason)`, `Deny(reason)`, `Guide(feedback)`, `Confirm(prompt, response, evaluate)` (tool calls only), `Transform(apply=fn)` |
| Hook around the whole invocation | `before_invocation(event: BeforeInvocationEvent)`; `event.messages` (the incoming messages, writable), `event.invocation_state` (from `agent(prompt, invocation_state={...})`), `event.cancel`. There is no `after_invocation` intervention, only a plain hook. |
| **Gotcha 1** | On `before_invocation`, **`Guide` cancels the call** (sets `cancel = "GUIDANCE: ..."`); it does not inject feedback. To wake the agent with extra context, use **`Transform`** to append to `event.messages`. (`Guide` only injects on `before_model_call`.) |
| **Gotcha 2** | A cancelled invocation appends `{"role": "assistant", "content": [{"text": "DENIED: <reason>"}]}` to `agent.messages` (the user prompt is not added). Repeated silent ticks would stack consecutive assistant turns. `InterjectionIntervention` strips its own denial messages at the start of every invocation. Covered by `tests/test_strands_wiring.py`. |

## Local environment notes

- Port 8000 is used on this machine (DynamoDB Local), so the Decider server runs on **8099** (`DECIDER_URL`).
- No WSL Ubuntu distro is installed; everything runs on native Windows with `uv` + Python 3.12.
- **Hugging Face downloads:** `huggingface_hub` stalled on the 4.5 GB base weights (with Xet, and at
  <1 MB/s without it), while `curl` of the same URL ran at ~6 MB/s. Workaround used here:
  - checkpoint copied to `.models/strands-decider-2B-qwen3.5-v1-2610/` (load by local path; MANIFEST.sha256 verified)
  - base `Qwen/Qwen3.5-2B-Base` curled into a project cache, `.hf_cache/hub/models--Qwen--Qwen3.5-2B-Base/{refs/main,snapshots/<commit>/}`
  - run with `HF_HOME=.hf_cache HF_HUB_OFFLINE=1`
- **Shared GPU:** other hackathon projects on this machine run Decider on the same RTX 3060. Measure
  latency only when the GPU is otherwise idle (`nvidia-smi`), or the numbers are meaningless.

## M0 smoke result (CPU, 2026-10-13)

`scripts/m0_smoke.py`, 7 hand-written windows × 6–7 questions, v1-2610 in-process on the i9-12900F CPU (fp32):
**34/43 agree at p=0.5.**

- Strong: decision_made on an explicit decision (0.94); factual_claim on a stated metric (0.84);
  the vague "someone should look at the deck" hard negative gets action_item 0.05; answered_prior 0.75.
- Weak: **LATEST scoping**. A claim two lines earlier still gives factual_claim 0.84, and open_question
  fires at 0.55–0.74 on lines that aren't questions. off_agenda is missed (0.46 vs launch_date) when the
  header names the current item. already_flagged on a restated item is 0.46.
- Next: iterate question/option wording on the *dev* split (not these 7) and track versions; try
  rendering the LATEST line as its own block. Thresholds per category absorb part of it (open_question
  is note-only by design).
- **Latency: 6.1 s per call on CPU** with transformers' reference kernels: `causal_conv1d` and
  `flash-linear-attention` (Gated DeltaNet) are not installed. The same fallback applies on GPU, so
  installing those kernels (Triton; awkward on native Windows) is a latency item for the 3060/EC2.

## M0 smoke on the GPU (RTX 3060, 2026-10-13)

Same script, in-process with `--device cuda --repeat 3`, GPU otherwise idle (0% util):
- **Same answers** as CPU (every probability within ±0.01), so **34/43** again.
- **Latency: p50 335 ms, p95 395 ms per call** (21 calls, 6–7 questions batched, ~300-token states),
  *still on the reference kernels*. That is inside the spec's 100–300 ms ballpark and fast enough to keep
  up with speech (utterances arrive every ~2–5 s). The fla/causal_conv1d kernels are now a nice-to-have,
  not a blocker.

## Still to verify

- [x] Measured latency on the 3060 at our state sizes: p50 335 ms (see above)
- [ ] Whether `flash-linear-attention` / `causal_conv1d` install on Windows, or only on Linux/EC2
- [ ] Exact Bedrock inference-profile IDs for Opus/Sonnet/Haiku 5.5 in our region (AWS session expired)
- [ ] Transcribe streaming speaker partitioning in our region
- [ ] Polly voices available (generative vs neural) in our region
