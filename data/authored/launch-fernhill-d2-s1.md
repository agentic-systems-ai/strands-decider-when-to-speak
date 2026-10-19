---
meeting_id: launch-fernhill-d2-s1
theme: Go/no-go for the Aurora mobile app launch
domain_pack: product_launch
drama: 0.2
seed: 1
author: claude-opus-5-5 (Claude Code session)
pack:
  title: Aurora trip planner - go/no-go
  org: Fernhill Transit Authority (fictional)
  agenda:
    - {id: quality, title: Quality, goal: Review stability, bugs and trip-plan accuracy, timebox_min: 5}
    - {id: accessibility, title: Accessibility, goal: Confirm the audit status and remaining issues, timebox_min: 4}
    - {id: operations, title: Operations readiness, goal: Support, the real-time feed and the press plan, timebox_min: 4}
    - {id: decision, title: Go/no-go, goal: Make the call for March 3, timebox_min: 3}
  facts:
    - {id: F1, key: crash_free_users, statement: "Crash-free users in beta = 99.6%", value: "99.6%"}
    - {id: F2, key: crash_free_target, statement: "Crash-free target for launch = 99.5%", value: "99.5%"}
    - {id: F3, key: open_sev2_bugs, statement: "Open severity-2 bugs = 5", value: "5"}
    - {id: F4, key: wcag_issues_open, statement: "Open WCAG issues = 4", value: "4"}
    - {id: F5, key: beta_riders, statement: "Beta riders = 2,800", value: "2,800"}
    - {id: F6, key: trip_plan_accuracy, statement: "Trip plans matching actual arrivals within 2 minutes = 96%", value: "96%"}
    - {id: F7, key: beta_rating, statement: "Beta store rating = 4.4", value: "4.4"}
    - {id: F8, key: support_staff_trained, statement: "Customer service staff trained = 22", value: "22"}
    - {id: F9, key: launch_date, statement: "Planned launch = March 3", value: "March 3"}
    - {id: F10, key: realtime_feed_uptime, statement: "Real-time feed uptime last 30 days = 99.1%", value: "99.1%"}
    - {id: F11, key: press_release_date, statement: "Press release = February 27", value: "February 27"}
    - {id: F12, key: screen_reader_sessions, statement: "Screen-reader test sessions run = 9", value: "9"}
personas:
  - name: Helen
    role: Director of digital services, chairs the review
    goals: A launch the agency won't have to apologize for
    hidden_agenda: The board chair rides the 14 bus and will try the app on day one
    verbosity: 3
    wpm: 145
    catchphrases: []
    voice_gender: female
  - name: Sipho
    role: QA lead
    goals: No surprises after launch
    hidden_agenda: Wants one more regression pass he hasn't asked for yet
    verbosity: 2
    wpm: 150
    catchphrases: ["for completeness"]
    voice_gender: male
  - name: Marta
    role: Accessibility and research lead
    goals: Riders with disabilities can use it from day one
    hidden_agenda: Ran some test sessions informally and counts them
    verbosity: 3
    wpm: 155
    catchphrases: []
    voice_gender: female
  - name: Jonah
    role: Engineering manager
    goals: Launch on time
    hidden_agenda: The real-time feed vendor has been flaky and he's nervous
    verbosity: 3
    wpm: 160
    catchphrases: ["so"]
    voice_gender: male
