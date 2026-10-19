---
meeting_id: wedding-family-d8-s1
theme: Family video call planning a cousin's wedding
domain_pack: family_planning
drama: 0.8
seed: 1
author: claude-opus-5-5 (Claude Code session)
pack:
  title: Nina and Sam's wedding - family planning call
  org: The Alvarez family (fictional)
  agenda:
    - {id: guest_list, title: Guest list and RSVPs, goal: Get a real headcount and chase missing RSVPs, timebox_min: 4}
    - {id: venue_catering, title: Venue and catering, goal: Confirm the venue numbers and the catering order, timebox_min: 4}
    - {id: budget, title: Budget check, goal: See where we are against the budget and what to cut, timebox_min: 4}
    - {id: day_logistics, title: Wedding day logistics, goal: Shuttle, hotel rooms and the day's schedule, timebox_min: 4}
  facts:
    - {id: F1, key: venue_deposit_paid, statement: "Venue deposit paid = $4,500", value: "$4,500"}
    - {id: F2, key: confirmed_rsvps, statement: "Confirmed RSVPs so far = 112", value: "112"}
    - {id: F3, key: invited_guests, statement: "Guests invited = 160", value: "160"}
    - {id: F4, key: catering_per_head, statement: "Catering cost per head = $68", value: "$68"}
    - {id: F5, key: total_budget, statement: "Total wedding budget = $32,000", value: "$32,000"}
    - {id: F6, key: venue_capacity, statement: "Venue seated capacity = 140", value: "140"}
    - {id: F7, key: rsvp_deadline, statement: "RSVP deadline = May 15", value: "May 15"}
    - {id: F8, key: wedding_date, statement: "Wedding date = Saturday, August 9", value: "August 9"}
    - {id: F9, key: shuttle_seats, statement: "Shuttle seats booked = 48", value: "48"}
    - {id: F10, key: hotel_block_rooms, statement: "Hotel room block = 25 rooms", value: "25"}
    - {id: F11, key: dj_quote, statement: "DJ quote = $1,800", value: "$1,800"}
    - {id: F12, key: ceremony_start, statement: "Ceremony starts at 4:00 pm", value: "4:00 pm"}
personas:
  - name: Carmen
    role: Mother of the bride, runs the call
    goals: Everything perfect, nobody offended
    hidden_agenda: Wants to invite her whole church group
    verbosity: 5
    wpm: 170
    catchphrases: ["mija", "listen, listen"]
    voice_gender: female
  - name: Nina
    role: The bride
    goals: Keep it small and on budget
    hidden_agenda: Quietly wants to drop the formal dinner for a taco truck
    verbosity: 3
    wpm: 160
    catchphrases: ["Mom", "can we not"]
    voice_gender: female
  - name: Dani
    role: Nina's sister, keeps the spreadsheet
    goals: Make the numbers add up
    hidden_agenda: Has been covering small costs out of pocket
    verbosity: 2
    wpm: 150
    catchphrases: ["per the spreadsheet", "okay but"]
    voice_gender: female
  - name: Leo
    role: Cousin, in charge of music and the shuttle
    goals: Be helpful without doing paperwork
    hidden_agenda: Already promised his band could play a set
    verbosity: 4
    wpm: 180
    catchphrases: ["dude", "no for sure"]
    voice_gender: male
---
## guest_list :: Carmen inflates the RSVP count; Nina pushes back on new invites
Carmen: Can everyone hear me? Leo, you're frozen. {~}
Leo: No, I'm here, I'm here, the camera's just being weird.
Carmen: Okay, listen, listen, we have a lot to get through, so the guest list first.
Nina: Mom, can we please keep it to the list this time.
Carmen: I am keeping it to the list! So we have a hundred and fifty yeses already, that's wonderful. {claim+ F2 "150"}
Dani: Per the spreadsheet it's a hundred and twelve confirmed. {claim- F2}
Carmen: That can't be right, everybody I talk to is coming.
Dani: Everybody you talk to isn't the same as everybody who's sent the card back.
Nina: And we invited a hundred and sixty total, so a hundred and fifty would be wild anyway. {claim- F3}
Leo: Dude, people always say yes in person and then never RSVP.
Carmen: So who hasn't sent it back? {question- @+1}
Dani: Mostly Dad's side, and the cousins in Phoenix.
Carmen: The Phoenix cousins always do this.
Leo: To be fair the Phoenix cousins don't check their mail. Like, ever.
Nina: When's the deadline again? {question- @+1}
Dani: May fifteenth. {claim- F7}
Carmen: That's so soon!
Nina: Which is why we're talking about it, Mom.
Dani: I'll text every Phoenix cousin individually tonight and get a yes or no. {action+}
Nina: Thank you. Seriously.
Carmen: And then the church group. I was thinking we could—
Nina: Mom, no. We talked about this.
Carmen: Just a few of them! Marisol and her husband, and the Ortegas.
Nina: That's how it started last time and it turned into forty people.
Leo: No for sure, church people travel in packs.
Carmen: That is not a nice thing to say about my friends.
Leo: I'm saying it with love!
Dani: Okay but, does adding the Ortegas actually fit under the venue limit? {question+} {~}
Carmen: The Ortegas are very small people.
Dani: Mom. The venue seats a hundred and forty, it's not about how much room they take up. {claim- F6}
Nina: Maybe we just say no plus-ones for anyone we haven't met? {decision-} {question- @+1}
Carmen: You can't do that to people, it's rude.
Leo: It's kind of normal now, though.
Nina: Fine, let's think about it and come back to it. {decision-}
Leo: Somebody should really call Tía Lupe about her plus-one, she's been asking. {action-}
## venue_catering :: Numbers for the venue and the catering order; Nina's taco truck idea
Carmen: Okay, the venue. Dani, what did we pay them already? {question- @+1}
Dani: The deposit was four and a half thousand. {claim- F1}
Leo: That's a lot for a deposit.
Carmen: Everything is a lot, mijo, it's a wedding.
Dani: And the catering is sixty-eight a head, so the headcount really matters. {claim- F4}
Carmen: Sixty-eight? I thought they said fifty-five. {claim+ F4 "$55"} {question- @+1}
Dani: That was the buffet price. We went with the plated dinner.
Carmen: Because the plated dinner is elegant.
Nina: Can I just float something? What if we didn't do the plated dinner at all? {question- @+1}
Carmen: What would people eat, air? {~}
Nina: A taco truck. Two, maybe. People love it, and it's way cheaper.
Carmen: At a wedding? Your grandmother would— {~}
Nina: Grandma would love a taco truck, Mom, she literally goes to one every Sunday.
Leo: Dude, this is the best idea anyone's had so far.
Dani: Okay but, has anyone asked the venue if outside food trucks are even allowed? {question- @+3}
Carmen: They won't allow it, a place like that.
Leo: My buddy did that at a winery and it was totally fine.
Nina: I actually emailed them yesterday. They allow it with a fee.
Carmen: You emailed them without telling me? {~}
Nina: I'm the bride, Mom. I'm allowed to email my own venue.
Dani: How much is the fee? {question- @+1}
Nina: They didn't say yet, they said they'd send a sheet.
Carmen: Speaking of Grandma, did you hear about her hip? {drift+ 6} {question- @+1}
Leo: Wait, what happened to her hip? {question- @+1} {~}
Carmen: She was dancing at the Garcias' anniversary and she went down like a tree.
Dani: Is she okay? {question- @+1}
Carmen: She's fine, she's fine, but now she says the doctor is too young to know anything.
Leo: Classic Grandma. She told my doctor he looked twelve.
Nina: Okay, can we, the catering. We need to tell them something this week.
Carmen: Fine. We keep the plated dinner for now. {decision-}
Nina: For now. I'm not dropping the taco truck.
Dani: I'll call the venue tomorrow and get the food truck fee in writing. {action+}
Leo: And then we vote? {question- @+1}
Carmen: There's no vote, I'm paying for a lot of it.
Dani: Per the spreadsheet, that's not quite true either, Mom.
## budget :: Where the money is; a quote misremembered; the DJ fight
Carmen: Okay, the budget. How bad is it? {question- @+1}
Dani: Not bad yet. Total budget is thirty-two thousand, and we've committed about two thirds. {claim- F5}
Carmen: I thought we said thirty-five. {claim+ F5 "$35,000"}
Nina: It was always thirty-two, Mom. Thirty-five was your number, not ours. {claim- F5}
Carmen: My number is a perfectly good number.
Leo: Sorry, sorry, my cat just walked across the keyboard. {drift- 2}
Nina: Hi, Mango.
Leo: Okay, so, the DJ. I got the quote back and it's like twelve hundred. {claim+ F11 "$1,200"}
Dani: The quote you sent me says eighteen hundred, Leo. {claim- F11}
Leo: Oh. That's, okay, yeah, eighteen hundred. I was thinking of the other guy. {claim- F11}
Nina: Eighteen hundred for a DJ? {claim- F11} {~}
Leo: Honestly, my band could do it for way less. Like, basically free.
Nina: Leo.
Leo: What! It's a good band!
Carmen: Is this the band that played at the quinceañera? {question- @+1}
Leo: Different drummer now. Much better drummer.
Dani: Okay but, are we booking the DJ or not? The quote expires Friday. {question- @+4}
Nina: I want a DJ. I love you, Leo, but I want a DJ.
Leo: Maybe the band does like one set during cocktails? {decision-} {question- @+1}
Carmen: That could be nice, actually.
Nina: Fine. We book the DJ at eighteen hundred, and Leo's band plays the cocktail hour. Done. {decision+} {claim- F11}
Leo: Yes! Okay, I'll book the DJ myself today and send Dani the contract. {action+}
Dani: Thank you. Band at zero dollars, noted.
Leo: Zero is harsh.
Carmen: Zero is generous.
Dani: Has anyone figured out what we do if the RSVPs blow past the venue limit? {question+} {~}
Carmen: Listen, the flowers. The florist wants a final count of centerpieces.
Nina: We should probably cut the flowers back, they're a huge chunk. {decision-}
Carmen: Weddings need flowers, mija.
Nina: Weddings need people, Mom. Flowers are optional.
## day_logistics :: Shuttle seats, hotel rooms and timing; a schedule mix-up gets corrected
Carmen: Okay, last thing, the day itself. Leo, the shuttle.
Leo: So the shuttle has forty-eight seats booked, and it does two runs from the hotel. {claim- F9}
Carmen: Two runs is enough? {question- @+1}
Leo: Two runs covers basically everyone who isn't driving.
Dani: And the hotel block is twenty-five rooms. {claim- F10}
Carmen: Twenty-five. Half of Phoenix is going to need a room. {claim- F10}
Leo: Somebody needs to sort out parking for the older relatives, too. {action-}
Nina: Half of Phoenix hasn't RSVP'd, Mom.
Leo: Wait, what time does the ceremony actually start? I told the shuttle three. {question- @+1} {~}
Carmen: Three o'clock, like always. {claim+ F12 "3:00 pm"}
Dani: It's four. It's been four since we booked the venue. {claim- F12}
Leo: Oh no. Okay. Okay, that's fixable.
Nina: Leo.
Leo: Fine. I'll call the shuttle company tomorrow morning and move both runs an hour later. {action+}
Carmen: And it's still Saturday the ninth, right? Nobody moved the date while I wasn't looking? {question- @+1} {claim- F8}
Nina: August ninth. Nobody moved anything. {claim- F8}
Carmen: Good. Your uncle already booked his flights.
Dani: Do we need a rain plan for the ceremony? It's outside. {question- @+1}
Nina: The venue has a tent option. It's an extra cost, though.
Carmen: Then we get the tent. I'm not watching my daughter get married in a storm. {decision-}
Nina: Mom, it's August. {~nc}
Carmen: August has storms! {~nc}
Dani: Okay. We're going with the tent. Final. {decision+}
Leo: Who's doing the welcome speech at the dinner? {question+} {~}
Carmen: Okay, I think that's everything. I love you all. This is going to be beautiful.
Nina: Love you, Mom. Thanks everyone.
Leo: Peace!
Dani: Bye, everyone.
