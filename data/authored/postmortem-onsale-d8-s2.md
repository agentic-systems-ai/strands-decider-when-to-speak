---
meeting_id: postmortem-onsale-d8-s2
theme: "Incident postmortem: the checkout outage last Tuesday"
domain_pack: incident_review
drama: 0.8
seed: 2
author: claude-opus-5-5 (Claude Code session)
pack:
  title: Postmortem - Tuesday on-sale checkout outage
  org: Quayside Tickets (fictional event ticketing)
  agenda:
    - {id: what, title: What happened, goal: Agree the sequence of events, timebox_min: 4}
    - {id: why, title: Why, goal: Understand the CDN change and the bot traffic, timebox_min: 5}
    - {id: fallout, title: Fallout, goal: Customers, the promoter and the money, timebox_min: 4}
    - {id: next_onsale, title: Before the next on-sale, goal: What must be true before March 21, timebox_min: 3}
  facts:
    - {id: F1, key: outage_duration, statement: "Checkout was down for 52 minutes", value: "52 minutes"}
    - {id: F2, key: onsale_start, statement: "The on-sale opened at 10:00 am", value: "10:00 am"}
    - {id: F3, key: bot_share, statement: "Bot traffic share during the on-sale = 70%", value: "70%"}
    - {id: F4, key: cdn_change_time, statement: "The CDN rule change went live at 9:41 am", value: "9:41 am"}
    - {id: F5, key: tickets_before_outage, statement: "Tickets sold before the outage = 3,100", value: "3,100"}
    - {id: F6, key: venue_capacity, statement: "Venue capacity = 18,000", value: "18,000"}
    - {id: F7, key: promoter_penalty, statement: "Promoter penalty clause = $50,000", value: "$50,000"}
    - {id: F8, key: queue_capacity, statement: "Queue system capacity = 40,000 concurrent users", value: "40,000"}
    - {id: F9, key: cs_emails, statement: "Customer service emails = 6,800", value: "6,800"}
    - {id: F10, key: rule_reviewers, statement: "Reviewers on the CDN rule change = 0", value: "0"}
    - {id: F11, key: duplicate_charges, statement: "Customers charged twice = 214", value: "214"}
    - {id: F12, key: next_onsale, statement: "Next major on-sale = March 21", value: "March 21"}
personas:
  - name: Tess
    role: Director of SRE, facilitates
    goals: Real fixes before the next big on-sale
    hidden_agenda: Her team pushed the CDN change
    verbosity: 3
    wpm: 160
    catchphrases: []
    voice_gender: female
  - name: Jonas
    role: Network engineer who made the CDN change
    goals: Explain the change honestly
    hidden_agenda: Was told the change was routine and low-risk
    verbosity: 2
    wpm: 145
    catchphrases: []
    voice_gender: male
  - name: Delphine
    role: Head of partnerships, owns the promoter relationship
    goals: Keep the promoter from walking
    hidden_agenda: The promoter's CEO called her personally, furious
    verbosity: 4
    wpm: 180
    catchphrases: []
    voice_gender: female
  - name: Kwesi
    role: On-call engineer during the on-sale
    goals: Get the double-charge customers refunded
    hidden_agenda: Has barely slept since Tuesday
    verbosity: 2
    wpm: 150
    catchphrases: []
    voice_gender: male
