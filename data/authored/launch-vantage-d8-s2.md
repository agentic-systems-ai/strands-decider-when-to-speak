---
meeting_id: launch-vantage-d8-s2
theme: Go/no-go for the Aurora mobile app launch
domain_pack: product_launch
drama: 0.8
seed: 2
author: claude-opus-5-5 (Claude Code session)
pack:
  title: Aurora 3.0 launch - go/no-go
  org: Vantage Fitness (fictional)
  agenda:
    - {id: readiness, title: App readiness, goal: Stability against the bar, timebox_min: 4}
    - {id: billing, title: Billing migration, goal: Decide whether the subscription migration is safe, timebox_min: 5}
    - {id: marketing, title: Launch campaign, goal: Size the campaign to what support can handle, timebox_min: 4}
    - {id: call, title: The call, goal: Go or no-go for January 6, timebox_min: 3}
  facts:
    - {id: F1, key: crash_free_sessions, statement: "Crash-free sessions = 98.7%", value: "98.7%"}
    - {id: F2, key: crash_free_target, statement: "Crash-free target = 99.5%", value: "99.5%"}
    - {id: F3, key: billing_users, statement: "Subscribers to migrate to the new billing system = 42,000", value: "42,000"}
    - {id: F4, key: billing_error_rate, statement: "Billing errors in the migration test = 1.2%", value: "1.2%"}
    - {id: F5, key: influencer_budget, statement: "Influencer campaign budget = $60,000", value: "$60,000"}
    - {id: F6, key: launch_date, statement: "Planned launch = January 6", value: "January 6"}
    - {id: F7, key: waitlist, statement: "Waitlist sign-ups = 15,000", value: "15,000"}
    - {id: F8, key: support_agents, statement: "Support agents = 9", value: "9"}
    - {id: F9, key: expected_tickets, statement: "Expected tickets in launch week = 4,000", value: "4,000"}
    - {id: F10, key: store_approval, statement: "App Store approval received December 18", value: "December 18"}
    - {id: F11, key: monthly_price, statement: "Monthly price = $12.99", value: "$12.99"}
    - {id: F12, key: beta_churn, statement: "Beta churn = 7% per month", value: "7%"}
personas:
  - name: Brooke
    role: Founder and CEO
    goals: Launch on January 6, the New Year's resolution window
    hidden_agenda: Investors were promised January numbers
    verbosity: 4
    wpm: 180
    catchphrases: []
    voice_gender: female
  - name: Ian
    role: CTO
    goals: Don't break billing for 42,000 paying people
    hidden_agenda: Has a resignation letter half-written
    verbosity: 3
    wpm: 150
    catchphrases: []
    voice_gender: male
  - name: Nadine
    role: Head of support
    goals: A launch her team can survive
    hidden_agenda: Two agents just gave notice
    verbosity: 3
    wpm: 160
    catchphrases: []
    voice_gender: female
  - name: Arturo
    role: Growth marketer
    goals: The biggest launch campaign the company has run
    hidden_agenda: Already signed three influencer contracts
    verbosity: 4
    wpm: 185
    catchphrases: []
    voice_gender: male
