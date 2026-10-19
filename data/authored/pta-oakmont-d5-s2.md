---
meeting_id: pta-oakmont-d5-s2
theme: School PTA budget meeting for next year
domain_pack: community_budget
drama: 0.5
seed: 2
author: claude-opus-5-5 (Claude Code session)
pack:
  title: PTA budget meeting
  org: Oakmont Middle School PTA (fictional)
  agenda:
    - {id: position, title: Where we stand, goal: Balance, income and membership, timebox_min: 3}
    - {id: tech_vs_arts, title: Chromebooks and the arts, goal: Decide between the two big requests, timebox_min: 6}
    - {id: smaller_asks, title: Smaller requests, goal: Band uniforms and Science Olympiad, timebox_min: 3}
    - {id: vote, title: The vote, goal: Agree what goes to members, timebox_min: 3}
  facts:
    - {id: F1, key: balance, statement: "Current balance = $14,200", value: "$14,200"}
    - {id: F2, key: income, statement: "Annual income = $27,600", value: "$27,600"}
    - {id: F3, key: chromebook_request, statement: "Chromebook request = $9,000", value: "$9,000"}
    - {id: F4, key: arts_request, statement: "Arts program request = $4,500", value: "$4,500"}
    - {id: F5, key: students, statement: "Students = 610", value: "610"}
    - {id: F6, key: chromebook_ratio, statement: "Students per Chromebook = 3", value: "3"}
    - {id: F7, key: band_uniforms, statement: "Band uniforms = $3,800", value: "$3,800"}
    - {id: F8, key: olympiad_fees, statement: "Science Olympiad fees = $1,250", value: "$1,250"}
    - {id: F9, key: dues, statement: "Membership dues = $20", value: "$20"}
    - {id: F10, key: members, statement: "Member families = 245", value: "245"}
    - {id: F11, key: tech_grant, statement: "District tech grant received = $5,000", value: "$5,000"}
    - {id: F12, key: vote_date, statement: "Membership vote = April 30", value: "April 30"}
personas:
  - name: Deborah
    role: PTA president
    goals: A balanced budget nobody storms out over
    hidden_agenda: Her daughter is in the art club
    verbosity: 3
    wpm: 155
    catchphrases: []
    voice_gender: female
  - name: Nnamdi
    role: Treasurer
    goals: Spend the grant money on what it was given for
    hidden_agenda: Already told the district the grant would go to devices
    verbosity: 2
    wpm: 140
    catchphrases: []
    voice_gender: male
  - name: Carla
    role: Art teacher
    goals: Save the arts program
    hidden_agenda: Has been buying clay with her own money
    verbosity: 4
    wpm: 165
    catchphrases: []
    voice_gender: female
  - name: Trevor
    role: Parent, works in IT
    goals: Every kid with a working laptop
    hidden_agenda: His son's Chromebook broke and he waited six weeks for a loaner
    verbosity: 4
    wpm: 175
    catchphrases: []
    voice_gender: male
---
## position :: Balance and membership; Deborah's member count stands
Deborah: Okay, let's get going. Nnamdi, the big picture first. {~}
Nnamdi: The balance is fourteen thousand two hundred. Income this year was twenty-seven six. {claim- F1} {claim- F2}
Deborah: And we have about three hundred member families now, which is a record. {claim+ F10 "300"}
Trevor: Dues are still twenty dollars? {question- @+1} {claim- F9}
Nnamdi: Twenty. We haven't raised them in years. {claim- F9}
Carla: Please don't raise them. Some families already struggle with the field trip fees.
Deborah: Nobody's raising dues tonight. {decision-}
Trevor: Good.
## tech_vs_arts :: Chromebooks vs the arts; two wrong figures, both corrected
Deborah: The two big requests. Chromebooks, and the arts program.
Trevor: The Chromebooks are nine thousand. Right now five kids share every machine. It's absurd. {claim- F3} {claim+ F6 "5"}
Carla: Is it five? The tech office told me one between three, I think. I might be wrong. {claim- F6} {~nc}
Trevor: Three. Okay, three. Still absurd for a school with six hundred and ten kids. {claim- F6} {claim- F5}
Carla: The arts request is forty-five hundred. Clay, paint, and the kiln repair. {claim- F4}
Trevor: The kiln's been broken since before my son started here.
Carla: Two winters. The kids keep asking when they can fire their pots.
Nnamdi: We also have the district tech grant. That has to go to devices.
Trevor: The grant was ten thousand, so the Chromebooks are basically covered already. {claim+ F11 "$10,000"}
Deborah: If the grant covers the Chromebooks, then the arts request is easy.
Carla: That would be wonderful. I've been buying clay out of my own pocket since October.
Nnamdi: Sorry, I'm looking at the award letter. The grant is five thousand, not ten. {claim- F11}
Trevor: Five. Then there's a four thousand gap on the Chromebooks. {claim- F11} {~nc}
Deborah: So it's both requests, with five thousand of help. Can we afford both? {question- @+1} {claim- F11}
Nnamdi: Both together is thirteen five. With the grant, eighty-five hundred from us. We'd be down to under six thousand. {~nc}
Carla: Under six thousand is still a reserve. {~nc}
Trevor: Who decides which matters more, a laptop or a kiln? {question+} {~}
Carla: Have you seen what kids make in that art room? Some of them only come to school for it. {~}
Deborah: Both matter. Could we fund the arts fully and the Chromebooks over two years? {question- @+1} {decision-}
Trevor: Two years means another year of kids sharing.
Nnamdi: With the grant plus half our part this year, we could replace the oldest machines first.
Deborah: Then: arts funded in full, and the Chromebooks in two stages, oldest machines first. That's our proposal. {decision+}
Trevor: I can live with that. I'll help the tech office pick the oldest machines. {action+}
## smaller_asks :: Uniforms and the Olympiad; a short tangent about a robotics video
Deborah: Smaller asks. Band uniforms, and Science Olympiad.
Nnamdi: Uniforms are thirty-eight hundred. Olympiad fees are twelve fifty. {claim- F7} {claim- F8}
Carla: The band uniforms are from the nineties. The kids call them the pajamas.
Trevor: Did anyone see the video of the high school's robot climbing the stairs? It went everywhere online. {drift+ 3} {~}
Carla: The one that fell down at the end? My students watched it twenty times. {~nc}
Deborah: My husband sent it to me three times.
Nnamdi: The Olympiad fees are small. I'd fund those without discussion.
Deborah: Agreed. Olympiad funded. Uniforms next year, unless a sponsor turns up. {decision+}
Carla: It would be good if somebody asked the music store downtown about sponsoring uniforms. {action-}
## vote :: Getting it to members
Deborah: The vote is April thirtieth. {claim- F12}
Nnamdi: I'll send the draft to the board by the fifteenth. {action+}
Carla: Should teachers speak at the vote, to explain the requests? {question- @+1}
Deborah: Yes, briefly. Two minutes each.
Trevor: Can I bring one of the broken Chromebooks? A visual helps. {question- @+1}
Deborah: Bring it. People should see it. Thank you, everyone. That was a real discussion, and we got somewhere.
