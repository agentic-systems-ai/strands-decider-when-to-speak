---
meeting_id: wedding-kowalski-d5-s1
theme: Family video call planning a cousin's wedding
domain_pack: family_planning
drama: 0.5
seed: 1
author: claude-opus-5-5 (Claude Code session)
pack:
  title: Zofia and Marcus's wedding - family call
  org: The Kowalski-Brennan family (fictional)
  agenda:
    - {id: guests, title: Guests and seating, goal: Lock the headcount and start the seating plan, timebox_min: 4}
    - {id: money, title: Money, goal: Be clear about who is paying for what, timebox_min: 4}
    - {id: schedule, title: Rehearsal and the morning, goal: Agree the rehearsal and the wedding-morning schedule, timebox_min: 4}
    - {id: gifts, title: Registry and gifts, goal: Check the registry and the honeymoon fund, timebox_min: 3}
  facts:
    - {id: F1, key: wedding_date, statement: "Wedding date = Saturday, September 6", value: "September 6"}
    - {id: F2, key: guest_count, statement: "Confirmed guests = 136", value: "136"}
    - {id: F3, key: venue_deposit, statement: "Venue deposit paid = $3,000", value: "$3,000"}
    - {id: F4, key: total_budget, statement: "Total wedding budget = $24,000", value: "$24,000"}
    - {id: F5, key: parents_contribution, statement: "Bride's parents' contribution = $10,000", value: "$10,000"}
    - {id: F6, key: bar_per_head, statement: "Bar package = $32 per head", value: "$32"}
    - {id: F7, key: tables, statement: "Reception tables = 14", value: "14"}
    - {id: F8, key: rehearsal_time, statement: "Rehearsal starts at 5:00 pm on Friday", value: "5:00 pm"}
    - {id: F9, key: hair_makeup_start, statement: "Hair and makeup start at 8:30 am", value: "8:30 am"}
    - {id: F10, key: registry_items_left, statement: "Registry items still unclaimed = 23", value: "23"}
    - {id: F11, key: honeymoon_fund, statement: "Honeymoon fund raised = $1,850", value: "$1,850"}
    - {id: F12, key: photographer_arrival, statement: "Photographer arrives at 1:00 pm", value: "1:00 pm"}
personas:
  - name: Agnieszka
    role: Bride's aunt, the family organizer
    goals: A schedule that runs to the minute
    hidden_agenda: Feels her sister leaves everything to her
    verbosity: 4
    wpm: 160
    catchphrases: []
    voice_gender: female
  - name: Patrick
    role: Bride's father
    goals: Pay his share and not a cent more
    hidden_agenda: Quietly worried about money after a rough year
    verbosity: 2
    wpm: 140
    catchphrases: []
    voice_gender: male
  - name: Zofia
    role: The bride
    goals: Get through planning without a family fight
    hidden_agenda: Marcus's mother keeps adding guests
    verbosity: 3
    wpm: 170
    catchphrases: ["okay so"]
    voice_gender: female
  - name: Danny
    role: Cousin and groomsman
    goals: Help, and be funny while doing it
    hidden_agenda: Lost the groomsmen's suit fitting receipt
    verbosity: 4
    wpm: 180
    catchphrases: []
    voice_gender: male
