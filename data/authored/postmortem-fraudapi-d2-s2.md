---
meeting_id: postmortem-fraudapi-d2-s2
theme: "Incident postmortem: the checkout outage last Tuesday"
domain_pack: incident_review
drama: 0.2
seed: 2
author: claude-opus-5-5 (Claude Code session)
pack:
  title: Postmortem - Tuesday checkout outage (fraud-check vendor)
  org: Alder & Finch Books (fictional online bookstore)
  agenda:
    - {id: timeline, title: Timeline, goal: Establish when it started, was detected and ended, timebox_min: 4}
    - {id: cause, title: Cause, goal: Understand why a slow vendor took checkout down, timebox_min: 5}
    - {id: impact, title: Impact, goal: Size the effect on customers and revenue, timebox_min: 3}
    - {id: actions, title: Actions, goal: Agree owners for the fixes, timebox_min: 4}
  facts:
    - {id: F1, key: outage_duration, statement: "Checkout outage lasted 38 minutes", value: "38 minutes"}
    - {id: F2, key: outage_start, statement: "Outage started at 3:15 pm", value: "3:15 pm"}
    - {id: F3, key: fraud_timeout, statement: "Fraud-check call timeout = 30 seconds", value: "30 seconds"}
    - {id: F4, key: fraud_p99, statement: "Fraud API p99 latency during the incident = 12 seconds", value: "12 seconds"}
    - {id: F5, key: failed_orders, statement: "Failed orders = 1,240", value: "1,240"}
    - {id: F6, key: revenue_impact, statement: "Estimated revenue impact = $41,000", value: "$41,000"}
    - {id: F7, key: detection_time, statement: "Time to detection = 4 minutes", value: "4 minutes"}
    - {id: F8, key: support_tickets, statement: "Support tickets = 310", value: "310"}
    - {id: F9, key: vendor_sla, statement: "Vendor SLA uptime = 99.9%", value: "99.9%"}
    - {id: F10, key: vendor_incidents_year, statement: "Vendor incidents affecting us this year = 2", value: "2"}
    - {id: F11, key: orders_retried, statement: "Orders automatically retried and recovered = 870", value: "870"}
    - {id: F12, key: vendor_credit, statement: "Service credit from the vendor = $5,000", value: "$5,000"}
personas:
  - name: Noor
    role: Incident manager, facilitates
    goals: A clear record and practical fixes
    hidden_agenda: Wants to make fallback paths a standard for every vendor
    verbosity: 3
    wpm: 150
    catchphrases: []
    voice_gender: female
  - name: Samuel
    role: On-call engineer
    goals: Explain the response honestly
    hidden_agenda: Wasn't sure he was allowed to switch the fraud check off
    verbosity: 2
    wpm: 145
    catchphrases: []
    voice_gender: male
  - name: Lin
    role: Payments engineer, owns the fraud-check integration
    goals: Fix the integration properly
    hidden_agenda: Wrote the original integration three years ago
    verbosity: 3
    wpm: 155
    catchphrases: []
    voice_gender: female
  - name: Abby
    role: Customer support lead
    goals: Clear answers for customers
    hidden_agenda: Her team found out from customers before engineering told them
    verbosity: 3
    wpm: 165
    catchphrases: []
    voice_gender: female
