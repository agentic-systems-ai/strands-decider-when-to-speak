---
meeting_id: sprint-payroll-d2-s1
theme: Sprint planning for a payments team at a fictional fintech
domain_pack: software_team
drama: 0.2
seed: 1
author: claude-opus-5-5 (Claude Code session)
pack:
  title: Payroll engine team - sprint 17 planning
  org: Penny Lane Payroll (fictional)
  agenda:
    - {id: retro_actions, title: Retro follow-ups, goal: Close or carry the open retro actions, timebox_min: 3}
    - {id: backlog, title: Top of the backlog, goal: Pick the sprint goal from the migration and the tax tables, timebox_min: 5}
    - {id: capacity, title: Capacity, goal: Fit the work to the holiday and the people, timebox_min: 4}
    - {id: dependencies, title: Dependencies and risks, goal: Name what could block us, timebox_min: 3}
  facts:
    - {id: F1, key: sprint_number, statement: "This is sprint 17", value: "17"}
    - {id: F2, key: avg_velocity, statement: "Average velocity = 31 points", value: "31"}
    - {id: F3, key: engineers, statement: "Engineers on the team = 4", value: "4"}
    - {id: F4, key: public_holidays, statement: "Public holidays in this sprint = 1", value: "1"}
    - {id: F5, key: payroll_run_date, statement: "Next big payroll run = March 28", value: "March 28"}
    - {id: F6, key: tax_table_deadline, statement: "New tax tables must be live by April 1", value: "April 1"}
    - {id: F7, key: open_payroll_bugs, statement: "Open payroll bugs = 9", value: "9"}
    - {id: F8, key: test_suite_runtime, statement: "Full test suite runtime = 42 minutes", value: "42 minutes"}
    - {id: F9, key: companies_migrated, statement: "Companies migrated to the new engine = 140", value: "140"}
    - {id: F10, key: migration_target, statement: "Companies to migrate by June = 600", value: "600"}
    - {id: F11, key: flaky_tests, statement: "Known flaky tests = 17", value: "17"}
    - {id: F12, key: open_retro_actions, statement: "Open retro actions = 3", value: "3"}
personas:
  - name: Tomas
    role: Engineering manager, runs planning
    goals: A calm sprint with the tax tables done early
    hidden_agenda: Wants to protect the team from another crunch like January
    verbosity: 3
    wpm: 150
    catchphrases: []
    voice_gender: male
  - name: Yuki
    role: Tech lead
    goals: Keep migrating companies at a steady pace
    hidden_agenda: Thinks the flaky tests are slowly poisoning morale
    verbosity: 3
    wpm: 155
    catchphrases: ["in practice"]
    voice_gender: female
  - name: Bea
    role: Product owner
    goals: Show progress on the migration to leadership
    hidden_agenda: Her quarterly target is the migration count
    verbosity: 3
    wpm: 165
    catchphrases: []
    voice_gender: female
  - name: Olu
    role: QA engineer
    goals: A test suite people trust
    hidden_agenda: Has a plan for the flaky tests he hasn't pitched yet
    verbosity: 2
    wpm: 145
    catchphrases: []
    voice_gender: male
