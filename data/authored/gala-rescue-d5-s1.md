---
meeting_id: gala-rescue-d5-s1
theme: Planning committee for a nonprofit's annual fundraising gala
domain_pack: nonprofit_events
drama: 0.5
seed: 1
author: claude-opus-5-5 (Claude Code session)
pack:
  title: Paws and Lights gala - planning committee
  org: Harbor Lights Animal Rescue (fictional)
  agenda:
    - {id: budget, title: Gala budget, goal: See what's spent and what's left, timebox_min: 4}
    - {id: program, title: Venue and program, goal: Settle the run of the evening, timebox_min: 4}
    - {id: sponsors, title: Sponsorship pipeline, goal: Confirm sponsors and chase the rest, timebox_min: 4}
    - {id: promotion, title: Ticket promotion, goal: Agree how to sell the remaining tickets, timebox_min: 3}
  facts:
    - {id: F1, key: gala_date, statement: "Gala date = Saturday, November 8", value: "November 8"}
    - {id: F2, key: ticket_price, statement: "Ticket price = $95", value: "$95"}
    - {id: F3, key: tickets_sold, statement: "Tickets sold = 140", value: "140"}
    - {id: F4, key: venue_capacity, statement: "Venue capacity = 250", value: "250"}
    - {id: F5, key: gala_budget, statement: "Gala budget = $28,000", value: "$28,000"}
    - {id: F6, key: spent_to_date, statement: "Spent to date = $11,300", value: "$11,300"}
    - {id: F7, key: fundraising_goal, statement: "Fundraising goal for the night = $75,000", value: "$75,000"}
    - {id: F8, key: sponsors_confirmed, statement: "Sponsors confirmed = 6", value: "6"}
    - {id: F9, key: sponsor_revenue, statement: "Confirmed sponsor revenue = $21,000", value: "$21,000"}
    - {id: F10, key: video_length, statement: "Adoption stories video = 4 minutes", value: "4 minutes"}
    - {id: F11, key: email_list, statement: "Email list = 9,400 subscribers", value: "9,400"}
    - {id: F12, key: last_year_attendance, statement: "Last year's attendance = 205", value: "205"}
personas:
  - name: Tamsin
    role: Volunteer event chair
    goals: A gala that feels warm, not corporate
    hidden_agenda: Wants to bring an adoptable dog on stage, which the venue may not allow
    verbosity: 4
    wpm: 165
    catchphrases: ["oh, I love that", "okay, so"]
    voice_gender: female
  - name: Ray
    role: Executive director
    goals: Hit the fundraising goal
    hidden_agenda: The rescue's kennel lease is up for renewal and costs are rising
    verbosity: 3
    wpm: 150
    catchphrases: ["the way I see it", "right"]
    voice_gender: male
  - name: Lucia
    role: Sponsorship volunteer
    goals: Land a headline sponsor
    hidden_agenda: Counting sponsors that haven't signed yet
    verbosity: 3
    wpm: 170
    catchphrases: ["super promising", "honestly"]
    voice_gender: female
  - name: Noah
    role: Volunteer treasurer
    goals: Keep spending inside the budget
    hidden_agenda: Hasn't entered last month's receipts yet
    verbosity: 2
    wpm: 145
    catchphrases: ["um", "let me double-check"]
    voice_gender: male