---
## what :: The sequence; Tess undercounts the duration
Tess: Let's keep this blameless. Kwesi, you were on call. What did you see? {question- @+1}
Kwesi: The on-sale opened at ten. Within a minute the checkout pages were timing out. {claim- F2}
Delphine: Within a minute. On the biggest on-sale of the year.
Tess: And we were down for about half an hour before it recovered. {claim+ F1 "half an hour"}
Kwesi: It was longer than that. The graphs say fifty-two minutes. {claim- F1}
Tess: Fifty-two. You're right. I was thinking of when we found the cause. {claim- F1}
Delphine: How many tickets did we sell before it fell over? {question- @+1}
Kwesi: Thirty-one hundred. Out of eighteen thousand. {claim- F5} {claim- F6}
Delphine: Thirty-one hundred. The promoter has the same graph. {claim- F5} {~}
Tess: What fixed it in the end? {question- @+1}
Jonas: Rolling back the CDN rule. Once the old rule was back, the queue started working.
Delphine: The CDN rule. That nobody reviewed.
Jonas: It wasn't reviewed, no. {claim- F10}
## why :: The rule change and the bots; Jonas's bot share is low and is corrected
Tess: Why. Jonas, what was the change? {question- @+1}
Jonas: A rule to cache the event pages more aggressively. It went live at nine forty-one. {claim- F4}
Kwesi: Nineteen minutes before the on-sale. {~}
Jonas: It was meant to help with load. It had the opposite effect on the queue tokens.
Tess: Who reviewed it? {question- @+1}
Jonas: Nobody. CDN rules don't go through review. They never have. {claim- F10}
Delphine: That's insane. Sorry, it is.
Tess: It's a gap. Let's call it a gap.
Jonas: The other thing is the bots. Maybe a third of the traffic was bots. {claim+ F3 "a third"}
Kwesi: The security dashboard has seventy percent. Seventy percent of requests were bots. {claim- F3}
Jonas: Seventy. Okay. That changes things. {claim- F3}
Delphine: So real fans were fighting robots for tickets, and then the site died.
Tess: Did the queue system hit its limit? {question- @+1}
Jonas: Not even close. It's built for forty thousand concurrent users. The CDN rule broke it before it got there. {claim- F8}
Delphine: My daughter tried to buy tickets for this concert. She got the error page eleven times. {drift+ 3}
Kwesi: She wasn't the only one. My cousin did too.
Delphine: She's fourteen. She thinks I work for the worst company on earth.
Tess: Okay. From now on, CDN rule changes need a second reviewer and can't go out within two hours of an on-sale. {decision+}
Jonas: That's fair. I'll write the review rule into the deploy pipeline this week. {action+}
## fallout :: Customers, refunds and the promoter; Delphine's penalty figure is inflated; Kwesi's double-charge count goes uncorrected
Tess: The fallout. Delphine, the promoter.
Delphine: The promoter is threatening the penalty clause. That's a hundred thousand dollars. {claim+ F7 "$100,000"}
Tess: I have the contract summary here. The penalty clause is fifty thousand. {claim- F7}
Delphine: Fifty. Fine. It's still fifty thousand dollars and a relationship. {claim- F7}
Kwesi: And some people got charged twice. Maybe fifty customers. {claim+ F11 "50"} {~nc}
Tess: Have they been refunded? {question- @+1}
Kwesi: Not yet. Finance needs a list.
Delphine: Customer service got sixty-eight hundred emails. People are angry. {claim- F9}
Tess: Could someone get finance the double-charge list today? {question- @+1}
Kwesi: I'll pull the list and send it to finance before lunch. {action+}
Delphine: Can we give the promoter something? A fee waiver, a statement, anything? {question- @+1}
Jonas: A public statement that says it was our fault, not theirs, would help.
Tess: Then we waive our booking fee on this event, and we put out a statement taking responsibility. {decision+}
Delphine: I'll draft the statement with comms and show it to the promoter first. {action+}
Jonas: Does legal need to see the statement before it goes out? {question+}
Kwesi: Who's going to answer the sixty-eight hundred emails? {claim- F9} {question- @+1}
Delphine: Support is doing a single reply to all of them, with the refund details.
## next_onsale :: Before March 21
Tess: Last. The next big on-sale is March twenty-first. What has to be true by then? {claim- F12} {question- @+1}
Jonas: The review rule, and a freeze on CDN changes during on-sales.
Kwesi: And bot protection. Seventy percent bots means real fans can't get in. {claim- F3} 
Jonas: Do we even know whose bots they were? {question+} {~}
Delphine: Maybe we try a verified-fan presale, like the bigger companies do. {decision-}
Tess: Let's look at what verified-fan would take before committing to it. {decision-}
Jonas: It'd be worth someone talking to the CDN vendor about their bot product. {action-}
Tess: Jonas, could you set up that call with the vendor? {question- @+1}
Jonas: Yes. This week. {action+}
Tess: Thank you, everyone. Get some sleep, Kwesi.
Kwesi: Working on it.
