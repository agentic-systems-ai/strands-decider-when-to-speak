---
meeting_id: postmortem-certexpiry-d5-s1
theme: "Incident postmortem: the checkout outage last Tuesday"
domain_pack: incident_review
drama: 0.5
seed: 1
author: claude-opus-5-5 (Claude Code session)
pack:
  title: Postmortem - Tuesday checkout outage (expired certificate)
  org: Hearthstone Market (fictional grocery delivery)
  agenda:
    - {id: timeline, title: Timeline, goal: Agree when it started, when we knew and when it was fixed, timebox_min: 4}
    - {id: root_cause, title: Root cause, goal: Understand why an expiring certificate went unnoticed, timebox_min: 5}
    - {id: impact, title: Customer and business impact, goal: Size the impact and settle refunds and comms, timebox_min: 4}
    - {id: follow_ups, title: Follow-ups, goal: Owners and dates for the fixes, timebox_min: 3}
  facts:
    - {id: F1, key: outage_duration, statement: "Checkout was down for 2 hours 10 minutes", value: "2 hours 10 minutes"}
    - {id: F2, key: outage_start, statement: "Outage started at 9:40 am local time", value: "9:40 am"}
    - {id: F3, key: cert_expired_at, statement: "The payment gateway certificate expired at 9:38 am", value: "9:38 am"}
    - {id: F4, key: orders_failed, statement: "Orders that failed at checkout = 6,200", value: "6,200"}
    - {id: F5, key: customers_affected, statement: "Unique customers affected = 4,900", value: "4,900"}
    - {id: F6, key: revenue_impact, statement: "Estimated revenue impact = $340,000", value: "$340,000"}
    - {id: F7, key: refunds_issued, statement: "Delivery-fee refunds issued = $18,750", value: "$18,750"}
    - {id: F8, key: cert_alerts_90d, statement: "Certificate-expiry alerts fired in the last 90 days = 0", value: "0"}
    - {id: F9, key: time_to_cause, statement: "Time from start to identifying the cause = 74 minutes", value: "74 minutes"}
    - {id: F10, key: certs_in_inventory, statement: "Certificates in the inventory = 312", value: "312"}
    - {id: F11, key: manual_renewals_per_year, statement: "Manual certificate renewals per year = 40", value: "40"}
    - {id: F12, key: last_cert_incident, statement: "Last certificate-related incident = 14 months ago", value: "14 months"}
personas:
  - name: Nadia
    role: Head of SRE, facilitates
    goals: Kill this class of incident for good
    hidden_agenda: Asked for cert automation budget a year ago and was told no
    verbosity: 3
    wpm: 155
    catchphrases: ["let's be precise", "okay"]
    voice_gender: female
  - name: Liam
    role: On-call engineer that morning
    goals: Explain why it took so long to find
    hidden_agenda: Assumed it was a deploy and lost time chasing it
    verbosity: 3
    wpm: 160
    catchphrases: ["so", "in hindsight"]
    voice_gender: male
  - name: Rosa
    role: Product manager for checkout
    goals: Make it right with customers
    hidden_agenda: Her VP is asking for a name to blame
    verbosity: 4
    wpm: 170
    catchphrases: ["from the customer's side", "look"]
    voice_gender: female
  - name: Kenji
    role: Security engineer, owns certificates
    goals: Get certificate renewal automated
    hidden_agenda: The expiring cert was on his team's spreadsheet
    verbosity: 2
    wpm: 145
    catchphrases: ["to be fair", "technically"]
    voice_gender: male
