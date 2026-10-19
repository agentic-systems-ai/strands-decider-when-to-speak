---
meeting_id: ecolab-coastal-d8-s1
theme: Weekly meeting of a university ecology research lab
domain_pack: research_lab
drama: 0.8
seed: 1
author: claude-opus-5-5 (Claude Code session)
pack:
  title: Calloway Lab weekly meeting
  org: Calloway Lab, Coastal Ecology, Tidemark University (fictional)
  agenda:
    - {id: contamination, title: The contaminated samples, goal: Decide what to do about the eelgrass samples from the freezer failure, timebox_min: 5}
    - {id: authorship, title: Seagrass paper authorship, goal: Settle the author order before drafting, timebox_min: 4}
    - {id: boat_time, title: Boat schedule, goal: Divide the remaining boat days between projects, timebox_min: 3}
    - {id: renewal, title: Grant renewal, goal: Plan the renewal application, timebox_min: 3}
  facts:
    - {id: F1, key: contaminated_samples, statement: "Samples contaminated in the freezer failure = 64", value: "64"}
    - {id: F2, key: total_samples, statement: "Eelgrass samples collected this year = 210", value: "210"}
    - {id: F3, key: boat_days_booked, statement: "Boat days booked for the season = 12", value: "12"}
    - {id: F4, key: boat_day_cost, statement: "Cost per boat day = $1,150", value: "$1,150"}
    - {id: F5, key: renewal_deadline, statement: "Grant renewal deadline = January 20", value: "January 20"}
    - {id: F6, key: renewal_ask, statement: "Renewal budget request = $480,000", value: "$480,000"}
    - {id: F7, key: submission_target, statement: "Seagrass paper submission target = December 1", value: "December 1"}
    - {id: F8, key: transects, statement: "Seagrass transects surveyed = 18", value: "18"}
    - {id: F9, key: freezer_failure_date, statement: "Freezer failure = September 3", value: "September 3"}
    - {id: F10, key: lab_members, statement: "Lab members = 9", value: "9"}
    - {id: F11, key: resequencing_cost, statement: "Re-sequencing the contaminated samples = $9,600", value: "$9,600"}
    - {id: F12, key: seasons_of_data, statement: "Seasons of eelgrass data = 3", value: "3"}
personas:
  - name: Bernard
    role: Principal investigator
    goals: Get the seagrass paper out before the renewal
    hidden_agenda: Wants his name last and a former student's name second
    verbosity: 4
    wpm: 160
    catchphrases: ["look"]
    voice_gender: male
  - name: Ama
    role: Postdoc who did most of the seagrass analysis
    goals: First authorship on the seagrass paper
    hidden_agenda: Needs a first-author paper for her job applications this winter
    verbosity: 3
    wpm: 165
    catchphrases: []
    voice_gender: female
  - name: Kieran
    role: PhD student, ran the freezer and the samples
    goals: Not be blamed for the freezer
    hidden_agenda: Noticed the freezer alarm was muted and didn't report it
    verbosity: 2
    wpm: 150
    catchphrases: ["sorry"]
    voice_gender: male
  - name: Sunita
    role: Lab manager
    goals: Keep the budget and the boat schedule straight
    hidden_agenda: Has already told the dock the lab may cancel days
    verbosity: 2
    wpm: 145
    catchphrases: []
    voice_gender: female
