---
meeting_id: sprint-tallyho-d2-s2
theme: Sprint planning for a payments team at a fictional fintech
domain_pack: software_team
drama: 0.2
seed: 2
author: claude-opus-5-5 (Claude Code session)
pack:
  title: Invoicing and payments team - sprint planning
  org: Tallyho Accounting (fictional)
  agenda:
    - {id: demo, title: Demo feedback, goal: Review what customers said at the sprint demo, timebox_min: 3}
    - {id: goal, title: Sprint goal, goal: Choose between payment reminders and the bank API migration, timebox_min: 5}
    - {id: capacity, title: Capacity, goal: Fit the plan to who is around, timebox_min: 3}
    - {id: risks, title: Risks, goal: Name the risks and owners, timebox_min: 3}
  facts:
    - {id: F1, key: invoices_per_day, statement: "Invoices sent per day = 52,000", value: "52,000"}
    - {id: F2, key: reminder_requests, statement: "Customer requests for payment reminders = 87", value: "87"}
    - {id: F3, key: avg_velocity, statement: "Average velocity = 34 points", value: "34"}
    - {id: F4, key: engineers, statement: "Engineers = 5", value: "5"}
    - {id: F5, key: pto_days, statement: "PTO days this sprint = 4", value: "4"}
    - {id: F6, key: bank_api_deprecation, statement: "Old bank API switched off on June 30", value: "June 30"}
    - {id: F7, key: open_bugs, statement: "Open bugs = 12", value: "12"}
    - {id: F8, key: nps, statement: "NPS last quarter = 38", value: "38"}
    - {id: F9, key: build_time, statement: "CI build time = 14 minutes", value: "14 minutes"}
    - {id: F10, key: a11y_issues, statement: "Open accessibility issues = 6", value: "6"}
    - {id: F11, key: ach_return_rate, statement: "ACH return rate = 0.8%", value: "0.8%"}
    - {id: F12, key: demo_attendees, statement: "Customers at the sprint demo = 23", value: "23"}
personas:
  - name: Priscilla
    role: Engineering manager
    goals: A predictable sprint
    hidden_agenda: Wants the bank migration done well before the deadline
    verbosity: 3
    wpm: 150
    catchphrases: []
    voice_gender: female
  - name: Kenta
    role: Senior engineer
    goals: Get the bank API migration started
    hidden_agenda: Has been reading the new API docs at night
    verbosity: 2
    wpm: 145
    catchphrases: []
    voice_gender: male
  - name: Mira
    role: Product owner
    goals: Ship payment reminders
    hidden_agenda: Promised a big customer reminders "soon"
    verbosity: 3
    wpm: 165
    catchphrases: []
    voice_gender: female
  - name: Dan
    role: QA engineer
    goals: Faster builds
    hidden_agenda: Wants to fix the build himself
    verbosity: 2
    wpm: 155
    catchphrases: []
    voice_gender: male
---
## demo :: What customers said
Priscilla: Good morning. Let's start with the demo. Twenty-three customers came, which is the most we've had. {claim- F12}
Mira: They loved the new invoice templates. The question everyone asked was about reminders.
Kenta: Reminders for late payments? {question- @+1}
Mira: Automatic reminders, yes. Over a hundred customers have asked for them. {claim+ F2 "over 100"}
Dan: Is that the number in the feedback tool? I thought it was lower. {question- @+1}
Mira: Let me check. Eighty-seven. I was counting the demo questions on top. {claim- F2}
Priscilla: Eighty-seven is still a lot. {claim- F2}
Kenta: The templates took longer than we thought, so it's nice to hear they landed.
Dan: The dark one got a round of applause. I've never seen that at a demo.
Mira: One customer said it was the first time invoicing felt like it was designed for humans.
Kenta: I'll take that as a compliment for the whole team, not just the designer. {~}
## goal :: Reminders or the bank migration
Priscilla: The sprint goal. Reminders, or the bank API migration.
Kenta: The old bank API is switched off on June thirtieth. Nothing gets paid after that if we haven't moved. {claim- F6}
Mira: June is three months away. Reminders are something customers want now. {claim- F6}
Kenta: Fifty-two thousand invoices a day go through that API. {claim- F1}
Dan: How long is the migration? {question- @+1}
Kenta: Three sprints, if nothing surprises us. Banks usually surprise us. {~}
Priscilla: Could we start the migration now and do a small version of reminders alongside? {question- @+1} {decision-}
Mira: A small version would be one reminder, sent seven days after the due date. That covers most of what people asked for. {~}
Kenta: That's a few days of work. It doesn't threaten the migration.
Dan: The email itself has to be friendly, though. Nobody wants a scary reminder from their accountant.
Mira: Friendly, with a link to pay. That's the whole thing.
Kenta: And it should stop the moment the invoice is paid. The old system kept nagging people.
Mira: The old system did a lot of things it shouldn't have.
Priscilla: Then the sprint goal is starting the bank migration, with the simple seven-day reminder alongside it. {decision+} {~}
Mira: I'll write the reminder story today, with the email text. {action+}
## capacity :: Who's around; Dan's build time stands
Priscilla: Capacity. Five engineers, four days of PTO between us. {claim- F4} {claim- F5}
Kenta: Our average is thirty-four. So about thirty this sprint. {claim- F3} {~}
Dan: The build is the hidden cost. It takes about twenty minutes every time. {claim+ F9 "20 minutes"}
Priscilla: Is there an easy fix for the build? {question- @+1}
Dan: The tests run in one long line. If we split them, it would be much faster. I'd like to try.
Kenta: Splitting them might expose the tests that depend on each other. There are a few of those.
Dan: Then it'll find them for us. That's a good thing in the end.
Priscilla: Then try it, but keep it to two days. {decision+}
Kenta: My neighbor started keeping bees last month. The whole street is waiting to see if they swarm. {drift+ 2}
Mira: Ours did that once. It looked like a cloud landing on the car.
Priscilla: Back to the plan. Risks.
## risks :: Open bugs, accessibility and the bank
Dan: Twelve open bugs. None are severe, but two are in the payment screen. {claim- F7}
Mira: And six accessibility issues on the invoice view. A customer flagged them at the demo. {claim- F10}
Priscilla: Should the accessibility issues be in this sprint? {question- @+1}
Mira: The two worst ones, yes. The rest can wait a sprint.
Kenta: The other risk is the bank's sandbox. Last time it was down for a week.
Priscilla: That was painful. We couldn't test anything for days.
Mira: Their support line was useless too. It just played music.
Dan: It might be worth asking the bank for a sandbox status page. {action-}
Kenta: I'll email our contact at the bank and ask. {action+}
Mira: The return rate on ACH is under one percent, right? Point eight? {claim- F11} {question- @+1}
Kenta: Point eight. The new API reports returns faster, which should help.
Dan: Does anyone know who owns the reminder emails if a customer complains? {question+} {~}
Priscilla: I think that's everything. Thanks, everyone.
