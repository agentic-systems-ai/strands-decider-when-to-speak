---
meeting_id: postmortem-checkout-d2-s1
theme: "Incident postmortem: the checkout outage last Tuesday"
domain_pack: incident_review
drama: 0.2
seed: 1
author: claude-opus-5-5 (Claude Code session)
pack:
  title: Postmortem - checkout outage (Tuesday)
  org: Larkspur Goods (fictional online retailer)
  agenda:
    - {id: timeline, title: Incident timeline, goal: Agree what happened and when, timebox_min: 4}
    - {id: root_cause, title: Root cause and contributing factors, goal: Understand why the bad config reached production, timebox_min: 5}
    - {id: customer_impact, title: Customer impact and comms, goal: Size the impact and decide on customer follow-up, timebox_min: 4}
    - {id: remediation, title: Remediation and follow-ups, goal: Agree owners for the fixes, timebox_min: 4}
  facts:
    - {id: F1, key: outage_duration, statement: "Checkout outage lasted 47 minutes", value: "47 minutes"}
    - {id: F2, key: outage_start, statement: "Outage started at 14:12 UTC", value: "14:12 UTC"}
    - {id: F3, key: page_fired, statement: "On-call was paged at 14:21 UTC", value: "14:21 UTC"}
    - {id: F4, key: failed_checkouts, statement: "Failed checkout attempts = 18,400", value: "18,400"}
    - {id: F5, key: revenue_at_risk, statement: "Estimated revenue at risk = $212,000", value: "$212,000"}
    - {id: F6, key: error_rate_peak, statement: "Peak checkout error rate = 64%", value: "64%"}
    - {id: F7, key: support_tickets, statement: "Support tickets about the outage = 1,130", value: "1,130"}
    - {id: F8, key: config_change_id, statement: "The bad change was CHG-4471", value: "CHG-4471"}
    - {id: F9, key: rollback_duration, statement: "Rollback took 6 minutes once started", value: "6 minutes"}
    - {id: F10, key: affected_regions, statement: "Regions affected = 2 (us-east, eu-west)", value: "2"}
    - {id: F11, key: monthly_sla_target, statement: "Monthly checkout availability target = 99.95%", value: "99.95%"}
    - {id: F12, key: previous_same_cause, statement: "A previous incident with the same cause happened on March 3", value: "March 3"}
personas:
  - name: Ana
    role: SRE manager, facilitates the postmortem
    goals: A blameless review with real follow-ups
    hidden_agenda: Wants budget for a config validation service
    verbosity: 3
    wpm: 150
    catchphrases: ["let's stay blameless", "okay"]
    voice_gender: female
  - name: Ben
    role: On-call engineer during the incident
    goals: Explain what he saw without being blamed
    hidden_agenda: Felt alone on the call for the first ten minutes
    verbosity: 2
    wpm: 145
    catchphrases: ["from what I saw"]
    voice_gender: male
  - name: Kofi
    role: Payments engineering lead
    goals: Fix the deploy path for payment config
    hidden_agenda: His team approved the change
    verbosity: 3
    wpm: 155
    catchphrases: ["in fairness", "the short version"]
    voice_gender: male
  - name: Mei
    role: Customer support lead
    goals: Get customers a clear answer and a goodwill gesture
    hidden_agenda: Her team was blindsided by the outage
    verbosity: 3
    wpm: 160
    catchphrases: ["from the customer side"]
    voice_gender: female
