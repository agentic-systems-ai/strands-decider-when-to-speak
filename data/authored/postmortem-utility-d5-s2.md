---
meeting_id: postmortem-utility-d5-s2
theme: "Incident postmortem: the checkout outage last Tuesday"
domain_pack: incident_review
drama: 0.5
seed: 2
author: claude-opus-5-5 (Claude Code session)
pack:
  title: Postmortem - Tuesday payment portal outage
  org: Copperline Energy (fictional utility)
  agenda:
    - {id: timeline, title: Timeline, goal: Agree what happened and when, timebox_min: 4}
    - {id: cause, title: Cause, goal: Understand the rate limit change and the due-date spike, timebox_min: 5}
    - {id: customers, title: Customer impact, goal: Late fees, the call center and communications, timebox_min: 4}
    - {id: actions, title: Actions, goal: Owners and dates, timebox_min: 3}
  facts:
    - {id: F1, key: outage_duration, statement: "Payment portal outage lasted 95 minutes", value: "95 minutes"}
    - {id: F2, key: outage_start, statement: "Outage started at 8:05 am", value: "8:05 am"}
    - {id: F3, key: rate_limit, statement: "New rate limit = 500 requests per second", value: "500"}
    - {id: F4, key: peak_traffic, statement: "Peak traffic = 1,400 requests per second", value: "1,400"}
    - {id: F5, key: failed_payments, statement: "Failed payments = 9,800", value: "9,800"}
    - {id: F6, key: late_fees_waived, statement: "Late fees waived = $73,500", value: "$73,500"}
    - {id: F7, key: call_volume, statement: "Calls to the call center = 4,200", value: "4,200"}
    - {id: F8, key: hold_time, statement: "Average hold time at peak = 38 minutes", value: "38 minutes"}
    - {id: F9, key: due_today, statement: "Customers with bills due that day = 120,000", value: "120,000"}
    - {id: F10, key: change_ticket, statement: "The rate limit change was CHG-2207", value: "CHG-2207"}
    - {id: F11, key: previous_peak, statement: "Previous peak handled = 1,100 requests per second", value: "1,100"}
    - {id: F12, key: status_page_delay, statement: "Status page updated 25 minutes after the start", value: "25 minutes"}
personas:
  - name: Imani
    role: Incident lead, facilitates
    goals: A clear record and fixes that stick
    hidden_agenda: Pushed for load testing last year and lost the budget fight
    verbosity: 3
    wpm: 155
    catchphrases: []
    voice_gender: female
  - name: Gareth
    role: Backend engineer who made the rate limit change
    goals: Explain the change honestly
    hidden_agenda: Was asked to make the change by the security team in a hurry
    verbosity: 2
    wpm: 145
    catchphrases: []
    voice_gender: male
  - name: Selin
    role: Customer operations manager
    goals: Look after the customers who were hurt
    hidden_agenda: Her call center staff were abused on the phones all morning
    verbosity: 3
    wpm: 165
    catchphrases: []
    voice_gender: female
  - name: Pablo
    role: Product manager for the portal
    goals: Win back customer trust
    hidden_agenda: The portal redesign launch is in two weeks and he's worried it slips
    verbosity: 3
    wpm: 160
    catchphrases: []
    voice_gender: male
