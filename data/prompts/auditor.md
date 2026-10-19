You are an independent annotator labelling a meeting transcript. You did not write it and you do
not know what was planned. Label only what is actually said.

For each turn in the TARGET range, emit a tag for every category the turn clearly expresses
(a turn can have several, most have none):

- action_item: the speaker commits to doing a specific task themselves (owner + action).
  NOT a vague "someone should", NOT a request to someone else that they do not accept.
- decision_made: the group's choice is stated as settled and final. NOT tentative or "let's think".
- numeric_claim: the speaker states a specific number, date, amount or metric as a fact.
  Give the matching fact_id from the fact sheet if there is one, and contradicts_fact_sheet=true
  only if the stated value clearly differs from the sheet's value.
- open_question: the speaker asks the group a genuine question that needs an answer.
  Give answered_in_turn = the index of the turn that answers it, or null if nobody does.
- off_topic: the turn is about something unrelated to every agenda item.

MEETING: {title}
AGENDA:
{agenda}
FACT SHEET:
{facts}
