---
meeting_id: wedding-nakamura-d8-s2
theme: Family video call planning a cousin's wedding
domain_pack: family_planning
drama: 0.8
seed: 2
author: claude-opus-5-5 (Claude Code session)
pack:
  title: Mika and Owen's wedding - family call
  org: The Nakamura-Reyes family (fictional)
  agenda:
    - {id: roles, title: Ceremony roles, goal: Decide who walks Mika down the aisle and who speaks, timebox_min: 4}
    - {id: guests, title: Guest list, goal: Stay under the cap, timebox_min: 4}
    - {id: budget, title: Budget, goal: Confirm contributions and the big quotes, timebox_min: 4}
    - {id: logistics, title: Logistics, goal: Ceremony time, hotel and the rehearsal dinner, timebox_min: 3}
  facts:
    - {id: F1, key: wedding_date, statement: "Wedding date = Saturday, October 18", value: "October 18"}
    - {id: F2, key: guest_cap, statement: "Guest cap = 110", value: "110"}
    - {id: F3, key: rsvps_yes, statement: "RSVPs yes so far = 87", value: "87"}
    - {id: F4, key: budget_total, statement: "Total budget = $27,500", value: "$27,500"}
    - {id: F5, key: akiko_contribution, statement: "Akiko's contribution = $8,000", value: "$8,000"}
    - {id: F6, key: ernesto_contribution, statement: "Ernesto's contribution = $8,000", value: "$8,000"}
    - {id: F7, key: venue_balance_due, statement: "Venue balance due = August 1", value: "August 1"}
    - {id: F8, key: dj_quote, statement: "DJ quote = $1,650", value: "$1,650"}
    - {id: F9, key: rehearsal_guests, statement: "Rehearsal dinner guests = 24", value: "24"}
    - {id: F10, key: hotel_block, statement: "Hotel block = 15 rooms", value: "15"}
    - {id: F11, key: flower_quote, statement: "Flower quote = $2,900", value: "$2,900"}
    - {id: F12, key: ceremony_time, statement: "Ceremony starts at 4:30 pm", value: "4:30 pm"}
personas:
  - name: Mika
    role: The bride
    goals: Get both parents through the day without a scene
    hidden_agenda: Has already asked her stepfather to do a reading
    verbosity: 3
    wpm: 165
    catchphrases: []
    voice_gender: female
  - name: Akiko
    role: Mother of the bride
    goals: A traditional ceremony
    hidden_agenda: Doesn't want Ernesto's new wife at the head table
    verbosity: 4
    wpm: 160
    catchphrases: []
    voice_gender: female
  - name: Ernesto
    role: Father of the bride, remarried
    goals: Be included and pay his fair share
    hidden_agenda: Overpromised money he doesn't quite have
    verbosity: 3
    wpm: 150
    catchphrases: []
    voice_gender: male
  - name: Joel
    role: Cousin, the family's peacemaker and planner
    goals: Keep the call on track
    hidden_agenda: Has a job interview tomorrow and is distracted
    verbosity: 3
    wpm: 175
    catchphrases: []
    voice_gender: male
