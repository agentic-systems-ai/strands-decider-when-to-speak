---
meeting_id: wedding-family-d2-s1
theme: Family video call planning a cousin's wedding
domain_pack: family_planning
drama: 0.2
seed: 1
author: claude-opus-5-5 (Claude Code session)
pack:
  title: Amara and Theo's wedding - Sunday family call
  org: The Adeyemi family (fictional)
  agenda:
    - {id: ceremony, title: The ceremony, goal: Settle the time, readings and who walks Amara in, timebox_min: 4}
    - {id: reception, title: Reception and food, goal: Confirm the venue, caterer and cake, timebox_min: 4}
    - {id: travel, title: Travel and lodging, goal: Get the out-of-town guests sorted, timebox_min: 4}
    - {id: tasks, title: Who's doing what, goal: Give every open job a name, timebox_min: 3}
  facts:
    - {id: F1, key: wedding_date, statement: "Wedding date = Saturday, June 21", value: "June 21"}
    - {id: F2, key: ceremony_time, statement: "Ceremony starts at 2:30 pm", value: "2:30 pm"}
    - {id: F3, key: church_capacity, statement: "Church capacity = 120", value: "120"}
    - {id: F4, key: guests_confirmed, statement: "Guests confirmed = 94", value: "94"}
    - {id: F5, key: reception_venue_cost, statement: "Reception hall cost = $6,800", value: "$6,800"}
    - {id: F6, key: cake_tiers, statement: "Cake = 3 tiers", value: "3"}
    - {id: F7, key: caterer_deposit, statement: "Caterer deposit paid = $1,200", value: "$1,200"}
    - {id: F8, key: hotel_rooms_held, statement: "Hotel rooms held = 18", value: "18"}
    - {id: F9, key: hotel_rate, statement: "Hotel group rate = $139 per night", value: "$139"}
    - {id: F10, key: guests_flying_from_lagos, statement: "Guests flying in from Lagos = 9", value: "9"}
    - {id: F11, key: rehearsal_dinner_date, statement: "Rehearsal dinner = Friday, June 20", value: "June 20"}
    - {id: F12, key: photographer_hours, statement: "Photographer booked for 6 hours", value: "6 hours"}
personas:
  - name: Joyce
    role: Mother of the bride, keeps the family organized
    goals: Every guest looked after
    hidden_agenda: Worried the Lagos relatives will feel second-class
    verbosity: 3
    wpm: 150
    catchphrases: ["my dear", "let me see"]
    voice_gender: female
  - name: Amara
    role: The bride
    goals: A relaxed wedding where her family and Theo's mix well
    hidden_agenda: Already decided on her readings and is waiting to be asked
    verbosity: 3
    wpm: 165
    catchphrases: ["Mum", "honestly"]
    voice_gender: female
  - name: Tobi
    role: Cousin, handling travel for the out-of-town guests
    goals: Get everyone from the airport to the hotel
    hidden_agenda: Hasn't booked the airport van yet
    verbosity: 3
    wpm: 170
    catchphrases: ["no wahala", "basically"]
    voice_gender: male
  - name: Ingrid
    role: Theo's grandmother, joining to help with the reception
    goals: Make the Swedish side feel part of it
    hidden_agenda: Wants to bake a traditional cake
    verbosity: 2
    wpm: 125
    catchphrases: ["oh, lovely", "in my day"]
    voice_gender: female
---
## ceremony :: Time and readings; Ingrid misremembers the date, gently corrected
Joyce: Hello, my dear, can you hear us all right, Ingrid? {~}
Ingrid: Oh, lovely, yes, I can hear you. Theo set it up for me. {~}
Joyce: Wonderful. So, the ceremony first. Amara, the time is still half past two? {question- @+1} {claim- F2}
Amara: Half two, yes. The church needed the morning for a christening. {claim- F2}
Ingrid: And that's on the twenty-eighth, isn't it? I have it on my calendar. {claim+ F1 "June 28"} {question- @+1}
Amara: It's the twenty-first, Ingrid. June twenty-first. {claim- F1}
Ingrid: The twenty-first. Oh dear, my calendar is wrong, then. In my day we just remembered. {claim- F1}
Tobi: Basically, the twenty-first is when the Lagos flights land the day before, so it's good. {claim- F1}
Joyce: How many can the church hold, again? {question- @+1}
Amara: A hundred and twenty. We're well under that. {claim- F3}
Joyce: And the readings, my dear? Have you chosen? {question- @+1}
Amara: Honestly, I was hoping someone would ask. I'd like Auntie Bisi to read one, and Ingrid to read the other.
Ingrid: Oh, lovely. In Swedish, or English? {question- @+1}
Amara: Whichever you prefer. Theo said Swedish would make his dad cry.
Ingrid: Then Swedish. I'd be honoured. {action+}
Joyce: Who walks you in, then? Your father, of course. {question- @+1}
Amara: Dad and you, Mum. Both of you. If that's okay.
Joyce: Oh, my dear. Of course it's okay.
Tobi: Basically, there won't be a dry eye in the place.
Joyce: So, Bisi and Ingrid for the readings, and both parents walk Amara in. That's settled, then. {decision+}
Amara: Settled. Thank you.
## reception :: Venue, caterer and cake; Joyce misremembers the deposit; the cake question
Joyce: Let me see, the reception. The hall is booked, and the caterer has the deposit. We paid them two thousand, I think. {claim+ F7 "$2,000"}
Amara: It was twelve hundred, Mum. The rest is due a month before. {claim- F7}
Joyce: Twelve hundred. Yes. I was thinking of the hall. {claim- F7}
Tobi: The hall was sixty-eight hundred, right? {claim- F5} {question- @+1}
Amara: Sixty-eight hundred. Theo's parents are covering half of that. {claim- F5}
Ingrid: About the cake. I wondered whether I might bake a prinsesstårta, for the Swedish side.
Amara: Oh, Ingrid, that would be amazing.
Joyce: But we have the three-tier cake ordered already. {claim- F6}
Ingrid: Mine would be small. Just a little one, next to it.
Tobi: Two cakes is basically the dream.
Joyce: Maybe we could have both. Let me think about where it would go. {decision-}
Amara: Honestly, Mum, there's room. The dessert table is huge.
Joyce: Then yes. The three-tier cake, and Ingrid's cake next to it. Both. {decision+}
Ingrid: Oh, lovely. I'll bake it the morning before and bring it in a tin. {action+}
Tobi: Is the caterer okay with outside food, though? Some of them are funny about it. {question+}
Joyce: Let me see, the menu. Jollof and the Swedish meatballs both, yes? {question- @+1}
Amara: Both. Theo's brother says it's the best idea anyone's had.
Ingrid: In my day, the meatballs were the whole menu.
Tobi: Did Theo ever finish building that canoe, by the way? {drift+ 3} {question- @+1}
Ingrid: Oh, the canoe. It's in my garage. It has been in my garage for three years.
Amara: It leaks. He won't admit it, but it leaks.
Tobi: Okay, okay. Back to the wedding.
## travel :: The Lagos guests, hotel rooms and the airport; Tobi's hotel rate is off and stays off
Joyce: Travel. Tobi, you're our travel person.
Tobi: No wahala. So, nine guests are flying in from Lagos. {claim- F10}
Joyce: Nine. And the hotel? {claim- F10} {question- @+1}
Tobi: We're holding eighteen rooms, at a hundred and nine a night. Not bad. {claim- F8} {claim+ F9 "$109"} {~nc}
Amara: That's good. Is breakfast included? {question- @+1}
Tobi: Basically, yes. Breakfast and parking.
Joyce: Are eighteen rooms enough for everyone coming from away? {question- @+2} {claim- F8}
Tobi: For Lagos, easily. For the cousins from Birmingham, I'm not sure.
Amara: The Birmingham cousins usually stay with Auntie Grace. They told me last week.
Joyce: Then eighteen is fine. And who's collecting the Lagos guests from the airport? They land on the Friday. {claim- F8} {question- @+1}
Tobi: Basically, I was going to sort a van. I just haven't yet. {action-}
Amara: Tobi.
Tobi: I know, I know. I'll book the airport van tomorrow and send everyone the pickup time. {action+}
Joyce: Thank you, my dear. And the rehearsal dinner is the Friday too, isn't it? {question- @+1}
Amara: Friday the twentieth. Same evening they land. {claim- F11}
Ingrid: Will they be too tired, after such a long flight? {question- @+1}
Joyce: Lagos people are never too tired for a party.
Amara: Mum!
Tobi: She's not wrong.
## tasks :: Who's doing what; one job gets an owner, one doesn't
Joyce: Let me see, the jobs that don't have a name yet. The order of service. The photographer timings. The flowers.
Amara: The photographer's booked for six hours. Someone needs to make a shot list. {claim- F12} {action-}
Tobi: Six hours is a lot of photos. {claim- F12}
Amara: Honestly, I'll do the shot list myself. I know who I want in which photo. {action+}
Joyce: And the order of service? {question- @+1}
Ingrid: I used to do the parish newsletter. I could do it, maybe, if someone sends me the words. {action-}
Amara: Oh, Ingrid, you don't have to.
Ingrid: I'd like to. It keeps my hands busy. {action+}
Joyce: The flowers, then. Does anyone know a florist near the church? {question+} {~}
Tobi: Sorry, my brother is shouting about the football. One second. {drift- 1}
Joyce: I think that's us for today, my dears. Same time next Sunday? {question- @+1}
Amara: Same time. Love you, Mum. Thank you, everyone.
Ingrid: Goodbye, my dears.
