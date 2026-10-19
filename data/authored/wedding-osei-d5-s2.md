---
meeting_id: wedding-osei-d5-s2
theme: Family video call planning a cousin's wedding
domain_pack: family_planning
drama: 0.5
seed: 2
author: claude-opus-5-5 (Claude Code session)
pack:
  title: Efua and Liam's wedding - family call
  org: The Osei-Murphy family (fictional)
  agenda:
    - {id: ceremonies, title: The two ceremonies, goal: Settle the engagement ceremony and the church wedding plans, timebox_min: 4}
    - {id: guests_travel, title: Guests and travel, goal: Track the visas and the flights from Accra, timebox_min: 4}
    - {id: food, title: Food, goal: Agree the menu across both families, timebox_min: 4}
    - {id: budget, title: Budget, goal: Check the big costs against the budget, timebox_min: 3}
  facts:
    - {id: F1, key: engagement_date, statement: "Traditional engagement ceremony = July 12", value: "July 12"}
    - {id: F2, key: church_date, statement: "Church wedding = July 19", value: "July 19"}
    - {id: F3, key: guests_expected, statement: "Guests expected = 180", value: "180"}
    - {id: F4, key: visa_applications, statement: "Visa applications from Ghana = 11", value: "11"}
    - {id: F5, key: visas_approved, statement: "Visas approved so far = 6", value: "6"}
    - {id: F6, key: caterer_quote, statement: "Caterer quote = $9,400", value: "$9,400"}
    - {id: F7, key: kente_yards, statement: "Kente cloth ordered = 14 yards", value: "14"}
    - {id: F8, key: budget, statement: "Total budget = $35,000", value: "$35,000"}
    - {id: F9, key: hall_capacity, statement: "Hall capacity = 200", value: "200"}
    - {id: F10, key: flight_cost, statement: "Flight from Accra = about $1,350 return", value: "$1,350"}
    - {id: F11, key: photographer_deposit, statement: "Photographer deposit = $800", value: "$800"}
    - {id: F12, key: rsvp_deadline, statement: "RSVP deadline = May 31", value: "May 31"}
personas:
  - name: Abena
    role: Mother of the bride
    goals: Both ceremonies done properly
    hidden_agenda: Invited more of her church than she has admitted
    verbosity: 4
    wpm: 160
    catchphrases: []
    voice_gender: female
  - name: Yaw
    role: Bride's uncle, handling the Ghana side
    goals: Get every relative a visa in time
    hidden_agenda: Lending money to two cousins for their flights
    verbosity: 3
    wpm: 150
    catchphrases: []
    voice_gender: male
  - name: Efua
    role: The bride
    goals: Keep both families happy and the budget sane
    hidden_agenda: Would elope if she could
    verbosity: 3
    wpm: 170
    catchphrases: []
    voice_gender: female
  - name: Declan
    role: The groom's brother
    goals: Make the Irish side feel welcome
    hidden_agenda: Has never been to a Ghanaian engagement and is nervous
    verbosity: 3
    wpm: 175
    catchphrases: []
    voice_gender: male
---
## ceremonies :: The engagement and the church; Declan's questions
Efua: Hi, everyone. Can we start with the two ceremonies? Declan has questions. {~}
Declan: I do. The engagement is the twelfth, the church is the nineteenth? {claim- F1} {claim- F2} {question- @+1}
Abena: Yes. July twelfth for the engagement at the house, July nineteenth for the church. {claim- F1} {claim- F2}
Declan: And what do I wear to the engagement? I don't want to get it wrong. {question- @+1}
Abena: Kente, if you can. We ordered fourteen yards, so there is cloth for Liam's side too. {claim- F7}
Declan: Oh, that's very kind. Mam will cry.
Yaw: The engagement has a lot of steps. Someone from Liam's side has to speak for the family.
Declan: Speak? Me? {~}
Yaw: Or your father. Someone who can say yes, the family agrees.
Declan: Dad will do it. He loves a speech. I'll tell him tonight. {action+}
Efua: Thank you. The engagement is at the house, the wedding is at the church, and nobody changes that now. {decision+} 
Declan: Got it.
## guests_travel :: Visas and flights; Yaw's visa count is high; Declan's flight number stands
Efua: Guests and travel. Uncle Yaw? {question- @+1}
Yaw: We had eleven visa applications from Ghana, and nine are approved. {claim- F4} {claim+ F5 "9"}
Abena: Nine! That's wonderful. {claim+ F5 "9"}
Efua: The tracker says six approved, Uncle. Three are still waiting for interviews. {claim- F5}
Yaw: Six. Yes, the other three have their interviews next week. {claim- F5}
Declan: How much are the flights from Accra? {question+} {~}
Yaw: They're expensive in July. {~nc}
Declan: I looked it up for curiosity. About nine hundred return, I think. {claim+ F10 "$900"}
Abena: And the RSVPs? The deadline is the end of May. {claim- F12} {question- @+1}
Efua: Most people have replied. We're expecting about a hundred and eighty. {claim- F3}
Abena: My church alone is a hundred. {~}
Efua: Mum. The hall holds two hundred. {claim- F9}
Abena: I'm only saying.
Yaw: Could someone help the three cousins with their interview paperwork? {question- @+1}
Efua: I'll call each of them on Sunday and go through the forms. {action+} 
Yaw: Thank you, Efua.
## food :: Two families, one menu; a little detour about a hurling match
Efua: Food. The caterer can do both jollof and a roast.
Declan: Jollof and a roast. That's the best of both worlds.
Abena: And waakye at the engagement. That's not negotiable.
Efua: Fine, Mum. Waakye at the engagement. {decision+}
Declan: Dad's going to be gutted, Kilkenny lost the hurling final on Sunday. He'll need cheering up. {drift+ 3}
Yaw: Hurling is the one with the sticks? {question- @+1}
Declan: The fastest game on grass. It's like hockey crossed with a war.
Efua: The menu, people.
Abena: Will there be enough vegetarian food? Liam's mother doesn't eat meat. {question- @+1}
Efua: The caterer has a vegetable stew and a mushroom roast.
Abena: Then that's the menu. Jollof, the roast, waakye at the engagement, and the vegetarian dishes. {decision+} {~}
## budget :: The big costs; Abena's guest number contradicts the plan, corrected later
Efua: Budget. The total is thirty-five thousand. {claim- F8}
Yaw: The caterer quote is ninety-four hundred. That's the biggest single line. {claim- F6}
Abena: For two hundred and fifty people, that's a good price. {claim+ F3 "250"}
Declan: Is it two fifty? I thought Efua said a hundred and eighty. {question- @+1} {claim- F3} {~}
Efua: A hundred and eighty, Mum. The caterer quoted for a hundred and eighty. {claim- F3}
Abena: A hundred and eighty. Then my church will have to share chairs. {claim- F3}
Yaw: The photographer wants the eight hundred deposit by Friday. {claim- F11}
Efua: I'll pay the photographer deposit tomorrow. {action+}
Declan: It might be worth asking the caterer whether the price holds if numbers change. {action-}
Abena: Maybe we just add ten more chairs for the church people and say nothing. {decision-}
Efua: Mum. No.
Yaw: Has anyone told Liam's grandmother about the engagement customs? She might be surprised. {question+} {~}
Efua: Okay. I think we've covered it. Thank you, all. Love you.
Declan: Love you too. Even the jollof.
