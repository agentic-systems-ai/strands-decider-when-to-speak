# Deploying Knows When to Speak on AWS

One CDK stack (Python) puts the whole demo on one GPU instance:

```
 your browser ──► :8080  EC2 g6.xlarge (NVIDIA L4, Deep Learning AMI, Ubuntu 24.04)
   (one IP only)          ├─ when-to-speak.service   FastAPI + WebSocket demo app (the meeting agent)
                          ├─ decider.service         Strands Decider, bound to 127.0.0.1:8099
                          └─ instance role ────────► Amazon Bedrock (gpt-oss-20b by default)
```

Everything is in the stack, so `cdk destroy` removes all of it: VPC (public subnets, no NAT
gateway), security group, IAM role, the instance and its disk, and an idle-stop alarm. There is
no SSH key and no port 22; you get a shell through SSM Session Manager.

> **Status:** deployed, tested and destroyed on 2026-10-16 (us-east-2). First boot took about 3
> minutes. The app replayed a full meeting with real Decider and Bedrock calls, and the Decider
> measured 163 / 184 ms p50 / p95 on the L4 over the 2,125 dev windows. Numbers in
> [`docs/RESULTS.md`](../docs/RESULTS.md#decider-latency-by-hardware).

## Rehearse first boot locally

`bash infra/test_bootstrap_docker.sh` runs the real first boot in a clean Ubuntu 24.04 container
with your GPU: the source bundle the CDK asset would ship, the env file from the synthesized user
data, `ec2_setup.sh`, and the systemd units (started by a small stand-in `systemctl`), with your
temporary AWS credentials standing in for the instance role. It ends with the app on
`http://127.0.0.1:18080`. `HOLD=1` stops before starting the services, and `--start` starts them
later (for example, once the GPU is free). Remove it with `docker rm -f wts-boot`.

What it caught: Triton needs a C compiler and Python headers for its first Decider call (now
installed), and the Decider checkpoint is a LoRA adapter whose 4.3 GB base model also has to be
prefetched. Measured in the container on an RTX 3060: Decider p50 283 ms with the Linux fast
kernels. One line in the first replay took 13 s, most likely Triton compiling and tuning kernels
for a new input shape (not confirmed), so expect a few slow lines on a fresh host.

## Before the first deploy

1. **GPU quota.** New accounts have 0 vCPUs for "Running On-Demand G and VT instances". A
   g6.xlarge needs 4. Request it in the Service Quotas console (EC2, quota code `L-DB2E81BA`) in
   your region; approval can take a few days.
2. **Bedrock model access** to the model in `bedrock_model` (default `openai.gpt-oss-20b-1:0`) in
   the same region.
3. **Tools:** Node.js with the CDK CLI (`npm i -g aws-cdk`), Python 3.11+, and AWS credentials.
4. **Bootstrap** the account and region once: `cdk bootstrap aws://<account-id>/us-east-2`.

```bash
cd infra
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cdk synth -c allowed_cidr=$(curl -s https://checkip.amazonaws.com)/32     # check the template
```

## Deploy, demo, tear down

```bash
cdk deploy -c allowed_cidr=$(curl -s https://checkip.amazonaws.com)/32
# Outputs: AppUrl, InstanceId, Shell (SSM command), Logs
```

First boot installs the Python environment and downloads Decider and its base model (about
10 minutes in the local rehearsal). Watch it with the `Shell` output command, then
`sudo tail -f /var/log/when-to-speak-setup.log`. When `journalctl -u when-to-speak` shows Uvicorn
running, open `AppUrl`, pick a meeting and press Start. The first replay warms Decider up.

To measure Decider latency on the instance for the article:

```bash
cd /opt/when-to-speak && sudo -u whentospeak .venv/bin/python scripts/eval_decider.py predict --split dev --backend decider --limit 300
sudo -u whentospeak .venv/bin/python scripts/eval_decider.py report --split dev --backend decider
```

Then tear it all down:

```bash
cdk destroy          # removes everything in the stack; nothing is left running
```

The CDK bootstrap bucket keeps the uploaded source zip (about 11 MB) until you empty it yourself.

## Settings

All in `cdk.json` under `context`; override any of them with `-c key=value`.

| Key | Default | What |
|---|---|---|
| `allowed_cidr` | *(required)* | The only address range that can reach the app port. `0.0.0.0/0` is refused. |
| `region` | `us-east-2` | Where the stack goes. Needs the GPU quota and the Bedrock model. |
| `instance_type` | `g6.xlarge` | `g5.xlarge` (A10G) also works. |
| `bedrock_model` | `openai.gpt-oss-20b-1:0` | The agent's LLM. A Claude inference profile such as `us.anthropic.claude-sonnet-5-5` works too; the IAM policy follows the id. |
| `bedrock_effort` | `low` | Reasoning effort for gpt-oss (`low`, `medium`, `high`). |
| `decider_model` | `StrandsAgents/strands-decider-2B-qwen3.5-v1-2610` | Decider checkpoint. |
| `decider_device` | `cuda` | `cpu` runs Decider without a GPU (CPU-only torch; much slower) on e.g. `c7i.2xlarge`. |
| `idle_stop_minutes` | `60` | Stop the instance after this long with max CPU below `idle_cpu_percent`; `0` disables it. |
| `volume_gb` | `100` | Root disk (gp3, encrypted). |
| `app_port` | `8080` | The app port opened to `allowed_cidr`. |

The source bundle is the repo minus everything `.gitignore` lists (venvs, model caches, run
logs, secrets). Changing the source or any setting and running `cdk deploy` again replaces the
instance, so what runs always matches the repo.

## What it costs (us-east-2, on-demand)

| Item | Price | Notes |
|---|---|---|
| g6.xlarge | $0.80 / hour while running | The idle-stop alarm stops it after an idle hour. |
| 100 GB gp3 disk | $8 / month (~$0.27 / day) | Billed while the stack exists, even when stopped. |
| Public IPv4 address | $0.005 / hour while running | |
| Bedrock gpt-oss-20b | $0.07 / $0.30 per million input / output tokens | One 10-minute meeting replay used about 50k tokens: under $0.01. |

A stopped instance keeps its disk; start it with `aws ec2 start-instances --instance-ids <id>`
(the public address changes; read the new one from the EC2 console). For the lowest cost, run
`cdk destroy` when you're done and deploy again when you need it.