---
## retro_actions :: The three open actions; one closes, two carry
Tomas: Morning, everyone. Sprint seventeen. Let's start with the retro actions, there are three still open. {claim- F1} {claim- F12}
Yuki: The first one was mine, the deploy checklist. That's done, it's in the wiki now.
Tomas: Great, that one closes. The second was the on-call handover notes.
Olu: That's still open. Nobody really owned it.
Tomas: Would you be willing to take it this sprint, Olu? {question- @+1}
Olu: Sure, I can take the handover notes. {action+}
Bea: And the third was the stakeholder demo. We never scheduled it.
Tomas: Let's leave the demo until the migration has something new to show. {decision-}
Bea: That's fair. Leadership will ask, though.
Yuki: In practice, they ask every sprint.
Bea: Who's going to tell them it's postponed again? {question+} {~}
## backlog :: Migration vs tax tables; Bea overstates the migration count and Yuki corrects it
Tomas: The backlog. Two big candidates: more migration batches, or the new tax tables.
Bea: The tax tables have a hard date. They have to be live by April first. {claim- F6}
Yuki: And the payroll run on March twenty-eighth has to use the old tables, so we can't switch early. {claim- F5}
Olu: So the switch has to happen in a three-day window. That's tight.
Tomas: How much of the tax work is already done? {question- @+1}
Yuki: The rates are loaded. What's left is the rounding rules and the year-end edge cases.
Bea: And on the migration side, we've moved about two hundred companies so far. {claim+ F9 "200"}
Yuki: I think it's a hundred and forty. Two hundred is the number for the end of this sprint, if it goes well. {claim- F9}
Bea: You're right, a hundred and forty. I was looking at the plan, not the actuals. {claim- F9}
Tomas: Out of six hundred by June. {claim- F10}
Bea: Which is why I want a migration batch in every sprint.
Yuki: In practice, I'd rather the sprint goal was the tax tables, with one small migration batch alongside.
Olu: What size is a small batch? {question- @+1}
Yuki: Forty companies. The ones on the simplest pay schedules. {~}
Bea: Forty is fine, as long as the batch happens.
Tomas: Okay. Sprint goal is the tax tables, plus one batch of forty simple companies. {decision+} {~}
Bea: I'll pick the forty companies and send Yuki the list by tomorrow. {action+}
## capacity :: The holiday, the people and the test suite; Olu's runtime figure goes unchallenged
Tomas: Capacity. We're four engineers, and there's one public holiday. {claim- F3} {claim- F4}
Yuki: Our average is thirty-one points. I'd plan to about twenty-seven with the holiday. {claim- F2} {~}
Tomas: Does anyone have time off planned? {question- @+1}
Olu: I'm out on the Friday of the second week. Nobody else, as far as I know.
Bea: Then twenty-seven feels right. {~}
Olu: The thing that eats our time is the test suite. It takes about half an hour for a full run. {claim+ F8 "half an hour"}
Yuki: And then it fails on a flaky test and you run it again.
Olu: There are seventeen known flaky tests. I'd like to fix the worst five this sprint. {claim- F11} {~}
Tomas: Do the flaky tests fit under twenty-seven points with everything else? {question- @+2} {~}
Bea: It would have to come out of the migration batch, wouldn't it? {question- @+1}
Yuki: Not necessarily. The tax work is mostly me and Kofi. Olu's capacity is separate.
Tomas: Then the five worst flaky tests go in as Olu's goal. {decision+}
Olu: Thank you. That'll help everyone, honestly.
Yuki: Kofi had his baby on Saturday, by the way. A girl. {drift+ 3}
Bea: Oh, wonderful! He sent a photo to the channel, she's tiny.
Olu: He said nobody has slept since Friday.
Tomas: That reminds me, Kofi's on paternity leave from next week, so he's not in the capacity.
Yuki: Oh. Then the tax work is mostly me.
Tomas: Could someone pair with Yuki on the rounding rules? {question- @+1}
Olu: I can. I know the rounding tests better than anyone. {action+}
## dependencies :: What could block us
Tomas: Dependencies and risks. What could stop us? {question- @+1}
Yuki: The tax authority sometimes publishes corrections late in March. If that happens, we redo some of the work. {~nc}
Bea: How often does that happen? {question- @+1}
Yuki: Two of the last three years.
Olu: Nine open payroll bugs is the other risk. Some of them touch the same code as the tax tables. {claim- F7}
Tomas: Are any of the nine likely to hit the March run? {question- @+1} {claim- F7}
Olu: One might. The overtime rounding one. I'd fix it before the run.
Tomas: Then the overtime rounding bug goes in first, before anything else. {decision+}
Yuki: It would be good if someone kept an eye on the tax authority's website this month. {action-}
Bea: I'll set up an alert for their bulletin page this afternoon. {action+}
Olu: Should we tell support about the tax table switch, in case customers notice? {question+}
Yuki: Do we have a rollback plan if the new tables are wrong on April first? {question- @+1} {claim- F6}
Tomas: We keep the old tables deployed and switch back with a flag. That's how we did it last year. Okay, I think that's a plan. Thanks, everyone. {decision+}
