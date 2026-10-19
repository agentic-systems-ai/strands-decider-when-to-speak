---
meeting_id: sprint-brightwater-d8-s2
theme: Sprint planning for a payments team at a fictional fintech
domain_pack: software_team
drama: 0.8
seed: 2
author: claude-opus-5-5 (Claude Code session)
pack:
  title: Payments platform - sprint 9 planning (after the reorg)
  org: Brightwater Bank (fictional)
  agenda:
    - {id: reorg, title: The reorg, goal: Acknowledge the team changes and who owns what now, timebox_min: 4}
    - {id: deadline, title: Instant payments deadline, goal: Plan the regulatory work against March 31, timebox_min: 5}
    - {id: tech_debt, title: Tech debt, goal: Decide what legacy work to keep in flight, timebox_min: 3}
    - {id: oncall, title: On-call, goal: Make on-call survivable with fewer people, timebox_min: 3}
  facts:
    - {id: F1, key: instant_payments_deadline, statement: "Instant payments regulatory deadline = March 31", value: "March 31"}
    - {id: F2, key: team_size_after, statement: "Engineers after the reorg = 6", value: "6"}
    - {id: F3, key: team_size_before, statement: "Engineers before the reorg = 9", value: "9"}
    - {id: F4, key: velocity_last, statement: "Velocity last sprint = 22 points", value: "22"}
    - {id: F5, key: fine_risk, statement: "Regulatory fine for missing the deadline = up to $250,000 per month", value: "$250,000"}
    - {id: F6, key: open_sev2, statement: "Open severity-2 incidents = 3", value: "3"}
    - {id: F7, key: legacy_batch_jobs, statement: "Legacy batch jobs still running = 47", value: "47"}
    - {id: F8, key: pages_last_month, statement: "Pages last month = 31", value: "31"}
    - {id: F9, key: test_coverage, statement: "Test coverage on the payments core = 58%", value: "58%"}
    - {id: F10, key: deploys_per_week, statement: "Deploys per week = 2", value: "2"}
    - {id: F11, key: p99_latency, statement: "Payments API p99 latency = 840 ms", value: "840 ms"}
    - {id: F12, key: sprint_number, statement: "This is sprint 9", value: "9"}
personas:
  - name: Gemma
    role: New engineering manager, joined after the reorg
    goals: Earn the team's trust and hit the deadline
    hidden_agenda: Was told the team is "difficult"
    verbosity: 3
    wpm: 160
    catchphrases: []
    voice_gender: female
  - name: Mateo
    role: Staff engineer, on the team for six years
    goals: Protect the team from another impossible plan
    hidden_agenda: His best friend was moved to another team in the reorg
    verbosity: 4
    wpm: 165
    catchphrases: []
    voice_gender: male
  - name: Aisha
    role: Product manager for payments
    goals: Meet the regulatory deadline at any cost
    hidden_agenda: The compliance director reports her progress weekly to the board
    verbosity: 3
    wpm: 170
    catchphrases: []
    voice_gender: female
  - name: Lukas
    role: Site reliability engineer
    goals: Fewer pages
    hidden_agenda: Interviewing elsewhere
    verbosity: 2
    wpm: 145
    catchphrases: []
    voice_gender: male
---
## reorg :: The elephant in the room; Mateo misremembers the old team size
Gemma: Hi, everyone. Sprint nine, and my first planning with you. I know the reorg was hard. {claim- F12}
Mateo: Hard is one word for it. We were twelve engineers last month. Now we're six. {claim+ F3 "12"} {claim- F2}
Aisha: The scope didn't shrink, though.
Gemma: I want to be honest about what six people can do. I'm not going to pretend. {claim- F2}
Lukas: Who owns the batch jobs now? Nobody told us. {question- @+1}
Gemma: We do. All forty-seven of them, unfortunately. {claim- F7}
Mateo: Forty-seven batch jobs, written by people who aren't here anymore. {claim- F7}
Aisha: Can we not spend the whole meeting on the reorg? We have a deadline. {~}
Mateo: The reorg is why the deadline is a problem.
Gemma: Both are true. Let's do the deadline, but I'm not ignoring the rest.
## deadline :: Instant payments; Aisha's fine figure is inflated and corrected
Aisha: Instant payments has to be live by March thirty-first. If we miss it, the fine is a million a month. {claim- F1} {claim+ F5 "$1,000,000"}
Lukas: A million? I thought it was much lower than that. {question- @+1} {~}
Gemma: The compliance memo says up to two hundred and fifty thousand a month. Still very serious. {claim- F5}
Aisha: Two fifty. Okay. I'd heard a million in the board meeting. {claim- F5}
Mateo: Last sprint we did twenty-two points. Instant payments is at least a hundred. {claim- F4} {~}
Gemma: Then it's five sprints, and we have five sprints. With nothing else.
Lukas: With nothing else is never true. We have three sev-twos open right now. {claim- F6}
Aisha: What if we cut the reporting dashboard from instant payments? Regulators don't need it at launch. {question- @+1} {decision-}
Mateo: That's maybe fifteen points. It helps. {~}
Gemma: Then the dashboard comes out of the launch scope. It goes in the first update after March. {decision+} {~nc}
Aisha: I'll tell the compliance director today that the dashboard moves. {action+}
Mateo: And the API latency. We're at eight forty milliseconds at p99. Instant payments needs better than that. {claim- F11}
Lukas: Somebody really ought to profile the payments API before we pile more on it. {action-}
Mateo: I'll profile it this sprint. It's my code anyway, from before. {action+}
## tech_debt :: What to keep in flight; Gemma's coverage number goes unchallenged
Gemma: Tech debt. Our test coverage on the payments core is about seventy percent, so we're not in terrible shape. {claim+ F9 "70%"}
Mateo: Seventy is fine for most things. {claim+ F9 "70%"}
Lukas: The batch jobs have no tests at all. That's where it hurts.
Aisha: Can the batch jobs wait until after March? {question- @+1} {~nc}
Mateo: Most of them, yes. Three of them break every month-end. Those can't wait.
Gemma: Then we fix the three month-end jobs and freeze the rest until April. {decision+}
Lukas: My brother just started a job at a bakery. Four a.m. starts. He says it's still better than on-call. {drift+ 3}
Mateo: He's not wrong.
Aisha: Four a.m. every day, though? {~}
Gemma: On-call. Let's talk about it properly.
## oncall :: Fewer people, same pages; Lukas undercounts the pages, then corrects himself
Lukas: Last month we had about fifteen pages. Which is a lot for six people. {claim+ F8 "15"}
Mateo: Fifteen? It felt like double. {~nc}
Lukas: You're right, let me look. Thirty-one. Fifteen was the night ones only. {claim- F8}
Gemma: Thirty-one pages for six people is not survivable. {claim- F8} {claim- F2}
Aisha: Could the old team still help with the batch job pages during the transition? {question- @+1}
Gemma: I'll ask their manager this week. I'd rather ask than assume. {action+}
Mateo: And we deploy twice a week. Every deploy is a page risk. {claim- F10}
Lukas: Maybe we freeze deploys the week before March thirty-first. {decision-} {claim- F1}
Gemma: Let's see how February goes before we freeze anything.
Mateo: Who decided the reorg dates in the first place? {question+} {~}
Gemma: Mateo, I hear you. I'll carry that upward. That's all for today, everyone. Thank you for being honest with me. {action+}
Lukas: Thanks, Gemma.
