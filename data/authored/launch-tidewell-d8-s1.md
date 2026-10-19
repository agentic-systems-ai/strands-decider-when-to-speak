---
meeting_id: launch-tidewell-d8-s1
theme: Go/no-go for the Aurora mobile app launch
domain_pack: product_launch
drama: 0.8
seed: 1
author: claude-opus-5-5 (Claude Code session)
pack:
  title: Aurora banking app - launch readiness review
  org: Tidewell Bank (fictional)
  agenda:
    - {id: readiness, title: Product readiness, goal: Stability, blockers and pilot feedback against the bar, timebox_min: 5}
    - {id: compliance, title: Compliance sign-off, goal: Confirm what compliance still needs before launch, timebox_min: 4}
    - {id: rollout, title: Rollout plan, goal: Agree the phases and the rollback trigger, timebox_min: 4}
    - {id: go_no_go, title: The go/no-go call, goal: Make the call and agree what the board hears, timebox_min: 3}
  facts:
    - {id: F1, key: crash_rate, statement: "Crash rate in the pilot = 0.6% of sessions", value: "0.6%"}
    - {id: F2, key: open_blockers, statement: "Open launch blockers = 4", value: "4"}
    - {id: F3, key: accessibility_issues_open, statement: "Open accessibility issues = 11", value: "11"}
    - {id: F4, key: compliance_items_outstanding, statement: "Compliance items still outstanding = 2", value: "2"}
    - {id: F5, key: pilot_customers, statement: "Pilot customers = 1,500", value: "1,500"}
    - {id: F6, key: pilot_csat, statement: "Pilot CSAT = 4.1 out of 5", value: "4.1"}
    - {id: F7, key: board_demo_date, statement: "Board demo = October 30", value: "October 30"}
    - {id: F8, key: phase1_share, statement: "Phase 1 rollout = 5% of customers", value: "5%"}
    - {id: F9, key: pilot_support_tickets, statement: "Support tickets from the pilot = 230", value: "230"}
    - {id: F10, key: load_test_peak, statement: "Load test peak = 8,000 requests per second", value: "8,000"}
    - {id: F11, key: regulator_notice, statement: "Regulator notice period = 30 days", value: "30 days"}
    - {id: F12, key: launch_target, statement: "Target launch date = November 12", value: "November 12"}
personas:
  - name: Victor
    role: VP of digital product
    goals: Launch on November 12 no matter what
    hidden_agenda: Already told the board it's a done deal
    verbosity: 5
    wpm: 180
    catchphrases: ["bottom line", "come on"]
    voice_gender: male
  - name: Hana
    role: Engineering director
    goals: Don't launch a banking app that crashes
    hidden_agenda: Her team has been doing weekend shifts for a month
    verbosity: 3
    wpm: 160
    catchphrases: ["with all due respect", "no"]
    voice_gender: female
  - name: Chloe
    role: Design lead
    goals: Ship something that works for everyone, including screen-reader users
    hidden_agenda: Lost the accessibility budget fight last quarter
    verbosity: 3
    wpm: 165
    catchphrases: ["to be clear", "honestly"]
    voice_gender: female
  - name: Ibrahim
    role: Compliance manager
    goals: No regulatory surprises
    hidden_agenda: Was not invited to the board prep
    verbosity: 2
    wpm: 140
    catchphrases: ["for the record", "strictly speaking"]
    voice_gender: male
