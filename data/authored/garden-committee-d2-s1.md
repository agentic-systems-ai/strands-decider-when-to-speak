---
meeting_id: garden-committee-d2-s1
theme: "Community garden committee: plots, water and the spring fair"
domain_pack: community_group
drama: 0.2
seed: 1
author: claude-opus-5-5 (Claude Code session)
pack:
  title: Garden committee - March meeting
  org: Elm Street Community Garden (fictional)
  agenda:
    - {id: plots, title: Plots and the waitlist, goal: Reassign abandoned plots and work through the waitlist, timebox_min: 4}
    - {id: water, title: Water system and the bill, goal: Understand the water bill and decide on the spring repairs, timebox_min: 4}
    - {id: spring_fair, title: Spring fair, goal: Confirm vendors, volunteers and the layout, timebox_min: 4}
    - {id: rules, title: Garden rules, goal: Agree what to do about unattended plots and shared tools, timebox_min: 3}
  facts:
    - {id: F1, key: total_plots, statement: "Total plots = 64", value: "64"}
    - {id: F2, key: waitlist_count, statement: "People on the waitlist = 29", value: "29"}
    - {id: F3, key: annual_plot_fee, statement: "Annual plot fee = $45", value: "$45"}
    - {id: F4, key: water_bill_last_year, statement: "Water bill last year = $1,870", value: "$1,870"}
    - {id: F5, key: water_rate_increase, statement: "City water rate increase this year = 12%", value: "12%"}
    - {id: F6, key: abandoned_plots, statement: "Plots abandoned last season = 7", value: "7"}
    - {id: F7, key: spring_fair_date, statement: "Spring fair = Saturday, April 26", value: "April 26"}
    - {id: F8, key: fair_vendor_slots, statement: "Vendor slots at the fair = 18", value: "18"}
    - {id: F9, key: shed_insurance, statement: "Tool shed insurance = $320 a year", value: "$320"}
    - {id: F10, key: compost_deliveries, statement: "Compost deliveries per season = 3", value: "3"}
    - {id: F11, key: bank_balance, statement: "Garden bank balance = $4,150", value: "$4,150"}
    - {id: F12, key: lease_renewal, statement: "City lease renewal due June 30", value: "June 30"}
personas:
  - name: Ruth
    role: Committee chair, retired teacher
    goals: A calm season and a full garden
    hidden_agenda: Worried the city won't renew the lease
    verbosity: 3
    wpm: 140
    catchphrases: ["now then", "lovely"]
    voice_gender: female
  - name: Hector
    role: Volunteer who looks after the water system
    goals: Fix the leaking main line before summer
    hidden_agenda: Has been paying for small parts himself
    verbosity: 2
    wpm: 145
    catchphrases: ["the thing with water is"]
    voice_gender: male
  - name: Mina
    role: Plot and waitlist coordinator
    goals: Get waitlisted families into plots
    hidden_agenda: Her friend is next on the waitlist
    verbosity: 3
    wpm: 160
    catchphrases: ["so basically", "honestly"]
    voice_gender: female
  - name: Sam
    role: Organizes the spring fair
    goals: A fair that pays for the water bill
    hidden_agenda: Wants to add a food truck the others may not like
    verbosity: 3
    wpm: 170
    catchphrases: ["super quick", "totally"]
    voice_gender: male
