---
meeting_id: ecolab-pollinator-d2-s2
theme: Weekly meeting of a university ecology research lab
domain_pack: research_lab
drama: 0.2
seed: 2
author: claude-opus-5-5 (Claude Code session)
pack:
  title: Pollinator lab weekly meeting
  org: Highland Pollinator Lab, Glenmoor University (fictional)
  agenda:
    - {id: surveys, title: Summer bee surveys, goal: Finalize sites and traps for the season, timebox_min: 4}
    - {id: move, title: The lab move, goal: Plan the move to the new building, timebox_min: 4}
    - {id: papers, title: Papers, goal: Status of the two papers under review, timebox_min: 3}
    - {id: undergrads, title: Undergraduate program, goal: Plan the summer research assistants, timebox_min: 3}
  facts:
    - {id: F1, key: survey_sites, statement: "Survey sites = 22", value: "22"}
    - {id: F2, key: species_recorded, statement: "Bee species recorded so far = 87", value: "87"}
    - {id: F3, key: pan_traps, statement: "Pan traps = 140", value: "140"}
    - {id: F4, key: move_date, statement: "Lab move = August 15", value: "August 15"}
    - {id: F5, key: freezers, statement: "Freezers to move = 3", value: "3"}
    - {id: F6, key: papers_in_review, statement: "Papers under review = 2", value: "2"}
    - {id: F7, key: undergrads, statement: "Undergraduate assistants this summer = 6", value: "6"}
    - {id: F8, key: stipend, statement: "Undergraduate pay = $15 per hour", value: "$15"}
    - {id: F9, key: grant_end, statement: "Current grant ends December 31", value: "December 31"}
    - {id: F10, key: specimens_pinned, statement: "Specimens pinned = 4,600", value: "4,600"}
    - {id: F11, key: conference_date, statement: "Regional conference = October 2", value: "October 2"}
    - {id: F12, key: greenhouse_bays, statement: "Greenhouse bays in the new building = 4", value: "4"}
personas:
  - name: Odile
    role: Principal investigator
    goals: A smooth move and a productive summer
    hidden_agenda: Writing the grant renewal and anxious about it
    verbosity: 3
    wpm: 145
    catchphrases: []
    voice_gender: female
  - name: Sanjay
    role: Postdoc, runs the surveys
    goals: More sites, more species
    hidden_agenda: Wants a site in the mountains that is a long drive away
    verbosity: 3
    wpm: 155
    catchphrases: []
    voice_gender: male
  - name: Bryn
    role: PhD student
    goals: Get the first paper through review
    hidden_agenda: Reviewer two has been harsh and Bryn is discouraged
    verbosity: 2
    wpm: 150
    catchphrases: []
    voice_gender: female
  - name: Lottie
    role: Lab coordinator, runs the undergraduate program
    goals: A good summer for the undergrads
    hidden_agenda: Has been promised a bigger budget than the grant has
    verbosity: 3
    wpm: 165
    catchphrases: []
    voice_gender: female
---
## surveys :: Sites and traps; Sanjay's site count is high
Odile: Good morning. Surveys first, since the season starts soon. Sanjay? {question- @+1}
Sanjay: We'll survey about thirty sites this summer, same as last year. {claim+ F1 "30"}
Lottie: I have twenty-two on the permit list. Did we add some? {claim- F1} {question- @+1}
Sanjay: No, you're right, twenty-two. I was thinking of the sites we scouted, not the ones we kept. {claim- F1}
Odile: Twenty-two is plenty. How many traps? {claim- F1} {question- @+1}
Sanjay: A hundred and forty pan traps. Most of them survived the winter in the shed. {claim- F3}
Bryn: The species count is up to eighty-seven, by the way. Two new ones from the meadow site last week. {claim- F2}
Odile: Eighty-seven. That's wonderful. {claim- F2}
Sanjay: I'd still love to add a mountain site. The bees up there are completely different.
Odile: How far is the mountain site? {question- @+1}
Sanjay: About three hours each way.
Lottie: That's a full day of driving for one site. 
Sanjay: Could we drop a couple of the meadow sites to make room for it? {decision-} {question- @+1}
Odile: Let's leave the mountain site for next year, when we have the new grant. {decision+}
Sanjay: Fair. I'll scout it on a weekend anyway, out of curiosity. {action+}
Bryn: The meadow farmer asked if we could share our species list with him. He's very proud of his bees.
Odile: Of course. I'll send him a copy with a thank-you note. {action+} 
Bryn: He'll love that.
## move :: The new building
Odile: The move. We go to the new building on August fifteenth. {claim- F4}
Lottie: That's right in the middle of the field season.
Odile: I know. The university picked the date.
Bryn: What happens to the specimens? {question- @+1}
Sanjay: Forty-six hundred pinned specimens, in drawers. They move as they are, carefully. {claim- F10}
Lottie: And three freezers. Those need a proper moving company. {claim- F5}
Odile: Then the freezers go with the university's movers and the specimens go with us, by hand. {decision+}
Bryn: Are there greenhouse bays in the new building? {question- @+1}
Odile: Four. More than we have now. {claim- F12}
Sanjay: Four bays. We could finally run the nesting experiment. {claim- F12}
Lottie: My cousin moved labs last year and they lost a whole freezer of samples because the power was off for an hour. {drift+ 2}
Bryn: That's my nightmare. Literally, I've had that dream.
Odile: Let's not lose any freezers. Lottie, could you ask facilities about backup power for the move day? {question- @+1}
Lottie: I'll email facilities this afternoon. {action+}
## papers :: Two in review
Odile: Papers. Two are under review. {claim- F6}
Bryn: Mine came back from reviewer two. They want a whole new analysis. {~nc}
Odile: How big a change? {question- @+1}
Bryn: A few weeks of work, if I do it properly. I'm a bit discouraged, honestly.
Odile: That's normal. The analysis they asked for is fair. It'll make the paper better.
Sanjay: I can help with the model. I did something similar last year. {action+}
Bryn: Thank you. That helps more than you know.
Odile: The other paper is still waiting for the editor.
## undergrads :: The summer program; Lottie's headcount stands
Lottie: Undergrads. We have eight starting in June. {claim+ F7 "8"}
Odile: At fifteen dollars an hour? {question- @+1} {claim- F8}
Lottie: Fifteen, yes. The department raised it last year. {claim- F8}
Sanjay: Eight is great for the surveys. Two per vehicle. {claim+ F7 "8"}
Bryn: Could they each get a small project of their own, not just trap duty? {question- @+1}
Odile: Yes. Pick something they can present at the regional conference on October second. {claim- F11}
Lottie: I'll draft a list of small projects and share it before June. {action+}
Sanjay: Somebody will need to do safety training with them on the first day. {action-}
Odile: When does the grant end, again? I want to make sure the summer pay is covered. {question- @+1}
Lottie: December thirty-first. The summer is covered. {claim- F9}
Bryn: Will the new building have parking for the field vehicles? {question+} {~}
Odile: Thank you, everyone. A good week. Let's have a good summer.
