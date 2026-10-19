---
meeting_id: postmortem-migration-d8-s1
theme: "Incident postmortem: the checkout outage last Tuesday"
domain_pack: incident_review
drama: 0.8
seed: 1
author: claude-opus-5-5 (Claude Code session)
pack:
  title: Postmortem - checkout outage during the flash sale
  org: Brindle Outfitters (fictional online outdoor-gear store)
  agenda:
    - {id: what_happened, title: What happened, goal: Establish the facts of the outage, timebox_min: 4}
    - {id: why, title: Why it happened, goal: Understand why a migration ran during the sale, timebox_min: 5}
    - {id: cost, title: What it cost, goal: Agree the impact on customers and revenue, timebox_min: 3}
    - {id: prevention, title: Prevention, goal: Agree the changes and their owners, timebox_min: 4}
  facts:
    - {id: F1, key: outage_duration, statement: "Checkout outage lasted 63 minutes", value: "63 minutes"}
    - {id: F2, key: sale_traffic, statement: "Sale traffic was 4x normal", value: "4x"}
    - {id: F3, key: migration_start, statement: "The migration started at 11:02 am", value: "11:02 am"}
    - {id: F4, key: table_lock_duration, statement: "The orders table was locked for 41 minutes", value: "41 minutes"}
    - {id: F5, key: lost_orders, statement: "Estimated lost orders = 3,700", value: "3,700"}
    - {id: F6, key: revenue_lost, statement: "Estimated revenue lost = $512,000", value: "$512,000"}
    - {id: F7, key: cs_contacts, statement: "Customer service contacts about the outage = 2,450", value: "2,450"}
    - {id: F8, key: rollback_time, statement: "Rolling back the migration took 22 minutes", value: "22 minutes"}
    - {id: F9, key: migration_approvals, statement: "Approvals on the migration change = 1", value: "1"}
    - {id: F10, key: change_freeze, statement: "Change freeze policy = 3 days before a sale", value: "3 days"}
    - {id: F11, key: negative_mentions, statement: "Negative social media mentions = 860", value: "860"}
    - {id: F12, key: previous_migration_incident, statement: "Previous migration-related incident = August", value: "August"}
personas:
  - name: Ifeoma
    role: SRE lead, facilitates
    goals: Keep it blameless and get real fixes
    hidden_agenda: Warned about migrations during sales in August and was ignored
    verbosity: 3
    wpm: 155
    catchphrases: ["let's stick to facts", "okay"]
    voice_gender: female
  - name: Greg
    role: CTO
    goals: Make sure this never happens again
    hidden_agenda: The CEO yelled at him for twenty minutes
    verbosity: 4
    wpm: 175
    catchphrases: ["frankly", "how does this happen"]
    voice_gender: male
  - name: Paolo
    role: Database engineer who ran the migration
    goals: Explain without being thrown under the bus
    hidden_agenda: Was told the migration was urgent by Greg's own team
    verbosity: 2
    wpm: 140
    catchphrases: ["to be honest"]
    voice_gender: male
  - name: Wren
    role: Head of customer experience
    goals: Get customers an apology that isn't corporate nonsense
    hidden_agenda: Her team worked until midnight answering emails
    verbosity: 3
    wpm: 165
    catchphrases: ["from where I sit", "honestly"]
    voice_gender: female
