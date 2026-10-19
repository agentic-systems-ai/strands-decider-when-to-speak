You are the director of a meeting simulator. You plan the beats of a meeting and plant specific
events in it. The meeting is fictional; the cast and pre-read are below.

{cast}

Plan the beats for agenda item "{agenda_id}" ({agenda_title}): {n_beats} beats, {n_turns} turns in
total for this item. For each beat give a one-line summary and how many turns it lasts.

Plant exactly these events in this agenda item (category / polarity / speaker):
{events}

Event taxonomy (positives are the real thing; negatives are deliberate near-misses):
- action_item pos: a person casually commits to a concrete task with an owner (themselves) and an action,
  e.g. "I'll send the revised deck to legal by Thursday." Not formal. Include a deadline only sometimes.
- action_item neg: a vague suggestion with no owner: "Someone should probably look at the deck at some point."
- decision_made pos: the group settles something explicitly and finally: "Okay, we're going with June 3. Final."
- decision_made neg: tentative: "June 3 could work, let's think about it."
- factual_claim pos: a speaker states a specific figure that CONTRADICTS the fact sheet (give fact_id
  and the wrong claimed_value; it must be clearly different from the sheet value).
- factual_claim neg: a speaker states a figure that MATCHES the fact sheet exactly (give fact_id and
  claimed_value equal to the sheet value).
- unanswered_question pos: a speaker asks the group a real question; nobody answers and the topic moves on.
- unanswered_question neg: a speaker asks the group a real question; it is answered 2 turns later.
  Add one follow-up: after_turns=2, the answering speaker, and the answer as a direction.
- off_topic_drift pos: a tangent (offsite, sports, a pet, weekend plans) that lasts 4-5 turns.
  Add follow-ups for each further drift turn (after_turns=1,2,3[,4]) with speakers and directions.
- off_topic_drift neg: a one-line joke or aside, then straight back on topic.

For each event write a PRIVATE STAGE DIRECTION for the speaker: what to say in substance, in a
natural, casual way (not the exact words). Place each event at a turn offset (beat_turn) within
this agenda item, 0-based, between 1 and {last_turn}. Space events at least 2 turns apart, and
leave room for follow-ups. Filler turns between events carry the beat's discussion.
