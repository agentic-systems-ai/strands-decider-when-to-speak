---
meeting_id: gala-orchestra-d8-s1
theme: Planning committee for a nonprofit's annual fundraising gala
domain_pack: nonprofit_events
drama: 0.8
seed: 1
author: claude-opus-5-5 (Claude Code session)
pack:
  title: Spring gala committee - emergency meeting
  org: Westbrook Youth Orchestra (fictional)
  agenda:
    - {id: sponsor_loss, title: The lost sponsor, goal: Understand what the withdrawal means, timebox_min: 4}
    - {id: budget, title: Budget adjustments, goal: Decide what to cut or change, timebox_min: 5}
    - {id: program, title: Performance program, goal: Settle the student program for the night, timebox_min: 3}
    - {id: tickets, title: Ticket push, goal: Agree how to sell the remaining seats, timebox_min: 3}
  facts:
    - {id: F1, key: gala_date, statement: "Gala date = Saturday, April 12", value: "April 12"}
    - {id: F2, key: lost_sponsorship, statement: "Withdrawn sponsorship = $25,000", value: "$25,000"}
    - {id: F3, key: sponsors_remaining, statement: "Sponsors remaining = 4", value: "4"}
    - {id: F4, key: gala_budget, statement: "Gala budget = $46,000", value: "$46,000"}
    - {id: F5, key: revenue_goal, statement: "Revenue goal = $150,000", value: "$150,000"}
    - {id: F6, key: tickets_sold, statement: "Tickets sold = 188", value: "188"}
    - {id: F7, key: venue_capacity, statement: "Venue capacity = 300", value: "300"}
    - {id: F8, key: ticket_price, statement: "Ticket price = $175", value: "$175"}
    - {id: F9, key: student_performers, statement: "Student performers = 60", value: "60"}
    - {id: F10, key: catering_per_head, statement: "Catering = $85 per head", value: "$85"}
    - {id: F11, key: last_year_net, statement: "Last year's gala netted $112,000", value: "$112,000"}
    - {id: F12, key: scholarships, statement: "Scholarships funded by last year's gala = 22", value: "22"}
personas:
  - name: Celeste
    role: Board chair
    goals: A gala worthy of the orchestra's reputation
    hidden_agenda: The withdrawn sponsor is her brother-in-law's firm
    verbosity: 4
    wpm: 165
    catchphrases: []
    voice_gender: female
  - name: Rafael
    role: Executive director
    goals: Protect the scholarship money
    hidden_agenda: Already drafted a smaller backup plan
    verbosity: 3
    wpm: 150
    catchphrases: ["to be candid"]
    voice_gender: male
  - name: Nkechi
    role: Volunteer gala chair
    goals: Keep the night joyful for the kids
    hidden_agenda: Commuting by train and half-distracted
    verbosity: 3
    wpm: 170
    catchphrases: []
    voice_gender: female
  - name: Howard
    role: Treasurer
    goals: Nobody spends money we don't have
    hidden_agenda: Warned the board about relying on one big sponsor
    verbosity: 2
    wpm: 135
    catchphrases: []
    voice_gender: male
