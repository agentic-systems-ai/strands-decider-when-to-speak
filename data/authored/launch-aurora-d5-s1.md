---
meeting_id: launch-aurora-d5-s1
theme: Go/no-go for the Aurora mobile app launch
domain_pack: product_launch
drama: 0.5
seed: 1
author: claude-opus-5-5 (Claude Code session)
pack:
  title: Aurora 2.0 go/no-go
  org: Brightfern Health (fictional)
  agenda:
    - {id: crash_metrics, title: Release readiness metrics, goal: Check stability and performance against the launch bar, timebox_min: 5}
    - {id: store_assets, title: Store listing and assets, goal: Confirm screenshots, copy and legal review are on track, timebox_min: 4}
    - {id: launch_date, title: Launch date, goal: Make the go/no-go call and pick a date, timebox_min: 5}
    - {id: comms_plan, title: Launch comms and support, goal: Agree the announcement and support readiness, timebox_min: 4}
  facts:
    - {id: F1, key: crash_free_sessions_last_week, statement: "Crash-free sessions last week = 99.2%", value: "99.2%"}
    - {id: F2, key: launch_bar_crash_free, statement: "Launch bar for crash-free sessions = 99.0%", value: "99.0%"}
    - {id: F3, key: p95_cold_start, statement: "p95 cold start on the release candidate = 1.8 seconds", value: "1.8 s"}
    - {id: F4, key: open_p1_bugs, statement: "Open P1 bugs = 3", value: "3"}
    - {id: F5, key: beta_testers, statement: "Active beta testers = 4,200", value: "4,200"}
    - {id: F6, key: beta_nps, statement: "Beta NPS = 41", value: "41"}
    - {id: F7, key: store_review_days, statement: "Typical app store review time = 2 days", value: "2 days"}
    - {id: F8, key: launch_marketing_budget, statement: "Launch marketing budget = $85,000", value: "$85,000"}
    - {id: F9, key: support_agents_trained, statement: "Support agents trained on 2.0 = 14", value: "14"}
    - {id: F10, key: android_share_of_beta, statement: "Android share of beta users = 62%", value: "62%"}
    - {id: F11, key: last_release_date, statement: "Last major release shipped on April 22", value: "April 22"}
    - {id: F12, key: legal_review_turnaround, statement: "Legal review turnaround = 5 business days", value: "5 business days"}
personas:
  - name: Maya
    role: Product manager, runs the meeting
    goals: Get a firm launch date today
    hidden_agenda: Already hinted June 3rd to the exec team
    verbosity: 3
    wpm: 165
    catchphrases: ["okay, so", "let's land this"]
    voice_gender: female
  - name: Raj
    role: Engineering lead
    goals: Do not ship with known stability issues
    hidden_agenda: Wants one more week to land the sync refactor
    verbosity: 3
    wpm: 150
    catchphrases: ["to be fair", "honestly"]
    voice_gender: male
  - name: Lena
    role: QA lead
    goals: Make sure the P1 bugs are tracked to closure
    hidden_agenda: Tired of being the last line of defence
    verbosity: 2
    wpm: 155
    catchphrases: ["for the record"]
    voice_gender: female
  - name: Tom
    role: Marketing lead
    goals: A big splashy launch
    hidden_agenda: Already booked a press slot and hasn't told anyone
    verbosity: 5
    wpm: 175
    catchphrases: ["love it", "the thing is"]
    voice_gender: male
