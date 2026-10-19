---
meeting_id: sprint-kestrel-d5-s2
theme: Sprint planning for a payments team at a fictional fintech
domain_pack: software_team
drama: 0.5
seed: 2
author: claude-opus-5-5 (Claude Code session)
pack:
  title: Wallet team - sprint planning
  org: Kestrel Pay (fictional mobile wallet)
  agenda:
    - {id: followups, title: Incident follow-ups, goal: Close the action items from last week's top-up incident, timebox_min: 4}
    - {id: roadmap, title: Top-up reliability vs card controls, goal: Pick this sprint's main bet, timebox_min: 5}
    - {id: estimates, title: Estimates, goal: Size the chosen work, timebox_min: 3}
    - {id: process, title: Meeting load, goal: Decide what to cut from the team's meetings, timebox_min: 3}
  facts:
    - {id: F1, key: topup_failure_rate, statement: "Top-up failure rate = 2.4%", value: "2.4%"}
    - {id: F2, key: card_controls_requests, statement: "Customer requests for card controls = 340", value: "340"}
    - {id: F3, key: avg_velocity, statement: "Average velocity over 3 sprints = 26 points", value: "26"}
    - {id: F4, key: engineers, statement: "Engineers on the team = 5", value: "5"}
    - {id: F5, key: incident_actions_open, statement: "Open incident action items = 4", value: "4"}
    - {id: F6, key: meeting_hours, statement: "Meeting hours per engineer per week = 9", value: "9"}
    - {id: F7, key: app_rating, statement: "App store rating = 4.1", value: "4.1"}
    - {id: F8, key: daily_topups, statement: "Daily top-ups = 18,000", value: "18,000"}
    - {id: F9, key: release_train, statement: "Next release train = November 14", value: "November 14"}
    - {id: F10, key: design_backlog, statement: "Screens waiting for design review = 6", value: "6"}
    - {id: F11, key: topup_contacts, statement: "Support contacts about top-ups per month = 1,150", value: "1,150"}
    - {id: F12, key: sprint_length, statement: "Sprint length = 2 weeks", value: "2 weeks"}
personas:
  - name: Hannah
    role: Engineering manager
    goals: Fewer fires, more focus time
    hidden_agenda: Her team's survey said meetings were the top complaint
    verbosity: 3
    wpm: 160
    catchphrases: []
    voice_gender: female
  - name: Ravi
    role: Senior engineer, owns top-ups
    goals: Fix top-up reliability properly
    hidden_agenda: Embarrassed that the incident was in his code
    verbosity: 3
    wpm: 150
    catchphrases: []
    voice_gender: male
  - name: Chen
    role: Product manager
    goals: Ship card controls before the competitor does
    hidden_agenda: Leadership asked for card controls by name
    verbosity: 4
    wpm: 170
    catchphrases: []
    voice_gender: male
  - name: Lola
    role: Product designer
    goals: Get the review backlog moving
    hidden_agenda: Has six screens waiting and feels ignored
    verbosity: 2
    wpm: 155
    catchphrases: []
    voice_gender: female
---
## followups :: The four open items from the incident; Ravi lowballs the failure rate
Hannah: Morning. Let's start with the incident follow-ups. There are four still open. {claim- F5}
Ravi: Two are mine. The retry logic and the alert on the bank callback.
Hannah: Where are they? {question- @+1}
Ravi: The alert is done, it went in yesterday. The retry logic is half done.
Chen: And the failure rate's back to normal now, right? About one percent? {claim+ F1 "1%"} {question- @+1}
Ravi: Roughly, yes. It's settled down. {claim+ F1 "1%"} {~}
Lola: The other two items are the status banner and the support macro. Both were mine and Hannah's. {~nc}
Hannah: The macro's done. The banner is waiting on design, which is, Lola, you. {~}
Lola: It's one of six screens waiting for review. I keep asking for a slot. {claim- F10}
Hannah: Then we'll give you a slot. That's on me. {action+}
Lola: Thank you.
Chen: It'd be good if someone wrote the incident up for the engineering blog. {action-}
## roadmap :: Reliability vs card controls; Chen's demand number is inflated
Hannah: The big choice. Top-up reliability, or card controls.
Chen: Card controls. Over a thousand customers have asked for them. It's the most requested feature we have. {claim+ F2 "over 1,000"}
Ravi: Is it a thousand? I thought the request count was in the hundreds. {question- @+1} {~nc}
Chen: Let me check. Three hundred and forty. A thousand was all the feedback mentioning cards at all. {claim- F2}
Ravi: Three forty. Meanwhile top-ups are eighteen thousand a day, and every failure is someone stuck at a till. {claim- F2} {claim- F8}
Lola: And support gets over a thousand contacts a month about top-ups. {claim- F11}
Chen: Leadership asked for card controls by name.
Hannah: Leadership also asked why the rating dropped to four point one. {claim- F7}
Ravi: I pulled the numbers this morning. I said one percent earlier, that was wrong. The failure rate is two point four. {claim- F1} {~nc}
Chen: Two point four. That's worse than I thought. {claim- F1} {~nc}
Hannah: Then reliability first. Card controls get a design spike so we're ready next sprint. {decision+}
Chen: A spike. Fine. As long as it's real.
Lola: I'll do the card controls designs this sprint, if the review slot happens. {action+}
## estimates :: Sizing; a detour into Lola's pottery class
Hannah: Estimates. Ravi, the retry logic and the reliability work.
Ravi: Thirteen points for retries done properly, plus five for the bank timeout handling. {~}
Hannah: We average twenty-six, with five engineers. That leaves room. {claim- F3} {claim- F4}
Chen: And the spike? {question- @+1}
Hannah: Three points, time-boxed. {~}
Lola: I finally finished my first bowl at the pottery class. It's lopsided, but it holds soup. {drift+ 3}
Chen: Pictures, or it didn't happen.
Ravi: My sister does pottery. She says the first fifty are all lopsided.
Hannah: Can we fit the banner and the design review backlog in too? {question- @+1}
Ravi: The banner, yes. It's small once Lola's done.
Hannah: Okay, retries, timeout handling, the banner and the spike. That's the sprint. {decision+} {~} 
Chen: Works for me.
## process :: Meeting load; the hours number goes unchecked
Hannah: Last thing. The survey said meetings are the top complaint. We spend about five hours a week each in meetings. {claim+ F6 "5 hours"}
Ravi: It feels like more.
Chen: Which ones can go? {question- @+1}
Lola: The Wednesday sync. It repeats standup.
Ravi: And standup could be async two days a week.
Chen: I'd keep standup daily. Async means I find out about problems late. {decision-}
Hannah: Then we cut the Wednesday sync and try async standup on Tuesdays and Thursdays for this sprint. {decision+}
Ravi: Could we also protect Friday mornings? No meetings at all. {question- @+1}
Hannah: Yes. I'll block Friday mornings on everyone's calendar today. {action+}
Lola: Who tells the other teams we've dropped the Wednesday sync? They join it sometimes. {question+} {~}
Chen: The release train is on November fourteenth, so the retries need to be in by then. {claim- F9}
Ravi: They'll be in. I'll have the retry logic in review by the eleventh. {action+}
Hannah: Good. Thanks, everyone.
