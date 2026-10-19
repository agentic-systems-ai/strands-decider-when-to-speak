---
meeting_id: garden-maplecourt-d2-s2
theme: "Community garden committee: plots, water and the spring fair"
domain_pack: community_group
drama: 0.2
seed: 2
author: claude-opus-5-5 (Claude Code session)
pack:
  title: Garden committee - spring planning
  org: Maple Court Community Garden (fictional)
  agenda:
    - {id: season, title: The new season, goal: Assign plots for returning and new gardeners, timebox_min: 3}
    - {id: water, title: Water and rain barrels, goal: Decide whether to add more rain barrels, timebox_min: 4}
    - {id: seedling_sale, title: Seedling sale, goal: Plan the spring seedling sale, timebox_min: 4}
    - {id: shed, title: Tool shed, goal: Decide on the shed repair, timebox_min: 3}
  facts:
    - {id: F1, key: plots, statement: "Plots = 36", value: "36"}
    - {id: F2, key: returning_gardeners, statement: "Returning gardeners = 29", value: "29"}
    - {id: F3, key: new_gardeners, statement: "New gardeners = 7", value: "7"}
    - {id: F4, key: plot_fee, statement: "Plot fee = $40", value: "$40"}
    - {id: F5, key: rain_barrels, statement: "Rain barrels installed = 10", value: "10"}
    - {id: F6, key: barrel_cost, statement: "Rain barrel = $85 each", value: "$85"}
    - {id: F7, key: water_bill, statement: "Water bill last year = $960", value: "$960"}
    - {id: F8, key: sale_date, statement: "Seedling sale = Saturday, April 12", value: "April 12"}
    - {id: F9, key: seedlings_grown, statement: "Seedlings grown for the sale = 600", value: "600"}
    - {id: F10, key: shed_quote, statement: "Shed repair quote = $1,100", value: "$1,100"}
    - {id: F11, key: bank_balance, statement: "Bank balance = $2,850", value: "$2,850"}
    - {id: F12, key: seedling_price, statement: "Seedling price = $3 each", value: "$3"}
personas:
  - name: Lorraine
    role: Committee chair
    goals: A smooth start to the season
    hidden_agenda: Hoping someone else will take over the seedling sale next year
    verbosity: 3
    wpm: 145
    catchphrases: []
    voice_gender: female
  - name: Ahmed
    role: Looks after water
    goals: Cut the water bill
    hidden_agenda: Has a line on cheap barrels from a juice factory
    verbosity: 2
    wpm: 150
    catchphrases: []
    voice_gender: male
  - name: Sunny
    role: Volunteer, runs the seedling sale
    goals: A bigger sale than last year
    hidden_agenda: Grew extra seedlings in her apartment and lost count
    verbosity: 3
    wpm: 170
    catchphrases: []
    voice_gender: female
  - name: Gordon
    role: Treasurer
    goals: Keep a little in reserve
    hidden_agenda: Repaired the shed door himself twice already
    verbosity: 2
    wpm: 135
    catchphrases: []
    voice_gender: male
---
## season :: Assigning plots
Lorraine: Hello, everyone. Let's start with plots. We have thirty-six this year. {claim- F1}
Gordon: Twenty-nine returning gardeners, and seven new ones. That fills every plot. {claim- F2} {claim- F3}
Sunny: Do the new gardeners get the plots by the gate? Those are the hardest to keep watered. {question- @+1}
Lorraine: They do, but we'll pair each one with a returning gardener for the first month. {decision+}
Gordon: That worked well last year.
Ahmed: And the fee is still forty? {question- @+1} {claim- F4}
Gordon: Forty for the season. No change. {claim- F4}
Lorraine: I'll send the plot assignments and the pairing list by email this weekend. {action+} 
Sunny: Thanks, Lorraine.
## water :: Rain barrels; Ahmed's count is corrected
Lorraine: Water. Ahmed? {question- @+1}
Ahmed: We have twelve rain barrels now, and they made a real difference to the bill. {claim+ F5 "12"}
Gordon: I count ten on the inventory. Two were promised but never arrived. {claim- F5}
Ahmed: Ten, right. The other two are still at the factory. {claim- F5}
Sunny: What was the water bill last year? {question- @+1}
Gordon: Nine hundred and sixty. Down from about twelve hundred the year before. {claim- F7} {~}
Ahmed: Barrels are eighty-five each new. But a juice factory nearby gives away used ones. {claim- F6}
Lorraine: Used ones would be lovely, if they're clean.
Ahmed: They need a good scrub. That's all. 
Gordon: The barrels really want labels on them, too, so nobody drinks from them. {action-}
Lorraine: Then we'll take the used barrels from the factory instead of buying new. {decision+}
Ahmed: I'll pick up six from the factory next Saturday. {action+} {~}
Sunny: The road by the factory is closed for the new bridge. You have to go all the way around. {drift+ 2}
Gordon: That bridge has been "nearly finished" for two years.
Lorraine: Sunny, the seedling sale.
## seedling_sale :: The sale; Sunny's seedling count stands
Sunny: The sale is on April twelfth. I've grown about eight hundred seedlings. {claim- F8} {claim+ F9 "800"}
Gordon: That's a lot of tomatoes.
Sunny: Tomatoes, peppers, kale and some herbs.
Lorraine: Are we keeping the price at three dollars? {question- @+1} {claim- F12}
Sunny: Three dollars, or four for the bigger pots. {~nc}
Ahmed: Who's helping on the day? Last year you were alone at the table for hours. {question- @+1}
Sunny: Nobody yet.
Gordon: I can do the morning. {action+}
Ahmed: And I'll do the afternoon, after the barrels. {action+}
Lorraine: Maybe we could put up a sign at the library too? People there love plants. {decision-} {question+} {~}
Sunny: The table needs to be in the shade this year. The basil wilted last time.
## shed :: The repair; one deferral
Lorraine: Last thing. The shed. Gordon? {question- @+1}
Gordon: The roof leaks and the door's off its hinges again. The quote to fix both is eleven hundred. {claim- F10}
Ahmed: Can we afford it? {question- @+1}
Gordon: The balance is twenty-eight fifty. So yes, but it's a big chunk. {claim- F11}
Sunny: The sale should bring in a good amount. That would help.
Lorraine: Let's wait until after the seedling sale, and then decide on the shed. {decision-}
Gordon: The door I can fix again in the meantime. I'm getting good at it. {action+}
Lorraine: Thank you, Gordon. That's everything. See you all in the garden.
