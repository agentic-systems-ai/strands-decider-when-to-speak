---
meeting_id: ecolab-weekly-d5-s1
theme: Weekly meeting of a university ecology research lab
domain_pack: research_lab
drama: 0.5
seed: 1
author: claude-opus-5-5 (Claude Code session)
pack:
  title: Hollis Lab weekly meeting
  org: Hollis Lab, Department of Ecology, Northfield University (fictional)
  agenda:
    - {id: field_season, title: Field season logistics, goal: Lock the start date, sites and equipment for the season, timebox_min: 4}
    - {id: data_status, title: Data and sample backlog, goal: Get an honest status on processing and what to sequence, timebox_min: 4}
    - {id: deadlines, title: Papers and deadlines, goal: Agree priorities between the thesis chapter and the side paper, timebox_min: 4}
    - {id: lab_ops, title: Lab operations and budget, goal: Check the grant balance and the lab's practical needs, timebox_min: 3}
  facts:
    - {id: F1, key: field_sites, statement: "Field sites this season = 14", value: "14"}
    - {id: F2, key: field_start_date, statement: "Planned field season start = May 18", value: "May 18"}
    - {id: F3, key: camera_traps_working, statement: "Camera traps working = 36 of 40", value: "36"}
    - {id: F4, key: samples_processed, statement: "Samples processed so far = 1,240", value: "1,240"}
    - {id: F5, key: sample_backlog, statement: "Samples still unprocessed = 380", value: "380"}
    - {id: F6, key: grant_remaining, statement: "Remaining grant balance = $27,400", value: "$27,400"}
    - {id: F7, key: abstract_deadline, statement: "Conference abstract deadline = February 2", value: "February 2"}
    - {id: F8, key: truck_rental_weekly, statement: "Field truck rental = $540 per week", value: "$540"}
    - {id: F9, key: permit_expiry, statement: "Research permit expires April 30", value: "April 30"}
    - {id: F10, key: undergrad_assistants, statement: "Undergraduate field assistants = 5", value: "5"}
    - {id: F11, key: sequencing_cost, statement: "Sequencing cost = $18 per sample", value: "$18"}
    - {id: F12, key: revision_due, statement: "Manuscript revision due March 9", value: "March 9"}
personas:
  - name: Elena
    role: Principal investigator
    goals: A productive season and June graduating on time
    hidden_agenda: The grant renewal depends on this season's data
    verbosity: 3
    wpm: 155
    catchphrases: ["right", "let's be strategic"]
    voice_gender: female
  - name: Tariq
    role: Postdoc, leads the field season
    goals: Get into the field early
    hidden_agenda: Interviewing for faculty jobs, distracted
    verbosity: 3
    wpm: 160
    catchphrases: ["basically", "in the field"]
    voice_gender: male
  - name: June
    role: Fourth-year PhD student
    goals: Finish the thesis chapter
    hidden_agenda: Behind on processing and embarrassed about it
    verbosity: 2
    wpm: 150
    catchphrases: ["I think", "sorry"]
    voice_gender: female
  - name: Felix
    role: Lab manager
    goals: Keep the equipment alive and the budget sane
    hidden_agenda: Has been fixing camera traps on weekends
    verbosity: 2
    wpm: 140
    catchphrases: ["for what it's worth"]
    voice_gender: male
---
## field_season :: Dates, sites and traps; Tariq gets the permit date wrong and nobody notices
Elena: Right, let's start. Field season first, since it's coming up fast. Tariq? {question- @+1}
Tariq: Basically, we're on track for May eighteenth, all fourteen sites. {claim- F2} {claim- F1}
Elena: All fourteen, including the ridge sites? {question- @+1} {claim- F1}
Tariq: Including the ridge. The access road was cleared last week.
Felix: For what it's worth, the camera traps are the bottleneck. Thirty-six of the forty work. {claim- F3}
Elena: What's wrong with the other four? {question- @+1}
Felix: Two have dead boards, two have cracked housings. The housings I can fix. The boards, not really.
June: Do we need all forty out at once? {question- @+1}
Tariq: In the field we lose a few to bears every season, so yes, basically.
Felix: I'll order two replacement boards this week, out of the equipment line. {action+}
Elena: Thank you, Felix.
Tariq: And the permit is good through the end of May, so no rush there. {claim+ F9 "end of May"}
Elena: Good. One less thing.
June: Are the undergrads confirmed? {question- @+1}
Tariq: Five confirmed. One more maybe, if her summer class gets cancelled. {claim- F10}
Elena: Five is enough. A sixth would be nice. {claim- F10}
Tariq: Somebody needs to do the safety training with them before we go. {action-}
Elena: Has anyone heard back from the parks office about site nine? {question+} {~}
Felix: Sorry, the truck. We should talk about the truck.
Tariq: Right, the truck rental is five forty a week. For the whole season that adds up. {claim- F8} {~nc}
Felix: We could share with the Okafor lab, they're out at the same time.
Elena: Maybe we split the truck with Okafor. Let me think about it. {decision-}
Tariq: In the field, sharing a truck means somebody's always waiting.
Elena: Okay, the season starts May eighteenth, all fourteen sites. That's locked. {decision+} {claim- F2} {claim- F1}
Tariq: Locked. Finally.
## data_status :: The backlog is bigger than June says; deciding what to sequence
Elena: Data. June, where are we with processing? {question- @+1}
June: I think, um, we've processed about twelve hundred. {claim- F4}
Elena: And what's left? {question- @+1}
June: About two hundred? Maybe a bit more. {claim+ F5 "200"} {~}
Felix: For what it's worth, the freezer log says three hundred and eighty still unprocessed. {claim- F5}
June: Sorry. Yes. I was counting the ones I'd already sorted. It's three eighty. {claim- F5}
Elena: That's okay. It's better to know now. How long would three eighty take you? {question- @+1} {claim- F5}
June: Honestly, at my current pace, most of the summer.
Tariq: Which is exactly when you need to be writing.
Elena: Right. Let's be strategic. Do we need to sequence all of them? {question- @+1}
Tariq: Basically, no. Half of them are the replicate sites. The core sites matter more.
Felix: Sequencing is eighteen dollars a sample, so three eighty is real money anyway. {claim- F11}
June: If we only did the core sites, I think it's about half of them. {~}
Elena: Then we sequence the core-site samples first and leave the replicates for the fall. That's the plan. {decision+}
June: Okay. That's, okay, that's a relief, actually.
Tariq: I can help with sorting if I'm not in the field. {action-}
Elena: Tariq, you're going to be in the field.
Tariq: Right, true.
Felix: I'll set up a shared sheet so we can see what's left, site by site. {action+}
June: Thank you.
Tariq: Did anyone else see the bear video from the ridge camera? {drift+ 3} {question- @+1}
Felix: The one where it licks the lens? I've watched it about ten times. {~}
June: My mom made it her phone background.
## deadlines :: Thesis chapter vs the side paper; Elena misremembers the abstract deadline, June corrects her
Elena: Okay, that's very good, and we're moving on. Deadlines. The conference abstract is due February twelfth, if I remember right. {claim+ F7 "February 12"}
June: Sorry, I think it's the second. February second. {claim- F7}
Elena: The second. That's, okay, that's sooner. {claim- F7}
Tariq: And the revision for the moth paper is due March ninth. {claim- F12}
June: Do I have to be on the moth paper revision? {question- @+1}
Elena: You're second author. But the chapter matters more. {~nc}
Tariq: The reviewers mostly want the stats redone. Basically, that's me anyway.
Elena: Then let's be strategic. June, the chapter comes first, the moth revision is Tariq's. Settled. {decision+}
June: Thank you. Really.
Tariq: I'll redo the stats for the moth revision by the end of February. {action+} {~nc}
Elena: And the abstract? Who's writing it? {question+} {~}
Tariq: It should probably come from the chapter data.
June: Maybe. If the chapter goes okay. I don't know. {action-}
Elena: Let's see where the chapter is next week before we commit to the abstract. {decision-}
June: Is it okay if I skip the reading group until the chapter's done? {question- @+1}
Elena: For a few weeks, yes.
June: Okay. Great.
## lab_ops :: The grant balance and a quiet fight about the freezer
Elena: Last thing, lab ops. Felix, the money.
Felix: Remaining on the grant is twenty-seven four. {claim- F6}
Tariq: That's less than I thought.
Felix: The sequencing and the truck are the big ones this summer.
Tariq: Sorry, someone's knocking, it's the department admin with a package. {drift- 2}
June: No worries.
Elena: Is the minus-eighty freezer still making that noise? {question- @+1}
Felix: It is. For what it's worth, I think the compressor's going.
Tariq: If that freezer dies, we lose everything June hasn't processed.
June: Please don't say that.
Elena: Should we move the samples to the department freezer as a backup? {question- @+1}
Felix: The department freezer is full. I asked last month.
Elena: Could we get the compressor serviced before the season? {question- @+1}
Felix: Probably. It's a few hundred dollars, not thousands. {~}
Elena: Then let's get it serviced. Out of this year's money. Done. {decision+}
Felix: I'll call the service company tomorrow and book it. {action+}
Tariq: What happens to the samples while it's being serviced? {question+} {~}
Elena: Right, I think that's everything. Good meeting. June, chapter.
June: Chapter. Got it.
