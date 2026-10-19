---
meeting_id: pta-lakeview-d2-s1
theme: School PTA budget meeting for next year
domain_pack: community_budget
drama: 0.2
seed: 1
author: claude-opus-5-5 (Claude Code session)
pack:
  title: PTA budget meeting
  org: Lakeview Primary School PTA (fictional)
  agenda:
    - {id: review, title: The year in review, goal: Agree last year's income, spending and reserve, timebox_min: 4}
    - {id: income, title: Income plan, goal: Choose next year's fundraisers, timebox_min: 4}
    - {id: grants, title: Grants and requests, goal: Set the classroom grants and decide on the library and assembly requests, timebox_min: 5}
    - {id: timeline, title: Timeline, goal: Agree the steps to the membership vote, timebox_min: 3}
  facts:
    - {id: F1, key: income_last_year, statement: "Income last year = $22,700", value: "$22,700"}
    - {id: F2, key: spending_last_year, statement: "Spending last year = $21,150", value: "$21,150"}
    - {id: F3, key: reserve, statement: "Reserve = $6,400", value: "$6,400"}
    - {id: F4, key: book_fair_profit, statement: "Book fair profit = $2,950", value: "$2,950"}
    - {id: F5, key: students, statement: "Students enrolled = 268", value: "268"}
    - {id: F6, key: teachers, statement: "Classroom teachers = 14", value: "14"}
    - {id: F7, key: classroom_grant, statement: "Classroom grant = $150 per teacher", value: "$150"}
    - {id: F8, key: library_request, statement: "Library request = $3,000", value: "$3,000"}
    - {id: F9, key: movie_night_profit, statement: "Movie night profit = $640", value: "$640"}
    - {id: F10, key: membership_rate, statement: "Families who are PTA members = 58%", value: "58%"}
    - {id: F11, key: assembly_cost, statement: "Science assembly cost = $1,200", value: "$1,200"}
    - {id: F12, key: vote_date, statement: "Membership vote = June 3", value: "June 3"}
personas:
  - name: Margaret
    role: PTA president
    goals: A simple, fair budget
    hidden_agenda: Wants to finish her term without a fuss
    verbosity: 3
    wpm: 145
    catchphrases: []
    voice_gender: female
  - name: Tunde
    role: Treasurer
    goals: Accurate books and a healthy reserve
    hidden_agenda: Training a successor and wants the process documented
    verbosity: 2
    wpm: 140
    catchphrases: []
    voice_gender: male
  - name: Ines
    role: Teacher representative
    goals: Classroom grants that actually cover supplies
    hidden_agenda: The library is her real priority
    verbosity: 3
    wpm: 155
    catchphrases: []
    voice_gender: female
  - name: Craig
    role: Parent volunteer, runs the book fair
    goals: A bigger book fair next year
    hidden_agenda: Remembers the good parts of every event
    verbosity: 3
    wpm: 165
    catchphrases: []
    voice_gender: male
---
## review :: Last year's numbers; Craig's book fair memory is generous
Margaret: Good evening, everyone. Let's start with last year, then work forward. Tunde, could you give us the summary? {question- @+1}
Tunde: Of course. Income was twenty-two thousand seven hundred, and we spent twenty-one thousand one hundred and fifty. {claim- F1} {claim- F2} {~}
Margaret: So a small surplus.
Tunde: Yes. The reserve is now six thousand four hundred. {claim- F3}
Craig: And the book fair did well, didn't it? I think it made about four thousand. {claim+ F4 "$4,000"} {question- @+1}
Tunde: It made two thousand nine hundred and fifty. Sales were close to four thousand, but that's before the publisher's share. {claim- F4}
Craig: Ah, that's right. The publisher takes their cut.
Ines: It's still the best fundraiser we have.
Margaret: And movie night? {question- @+1}
Tunde: Six hundred and forty. Small, but the families enjoy it. {claim- F9}
Craig: The popcorn machine nearly caught fire, if I remember correctly.
Ines: The popcorn machine is fine now. The caretaker replaced the element.
Margaret: How many families are members at the moment? {question- @+1}
Tunde: Fifty-eight percent of families. Up a little from last year. {claim- F10}
Ines: That's good for a school our size.
## income :: Next year's fundraisers; a quick detour about the new caretaker's dog
Margaret: Income for next year. I'd suggest we keep what works.
Craig: The book fair, certainly. I'd like to try two book fairs, one in autumn and one in spring.
Tunde: Would the publisher agree to two in one year? {question- @+1}
Craig: They offer it to every school. We've just never asked.
Ines: Two book fairs would mean more volunteers.
Craig: I'll ask the publisher about a spring date and check how many volunteers they recommend. {action+}
Tunde: Does the publisher pay for delivery, or do we? {question+} {~}
Margaret: Thank you, Craig. And movie night stays.
Tunde: Movie night stays. It's low effort. {decision+}
Ines: Has everyone met Pepper? The caretaker brings her in on Fridays now. {drift+ 2} {question- @+1}
Craig: The children adore her. She sat through a whole assembly last week.
Margaret: Shall we add a sponsored walk? Other schools do very well with them. {question+} {~}
Tunde: It would need a permit for the park, I think.
Ines: The children would enjoy it, and it gets families outside.
Margaret: Let's think about the walk over the summer and decide in September. {decision-}
Tunde: That seems sensible.
## grants :: Classroom grants and two requests; the teacher count nobody checks
Margaret: Grants. The classroom grant is a hundred and fifty per teacher at the moment. {claim- F7}
Ines: Which is not much. A box of good markers costs a fortune.
Margaret: With eighteen teachers, that's two thousand seven hundred. {claim+ F6 "18"} {~}
Tunde: Could we raise it to two hundred? {question- @+1} {decision-} {~}
Ines: That would make a real difference to the younger classes.
Tunde: Then the classroom grant goes up to two hundred per teacher. We can afford it. {decision+} {~}
Ines: Thank you. And the library request. Three thousand, for new books and two reading chairs. {claim- F8}
Craig: Three thousand is more than the book fair makes. {claim- F8}
Ines: The library hasn't had new chairs since before I started here.
Craig: It would be lovely if somebody looked into the council's library grants. {action-}
Tunde: The reserve could cover part of it. Perhaps half from the reserve and half from next year's income. {decision-}
Margaret: I like that. It doesn't touch the classroom grants. And the science assembly? The company quoted twelve hundred. {claim- F11} {question- @+1}
Ines: The children talked about last year's for weeks. The exploding pumpkin.
Craig: Twelve hundred for one morning is a lot, though. {claim- F11}
Ines: It's two hundred and sixty-eight children for one morning. That's under five dollars each. {claim- F5} {~}
Margaret: Then the library gets its three thousand, half from the reserve, and the assembly stays. {decision+} {claim- F8}
Tunde: I'll update the draft budget with those changes this week. {action+}
## timeline :: Steps to the vote; one question left open
Margaret: Timeline. The vote is on June third. {claim- F12}
Tunde: The draft should go to families two weeks before, so around the twentieth of May. {~}
Ines: Could it be shared in the school newsletter as well? More people read that than the emails. {question- @+1}
Margaret: That's a good idea. The newsletter goes out every other Friday.
Craig: I'll write a short piece about the book fairs for the same newsletter. {action+}
Tunde: Should we explain why the reserve is going down? Some families watch it closely. {question+} {~}
Ines: Who prints the voting slips this year? Last year we ran short. {question- @+1}
Margaret: The school office has offered. I'll confirm with them. That's everything. Thank you all, and good night. {action+}
Tunde: Good night.
