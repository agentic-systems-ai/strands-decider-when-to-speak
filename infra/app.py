#!/usr/bin/env python3
"""CDK entry point: `cd infra && cdk synth -c allowed_cidr=<your ip>/32` (see README.md)."""

import os

import aws_cdk as cdk
from when_to_speak_stack import WhenToSpeakStack

app = cdk.App()
WhenToSpeakStack(
    app, "WhenToSpeakStack",
    # Region only, no account: synth needs no lookups, so no account id lands in cdk.context.json.
    env=cdk.Environment(region=app.node.try_get_context("region") or os.environ.get("CDK_DEFAULT_REGION")),
    description="Knows When to Speak: Strands Decider on a GPU EC2 instance + Amazon Bedrock (demo; tear down with cdk destroy)",
)
app.synth()
