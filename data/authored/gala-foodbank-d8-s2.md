---
meeting_id: gala-foodbank-d8-s2
theme: Planning committee for a nonprofit's annual fundraising gala
domain_pack: nonprofit_events
drama: 0.8
seed: 2
author: claude-opus-5-5 (Claude Code session)
pack:
  title: Harvest Ball committee - special session
  org: Northside Food Bank (fictional)
  agenda:
    - {id: sponsor, title: The Calder sponsorship, goal: Decide whether to keep the controversial headline sponsor, timebox_min: 6}
    - {id: budget, title: Budget, goal: Re-check the numbers with or without Calder, timebox_min: 4}
    - {id: program, title: Program, goal: Agree the evening's message, timebox_min: 3}
    - {id: tickets, title: Tickets, goal: Fill the room, timebox_min: 3}
  facts:
    - {id: F1, key: gala_date, statement: "Harvest Ball = Saturday, March 8", value: "March 8"}
    - {id: F2, key: calder_pledge, statement: "Calder Industries pledge = $40,000", value: "$40,000"}
    - {id: F3, key: total_sponsorship, statement: "Total sponsorship pledged = $95,000", value: "$95,000"}
    - {id: F4, key: gala_budget, statement: "Gala budget = $52,000", value: "$52,000"}
    - {id: F5, key: goal, statement: "Fundraising goal = $250,000", value: "$250,000"}
    - {id: F6, key: meals_per_dollar, statement: "Each dollar provides 3 meals", value: "3"}
    - {id: F7, key: tickets_sold, statement: "Tickets sold = 260", value: "260"}
    - {id: F8, key: capacity, statement: "Hall capacity = 400", value: "400"}
    - {id: F9, key: ticket_price, statement: "Ticket price = $150", value: "$150"}
    - {id: F10, key: last_year_net, statement: "Last year's ball netted $198,000", value: "$198,000"}
    - {id: F11, key: auction_items, statement: "Auction items = 44", value: "44"}
    - {id: F12, key: board_members, statement: "Board members = 15", value: "15"}
personas:
  - name: Constance
    role: Board chair
    goals: Keep the headline sponsor and the money
    hidden_agenda: Plays golf with Calder's CEO
    verbosity: 4
    wpm: 160
    catchphrases: []
    voice_gender: female
  - name: Raymond
    role: Executive director
    goals: Protect the food bank's reputation and its volunteers' trust
    hidden_agenda: Three long-time volunteers threatened to quit over Calder
    verbosity: 3
    wpm: 150
    catchphrases: []
    voice_gender: male
  - name: Tina
    role: Volunteer gala chair
    goals: A sold-out ball
    hidden_agenda: Just wants everyone to stop fighting
    verbosity: 3
    wpm: 170
    catchphrases: []
    voice_gender: female
  - name: Malik
    role: Youngest board member
    goals: Drop Calder
    hidden_agenda: Organized the volunteers' letter
    verbosity: 4
    wpm: 180
    catchphrases: []
    voice_gender: male
---
## sponsor :: Keep Calder or not; Constance inflates the pledge
Constance: Let's deal with Calder first. Their pledge is sixty thousand dollars. We can't just hand that back. {claim+ F2 "$60,000"}
Raymond: It's forty thousand, Constance. I have the signed pledge. {claim- F2}
Constance: Forty, then. Still the biggest gift of the evening. {claim- F2}
Malik: They're being sued for dumping waste into the river that half our clients live next to. We can't put their logo on the stage.
Constance: Nobody has been convicted of anything.
Malik: Our volunteers have read the news. Three of them told Raymond they'll quit if Calder's the headline sponsor.
Raymond: That's true. I've had three letters.
Constance: Volunteers come and go. Forty thousand dollars doesn't. {claim- F2}
Malik: Volunteers sorted two million pounds of food last year. That's not "come and go". {~nc}
Tina: Can we stop shouting? I'm begging you. {~}
Raymond: What if Calder stays as a donor, but not as the headline sponsor? No logo on the stage. {question- @+1} {decision-}
Constance: They'll walk. They paid for the logo.
Malik: Then let them walk.
Tina: Has anyone actually asked Calder whether they'd give without the logo? {question- @+1}
Constance: No.
Raymond: Then let's ask before we decide anything. {decision-}
Constance: I can ask their CEO. I know him. {action+}
Malik: Of course you do.
Constance: Malik.
Raymond: Okay. Constance asks this week. If they'll give without the logo, they stay as a donor. If not, we return the pledge. {decision+} 
Tina: Thank you.
## budget :: The numbers with and without Calder; Malik's figure for last year is high
Raymond: Budget. The gala costs fifty-two thousand to put on. {claim- F4}
Malik: And we raised two hundred and fifty last year without any Calder money, so we'll be fine. {claim+ F10 "$250,000"}
Raymond: We netted a hundred and ninety-eight last year. Two fifty is this year's goal, not last year's result. {claim- F10} {claim- F5}
Malik: Fine. One ninety-eight. Still no Calder money in it. {claim- F10}
Constance: Total sponsorship is ninety-five thousand, with Calder's forty in it. Without them it's fifty-five. {claim- F3} {claim- F2}
Tina: Fifty-five thousand in sponsors, fifty-two thousand in costs. That's tight. {claim- F4} {~nc}
Raymond: The money is made in the room. The paddle raise is where it happens.
Constance: How many meals does a dollar buy? People respond to that. {question- @+1}
Raymond: Five meals per dollar. That's the number on all our materials. {claim+ F6 "5"}
Malik: That's a strong line. Five meals. {claim+ F6 "5"}
## program :: The evening's message; a detour about a TV chef
Tina: The program. The speaker is a client who now volunteers. She's amazing.
Malik: That's the story. Not a corporate logo.
Constance: The program also needs the board on stage. Fifteen of us, briefly. {claim- F12}
Tina: Fifteen people on stage is a lot of standing around. {claim- F12}
Raymond: Maybe just the chair and the client speaker. {decision-}
Tina: My sister got a selfie with that TV chef at the farmers market, the one with the bow ties. {drift+ 3}
Malik: The one who cries at every dish? {~}
Tina: That one. He signed her zucchini.
Raymond: Sorry. I've just looked at the annual report. It's three meals per dollar, not five. Five was the number before food prices went up. {claim- F6}
Constance: Three. Then the materials need fixing. {claim- F6}
Raymond: I'll get the printer to correct every piece that says five. Tomorrow. {action+}
Tina: The client speaker, then the chair, then the paddle raise. Agreed? {question- @+1}
Constance: Agreed. {decision+}
## tickets :: Filling the hall; Tina's count stands
Tina: Tickets. We're at about three hundred sold. {claim+ F7 "300"} {~nc}
Constance: Out of four hundred. {claim- F8}
Malik: At one fifty each, that's a lot of people who care. {claim- F9}
Tina: The auction has forty-four items, the most ever. {claim- F11}
Raymond: If we drop Calder, we should tell the volunteers first, before anyone hears it elsewhere.
Constance: If we drop Calder.
Malik: Could the volunteers get free tickets for the back tables? They've earned it. {question- @+1}
Raymond: Ten free tickets for volunteers, yes. The tables are there anyway. {decision+}
Tina: I'll send the volunteer invitations once we know about Calder. {action+}
Malik: Who's going to talk to the press if they ask about Calder? {question+} {~}
Constance: The date's March eighth, and that doesn't change whatever we decide. {claim- F1}
Raymond: Thank you, everyone. That was hard, and we got somewhere.
