---
meeting_id: pta-hillcrest-d8-s2
theme: School PTA budget meeting for next year
domain_pack: community_budget
drama: 0.8
seed: 2
author: claude-opus-5-5 (Claude Code session)
pack:
  title: PTSA budget meeting
  org: Hillcrest High School PTSA (fictional)
  agenda:
    - {id: finances, title: Where the money is, goal: Agree the balance and income, timebox_min: 4}
    - {id: prom, title: Prom subsidy, goal: Decide on the prom subsidy request, timebox_min: 4}
    - {id: wellness, title: Wellness program, goal: Decide whether to fund the student wellness program, timebox_min: 5}
    - {id: vote, title: The vote, goal: Agree what goes to the membership, timebox_min: 3}
  facts:
    - {id: F1, key: balance, statement: "Current balance = $18,400", value: "$18,400"}
    - {id: F2, key: annual_income, statement: "Annual income = $36,900", value: "$36,900"}
    - {id: F3, key: prom_cost, statement: "Total prom cost = $24,000", value: "$24,000"}
    - {id: F4, key: prom_ticket, statement: "Prom ticket price = $85", value: "$85"}
    - {id: F5, key: prom_subsidy_request, statement: "Prom subsidy request = $6,000", value: "$6,000"}
    - {id: F6, key: wellness_cost, statement: "Wellness program cost = $7,200", value: "$7,200"}
    - {id: F7, key: students, statement: "Students enrolled = 1,140", value: "1,140"}
    - {id: F8, key: seniors, statement: "Seniors = 268", value: "268"}
    - {id: F9, key: counselor_ratio, statement: "Students per counselor = 380", value: "380"}
    - {id: F10, key: grad_night, statement: "Grad night cost = $9,500", value: "$9,500"}
    - {id: F11, key: member_families, statement: "Member families = 205", value: "205"}
    - {id: F12, key: vote_date, statement: "Membership vote = February 12", value: "February 12"}
personas:
  - name: Valerie
    role: PTSA president
    goals: Get a budget through without a revolt
    hidden_agenda: Her own son is a senior and wants a cheaper prom
    verbosity: 3
    wpm: 160
    catchphrases: []
    voice_gender: female
  - name: Dwayne
    role: Treasurer
    goals: Don't empty the account
    hidden_agenda: Was outvoted on grad night last year and is still sore
    verbosity: 2
    wpm: 140
    catchphrases: []
    voice_gender: male
  - name: Sienna
    role: Student representative, a junior
    goals: Fund the wellness program
    hidden_agenda: Several friends are on the counselor waitlist
    verbosity: 3
    wpm: 175
    catchphrases: []
    voice_gender: female
  - name: Phil
    role: Parent, new to the PTSA
    goals: Spend the money on the kids now
    hidden_agenda: Thinks the PTSA hoards money
    verbosity: 4
    wpm: 180
    catchphrases: []
    voice_gender: male
---
## finances :: The balance; Phil's number is much higher than the real one
Valerie: Thanks for coming, everyone. Dwayne, start us off with where we are? {question- @+1}
Dwayne: Balance is eighteen thousand four hundred. Annual income was thirty-six nine. {claim- F1} {claim- F2}
Phil: Hold on. I was told we're sitting on thirty grand. Where's the rest? {claim+ F1 "$30,000"} {question- @+1}
Dwayne: There is no rest. It was never thirty. {~nc}
Phil: My neighbor said thirty. {claim+ F1 "$30,000"}
Valerie: Your neighbor is not the treasurer, Phil.
Dwayne: Eighteen four. I can send you every statement if you want them. {claim- F1} {action-}
Phil: Yeah, I want them.
Dwayne: Fine. You'll have them tonight. {action+}
Sienna: How many families are members now? {question- @+1}
Valerie: Two hundred and five, out of about eleven hundred students. {claim- F11} {claim- F7} {~}
Phil: Two hundred families paying for eleven hundred kids. That's the real problem. {claim- F11} {claim- F7}
## prom :: The subsidy request; Sienna's ticket price is off, and corrected only at the end of the section
Valerie: The prom. The class officers asked for six thousand to bring the ticket price down. {claim- F5}
Sienna: Tickets are a hundred dollars right now. That's a lot for some families. {claim+ F4 "$100"}
Phil: Then give them the six grand. Easy. {claim- F5}
Dwayne: Prom costs twenty-four thousand total. The subsidy is a quarter of it. {claim- F3}
Valerie: We have about four hundred seniors, so six thousand is fifteen dollars each. {claim+ F8 "400"} {claim- F5}
Dwayne: That's a lot of money for one night.
Sienna: It's the one night some of them will remember.
Phil: The Tigers might make the state semifinal, did you see? First time in twenty years. {drift+ 3} {~}
Dwayne: They lost to Eastfield last week.
Phil: Eastfield cheats. Everyone knows it.
Sienna: Can we please stay on prom? {~}
Dwayne: What about a sliding scale instead? Free for kids on lunch assistance, full price for everyone else. {question- @+1} {decision-}
Valerie: That's harder to run, but it's fairer.
Sienna: Wait, I just checked the student portal. Tickets are eighty-five, not a hundred. I had last year's price. {claim- F4}
Phil: Eighty-five, a hundred, kids still can't afford it. {claim- F4}
Valerie: Okay. Three thousand for a sliding scale, aimed at students on lunch assistance. That's what we'll propose. {decision+} {~}
## wellness :: The real fight; the counselor ratio
Sienna: The wellness program. Seventy-two hundred for a part-time counselor and the peer support training. {claim- F6}
Phil: Isn't that the school district's job? {question- @+1}
Sienna: It should be. But each counselor has like six hundred kids. {claim+ F9 "600"}
Dwayne: The district number is three eighty per counselor. Still too many, but not six hundred. {claim- F9}
Sienna: Three eighty. Okay. It's still a waitlist of weeks. {claim- F9}
Phil: Seventy-two hundred and we can't even do grad night? {~} {claim- F6}
Dwayne: Grad night is ninety-five hundred. We've never covered all of it. {claim- F10}
Valerie: Here's what I'm hearing. Wellness matters more than one party.
Phil: Says the woman whose kid wants a cheap prom.
Valerie: That's not fair, Phil.
Dwayne: It's not. Let's keep it about the budget.
Sienna: Could the program start with just the peer support training this year? It's cheaper. {question- @+1} {decision-}
Dwayne: That part is about two thousand. The counselor is the expensive part. {~}
Sienna: Then the full program. It's seventy-two hundred and it's worth it. {claim- F6}
Valerie: We fund the wellness program in full, and grad night gets what's left after that. {decision+}
Phil: Grad night gets nothing, then.
Dwayne: Not nothing. Less.
## vote :: What goes to the membership
Valerie: The vote is on February twelfth. {claim- F12}
Dwayne: I'll put together the proposed budget and send it to the board by Monday. {action+}
Phil: Can parents propose changes at the meeting? {question- @+1}
Valerie: Amendments are allowed, if they're seconded.
Phil: Then I'll be proposing one. {action+}
Sienna: Will students be allowed to speak at the vote? {question+} {~}
Dwayne: Phil, if you're proposing an amendment, send it to me in writing first. {~}
Phil: Fine. Who's chairing the vote, you or Valerie? {question- @+1} {action+}
Valerie: I am. And it'll be orderly.
Phil: We'll see.
