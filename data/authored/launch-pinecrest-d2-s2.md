---
meeting_id: launch-pinecrest-d2-s2
theme: Go/no-go for the Aurora mobile app launch
domain_pack: product_launch
drama: 0.2
seed: 2
author: claude-opus-5-5 (Claude Code session)
pack:
  title: Aurora library app - launch review
  org: Pinecrest Library System (fictional)
  agenda:
    - {id: beta, title: Beta results, goal: Review how patrons used the beta, timebox_min: 5}
    - {id: quality, title: Quality and access, goal: Stability, login and accessibility, timebox_min: 5}
    - {id: branches, title: Branch readiness, goal: Make sure every branch can support the app, timebox_min: 4}
    - {id: decision, title: Decision, goal: Go or no-go for September 9, timebox_min: 3}
  facts:
    - {id: F1, key: beta_patrons, statement: "Beta patrons = 1,900", value: "1,900"}
    - {id: F2, key: crash_free, statement: "Crash-free sessions = 99.7%", value: "99.7%"}
    - {id: F3, key: crash_target, statement: "Crash-free target = 99.5%", value: "99.5%"}
    - {id: F4, key: holds_placed, statement: "Holds placed in the beta = 6,400", value: "6,400"}
    - {id: F5, key: ebook_checkouts, statement: "E-book checkouts in the beta = 3,150", value: "3,150"}
    - {id: F6, key: branches, statement: "Library branches = 12", value: "12"}
    - {id: F7, key: open_bugs, statement: "Open bugs = 8", value: "8"}
    - {id: F8, key: staff_trained, statement: "Staff trained on the app = 64", value: "64"}
    - {id: F9, key: launch_date, statement: "Planned launch = September 9", value: "September 9"}
    - {id: F10, key: screen_reader_issues, statement: "Open screen-reader issues = 2", value: "2"}
    - {id: F11, key: login_failures, statement: "Login failure rate = 1.4%", value: "1.4%"}
    - {id: F12, key: card_holders, statement: "Active library card holders = 48,000", value: "48,000"}
personas:
  - name: Margot
    role: Director of digital services, chairs
    goals: A launch that works for every patron, including the oldest
    hidden_agenda: The library board wants the app live before the budget hearing
    verbosity: 3
    wpm: 145
    catchphrases: []
    voice_gender: female
  - name: Elliot
    role: Development lead (contractor)
    goals: Launch on schedule
    hidden_agenda: His contract renewal depends on a smooth launch
    verbosity: 3
    wpm: 160
    catchphrases: []
    voice_gender: male
  - name: Fatou
    role: Accessibility and outreach librarian
    goals: The app works with screen readers and for people new to smartphones
    hidden_agenda: Runs a weekly phone-skills class for seniors and knows what confuses them
    verbosity: 3
    wpm: 150
    catchphrases: []
    voice_gender: female
  - name: Stan
    role: IT operations
    goals: No surprises for the help desk
    hidden_agenda: The login system is old and he worries about it
    verbosity: 2
    wpm: 140
    catchphrases: []
    voice_gender: male
