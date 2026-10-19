---
meeting_id: gala-lantern-d5-s2
theme: Planning committee for a nonprofit's annual fundraising gala
domain_pack: nonprofit_events
drama: 0.5
seed: 2
author: claude-opus-5-5 (Claude Code session)
pack:
  title: Lantern Gala committee
  org: Lantern House Women's Shelter (fictional)
  agenda:
    - {id: money, title: Budget and goal, goal: Check the budget against the fundraising goal, timebox_min: 4}
    - {id: program, title: Speakers and program, goal: Settle the keynote and the survivor speaker, timebox_min: 5}
    - {id: tables, title: Tables and sponsors, goal: Sell the remaining tables, timebox_min: 4}
    - {id: logistics, title: Logistics, goal: Volunteers and the evening's details, timebox_min: 3}
  facts:
    - {id: F1, key: gala_date, statement: "Gala = Saturday, November 15", value: "November 15"}
    - {id: F2, key: budget, statement: "Gala budget = $38,000", value: "$38,000"}
    - {id: F3, key: goal, statement: "Fundraising goal = $200,000", value: "$200,000"}
    - {id: F4, key: last_year_raised, statement: "Last year's gala raised $164,000", value: "$164,000"}
    - {id: F5, key: tickets_sold, statement: "Individual tickets sold = 210", value: "210"}
    - {id: F6, key: capacity, statement: "Ballroom capacity = 320", value: "320"}
    - {id: F7, key: table_price, statement: "Corporate table = $3,000", value: "$3,000"}
    - {id: F8, key: tables_sold, statement: "Corporate tables sold = 9", value: "9"}
    - {id: F9, key: keynote_fee, statement: "Keynote speaker fee = $7,500", value: "$7,500"}
    - {id: F10, key: matching_pledge, statement: "Matching gift pledge = $25,000", value: "$25,000"}
    - {id: F11, key: bed_cost, statement: "Each $10,000 funds one shelter bed for a year", value: "$10,000"}
    - {id: F12, key: volunteers, statement: "Volunteers signed up = 35", value: "35"}
personas:
  - name: Yvonne
    role: Executive director
    goals: Fund four more beds this year
    hidden_agenda: The shelter turned away eleven women last month
    verbosity: 3
    wpm: 155
    catchphrases: []
    voice_gender: female
  - name: Graham
    role: Board treasurer
    goals: A gala that costs a lot less than it raises
    hidden_agenda: Thinks the keynote is overpriced
    verbosity: 2
    wpm: 140
    catchphrases: []
    voice_gender: male
  - name: Pilar
    role: Volunteer gala chair
    goals: An evening that moves people to give
    hidden_agenda: Booked the keynote speaker before checking the fee with the board
    verbosity: 4
    wpm: 170
    catchphrases: []
    voice_gender: female
  - name: Jerome
    role: Corporate relations
    goals: Sell every table
    hidden_agenda: Two companies said maybe and he counted them
    verbosity: 3
    wpm: 165
    catchphrases: []
    voice_gender: male
---
## money :: Budget, goal and last year; Yvonne's memory of last year is high, corrected later
Yvonne: Thank you for coming. This gala matters more than usual this year. We turned women away last month.
Graham: The budget for the evening is thirty-eight thousand. The goal is two hundred thousand. {claim- F2} {claim- F3}
Yvonne: Last year we raised a hundred and eighty, so two hundred is a stretch but not a fantasy. {claim+ F4 "$180,000"} {claim- F3}
Pilar: And this year we have the matching pledge. Twenty-five thousand, if we raise it first. {claim- F10}
Jerome: The matching pledge is a great story for the paddle raise. Every dollar doubled.
Yvonne: What does a bed cost us, for the paddle raise? People like to know what their money does. {question- @+1}
Graham: Ten thousand funds one bed for a year. {claim- F11}
Pilar: So the paddle raise could literally be "fund a bed". That's powerful.
Yvonne: That's exactly what I want. Four beds is the dream.
Graham: Sorry, a small thing. Last year's total, was it a hundred and eighty? My notes have a hundred and sixty-four. {question- @+1} {claim- F4}
Yvonne: Oh. You're probably right. A hundred and eighty was the pledges, before a few fell through. {claim- F4}
Graham: A hundred and sixty-four, then. So two hundred is a bigger jump than it sounded. {claim- F4} {claim- F3}
## program :: The keynote and the survivor speaker; Pilar's fee figure stands
Pilar: The program. I've booked Dana Whitlock as the keynote. She's wonderful, and the fee is five thousand. {claim+ F9 "$5,000"}
Graham: That's a lot for a speech, in my opinion.
Pilar: She brings people. Last time she spoke at a gala, they raised a fortune.
Yvonne: The survivor speaker matters more to me than the keynote. Who is it this year? {question- @+1}
Pilar: Rosa, from our transitional housing. She asked to do it. She's been practicing.
Yvonne: Rosa. That's brave of her. We need to make sure she's supported that night.
Jerome: Could she speak before dinner instead of after? People are more focused before the wine. {question- @+1} {decision-}
Pilar: She wanted to speak right before the paddle raise. That's when it matters most.
Yvonne: Then Rosa speaks right before the paddle raise, and the keynote opens the evening. {decision+}
Pilar: I'll tell Rosa tomorrow and schedule a rehearsal with her at the hotel. {action+}
Graham: Has Dana's contract been signed by the board? {question- @+1}
Pilar: Not yet. I signed the letter of intent myself.
Graham: That's not how it works, Pilar.
Pilar: I know. It was going to go to someone else. I'm sorry.
Yvonne: Let's get the contract to the board this week and do it properly. {decision-}
## tables :: Corporate tables; Jerome's count is high; an off-topic stretch about a new restaurant
Jerome: Tables. We've sold twelve corporate tables, at three thousand each. {claim+ F8 "12"} {claim- F7}
Graham: Twelve? I only have nine invoices, I think. Maybe I'm missing some? {question- @+1} {claim- F8}
Jerome: No, you're right. Nine paid. Three said yes on the phone but haven't signed. {claim- F8} {~nc}
Yvonne: Then nine, until they sign. {claim- F8}
Jerome: I'll chase the three this week. One of them is the bank, and they always come through. {action+} {~nc}
Pilar: Individual tickets are at two hundred and ten. The ballroom holds three twenty. {claim- F5} {claim- F6}
Graham: So plenty of room for the last tables.
Jerome: Has anyone been to that new Lebanese place on Fifth? I took the bank people there and they loved it. {drift+ 3} {~}
Pilar: The one with the garden? I want to go. I hear the bread is incredible. {~}
Graham: My wife's been twice already. She says the lamb is the best in the city.
Yvonne: We should eat there to celebrate when this is over. Back to tables, though.
Jerome: Could the board members each bring a table of friends? That's how other galas fill up. {question- @+1}
Graham: Some can. Some of us are the friends.
Yvonne: Let's ask every board member to host a table or buy two tickets. Not a requirement. An ask. {decision+}
## logistics :: Volunteers and the night
Pilar: Logistics. We have thirty-five volunteers so far. {claim- F12}
Yvonne: Is that enough? Last year felt thin at check-in. {question- @+1}
Pilar: For check-in, yes. For the auction tables, we need about five more.
Graham: The high school's service club helped another charity last month. They were very good. 
Jerome: Someone ought to read the hotel's cancellation terms too, just in case. {action-}
Pilar: I'll call their advisor on Monday. {action+}
Jerome: The date's November fifteenth for everything, including the hotel contract? {question- @+1} {claim- F1}
Pilar: The fifteenth. The hotel, the caterer and Dana are all booked for that night. {claim- F1}
Yvonne: Who's taking care of Rosa on the night, so she isn't alone before she speaks? {question+} {~}
Graham: I'll have a budget update for the next meeting, with the keynote fee in it. {action+}
Yvonne: Thank you. We'll fund those beds.
