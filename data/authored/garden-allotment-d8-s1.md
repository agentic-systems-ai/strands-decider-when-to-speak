---
meeting_id: garden-allotment-d8-s1
theme: "Community garden committee: plots, water and the spring fair"
domain_pack: community_group
drama: 0.8
seed: 1
author: claude-opus-5-5 (Claude Code session)
pack:
  title: Allotment society - committee meeting
  org: Fairview Allotment Society (fictional)
  agenda:
    - {id: complaint, title: The pesticide complaint, goal: Hear the complaint about plot 22 and decide what happens next, timebox_min: 5}
    - {id: water, title: Water use, goal: Understand why the water bill jumped and what to do, timebox_min: 4}
    - {id: fair, title: Spring fair, goal: Confirm the date and who runs what, timebox_min: 3}
    - {id: elections, title: Committee elections, goal: Agree how the election will run, timebox_min: 3}
  facts:
    - {id: F1, key: plot_holders, statement: "Plot holders = 48", value: "48"}
    - {id: F2, key: water_use_increase, statement: "Water use is up 35% on last year", value: "35%"}
    - {id: F3, key: water_bill, statement: "Last quarter's water bill = $2,240", value: "$2,240"}
    - {id: F4, key: warnings_issued, statement: "Rule-violation warnings issued this year = 3", value: "3"}
    - {id: F5, key: organic_rule_year, statement: "The organic-only rule was adopted in 2019", value: "2019"}
    - {id: F6, key: fair_date, statement: "Spring fair = Saturday, May 17", value: "May 17"}
    - {id: F7, key: fair_profit, statement: "Spring fair profit last year = $1,380", value: "$1,380"}
    - {id: F8, key: committee_seats, statement: "Committee seats up for election = 5", value: "5"}
    - {id: F9, key: candidates, statement: "Candidates standing = 7", value: "7"}
    - {id: F10, key: annual_dues, statement: "Annual dues = $60", value: "$60"}
    - {id: F11, key: hose_taps, statement: "Shared hose taps = 12", value: "12"}
    - {id: F12, key: insurance_renewal, statement: "Insurance renewal = $410", value: "$410"}
personas:
  - name: Doreen
    role: Chair
    goals: Get through the meeting without anyone storming out
    hidden_agenda: Not standing for re-election and hasn't said so
    verbosity: 3
    wpm: 150
    catchphrases: []
    voice_gender: female
  - name: Marco
    role: Plot holder on plot 22, the subject of the complaint
    goals: Clear his name
    hidden_agenda: Did use a slug pellet product, not knowing it wasn't organic
    verbosity: 4
    wpm: 175
    catchphrases: ["with respect"]
    voice_gender: male
  - name: Fatima
    role: Secretary
    goals: Keep the record straight
    hidden_agenda: Standing for chair
    verbosity: 2
    wpm: 155
    catchphrases: []
    voice_gender: female
  - name: Gus
    role: Founding member, forty years on the allotments
    goals: Keep things the way they were
    hidden_agenda: Has his own leaky hose he doesn't mention
    verbosity: 4
    wpm: 130
    catchphrases: ["back in my day"]
    voice_gender: male