---
## beta :: How patrons used it
Margot: Good afternoon, everyone. Let's start with the beta. Elliot, what did patrons actually do with it? {question- @+1}
Elliot: About nineteen hundred patrons used the beta over six weeks. The most popular thing by far was holds. They placed sixty-four hundred holds through the app. {claim- F1} {claim- F4}
Fatou: That matches what I hear at the desk. People love not having to call.
Stan: The phone line has been quieter, actually. I noticed that before I knew why.
Margot: And e-books? {question- @+1}
Elliot: Thirty-one fifty checkouts. Fewer than holds, but growing every week. {claim- F5}
Fatou: Some of the older patrons didn't know e-books were free. The app is the first time they've seen them.
Margot: That's lovely to hear. That's the whole point of the thing.
Stan: Did people use the barcode on the phone instead of the plastic card? {question- @+1}
Elliot: More than we expected. At the main branch the self-checkout machines read it fine.
Fatou: At the smaller branches the scanners are older. A few struggled with phone screens.
Margot: Which branches? {question- @+1}
Fatou: Riverside and the bookmobile, mostly. Bright screens confuse the old scanners.
Stan: Those scanners are on the replacement list. Next year, I think.
Fatou: Should we hold the launch at those two until the scanners are replaced? {decision-} {question- @+1}
Margot: Then for now we tell patrons at those two to bring the plastic card as well. {decision+}
Fatou: I'll put a note in the app's help section about the older scanners. {action+}
## quality :: Stability, login and screen readers; Elliot's login figure is challenged and corrected
Margot: Quality. How stable is it? {question- @+1}
Elliot: Crash-free sessions were ninety-nine point seven percent. Our target is ninety-nine five. {claim- F2} {claim- F3}
Stan: So we're above the bar. Good.
Elliot: And login failures are down to about half a percent. {claim+ F11 "0.5%"}
Stan: Hmm. I'm not sure about that. The help desk log felt worse than half a percent. More like one in a hundred. {~nc}
Elliot: You might be right. Let me look properly. Yes, it's one point four. Half a percent was iOS on its own. {claim- F11}
Margot: One point four percent of people can't log in. That's a lot of frustrated patrons. {claim- F11}
Stan: Most of it is people who've forgotten their PIN. The old system makes resetting it painful.
Fatou: In my class, half the questions are about PINs. People write them on the back of the card.
Margot: Can the app make resetting a PIN easier? {question- @+1}
Elliot: It can link straight to the reset page. That's a small change.
Stan: The reset page itself is the problem. It's from two thousand eleven. {~nc}
Margot: Let's do the link now, and look at replacing the reset page after launch. {decision+}
Elliot: I'll add the reset link this week. {action+}
Fatou: Screen readers. There are still two issues open. {claim- F10}
Margot: Are they serious? {question- @+1}
Fatou: One is. The hold confirmation isn't announced, so a blind patron doesn't know if the hold worked.
Elliot: That one we can fix before launch. The other is a label on the settings page.
Fatou: Both, ideally. It's not much.
Elliot: Both, then. They're small. {action+}
Margot: And general bugs? {question- @+1}
Elliot: Eight open. None of them stop anyone doing anything. {claim- F7}
## branches :: Readiness across the system; Margot's branch count is off and stays off
Margot: Branches. We have fifteen branches, and every one needs to be able to help a patron with the app. {claim+ F6 "15"}
Stan: Sixty-four staff have done the training so far. {claim- F8}
Fatou: Mostly from the bigger branches. The small ones have one or two people on shift.
Margot: How do we cover the small ones? {question- @+1}
Fatou: A one-page guide at every desk, with screenshots. People can follow it even if they haven't done the training.
Stan: And the help desk number on the bottom, for anything harder.
Margot: I like that. A one-page guide at every desk, then. {decision+} {~}
Fatou: I'll design it and get it printed before launch. {action+}
Stan: My daughter just started at the community college, by the way. She says their library app is terrible. {drift+ 3}
Elliot: Most university library apps are terrible. They're built by committees.
Fatou: Ours is built by a committee too, if we're honest.
Margot: Well, a careful committee. Let's get back to it.
Stan: The help desk needs to know the launch date before anything goes public. {~}
Elliot: It'd be good if someone wrote up the five questions the help desk will get most. {action-}
Stan: I can do that. I already know what they'll be. {action+}
## decision :: Go or no-go
Margot: So. Are we ready for September ninth? {question- @+1} {claim- F9}
Elliot: From the development side, yes, with the reset link and the two screen-reader fixes.
Fatou: Yes, if the hold confirmation is announced. That's the one I care about.
Stan: Yes. The help desk will be ready.
Margot: Then it's a go for September ninth, with those fixes in. {decision+} {claim- F9}
Fatou: Will we tell all forty-eight thousand card holders at once, or start smaller? {question- @+1} {claim- F12}
Margot: An email to everyone, but we start the promotion at the branches the week before. {decision+} {~}
Stan: Has anyone asked the board whether they want a launch event? {question+} {~}
Elliot: I'll send the final build to the app stores on the second, so there's time for review. {action+}
Margot: Thank you, all. This has been a careful piece of work.
