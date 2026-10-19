---
meeting_id: sprint-payments-d5-s1
theme: Sprint planning for a payments team at a fictional fintech
domain_pack: software_team
drama: 0.5
seed: 1
author: claude-opus-5-5 (Claude Code session)
pack:
  title: Payments squad - sprint 23 planning
  org: Quillpay (fictional fintech)
  agenda:
    - {id: carryover, title: Carryover from last sprint, goal: Decide what rolls over and why it slipped, timebox_min: 4}
    - {id: priorities, title: Sprint priorities, goal: Rank the refund API, the bank certification and tech debt, timebox_min: 5}
    - {id: capacity, title: Capacity and estimates, goal: Match the plan to the people actually available, timebox_min: 4}
    - {id: risks, title: Risks and dependencies, goal: Name the risks and who is watching each one, timebox_min: 3}
  facts:
    - {id: F1, key: velocity_last_sprint, statement: "Velocity last sprint = 34 points", value: "34"}
    - {id: F2, key: avg_velocity_3_sprints, statement: "Average velocity over the last 3 sprints = 38 points", value: "38"}
    - {id: F3, key: carryover_tickets, statement: "Tickets carried over from last sprint = 5", value: "5"}
    - {id: F4, key: sprint_length, statement: "Sprint length = 10 working days", value: "10 working days"}
    - {id: F5, key: team_size, statement: "Engineers on the squad = 6", value: "6"}
    - {id: F6, key: pto_days_next_sprint, statement: "Planned PTO next sprint = 7 person-days", value: "7"}
    - {id: F7, key: refund_api_deadline, statement: "Refund API committed date to the partner = November 4", value: "November 4"}
    - {id: F8, key: open_security_findings, statement: "Open security findings on payments = 2", value: "2"}
    - {id: F9, key: payment_success_rate, statement: "Payment success rate last 30 days = 97.8%", value: "97.8%"}
    - {id: F10, key: oncall_pages_last_sprint, statement: "On-call pages last sprint = 11", value: "11"}
    - {id: F11, key: bank_cert_window, statement: "Bank partner certification window = 3 weeks", value: "3 weeks"}
    - {id: F12, key: payments_test_coverage, statement: "Test coverage on the payments service = 72%", value: "72%"}
personas:
  - name: Sofia
    role: Engineering manager, runs planning
    goals: A realistic sprint the team can actually finish
    hidden_agenda: Her director already promised the refund API to the partner
    verbosity: 3
    wpm: 160
    catchphrases: ["okay, team", "let's be honest"]
    voice_gender: female
  - name: Marcus
    role: Senior backend engineer
    goals: Get the ledger refactor into the sprint
    hidden_agenda: Burned out from on-call
    verbosity: 3
    wpm: 150
    catchphrases: ["look", "realistically"]
    voice_gender: male
  - name: Aiko
    role: Product owner
    goals: Refund API first, everything else second
    hidden_agenda: Overpromised the partner on scope
    verbosity: 4
    wpm: 170
    catchphrases: ["from a product point of view", "the partner"]
    voice_gender: female
  - name: Diego
    role: Junior engineer, newest on the team
    goals: Be useful, not be the reason anything slips
    hidden_agenda: Doesn't fully understand the bank certification
    verbosity: 2
    wpm: 155
    catchphrases: ["sorry, quick one"]
    voice_gender: male
