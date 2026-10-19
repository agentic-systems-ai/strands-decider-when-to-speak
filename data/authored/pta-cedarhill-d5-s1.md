---
meeting_id: pta-cedarhill-d5-s1
theme: School PTA budget meeting for next year
domain_pack: community_budget
drama: 0.5
seed: 1
author: claude-opus-5-5 (Claude Code session)
pack:
  title: PTSA budget planning - next school year
  org: Cedar Hill Middle School PTSA (fictional)
  agenda:
    - {id: actuals, title: This year's actuals, goal: Agree what we earned, spent and carried over, timebox_min: 4}
    - {id: revenue, title: Revenue plan, goal: Decide on dues and fundraisers for next year, timebox_min: 4}
    - {id: requests, title: Funding requests, goal: Weigh instruments, the science fair and the eighth-grade trip, timebox_min: 5}
    - {id: process, title: Budget process, goal: Agree the timeline to the membership vote, timebox_min: 3}
  facts:
    - {id: F1, key: income_this_year, statement: "Income this year = $31,400", value: "$31,400"}
    - {id: F2, key: expenses_this_year, statement: "Expenses this year = $29,800", value: "$29,800"}
    - {id: F3, key: carryover, statement: "Carryover into next year = $9,100", value: "$9,100"}
    - {id: F4, key: membership_dues, statement: "Membership dues = $15 per family", value: "$15"}
    - {id: F5, key: member_families, statement: "Member families = 312", value: "312"}
    - {id: F6, key: instrument_request, statement: "Music instrument request = $7,500", value: "$7,500"}
    - {id: F7, key: science_fair_cost, statement: "Science fair cost = $1,900", value: "$1,900"}
    - {id: F8, key: trip_subsidy, statement: "Eighth-grade trip subsidy = $40 per student", value: "$40"}
    - {id: F9, key: eighth_graders, statement: "Eighth graders next year = 228", value: "228"}
    - {id: F10, key: spirit_wear_profit, statement: "Spirit wear profit = $3,200", value: "$3,200"}
    - {id: F11, key: district_grant, statement: "District matching grant = $2,000", value: "$2,000"}
    - {id: F12, key: budget_vote_date, statement: "Membership budget vote = May 14", value: "May 14"}
personas:
  - name: Monica
    role: PTSA president
    goals: A budget that funds something for every grade
    hidden_agenda: Promised the band director she'd fight for instruments
    verbosity: 3
    wpm: 160
    catchphrases: ["alrighty", "so here's my thinking"]
    voice_gender: female
  - name: Kwame
    role: Treasurer
    goals: Never spend the carryover to zero
    hidden_agenda: Got burned two years ago when a fundraiser flopped
    verbosity: 2
    wpm: 140
    catchphrases: ["per the books", "carefully"]
    voice_gender: male
  - name: Lisa
    role: Teacher representative, music teacher
    goals: New instruments for the band
    hidden_agenda: Half the trumpets are held together with tape
    verbosity: 3
    wpm: 165
    catchphrases: ["I'll be honest", "the kids"]
    voice_gender: female
  - name: Arjun
    role: Parent, works in data analytics
    goals: Spend where it helps the most kids
    hidden_agenda: Thinks the trip subsidy is regressive
    verbosity: 3
    wpm: 170
    catchphrases: ["if you look at the numbers", "quick thought"]
    voice_gender: male
---
## actuals :: What came in and went out; Arjun's carryover number is too rosy
Monica: Alrighty, let's start with where we ended up this year. Kwame, the headline? {question- @+1}
Kwame: Per the books, income was thirty-one four, expenses twenty-nine eight. {claim- F1} {claim- F2}
Arjun: So, if you look at the numbers, we're carrying over something like fifteen thousand. {claim+ F3 "$15,000"}
Kwame: Carefully. It's nine thousand one hundred. The rest was already committed to the library fund. {claim- F3}
Arjun: Ah. Right, the library fund. I forgot that moved.
Lisa: Nine thousand. Okay. That's less than I hoped. {claim- F3}
Monica: What did spirit wear bring in? It felt like a good year. {question- @+1}
Kwame: Thirty-two hundred profit. Best year yet. {claim- F10}
Lisa: The hoodies. Every kid has the hoodie.
Arjun: Quick thought, should spirit wear just become a bigger part of the plan? {question+} {~}
Monica: Maybe. Let's hold that for revenue.
Kwame: And the district matched two thousand, which we should not count on again. {claim- F11}
Arjun: Why not? {question- @+1}
Kwame: Per the district, it was a one-time pilot.
Monica: Alrighty. So we start next year with nine one and no guarantee of the match. {claim- F3}
Lisa: I'll be honest, that's a sobering start. {~}
## revenue :: Dues, fundraisers and Monica's membership guess
Monica: So here's my thinking. Dues are fifteen dollars, and we have about four hundred families. {claim- F4} {claim+ F5 "400"}
Arjun: Should we raise dues? Twenty dollars wouldn't kill anyone. {question- @+1}
Lisa: It would kill some families. Some of our kids are on free lunch.
Kwame: Carefully. Raising dues usually drops membership. We saw that at the elementary school.
Monica: Then dues stay at fifteen. I don't want to price anyone out. {decision+} {claim- F4}
Arjun: Then spirit wear is the lever. If you look at the numbers, it's our best margin.
Lisa: A second spirit wear sale in the spring? The kids would love it. {question- @+1} {decision-}
Kwame: The vendor has a minimum order. We'd need to check.
Arjun: I can look into the vendor minimums, if nobody else wants it. {action-}
Monica: Would you? That'd be great. {question- @+1}
Arjun: Sure. I'll get the vendor's minimums and pricing by next week. {action+} {~}
Lisa: Quick question, what happened to the restaurant nights? They used to be fun. {question+} {~}
Monica: Did everyone see the new crosswalk on Birch? It finally has a light. {drift+ 3} {question- @+1}
Kwame: About time. I've been honking at that intersection for years.
Lisa: The crossing guard brought cookies to celebrate.
Arjun: So, the fun run. Are we doing it again? {question- @+1}
Monica: Yes, the fun run stays. It's half our income. {decision+} {~}
Kwame: Agreed.
## requests :: Instruments vs the science fair vs the trip; the eighth-grade count gets fixed
Monica: Requests. Lisa, you go first. I know you're dying to.
Lisa: I'll be honest, the band needs instruments. The request is seventy-five hundred. {claim- F6} {~}
Arjun: That's most of our carryover.
Lisa: It's ten years of trumpets that are held together with tape.
Kwame: And the science fair is nineteen hundred, same as always. {claim- F7}
Monica: And the eighth-grade trip subsidy. Forty dollars a kid. {claim- F8}
Arjun: If you look at the numbers, two hundred eighth graders at forty is eight thousand. {claim+ F9 "200"} {claim- F8}
Lisa: It's two twenty-eight next year. It's a big class. {claim- F9}
Arjun: Two twenty-eight. So, over nine thousand. {claim- F9} {~}
Kwame: Carefully. We cannot fund all three in full.
Monica: So here's my thinking. Science fair in full, instruments in full, trip subsidy cut in half. {decision-}
Arjun: Quick thought, what if the trip subsidy only goes to families who need it? {question- @+1}
Lisa: The kids would know who got it. Kids always know.
Arjun: Not if it's done quietly through the counselor.
Kwame: That could work. It also costs a lot less.
Monica: Alrighty. Science fair in full, instruments in full, and the trip subsidy goes need-based through the counselor. That's what we're proposing. {decision+}
Lisa: The trumpets thank you. I'll get three quotes for the instruments before the vote. {action+}
Kwame: Somebody should probably talk to the counselor before we put that in writing. {action-}
## process :: Timeline to the vote; a date mix-up corrected
Monica: Last thing. The vote is May fourth, right? {claim+ F12 "May 4"} {question- @+1}
Kwame: Per the books, it's the fourteenth. May fourteenth. {claim- F12}
Monica: Fourteenth. Thank you. {claim- F12}
Arjun: When does the draft go out to members? {question- @+1}
Kwame: Two weeks before. Carefully, so people have time to read it.
Monica: I'll write the cover letter explaining the need-based subsidy, so nobody's surprised. {action+}
Lisa: Should I bring a trumpet to the vote? For drama? {question- @+1}
Monica: Absolutely bring the trumpet.
Arjun: Who's presenting the numbers at the vote? {question+} {~}
Monica: Alrighty, I think we're done. Thank you, everyone.
Kwame: Goodnight.