---
## quality :: Stability, bugs and accuracy; Jonah undercounts the bugs and Sipho corrects him
Helen: Thank you all for coming. We'll go through quality, accessibility and operations, and then make the call. Sipho, would you start with stability? {question- @+1}
Sipho: Crash-free users in the beta are at ninety-nine point six percent. {claim- F1} {~}
Helen: Against a target of ninety-nine point five. {claim- F2} {~nc}
Sipho: Yes. Just above. For completeness, the beta is small, so I'd treat that as encouraging rather than proven.
Helen: How many riders are in the beta now? {question- @+1}
Jonah: Twenty-eight hundred. Mostly on the busier routes. {claim- F5}
Marta: Which skews toward commuters. We have fewer older riders than I'd like.
Helen: That's worth noting. What about bugs? {question- @+1}
Jonah: So, we're down to two severity-two bugs, which I'm pleased about. {claim+ F3 "2"}
Sipho: I have five open in the tracker. Two were fixed this week, which might be what you're thinking of. {claim- F3}
Jonah: Ah, yes. Five open, two fixed. You're right. {claim- F3}
Helen: What are the five? {question- @+1} {claim- F3}
Sipho: Three are display issues on older Android phones. One is a timetable that doesn't refresh after midnight. One is the fare calculator rounding.
Helen: The fare calculator rounding sounds like the kind of thing that ends up in the newspaper.
Jonah: It's a few cents in edge cases, but I agree it's visible.
Sipho: For completeness, the midnight timetable one worries me more. Night riders depend on it.
Jonah: The midnight refresh is a small fix. I'll have someone on it tomorrow and aim to close it this week. {action+}
Helen: And accuracy? Are trip plans matching reality? {question- @+1}
Jonah: Ninety-six percent of trip plans match actual arrivals within two minutes. {claim- F6}
Marta: Riders in the interviews said it felt more accurate than the old app.
Helen: That's encouraging. And the store rating in beta? {question- @+1}
Sipho: Four point four, from about three hundred reviews. {claim- F7} {~}
Helen: All right. Quality looks reasonable, with the midnight timetable and the fare rounding as the two to watch.
Jonah: It snowed so much on the north side this morning that the 22 didn't run at all. {drift+ 2} {~nc}
Sipho: My street still hasn't been plowed. I walked to the train in hiking boots.
## accessibility :: Audit status; Marta's session count is higher than the record and stays that way
Helen: Let's move on. Marta, accessibility? {question- @+1}
Marta: We've closed most of the audit. Four WCAG issues are still open. {claim- F4}
Helen: Are any of them blockers? {question- @+1}
Marta: One is. The route map can't be explored with a screen reader. The other three are contrast and labels.
Jonah: The route map is the hardest one. It's a custom component.
Marta: We've run twelve screen-reader test sessions so far, and the map came up in almost every one. {claim+ F12 "12"}
Helen: Then the map matters. What would it take to fix it? {question- @+1}
Jonah: A text alternative for the map, listing the stops in order, is about a week of work.
Marta: That would actually be better for a lot of people, not just screen-reader users.
Sipho: I can put that alternative through a regression pass once it's ready. {action+}
Helen: Thank you, Sipho. Jonah, would a week fit before March third? {question- @+1} {claim- F9}
Jonah: It would be tight, but yes, if we start Monday.
Helen: Then the text alternative for the route map is a launch requirement. {decision+}
Marta: I'll sit with the developers on Monday and go through what the text version needs to say. {action+}
Jonah: Could we ship the contrast fixes in the first update instead of at launch? {question- @+1} {decision-}
Marta: I'd prefer launch, but the contrast issues are minor. I can live with the first update.
Helen: Let's look at how the week goes before we decide on the contrast fixes. {decision-} 
Jonah: Fair.
## operations :: Support, the real-time feed and the press release date
Helen: Operations. Who's ready on the support side? {question- @+1}
Marta: Customer service has trained twenty-two people on the new app. {claim- F8}
Sipho: Is that enough for launch week? {question- @+1}
Helen: It's more than we had for the last app. I think it's enough.
Jonah: The thing that worries me is the real-time feed. Uptime was ninety-nine point one percent over the last month. {claim- F10}
Sipho: For completeness, that's about six or seven hours of the feed being down in a month. {~}
Helen: What happens in the app when the feed is down? {question- @+1}
Jonah: It falls back to the timetable, with a little banner. Riders can still plan trips.
Marta: The banner needs to be read out by a screen reader too. I'll check that it is. {action+}
Jonah: Sorry, my connection dropped for a second. What did I miss? {drift- 2} {question- @+1}
Helen: Only Marta checking the banner. Nothing else. 
Jonah: Got it, thanks. {~}
Helen: And the press release goes out on the twenty-fifth, I believe. {claim+ F11 "February 25"}
Jonah: I'll ask the vendor for their maintenance calendar, so nothing's planned for launch week. {action+}
Sipho: It might be worth having someone from engineering on call that first weekend. {action-}
Marta: Communications sent the schedule this morning. The press release is the twenty-seventh, not the twenty-fifth. {claim- F11}
Helen: The twenty-seventh. Thank you, Marta. {claim- F11} 
Sipho: Good catch.
## decision :: The call
Helen: So. Are we ready to go on March third? {question- @+3} {claim- F9}
Sipho: With the midnight timetable fixed and the route map alternative in, I'm comfortable.
Marta: Same conditions for me. The map has to be in.
Jonah: Agreed. We can do both.
Helen: Then it's a go for March third, on those two conditions. {decision+} {claim- F9}
Sipho: For completeness, I'd like one more full regression pass the week before. Is that possible? {question- @+1}
Jonah: Yes. We'll freeze the code on the twenty-fourth to make room for it. {action+}
Sipho: Then I'll run the full regression pass starting on the twenty-fifth. {action+}
Helen: Who will tell the board chair? He'll be on the 14 bus on day one. {question+} {~}
Jonah: Has anyone checked how the app behaves on the old tablets in the bus shelters? {question+} {~}
Helen: Thank you, everyone. A careful review. We'll meet again the week before launch.
