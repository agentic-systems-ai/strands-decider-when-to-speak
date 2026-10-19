---
meeting_id: wedding-petrov-d2-s2
theme: Family video call planning a cousin's wedding
domain_pack: family_planning
drama: 0.2
seed: 2
author: claude-opus-5-5 (Claude Code session)
pack:
  title: Katya and Sam's wedding - Sunday call
  org: The Petrov-Hughes family (fictional)
  agenda:
    - {id: venue_day, title: The venue and the day, goal: Confirm the garden venue, time and the rain plan, timebox_min: 4}
    - {id: guests, title: Guests, goal: Headcount and the RSVP chase, timebox_min: 3}
    - {id: food_music, title: Food and music, goal: Caterer, cake and the band, timebox_min: 4}
    - {id: travel, title: Travel and cabins, goal: Where everyone sleeps and how they get there, timebox_min: 3}
  facts:
    - {id: F1, key: wedding_date, statement: "Wedding = Saturday, June 14", value: "June 14"}
    - {id: F2, key: ceremony_time, statement: "Ceremony at 3:00 pm", value: "3:00 pm"}
    - {id: F3, key: venue_capacity, statement: "Garden venue capacity = 90", value: "90"}
    - {id: F4, key: guests_confirmed, statement: "Guests confirmed = 72", value: "72"}
    - {id: F5, key: caterer_per_head, statement: "Caterer = $55 per head", value: "$55"}
    - {id: F6, key: band_fee, statement: "Band fee = $1,400", value: "$1,400"}
    - {id: F7, key: cake_tiers, statement: "Cake = 2 tiers", value: "2"}
    - {id: F8, key: cabins, statement: "Cabins booked = 9", value: "9"}
    - {id: F9, key: cabin_rate, statement: "Cabin rate = $160 per night", value: "$160"}
    - {id: F10, key: shuttle_seats, statement: "Shuttle seats = 30", value: "30"}
    - {id: F11, key: rain_tent, statement: "Rain tent = $900", value: "$900"}
    - {id: F12, key: rsvp_deadline, statement: "RSVP deadline = May 1", value: "May 1"}
personas:
  - name: Galina
    role: Bride's aunt, the family organizer
    goals: Nobody gets forgotten
    hidden_agenda: Has a list of relatives Katya hasn't heard of
    verbosity: 3
    wpm: 150
    catchphrases: []
    voice_gender: female
  - name: Rob
    role: Bride's father
    goals: A lovely day that doesn't break the bank
    hidden_agenda: Secretly booked the band without telling anyone the final price
    verbosity: 2
    wpm: 140
    catchphrases: []
    voice_gender: male
  - name: Katya
    role: The bride
    goals: A relaxed garden wedding
    hidden_agenda: Would like fewer second cousins
    verbosity: 3
    wpm: 165
    catchphrases: []
    voice_gender: female
  - name: Misha
    role: Cousin, amateur photographer
    goals: Help, and take great photos
    hidden_agenda: Hopes to be asked to do the photos officially
    verbosity: 3
    wpm: 170
    catchphrases: []
    voice_gender: male
---
## venue_day :: The garden, the time and the rain plan
Galina: Hello, everyone. Can you all see me? Rob, your camera's pointing at the ceiling. {~}
Rob: Sorry. Better? {~}
Galina: Much better. Katya, let's start with the day itself.
Katya: The garden venue is confirmed for June fourteenth, ceremony at three. {claim- F1} {claim- F2}
Misha: Three is perfect for photos. The light in that garden in the afternoon is beautiful. {claim- F2}
Galina: And if it rains? {question- @+1}
Katya: The venue has a tent we can rent. Nine hundred dollars. {claim- F11}
Rob: Nine hundred for a tent. Well, it's cheaper than ruined dresses. {claim- F11}
Galina: Do we have to decide about the tent now? {question- @+1}
Katya: By the end of May. They need a week's notice. {~nc}
Rob: Let's book it anyway. I'd rather not watch the forecast all week. {decision+}
Katya: Thank you, Dad. I'll tell the venue on Monday. {action+}
## guests :: Headcount; Galina's number stands
Galina: Guests. We're at about eighty confirmed, I think. {claim+ F4 "80"}
Katya: That's close to the garden's limit. It holds ninety. {claim- F3}
Galina: I have a few more names, actually. Your grandfather's cousins in Riga.
Katya: Auntie. I've never met them.
Galina: They knew you when you were a baby.
Rob: The RSVP deadline is the first of May. Anyone who hasn't replied by then isn't coming. {claim- F12}
Galina: That seems harsh for family. 
Rob: Maybe we invite the Riga cousins anyway and see who comes? {decision-} {question- @+1}
Katya: It's not harsh. It's a garden with ninety chairs. {claim- F3}
Galina: All right. I'll send the Riga cousins a card, but no invitation. {action+}
## food_music :: Caterer, cake and the band; Rob's band fee is corrected
Katya: Food. The caterer is fifty-five a head, buffet style. {claim- F5}
Misha: Buffets are great for photos. People actually talk to each other.
Galina: And the cake? {question- @+1}
Katya: Two tiers. Lemon on the bottom, chocolate on top. {claim- F7}
Rob: The band is booked. A thousand dollars for the whole evening. {claim+ F6 "$1,000"}
Katya: Dad, the contract you forwarded says fourteen hundred. {claim- F6}
Rob: Ah. Fourteen hundred. They added the extra hour. {claim- F6}
Galina: That's still reasonable for a whole band. 
Rob: The neighbors should probably hear about the band before the day. {action-}
Misha: My friend's band played at my office party. They did a polka at the end and everyone joined in. {drift+ 2}
Galina: A polka! Your grandfather would have loved that.
Katya: Who's doing the photos? We haven't booked anyone yet. {question- @+2}
Rob: Professional photographers are expensive.
Misha: I could do them, if you want. I'd love to. {action+}
Katya: Really? Misha, that would be amazing. {~}
Galina: Then Misha does the photos. That's settled. {decision+} 
Misha: I won't let you down.
## travel :: Cabins and the shuttle
Galina: Travel. Where is everyone sleeping? {question- @+1}
Rob: Nine cabins booked near the venue, a hundred and sixty a night. {claim- F8} {claim- F9}
Katya: Is that enough for the out-of-town family? {question- @+1}
Galina: Nine cabins, two or three per cabin. That's most of them. {claim- F8}
Misha: And the shuttle has thirty seats, from the cabins to the garden. {claim- F10}
Rob: Thirty is plenty. Some people will drive. {claim- F10}
Katya: Could someone make a map for the guests, with the cabins and the garden? {question- @+1}
Misha: I'll make one. I'll put a little photo of the garden on it, too. {action+}
Galina: Is anyone picking up Grandma from the airport? {question+} {~}
Katya: Thank you, everyone. This is going to be lovely.
Rob: It already is.
