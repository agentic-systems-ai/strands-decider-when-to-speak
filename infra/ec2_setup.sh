#!/usr/bin/env bash
# First-boot setup for the Knows When to Speak host (run by EC2 user data as root; safe to re-run).
# Expects the repo in /opt/when-to-speak and settings in /etc/when-to-speak.env (written by the CDK stack).
set -euxo pipefail
exec > >(tee -a /var/log/when-to-speak-setup.log) 2>&1

APP_DIR=/opt/when-to-speak
UV_VERSION=0.12.13

id whentospeak &>/dev/null || useradd --system --home-dir "$APP_DIR" --shell /usr/sbin/nologin whentospeak
mkdir -p "$APP_DIR/.cache" "$APP_DIR/runs"

# uv, pinned, installed system-wide
if ! command -v uv &>/dev/null; then
  curl -LsSf "https://astral.sh/uv/${UV_VERSION}/install.sh" | env UV_INSTALL_DIR=/usr/local/bin INSTALLER_NO_MODIFY_PATH=1 sh
fi

set -a; . /etc/when-to-speak.env; set +a
DEVICE="${DECIDER_DEVICE:-cuda}"

cd "$APP_DIR"
# If uv has to download Python, keep it where the service user can read it (not in /root).
export UV_PYTHON_INSTALL_DIR="$APP_DIR/.uv-python"
uv venv --allow-existing --python 3.12 .venv
if [ "$DEVICE" = cuda ]; then
  # Triton (pulled in by torch on Linux) compiles a C helper with a C compiler against Python.h on
  # Decider's first call; the DLAMI has no Python headers (and build-essential keeps gcc certain).
  # First boot races unattended-upgrades for the dpkg lock, and the AMI's package lists are stale.
  apt-get -o DPkg::Lock::Timeout=600 update
  DEBIAN_FRONTEND=noninteractive apt-get -o DPkg::Lock::Timeout=600 install -y python3.12-dev build-essential
  # On Linux the default PyPI torch wheel bundles CUDA, so no extra index is needed.
  uv pip install --python .venv/bin/python -e ".[decider,app]"
  # Optional faster kernels for Decider on Linux; the app still works without them.
  uv pip install --python .venv/bin/python -e ".[fast]" || echo "fast kernels not installed; continuing"
  .venv/bin/python -c "import torch; assert torch.cuda.is_available(), 'CUDA not available'; print(torch.cuda.get_device_name(0))"
else
  uv pip install --python .venv/bin/python --torch-backend cpu -e ".[decider,app]"
fi

chown -R whentospeak:whentospeak "$APP_DIR"

# Download Decider now, so the first replay doesn't wait: the checkpoint is a LoRA adapter, and its
# base model (named in lora/adapter_config.json) is the multi-GB part.
sudo -u whentospeak env HF_HOME="$HF_HOME" DECIDER_MODEL="$DECIDER_MODEL" .venv/bin/python - <<'PY' || echo "prefetch failed; decider.service will download it"
import json, os
from huggingface_hub import snapshot_download
path = snapshot_download(os.environ["DECIDER_MODEL"])
cfg = os.path.join(path, "lora", "adapter_config.json")
if os.path.exists(cfg):
    base = json.load(open(cfg)).get("base_model_name_or_path")
    if base:
        print("base model:", base, snapshot_download(base))
PY

install -m 0644 infra/systemd/decider.service infra/systemd/when-to-speak.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable --now decider.service when-to-speak.service
