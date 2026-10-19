#!/usr/bin/env bash
# Rehearse the EC2 first boot in a clean Ubuntu 24.04 container, without an AWS GPU instance.
#
#   bash infra/test_bootstrap_docker.sh            # needs Docker with --gpus, the CDK CLI and AWS credentials
#   HOLD=1 bash infra/test_bootstrap_docker.sh     # run first boot but don't start the services yet
#   bash infra/test_bootstrap_docker.sh --start    # then start them (e.g. once the GPU is free)
#
# What is real: the source bundle (the repo minus .gitignore, like the CDK asset), the env file
# (taken from the synthesized template's user data), infra/ec2_setup.sh, the systemd unit
# definitions, Decider on the GPU and Amazon Bedrock. What is stood in: the AMI (plain Ubuntu plus
# python3, curl, sudo, unzip), systemd (a small systemctl that starts each unit's ExecStart as its
# User), and the instance role (your temporary credentials, passed as environment variables).
#
# The app ends up on http://127.0.0.1:18080. Remove the container with `docker rm -f wts-boot`.
set -euo pipefail
cd "$(dirname "$0")/.."
NAME=wts-boot
PORT=${PORT:-18080}
PROFILE=${AWS_PROFILE:-default}
export MSYS_NO_PATHCONV=1
PY=${PYTHON:-$( [ -x .venv/Scripts/python.exe ] && echo .venv/Scripts/python.exe || echo .venv/bin/python )}
export PATH="$PWD/infra/.venv/Scripts:$PWD/infra/.venv/bin:$PATH"   # aws-cdk-lib for `cdk synth`

wait_ready() {
  echo "== wait for Decider and the app"
  for i in $(seq 1 120); do
    docker exec "$NAME" curl -sf http://127.0.0.1:8099/health >/dev/null 2>&1 && break
    sleep 5
  done
  docker exec "$NAME" curl -s http://127.0.0.1:8099/health; echo
  for i in $(seq 1 60); do curl -sf "http://127.0.0.1:$PORT/api/meetings" >/dev/null && break; sleep 2; done
  echo "app: $(curl -s "http://127.0.0.1:$PORT/api/meetings" | "$PY" -c 'import json,sys; print(len(json.load(sys.stdin)), "meetings")')"
  echo "== ready: http://127.0.0.1:$PORT  (logs: docker exec $NAME tail -f /var/log/decider.log /var/log/when-to-speak.log)"
}

if [ "${1:-}" = --start ]; then
  docker exec "$NAME" bash -c 'rm -f /etc/wts-hold && systemctl $(cat /var/lib/wts-pending)'
  wait_ready
  exit 0
fi

WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT
# Git Bash: give Docker Windows paths for host files (container paths stay as written).
host() { if command -v cygpath >/dev/null; then cygpath -w "$1"; else echo "$1"; fi; }

echo "== synthesize the stack and read its env file"
(cd infra && cdk synth -c allowed_cidr=203.0.113.7/32 --quiet >/dev/null)
"$PY" - "$(host "$WORK/when-to-speak.env")" <<'PYCODE'
import json, sys
t = json.load(open("infra/cdk.out/WhenToSpeakStack.template.json"))
host = next(r for r in t["Resources"].values() if r["Type"] == "AWS::EC2::Instance")
parts = host["Properties"]["UserData"]["Fn::Base64"]["Fn::Join"][1]
script = "".join(p for p in parts if isinstance(p, str))
env = script.split("cat > /etc/when-to-speak.env <<'ENV'\n", 1)[1].split("\nENV", 1)[0]
open(sys.argv[1], "w", newline="\n").write(env + "\n")
print(env)
PYCODE

echo "== bundle the source (what git tracks or would track, like the CDK asset)"
git ls-files --cached --others --exclude-standard -z | tar --null -T - -cf "$WORK/src.tar"

cat > "$WORK/systemctl" <<'SH'
#!/usr/bin/env bash
# Stand-in for systemd: `enable --now a.service ...` starts each unit's ExecStart as its User.
[ "${1:-}" = enable ] || exit 0
if [ -f /etc/wts-hold ]; then echo "$@" > /var/lib/wts-pending; echo "held: $*"; exit 0; fi
for unit in "$@"; do
  f="/etc/systemd/system/$unit"; [ -f "$f" ] || continue
  get() { sed -n "s/^$1=//p" "$f" | head -1; }
  envs=$(sed -n 's/^Environment=//p' "$f" | tr '\n' ' ')
  # root opens the log (systemd would use the journal); the unit's command runs as its User, with
  # the instance role's stand-in credentials from /etc/wts-aws.env.
  nohup su -s /bin/bash "$(get User)" -c "cd '$(get WorkingDirectory)' && set -a && . '$(get EnvironmentFile)' && . /etc/wts-aws.env && set +a && export $envs; exec $(get ExecStart)" \
    > "/var/log/${unit%.service}.log" 2>&1 &
  echo "started $unit"
done
SH

echo "== start a clean Ubuntu 24.04 container with the GPU"
docker rm -f "$NAME" >/dev/null 2>&1 || true
docker run -d --name "$NAME" --gpus all -p "127.0.0.1:$PORT:8080" \
  $(aws configure export-credentials --profile "$PROFILE" --format env-no-export | grep -v EXPIRATION | sed 's/^/-e /') \
  ubuntu:24.04 sleep infinity >/dev/null
docker cp "$(host "$WORK/src.tar")" "$NAME:/tmp/src.tar"
docker cp "$(host "$WORK/when-to-speak.env")" "$NAME:/etc/when-to-speak.env"
docker cp "$(host "$WORK/systemctl")" "$NAME:/usr/local/bin/systemctl"
# The instance role's stand-in: temporary credentials in a file the services source, not on their
# command lines (where `ps` would show them).
docker exec "$NAME" bash -c 'env | grep -E "^AWS_(ACCESS_KEY_ID|SECRET_ACCESS_KEY|SESSION_TOKEN)=" > /etc/wts-aws.env'
[ -n "${HOLD:-}" ] && docker exec "$NAME" touch /etc/wts-hold

echo "== stand in for the AMI, then run the real first-boot script"
docker exec "$NAME" bash -c '
  set -e
  apt-get update -q >/dev/null && DEBIAN_FRONTEND=noninteractive apt-get install -yq python3 curl sudo unzip ca-certificates >/dev/null
  chmod +x /usr/local/bin/systemctl
  mkdir -p /opt/when-to-speak && tar -xf /tmp/src.tar -C /opt/when-to-speak && rm /tmp/src.tar
  bash /opt/when-to-speak/infra/ec2_setup.sh'

if [ -n "${HOLD:-}" ]; then
  echo "== first boot done; services held. Start them with: bash infra/test_bootstrap_docker.sh --start"
else
  wait_ready
fi