---
## sponsor_loss :: How bad it is; Celeste inflates the loss and gets corrected
Celeste: Thank you for joining at short notice. Hartwell Partners has pulled out. We've lost forty thousand dollars, just like that. {claim+ F2 "$40,000"}
Howard: Twenty-five. Their pledge was twenty-five thousand. I have the letter in front of me. {claim- F2}
Celeste: Twenty-five, forty, it's a catastrophe either way. {claim- F2}
Rafael: To be candid, it's serious, but it isn't a catastrophe. We still have four sponsors. {claim- F3}
Nkechi: Did they say why they pulled out? {question- @+1}
Celeste: Something about a restructuring. I don't know the details.
Nkechi: Does the press know yet? {question+} {~}
Howard: I said at the board retreat that one sponsor was a third of our income. Nobody wanted to hear it. {~}
Celeste: Howard, this isn't the moment for I-told-you-so.
Howard: It's exactly the moment. Otherwise we do it again next year.
Rafael: Can we focus on what we can control? {~}
Nkechi: My train's going into a tunnel, I might cut out for a minute. {drift- 1}
Rafael: What's the revenue goal still, with this hole in it? {question- @+1}
Howard: One hundred and fifty thousand, on paper. Realistically, less. {claim- F5}
Celeste: Last year we netted a hundred and fifty, so the goal is not crazy. {claim+ F11 "$150,000"}
Rafael: The goal stays as it is for now. We'll see where the budget lands. {decision-}
## budget :: Cuts; the catering figure; Rafael's backup plan; a long detour about Vienna
Celeste: The budget. Howard? {question- @+1}
Howard: Forty-six thousand budgeted. We've committed about thirty so far. {claim- F4} {~}
Rafael: The biggest line is catering. It's ninety-five a head. {claim+ F10 "$95"}
Howard: Eighty-five. It's eighty-five a head, with the wine. {claim- F10}
Rafael: Eighty-five. Right, ninety-five was the first quote. {claim- F10}
Celeste: We are not serving people sandwiches at a gala.
Nkechi: Nobody's saying sandwiches. A plated dinner without the third course, maybe? {question- @+1} {decision-}
Celeste: The third course is the dessert. The dessert is the part people remember.
Rafael: Fair enough.
Celeste: When I was in Vienna last spring, the opera ball had seven courses. Seven. {drift+ 4}
Howard: I'm sure it did.
Celeste: And a waltz between every one. The children there learn to waltz at ten.
Nkechi: Our children learn the Bach double concerto at ten. That's better than a waltz.
Rafael: To be candid, I drafted a smaller version of the gala last night, just in case.
Celeste: Of course you did.
Rafael: Same venue, no printed program, digital auction catalog, and the string quartet instead of hiring a band. It saves about nine thousand. {~}
Howard: That's real money.
Celeste: The band was the best part last year.
Nkechi: The kids are the best part. The quartet is the kids.
Celeste: Fine. The quartet, then. And the digital catalog. But we keep the dessert. {decision+}
Howard: I can live with that.
Rafael: I'll send the revised budget to the board tonight. {action+}
Howard: Send it to me first, please. {~}
Rafael: Of course. You first, then the board. {action+}
## program :: The student program; who plays and how long
Nkechi: Sorry, my signal was patchy through all of that. Where did we land? {question- @+1}
Celeste: We cut the band. The quartet will play.
Nkechi: Good. Then the program. Sixty students are performing in total. {claim- F9}
Rafael: Sixty is wonderful, but the program can't run longer than forty minutes. People start leaving. {claim- F9} {~}
Celeste: Is there a way to let every section play something? {question- @+1}
Nkechi: The full orchestra opens, then three short ensembles, then the soloist. Everyone plays at least once.
Howard: Who's the soloist this year? {question- @+1}
Nkechi: Mei-Lin, the cellist. She won the regional competition.
Celeste: Then Mei-Lin closes the program. It's settled. {decision+}
Rafael: Somebody needs to talk to the venue about the stage size for the full orchestra. {action-}
Nkechi: I've measured it twice. It fits if the timpani go stage left.
Howard: Excuse me. Frog in my throat. {drift- 1}
## tickets :: Selling the rest; Nkechi's count is high and is corrected later
Rafael: Tickets. How many have we sold? {question- @+1} {~}
Nkechi: About two hundred and fifty. It's going really well. {claim+ F6 "250"}
Celeste: Excellent. Then we're nearly full.
Howard: Out of three hundred seats. {claim- F7}
Rafael: At a hundred seventy-five a ticket, every remaining seat matters. {claim- F8}
Celeste: Could the parents of the performers sell tickets to their own families? {question- @+2}
Nkechi: They already get two free tickets each. That's part of the problem.
Rafael: Then we ask each family to bring one paying guest. That's the ask. {decision+}
Howard: I have the box office report open. It's a hundred and eighty-eight sold, not two fifty. {claim- F6}
Nkechi: Oh. I counted the free family tickets. Sorry.
Celeste: A hundred and eighty-eight. Then we need that ask more than ever. {claim- F6}
Nkechi: I'll write to all the performer families tomorrow morning about the paying guest. {action+}
Celeste: And mention the scholarships. Twenty-two students last year. {claim- F12}
Howard: Who's going to ask Hartwell if they'd still buy a table? {question+}
Rafael: The date hasn't moved, has it? Still the twelfth? {question- @+1} {claim- F1}
Celeste: April twelfth. It never moves. Thank you all. We'll get through this. {claim- F1}