---
## what_happened :: The facts; Paolo undercounts the lock and the tension starts
Ifeoma: Okay. Let's stick to facts and keep it blameless. Paolo, what happened, in order? {question- @+1}
Paolo: To be honest, it was a schema migration on the orders table. It started at eleven oh two. {claim- F3}
Greg: In the middle of the flash sale.
Ifeoma: Greg, facts first. Paolo, what did the migration do to the table? {question- @+1}
Paolo: It locked it. For maybe ten minutes. Then checkout started timing out. {claim+ F4 "10 minutes"}
Wren: From where I sit it was a lot more than ten minutes. {~nc}
Ifeoma: How long was checkout actually down? {question- @+1}
Paolo: Sixty-three minutes, end to end. Including the rollback. {claim- F1}
Greg: Sixty-three minutes. During a sale with four times normal traffic. {claim- F1} {claim- F2}
Ifeoma: And the rollback itself? {question- @+1}
Paolo: Twenty-two minutes. Rolling back a half-done migration is slow. {claim- F8}
Greg: Frankly, how does this happen? Who approved a migration on sale day? {question- @+17}
Ifeoma: We'll get to why. Let's finish what.
Wren: Honestly, from the customer side, people got charged and then got an error. That's the worst version.
Ifeoma: Did anyone actually get charged twice? {question- @+1}
Wren: A few dozen. We've refunded them already.
Paolo: Why did our status page say everything was fine the whole time? {question+}
Ifeoma: Okay. Let's stick to facts. The lock was the trigger, sale traffic made it worse. Agreed? {question- @+1}
Paolo: Agreed.
Greg: Agreed. Now can we talk about why? {~} {decision+}
## why :: How the migration got through; the approval, the freeze, and an earlier warning
Ifeoma: Why. Paolo, why did it run that morning? {question- @+1}
Paolo: I was told it was urgent. The new returns feature needed the column.
Greg: Told by whom? {question- @+2}
Ifeoma: Greg. Blameless.
Paolo: By the returns team. Who, to be honest, report to you.
Greg: Okay. Okay. Fair.
Wren: My team keeps texting me about the queue. Hang on. {drift- 1}
Ifeoma: How many people approved the change? {question- @+1} {~}
Paolo: One. The usual one. {claim- F9}
Wren: One person approves a change to the table that takes all our money? {~nc}
Greg: Frankly, we have a change freeze for exactly this. It's a week before any sale. {claim+ F10 "a week"}
Ifeoma: It's three days, Greg. It's been three days since we wrote it. {claim- F10}
Greg: Three days. Fine. Then why didn't it apply? {claim- F10} {question- @+1}
Paolo: The sale was announced two days before. The freeze started after the change was already scheduled.
Wren: So the freeze didn't know about the sale.
Ifeoma: To be blunt, this isn't new. We had a migration incident in August. {claim- F12}
Greg: August was different. {claim- F12}
Ifeoma: It was the same table.
Greg: Was it? I don't remember that. {question- @+1}
Ifeoma: It was. I wrote the postmortem. There was an action item to block migrations during sales. Nobody picked it up.
Greg: Then frankly, that's on leadership. That's on me.
Paolo: To be honest, I appreciate you saying that.
Wren: Did anyone check the lock time on the replica before running it? {question- @+1}
Paolo: We usually do. Not this time, because of the rush. And, okay, I said ten minutes earlier. The log says the lock was forty-one. {claim- F4}
Greg: Forty-one minutes. {claim- F4} {~}
Ifeoma: Okay. Migrations on the orders table need two approvals and a replica test, effective today. {decision+}
Greg: Agreed.
## cost :: What it cost; the CEO number vs the real number; Wren's contact count goes unchecked
Ifeoma: Cost. Greg, what's the number the CEO has? {question- @+1}
Greg: Frankly, she thinks we lost a million dollars in sales. That's what she said to me. {claim+ F6 "$1,000,000"}
Ifeoma: Let's stick to facts. Finance estimates five hundred and twelve thousand. {claim- F6}
Greg: Five twelve. That's still awful, but it's not a million. I'll correct her. {claim- F6} {action+}
Paolo: How many orders is that? {question- @+1}
Ifeoma: About thirty-seven hundred lost orders. Some will come back, some won't. {claim- F5}
Wren: From where I sit, we got about five thousand customer contacts. Email, chat, phone, all of it. {claim+ F7 "5,000"}
Greg: Five thousand. Wow. {claim+ F7 "5,000"}
Wren: And eight hundred and sixty angry posts. Honestly, some of them were funny. {claim- F11}
Paolo: Funny how? {question- @+1}
Wren: Someone made a meme of a shopping cart stuck in a revolving door. {drift+ 5}
Greg: That one's actually good.
Paolo: The one with the melting ice cream truck was better.
Wren: The ice cream one went to the CEO's sister. She sent it to the CEO.
Greg: Of course she did.
Ifeoma: Okay. Prevention. Let's land this.
## prevention :: Owners, plus a fight about whether to freeze all changes
Greg: Frankly, I want a full freeze. No changes at all during a sale.
Paolo: To be honest, that's how we end up with a backlog of risky changes the day after.
Ifeoma: What about a freeze on schema changes only, from the moment a sale is announced? {question- @+2}
Wren: Honestly, that makes sense to me. The sale announcement is the trigger, not a calendar.
Greg: Fine. Schema changes only.
Ifeoma: Then schema changes are frozen from sale announcement to sale end. Decided. {decision+}
Paolo: Works for me.
Ifeoma: I'll update the change policy and get it into the deploy tooling by next Friday. {action+}
Greg: And the August action item? The one nobody picked up? {question- @+1} {claim- F12}
Ifeoma: It's the same fix. This time it gets an owner. Me. {action+}
Paolo: I'll write the replica lock-test script so anyone can run it before a migration. {action+}
Wren: And the customers. We need an apology that doesn't sound like a robot wrote it.
Greg: Maybe a discount code? Ten percent? {decision-} {question- @+1} {~}
Wren: Twenty. They lost an hour of their sale, honestly.
Greg: Let's think about it. I want finance's view first. {decision-}
Paolo: Someone ought to ask finance before Monday, then. {action-}
Wren: I'll draft the apology email today and send it to Greg. {action+}
Paolo: Should someone look at the returns team's other pending migrations too? {question- @+1}
Ifeoma: Yes. Any pending migration on that table waits for the new process. {decision+}
Greg: Who is telling the returns team their feature slips? {question+} {~}
Ifeoma: Okay. Thank you, everyone. This was hard and you all stuck to facts. Mostly.
Greg: Mostly.
