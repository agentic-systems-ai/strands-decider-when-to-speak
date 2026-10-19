---
meeting_id: gala-nonprofit-d2-s1
theme: Planning committee for a nonprofit's annual fundraising gala
domain_pack: nonprofit_events
drama: 0.2
seed: 1
author: claude-opus-5-5 (Claude Code session)
pack:
  title: Spring gala committee - monthly meeting
  org: Riverbend Literacy Project (fictional)
  agenda:
    - {id: tickets_venue, title: Tickets and venue, goal: Check ticket sales against the venue and catering numbers, timebox_min: 4}
    - {id: sponsorships, title: Sponsorships, goal: Review sponsorship commitments and who to chase, timebox_min: 4}
    - {id: auction, title: Silent auction, goal: Confirm auction items and how bidding will work, timebox_min: 4}
    - {id: volunteers, title: Volunteers and run of show, goal: Staff the evening and agree the program, timebox_min: 4}
  facts:
    - {id: F1, key: gala_date, statement: "Gala date = Saturday, March 14", value: "March 14"}
    - {id: F2, key: venue_capacity, statement: "Venue capacity = 220 guests", value: "220"}
    - {id: F3, key: tickets_sold, statement: "Tickets sold so far = 96", value: "96"}
    - {id: F4, key: ticket_price, statement: "Individual ticket price = $150", value: "$150"}
    - {id: F5, key: fundraising_goal, statement: "Gala fundraising goal = $120,000", value: "$120,000"}
    - {id: F6, key: sponsorship_committed, statement: "Sponsorship committed so far = $38,500", value: "$38,500"}
    - {id: F7, key: last_year_net, statement: "Last year's gala netted $91,000", value: "$91,000"}
    - {id: F8, key: auction_items_secured, statement: "Silent auction items secured = 23", value: "23"}
    - {id: F9, key: volunteers_signed_up, statement: "Volunteers signed up = 31", value: "31"}
    - {id: F10, key: venue_balance_due, statement: "Venue balance due = January 10", value: "January 10"}
    - {id: F11, key: catering_minimum, statement: "Catering minimum = 180 guests", value: "180"}
    - {id: F12, key: table_sponsor_price, statement: "Table sponsorship price = $2,500", value: "$2,500"}
personas:
  - name: Grace
    role: Board chair, runs the committee
    goals: Beat last year without burning out the volunteers
    hidden_agenda: Considering stepping down after this gala
    verbosity: 3
    wpm: 150
    catchphrases: ["wonderful", "let's keep going"]
    voice_gender: female
  - name: Owen
    role: Development director (staff)
    goals: Land two more corporate sponsors
    hidden_agenda: His annual review depends on the gala number
    verbosity: 4
    wpm: 165
    catchphrases: ["in terms of", "honestly"]
    voice_gender: male
  - name: Priya
    role: Volunteer coordinator
    goals: Enough hands on the night
    hidden_agenda: Half her volunteers are the same tired people every year
    verbosity: 3
    wpm: 160
    catchphrases: ["just to flag"]
    voice_gender: female
  - name: Walter
    role: Treasurer, retired accountant
    goals: Nobody spends money that isn't there
    hidden_agenda: Remembers every gala since the nineties and will tell you
    verbosity: 3
    wpm: 130
    catchphrases: ["if I may", "for the minutes"]
    voice_gender: male
