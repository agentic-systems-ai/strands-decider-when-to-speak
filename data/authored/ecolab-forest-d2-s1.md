---
meeting_id: ecolab-forest-d2-s1
theme: Weekly meeting of a university ecology research lab
domain_pack: research_lab
drama: 0.2
seed: 1
author: claude-opus-5-5 (Claude Code session)
pack:
  title: Forest ecology lab - weekly meeting
  org: Pine Ridge Forest Ecology Lab, Alder State University (fictional)
  agenda:
    - {id: census, title: Plot census, goal: Plan the permanent plot re-census, timebox_min: 4}
    - {id: drones, title: Drone survey, goal: Decide on the LiDAR rental and the remaining flights, timebox_min: 4}
    - {id: students, title: Student progress, goal: Check thesis timelines, timebox_min: 4}
    - {id: outreach, title: School outreach day, goal: Plan the visit from the middle school, timebox_min: 3}
  facts:
    - {id: F1, key: permanent_plots, statement: "Permanent plots = 48", value: "48"}
    - {id: F2, key: trees_tagged, statement: "Trees tagged across all plots = 6,300", value: "6,300"}
    - {id: F3, key: census_interval, statement: "Re-census interval = 5 years", value: "5 years"}
    - {id: F4, key: drone_flights_done, statement: "Drone flights completed = 21", value: "21"}
    - {id: F5, key: drone_batteries, statement: "Working drone batteries = 6", value: "6"}
    - {id: F6, key: lidar_rental, statement: "LiDAR sensor rental = $2,400 per week", value: "$2,400"}
    - {id: F7, key: defense_date, statement: "Mariana's thesis defense = May 9", value: "May 9"}
    - {id: F8, key: chapters_drafted, statement: "Thesis chapters drafted = 2 of 4", value: "2"}
    - {id: F9, key: outreach_date, statement: "Outreach day = April 18", value: "April 18"}
    - {id: F10, key: visiting_students, statement: "Middle school students visiting = 75", value: "75"}
    - {id: F11, key: mileage_budget, statement: "Field vehicle mileage budget = 3,000 miles", value: "3,000"}
    - {id: F12, key: seedling_mortality, statement: "Seedling mortality since last census = 31%", value: "31%"}
personas:
  - name: Chidi
    role: Principal investigator
    goals: A careful census and students who finish on time
    hidden_agenda: Is quietly planning a sabbatical next year
    verbosity: 3
    wpm: 140
    catchphrases: []
    voice_gender: male
  - name: Lars
    role: Postdoc, coordinates fieldwork
    goals: Get the LiDAR data this season
    hidden_agenda: The LiDAR data is central to his fellowship application
    verbosity: 3
    wpm: 155
    catchphrases: []
    voice_gender: male
  - name: Mariana
    role: Master's student
    goals: Defend in May
    hidden_agenda: Has drafted less than she lets on
    verbosity: 2
    wpm: 160
    catchphrases: []
    voice_gender: female
  - name: Pat
    role: Lab technician
    goals: Equipment that works and a realistic schedule
    hidden_agenda: Has been asked to run the outreach day alone again
    verbosity: 3
    wpm: 150
    catchphrases: []
    voice_gender: female
