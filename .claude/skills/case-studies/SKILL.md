---
name: case-studies
description: Scope and standards for data-science/case-studies — open-ended product prompts: metric drops, "how would you measure X", ranking/model design, launch decisions, product sense. Use when tutoring or writing a problem in data-science/case-studies/.
---

# Case studies

Folder: [data-science/case-studies/](../../../data-science/case-studies/)

Deliberately underspecified prompts. Graded on structure, on the quality of your clarifying
questions, and on whether you land on a decision — not on getting a right answer.

## Prompt types

1. **Metric investigation.** "DAU dropped 8% overnight. Go."
2. **Metric definition.** "How would you measure whether the new onboarding is working?"
3. **Model/system design.** "Design ranking for the search results page."
4. **Launch decision.** "The test is +2% engagement, −1% revenue. Ship it?"
5. **Product sense / trade-off.** "Should we let users hide their activity?"
6. **Estimation.** "How many delivery drivers does this city need?"

## Frameworks

**Metric drop** — say the structure out loud before diving in:
1. *Is it real?* Logging change, deploy, bot filter, backfill delay, timezone, duplicate events.
2. *Cut it.* Time (gradual vs cliff — a cliff means a release or an outage), platform, version,
   geo, new vs returning, acquisition channel.
3. *Decompose.* Numerator or denominator? Rate change vs mix shift (Simpson's paradox).
   `DAU = new + retained + resurrected − churned` localizes it fast.
4. *Internal vs external.* Release, model push, pricing, marketing spend | seasonality,
   holiday, competitor, platform policy, outage upstream.
5. *Quantify each candidate* — how much of the 8% does it explain? Don't stop at a plausible
   story; check whether it accounts for the magnitude.
6. *Recommend* an action and what you'd monitor.

**Metric definition** — goal → user behavior that represents it → a countable event → the
rate/ratio form → guardrails → how it can be gamed → how you'd validate it correlates with
long-term value.

**Model design** — business goal → label → unit of prediction → features available *at serve
time* → baseline (heuristic first) → offline metric → online metric → failure modes →
monitoring and retraining.

## What a good problem here looks like

- One or two sentences, with numbers, and genuinely ambiguous.
- Accompanied by a "what the interviewer reveals if asked" list — the hidden facts (it's only
  on Android, the drop is exactly 8% every day, a logging library shipped Tuesday). That list
  is what makes the file reusable, and it's the answer to whether the user asked the right
  questions.
- A reference write-up that commits to a recommendation, with the reasoning for rejecting the
  alternatives.
- Follow-ups: the obvious hypothesis is ruled out, the data you wanted doesn't exist, you have
  one hour before an exec meeting.

## Traps to build into problems and to catch when tutoring

- Diving into hypotheses without confirming the metric is real (instrumentation first, always).
- Unstructured hypothesis spraying — twelve guesses, no framework, no prioritization.
- Never asking a clarifying question; solving a different problem than the one intended.
- Not quantifying: "seasonality could explain it" without checking last year's same week.
- Mix shift misread as a rate change.
- Proposing a deep-learning solution where a heuristic baseline and a week of logging is right.
- Defining a metric that's trivially gameable (clicks without dwell time).
- Never landing on a decision. Ambiguity is not an excuse for no recommendation.

## Tutoring note

Play the interviewer: hold the hidden facts and reveal them **only when asked the right
question**. Say "what would you like to know?" rather than volunteering. Push for prioritization
("which of those five would you check first, and why that one?") and always for the final
recommendation.

## Sources

*Ace the Data Science Interview*, *Trustworthy Online Controlled Experiments* ch. 1–3, and the
target company's own product — the best case studies are about products the user actually uses.
Pandas execution belongs in [product-analytics](../product-analytics/SKILL.md).