---
## tickets_venue :: Sales against the catering minimum; a quiet worry about the gap
Grace: Wonderful, I think we're all here. Let's start with tickets and the venue.
Owen: In terms of tickets, we're at ninety-six sold as of this morning. {claim- F3}
Walter: If I may, the catering minimum is a hundred and eighty, so we're a fair way short. {claim- F11}
Grace: How worried should we be about that? {question- @+1}
Owen: Honestly, not very yet. Most of the sales come in the last six weeks. {~}
Walter: That has been true most years. Not every year.
Priya: Just to flag, the early-bird price ended last week, so there might be a slowdown now.
Grace: What are tickets now, after early-bird? {question- @+1}
Owen: A hundred and fifty each. Tables are separate. {claim- F4}
Walter: And the balance on the venue is due January tenth, for the minutes. {claim- F10}
Grace: Do we have that money set aside already? {question- @+1}
Walter: We do. It is sitting in the event account, untouched, as it should be.
Grace: Wonderful.
Priya: Is the venue still okay with a big crowd on the dance floor at once? Last time it got tight. {question+} {~}
Owen: It's two twenty capacity overall, so the room itself is fine. {claim- F2}
Priya: It's the dance floor I'm worried about, not the room.
Grace: That's a run-of-show question. Let's hold it for the end.
Owen: It'd be worth someone walking the space again before we finalize the layout. {action-}
Walter: The last time we did a walk-through, in ninety-eight, the caterer brought a tape measure and a flask. {drift+ 3}
Grace: Walter, you've told us about the flask.
Walter: The flask is an important part of the story. The tape measure was wrong, the flask was not.
Owen: Okay, in terms of the sales push, I'd like to send a reminder email to last year's attendees. {action-}
Grace: When would that go out? {question- @+1}
Owen: I'll send the reminder email to last year's attendees on Monday. {action+}
## sponsorships :: Committed vs hoped-for; Owen rounds up, Walter rounds him back down
Grace: Sponsorships. Owen, where are we? {question- @+1}
Owen: Honestly, really well. We're at about forty-five thousand committed. {claim+ F6 "$45,000"}
Walter: If I may, I have thirty-eight five in signed letters. {claim- F6}
Owen: The rest is verbal. The hardware store and the credit union both said yes on the phone.
Walter: For the minutes, verbal is not committed.
Owen: Fair. Thirty-eight five signed, with two verbals. {claim- F6}
Grace: And the goal for the whole night is one twenty? {question- @+1} {claim- F5}
Walter: One hundred and twenty thousand, yes. Which is ambitious. {claim- F5}
Grace: Last year we cleared a hundred thousand, so it's a stretch but not crazy. {claim+ F7 "$100,000"}
Priya: Are we still offering tables at the same price as last year? {question- @+1}
Owen: Twenty-five hundred a table. We kept it flat. {claim- F12}
Walter: Flat is generous, with catering costs where they are.
Owen: Maybe we nudge it to three thousand for next year. {decision-} {~}
Grace: Next year is next year. For this year it stays where it is. {decision+}
Priya: Who are we still waiting on, sponsor-wise? {question- @+1}
Owen: The bank, the dental group and the brewery. The brewery is the most likely.
Grace: Could someone get a signed letter from the hardware store and the credit union this week? {question- @+1}
Owen: I'll get both verbals turned into signed letters by Friday. {action+}
Walter: Thank you. I'll sleep better. {~}
Priya: Has anyone asked the mayor's office about doing a proclamation, like the library did? {question+}
Owen: The brewery, by the way, wants their logo on the cocktail napkins. Is that fine? {question- @+1}
Grace: That's fine. Logos on napkins are fine. {decision+}
Walter: As long as they pay for the napkins.
## auction :: Items and bidding; the online bidding decision
Grace: The silent auction. Priya, you've been collecting items.
Priya: We have twenty-three items secured. A few more are promised. {claim- F8}
Walter: Twenty-three is more than last year at this point, I believe. {claim- F8}
Grace: What's the best item so far? {question- @+1}
Priya: The weekend at the lake cabin. People will fight over it.
Owen: Sorry, my dog is losing it at the mail carrier, give me a second. {drift- 2}
Grace: Hello, Biscuit.
Owen: There's a question about whether we do mobile bidding this year, on phones.
Walter: Mobile bidding costs money. The platform takes a cut.
Priya: But people bid more on phones, honestly. They get the notifications and they get competitive.
Grace: Do we know what the cut is? {question- @+1}
Owen: Five percent of the winning bids, plus a setup fee. {~}
Walter: Five percent of a good auction is real money. {~}
Priya: And paper bid sheets mean someone has to sit there all night watching the clipboards.
Grace: Maybe we try mobile bidding for the big items only? {decision-} {question- @+1}
Owen: That's actually what most groups do now.
Walter: I could live with that.
Grace: Then we'll do mobile bidding for the top ten items and paper for the rest. That's what we'll do. {decision+}
Priya: Lovely. I'll set up the top ten on the platform this weekend. {action+}
Walter: Just the top ten, Priya.
Priya: Just the top ten, promise. {action+}
Owen: Someone should probably double-check the cabin's insurance covers a stranger staying there. {action-}
## volunteers :: Staffing the night; Priya's number is off and nobody notices; the dance floor comes back
Grace: Volunteers and the run of show. Priya? {question- @+1}
Priya: We have about forty volunteers signed up, which is a good start. {claim+ F9 "40"}
Grace: That's wonderful.
Owen: How many do we actually need on the night? {question- @+1}
Priya: Realistically, forty-five or fifty, with check-in, the auction tables and cleanup. {~}
Walter: Are they the same people as last year? {question- @+1}
Priya: Mostly. Just to flag, a lot of them told me this would be their last one.
Grace: We should think about how to recruit younger volunteers next year. {decision-}
Owen: The high school needs service hours. That's usually a good pool.
Priya: Owen, could you reach out to the high school counselor about service hours? {action-} {question- @+1}
Owen: Honestly, I'm stretched thin until the sponsorships are done. {~}
Priya: Okay, then I'll email the high school counselor myself tomorrow. {action+}
Grace: Thank you, Priya. And the program for the evening? {question- @+1}
Walter: Speeches should be short. For the minutes, last year's speeches ran forty minutes. {~}
Grace: That was my fault. I'll own that. {~}
Owen: What if we cap speeches at fifteen minutes total, and the rest is the video? {question- @+2}
Priya: People love the video. The kids reading always gets them.
Grace: Then we cap the speeches at fifteen minutes and lead with the video. Agreed. {decision+}
Priya: And the dance floor? You said we'd come back to it. {question+}
Grace: We did. Is it the space or the number of people? {question- @+1}
Priya: The space. If we put the auction tables along the wall instead of the middle, it frees up the floor.
Walter: That seems sensible, and it costs nothing.
Grace: Let's look at the floor plan before we decide. {decision-}
Walter: Who is handling the raffle license this year? {question+} {~}
Owen: Is the date still Saturday the fourteenth? I keep getting asked. {question- @+1} {claim- F1}
Grace: March fourteenth, yes. Nothing has moved. And I think that's everything. Thank you all. {claim- F1}
Walter: For the minutes, meeting adjourned.
