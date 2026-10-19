---
meeting_id: gala-landtrust-d2-s2
theme: Planning committee for a nonprofit's annual fundraising gala
domain_pack: nonprofit_events
drama: 0.2
seed: 2
author: claude-opus-5-5 (Claude Code session)
pack:
  title: Harvest dinner committee
  org: Greenway Land Trust (fictional)
  agenda:
    - {id: venue_menu, title: Venue and menu, goal: Confirm numbers for the hall and the caterer, timebox_min: 4}
    - {id: auction, title: Silent auction, goal: Review items and the bidding plan, timebox_min: 4}
    - {id: sponsors, title: Sponsors, goal: Check commitments against the goal, timebox_min: 3}
    - {id: volunteers, title: Volunteers, goal: Fill the remaining volunteer spots, timebox_min: 3}
  facts:
    - {id: F1, key: dinner_date, statement: "Harvest dinner = Saturday, October 4", value: "October 4"}
    - {id: F2, key: tickets_sold, statement: "Tickets sold = 112", value: "112"}
    - {id: F3, key: hall_capacity, statement: "Hall capacity = 180", value: "180"}
    - {id: F4, key: ticket_price, statement: "Ticket price = $125", value: "$125"}
    - {id: F5, key: goal, statement: "Fundraising goal = $60,000", value: "$60,000"}
    - {id: F6, key: auction_items, statement: "Auction items = 31", value: "31"}
    - {id: F7, key: sponsors, statement: "Sponsors = 5", value: "5"}
    - {id: F8, key: sponsor_total, statement: "Sponsorship total = $14,500", value: "$14,500"}
    - {id: F9, key: volunteers_needed, statement: "Volunteers needed = 20", value: "20"}
    - {id: F10, key: volunteers_signed, statement: "Volunteers signed up = 13", value: "13"}
    - {id: F11, key: menu_cost, statement: "Menu cost = $48 per head", value: "$48"}
    - {id: F12, key: last_year_raised, statement: "Last year's dinner raised $52,300", value: "$52,300"}
personas:
  - name: Beatrice
    role: Committee chair
    goals: A warm evening that beats last year
    hidden_agenda: Promised the board a record year
    verbosity: 3
    wpm: 145
    catchphrases: []
    voice_gender: female
  - name: Oren
    role: Development director
    goals: More auction revenue
    hidden_agenda: Counts promised items before they arrive
    verbosity: 3
    wpm: 160
    catchphrases: []
    voice_gender: male
  - name: Fumiko
    role: Volunteer logistics lead
    goals: Enough hands on the night
    hidden_agenda: Recruits the same retirees every year and worries about burning them out
    verbosity: 2
    wpm: 150
    catchphrases: []
    voice_gender: female
  - name: Desmond
    role: Treasurer
    goals: Keep costs predictable
    hidden_agenda: Local history buff
    verbosity: 2
    wpm: 135
    catchphrases: []
    voice_gender: male
---
## venue_menu :: Numbers for the hall and caterer
Beatrice: Good evening. Let's start with the hall and the menu. Oren, how are tickets? {question- @+1}
Oren: A hundred and twelve sold, at a hundred and twenty-five each. {claim- F2} {claim- F4}
Beatrice: And the hall holds a hundred and eighty, so there's room. {claim- F3}
Desmond: The menu is forty-eight a head. The caterer needs a final number two weeks out. {claim- F11}
Fumiko: Do we order for the tickets sold, or for the hall? {question- @+1}
Desmond: For the tickets sold, plus ten percent. That's what we did last year. {~}
Oren: The hall used to be a cannery, you know. My grandfather worked the line there in the fifties. {drift- 2}
Beatrice: I didn't know that. How lovely.
Fumiko: Is there a vegetarian option this year? Several people asked. {question- @+1}
Desmond: The squash risotto. The caterer says it's popular.
Beatrice: Then we'll order on tickets sold plus ten percent, with the risotto as the vegetarian main. {decision+} {~} 
Fumiko: Good.
## auction :: Items and bidding; Oren counts items that haven't arrived
Beatrice: The auction. Oren? {question- @+1}
Oren: We're at about forty items. Some lovely ones, too. {claim+ F6 "40"}
Fumiko: I have the intake sheet here. It's thirty-one that have actually arrived. {claim- F6}
Oren: Thirty-one in hand, and about nine more promised. Fair point. {claim- F6}
Desmond: What's the best item so far? {question- @+1}
Oren: The guided canoe trip on the reserve. And the hand-made quilt from the Hendersons.
Beatrice: Should we put the quilt in a live auction instead of the silent one? {question- @+1} {decision-}
Oren: It might do better live. One live item is a nice moment in the evening.
Desmond: Who'd run the live part? We don't have an auctioneer. {question- @+1}
Beatrice: I could do it. I've done it at the school before. {action+}
Oren: That would be perfect.
Fumiko: It might help if someone chased the nine promised items this week. {action-}
Oren: I'll call the nine donors on Monday and confirm drop-off dates. {action+}
## sponsors :: Commitments and the goal; Beatrice's memory of last year goes unchecked
Beatrice: Sponsors. Desmond? {question- @+1}
Desmond: Five sponsors, fourteen thousand five hundred in total. {claim- F7} {claim- F8}
Oren: The goal for the evening is sixty thousand. {claim- F5}
Beatrice: Last year we raised fifty-eight thousand, so sixty is within reach. {claim+ F12 "$58,000"} {claim- F5}
Fumiko: My neighbor just put solar panels on her whole roof. She says her bill is nearly zero. {drift+ 2}
Desmond: My brother-in-law is thinking about it. The installers are booked for months.
Oren: Could we ask the solar company to sponsor? It fits what we do. {question- @+1}
Beatrice: That's a good thought. Let's think about it for next year, since the program is printed already. {decision-}
Desmond: Has anyone heard back from the bank about renewing their sponsorship? {question+} {~}
Oren: The brewery wants to donate the beer instead of cash. Is that okay? {question- @+1}
Desmond: That's fine. In-kind counts, I just record it differently. {decision+}
## volunteers :: Filling the gaps
Beatrice: Volunteers. Fumiko? {question- @+1}
Fumiko: We need twenty and we have thirteen. {claim- F9} {claim- F10}
Oren: Seven short. Where are the gaps? {question- @+1}
Fumiko: Setup in the afternoon, and cleanup at the end. Nobody wants cleanup.
Desmond: I'll do cleanup. I'm always last to leave anyway. {action+}
Beatrice: Could we ask the high school's environmental club? They need service hours. {question- @+1}
Fumiko: That's a good idea. I'll email their teacher tomorrow. {action+} 
Beatrice: Then Desmond has cleanup, and we ask the club to cover setup. {decision+}
Oren: And the date's still October fourth for everyone, right? A sponsor asked me. {question- @+1} {claim- F1}
Beatrice: October fourth. Nothing's changed. Thank you, everyone. A lovely meeting. {claim- F1}
