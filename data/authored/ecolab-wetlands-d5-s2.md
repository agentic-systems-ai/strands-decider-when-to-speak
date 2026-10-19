---
meeting_id: ecolab-wetlands-d5-s2
theme: Weekly meeting of a university ecology research lab
domain_pack: research_lab
drama: 0.5
seed: 2
author: claude-opus-5-5 (Claude Code session)
pack:
  title: Wetlands lab meeting
  org: Marsh and Wetlands Lab, Bayou State University (fictional)
  agenda:
    - {id: sensors, title: Sensor network, goal: Decide how to deal with the failed water-level sensors, timebox_min: 4}
    - {id: data, title: Data backlog, goal: Get the processing backlog under control, timebox_min: 4}
    - {id: conference, title: Conference abstracts, goal: Agree who submits what, timebox_min: 3}
    - {id: safety, title: Field safety, goal: Act on the April incident, timebox_min: 4}
  facts:
    - {id: F1, key: sensors_deployed, statement: "Water-level sensors deployed = 32", value: "32"}
    - {id: F2, key: sensors_failed, statement: "Sensors failed since winter = 7", value: "7"}
    - {id: F3, key: sensor_cost, statement: "Replacement sensor = $420 each", value: "$420"}
    - {id: F4, key: backlog_months, statement: "Unprocessed sensor data = 5 months", value: "5 months"}
    - {id: F5, key: storage_used, statement: "Lab storage used = 78% of quota", value: "78%"}
    - {id: F6, key: abstract_deadline, statement: "Abstract deadline = June 6", value: "June 6"}
    - {id: F7, key: abstracts_planned, statement: "Abstracts planned = 3", value: "3"}
    - {id: F8, key: incident_date, statement: "Field incident = April 22", value: "April 22"}
    - {id: F9, key: first_aid_certified, statement: "Field staff with first-aid certification = 4", value: "4"}
    - {id: F10, key: travel_budget, statement: "Travel budget remaining = $6,500", value: "$6,500"}
    - {id: F11, key: airboat_hours, statement: "Airboat hours remaining this season = 40", value: "40"}
    - {id: F12, key: lab_members, statement: "Lab members = 7", value: "7"}
personas:
  - name: Adaeze
    role: Principal investigator
    goals: A safe, productive field season
    hidden_agenda: The April incident scared her more than she shows
    verbosity: 3
    wpm: 155
    catchphrases: []
    voice_gender: female
  - name: Tomasz
    role: Postdoc, runs the data pipeline
    goals: Clear the backlog and present at the conference
    hidden_agenda: Wants to bring his partner to the conference city
    verbosity: 3
    wpm: 150
    catchphrases: []
    voice_gender: male
  - name: Riya
    role: PhD student
    goals: Get her first conference abstract accepted
    hidden_agenda: Nervous about presenting
    verbosity: 2
    wpm: 165
    catchphrases: []
    voice_gender: female
  - name: Wes
    role: Field technician
    goals: Working sensors and a working airboat
    hidden_agenda: Was the one who slipped in April
    verbosity: 3
    wpm: 145
    catchphrases: []
    voice_gender: male
---
## sensors :: How many are down; Wes undercounts, then the cost
Adaeze: Let's start with the sensors. Wes, how many are down? {question- @+1}
Wes: Three, as of last week. The ones out by the channel. {claim+ F2 "3"}
Tomasz: The pipeline shows seven with no data since winter. Three are the ones you've visited. {claim- F2}
Wes: Seven. I haven't been out to the far ones since the water came up. {claim- F2}
Adaeze: Out of thirty-two, that's a lot. {claim- F1}
Riya: How much is a replacement? {question- @+1}
Wes: Four hundred and twenty each. {claim- F3}
Tomasz: So almost three thousand to replace all seven. {~nc}
Adaeze: Can any of them be repaired instead? {question- @+1}
Wes: Maybe two. The others have water in the housing. That's the end of them.
Adaeze: Then we replace five and try to repair two. {decision+} {~}
Wes: I'll order the five sensors this week and take the two broken ones to the electronics shop. {action+}
Tomasz: We should really think about moving the sensors to higher ground at some point. {action-}
## data :: The backlog and storage; Riya's storage number stands
Adaeze: Data. Tomasz, where's the backlog? {question- @+1}
Tomasz: Five months of sensor data is unprocessed. The pipeline broke when the university changed servers. {claim- F4}
Riya: And we're at about ninety percent of our storage. {claim+ F5 "90%"}
Adaeze: Ninety? Then we can't even store new data for long. {~} {claim+ F5 "90%"}
Tomasz: Fixing the pipeline is a week of work. Then the backlog runs by itself over a weekend. {~}
Adaeze: Then the pipeline is your priority this week, ahead of the abstract. {decision+}
Tomasz: Ahead of the abstract. Fine, but the deadline's tight.
Riya: Could the raw data go to the archive service, to free up space? {question- @+1}
Tomasz: Yes, the older files can. I'll do that when the pipeline's back. {action+}
Wes: Did anyone see the cooking show where they made jambalaya with crawfish from a bayou? I swear it was our bayou. {drift+ 2} {~}
Riya: My roommate watches it every night. The host keeps saying "y'all" wrong.
## conference :: Abstracts; Tomasz's travel budget figure is high and is corrected later
Adaeze: Okay. Conference. The abstract deadline is June sixth. We planned three. {claim- F6} {claim- F7}
Tomasz: Mine, Riya's, and the sensor network one with Wes.
Riya: Do I really have to submit one? I've never presented. {question- @+1}
Adaeze: You do. You're ready, and a poster is a gentle start.
Riya: A poster. Okay. I can do a poster. {action+}
Tomasz: And the travel budget is ten thousand, so all three of us can go. {claim+ F10 "$10,000"}
Wes: I'd rather not go. Somebody has to keep the sensors alive.
Riya: Maybe Wes could present remotely? {decision-} {question- @+3}
Adaeze: I checked the grant account this morning. Travel has sixty-five hundred left, not ten. {claim- F10}
Tomasz: Sixty-five hundred. That's two people, not three. {claim- F10}
Adaeze: Then Riya and Tomasz go, and the sensor abstract is presented by Tomasz. {decision+}
Tomasz: Fair enough.
## safety :: The April incident; first aid; airboat hours
Adaeze: Safety. I want to talk about April twenty-second. {claim- F8}
Wes: I slipped off the boardwalk into the channel. I'm fine. It was my fault.
Adaeze: It wasn't a fault. It was a wet boardwalk and no second person. That's on the process.
Riya: How many of us have first-aid certification? {question- @+1}
Wes: Four. Me, Tomasz, and the two undergrads from last summer, who've left. {claim- F9}
Adaeze: So really two, out of seven of us. {claim- F12} {~}
Tomasz: Could the department pay for a first-aid course for everyone? {question- @+1}
Adaeze: They should. I'll ask the chair this week. {action+}
Wes: And nobody goes out alone. That should be a rule.
Adaeze: From today, nobody goes to the field alone, and the boardwalk sites need two people. {decision+}
Riya: What about the airboat? We have forty hours left. Does that need two people too? {question- @+1} {claim- F11}
Wes: The airboat always has two. You can't drive and anchor at the same time.
Tomasz: Is the department going to fix the boardwalk itself? {question+} {~}
Adaeze: Okay. Thank you, all. Wes, please be careful out there.
Wes: Always.