---
## timeline :: When it started, when we knew; Liam undercounts the time to cause
Nadia: Okay, thanks everyone. Blameless as always. Liam, take us through the morning? {question- @+1}
Liam: So, checkout started failing at nine forty. Every payment call came back with a handshake error. {claim- F2}
Nadia: And when did we find out it was the certificate? {question- @+1}
Liam: In hindsight, it felt like we found it in about half an hour. {claim+ F9 "half an hour"}
Nadia: Let's be precise. The incident log has seventy-four minutes from start to cause. {claim- F9}
Liam: Seventy-four. Yeah. We spent the first forty chasing the deploy from that morning. {claim- F9} {~}
Rosa: Why the deploy? {question- @+1}
Liam: There was a deploy at nine thirty. Two things changing ten minutes apart, you blame the deploy. {~nc}
Kenji: Technically, the cert expired at nine thirty-eight. Two minutes before the errors. {claim- F3}
Nadia: So the deploy was a red herring.
Liam: A very convincing one.
Rosa: From the customer's side, the app just said "something went wrong". No hint at all.
Nadia: How long were we down in total? {question- @+1}
Liam: Two hours ten, start to finish. The renewal itself was fast once we knew. {claim- F1}
Kenji: Getting a new cert issued took about fifteen minutes. The rest was rollout. {~}
Nadia: Okay. So the timeline is clear. The gap is the seventy-four minutes to cause. {claim- F9}
Liam: In hindsight, the handshake error was the clue. I just didn't read it right.
Nadia: Nobody's blaming you. Let's figure out why the system didn't tell you.
Liam: Thanks.
## root_cause :: Why nobody saw the expiry coming; the spreadsheet; Kenji's inventory number goes unchallenged
Nadia: Root cause. Kenji, how do we track certificate expiry today? {question- @+1}
Kenji: To be fair, it's a spreadsheet. Plus a calendar reminder for the big ones.
Rosa: A spreadsheet? For payment certificates? {~}
Kenji: For all of them. We have around two hundred certificates in the inventory. {claim+ F10 "200"}
Nadia: And this one was in the spreadsheet? {question- @+1}
Kenji: It was. The reminder went to someone who left in the spring.
Liam: So the alert existed, it just went to nobody.
Nadia: Did any automated monitoring fire? {question- @+1}
Kenji: No. Zero cert-expiry alerts in the last ninety days. We never set them up for the gateway. {claim- F8}
Rosa: Look, my VP is going to ask whose fault this is.
Nadia: Then the answer is "the process". A spreadsheet that depends on one person's calendar.
Kenji: Technically, we renew about forty certs a year by hand. Something was always going to slip. {claim- F11}
Rosa: Forty a year, by hand? {claim- F11} {~}
Nadia: And when was the last cert incident? {question- @+1}
Kenji: Fourteen months ago. The internal wiki, nobody really noticed. {claim- F12}
Liam: Fourteen months, and the lesson didn't stick. {claim- F12}
Nadia: Let's be precise about the fix. Should all certs auto-renew, or just the external ones? {question- @+2}
Kenji: To be fair, all of them, eventually.
Liam: But the external ones first. The ones customers can hit.
Nadia: Okay. External certificates move to automatic renewal first, internal ones after. That's the direction we're committing to. {decision+}
Kenji: Agreed.
Rosa: Is automatic renewal something we can buy, or do we build it? {question- @+1}
Kenji: Buy, mostly. The cloud provider does it if the cert lives there.
Liam: Did anyone else's coffee order fail on Tuesday, by the way? I couldn't even get a latte from our own app. {drift+ 3} {question- @+1}
Rosa: Mine did. I ended up at the gas station. Terrible coffee.
Kenji: I made tea. Tea doesn't need TLS.
## impact :: Orders, customers, money; Rosa's order number corrected; refunds misstated and corrected late
Nadia: Okay, the impact. Rosa? {question- @+1}
Rosa: From the customer's side, about ten thousand orders failed. It was a disaster. {claim+ F4 "10,000"}
Liam: The dashboard has sixty-two hundred failed orders. Ten thousand might be attempts, with retries. {claim- F4}
Rosa: Right, sixty-two hundred orders. From about forty-nine hundred customers. {claim- F4} {claim- F5}
Nadia: And revenue? {question- @+1}
Rosa: Finance estimates three hundred forty thousand. Some of those people ordered later, so it's softer than it sounds. {claim- F6} {~}
Kenji: How many came back the same day? {question+} {~}
Nadia: We gave delivery-fee refunds, right? Around twenty-five grand, I think. {claim+ F7 "$25,000"} {question- @+1}
Rosa: Look, I'd like to do more than refund the delivery fee. These are people's groceries.
Liam: What did you have in mind? {question- @+1}
Rosa: A credit. Ten dollars, maybe, for everyone affected. {~nc}
Nadia: Ten dollars times forty-nine hundred is real money. {claim- F5}
Rosa: It's less than losing them.
Kenji: Maybe we only give credits to people who didn't come back. {decision-}
Rosa: That's harder to explain, though.
Kenji: Sorry, that's my building's fire alarm test, it'll stop in a second. {drift- 1}
Liam: Sorry, I've got the refund report open. It's eighteen seven fifty in refunds, not twenty-five. {claim- F7}
Rosa: Eighteen seven fifty, okay. {claim- F7}
Nadia: Okay. We give a ten-dollar credit to every affected customer, plus the refunds already issued. Decided. {decision+} {~}
Rosa: Thank you. I'll write the apology email and get it to legal by Thursday. {action+}
Liam: It would be good if the email explained what actually happened, in plain words. {action-}
## follow_ups :: Owners and dates; one deferred
Nadia: Follow-ups. Let's be precise: owner and date for each.
Kenji: I'll move every external certificate to automatic renewal by the end of the month. {action+}
Nadia: Thank you. And monitoring? {question- @+1}
Liam: I'll add expiry alerts for every cert in the inventory, at thirty and seven days. {action+} {~}
Nadia: Every one of them, Liam. All three hundred and twelve. {claim- F10}
Kenji: Three hundred and twelve. I said two hundred earlier, that was wrong. {claim- F10}
Nadia: That's fine. That's why we check.
Rosa: And error messages. Can the app say something better than "something went wrong"? {question- @+1}
Liam: It can. It's a product decision what it says.
Rosa: Then let's maybe look at that next quarter. {decision-}
Nadia: Someone should check the other payment providers' certs too, while we're at it. {action-}
Kenji: Already on the list. To be fair, they're on the spreadsheet.
Liam: The spreadsheet that caused this.
Kenji: The spreadsheet that is about to be retired.
Rosa: Does my VP get a written summary, or do I just forward the notes? {question+} {~}
Nadia: Okay. Good review. Thank you, everyone.
Rosa: Thanks, all.
