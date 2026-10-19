---
meeting_id: pta-willowcreek-d2-s2
theme: School PTA budget meeting for next year
domain_pack: community_budget
drama: 0.2
seed: 2
author: claude-opus-5-5 (Claude Code session)
pack:
  title: PTO budget planning
  org: Willow Creek Elementary PTO (fictional)
  agenda:
    - {id: recap, title: This year's numbers, goal: Agree income, expenses and the reserve, timebox_min: 4}
    - {id: fundraisers, title: Fundraisers, goal: Keep, change or drop each fundraiser, timebox_min: 4}
    - {id: spending, title: Spending plan, goal: Classroom grants, buses, the playground and the yearbook, timebox_min: 5}
    - {id: next_steps, title: Next steps, goal: Get the draft ready for the vote, timebox_min: 3}
  facts:
    - {id: F1, key: income, statement: "Income this year = $19,300", value: "$19,300"}
    - {id: F2, key: expenses, statement: "Expenses this year = $18,050", value: "$18,050"}
    - {id: F3, key: reserve, statement: "Reserve = $4,800", value: "$4,800"}
    - {id: F4, key: walkathon_net, statement: "Walkathon net = $8,900", value: "$8,900"}
    - {id: F5, key: students, statement: "Students = 340", value: "340"}
    - {id: F6, key: classroom_grant, statement: "Classroom grant = $125 per teacher", value: "$125"}
    - {id: F7, key: teachers, statement: "Classroom teachers = 17", value: "17"}
    - {id: F8, key: bus_cost, statement: "Field trip bus = $520 each", value: "$520"}
    - {id: F9, key: paint_quote, statement: "Playground paint quote = $2,200", value: "$2,200"}
    - {id: F10, key: yearbook_cost, statement: "Yearbook cost = $14 per book", value: "$14"}
    - {id: F11, key: yearbook_orders, statement: "Yearbook orders = 210", value: "210"}
    - {id: F12, key: vote_date, statement: "Membership vote = May 20", value: "May 20"}
personas:
  - name: Rebecca
    role: PTO president
    goals: A calm, simple budget
    hidden_agenda: Wants the playground painted before her youngest moves on
    verbosity: 3
    wpm: 150
    catchphrases: []
    voice_gender: female
  - name: Hiro
    role: Treasurer
    goals: Accurate numbers, no surprises
    hidden_agenda: Has a spreadsheet for everything
    verbosity: 2
    wpm: 140
    catchphrases: []
    voice_gender: male
  - name: Gloria
    role: Teacher representative, third grade
    goals: Supplies and field trips for the kids
    hidden_agenda: Her class missed the zoo trip last year
    verbosity: 3
    wpm: 155
    catchphrases: []
    voice_gender: female
  - name: Samir
    role: Parent volunteer, runs the walkathon
    goals: A bigger walkathon
    hidden_agenda: Remembers the pledges, not what was collected
    verbosity: 3
    wpm: 165
    catchphrases: []
    voice_gender: male
---
## recap :: This year's numbers; Samir's walkathon memory is generous
Rebecca: Hi, everyone. Thanks for staying after pickup. Hiro, could you start us off? {question- @+1}
Hiro: Sure. Income was nineteen thousand three hundred, and expenses were eighteen thousand and fifty. {claim- F1} {claim- F2} {~}
Rebecca: So we ended up a little ahead.
Hiro: A little. The reserve is forty-eight hundred now. {claim- F3}
Gloria: That's more than I expected, honestly.
Samir: The walkathon did most of it. I think it brought in about twelve thousand. {claim+ F4 "$12,000"}
Hiro: The pledges were about twelve. What we actually collected was eighty-nine hundred. {claim- F4}
Samir: Oh, right. Some families never paid their pledges. That happens every year.
Gloria: Still, eighty-nine hundred from kids walking in circles. That's amazing. {claim- F4}
Rebecca: It really is. The kids love it, too.
Samir: My son asked if he could do it twice this year.
Hiro: The other fundraisers were small. The book fair and the spring concert bake sale.
Rebecca: Anything that lost money? {question- @+1}
Hiro: The movie night broke even. Nothing lost money.
## fundraisers :: What to keep
Rebecca: Fundraisers for next year. I'd keep the walkathon, obviously.
Samir: Could we send pledge reminders this time? It might close the gap between pledged and collected. {question- @+1}
Hiro: Yes, please. The online form can send a reminder after a week.
Samir: I'll set up the reminders on the form before the walkathon. {action+}
Gloria: The bake sale is a lot of work for what it makes. The teachers end up baking half of it.
Rebecca: Should we drop it? {question- @+2}
Gloria: Maybe just make it smaller. Cookies only.
Hiro: The concert families like it, though. It's part of the evening.
Rebecca: Then the bake sale stays, but it's cookies only and parents bring them. {decision+}
Gloria: Thank you. The teachers will be grateful.
Samir: The new bakery on Elm makes the best cookies I've ever had, by the way. The ginger ones. {drift+ 3}
Hiro: Is that the one with the blue door? I've walked past it every day. {~}
Gloria: Go in. Trust me. The lemon bars too.
## spending :: Grants, buses, the playground and the yearbook; Rebecca's teacher count goes unchecked
Rebecca: Okay, I'm hungry now. Spending. Classroom grants are a hundred and twenty-five per teacher, and we have twenty teachers, so that's twenty-five hundred. {claim- F6} {claim+ F7 "20"}
Gloria: A hundred and twenty-five doesn't go far, but every bit helps. {claim- F6}
Hiro: We could raise it to a hundred and fifty with the surplus. {decision-} {~nc}
Rebecca: Let's keep it at a hundred and twenty-five this year, and see how the walkathon does. {decision+} {claim- F6}
Gloria: The buses are the thing I really want. Five hundred and twenty a bus, and we lost the zoo trip last year. {claim- F8}
Hiro: How many buses would the zoo need? {question- @+1}
Gloria: Three. One per class in the grade.
Hiro: That's fifteen sixty. We can do that. {~nc}
Rebecca: Then the third-grade zoo trip is funded this year. {decision+}
Gloria: I'll book the zoo date with the office tomorrow. {action+}
Rebecca: And the playground. The paint quote was twenty-two hundred. {claim- F9}
Hiro: That's half the reserve. {~nc}
Rebecca: The lines are so faded the kids can't see the hopscotch.
Samir: Could parents paint it on a Saturday instead? We'd just need the paint. {question- @+1}
Hiro: Paint is maybe four hundred. Much cheaper. {~nc}
Rebecca: A parent paint day. I love that.
Gloria: Somebody would need to check the school allows it. Insurance and so on. {action-}
Rebecca: I'll ask the principal this week. {action+}
Hiro: Yearbooks are fourteen dollars each, and we have two hundred and ten orders so far. {claim- F10} {claim- F11}
Samir: Do the yearbooks pay for themselves? {question- @+1}
Hiro: They do, with a little left over.
## next_steps :: The vote
Rebecca: Next steps. The vote is on May twentieth. {claim- F12}
Hiro: I'll put the draft budget together and send it to the board a week before. {action+}
Gloria: Can the draft go home in backpacks too? Not every family reads email. {question- @+1}
Rebecca: Yes. Paper copies in the Friday folders.
Samir: Will there be childcare at the vote meeting? Turnout is always low without it. {question+} {~}
Rebecca: Thank you, everyone. That was easy. I wish every meeting was like this.
