---
meeting_id: launch-marlowe-d5-s2
theme: Go/no-go for the Aurora mobile app launch
domain_pack: product_launch
drama: 0.5
seed: 2
author: claude-opus-5-5 (Claude Code session)
pack:
  title: Aurora guest app - launch decision
  org: Marlowe Hotels (fictional)
  agenda:
    - {id: pilot, title: Pilot results, goal: Review the mobile check-in and digital key pilot, timebox_min: 5}
    - {id: hotel_ops, title: Hotel readiness, goal: Confirm the front desks are ready, timebox_min: 4}
    - {id: security, title: Security review, goal: Close out the penetration test, timebox_min: 3}
    - {id: launch_call, title: Launch call, goal: Decide on June 10 and the rollout order, timebox_min: 3}
  facts:
    - {id: F1, key: pilot_hotels, statement: "Pilot hotels = 7", value: "7"}
    - {id: F2, key: pilot_checkins, statement: "Mobile check-ins in the pilot = 4,350", value: "4,350"}
    - {id: F3, key: checkin_success, statement: "Mobile check-in success rate = 92%", value: "92%"}
    - {id: F4, key: time_saved, statement: "Average time saved per check-in = 6 minutes", value: "6 minutes"}
    - {id: F5, key: key_failures, statement: "Digital key failure rate = 3.5%", value: "3.5%"}
    - {id: F6, key: staff_trained, statement: "Front desk staff trained = 160", value: "160"}
    - {id: F7, key: total_hotels, statement: "Hotels in the chain = 38", value: "38"}
    - {id: F8, key: pentest_open, statement: "Open penetration-test findings = 2 (medium)", value: "2"}
    - {id: F9, key: launch_date, statement: "Planned launch = June 10", value: "June 10"}
    - {id: F10, key: pilot_rating, statement: "Guest rating in the pilot = 4.6", value: "4.6"}
    - {id: F11, key: support_calls_rate, statement: "Support calls per 100 check-ins = 1.8", value: "1.8"}
    - {id: F12, key: loyalty_members, statement: "Loyalty members with email = 210,000", value: "210,000"}
personas:
  - name: Isabel
    role: VP of guest experience, chairs the meeting
    goals: Launch for the summer season
    hidden_agenda: The CEO mentioned the app in an investor call
    verbosity: 3
    wpm: 165
    catchphrases: []
    voice_gender: female
  - name: Femi
    role: Mobile engineering lead
    goals: Launch without the key problems coming back
    hidden_agenda: The lock vendor's SDK is still a black box to his team
    verbosity: 3
    wpm: 155
    catchphrases: []
    voice_gender: male
  - name: Gwen
    role: Director of hotel operations
    goals: Front desks that aren't overwhelmed
    hidden_agenda: Two general managers told her they don't want the app
    verbosity: 3
    wpm: 150
    catchphrases: []
    voice_gender: female
  - name: Rahul
    role: Data analyst for the pilot
    goals: Make sure the numbers are read correctly
    hidden_agenda: Found that the success rate drops at night
    verbosity: 2
    wpm: 160
    catchphrases: []
    voice_gender: male