---
## crash_metrics :: Stability and performance against the bar; Tom misremembers the crash rate
Maya: Okay, so, thanks everyone. Four things today and I really want to land a date by the end, so let's keep moving.
Tom: Love it. I've got a hard stop at the top of the hour, just so you know.
Maya: Noted. First up, readiness. Raj, Lena, where are we on stability? {question- @+1}
Raj: Honestly, better than I expected two weeks ago. The sync fix helped a lot.
Tom: Yeah, crash-free was like ninety-seven percent last week. That's basically perfect. {claim+ F1 "97%"}
Lena: Hm, that's not the number I have—
Raj: It was ninety-nine point two, Tom. Ninety-seven would actually be a disaster. {claim- F1}
Tom: Oh. Okay, even better then.
Maya: And the bar we agreed for launch was ninety-nine flat, right? {claim- F2} {question- @+1} {~nc}
Lena: Right, ninety-nine. So we're over it, but not by a mile. {claim- F2} {~nc}
Raj: To be fair, last week was a quiet week. Usage was down because of the holiday.
Maya: So you think the number flatters us? {question- @+1}
Raj: A little. I'd want to see it hold with normal traffic before I get excited.
Tom: The thing is, it's never going to be a normal week, there's always something.
Lena: For the record, the crash clusters we do have are almost all on older Android devices.
Maya: How much of the beta is Android these days? {question- @+1}
Lena: About sixty-two percent of active testers. {claim- F10}
Tom: Which makes sense, that's our market.
Raj: Cold start is the other thing. p95 cold start on the release candidate is one point eight seconds. {claim- F3}
Maya: Is that good or bad? I genuinely don't remember what we were aiming for. {question- @+1}
Raj: It's fine. It's not great, but it's fine. Users won't notice on anything from the last three years.
Lena: Older phones they will, though.
Tom: Older phones are slow at everything. Nobody blames the app for that.
Lena: People absolutely blame the app for that. Read the store reviews sometime.
Maya: Okay. And the P1s? How many are still open? {question- @+1} {~}
Lena: Three. Two are on the sync screen and one is the login loop on tablets. {claim- F4}
Raj: The login loop is nasty. That one I don't want to ship with.
Maya: Is anyone actually on it right now? {question- @+1}
Raj: Dmitri was looking at it on Friday, but he got pulled onto the payments thing.
Lena: Which is how it always goes.
Raj: Fine. I'll pair with Dmitri on the tablet login loop tomorrow morning and get a fix into the next build. {action+}
Maya: Great, thank you.
Lena: And someone should probably keep an eye on the other two sync ones at some point. {action-}
Tom: Do we have any data on how many people actually hit the login thing? {question+} {~}
Raj: Anyway, the sync ones are lower risk, they only show up when you're offline for days.
Maya: Okay. Overall, it sounds like the metrics are basically there, with the tablet bug as the open risk.
Raj: That's fair. I'd say metrics are a soft yes, for now. {decision-}
## store_assets :: Screenshots and copy are behind; legal review timing is fuzzy
Maya: Let's move to the store listing. Tom, how are the assets looking? {question- @+1}
Tom: Screenshots are mostly done. The copy is done, it's great, I'm really happy with it.
Lena: Are the screenshots from the release candidate or the old build? {question- @+1}
Tom: Mix. The onboarding ones are from the old build, which, yeah, I know.
Raj: The onboarding flow changed quite a bit, so those will look wrong.
Tom: It's three screens, it's not a big deal to redo them.
Maya: Who's redoing them, though? Design is slammed this week. {question- @+1}
Tom: I'll grab the new onboarding screenshots from the RC myself and get them to design by Wednesday. {action+}
Maya: Perfect.
Lena: Has legal looked at the copy yet? There's the line about "clinically proven" that worried me. {question- @+3}
Tom: That line is staying, it tested really well.
Maya: Tom, that's not really what she asked.
Tom: Right, sorry. No, legal hasn't seen it yet. It's going over this week.
Raj: Legal usually takes two weeks on anything health-related. {claim+ F12 "two weeks"}
Maya: I thought it was faster than that these days.
Lena: It's five business days, that's what they told us after the last release. {claim- F12}
Tom: Five days is fine. That still works. {claim- F12}
Maya: Okay, but it has to actually go to them first.
Raj: Maybe we drop the clinically proven line to be safe? {decision-} {question- @+1}
Tom: Let's not decide that without seeing what legal says.
Maya: Yeah, let's see what legal says first and come back to it. {decision-}
Lena: And store review on top of that is usually a couple of days. {claim- F7}
Tom: Two days, yeah, Apple's been quick lately. {claim- F7}
Raj: Side note, has anyone else noticed the coffee machine on four is broken again? {drift- 2} {question- @+1}
Lena: Since Monday. It's a tragedy.
Maya: So legal plus store review is a fair bit of runway, minimum.
Raj: Before anything else goes wrong, yes.
## launch_date :: The real fight: June 3rd vs one more week; a drift into Tom's marathon
Maya: Okay, which brings us to the date. I'd love to land on June 3rd. {~}
Raj: I figured you'd say that.
Tom: June 3rd is great for us. It lines up with the newsletter. {~}
Raj: Honestly, I'd rather go on the tenth. One more week lets the sync refactor land properly.
Lena: We should really get the refactor reviewed by someone outside the team, whatever the date. {action-}
Maya: What does the refactor give us that users would actually notice? {question- @+1}
Raj: Fewer of those offline sync crashes, mostly. It's the stuff that hits the long-tail devices.
Lena: Which is where most of our crashes are.
Tom: Can we ship the refactor in a point release after? {question- @+1}
Raj: We could. It's just riskier to ship the big change after everyone's already on 2.0. {~}
Maya: How many people are in the beta now? {question- @+1}
Tom: Something like six thousand. It's been growing like crazy. {claim+ F5 "6,000"}
Lena: It's forty-two hundred active. Six thousand is total sign-ups. {claim- F5}
Tom: Active, sign-ups, whatever, it's a lot of people.
Maya: And they're happy? What did the beta NPS land at? {question- @+1}
Tom: Fifty-one, which for health apps is honestly amazing. {claim+ F6 "51"}
Lena: For the record, it was forty-one in the last survey. {claim- F6}
Tom: Huh. I could swear I saw a higher number somewhere.
Raj: Maybe that was the iOS-only cut.
Maya: Either way, it's decent. Okay. Tom, unrelated, but how was the marathon? {drift+ 4} {question- @+1}
Tom: Oh, brutal. Near the end I genuinely thought I was going to die.
Lena: Did you finish under four hours in the end? {question- @+1}
Tom: Just over. So close. My knees are still not speaking to me.
Raj: Okay, back to the date. Where does that leave us? {question- @+1}
Maya: Right. So the honest version is June 3rd with the refactor as a fast follow, or the tenth with it in. {~}
Tom: The thing is, I've sort of already got a press slot on the third.
Maya: You've what? {~}
Tom: It's soft! It's a soft hold. It can move, probably.
Lena: That's the first I'm hearing of this.
Raj: Same.
Maya: Okay. Let's not make the press slot the reason we pick a date. {decision-}
Raj: Agreed.
Maya: Here's where I am. Tablet login fix is a must, refactor is a nice-to-have. {decision-}
Raj: I can live with that, as long as the login loop is fixed and verified.
Lena: Verified by QA, not just merged.
Maya: Fine. Then we're going with June 3rd, conditional on the tablet login fix passing QA by the twenty-eighth. That's the call. {decision+} {~}
Tom: Love it.
Raj: Okay. Then the refactor is the one thing still hanging.
Lena: Just to check, if the login fix slips, the date slips too? {question- @+1}
Maya: Yes. If it slips, we move to the tenth. No debate. {decision+}
Tom: Can I tell the press contact it's the third, then? {question- @+1}
Maya: You can tell them it's likely, not final.
Lena: I'll write up the QA sign-off criteria for the login fix today so there's no argument later. {action+}
Raj: Good. And the refactor ships in 2.0.1, not 2.0. That's decided. {decision+} {~}
## comms_plan :: Announcement, support readiness and budget; one question never gets answered
Maya: Last item, comms and support. Tom, the announcement.
Tom: Blog post, newsletter, and the in-app banner on launch day. Plus paid social for two weeks.
Raj: What's the paid social spend? {question+} {~}
Tom: We've got a hundred and twenty grand for the whole launch. {claim+ F8 "$120,000"}
Maya: I have eighty-five thousand in the plan, not a hundred and twenty. {claim- F8}
Tom: Eighty-five was before the press stuff. {claim- F8}
Maya: There is no "before the press stuff", the budget is the budget.
Lena: Is support ready for a spike? Last launch they got hammered. {question- @+1}
Maya: They've trained fourteen agents on 2.0 so far. {claim- F9}
Lena: Fourteen is fewer than last time. {claim- F9}
Raj: Last time we shipped on April twenty-second and support was underwater for a week. {claim- F11}
Maya: Maybe we keep a couple of engineers on support rotation for launch week. {decision-}
Raj: Maybe. I'd want to think about who, honestly.
Tom: We could also just put a really good FAQ up.
Lena: An FAQ doesn't answer the phone.
Maya: Who on the support side is actually signing off that they're ready? {question+} {~}
Tom: Anyway, I'll draft the launch blog post and send it round by Friday. {action+}
Raj: Send it to me as well, I want to check the technical claims.
Tom: Sure, sure. {action+}
Lena: Someone should probably update the release notes template too, it still says 1.9. {action-} {~}
Maya: Okay. Should we do a dry run of the launch day checklist? {question- @+1}
Raj: Probably worth it, the last one caught two things.
Maya: Let's maybe do the dry run next Thursday, if people are around. {decision-}
Tom: I'm around Thursday.
Lena: I might be at the vendor thing, I'll know Monday. {~}
Maya: Okay. I think that's everything. Recap is in the doc. Thanks all.
Raj: Thanks.
Tom: Thanks, team. Big launch!