---
## timeline :: Start, detection and end; Samuel overstates the duration
Noor: Thanks, everyone. This is a blameless review. Samuel, could you take us through Tuesday afternoon? {question- @+1}
Samuel: Sure. Checkout errors started at about a quarter past three. {claim- F2} {~}
Noor: How quickly did we notice? {question- @+1}
Samuel: The alert fired four minutes in. That part worked well. {claim- F7}
Abby: Our chat queue lit up at about the same time, for what it's worth. 
Lin: Did anyone tell support at that point? {question+} {~}
Noor: And how long were we down altogether? {question- @+1}
Samuel: About an hour, I'd say. It felt like a long afternoon. {claim+ F1 "an hour"}
Noor: The incident record has thirty-eight minutes, from first error to recovery. {claim- F1}
Samuel: Thirty-eight. That's right. The hour includes the time we spent watching it afterwards. {claim- F1}
Noor: What ended it? {question- @+1}
Samuel: The vendor's latency came back down on its own. We didn't actually fix anything.
Lin: Which is the uncomfortable part. We were waiting on them.
Noor: Did anyone consider switching the fraud check off? {question- @+1}
Samuel: I thought about it. I wasn't sure I was allowed to. There's no runbook entry for it.
Lin: That's a gap in the runbook, not on you, Samuel.
## cause :: Why a slow vendor stopped checkout; Lin's timeout figure stays wrong
Noor: The cause. Lin, you know the integration best.
Lin: The fraud-check vendor got slow. Their p99 latency went up to twelve seconds. {claim- F4}
Abby: Twelve seconds per check? {question- @+1} {claim- F4}
Lin: Per check. And our timeout is ten seconds, so most calls timed out and the order failed. {claim+ F3 "10 seconds"}
Noor: Why does a timeout fail the order, rather than letting it through? {question- @+1}
Lin: When I built it, the rule was "if in doubt, block". We never revisited it.
Samuel: So a slow vendor looks the same as a fraudulent order.
Noor: Exactly that. What does the vendor promise us? {question- @+1}
Lin: Ninety-nine point nine percent uptime. They'd argue they were up, just slow. {claim- F9}
Abby: Has this happened before with them? {question- @+1}
Lin: Twice this year now. The first one was short enough that nobody noticed. {claim- F10}
Samuel: The weather station in my village says it's going to snow on Friday, by the way. In April. {drift+ 2}
Abby: My tulips are going to be furious.
Noor: Let's come back to the cause. Lin, what would a safer default look like? {question- @+1}
Lin: Let small orders through when the check times out, and hold large orders for manual review. {decision-}
Noor: Is there a threshold that makes sense? {question- @+1}
Lin: Most fraud we see is over a hundred and fifty dollars. Under that, letting it through is low risk. {~}
Noor: Then let's adopt that: on a timeout, orders under a hundred and fifty go through, and larger ones are held for review. {decision+} {~}
Lin: I'll build the fallback and have it in review by next Thursday. {action+}
## impact :: Orders, money and tickets; Abby's ticket count corrected later
Noor: Impact. How many orders failed? {question- @+1}
Lin: Twelve hundred and forty failed. But eight hundred and seventy were retried automatically and went through later. {claim- F5} {claim- F11} {~}
Noor: So the real loss is smaller than the first number.
Samuel: And the revenue impact? {question- @+1}
Noor: Finance estimates forty-one thousand, before the retries are counted. {claim- F6}
Abby: We had about five hundred support tickets. People were very worried their cards had been charged. {claim+ F8 "500"}
Noor: Were they charged? {question- @+1}
Lin: No. A failed fraud check means no charge was made.
Abby: That's good to know. Our macros didn't say that clearly.
Samuel: Could support get a short statement for this kind of failure, so they're not guessing? {question- @+1}
Abby: Yes, please. I'll write a draft macro and send it to Lin to check. {action+} 
Lin: Happy to check it. {action+}
Abby: Sorry, correcting myself, the ticket report says three hundred and ten, not five hundred. Five hundred was all contacts, including chat. {claim- F8}
## actions :: Owners and dates; one item without an owner
Noor: Actions. We have the fallback from Lin and the macro from Abby.
Samuel: And a runbook entry for switching the fraud check off. So the next person knows they can. {action-}
Noor: Samuel, would you write that entry, since you were there? {question- @+1}
Samuel: Yes. I'll write the runbook entry this week. {action+}
Noor: Should we ask the vendor for a service credit? Their SLA is about uptime, but it's worth asking. {question- @+1}
Lin: They've already offered five thousand. It came in this morning. {claim- F12}
Noor: Then we accept the credit and ask for a latency commitment in the renewal. {decision+}
Abby: Who's talking to the vendor about the renewal? {question+}
Samuel: Should every vendor integration have a fallback like this one? {question- @+1}
Noor: I think so. I'll raise it with the architecture group next week. Thank you, everyone. A good, honest review. {action+} {~}