---
## pilot :: Results; Isabel rounds up the success rate; Femi lowballs key failures and is corrected later
Isabel: Thanks for joining. Let's start with the pilot. The headline is a ninety-eight percent check-in success rate, which is fantastic. {claim+ F3 "98%"}
Rahul: The dashboard says ninety-two. Ninety-eight was the success rate at the iOS hotels only. {claim- F3}
Isabel: Ninety-two, then. Still good. {claim- F3}
Rahul: It is. It drops at night, though. After eleven it's closer to eighty-five. {~}
Gwen: That's when the night auditor is alone at the desk. Exactly when you don't want failures.
Femi: The night drop is the lock vendor's server doing maintenance. We've asked them to move it.
Isabel: How many check-ins was the pilot in total? {question- @+1}
Rahul: Forty-three fifty, across seven hotels. {claim- F2} {claim- F1}
Isabel: And the time saved? {question- @+1}
Rahul: Six minutes per check-in on average. {claim- F4}
Gwen: Six minutes for the guest. Not for the desk when it goes wrong. {claim- F4}
Isabel: What about the digital keys? {question- @+1}
Femi: Key failures are under one percent now. Much better than in March. {claim+ F5 "under 1%"}
Isabel: Good. Guests rated the pilot four point six, which is the highest we've had for anything. {claim- F10} {~nc}
Gwen: Guests who got in. The ones who didn't call the front desk.
Rahul: Support calls were one point eight per hundred check-ins. {claim- F11}
Femi: That's lower than the old kiosk.
Gwen: Hang on. I have the incident log from the Seaport hotel open. Key failures there were three and a half percent last month, not under one. {claim- F5} {~nc}
Femi: Three point five across the chain, yes. Under one was the target after the firmware update, which isn't out yet. {claim- F5} {~nc}
Isabel: Then the firmware update matters for the launch. 
Femi: It does.
## hotel_ops :: Front desk readiness; Gwen's training number stands
Isabel: Hotel readiness. Gwen? {question- @+1}
Gwen: We've trained about a hundred front desk staff so far. {claim+ F6 "100"}
Isabel: Out of how many hotels? {question- @+1}
Gwen: Thirty-eight in the chain, but we'd start with the bigger ones. {claim- F7}
Femi: What do the desk staff do when a digital key fails? {question- @+1}
Gwen: They cut a plastic key, like always. That part's easy. It's the queue that's the problem.
Rahul: Did anyone watch the finale last night? I'm still upset. {drift+ 3} {~}
Femi: Don't. I haven't seen it yet. I'm watching tonight.
Gwen: I stopped after the season with the twins. It got silly.
Isabel: Okay. Could we have a manager on duty at the desk for the first week at each hotel? {question- @+1}
Gwen: For the big ones, yes. For the small ones, it's one person at night anyway.
Isabel: Then the first week has a manager on the desk at every hotel with more than two hundred rooms. {decision+} {~}
Gwen: I'll send the general managers a staffing note on Monday. {action+} 
Femi: Has anyone asked the night auditors what they think of it? {question+} {~}
Rahul: Two general managers have said they don't want the app at all. Is that a problem? {question- @+1}
Gwen: It's a conversation. Not a problem yet.
## security :: The pen test; one owner, one wobble
Isabel: Security. Femi, the pen test.
Femi: Two medium findings are still open. Both are in the key-sharing feature. {claim- F8}
Isabel: Can we launch with them open? {question- @+1}
Femi: I'd rather not. If we turn key sharing off at launch, both findings go away.
Gwen: Guests won't miss key sharing. Most don't know it exists.
Isabel: Then key sharing is off at launch, and we turn it on when the two findings are closed. {decision+} {claim- F8}
Femi: I'll get the flag set and ask the testers to confirm the findings are out of scope. {action+}
Rahul: It'd be worth someone checking how many pilot guests actually used key sharing. {action-}
Isabel: Rahul, you'd know better than anyone. Could you pull that number? {question- @+1}
Rahul: Sure. By tomorrow. {action+}
## launch_call :: June 10, conditionally; the rollout order
Isabel: The call. Are we launching on June tenth? {question- @+3} {claim- F9}
Femi: Only if the firmware update is out. The key failures need to come down first.
Gwen: And not at the two hotels whose managers said no. Not yet.
Isabel: Then June tenth, conditional on the firmware, starting with the twelve biggest hotels. The rest follow in July. {decision+} {claim- F9}
Rahul: Should we email the loyalty members? That's two hundred and ten thousand people. {question- @+1} {claim- F12} {~nc}
Isabel: Not on day one. Let's see the first two weeks before we tell everyone. {decision-} {~}
Gwen: Who tells the CEO it's conditional? {question+}
Femi: When does the lock vendor ship the firmware? Do we have a date? {question- @+1}
Rahul: They said the first week of June. They also said April. {~nc}
Isabel: Thank you, everyone. We'll check in on the firmware next Friday.
