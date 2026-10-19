---
meeting_id: pta-budget-d8-s1
theme: School PTA budget meeting for next year
domain_pack: community_budget
drama: 0.8
seed: 1
author: claude-opus-5-5 (Claude Code session)
pack:
  title: PTA budget meeting - next school year
  org: Maplewood Elementary PTA (fictional)
  agenda:
    - {id: last_year, title: Last year's actuals, goal: Agree what came in and what went out last year, timebox_min: 4}
    - {id: fundraising, title: Fundraising plan, goal: Pick next year's fundraisers and realistic targets, timebox_min: 4}
    - {id: spending, title: Spending requests, goal: Weigh the playground, teacher grants and field trips, timebox_min: 5}
    - {id: approval, title: Approval and next steps, goal: Agree how the budget gets voted on, timebox_min: 3}
  facts:
    - {id: F1, key: last_year_revenue, statement: "Last year's total revenue = $48,200", value: "$48,200"}
    - {id: F2, key: last_year_spend, statement: "Last year's total spending = $44,900", value: "$44,900"}
    - {id: F3, key: reserve_balance, statement: "Reserve balance = $12,600", value: "$12,600"}
    - {id: F4, key: fun_run_net, statement: "Fun run net last year = $17,300", value: "$17,300"}
    - {id: F5, key: enrollment, statement: "Student enrollment = 412", value: "412"}
    - {id: F6, key: teacher_grant_requests, statement: "Teacher grant requests total = $9,800", value: "$9,800"}
    - {id: F7, key: bus_cost, statement: "Field trip bus cost = $650 per bus", value: "$650"}
    - {id: F8, key: playground_quote, statement: "Playground resurfacing quote = $22,000", value: "$22,000"}
    - {id: F9, key: member_families, statement: "PTA member families = 186", value: "186"}
    - {id: F10, key: auction_net_last_year, statement: "Spring auction net last year = $8,400", value: "$8,400"}
    - {id: F11, key: budget_vote_date, statement: "General membership budget vote = September 25", value: "September 25"}
    - {id: F12, key: classroom_grant, statement: "Classroom grant per teacher = $200", value: "$200"}
personas:
  - name: Denise
    role: PTA president, runs the meeting
    goals: Get a budget everyone can live with before the vote
    hidden_agenda: Exhausted; wants someone else to chair next year
    verbosity: 4
    wpm: 170
    catchphrases: ["okay, folks", "bear with me"]
    voice_gender: female
  - name: Carl
    role: Treasurer
    goals: Defend the books
    hidden_agenda: Feels accused every time someone asks about money
    verbosity: 3
    wpm: 145
    catchphrases: ["it's all in the report", "with respect"]
    voice_gender: male
  - name: Yolanda
    role: Teacher representative
    goals: More money for classroom grants
    hidden_agenda: Her own classroom grant was denied last year
    verbosity: 4
    wpm: 165
    catchphrases: ["for the kids", "I'm sorry, but"]
    voice_gender: female
  - name: Brett
    role: Parent, new to the PTA, outspoken
    goals: Fix the playground now
    hidden_agenda: Suspects the PTA is hoarding money
    verbosity: 5
    wpm: 180
    catchphrases: ["here's the thing", "no offense"]
    voice_gender: male
---
## last_year :: Actuals; Brett inflates the revenue and suspects a hoard
Denise: Okay, folks, bear with me, my screen share is being difficult. Can everybody see the budget sheet? {~}
Carl: I can see it. It's all in the report, too, if anyone wants the numbers in front of them.
Denise: Great. So, last year first. Carl, the headline? {question- @+1}
Carl: Total revenue was forty-eight thousand two hundred, and we spent forty-four nine. {claim- F1} {claim- F2}
Brett: Here's the thing, I heard we raised sixty grand last year. Where did the rest go? {claim+ F1 "$60,000"} {question- @+2}
Carl: With respect, I don't know where you heard—
Denise: Brett, the number's on the sheet. It's forty-eight two. {claim- F1}
Brett: Okay, no offense, but people talk. My neighbor was on the board two years ago.
Carl: Two years ago is a different year.
Yolanda: I'm sorry, but can we not start with an accusation? We have a lot to get through. {~}
Brett: I'm not accusing. I'm asking.
Denise: You're both right. Let's look at what's actually left over. Carl? {question- @+1}
Carl: The reserve is twelve thousand six hundred. That's after the spring auction cleared. {claim- F3}
Brett: Twelve six just sitting in an account while the playground is falling apart. {claim- F3}
Carl: A reserve is a reserve. If a fundraiser flops, it covers us.
Yolanda: And the teachers didn't see much of it, for the record.
Denise: How much did the auction actually clear last year? {question- @+1}
Carl: Eight four. Lower than the year before. {claim- F10}
Brett: Eight four for all that work? Honestly, that's depressing. {claim- F10} {~}
Denise: It's a lot of work for that, yes.
Yolanda: Maybe we drop the auction this year. {decision-}
Carl: Let's not drop anything before we've talked fundraising. {decision-}
## fundraising :: What to keep; Denise misstates the fun run and nobody catches it; a drop-off-line rant
Denise: Okay, folks, fundraising. The fun run is our big one. It brought in about twenty-five thousand last year. {claim+ F4 "$25,000"}
Carl: The fun run is the one I'd never touch.
Yolanda: The kids love it, too. It's the one fundraiser that doesn't feel like begging.
Brett: What about a corporate match thing? My company matches donations. {question- @+1}
Denise: Some do. We've never really pushed it.
Carl: It'd be good if somebody made a list of local employers who match. {action-}
Brett: I can— actually, never mind, I'm traveling all of October. {action-}
Denise: And membership? How many families paid dues this year? {question- @+1}
Carl: A hundred and eighty-six. Out of four hundred and twelve kids, so not even half. {claim- F9} {claim- F5}
Yolanda: Half the families don't know what the PTA does. That's the problem.
Brett: Speaking of things nobody knows, has anyone actually timed the drop-off line? It's twenty-five minutes some mornings. {drift+ 5} {~}
Denise: Oh, don't get me started on the drop-off line.
Yolanda: The crossing guard is doing her best, I'm sorry, but it's the parents who won't pull forward.
Brett: Here's the thing, it's the minivans. They stop right in the middle to unload backpacks.
Carl: I drive a minivan.
Denise: Okay, folks, the drop-off line is a whole other meeting. Fundraising.
Yolanda: So do we keep the auction or not? {question- @+3}
Carl: With respect, the auction is the only fundraiser that grandparents give to.
Brett: Then make it smaller. Fewer baskets, better ones.
Denise: Okay, we keep the fun run, we keep the auction but smaller, and we try the corporate match. That's the plan. {decision+}
Yolanda: Fine by me.
Denise: I'll call the three biggest local employers about matching before the next meeting. {action+}
Brett: If you need a script, I'm happy to write one. {action-}
## spending :: Playground vs teacher grants vs buses; Yolanda's number is off and gets corrected later
Denise: Okay, the hard part. Spending. Three big asks. Playground, teacher grants, field trips.
Brett: The playground. The resurfacing quote was twenty-two thousand. {claim- F8}
Carl: Which is more than our entire reserve.
Brett: Then we raise it. That's literally what a PTA is for.
Yolanda: I'm sorry, but teacher grant requests total twelve thousand, and those are for the kids too. {claim+ F6 "$12,000"}
Denise: Twelve thousand in requests, okay. {claim+ F6 "$12,000"}
Brett: Teachers have a district budget. The playground doesn't.
Yolanda: Do you know what the district budget for my classroom is? {~}
Brett: No, I—
Yolanda: Zero. It's zero. I buy the glue sticks.
Denise: Okay, folks, nobody's saying grants don't matter.
Carl: The classroom grant is two hundred per teacher. That part we always fund. {claim- F12}
Yolanda: Two hundred is the floor, not the request. {claim- F12}
Carl: Bear with me, I'm looking at the request sheet. The grant requests add up to nine thousand eight hundred, not twelve. {claim- F6}
Yolanda: Oh. I had the old list with the smartboard request on it.
Denise: Okay, nine eight. And field trips? {question- @+1} {claim- F6}
Yolanda: Buses are six fifty each, and we need about twenty trips. {claim- F7} {~}
Brett: Can the field trips just be cheaper? Like, closer places? {question- @+1}
Yolanda: Closer places are the places they went last year. And the year before.
Denise: What if we fund the grants fully and put the playground in a two-year plan? {question- @+2}
Brett: Two years? My kid will be in middle school. {~}
Carl: With respect, that is fiscally the only thing that works.
Brett: Here's the thing, there's a grant for playgrounds. The county does one. Has anyone applied for it? {question+} {~}
Yolanda: I'm sorry, but the field trips, we haven't settled the field trips.
Denise: Okay. The teacher grants are funded at nine eight. That part's decided. {decision+} {claim- F6}
Yolanda: Thank you. Honestly, thank you.
Brett: And the playground just waits.
Denise: The playground goes into a two-year plan. Maybe we start with half the resurfacing this year. {decision+}
Carl: I'll build a two-year version of the budget with the playground split in half, before the vote. {action+}
Brett: Fine. But I want it on record that I think it's too slow.
Yolanda: Noted, Brett.
## approval :: How the vote works; a date gets corrected; a parked question
Denise: Last thing. How this gets approved. Carl, remind everyone? {question- @+1}
Carl: The board recommends a budget, and then the general membership votes. It's all in the bylaws.
Brett: When's the vote? {question- @+1}
Denise: September twentieth. {claim+ F11 "September 20"}
Carl: Bear with me, it's the twenty-fifth. The twentieth was the original date before the gym conflict. {claim- F11}
Denise: The twenty-fifth. Sorry, folks, it's been a week. {claim- F11}
Brett: Who decided the reserve has to be that big, anyway? {~}
Yolanda: Can members vote by email, or do they have to be there in person? {question- @+1}
Carl: In person or by proxy. It's in the—
Brett: In the bylaws. We know.
Carl: Well, it is.
Denise: Okay. Could someone send the proposed budget to the membership a week before the vote? {question- @+1}
Carl: I'll email the proposed budget to every member family by the eighteenth. {action+}
Brett: Should we do a playground info table at the vote, so people understand the plan? {question+} {~}
Denise: Maybe. Let's see how the two-year version looks first. {decision-}
Yolanda: Sorry, Denise, my son needs help with his math, one second. {drift- 3}
Denise: Go, go, it's fine.
Yolanda: Okay, I'm back. Sorry.
Denise: Okay, folks. I think that's it. Thank you all for coming, even the heated parts.
Brett: Especially the heated parts.
Carl: Goodnight, everyone.
