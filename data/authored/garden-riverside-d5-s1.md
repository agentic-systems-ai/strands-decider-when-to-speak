---
meeting_id: garden-riverside-d5-s1
theme: "Community garden committee: plots, water and the spring fair"
domain_pack: community_group
drama: 0.5
seed: 1
author: claude-opus-5-5 (Claude Code session)
pack:
  title: Riverside garden committee
  org: Riverside Community Garden (fictional)
  agenda:
    - {id: plots, title: Plots, goal: Fill the vacant plots from the waitlist, timebox_min: 4}
    - {id: irrigation, title: Irrigation, goal: Decide whether to install the drip system, timebox_min: 5}
    - {id: spring_fair, title: Spring fair, goal: Confirm vendors and the layout, timebox_min: 4}
    - {id: volunteers, title: Volunteer hours, goal: Agree what happens when people don't do their hours, timebox_min: 3}
  facts:
    - {id: F1, key: plots_total, statement: "Total plots = 52", value: "52"}
    - {id: F2, key: plots_vacant, statement: "Vacant plots = 6", value: "6"}
    - {id: F3, key: waitlist, statement: "People on the waitlist = 17", value: "17"}
    - {id: F4, key: plot_fee, statement: "Plot fee = $55 a season", value: "$55"}
    - {id: F5, key: drip_quote, statement: "Drip irrigation quote = $3,800", value: "$3,800"}
    - {id: F6, key: water_bill_summer, statement: "Water bill last summer = $2,100", value: "$2,100"}
    - {id: F7, key: fair_date, statement: "Spring fair = Saturday, May 3", value: "May 3"}
    - {id: F8, key: fair_vendors, statement: "Fair vendors confirmed = 11", value: "11"}
    - {id: F9, key: volunteer_hours, statement: "Required volunteer hours = 8 per plot holder", value: "8"}
    - {id: F10, key: hours_compliance, statement: "Plot holders who completed their hours last year = 64%", value: "64%"}
    - {id: F11, key: garden_balance, statement: "Garden bank balance = $5,600", value: "$5,600"}
    - {id: F12, key: grant_deadline, statement: "City green-space grant deadline = March 15", value: "March 15"}
personas:
  - name: Esther
    role: Committee chair
    goals: A fair process and no shouting
    hidden_agenda: Founded the garden and finds change hard
    verbosity: 3
    wpm: 145
    catchphrases: []
    voice_gender: female
  - name: Dmitri
    role: Looks after irrigation
    goals: Get the drip system installed this year
    hidden_agenda: Already got a second quote he hasn't shared
    verbosity: 3
    wpm: 155
    catchphrases: []
    voice_gender: male
  - name: Holly
    role: Spring fair organizer
    goals: The biggest fair yet
    hidden_agenda: Counting vendors who haven't paid
    verbosity: 4
    wpm: 175
    catchphrases: []
    voice_gender: female
  - name: Bao
    role: Plot coordinator
    goals: Shorten the waitlist
    hidden_agenda: Thinks the volunteer-hours rule is unfair to shift workers
    verbosity: 2
    wpm: 160
    catchphrases: []
    voice_gender: male
---
## plots :: Vacant plots and the waitlist; Bao overstates the waitlist
Esther: Let's begin. Bao, the plots.
Bao: We have six vacant plots this season, out of the fifty-two. {claim- F2} {claim- F1}
Esther: And who's waiting for them? {question- @+1}
Bao: The waitlist is around thirty people now. It's grown a lot. {claim+ F3 "30"}
Holly: Thirty? I thought it was under twenty. {question- @+2} {~nc}
Esther: Bao, could you check the sheet? {question- @+1}
Bao: You're right, it's seventeen. I was counting people who emailed twice. {claim- F3} {~}
Holly: Seventeen for six plots is still a long wait. {claim- F3} {claim- F2}
Dmitri: Could we split a couple of the big plots in half? {question- @+1} {decision-}
Esther: Some of those plot holders have been here fifteen years. They won't like it.
Dmitri: They don't use half of it, though. It's all squash.
Esther: That reminds me, the old fence by the gate went up the year I joined. Fifteen years ago. {drift- 1} {~}
Bao: I'll offer the six plots to the first six on the list this week. {action+}
Esther: Good. And splitting plots, we'll leave that for the annual meeting. {decision-} 
Dmitri: Fine.
## irrigation :: The drip system; Dmitri's quote figure is low and nobody notices
Esther: Irrigation. Dmitri, you've been pushing the drip system.
Dmitri: I have. The quote was three thousand dollars, installed. {claim+ F5 "$3,000"}
Holly: That's a lot of money for hoses.
Dmitri: It's not hoses. It's a timed system. It would cut our water use by half. {~} 
Holly: And who maintains the timers once it's in? {question+} {~}
Bao: What did the water cost last summer? {question- @+1}
Esther: Twenty-one hundred, from the bill. {claim- F6}
Dmitri: So it pays for itself in a couple of summers.
Holly: Can we even afford it right now? {question- @+1}
Esther: The bank balance is fifty-six hundred. We could, but it would leave very little. {claim- F11}
Dmitri: There's a city green-space grant. The deadline is March fifteenth. {claim- F12}
Bao: Could the grant cover the whole thing? {question- @+1}
Dmitri: Most of it. They fund up to seventy-five percent. {~}
Holly: Then we apply for the grant and only pay the rest ourselves.
Esther: That's the sensible way. We'll apply for the grant, and install the drip system if we get it. {decision+}
Dmitri: I'll write the grant application this weekend and send it round by Wednesday. {action+}
Holly: Somebody has to show the city photos of the plots. They always want photos. {action-}
Bao: I take photos every week anyway. I'll send Dmitri the best ones. {action+}
## spring_fair :: Vendors and layout; Holly's vendor count is corrected later; a tangent about the mayoral debate
Esther: The spring fair. Holly? {question- @+1}
Holly: May third, rain or shine. And we have fifteen vendors confirmed, which is our best year. {claim- F7} {claim+ F8 "15"}
Esther: Fifteen. Wonderful. {claim+ F8 "15"}
Bao: Where do they all go? The path by the beds is narrow. {question- @+1}
Holly: Along the fence, and the food ones in the parking lot.
Dmitri: The parking lot is where the mayoral debate stage was last fall. {drift+ 3}
Esther: That debate. Neither of them knew where the garden even was.
Holly: One of them called it a park. A park!
Bao: So, the parking lot for food. Do we need a permit for that? {question- @+1}
Holly: The church owns the lot. They just want us to clean up after.
Esther: Holly, how many vendors have actually paid their fee? {question- @+1}
Holly: Oh. Paid? Eleven. The other four said yes but haven't paid. {claim- F8} {~}
Esther: Then it's eleven confirmed until they pay. {claim- F8}
Holly: Fine. Eleven confirmed, four likely. {claim- F8}
Dmitri: I'll chase the four unpaid vendors on Friday if you send me their numbers. {action+}
Holly: I'll send you the list tonight. {action+}
Bao: Who's doing the plant sale table this year? {question+} {~}
Holly: The layout map should go on the shed door so people know where to set up.
## volunteers :: The hours rule; a real disagreement
Esther: Volunteer hours. Eight hours per plot holder, as always. {claim- F9}
Bao: Only sixty-four percent did their hours last year. {claim- F10}
Holly: Then the other third should lose their plots. That's the rule.
Bao: Some of them work nights. They can't come to Saturday work days.
Esther: The rule doesn't say Saturdays. It says eight hours. {claim- F9}
Bao: In practice, all the work days are Saturdays.
Dmitri: What if we had a weekday evening work day once a month? {question- @+1}
Esther: That's fair. Nobody can say we didn't offer.
Holly: Okay, evening work days. But after that, if you don't do your hours, you lose the plot.
Esther: Then that's the rule: one evening work day a month, and the hours are enforced from June. {decision+}
Bao: I'll put the evening dates on the shared calendar this week. {action+}
Dmitri: Does a plot holder get a warning before they lose the plot? {question- @+1}
Esther: A written warning in August, and then a conversation. Nobody loses a plot by email. Thank you all. Good meeting. {decision+}