---
## readiness :: Victor cherry-picks; Hana corrects the crash rate; the CSAT inflation slips by
Victor: Bottom line, we're launching November twelfth, and this meeting is about how, not whether. {claim- F12}
Hana: With all due respect, that's exactly what this meeting is about.
Victor: Come on, Hana. The pilot went great. Crash rate's under a tenth of a percent. {claim+ F1 "0.1%"}
Hana: No. It's zero point six. Six times what you just said. {claim- F1}
Victor: Zero point six, zero point one, it's a rounding error. {claim- F1}
Hana: It's not a rounding error on a banking app. People are moving money when it crashes.
Chloe: To be clear, most of the crashes are on the transfer screen. That's the scary one.
Victor: And customers love it. Pilot CSAT was four point six. {claim+ F6 "4.6"}
Chloe: Honestly, the comments are good. People like the new home screen.
Ibrahim: How many pilot customers was that? {question- @+1}
Hana: Fifteen hundred. Which is not a lot of phones. {claim- F5}
Victor: Fifteen hundred real customers, real money. That's a real signal. {claim- F5}
Hana: How many blockers are still open? Because I have four. {question- @+1} {claim- F2}
Victor: Four, but two of them are basically done. {claim- F2}
Hana: Basically done is not done.
Chloe: And accessibility. We're down to three open issues, which is huge progress. {claim+ F3 "3"}
Ibrahim: For the record, I'd want to see the accessibility list myself before launch.
Victor: Come on, three issues. We can patch those after. {claim+ F3 "3"}
Hana: As far as I'm concerned, the transfer crash has to be fixed before launch. {decision-}
Victor: Fine, fine. Who's on it? {question- @+1} {decision+}
Hana: Marco's team. I'll get you a fix date from Marco by end of day tomorrow. {action+}
Chloe: And somebody really needs to test the transfer flow with a screen reader. {action-}
Ibrahim: Has the call center seen the new transfer flow? Because last time— {question+} {~}
Victor: Did anyone see the parking garage memo? They're moving us to level four. {drift+ 4} {question- @+1}
Chloe: Level four has no elevator access from the east side. It's a nightmare.
Hana: I park on the street now. It's faster.
Victor: The street? With my car? Absolutely not. {~}
Ibrahim: Strictly speaking, we were talking about the launch.
## compliance :: What's outstanding; Hana overstates the regulator notice; the accessibility number gets corrected late
Victor: Fine. Compliance. Ibrahim, give me good news.
Ibrahim: There are two items outstanding. The disclosures text and the data retention review. {claim- F4}
Victor: Two items. That's nothing. {claim- F4}
Ibrahim: The retention review is not nothing. It's the one the regulator asked about last year.
Hana: And don't we have to notify the regulator sixty days before launch? {claim+ F11 "60 days"} {question- @+1}
Ibrahim: Thirty. It's a thirty-day notice. {claim- F11}
Victor: Thirty days. When did we send it? {question- @+1} {claim- F11}
Ibrahim: We haven't. Nobody told me there was a date until last week.
Victor: Come on, that's—
Hana: That's on us, not on him.
Ibrahim: For the record, if the notice goes out this week, the twelfth still works. Just. {claim- F12}
Victor: So it needs to go out this week. {decision-}
Ibrahim: I'll file the regulator notice by Friday, if I get the final feature list from Chloe by Wednesday. {action+}
Chloe: To be clear, I can get you the feature list tomorrow. {action+}
Ibrahim: Then I'll file the notice on Thursday. {action+}
Victor: Bottom line, so compliance is a yes.
Ibrahim: Strictly speaking, compliance is a "not yet".
Chloe: Sorry, I just pulled up the tracker. Accessibility is eleven open, not three. Three are the critical ones. {claim- F3}
Hana: Eleven. {claim- F3}
Victor: Three critical, that's what matters.
Chloe: Honestly, eleven matters if you're the person who can't use the app. {claim- F3}
## rollout :: Phases, load and the rollback trigger
Victor: Rollout. Hana, your plan? {question- @+1}
Hana: Phase one is five percent of customers. We watch it for a week before going wider. {claim- F8}
Victor: A week? Come on. Three days. {~}
Hana: A week. Banks don't get to move fast and break things.
Ibrahim: Sorry, my laptop's about to die, let me grab a charger. {drift- 1}
Chloe: What's the rollback trigger? Like, what number makes us pull it? {question- @+1}
Hana: Crash rate over one percent, or transfer failures over two percent, and we roll back. No meeting. {decision-} {~}
Victor: No meeting is a bit much.
Hana: No meeting is the point.
Ibrahim: Has the load test been run at full scale? {question- @+1}
Hana: It peaked at eight thousand requests a second without errors. {claim- F10}
Victor: Eight thousand. See? It's ready. {claim- F10} {~}
Hana: For phase one. Not for everyone at once.
Chloe: Are we telling support what's in phase one? They had two hundred and thirty tickets from the pilot alone. {question- @+5} {claim- F9}
Victor: Support will be fine.
Chloe: Support was not fine. Honestly, that's why the CSAT comments mention wait times.
Hana: Okay. Phase one at five percent, one week, with the rollback trigger as I said, automatic. That's the rollout. Decided. {decision+} {claim- F8}
Victor: Fine. A week.
Chloe: I'll brief the support leads on phase one before it starts. {action+} {~}
Victor: Who's going to explain the rollback rule to the board, though? {question+} {~}
Chloe: Honestly, I'm still thinking about the support queue.
## go_no_go :: The call; Victor's board promise comes out
Victor: Okay. The call. I want a go.
Hana: With all due respect, it's a conditional go. Transfer crash fixed, regulator notice filed, critical accessibility issues closed.
Ibrahim: For the record, I agree with conditional.
Chloe: Same.
Victor: Come on, the board demo is October thirtieth. I need to tell them something clean. {claim- F7}
Hana: Tell them it's conditional. That is clean.
Victor: I may have already told them it's a done deal.
Hana: You what? {~}
Ibrahim: Strictly speaking, you can't tell a board a launch is done before compliance signs off.
Victor: Okay, okay. I hear you.
Hana: So we're agreed? Conditional go for November twelfth, with the three conditions? {question- @+1} {claim- F12}
Victor: Bottom line, yes. Conditional go for the twelfth, three conditions. Final. {decision+} {claim- F12}
Hana: Thank you. And the board? {question- @+1}
Victor: I'll send the board an update on Monday with the conditions spelled out. {action+}
Chloe: Can I see that before it goes? {question- @+1}
Victor: Fine. You can all see it. {action+}
Ibrahim: Thank you, Victor.