---
## readiness :: Brooke claims the bar is met; Ian disagrees
Brooke: Okay, let's go. We're at ninety-nine and a half crash-free, we hit the target, so readiness is a yes. {claim+ F1 "99.5%"}
Ian: We're at ninety-eight point seven. The target is ninety-nine five. We haven't hit it. {claim- F1} {claim- F2}
Brooke: Ninety-eight seven, ninety-nine five. That's a rounding difference. {claim- F1} {claim- F2}
Ian: It's twice as many crashes. On a workout app, a crash mid-workout is a one-star review.
Arturo: Users don't care about decimals, Ian.
Ian: They care when the timer resets in the middle of a sprint interval.
Nadine: Where are the crashes? {question- @+1}
Ian: The new video player on older Android phones. We have a fix in testing.
Brooke: When does the fix ship? {question- @+1}
Ian: If testing goes well, the thirtieth. {~}
Brooke: Then readiness is a yes, pending the thirtieth. {decision-}
Ian: Pending. That's not a yes.
## billing :: The migration; the error rate argument
Brooke: Billing. Ian.
Ian: We're moving forty-two thousand subscribers to the new billing system. The test run had one point two percent errors. {claim- F3} {claim- F4}
Brooke: Half a percent is nothing. That's basically clean. {claim+ F4 "0.5%"}
Nadine: One percent of forty-two thousand is four hundred people charged wrong. {~} {claim- F3} {claim- F4}
Arturo: Can't we just refund anyone who complains? {question- @+1}
Ian: We can, but people who get double-charged at twelve ninety-nine don't complain. They cancel. {claim- F11}
Nadine: Our beta churn is already seven percent a month. {claim- F12}
Brooke: So what do you want, Ian? {question- @+1}
Ian: Launch the app on the sixth, but don't migrate billing until February. Run both systems for a month.
Brooke: Two billing systems for a month. That's twice the work.
Ian: It's twice the work instead of four hundred angry people. {~}
Brooke: Fine. Billing migrates in February. The app launches without it. {decision+}
Ian: Thank you. I'll keep both systems running and write the cutover plan for February. {action+} 
Nadine: It'd be nice if engineering looked over the help articles before launch, too. {action-}
## marketing :: The campaign vs support capacity; Nadine's agent count is wrong at first; a tangent about a ski trip
Arturo: The campaign. We have sixty thousand for influencers and the waitlist is at fifty thousand. {claim- F5} {claim+ F7 "50,000"}
Brooke: Fifty thousand people waiting. That's the story. {claim+ F7 "50,000"}
Nadine: How many tickets are we expecting launch week? {question- @+1}
Arturo: Our model says about four thousand. {claim- F9}
Nadine: With twelve agents, that's over three hundred tickets each. In one week. {claim+ F8 "12"}
Ian: Twelve? I thought two people just left. {question- @+1} {~nc}
Nadine: They did. Sorry, I'm still counting them. Nine agents. {claim- F8}
Brooke: Nine. Then we hire temps. {claim- F8}
Arturo: I was on the slopes in Whistler last week and three people in the lift line had the app. {drift+ 3}
Brooke: In Whistler! That's the demographic.
Ian: Did you actually ski, or just count app users? {~}
Nadine: Can we hire temps before the sixth? {question- @+1}
Brooke: We can. I'll approve the budget for four temps today. {action+}
Ian: I just checked the waitlist dashboard. It's fifteen thousand, not fifty. {claim- F7}
Arturo: Fifteen. I was looking at the email list. {claim- F7}
Brooke: Fifteen is still great. {claim- F7}
Arturo: Maybe we hold back half the influencer posts until week two, when support has caught up. {decision-}
Nadine: That would help us a lot.
Brooke: Let's see how week one goes before we hold anything back. {decision-}
Arturo: I've already signed three of the influencer contracts. They post on the sixth.
Ian: You signed contracts? Before this meeting? {~}
Arturo: They were going to go to a competitor.
## call :: Go or no-go
Brooke: The call. January sixth. Go. {claim- F6}
Ian: Conditional go. The crash fix ships, and billing stays where it is.
Nadine: And the temps start before launch.
Brooke: Fine. Conditional go for January sixth: crash fix in, billing in February, temps by launch. {decision+} {claim- F6}
Nadine: Could someone tell the support team tonight, so they hear it from us first? {question- @+1}
Ian: I'll write to them. They should hear it from the CTO. {action+}
Brooke: Is the App Store approval still valid for the new build? {question- @+1}
Ian: The approval from the eighteenth covers this version. The crash fix needs a fast re-review. {claim- F10}
Arturo: Who's telling investors that billing moved to February? {question+} {~}
Brooke: Okay. We launch on the sixth. Good work, everyone.
