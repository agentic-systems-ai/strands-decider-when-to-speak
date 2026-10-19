---
meeting_id: ecolab-alpine-d8-s2
theme: Weekly meeting of a university ecology research lab
domain_pack: research_lab
drama: 0.8
seed: 2
author: claude-opus-5-5 (Claude Code session)
pack:
  title: Alpine ecology lab meeting
  org: Ridgeway Alpine Ecology Lab, Northcrest University (fictional)
  agenda:
    - {id: errors, title: The dataset errors, goal: Understand the errors Leila found in the published dataset, timebox_min: 5}
    - {id: correction, title: The correction, goal: Decide how to correct the record, timebox_min: 4}
    - {id: fieldwork, title: Fieldwork, goal: Huts, helicopter lifts and loggers for the season, timebox_min: 4}
    - {id: morale, title: The lab, goal: Talk about how people are doing, timebox_min: 3}
  facts:
    - {id: F1, key: affected_records, statement: "Records affected by the unit error = 312", value: "312"}
    - {id: F2, key: total_records, statement: "Records in the published dataset = 9,800", value: "9,800"}
    - {id: F3, key: citations, statement: "Citations of the paper = 41", value: "41"}
    - {id: F4, key: hut_nights, statement: "Hut nights booked = 18", value: "18"}
    - {id: F5, key: helicopter_cost, statement: "Helicopter lift = $3,200 each", value: "$3,200"}
    - {id: F6, key: lifts_booked, statement: "Helicopter lifts booked = 2", value: "2"}
    - {id: F7, key: correction_window, statement: "Journal asks for corrections within 30 days of notice", value: "30 days"}
    - {id: F8, key: field_start, statement: "Field season starts July 7", value: "July 7"}
    - {id: F9, key: lab_members, statement: "Lab members = 8", value: "8"}
    - {id: F10, key: loggers_deployed, statement: "Temperature loggers deployed = 60", value: "60"}
    - {id: F11, key: loggers_recovered, statement: "Loggers recovered last season = 52", value: "52"}
    - {id: F12, key: grant_balance, statement: "Grant balance = $41,000", value: "$41,000"}
personas:
  - name: Gunnar
    role: Principal investigator
    goals: Protect the lab's reputation
    hidden_agenda: Wrote the script that introduced the error, years ago
    verbosity: 4
    wpm: 155
    catchphrases: []
    voice_gender: male
  - name: Leila
    role: Postdoc who found the errors
    goals: Fix the published record properly
    hidden_agenda: Afraid this will cost her the recommendation letter she needs
    verbosity: 3
    wpm: 160
    catchphrases: []
    voice_gender: female
  - name: Kai
    role: PhD student
    goals: Keep the field season on track
    hidden_agenda: Has been talking to another lab about switching
    verbosity: 2
    wpm: 165
    catchphrases: []
    voice_gender: male
  - name: Hester
    role: Lab manager
    goals: Logistics that work and a lab that isn't miserable
    hidden_agenda: Knows Kai is thinking of leaving
    verbosity: 3
    wpm: 145
    catchphrases: []
    voice_gender: female
---
## errors :: What Leila found; Gunnar minimizes it
Gunnar: Leila, you sent an email about the dataset. Let's hear it, briefly. {~}
Leila: Some of the soil temperature records were converted twice. Fahrenheit to Celsius, and then again. They're wrong in the published data.
Gunnar: How many records are we talking about? A handful? {question- @+2}
Kai: Is it the old logger script? The one from twenty sixteen? {question- @+1} {~nc}
Leila: Yes. It's three hundred and twelve records, out of ninety-eight hundred. {claim- F1} {claim- F2}
Gunnar: So about fifty that matter, realistically. The rest are in winter, when nothing grows. {claim+ F1 "50"}
Leila: All three hundred and twelve are wrong, Gunnar. They're in the published file. {claim- F1}
Gunnar: Three percent of the data. It doesn't change the conclusions. {~nc}
Leila: It changes figure four. The warming trend is smaller once you fix them.
Hester: How much smaller? {question- @+1}
Leila: The trend drops by about a third. It's still there, but it's weaker.
Gunnar: The paper has over a hundred citations. People rely on it. {claim+ F3 "over 100"}
Kai: That's exactly why it matters, isn't it? {~}
Gunnar: Nobody asked you, Kai.
Hester: Gunnar. That's not okay.
Gunnar: I'm sorry. Kai, I'm sorry. This is my paper, and it's hard to hear.
## correction :: How to fix the record; the citation count corrected
Leila: The journal wants corrections within thirty days of notice. I think we notify them now. {claim- F7}
Gunnar: Or we fix it quietly in the next paper. {decision-}
Leila: Quietly isn't an option. The data are public.
Hester: I checked the journal page while you were talking, Gunnar. It's forty-one citations, not over a hundred. {claim- F3}
Gunnar: Forty-one. It felt like more. {claim- F3}
Kai: Forty-one people who used the wrong numbers. {claim- F3} {~}
Gunnar: All right. All right. We notify the journal this week and publish a correction with the fixed data. {decision+}
Leila: Thank you. I'll draft the correction notice and the corrected figure. {action+}
Gunnar: I'll write to the editor myself. It should come from me, as the senior author. {action+}
Kai: Should we tell the people who cited it? {question- @+1}
Leila: The journal notifies them automatically when a correction is published.
## fieldwork :: Huts, helicopters and loggers; Kai's helicopter figure is low and is corrected; Hester's logger count stands
Hester: Fieldwork. We start on July seventh. Eighteen hut nights are booked. {claim- F8} {claim- F4}
Kai: And two helicopter lifts, at about two thousand each. {claim- F6} {claim+ F5 "$2,000"}
Hester: The loggers did well last winter. We recovered all sixty. {claim+ F11 "60"}
Gunnar: Good. The loggers are the whole study.
Kai: Can we afford a third lift, for the high plots? {question- @+1}
Gunnar: The grant balance is forty-one thousand. A lift is cheap compared to losing a season. {claim- F12}
Leila: Did anyone else see the avalanche video from the pass last week? The whole slope just went. {drift+ 3} {~}
Hester: The guides posted it. It's terrifying.
Kai: That's the slope right above the second hut.
Hester: Sorry, I'm looking at the invoice from last year. The helicopter was thirty-two hundred a lift, not two thousand. {claim- F5}
Kai: Thirty-two hundred. That changes the math a bit. {claim- F5}
Gunnar: We still book the third lift. I'd rather pay than risk the high plots. {decision+}
Hester: I'll call the helicopter company tomorrow and add the third lift. {action+}
Leila: It might be worth someone checking the second hut is safe after that avalanche. {action-}
## morale :: How people are doing
Hester: Last thing. I want to ask how everyone's doing. It's been a hard few weeks.
Kai: Honestly? Not great. I've been thinking about whether this lab is right for me. {~}
Gunnar: Because of today? {question- @+1}
Kai: Partly. Partly before today.
Leila: I was scared to raise the error at all. I thought it might cost me my reference letter.
Gunnar: It won't. Finding it was the right thing. I should have said that first.
Hester: Can we have a lab lunch next week, no agenda, just to talk? {question- @+1}
Gunnar: Yes. Please. I'll pay for it. {decision+} {action+}
Kai: Will the correction affect my thesis chapter that uses the same data? {question+} {~}
Gunnar: Thank you, all of you. Especially you, Leila.