---
## guests :: The headcount; Danny inflates it and nobody checks; seating starts; a fantasy football tangent
Agnieszka: Okay, everyone is here. Zofia, the guest list first, because the venue wants numbers.
Zofia: Okay so, we're at a hundred and thirty-six confirmed. {claim- F2}
Patrick: That's more than we said.
Zofia: Marcus's mom keeps adding people. Every week there's a new second cousin.
Agnieszka: Maybe we cap it somewhere and tell her, politely. {decision-}
Danny: A hundred and fifty, give or take. It's going to be a party. {claim+ F2 "150"}
Agnieszka: And how many tables does that mean? {question- @+1}
Zofia: Fourteen tables, ten at each, and a few spare seats. {claim- F7}
Patrick: Fourteen tables. When I got married there were six. {claim- F7}
Danny: When you got married, Uncle Pat, there were also no phones.
Agnieszka: The seating plan. Where do the Brennan grandparents go? {question- @+1}
Zofia: Near the front, but not near the speakers. Grandpa's hearing aid squeals.
Danny: Also, my fantasy league is a disaster. I'm last. {drift+ 3}
Patrick: I don't know what that is.
Danny: It's like gambling, but with spreadsheets and no money.
Agnieszka: Danny. Seating.
Zofia: I'll do a first draft of the seating chart this weekend and share it. {action+}
Agnieszka: Put Marcus's mother where she can see everything. It'll keep her calm.
Zofia: That's actually smart.
## money :: Who pays what; Patrick overstates his contribution and the room goes quiet
Agnieszka: Money. I know nobody wants to, but we have to.
Patrick: Your mother and I put in fifteen thousand. That's our part. {claim+ F5 "$15,000"}
Zofia: Dad. It was ten. We talked about it at Easter. {claim- F5}
Patrick: Ten. Yes. Ten. I'm sorry, I was thinking of what we'd hoped. {claim- F5}
Danny: Awkward.
Agnieszka: The total budget is twenty-four thousand. So the rest is Zofia and Marcus, and his parents. {claim- F4}
Zofia: And we already paid the three thousand deposit for the venue. {claim- F3}
Patrick: What's the bar going to cost? {question- @+1}
Zofia: Thirty-two a head for the package. {claim- F6}
Patrick: Thirty-two times a hundred and thirty-six. That's a lot of beer. {claim- F6} {claim- F2}
Danny: It's not just beer, it's also wine.
Agnieszka: Could we do a cash bar after ten o'clock? Lots of weddings do. {question- @+2}
Patrick: I'd rather that than a bill nobody can pay.
Zofia: Okay so, open bar until ten, then cash bar. That's fine. {decision+}
Danny: Who's paying for the rehearsal dinner, by the way? {question+} {~}
Agnieszka: Patrick, are you okay? You've gone quiet. {question- @+1}
Patrick: I'm fine. It's been a long year, that's all.
## schedule :: The rehearsal and the morning; Agnieszka gets the rehearsal time wrong and fixes it later
Agnieszka: The schedule. The rehearsal on Friday is at six. {claim+ F8 "6:00 pm"}
Danny: Six works for me. I finish work at five. {claim+ F8 "6:00 pm"}
Zofia: And the morning? What time do we start? {question- @+1}
Agnieszka: Hair and makeup at eight thirty, at the hotel. {claim- F9}
Zofia: Eight thirty is so early. Maybe we push it to nine? {claim- F9} {decision-} {question- @+1}
Agnieszka: Eight thirty is late. The photographer comes at one, and you need to be dressed by then. {claim- F9} {claim- F12}
Danny: Is the photographer the guy with the drone? {question- @+1}
Zofia: No drone. I said no drone.
Danny: What do the groomsmen do in the morning? Anything? {question- @+1}
Agnieszka: You collect the suits by nine and you're at the church by one thirty. Sober. {~nc}
Danny: About the suits. I may have lost the fitting receipt.
Zofia: Danny!
Danny: I know the shop! They know me! It's fine. I'll go in Thursday and sort it out with them. {action+}
Patrick: My cat has a vet appointment that Thursday, actually. Surgery on her paw. {drift+ 3}
Zofia: Oh no, poor Pierogi. Is she okay? {question- @+1}
Patrick: She'll be fine. She's tougher than me.
Agnieszka: I'm looking at the booking email. The rehearsal is at five, not six. Sorry, I had the dinner time in my head. {claim- F8}
Danny: Five. Then I'll leave work early. {claim- F8} {action+}
Agnieszka: Rehearsal at five, dinner at six thirty, and nobody is late. {decision+} {~} {claim- F8}
## gifts :: The registry and the honeymoon fund
Zofia: The registry. There are like forty things still left on it. {claim+ F10 "40"}
Agnieszka: I checked last night, it's twenty-three. People bought a lot this week. {claim- F10}
Zofia: Oh, nice. Twenty-three. {claim- F10}
Patrick: Has anyone heard whether Aunt Halina is actually coming? {question+}
Danny: And the honeymoon fund? How's that going? {question- @+1}
Zofia: Eighteen fifty so far. Enough for the flights, almost. {claim- F11}
Patrick: Is my picture frozen? I see myself upside down. {drift- 2} {~}
Danny: You're fine, Uncle Pat. You're just upside down.
Agnieszka: Someone should remind the Polish side about the registry. They don't use the internet much. {action-}
Patrick: I'll call my brother on Sunday and tell him. He'll tell everyone else. {action+}
Zofia: Thank you, Dad.
Danny: Does anyone know if the date is on the invitations right? I keep getting asked if it's the sixth or the seventh. {question- @+1}
Zofia: It's the sixth. September sixth. It's on the invitations. {claim- F1}
Agnieszka: Then we're done. Next call in two weeks. Same time.
Danny: Same bat time, same bat channel.
Patrick: I don't know what that means either.