---
## carryover :: What slipped and why; Marcus inflates last sprint's velocity
Sofia: Okay, team, sprint twenty-three. Let's start with what we didn't finish. {~}
Marcus: Realistically, most of it was the reconciliation job. It ate the second week.
Sofia: How many tickets are rolling over? {question- @+1}
Diego: Five. Three of them are the reconciliation ones. {claim- F3}
Aiko: And the other two are mine, the refund status page and the email template.
Marcus: Look, we still did forty points, which is pretty good given the incident. {claim+ F1 "40"}
Sofia: Forty sounds high to me. I'd want to check the board before we celebrate. {action-} {claim+ F1 "40"}
Aiko: From a product point of view I don't care about points, I care about the refund API.
Marcus: Points are how we know if the refund API is even possible.
Diego: Sorry, quick one, does carryover count against this sprint's points or last sprint's? {question- @+1}
Sofia: It's re-estimated and counted in this sprint, that's how we've always done it.
Diego: Okay, cool. Thanks.
Marcus: The reconciliation job slipped because the bank sandbox was down for two days. That's not on us. {~}
Aiko: It's not on anyone, it's just the reality of working with banks.
Sofia: Let's be honest, though, we also started it late.
Marcus: Fair.
Sofia: Do the reconciliation tickets need re-estimating, or are the old numbers still good? {question- @+1}
Marcus: They're still good. Most of the hard part is done, it's testing now.
Diego: I can help with the testing, if that's useful. {action-}
Sofia: Let's figure out who's on what in capacity. Hold that.
Aiko: The template ticket can probably drop, honestly. Marketing hasn't even sent copy. {decision-}
Sofia: Is that a drop, or a not-yet? {question- @+1}
Aiko: A not-yet. Let's keep it in the backlog.
Sofia: Okay. Then the reconciliation tickets and the status page roll over, and the template goes back to the backlog. That's settled. {decision+}
Marcus: Works for me.
## priorities :: Refund API vs bank certification vs the ledger refactor; Aiko misstates the deadline, nobody catches it
Sofia: Priorities. Aiko, you want to frame it? {question- @+1}
Aiko: Refund API, then the bank certification, then whatever's left. The partner is expecting refunds on November fourteenth. {claim+ F7 "November 14"}
Marcus: And the ledger refactor? {question- @+1}
Aiko: The ledger refactor is invisible to customers.
Marcus: It's invisible until the ledger breaks. Then it's very visible.
Sofia: How long is the certification window with the bank? {question- @+1}
Diego: Three weeks, I think. That's what the email said. {claim- F11}
Marcus: Three weeks, but the first week is usually them not answering emails. {claim- F11}
Aiko: Which is why we start it now.
Marcus: Sorry, my headphones just died, one sec. {drift- 2}
Diego: Classic Monday.
Sofia: Can we run certification and refunds in parallel? Or is that the same people? {question- @+1}
Marcus: Look, it's mostly me on both.
Aiko: Then we need someone else on certification.
Diego: I could do certification? I'd need someone to walk me through it first. {action-} {~}
Marcus: The first time takes ages. There's a lot of tribal knowledge.
Sofia: Does anyone else here actually know the cert process end to end? Because if it's just— {question+} {~}
Marcus: My bigger worry is test coverage. We're at eighty percent on payments, and that's not enough for a new API. {claim+ F12 "80%"}
Aiko: Eighty sounds fine to me. {claim+ F12 "80%"}
Sofia: Coverage aside, I hear refunds first. Does anyone object? {question- @+1}
Marcus: I object a little. I want the ledger refactor in this sprint, even half of it.
Aiko: Half a refactor is how you get two ledgers.
Marcus: That's, okay, that's actually a fair point.
Sofia: So the ranking is refunds, then certification, then the ledger work if there's room. {decision+}
Aiko: If there's room. Which there won't be.
Marcus: There's never room. That's my point.
## capacity :: Who is actually around; PTO and on-call; an aside about the office plant becomes a whole thing
Sofia: Okay, capacity. We're six engineers, but two of you aren't here today. {claim- F5}
Marcus: And Hannah's out the second week, right? {question- @+1}
Sofia: Right. PTO next sprint is seven person-days total. {claim- F6}
Aiko: Seven days is a lot. That's almost a whole person. {claim- F6}
Marcus: And on-call ate half a person last sprint. Eleven pages. {claim- F10}
Diego: Eleven? It felt like more. {claim- F10} {~}
Marcus: It felt like a hundred. I got paged during my kid's recital. {~}
Sofia: Okay. What velocity do we plan to? {question+} {~}
Marcus: Our three-sprint average is thirty-eight. {claim- F2}
Sofia: Then with the PTO, I'd plan to thirty, maybe thirty-two. {~}
Aiko: Thirty doesn't fit refunds and certification. {~}
Sofia: Then something doesn't fit. Let's be honest about it now, not in two weeks.
Aiko: Has anyone actually told the partner we might be short-staffed? {question+} {~}
Sofia: Good question. Let's come back to that one.
Diego: Sorry, quick one, is anyone watering the plant by the window? It's looking really sad. {drift+ 4} {question- @+2}
Marcus: That plant has been dying since March. It's a lifestyle at this point.
Aiko: I watered it last week! I think it's the radiator, it's right next to it.
Diego: I read that they like being talked to. Maybe it's lonely.
Sofia: Okay, nobody's adopting the plant in sprint planning. Capacity.
Marcus: Realistically, I can't be on refunds, certification and on-call at the same time.
Sofia: Then you're off the on-call rotation this sprint. Diego shadows Priyanka on-call instead. Done. {decision+}
Marcus: Thank you. Seriously.
Diego: Shadow on-call. Okay. That's, okay. {action+}
Sofia: Diego, could you pair with Marcus on certification for the first week, so the knowledge isn't just in one head? {question- @+1}
Diego: Yeah, I'll take the cert onboarding with Marcus, starting Monday. {action+}
Marcus: I'll write up the cert steps as we go, so it's not tribal anymore. {action+}
Aiko: And the status page ticket? {question- @+1}
Sofia: Status page is probably the first thing to drop if refunds slip. {decision-}
Aiko: That's fair.
## risks :: Security findings, the bank, the date; one owner, one non-owner, a dodged question
Sofia: Last one, risks. What keeps you up at night? {question- @+1}
Marcus: The two open security findings on payments. They're not critical, but they're old. {claim- F8}
Aiko: Are they blocking the partner launch? {question- @+1}
Marcus: Not technically. But if the partner's security team asks, it looks bad.
Sofia: Can someone own getting those two closed this sprint? {question- @+3} {claim- F8}
Marcus: I'd love to, but you just saw my sprint.
Aiko: It would be good if someone from platform took a look at them. {action-}
Sofia: I'll raise the security findings with the platform lead on Thursday and ask for an owner. {action+}
Diego: What happens if the bank certification fails the first time? Do we just get another window? {question- @+2}
Marcus: Good question.
Aiko: You get another window, but it's another three weeks of waiting. {claim- F11}
Sofia: That's the real risk then. If cert slips, the partner date slips.
Aiko: The refund date is fixed, though. The partner announced it.
Marcus: And our success rate is only ninety-seven point eight right now, so I'd rather not rush anything that touches money. {claim- F9}
Sofia: Agreed. I want a weekly check on cert progress, every Wednesday, for the whole sprint. That's decided. {decision+}
Aiko: Fine by me.
Diego: Should I put that on the calendar? {question- @+1}
Sofia: Please. Thank you, Diego.
Diego: Okay, I'll send the invite for the Wednesday cert check today. {action+}
Sofia: Okay, team. That's the plan. Let's be honest in standup if it starts slipping. Thanks all.
Marcus: Thanks.
Aiko: Thanks, everyone.