---
## contamination :: How bad the freezer damage is; Bernard lowballs it; resequencing cost is overstated then fixed
Bernard: Look, let's deal with the freezer first, because it touches everything else. Kieran, how many did we lose? {question- @+3}
Kieran: Sorry, I've been going through the inventory all week.
Bernard: And? {~}
Kieran: Sixty-four contaminated. Out of the two hundred and ten we collected this year. {claim- F1} {claim- F2}
Bernard: Sixty-four. I'd been telling people it was about thirty. {claim+ F1 "30"}
Ama: Thirty would have been bad. Sixty-four is a third of the season. {claim- F1}
Sunita: The failure was on the third of September. Nobody caught it for two days. {claim- F9}
Bernard: Why did nobody catch it for two days? {question- @+1}
Kieran: The alarm— it's an old freezer.
Ama: Can we resequence them? Is the tissue still usable for that? {question- @+1}
Kieran: For most of them. The sequencing would be about fifteen thousand. {claim+ F11 "$15,000"}
Bernard: Fifteen thousand. Absolutely not. {claim+ F11 "$15,000"}
Ama: Then the paper is missing a third of this year.
Bernard: We have three seasons of data. One bad batch doesn't sink a paper. {claim- F12}
Ama: It does if the bad batch is all from the two sites the paper is about.
Bernard: Is that true? {question- @+1}
Kieran: Mostly, yes. The north transects were all on the bottom shelf.
Sunita: I just checked the core facility quote. Resequencing is ninety-six hundred, not fifteen. {claim- F11}
Kieran: Oh. Sorry, I had the old price with the extra library prep.
Bernard: Ninety-six hundred. Still a lot. {claim- F11}
Ama: It's a lot less than a paper with a hole in it.
Bernard: Look. Fine. We resequence the north-transect samples only, and we pay for it out of the general account. {decision+}
Kieran: I'll pull the north-transect samples and send them to the core facility on Monday. {action+}
Sunita: Somebody should really replace that freezer alarm, too. {action-}
## authorship :: Who goes first; a loud disagreement; a drift into the chair's retirement party
Bernard: Look, authorship. I was thinking Ama second, and Priyanka first, since the original idea was her thesis.
Ama: Priyanka left two years ago. I did the analysis, the models, and the figures.
Bernard: The idea matters.
Ama: The idea was one paragraph in a thesis chapter. I wrote the paper.
Kieran: Can I say something? {~}
Bernard: Go ahead.
Kieran: Sorry. I just think whoever wrote it should be first. That's the norm in this field.
Bernard: The norm in this field is that the PI decides.
Kieran: Could it maybe be co-first? {decision-} {question- @+1}
Ama: Co-first with someone who left two years ago doesn't help me.
Sunita: Did you all hear Dean Whitfield is retiring? The party is next Friday. {drift+ 3} {~}
Kieran: Is there going to be the slideshow again? Last time it was forty minutes. {question- @+1}
Sunita: There will absolutely be a slideshow.
Ama: Can we please finish the authorship conversation? This matters to me. {question- @+1}
Bernard: All right. Look. Ama, you're right that you did the work.
Ama: So I'm first? {question- @+1}
Bernard: You're first. Priyanka second, me last. {decision+}
Ama: Thank you. Truly.
Bernard: And the paper goes out by December first, which means a full draft by the middle of November. {claim- F7}
Ama: I'll have a full draft to everyone by November fifteenth. {action+}
Bernard: Fine.
## boat_time :: Dividing the boat days; Ama's count is off
Sunita: Boat time. We have twelve days booked for the rest of the season. {claim- F3}
Ama: Twelve? I thought we had twenty. We booked extra in the spring. {claim+ F3 "20"} {question- @+1}
Sunita: We booked twenty, and I cancelled eight when the engine was in the shop. Twelve. {claim- F3}
Bernard: Each day is eleven-fifty, so every cancelled day is money we kept, at least. {claim- F4}
Kieran: My transects need four days. Minimum. {~}
Ama: The seagrass revisits need four too.
Bernard: And the new kelp pilot needs at least three. {~}
Sunita: That's eleven. One day spare for weather. {~}
Bernard: Then Kieran four, Ama four, kelp three, one spare. {decision+} {~}
Ama: Works for me.
Sunita: I'll update the dock calendar tonight with the split. {action+}
Kieran: Saw a seal hauled out on the dock ramp yesterday. Huge one. {drift+ 2}
Ama: The one with the scar? That's Clyde. He's been around for years. {~}
## renewal :: The renewal plan; a date nobody checks
Bernard: Renewal. The deadline is mid-February, so there's breathing room. {claim+ F5 "mid-February"}
Ama: What are we asking for? {question- @+1}
Bernard: Four hundred eighty thousand over three years. {claim- F6}
Sunita: The budget justification needs the boat costs, which we now actually know.
Bernard: We could ask for more, given costs went up. I'd want to see the numbers first. {decision-}
Kieran: Will the freezer thing hurt the renewal? {question- @+1}
Bernard: Not if the resequenced data is in the preliminary results.
Ama: That's another reason the paper has to go out on time.
Bernard: Sunita, could you start the budget spreadsheet for the renewal this week? {question- @+1}
Sunita: Yes. I'll have a first version by Friday. {action+}
Kieran: Who's writing the data management plan? Last time it was a mess. {question+} {~}
Bernard: Look, I think that's enough for today. Good meeting. Mostly.
Ama: Mostly.