---
## timeline :: What happened and when
Imani: Thanks for coming. Blameless, as usual. Let's start with the timeline. {~}
Gareth: The portal started rejecting payments at five past eight in the morning. {claim- F2}
Pablo: Which is exactly when people pay their bills before work.
Imani: When did the status page go up? {question- @+1}
Selin: Twenty-five minutes later. My team was already drowning by then. {claim- F12} {~}
Imani: How long was the portal down in total? {question- @+1}
Gareth: Ninety-five minutes, until the limit was raised again. {claim- F1}
Selin: It felt like a whole day on the phones.
Pablo: I was on the train when it started. My own payment failed. That's how I found out.
Imani: Not ideal, but at least you saw what customers saw.
Pablo: I saw a page that said "too many requests". Customers have no idea what that means.
Selin: They thought we were blaming them for paying too often.
Imani: That error message is going on the action list.
Gareth: In fairness, it's the default message from the gateway. Nobody ever wrote a friendly one.
Selin: Then let's write one.
## cause :: The rate limit change; Gareth misstates the new limit and is corrected
Imani: Gareth, what changed? {question- @+1}
Gareth: The security team asked us to add a rate limit on the payment API after the credential-stuffing attempts last month. I set it to a thousand requests a second. {claim+ F3 "1,000"}
Imani: The change ticket says five hundred. CHG-2207. {claim- F3} {claim- F10}
Gareth: Five hundred. You're right. A thousand was the number I'd proposed, and it got lowered in review. {claim- F3}
Pablo: And the traffic that morning? {question- @+1}
Gareth: It peaked at fourteen hundred a second. Almost three times the limit. {claim- F4}
Selin: Why that morning in particular? {question- @+1}
Pablo: A hundred and twenty thousand customers had bills due that day. It's the first of the month. {claim- F9}
Imani: Had we ever seen that much traffic before? {question- @+1}
Gareth: The previous peak was eleven hundred. So even the old high-water mark would have been blocked. {claim- F11}
Imani: So the limit was set without anyone checking real traffic.
Gareth: Without anyone checking the first of the month, no. The security team looked at an average day.
Selin: An average day is not the day people pay their bills.
Imani: It's a gap in how we review limits, not in Gareth.
Pablo: Has the security team been told what happened? {question- @+1}
Imani: I spoke to their lead yesterday. They're joining the actions part next week. {~}
Gareth: Rate limits should be set from the busiest day of the year, not an average. That should be a rule.
Imani: Then that's the rule from today: limits are set from the busiest day in the last year, with headroom. {decision+} 
Selin: Good.
Gareth: I'll rewrite the limit using the first-of-month peaks and get it reviewed by both teams. {action+}
## customers :: The human side; Selin's hold time is high, corrected later; Pablo's failure count stands
Imani: Customers. Selin? {question- @+1}
Selin: We took forty-two hundred calls that morning. Hold times hit an hour at the worst point. {claim- F7} {claim+ F8 "an hour"}
Pablo: And about five thousand payments failed outright. {claim+ F5 "5,000"}
Imani: Those people will get late fees, unless we waive them.
Selin: We have to waive them. It wasn't their fault.
Pablo: Waiving every late fee from that morning is seventy-three and a half thousand dollars. Finance already ran it. {claim- F6}
Imani: That's a lot, but it's the right thing.
Selin: Some customers were in tears on the phone. One woman thought her heating would be cut off.
Pablo: Was it? {question- @+1}
Selin: No. Nobody gets disconnected for a missed payment on a day we were down. We made sure of that.
Imani: Then we waive every late fee caused by the outage, automatically, with no need to call. {decision+}
Selin: Could someone send customers an apology that explains it in plain words? {question- @+1}
Pablo: I'll write it today, and get Selin to read it before it goes. {action+}
Selin: Thank you. Sorry, one more correction. I checked the call log after the meeting started. The average hold at peak was thirty-eight minutes, not an hour. {claim- F8}
Imani: Thirty-eight minutes is still terrible. {claim- F8}
Selin: It is. My team deserves a thank-you, honestly.
Pablo: The weather didn't help, either. That freezing fog had half the city working from home and online at eight. {drift+ 3}
Gareth: The fog was wild. I couldn't see the end of my street.
Selin: My kids had a snow day and there wasn't even any snow.
Pablo: Actions, then.
## actions :: Owners, dates, and one open question
Imani: Actions. We have Gareth on the limit, Pablo on the apology, and the fees waived automatically.
Selin: And the error message. Customers need to know it's us, not them.
Pablo: That one's mine. The new message will say we're having trouble and their payment hasn't been taken. {action+}
Gareth: It might be worth load-testing the portal before the redesign launch too. {action-}
Imani: I'd like that very much. I'll put a load test in the launch checklist. {action+}
Pablo: Will the load test delay the redesign? It launches in two weeks. {question- @+1}
Imani: Not if we start it this week. A day of testing, maybe two.
Selin: Who checks that the late-fee waivers actually went through for everyone? {question+} {~}
Gareth: I can pull a report of every failed payment from that morning, if that helps whoever does it. {action+}
Imani: Thank you, everyone. This was a hard morning for a lot of people, and you handled it well.