---
## census :: The re-census plan; Lars undercounts the plots
Chidi: Good afternoon. Let's start with the census. Lars, where are we with the plan? {question- @+1}
Lars: We'll re-census all the permanent plots this summer. That's about forty plots. {claim+ F1 "40"}
Pat: Forty-eight, I think. The eight we added along the creek count too. {claim- F1}
Lars: Right, forty-eight with the creek plots. Thanks, Pat. {claim- F1}
Chidi: And how many trees is that in total? {question- @+1}
Pat: Sixty-three hundred tagged trees. Some tags will be gone, of course. {claim- F2}
Mariana: When was the last full census? {question- @+1}
Chidi: Five years ago. It's on a five-year cycle. {claim- F3}
Lars: Seedling mortality has been high since then. Roughly half the seedlings died, from the plots I've checked. {claim+ F12 "50%"}
Chidi: That would be a lot. Let's see what the full census says.
Pat: The truck is the other question. We've got a three thousand mile budget for the season. {claim- F11}
Lars: Forty-eight plots over that many miles should be fine if we group them by area. {claim- F1}
Pat: I'll plan the route so we visit the plots by area, two days per cluster. {action+}
## drones :: The LiDAR rental decision; batteries; a short detour about the conference hotel
Chidi: The drone survey. Lars? {question- @+1}
Lars: We've done twenty-one flights with the regular camera. For the canopy structure, we need the LiDAR sensor. {claim- F4}
Chidi: What does the rental cost? {question- @+1}
Lars: Twenty-four hundred a week. I'd like two weeks. {claim- F6} {~}
Pat: The batteries are the limit. We have six that hold a charge. {claim- F5}
Lars: Six is enough for about two flights a day. {claim- F5} {~}
Chidi: Is one week enough if we plan the flights carefully? {question- @+1} {decision-}
Lars: One week is enough for the core plots. Two would cover the creek plots as well.
Chidi: Then let's rent it for one week, and we'll consider a second week if the weather is kind. {decision+} 
Pat: Who's actually certified to fly with the LiDAR payload? {question+} {~}
Lars: That works. I'll book the sensor for the first week of June. {action+}
Mariana: Is the conference hotel booked for July, by the way? I saw prices going up. {drift+ 2} {question- @+1}
Pat: I booked it last month. You're sharing with the student from Oregon.
## students :: Mariana's thesis; the honest version comes out
Chidi: Good. Let's talk about student progress. Mariana, how's the thesis going? {question- @+1}
Mariana: It's going. I have two of the four chapters drafted. {claim- F8}
Chidi: And the defense is on May ninth. {claim- F7}
Mariana: Yes. May ninth. {claim- F7}
Lars: Two chapters with about ten weeks to go. That's doable, but tight. {claim- F8} {~}
Chidi: Which chapters are left? {question- @+1}
Mariana: The seedling chapter and the discussion. The seedling data shows about fifty percent mortality, so it's a big story. {claim+ F12 "50%"}
Pat: Sorry, I just checked the summary sheet. It's thirty-one percent, not fifty. {claim- F12}
Lars: That was my number earlier. I only had the north plots in mind.
Mariana: Thirty-one. Still a story, just a smaller one. {claim- F12}
Chidi: Could we meet weekly until the defense, just for half an hour? {question- @+1}
Mariana: Yes, please. That would help me keep moving.
Chidi: Then weekly meetings on Tuesdays until May. {decision+} {~nc}
Mariana: I'll send you the seedling chapter outline before next Tuesday. {action+}
Lars: It might help if someone read the methods chapter with fresh eyes. {action-}
Pat: Excuse me, the delivery driver is here with the soil cores. One moment. {drift- 1}
## outreach :: The middle school visit; Pat's student count stands
Chidi: Outreach day. Pat, you've been organizing it. {~}
Pat: It's on April eighteenth. Ninety students are coming from Cedar Middle School. {claim- F9} {claim+ F10 "90"}
Lars: Ninety is a lot of twelve-year-olds in one forest. {claim+ F10 "90"}
Pat: It is. I'd like help. Last year I ran it on my own.
Chidi: That's not fair on you. Who can help on the day? {question- @+1}
Mariana: I can come in the morning, before my writing day. {action+}
Lars: I'll take the afternoon group and do the tree measuring station. {action+}
Pat: Thank you both. That makes a real difference.
Mariana: Do we have enough hand lenses for that many students? {question+}
Chidi: What happens if it rains? {question- @+1}
Pat: We move into the teaching lab and do the leaf pressing station instead.
Chidi: I think that's everything. Thank you, all. Good week, everyone.