---
## complaint :: Plot 22; tempers; Gus misdates the organic rule and nobody corrects him
Doreen: Right. The complaint. Three plot holders say plot twenty-two used chemical slug pellets. Marco, you're here, so you can respond. {~}
Marco: With respect, this is a witch hunt. I grow vegetables. That's it.
Gus: The organic rule's been in since twenty fifteen. Everyone knows it. {claim+ F5 "2015"}
Marco: I know the rule.
Fatima: The complaint says there were blue pellets around the brassicas. Blue pellets are metaldehyde.
Marco: They were from the garden center! The bag said "pet friendly".
Doreen: Do you still have the bag? {question- @+1}
Marco: In the shed. Yes.
Fatima: Pet friendly doesn't mean organic. That's the problem with those bags.
Marco: Then the garden center lied to me, not the other way around.
Gus: Back in my day you'd get one warning and then you'd be out.
Doreen: How many warnings have we given this year? {question- @+1}
Fatima: Three. None of them to Marco. {claim- F4}
Gus: Three this year. That's three too many. {claim- F4}
Marco: So I'm being judged on everyone else's warnings now? {~}
Doreen: Nobody's judging. Let's get the facts.
Fatima: Could you bring the bag to the shed on Saturday so we can read the label? {question- @+1}
Marco: Fine. Saturday morning. {action+}
Doreen: Then it's a formal warning only if the label shows metaldehyde. Otherwise nothing. {decision+}
Marco: That's all I wanted. A fair hearing.
Gus: Hmph.
## water :: The bill; Marco plays down the rise; Gus overcounts the plot holders and is corrected much later
Doreen: The water. Fatima? {question- @+1}
Fatima: Last quarter's bill was two thousand two hundred and forty. Usage is up thirty-five percent on last year. {claim- F3} {claim- F2}
Marco: With respect, it's barely up. Ten percent, maybe, with the heat. {claim+ F2 "10%"}
Fatima: It's thirty-five. I read the meter myself. {claim- F2}
Gus: With sixty plot holders, it's no surprise. More people, more water. {claim+ F1 "60"}
Doreen: Does anyone know of a leak? A tap left running? {question+} {~}
Gus: Back in my day we used watering cans. No hoses at all.
Marco: There are twelve taps, Gus. It's not the eighteen hundreds. {claim- F11}
Fatima: If it goes on like this, dues won't cover it. Dues are sixty a year. {claim- F10}
Doreen: Are we raising dues, then? {question- @+4}
Gus: Over my dead body.
Marco: Maybe a water surcharge for the big plots? {decision-} {question- @+1}
Fatima: That's complicated to measure.
Doreen: We'll put timers on the hoses first and see what the next bill says. {decision+}
Fatima: I'll order the hose timers this week, twelve of them. {action+} {claim- F11}
Doreen: My phone keeps buzzing, it's my daughter. Ignore it. {drift- 1}
Fatima: Gus, for the record, the register has forty-eight plot holders. Not sixty. {claim- F1}
Gus: Forty-eight. Well. It feels like sixty. {claim- F1}
## fair :: Date and jobs, quickly
Doreen: The fair. It's Saturday the seventeenth of May. {claim- F6}
Fatima: And last year we made about two thousand. {claim+ F7 "$2,000"}
Gus: Was it that much? It felt quieter. {question- @+1}
Fatima: Sorry, I'm looking at the accounts. Thirteen eighty. I had the gross, not the profit. {claim- F7}
Marco: I can run the plant stall again. It sold out last year. {action+}
Doreen: Thank you, Marco. That would help.
Gus: It'd be nice if somebody sorted the tea urn this time. It was cold by eleven. {action-}
Fatima: The urn's mine. I'll get the new one from the church hall. {action+}
Gus: Good. The plant stall and the tea are covered, then.
## elections :: Five seats, seven candidates; Doreen's news slips out
Doreen: The elections. Fatima, remind us.
Fatima: Five seats, seven candidates. Ballots at the fair, counted that evening. {claim- F8} {claim- F9}
Gus: Seven? Who are the seven? {question+} {claim- F9} {~}
Fatima: The list goes up on the shed door on Monday.
Marco: Is Doreen standing again? {question- @+2}
Doreen: Well.
Fatima: She's not. She told me last week.
Gus: You're not? After all this time? {question- @+1}
Doreen: No. It's someone else's turn. I'm tired, Gus.
Marco: With respect, you've been a good chair. Even tonight.
Doreen: Thank you, Marco. Ballots at the fair, counted that evening, as Fatima said. That's how we'll do it. {decision+}
Gus: Who's counting the ballots? It shouldn't be a candidate. {question+} {~}
Doreen: Right. I think that's everything. Thank you all for coming.
Fatima: Goodnight.
