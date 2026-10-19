---
meeting_id: sprint-ledgerly-d8-s1
theme: Sprint planning for a payments team at a fictional fintech
domain_pack: software_team
drama: 0.8
seed: 1
author: claude-opus-5-5 (Claude Code session)
pack:
  title: Card platform team - sprint 41 planning
  org: Ledgerly (fictional payments startup)
  agenda:
    - {id: review, title: Last sprint review, goal: Be honest about what shipped and what didn't, timebox_min: 4}
    - {id: scope, title: Sprint scope, goal: Choose between the chargeback flow and the PCI audit fixes, timebox_min: 5}
    - {id: estimates, title: Estimates, goal: Size the chosen work and check it fits, timebox_min: 4}
    - {id: team, title: Team health and on-call, goal: Sort out the on-call load and the hiring gap, timebox_min: 3}
  facts:
    - {id: F1, key: committed_points, statement: "Points committed last sprint = 45", value: "45"}
    - {id: F2, key: delivered_points, statement: "Points delivered last sprint = 29", value: "29"}
    - {id: F3, key: pci_findings_open, statement: "Open PCI audit findings = 6", value: "6"}
    - {id: F4, key: pci_deadline, statement: "PCI remediation deadline = December 15", value: "December 15"}
    - {id: F5, key: chargeback_rate, statement: "Chargeback rate last month = 0.9%", value: "0.9%"}
    - {id: F6, key: chargeback_fees_monthly, statement: "Chargeback fees last month = $14,200", value: "$14,200"}
    - {id: F7, key: engineers_on_team, statement: "Engineers on the team = 5", value: "5"}
    - {id: F8, key: open_headcount, statement: "Open engineering roles = 2", value: "2"}
    - {id: F9, key: oncall_pages, statement: "Pages last sprint = 23", value: "23"}
    - {id: F10, key: p1_incidents, statement: "P1 incidents last sprint = 2", value: "2"}
    - {id: F11, key: merchant_escalations, statement: "Merchant escalations about chargebacks = 17", value: "17"}
    - {id: F12, key: sprint_end_date, statement: "This sprint ends November 21", value: "November 21"}
personas:
  - name: Rachel
    role: Engineering manager
    goals: Stop over-committing
    hidden_agenda: Her skip-level asked why the team keeps missing
    verbosity: 3
    wpm: 165
    catchphrases: ["okay, real talk", "hang on"]
    voice_gender: female
  - name: Dev
    role: Staff engineer
    goals: Do the PCI fixes before the auditors come back
    hidden_agenda: Thinks product doesn't understand the audit risk
    verbosity: 4
    wpm: 160
    catchphrases: ["the reality is", "I mean"]
    voice_gender: male
  - name: Carmen
    role: Product manager for merchant tools
    goals: Ship the chargeback flow this sprint
    hidden_agenda: Promised two big merchants a date
    verbosity: 4
    wpm: 175
    catchphrases: ["merchants are screaming", "okay but"]
    voice_gender: female
  - name: Oskar
    role: Engineer, carries most of the on-call
    goals: Fewer pages, more sleep
    hidden_agenda: Has a job offer elsewhere
    verbosity: 2
    wpm: 145
    catchphrases: ["sure", "whatever works"]
    voice_gender: male
---
## review :: The miss; Carmen remembers the delivery as better than it was
Rachel: Okay, real talk. Last sprint we committed forty-five points and we did not get close. {claim- F1}
Carmen: We got most of it, though. Like thirty-eight? {claim+ F2 "38"} {~}
Dev: The board says twenty-nine. {claim- F2}
Carmen: Twenty-nine? Hang on, that can't include the dispute API work. {claim- F2} {~}
Rachel: It includes it. It was split across two tickets and one didn't close.
Oskar: The two P1s didn't help. Each one ate a day of somebody. {claim- F10}
Dev: The reality is we plan like nobody gets paged and then everybody gets paged.
Carmen: Okay but that's every team.
Dev: It's not every team. Most teams don't own card authorization.
Carmen: Ugh, Slack is on fire over here. Ignore my face. {drift- 1}
Rachel: Hang on, let's not do this again. The question is what we change.
Oskar: Plan for the pages. That's what we change.
Rachel: How many pages were there, Oskar? {question- @+1}
Oskar: Twenty-three. Most of them at night. {claim- F9}
Carmen: Twenty-three? That's insane. {claim- F9} {~}
Oskar: Sure. It was.
Rachel: Okay. Then this sprint we plan to what we actually delivered, not what we wish we'd delivered. {decision+}
Dev: I mean, that's the first sensible thing anyone's said about planning all year.
## scope :: Chargebacks vs PCI; a shouting match; Dev overstates the PCI findings and Rachel catches it much later
Rachel: Scope. Carmen, you want the chargeback flow.
Carmen: Merchants are screaming. We had seventeen escalations about chargebacks last month. {claim- F11}
Dev: And we have ten open PCI findings. Auditors don't scream, they just fail you. {claim+ F3 "10"}
Carmen: Okay but the chargeback rate is like two percent. We're paying for every one of them. {claim+ F5 "2%"}
Rachel: What did chargebacks actually cost us last month? {question- @+1}
Carmen: Fourteen thousand two hundred in fees. Every month this doesn't ship. {claim- F6}
Dev: PCI remediation is due December fifteenth. That's a hard date with real consequences. {claim- F4}
Carmen: The merchants' date is a hard date too! I told Pivot Coffee and Brightline—
Rachel: You told them a date? {question- @+1}
Carmen: I told them "this quarter". Roughly.
Dev: The reality is, "roughly" is how we got here.
Carmen: Don't make this about me, Dev.
Dev: I'm making it about the audit.
Oskar: Can we do half and half? {question- @+1}
Rachel: Half of each usually means none of either.
Oskar: Sure. Whatever works.
Rachel: Okay, real talk. Which of the PCI findings actually block the audit? {question- @+1}
Dev: The ones about key rotation and the log retention. Those are the scary ones.
Carmen: So not all of them are scary.
Dev: I mean, they're all findings. Some are scarier.
Rachel: Hang on. Then we do the scary PCI ones first, and the chargeback flow gets whatever's left. {decision-}
Carmen: Whatever's left is nothing. You know it's nothing.
Rachel: Hang on, I just pulled up the audit tracker. It's six open findings, not ten. {claim- F3}
Dev: Six. Okay, six. Still. {claim- F3}
Rachel: Six, of which two are scary. Okay. Key rotation and log retention, then the chargeback flow, in that order. That's the scope. Decided. {decision+} {claim- F3}
Carmen: Fine. But I'm writing down that it's on you if Brightline churns.
Rachel: Write it down. I'll talk to Brightline myself if it comes to that. {action-}
Oskar: Sure.
## estimates :: Sizing; a running joke about Oskar's sourdough takes over for a bit
Rachel: Estimates. Dev, key rotation.
Dev: Eight points. Maybe thirteen if the HSM vendor is slow again. {~}
Oskar: The vendor is always slow.
Carmen: How big is the chargeback flow, honestly? {question- @+1}
Dev: The reality is, it's two sprints of work if we do it right.
Carmen: Then we do a first version. Merchants just need the evidence upload.
Rachel: Could the evidence upload alone fit this sprint? {question- @+2}
Oskar: Probably.
Dev: If nobody gets paged. So, no.
Oskar: Unrelated, but my sourdough starter died this weekend. {drift+ 4}
Carmen: Oskar. You named that thing.
Oskar: Gerald. His name was Gerald.
Dev: I mean, I'm sorry for your loss.
Rachel: Okay, can we bury Gerald after planning? {~}
Carmen: So the evidence upload, is it in or out? {question- @+1}
Rachel: Hang on. Five engineers, two open roles, a week of on-call each. It's in, as a stretch goal, behind the PCI work. Okay, that's the call. {claim- F7} {claim- F8} {decision+} {~}
Carmen: A stretch goal. Fine. I'll write the evidence upload ticket today so it's ready if there's room. {action+}
## team :: On-call load, hiring and Oskar's job offer
Rachel: Last thing. Team. Oskar, you took most of the pages again.
Oskar: Sure. It's fine.
Dev: It's not fine. You look terrible. No offense.
Oskar: Some taken.
Rachel: Real talk, should we change the rotation so nobody does back-to-back weeks? {question- @+1}
Dev: Yes. Obviously yes.
Rachel: Then no back-to-back on-call weeks, starting this sprint. {decision+}
Dev: I'll redo the on-call schedule tonight so Oskar's off next week. {action+}
Oskar: Thanks, Dev.
Carmen: Where are we on the two open roles? {question- @+1}
Rachel: One final round next week. The other one, we haven't even posted. {claim- F8} {~}
Carmen: Why not? {question- @+1}
Rachel: Budget approval. It's been stuck with finance for a month.
Dev: It'd be great if someone leaned on finance about that. {action-}
Oskar: Is anyone else here thinking about leaving? Asking for a friend. {question+} {~}
Rachel: Hang on— Oskar.
Carmen: Okay, that's a conversation for a one-on-one.
Rachel: I'll set up a one-on-one with Oskar for tomorrow morning. {action+}
Oskar: Sure. Okay.
Rachel: Okay. Sprint ends November twenty-first. Let's actually finish it this time. {claim- F12}
Dev: Famous last words.