---
## timeline :: Reconstruct the timeline; Ben misremembers the duration
Ana: Okay, thanks for making time. Let's stay blameless, we're here to fix the system, not find a person.
Kofi: Appreciated.
Ana: Let's start with the timeline. Ben, you were on call, can you walk us through it? {question- @+1}
Ben: Sure. From what I saw, errors started at twelve past two UTC. {claim- F2} {~}
Kofi: And the alert didn't go to Ben first, it went to the old payments rotation.
Ana: Okay, so when did you actually get paged? {question- @+1}
Ben: The page fired at fourteen twenty-one. So about nine minutes after it started. {claim- F3} {~nc}
Mei: Support saw it before that, for what it's worth. The chat queue spiked almost immediately.
Ana: That's useful. Did support have a way to tell engineering? {question- @+1}
Mei: Not really. We posted in the incidents channel but nobody was watching it yet.
Ana: Okay, noting that as a gap.
Kofi: Sorry, someone's at my door, one second. {drift- 1}
Ben: Once I was on, the error rate was obviously way up. Dashboards were all red.
Kofi: In fairness, the dashboard was red for both regions, so it wasn't a single bad host. {claim- F10}
Ana: And how long was checkout down overall? {question- @+1}
Ben: About half an hour, start to finish. {claim+ F1 "half an hour"}
Ana: I have forty-seven minutes in the incident doc. {claim- F1}
Ben: Oh, right, I was counting from when I joined, not from the start.
Kofi: That's fair, it felt shorter from inside the call.
Ana: When did we decide to roll back? {question- @+1}
Ben: Once Kofi joined. He spotted the config change pretty fast.
Kofi: The short version is, the change was the only deploy in that window, so it was the obvious suspect.
Ana: And the rollback itself was quick? {question- @+1}
Kofi: Six minutes once we started it. {claim- F9}
Mei: From the customer side, it was a bit longer, because carts had to be retried.
Ana: Okay. So, the timeline is roughly agreed, with the paging gap as the first thing to dig into. {decision-}
Ben: Yeah, that's accurate.
## root_cause :: The bad config change, why review missed it, and the repeat incident
Ana: Root cause. Kofi, what was in the change? {question- @+1}
Kofi: CHG-4471. It updated the payment provider timeout from milliseconds to seconds, but the value wasn't converted. {claim- F8}
Ben: So it was set to five thousand seconds instead of five seconds? {question- @+1} {~}
Kofi: Effectively, yes. Every checkout call waited until the gateway gave up.
Ana: How did that get through review? {question- @+1}
Kofi: In fairness, the diff looked tiny. One line. The reviewer approved it in a couple of minutes.
Mei: Is there any validation on those config values at all? {question- @+1}
Kofi: Type checks, yes. Range checks, no.
Ana: And this isn't the first time, right? We had something similar before. {question- @+1}
Kofi: Yeah, there was the one in February with the retry config, same kind of thing. {claim+ F12 "February"}
Ana: I think that was March third, actually. The retry limit one. {claim- F12}
Kofi: You're right, March. Early March. {claim- F12}
Ben: So we've had the same root cause twice in a few months.
Ana: Which is exactly why this matters. Let's stay blameless, but that's a pattern.
Kofi: Agreed. And in fairness, the fix from March was a wiki page, not a guardrail. {claim- F12}
Mei: Out of curiosity, did the new office badge readers ever get fixed? Mine still doesn't work. {drift+ 3} {question- @+1}
Ben: Mine works on the second floor but not the third. {~nc}
Kofi: Facilities said next week, but they've been saying that for a month.
Ana: Okay, let's get back to it. Was there a staged rollout for this change? {question- @+1}
Kofi: No. Payment config goes to all regions at once. That's the deeper problem.
Ana: So two regions went down together instead of one. {claim- F10}
Ben: Which is why there was nothing healthy to fail over to.
Ana: Okay. Should we require staged rollouts for payment config? {question- @+1}
Kofi: I think we have to. Maybe one region first with a fifteen-minute bake. {decision-}
Ben: Fifteen minutes would have caught this one easily. {~}
Ana: Let's hold that thought for remediation, but I think everyone agrees on the direction. {decision-}
Kofi: Someone should really audit the other payment config values too, there might be more unit mismatches. {action-}
## customer_impact :: Size the impact; Mei overstates the tickets; decide on goodwill credits
Ana: Okay, customer impact. Mei, what does it look like from your side? {question- @+1}
Mei: From the customer side, it was rough. We had about two thousand tickets in the first day. {claim+ F7 "2,000"}
Ana: The support dashboard I have says eleven thirty. {claim- F7}
Mei: Let me check. Oh, yes. Eleven thirty tickets, two thousand was chats plus tickets. {claim- F7}
Kofi: How many checkouts actually failed? {question- @+1}
Ana: Eighteen thousand four hundred attempts. Some of those are the same customers retrying. {claim- F4}
Ben: Do we know how many unique customers that is? {question+} {~}
Mei: And revenue? Finance asked me yesterday and I didn't have a number. {question- @+1}
Ana: Estimated revenue at risk is two hundred and twelve thousand. {claim- F5}
Kofi: At risk, not lost. A lot of those people came back and bought later.
Mei: Some did. Some told us they went to a competitor.
Ana: What did the error rate peak at? I want it in the doc. {question- @+1}
Kofi: Around forty percent, I think. {claim+ F6 "40%"}
Ben: It was higher than that. Sixty-four at the peak. I have the screenshot. {claim- F6}
Kofi: Sixty-four. Okay, that's worse than I remembered. {claim- F6}
Ana: And for the monthly availability target, we're over budget now, right? {question- @+1}
Kofi: Way over. The target's ninety-nine point nine five, and one outage like this blows the month. {claim- F11}
Mei: Can we do something for affected customers? A credit, a discount code? {question- @+2}
Kofi: Finance will have opinions.
Ana: Finance always does. But I think a goodwill code is reasonable here.
Mei: Maybe ten percent off the next order? {decision-} {question- @+1} {~}
Ana: That sounds right to me. Kofi, Ben, any objections? {question- @+1} {~}
Kofi: None.
Ben: None from me.
Ana: Okay. We're sending a ten percent goodwill code to every customer with a failed checkout. That's agreed. {decision+} {~}
Mei: Thank you. I'll draft the customer email today and send it to Ana for review. {action+}
## remediation :: Owners for the fixes; one parked question
Ana: Okay, remediation. Let's get owners on these.
Kofi: First one's mine. I'll add range validation for every payment timeout and retry value, starting this sprint. {action+}
Ana: Great. And staged rollouts for payment config? {question- @+1}
Kofi: I think we said yes in principle.
Ana: Then let's make it official. Payment config changes go to one region first, with a fifteen-minute bake, starting Monday. {decision+}
Ben: Good. That would have saved us.
Ana: Paging. Ben, can you fix the rotation so payment alerts go to the current on-call? {question- @+1}
Ben: Yes. I'll move the payment alerts to the main on-call rotation by Thursday. {action+}
Mei: And support needs a way to escalate. The channel didn't work.
Ana: What would work for your team? {question- @+1}
Mei: Honestly, a button in the support tool that pages on-call directly.
Kofi: That's probably a quick integration. Maybe we look at it next quarter? {decision-} {question- @+1}
Ana: Let's not commit to a quarter yet. We can pick it up offline. {decision-}
Mei: That's fair.
Ben: Should we also add an alert on checkout latency, not just errors? {question- @+1}
Kofi: Yes, the latency went crazy minutes before the errors did.
Ana: I'll add the latency alert to our SLO dashboard work and own that one. {action+}
Kofi: Someone should probably write up the unit conversion gotcha for the wiki too. {action-}
Ana: We have a wiki page already, that's part of the problem.
Kofi: Fair point.
Ana: Do we need an exec summary for this, or is the doc enough? {question+} {~}
Ben: I'm just glad we got through it.
Ana: Okay. I think we've got good owners. Thanks everyone, this was a really good review.
Mei: Thanks, Ana.
Kofi: Thanks all.
