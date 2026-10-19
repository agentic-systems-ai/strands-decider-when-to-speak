---
meeting_id: garden-eastgate-d8-s2
theme: "Community garden committee: plots, water and the spring fair"
domain_pack: community_group
drama: 0.8
seed: 2
author: claude-opus-5-5 (Claude Code session)
pack:
  title: Allotment association - emergency meeting
  org: Eastgate Allotments Association (fictional)
  agenda:
    - {id: lease, title: The lease, goal: Respond to the city's lease proposal, timebox_min: 6}
    - {id: campaign, title: The campaign, goal: Plan the petition and the council meeting, timebox_min: 4}
    - {id: money, title: Money, goal: What we can afford, timebox_min: 3}
    - {id: fair, title: Spring fair, goal: Decide whether the fair goes ahead, timebox_min: 3}
  facts:
    - {id: F1, key: lease_end, statement: "Current lease ends June 30", value: "June 30"}
    - {id: F2, key: rent_increase, statement: "City's proposed rent increase = 60%", value: "60%"}
    - {id: F3, key: current_rent, statement: "Current rent = $2,400 a year", value: "$2,400"}
    - {id: F4, key: plots, statement: "Plots = 58", value: "58"}
    - {id: F5, key: waitlist, statement: "Waitlist = 41", value: "41"}
    - {id: F6, key: petition_signatures, statement: "Petition signatures so far = 830", value: "830"}
    - {id: F7, key: council_meeting, statement: "City council meeting = April 9", value: "April 9"}
    - {id: F8, key: legal_consult, statement: "Legal consultation = $600", value: "$600"}
    - {id: F9, key: balance, statement: "Association balance = $6,200", value: "$6,200"}
    - {id: F10, key: water_bill, statement: "Last year's water bill = $1,900", value: "$1,900"}
    - {id: F11, key: fair_date, statement: "Spring fair = Saturday, May 24", value: "May 24"}
    - {id: F12, key: years_on_site, statement: "Years on the current site = 34", value: "34"}
personas:
  - name: Bernadette
    role: Chair
    goals: Keep the allotments
    hidden_agenda: Knows a councillor personally but doesn't want to look like she's using it
    verbosity: 3
    wpm: 155
    catchphrases: []
    voice_gender: female
  - name: Cyril
    role: Founding member
    goals: Fight the city with everything
    hidden_agenda: His late wife's roses are on plot 3
    verbosity: 4
    wpm: 140
    catchphrases: []
    voice_gender: male
  - name: Amara
    role: Young organizer, runs the petition
    goals: A loud public campaign
    hidden_agenda: Has already talked to a local reporter
    verbosity: 4
    wpm: 180
    catchphrases: []
    voice_gender: female
  - name: Felipe
    role: Treasurer
    goals: A plan that doesn't bankrupt the association
    hidden_agenda: Thinks the rent increase is actually survivable
    verbosity: 2
    wpm: 145
    catchphrases: []
    voice_gender: male
---
## lease :: The city's proposal; tempers; Felipe overstates the increase and is corrected later
Bernadette: Thank you for coming at short notice. The city wants a new lease from July, and the rent goes up.
Felipe: The rent's doubling. That's what the letter says. {claim+ F2 "doubling"}
Cyril: Doubling! After all these years. We've been on this site fifty years. {claim+ F12 "50"}
Amara: This is exactly what they do. Squeeze community spaces until they give up.
Bernadette: The current lease ends June thirtieth. We have until then to respond. {claim- F1}
Cyril: We respond by fighting them. Every one of us.
Felipe: Fighting costs money. A lawyer just to read the lease is six hundred. {claim- F8}
Amara: Six hundred is nothing compared to losing the allotments. {claim- F8}
Cyril: My wife planted those roses on plot three. I'm not handing them to a car park.
Bernadette: Nobody's handing anything to anybody, Cyril.
Amara: I've already talked to a reporter at the Gazette. She's interested.
Bernadette: Before we'd even met as a committee? {~}
Amara: Someone had to do something.
Felipe: I've got the letter here, sorry. It's not doubling. It's a sixty percent increase. I misread the table. {claim- F2}
Cyril: Sixty percent. That's still robbery. {claim- F2}
Felipe: The current rent is twenty-four hundred a year. Sixty percent more is about thirty-eight hundred. {claim- F3} {~nc}
Bernadette: Then we spend six hundred on the lawyer, and we make our case before we sign anything. {decision+} {claim- F8}
Felipe: I'll book the lawyer for next week. {action+}
## campaign :: Petition and council; Amara's count is high
Amara: The petition is at about two thousand signatures already. People really care. {claim+ F6 "2,000"}
Bernadette: Two thousand online, or on paper? {question- @+1} {~nc}
Amara: Well, about eight hundred and thirty verified. The rest are shares and likes. {claim- F6}
Felipe: Eight hundred and thirty real signatures is still impressive. {claim- F6}
Cyril: When is the council meeting? {question- @+1}
Bernadette: April ninth. Public comments are allowed. {claim- F7}
Amara: Then we fill the room. Fifty-eight plot holders, forty-one on the waitlist, their families. {claim- F4} {claim- F5}
Cyril: I'll speak. I've earned it. {action+}
Bernadette: Cyril, you'll speak from the heart, which is good. But someone needs to speak to the numbers too.
Felipe: I can do the numbers. Calmly. {action+}
Amara: And I'll organize who sits where, so it looks like a crowd and not a rabble. {action+}
Bernadette: Should I mention that I know Councillor Pryce? {question+} {~}
Cyril: The council parking lot is always full on meeting nights. Last time I parked three streets away and got a ticket. {drift+ 3}
Felipe: Did you appeal it? {~}
Cyril: Of course I appealed. I lost.
Amara: The campaign, everyone, please.
## money :: What we can afford
Felipe: Money. We have sixty-two hundred in the account. {claim- F9}
Cyril: Then we can afford to fight.
Felipe: We can afford a lawyer and the new rent for a year. Not a long legal battle.
Amara: Could we ask for donations alongside the petition? {question- @+1}
Felipe: We can, but we have to account for every penny.
Bernadette: Then a donation link goes on the petition, and Felipe keeps a separate record. {decision+}
Felipe: The water bill was nineteen hundred last year. That doesn't go away either. {claim- F10}
Amara: Maybe we propose a lower increase and offer to maintain the park strip next to us in return. {decision-}
Bernadette: Let's see what the lawyer says before we offer anything. {decision-}
## fair :: Does it go ahead
Amara: The fair. May twenty-fourth. Do we still hold it? {claim- F11} {question- @+1}
Cyril: Of course we hold it. Especially now.
Bernadette: It would show the city what the allotments are for.
Felipe: And bring in money. We'll need it.
Bernadette: The fair goes ahead, and we make it part of the campaign. {decision+}
Amara: I'll ask the reporter to come to the fair. That's a much better story than an angry meeting. {action+}
Cyril: It would be good if someone made a display of the history. Old photos. {action-}
Bernadette: Thank you, all of you. We're not giving up these plots.
