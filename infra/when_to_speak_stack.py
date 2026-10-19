"""One GPU EC2 instance running Decider (localhost only) and the demo app, with Bedrock access.

Everything the deployment needs is in this stack, so `cdk destroy` removes all of it. Settings come
from cdk.json context and can be overridden with `-c key=value` (see infra/README.md).
"""

from __future__ import annotations

from pathlib import Path

from aws_cdk import CfnOutput, Duration, IgnoreMode, Stack, Tags
from aws_cdk import aws_cloudwatch as cw
from aws_cdk import aws_cloudwatch_actions as cw_actions
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_iam as iam
from aws_cdk import aws_s3_assets as s3_assets
from constructs import Construct

REPO_ROOT = Path(__file__).resolve().parent.parent
APP_DIR = "/opt/when-to-speak"
# Never shipped to the instance: whatever git ignores (venvs, model caches, run logs, secrets), plus
# git's own folder and CDK's build output. Patterns use .gitignore syntax.
ASSET_EXCLUDES = [line.strip() for line in (REPO_ROOT / ".gitignore").read_text().splitlines()
                  if line.strip() and not line.startswith("#")] + [".git/", "cdk.out/", "cdk.context.json"]


def bedrock_model_arns(stack: Stack, model_id: str) -> list[str]:
    """ARNs a Bedrock caller needs for `model_id`. A cross-region inference profile id ("us.…",
    "global.…") needs the profile itself plus the foundation model in every region it routes to."""
    prefix, _, base = model_id.partition(".")
    if prefix in ("us", "eu", "apac", "global") and base:
        return [f"arn:aws:bedrock:{stack.region}:{stack.account}:inference-profile/{model_id}",
                f"arn:aws:bedrock:*::foundation-model/{base}"]
    return [f"arn:aws:bedrock:{stack.region}::foundation-model/{model_id}"]


class WhenToSpeakStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        ctx = self.node.try_get_context
        allowed_cidr = ctx("allowed_cidr")
        if not allowed_cidr or allowed_cidr == "0.0.0.0/0":
            raise ValueError("Set -c allowed_cidr=<your.ip.address>/32: the app port is never opened to the world.")
        app_port = int(ctx("app_port"))
        bedrock_model = ctx("bedrock_model")
        idle_stop_minutes = int(ctx("idle_stop_minutes"))
        Tags.of(self).add("project", "strands-decider-when-to-speak")

        # Public subnets only: no NAT gateway to pay for. The instance gets a public IP for the app port.
        vpc = ec2.Vpc(self, "Vpc", max_azs=2, nat_gateways=0,
                      subnet_configuration=[ec2.SubnetConfiguration(name="public", subnet_type=ec2.SubnetType.PUBLIC)])

        sg = ec2.SecurityGroup(self, "AppSg", vpc=vpc, allow_all_outbound=True,
                               description="Demo app port from one CIDR. No SSH: use SSM Session Manager.")
        sg.add_ingress_rule(ec2.Peer.ipv4(allowed_cidr), ec2.Port.tcp(app_port), "Knows When to Speak web app")

        role = iam.Role(self, "InstanceRole", assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
                        managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore")])
        role.add_to_policy(iam.PolicyStatement(
            sid="BedrockConverse",
            actions=["bedrock:InvokeModel", "bedrock:InvokeModelWithResponseStream"],   # also covers Converse(Stream)
            resources=bedrock_model_arns(self, bedrock_model)))

        source = s3_assets.Asset(self, "Source", path=str(REPO_ROOT), exclude=ASSET_EXCLUDES,
                                 ignore_mode=IgnoreMode.GIT)
        source.grant_read(role)

        env = {
            "APP_PORT": str(app_port),
            "AWS_REGION": self.region,
            "LLM_PROVIDER": "bedrock",
            "BEDROCK_MODEL_MAIN": bedrock_model,
            "BEDROCK_MODEL_BASELINE": bedrock_model,
            "BEDROCK_REASONING_EFFORT": ctx("bedrock_effort"),
            "DECIDER_MODEL": ctx("decider_model"),
            "DECIDER_MODEL_ID": ctx("decider_model"),
            "DECIDER_DEVICE": ctx("decider_device"),
            "DECIDER_URL": "http://127.0.0.1:8099",
            "HF_HOME": f"{APP_DIR}/.cache/huggingface",
        }
        user_data = ec2.UserData.for_linux()
        user_data.add_commands(
            "set -euxo pipefail",
            "cat > /etc/when-to-speak.env <<'ENV'",
            *[f"{k}={v}" for k, v in env.items()],
            "ENV",
            "command -v unzip >/dev/null || (apt-get -o DPkg::Lock::Timeout=600 update -q"
            " && apt-get -o DPkg::Lock::Timeout=600 install -yq unzip)",
            f"mkdir -p {APP_DIR}",
            f"aws s3 cp s3://{source.s3_bucket_name}/{source.s3_object_key} /tmp/when-to-speak-src.zip --region {self.region}",
            f"unzip -oq /tmp/when-to-speak-src.zip -d {APP_DIR} && rm /tmp/when-to-speak-src.zip",
            f"bash {APP_DIR}/infra/ec2_setup.sh",
        )

        instance = ec2.Instance(
            self, "Host",
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            instance_type=ec2.InstanceType(ctx("instance_type")),
            machine_image=ec2.MachineImage.from_ssm_parameter(ctx("ami_ssm_parameter")),
            security_group=sg,
            role=role,
            user_data=user_data,
            # A new source asset means a new instance: the deployed code always matches the repo.
            user_data_causes_replacement=True,
            require_imdsv2=True,
            associate_public_ip_address=True,
            block_devices=[ec2.BlockDevice(device_name="/dev/sda1", volume=ec2.BlockDeviceVolume.ebs(
                int(ctx("volume_gb")), volume_type=ec2.EbsDeviceVolumeType.GP3, encrypted=True,
                delete_on_termination=True))],
        )

        if idle_stop_minutes > 0:
            # Stop (not terminate) the instance after it has sat idle, so a forgotten demo stops billing
            # for compute. Start it again with `aws ec2 start-instances`; the disk is kept.
            alarm = cw.Alarm(
                self, "IdleStop",
                metric=cw.Metric(namespace="AWS/EC2", metric_name="CPUUtilization",
                                 dimensions_map={"InstanceId": instance.instance_id},
                                 statistic="Maximum", period=Duration.minutes(5)),
                threshold=float(ctx("idle_cpu_percent")),
                comparison_operator=cw.ComparisonOperator.LESS_THAN_THRESHOLD,
                evaluation_periods=max(1, idle_stop_minutes // 5),
                treat_missing_data=cw.TreatMissingData.NOT_BREACHING,
                alarm_description=f"Stop the Knows When to Speak host after {idle_stop_minutes} idle minutes")
            alarm.add_alarm_action(cw_actions.Ec2Action(cw_actions.Ec2InstanceAction.STOP))

        CfnOutput(self, "AppUrl", value=f"http://{instance.instance_public_dns_name}:{app_port}")
        CfnOutput(self, "InstanceId", value=instance.instance_id)
        CfnOutput(self, "Shell", value=f"aws ssm start-session --target {instance.instance_id} --region {self.region}")
        CfnOutput(self, "Logs", value="sudo tail -f /var/log/when-to-speak-setup.log; journalctl -u decider -u when-to-speak -f")