---
## budget :: What's spent; Noah's number is low and Ray catches it later
Tamsin: Okay, so, budget first so we know what we're working with. Noah? {question- @+1}
Noah: Um, the total budget is twenty-eight thousand, and we've spent about eight so far. {claim- F5} {claim+ F6 "$8,000"}
Ray: Eight. Right. That's less than I expected. {claim+ F6 "$8,000"}
Tamsin: Oh, I love that. So we have room for the photo booth? {question- @+1}
Noah: Let me double-check, but probably, yes.
Lucia: Honestly, a photo booth with the rescue dogs would be super promising for social.
Ray: The way I see it, every dollar we don't spend on the night goes to the dogs.
Tamsin: But people give more when they're having fun. That's the whole point of a gala.
Ray: Right. I'm not against fun. I'm against a fifteen-hundred-dollar booth. {~}
Noah: Um, the booth quote was nine hundred. {~}
Ray: Nine hundred I can live with. {~}
Tamsin: So, photo booth, yes? {question- @+1}
Ray: Let's wait and see what the sponsors cover first. {decision-}
Lucia: The pet food company might sponsor the booth, actually.
Ray: Noah, did the October invoices go in? The caterer and the printer? {question- @+1}
Noah: Um. Not yet. I have them, I just haven't entered them.
Ray: Then I don't think we've spent eight. With those it's over eleven. {claim- F6}
Noah: Let me double-check. Yes. Eleven thousand three hundred, with the October invoices. {claim- F6}
Ray: Right. So we have less room than we thought.
Noah: I'll enter all the October receipts tonight and send the updated sheet. {action+}
## program :: The run of the evening; the dog-on-stage question; an unsignposted detour about a bake-off
Tamsin: Okay, so, the program. Doors at six, dinner at seven, the video, then the paddle raise.
Ray: How long is the video? {question- @+1}
Tamsin: Four minutes. The adoption stories. I cried three times editing it. {claim- F10}
Lucia: Four minutes is perfect. Any longer and people check their phones. {claim- F10}
Tamsin: And I had an idea. What if we brought Juniper on stage during the paddle raise? {question- @+1}
Noah: The venue has a no-animals rule, I think. It's in the contract somewhere.
Tamsin: Could we ask the venue for an exception, just for him? {question+}
Lucia: Totally unrelated, but the bake-off the bake-off at the farmers market on Sunday? {drift+ 4} {~}
Ray: My wife entered. She came second with a lemon tart.
Tamsin: Second! The judge was clearly bribed.
Lucia: The winner was the guy who runs the bakery. That's basically cheating.
Noah: So, um, for the paddle raise, who's the auctioneer? {question- @+1}
Ray: I asked Councilwoman Reyes. She said probably.
Tamsin: Probably is not a yes.
Ray: Right. I'll call her office tomorrow and get a firm yes or no. {action+}
Lucia: It'd be good to have a backup auctioneer, honestly. {action-}
Tamsin: Doors at six, dinner at seven, the video, then the paddle raise with Reyes or a backup. That's the run of show. {decision+}
## sponsors :: Lucia counts unsigned sponsors; Ray pushes back
Ray: Sponsors. Lucia, how's the pipeline? {question- @+1}
Lucia: Super promising. We have ten sponsors confirmed. {claim+ F8 "10"}
Ray: Ten? I have six signed agreements. {claim- F8} {~}
Lucia: Six signed, four who said yes on calls. Honestly, the calls count. {claim- F8}
Ray: The way I see it, a sponsor counts when the check clears.
Noah: Um, the six signed come to twenty-one thousand. {claim- F9} {claim- F8}
Ray: Twenty-one thousand toward a seventy-five thousand goal. {claim- F9} {claim- F7}
Tamsin: Who are the four verbal ones? {question- @+1}
Lucia: The vet clinic, the pet food company, the bank on Main and the brewery.
Noah: Is that vacuum coming through? My roommate has impeccable timing. {drift- 2} {~}
Tamsin: A little. It's fine.
Ray: Could we get paperwork from those four before the gala? {question- @+1}
Lucia: I'll send agreements to all four verbal sponsors by Friday. {action+}
Tamsin: Oh, I love that. And the headline sponsor? We still don't have one. {question- @+1}
Lucia: The bank might go headline. They asked what it would cost.
Ray: What would it cost? {question- @+1}
Tamsin: Last year the headline was five thousand, I think. {~}
Ray: Then we ask for seventy-five hundred this year. Costs are up. {decision-} {~}
Lucia: Honestly, I'd ask for ten and let them talk us down.
Ray: Fine. We ask the bank for ten thousand as headline sponsor and settle no lower than seventy-five hundred. {decision+} {~}
## promotion :: Selling the rest; the attendance number nobody checks
Tamsin: Okay, so, selling tickets. We're at a hundred and forty. {claim- F3}
Ray: Out of two fifty capacity. {claim- F4}
Tamsin: Last year we had three hundred people, so we can definitely fill it. {claim+ F12 "300"}
Lucia: Honestly, we just need to email the list more.
Noah: How big is the email list now? {question- @+1}
Lucia: About ninety-four hundred. {claim- F11}
Ray: Right. And tickets are ninety-five, which is fair for dinner and a cause. {claim- F2}
Tamsin: What if we did a "bring a friend" discount? {question- @+1}
Ray: I'd rather not discount. Maybe a free drink voucher instead. {decision-}
Lucia: Someone should ask the brewery about donating drink vouchers. {action-}
Noah: Um, is the date on all the flyers right? I saw one that said the ninth. {question- @+1}
Tamsin: Oh no. It's the eighth. November eighth. {claim- F1}
Noah: Let me double-check which flyer it was.
Tamsin: I'll get the printer to reprint any flyer with the wrong date. Today. {action+}
Ray: Good. The way I see it, we're in decent shape, as long as the sponsors sign.
Lucia: Has anyone told the kennel staff they're invited? {question+} {~}
Tamsin: Okay, so, I think that's everything. Thank you, all. For the dogs!
Ray: For the dogs.
