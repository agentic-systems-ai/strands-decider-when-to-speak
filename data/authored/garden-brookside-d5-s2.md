---
meeting_id: garden-brookside-d5-s2
theme: "Community garden committee: plots, water and the spring fair"
domain_pack: community_group
drama: 0.5
seed: 2
author: claude-opus-5-5 (Claude Code session)
pack:
  title: Garden committee - monthly meeting
  org: Brookside Community Garden (fictional)
  agenda:
    - {id: theft, title: Produce theft, goal: Decide what to do about the thefts, timebox_min: 5}
    - {id: water, title: Water, goal: Timers and the bill, timebox_min: 4}
    - {id: fair, title: Spring fair, goal: Plan the fair, timebox_min: 4}
    - {id: fees, title: Fees and hours, goal: Confirm next year's fee and volunteer hours, timebox_min: 3}
  facts:
    - {id: F1, key: plots, statement: "Plots = 44", value: "44"}
    - {id: F2, key: theft_reports, statement: "Theft reports this season = 9", value: "9"}
    - {id: F3, key: fence_quote, statement: "Taller fence quote = $4,200", value: "$4,200"}
    - {id: F4, key: camera_cost, statement: "Trail camera = $350", value: "$350"}
    - {id: F5, key: water_timers, statement: "Water timers installed = 8", value: "8"}
    - {id: F6, key: water_bill, statement: "Last season's water bill = $1,640", value: "$1,640"}
    - {id: F7, key: fair_date, statement: "Spring fair = Saturday, May 10", value: "May 10"}
    - {id: F8, key: fair_profit, statement: "Fair profit last year = $1,920", value: "$1,920"}
    - {id: F9, key: balance, statement: "Bank balance = $3,700", value: "$3,700"}
    - {id: F10, key: plot_fee, statement: "Plot fee = $50", value: "$50"}
    - {id: F11, key: volunteer_hours, statement: "Volunteer hours per plot = 6", value: "6"}
    - {id: F12, key: gate_code_changes, statement: "Gate code changes this year = 2", value: "2"}
personas:
  - name: Odette
    role: Committee chair
    goals: Keep the garden open and friendly
    hidden_agenda: Doesn't want a garden that feels like a fortress
    verbosity: 3
    wpm: 150
    catchphrases: []
    voice_gender: female
  - name: Ike
    role: Plot holder, upset about the thefts
    goals: Stop the thefts
    hidden_agenda: Lost his entire tomato crop and is furious
    verbosity: 4
    wpm: 175
    catchphrases: []
    voice_gender: male
  - name: Raul
    role: Looks after water
    goals: Lower the water bill
    hidden_agenda: Installed the timers himself on a weekend
    verbosity: 2
    wpm: 145
    catchphrases: []
    voice_gender: male
  - name: Petra
    role: Spring fair organizer
    goals: A fair that funds the garden
    hidden_agenda: Wants to sell plant starts from her own greenhouse
    verbosity: 3
    wpm: 165
    catchphrases: []
    voice_gender: female
---
## theft :: How bad it is; Ike exaggerates, then the options
Odette: Let's start with the thefts. I know people are upset.
Ike: Upset is an understatement. There have been over twenty thefts this season. My tomatoes are gone. All of them. {claim+ F2 "over 20"}
Odette: I'm so sorry, Ike. The log has nine reports, though. Maybe some weren't reported? {claim- F2} {~nc}
Ike: Nine reported. Probably more that people didn't bother to write down. {claim- F2}
Petra: Mine weren't touched, for what it's worth. It seems to be the plots by the back gate.
Raul: The back gate is the one with the broken latch. Anyone can push it open.
Ike: Then why hasn't it been fixed? {question- @+1}
Raul: I've fixed it twice. It keeps getting forced.
Ike: We need a taller fence. Now.
Odette: The fence quote was forty-two hundred. That's more than we have. {claim- F3}
Raul: The balance is thirty-seven hundred. So, no fence this year. {claim- F9}
Petra: What about a trail camera? They're about three hundred and fifty. {claim- F4} {question- @+1}
Odette: I don't love cameras in a community garden. It feels unfriendly.
Ike: It feels unfriendly to have your tomatoes stolen.
Odette: Fair. Okay, a camera on the back gate only, and a sign saying it's there. {decision+}
Raul: I'll buy the camera and put it up this weekend, and fix the latch properly with a padlock. {action+}
Petra: Do we change the gate code again? That's twice already this year. {question- @+1} {claim- F12}
Odette: Not yet. Let's see if the camera helps first. {decision-} {~}
Ike: Fine.
## water :: Timers and the bill; Raul's figure stands
Odette: Water. Raul? {question- @+1}
Raul: We have eight timers on the main beds now. The bill last season was twenty-two hundred, so they should help a lot. {claim- F5} {claim+ F6 "$2,200"}
Petra: That's a lot of water for forty-four plots. {claim- F1}
Raul: The timers alone should cut it by a quarter.
Odette: Do we need more timers? {question- @+1}
Raul: Two more would cover the herb beds. They're cheap.
Odette: Then let's get two more. {decision+}
Ike: My plot's tap leaks, by the way. It'd be nice if it got looked at before summer. {action-}
Raul: Send me a photo and I'll fix it. {action+}
## fair :: The spring fair; Petra's profit memory is high, corrected later; a detour about a neighbor's chickens
Petra: The fair. It's on May tenth. Last year we made about three thousand. {claim- F7} {claim+ F8 "$3,000"}
Odette: That would be lovely again.
Ike: Could we sell the excess produce at the fair? Well, what's left of it. {question- @+1}
Petra: Absolutely. A produce table would be great.
Raul: The neighbor's chickens got into the garden again on Tuesday. They ate half my lettuce. {drift+ 3}
Ike: Maybe the chickens are the thieves.
Petra: The chickens don't take whole tomatoes, Ike.
Odette: The fair. Petra, tell us what you need.
Petra: Sorry, I just found last year's report. We made nineteen twenty, not three thousand. Three thousand was before the tent rental. {claim- F8}
Odette: Nineteen twenty. Still very useful. {claim- F8}
Petra: I'd like to sell plant starts from my greenhouse at the fair, with the money going to the garden.
Odette: That's generous. Yes, please. {decision+}
Petra: I'll make the posters and put them up at the library and the cafe. {action+}
## fees :: Next year's fee
Odette: Fees. The plot fee is fifty, and six volunteer hours per plot. {claim- F10} {claim- F11}
Ike: If we need a fence, maybe the fee should go up. {decision-}
Raul: Sixty dollars would raise four hundred and forty more. Not a fence, but a start. {~nc}
Odette: Let's put the fee question to the members at the fair, so everyone has a say. {decision-}
Petra: Who counts the votes at the fair? {question+} {~}
Ike: Do we know if the city has any grants for garden fencing? {question- @+1}
Odette: I don't know. I'll look into it this week. Thank you, everyone. {action+}
Petra: Ike, I really am sorry about your tomatoes.
Ike: Thanks. Next year they'll be behind a camera.