---
## roles :: Who walks Mika in; old tensions
Joel: Okay, everyone's on. Mika, do you want to start with the ceremony roles? {question- @+1}
Mika: Yes. I want both of you to walk me down the aisle. Mom and Dad. Together.
Akiko: Together. Next to him.
Ernesto: I can manage that if your mother can.
Akiko: I can manage anything for one aisle.
Joel: That's a yes from both of you, then? {question- @+1}
Ernesto: Yes.
Akiko: Yes. For Mika.
Mika: Thank you. Both of you. Then that's how we're doing it. {decision+}
Joel: And speeches? Who's giving one? {question- @+1}
Mika: Dad, and Owen's best man. And I asked Sandra to do a reading.
Akiko: You asked Sandra? Ernesto's wife? {~}
Mika: She's been in my life for eight years, Mom. {~}
Akiko: I gave birth to you. That's thirty-one years.
Joel: That reminds me of Aunt Rosie's wedding, the one with the bagpipes nobody asked for. {drift- 1}
Mika: Joel, not now. {~}
Ernesto: Akiko, Sandra will read and sit down. That's all.
Akiko: Then I'll do a reading too. {action+}
Mika: Okay. Mom reads, Sandra reads. Two readings. {decision+}
## guests :: The cap; Akiko's count is high; a tense tangent about the restaurant
Joel: Guest list. The cap is a hundred and ten. {claim- F2}
Akiko: And we already have about a hundred yeses, so we're nearly there. {claim+ F3 "100"}
Ernesto: Then where do my side go? {~}
Akiko: Your side is very large for someone who left.
Mika: Mom.
Joel: Can we look at the actual list before we fight about it? {~}
Ernesto: Sandra's restaurant could do the rehearsal dinner, you know. She's offered.
Akiko: I'm sure the food is very authentic.
Ernesto: It's very good, actually. It was in the paper last month.
Joel: I have the RSVP sheet open. It's eighty-seven yeses, not a hundred. {claim- F3}
Akiko: Eighty-seven. I was counting the maybes. {claim- F3}
Mika: So twenty-three spots left, roughly. {~}
Joel: How many does each side want to add? {question- @+1}
Ernesto: Eight from my side. Cousins in Monterrey.
Akiko: Then eight from mine. That's fair.
Mika: Sixteen more is fine. Eight each, and that's the list. {decision+} {~}
Joel: I'll update the sheet tonight with both sets of eight. {action+}
Akiko: Is the rehearsal dinner at Sandra's restaurant, then? {question- @+28}
## budget :: Contributions; Ernesto overstates his; the flower quote nobody checks
Joel: Budget. Total is twenty-seven five. {claim- F4}
Ernesto: I'm putting in ten thousand, like I said. {claim+ F6 "$10,000"}
Mika: Dad. We agreed on eight. Each of you, eight. {claim- F6} {claim- F5}
Ernesto: Eight. Right. Eight. I'd said ten at first, I know. {claim- F6} {~nc}
Akiko: Eight from me as well. Already transferred. {claim- F5} {~nc}
Joel: So sixteen from you both, and Mika and Owen cover the rest. 
Akiko: Has Owen's family said what they're putting in? {question+} {~}
Mika: The big quotes are the DJ and the flowers.
Joel: The DJ is sixteen fifty. The flowers came in at twenty-two hundred. {claim- F8} {claim+ F11 "$2,200"}
Akiko: Twenty-two hundred for flowers is reasonable, I suppose. {claim+ F11 "$2,200"}
Ernesto: Could we do fewer flowers and more food? {question- @+1} {decision-}
Mika: The flowers are already small. It's mostly greenery.
Joel: Somebody should probably ask the florist about a payment plan. {action-}
Mika: I'll call the florist on Friday about splitting the payment. {action+}
Akiko: When is the venue balance due? {question- @+1}
Joel: August first. {claim- F7}
Ernesto: August. That's soon. {claim- F7}
## logistics :: Time, hotel and the rehearsal dinner; a job interview detour
Joel: Logistics. The ceremony is at four, right? {claim+ F12 "4:00 pm"} {question- @+1}
Mika: Four thirty. The church moved us because of a baptism. {claim- F12}
Akiko: Four thirty. I'll tell the photographer. {action+} {claim- F12}
Joel: The hotel block is fifteen rooms. Is that enough for the Monterrey cousins? {claim- F10} {question- @+1}
Ernesto: Fifteen is plenty. Most of them will share. {claim- F10}
Joel: Sorry, I'm distracted, I have a job interview at nine tomorrow. {drift+ 2}
Mika: Joel! Where? {~}
Akiko: The rehearsal dinner. How many people? {question- @+1}
Mika: Twenty-four. Family and the wedding party. {claim- F9}
Ernesto: Sandra's restaurant seats thirty in the back room. {~}
Akiko: Fine. Sandra's restaurant. For the rehearsal dinner only. {decision+} {~}
Ernesto: Thank you, Akiko. Really.
Mika: Did anyone check the date's on the save-the-dates right? Owen's aunt thinks it's the nineteenth. {question- @+1}
Joel: It's the eighteenth, October eighteenth. I'll text Owen's aunt myself. {claim- F1} {action+}
Mika: Thank you, everyone. That went better than I thought.
Akiko: It did.