---
## plots :: Abandoned plots and the waitlist; Ruth overstates the waitlist and Mina corrects it gently
Ruth: Now then, let's get started. Plots first. Mina, how does it look? {question- @+1}
Mina: So basically, seven plots were abandoned last season. Nobody touched them after July. {claim- F6}
Ruth: Seven. That's more than usual. And the waitlist must be, what, forty people by now? {claim+ F2 "40"} {question- @+1} {claim- F6}
Mina: Honestly, it's twenty-nine. It feels like more because people email twice. {claim- F2}
Ruth: Twenty-nine. Still a lot of people waiting. {claim- F2}
Sam: Do the abandoned plots go straight to the waitlist? {question- @+1}
Mina: That's the rule. First come, first served.
Hector: The thing with those plots is, some of them are a real mess. Bindweed everywhere.
Ruth: Should we clear them before handing them over? {question- @+1}
Mina: It would be kinder. Nobody wants to start with a jungle.
Sam: Totally. Could we do a work day for it? {question- @+1}
Ruth: A work day sounds lovely. Maybe the first Saturday in April? {decision-} {question+} {~nc}
Hector: I'd come, but my back might not.
Mina: I'll email the next seven people on the waitlist this week and offer them the plots. {action+}
Ruth: Lovely. Will they pay the full fee, joining this late? {question- @+1}
Mina: The fee's forty-five for the year. We've always charged it in full. {claim- F3}
Sam: Forty-five is pretty cheap honestly, for a whole season. {claim- F3}
Ruth: Then the seven abandoned plots go to the next seven on the waitlist, full fee. That's settled. {decision+} {claim- F6}
Mina: Great.
## water :: The bill is going up; Hector's percentage is off and nobody notices; the main line repair
Ruth: Now then, water. Hector? {question- @+1}
Hector: The thing with water is, it's our biggest cost. Last year the bill was eighteen seventy. {claim- F4}
Sam: And it's going up this year? {question- @+1}
Hector: The city put the rate up about twenty percent. {claim+ F5 "20%"}
Ruth: Twenty percent. Goodness. {claim+ F5 "20%"}
Mina: So basically, the plot fees don't even cover the water anymore.
Hector: And the main line is leaking near the shed. Every drip is money.
Sam: How much would it cost to fix the leak properly? {question- @+1}
Hector: A plumber quoted me a few hundred. I could do it myself for less, with a helper. {~}
Ruth: Do we have the money for that? {question- @+1}
Sam: Super quick, the bank balance is forty-one fifty. So yes, we can cover a repair. {claim- F11}
Ruth: Then let's not wait. It would be good if somebody found Hector a helper. {action-}
Mina: My neighbor is a retired plumber, actually. He's very bored.
Hector: A bored plumber is the best kind of plumber.
Ruth: Mina, could you ask your neighbor if he'd help Hector on the main line? {question- @+1}
Mina: Of course. I'll ask him tonight and put him in touch with Hector. {action+}
Ruth: Lovely. Then we fix the main line before the season starts, and the garden pays for parts. Agreed. {decision+}
Hector: Thank you. I've been buying the washers myself, honestly.
Ruth: Hector! You should have said.
Hector: It's only a few dollars here and there. {~}
Sam: Has anyone looked at whether rain barrels would help with the bill? {question+} {~}
Ruth: Now then, the fair.
## spring_fair :: Vendors, the date, a food truck idea; a detour into the high school's football season
Sam: Super quick, so, the fair. It's Saturday, April twenty-sixth. {claim- F7}
Ruth: Lovely. And the vendors? {question- @+1}
Sam: We have eighteen vendor slots, and fourteen are already taken. {claim- F8} {~}
Mina: That's great for this early.
Sam: I also had an idea. What if we had a food truck this year? The taco place on Fifth said they'd come. {question- @+11}
Hector: A food truck in a garden? {~}
Ruth: Hm. I'd want to think about that. The bake sale has always been the food. {decision-}
Mina: Honestly, people would love tacos. The bake sale sells out by noon anyway.
Sam: They'd pay a vendor fee, too, like everyone else.
Ruth: Maybe we try it this year and see. {decision-}
Hector: My grandson's team made the playoffs, by the way. The game's that same weekend. {drift+ 3}
Mina: Oh, congratulations! Is he still playing quarterback? {question- @+1}
Hector: Linebacker now. He likes hitting people more than throwing, apparently.
Ruth: Now then, we were on the fair.
Sam: So, food truck or no food truck? {question- @+1}
Ruth: Food truck, this year, as a trial. If the bake sale people are upset, we revisit. Decided. {decision+}
Sam: Totally. I'll confirm with the taco place and send them the vendor form this week. {action+}
Mina: Do we need more volunteers for the day? {question- @+1}
Sam: Probably four or five more, for setup and the plant sale table. {~}
Mina: We could really use a sign-up sheet on the shed door. {action-}
## rules :: Unattended plots and the shared tools; the lease question hangs in the air
Ruth: Last item. The rules. The unattended plots, and the tools.
Mina: So basically, we should say what counts as abandoned. Last year it was a judgment call.
Hector: Six weeks with no watering. That's what most gardens use. {~}
Ruth: Six weeks feels fair. Should we put it in the rules? {question- @+1}
Sam: Totally. And send a warning email at four weeks, so it's not a surprise. {~}
Mina: Could we vote on it at the spring members' meeting rather than deciding here? {decision-} {question- @+1}
Ruth: That's probably right. It affects everyone.
Sam: Sorry, my phone's buzzing, it's my sister. Ignore me. {drift- 1}
Hector: The tools. Somebody keeps leaving the good shovel out in the rain.
Sam: It's not me, for the record.
Mina: It's absolutely not me.
Hector: I'm not accusing anybody. I'd just like a hook by the door with a sign.
Ruth: Hector, would you put up a hook and a sign? {question- @+1}
Hector: Happy to. I'll put up the hook and a sign by the shed door this weekend. {action+}
Ruth: Lovely. And the lease. The city renewal is due June thirtieth. {claim- F12}
Mina: Have we heard anything from the city about it? {question+} {~}
Ruth: Now then, I think that's everything for tonight. Thank you, everyone.
Sam: Thanks, Ruth.
Hector: Goodnight.
