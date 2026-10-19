"""A Slack-channel lurker that speaks up only for bug reports and customer escalations.

    strands-decider serve StrandsAgents/strands-decider-2B-qwen3.5-v1-2610 --port 8099
    BEDROCK_MODEL_MAIN=<inference profile id> python -m interjection_policy.example
"""

import os

from decider_client import DeciderClient
from strands import Agent

from interjection_policy import (InterjectionGate, InterjectionIntervention, RollingWindow,
                                 Thresholds, TieredPolicy, make_interjection_questions)

CHANNEL = [("ana", "morning! coffee machine on 3 is fixed btw"),
           ("ben", "anyone tried the new lunch place?"),
           ("cleo", "checkout returns a 500 for every EU card since the 10:00 deploy"),
           ("dev", "Acme Corp's CTO just emailed, they'll cancel if SSO isn't back today")]

window = RollingWindow(max_tokens=400)
gate = InterjectionGate(
    DeciderClient(),
    make_interjection_questions({"bug_report": "a report of a software bug or outage",
                                 "customer_escalation": "an upset customer threatening to leave"}),
    TieredPolicy({"bug_report": Thresholds(0.8, 0.5),
                  "customer_escalation": Thresholds(0.8, 0.5)}, cooldown_s=0, dedupe=None))
hook = InterjectionIntervention(gate, render_state=lambda _: window.render(),
                                on_result=lambda r: print("   ", r.ticker()))
lurker = Agent(model=os.environ.get("BEDROCK_MODEL_MAIN"), callback_handler=None,
               system_prompt="You lurk in a team channel. When woken, reply in one short line.",
               interventions=[hook])

for user, text in CHANNEL:
    window.add(user, text)
    print(f"[{user}] {text}")
    result = lurker(f"[{user}] {text}")        # denied (no LLM call) unless the gate says SPEAK
    if hook.last_result.wake:
        print(f"  >> lurker: {result}")
