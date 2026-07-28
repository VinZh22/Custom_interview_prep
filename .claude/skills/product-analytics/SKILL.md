---
name: product-analytics
description: Scope and standards for data-science/product-analytics — funnels, retention and cohort analysis, attribution, sessionization, computed in pandas (this repo uses pandas, never SQL). Use when tutoring or writing a problem in data-science/product-analytics/.
---

# Product analytics (in pandas)

Folder: [data-science/product-analytics/](../../../data-science/product-analytics/)

The applied half of data wrangling: given an event log, compute the metric a PM asked for.
[data-manipulation](../data-manipulation/SKILL.md) covers the pandas mechanics; this covers the
analyses and the definitional judgment they require.

**No SQL in this repo.** These are traditionally SQL interview questions; here they are posed
and solved with pandas on a DataFrame of events.

## Scope

Event-log shape (`user_id`, `event`, `timestamp`, properties) · sessionization with an
inactivity gap · funnel conversion, ordered vs unordered steps, per-step drop-off · retention:
day-N vs unbounded vs rolling, cohort tables and triangles · churn and resurrection · DAU/WAU/MAU
and stickiness · active-user decomposition
(`DAU = new + retained + resurrected − churned`) · attribution: first-touch, last-touch, linear,
time-decay · lifetime value at a basic level · gaps-and-islands: streaks of consecutive active
days · time-to-event between a user's ordered actions · top-n per group · dedup of double-fired
events.

## The standard computations, and the pandas shape of each

| Analysis | Approach |
| --- | --- |
| Sessionize | sort by user+time, `groupby('user_id')['ts'].diff()`, `gt(gap).cumsum()` as session id |
| Funnel | pivot first-timestamp per step per user, then require increasing timestamps across steps |
| Day-N retention | join cohort day to activity days, `(day - cohort_day).dt.days`, then `crosstab` |
| Cohort triangle | `pivot_table(index=cohort_month, columns=months_since, values=n_users)` |
| Streaks | rank dates per user, subtract the rank from the date, `groupby` the difference |
| Time-to-second-event | `groupby('user_id')['ts'].nth(0)`/`nth(1)`, or `shift` within group |
| Top-n per group | `sort_values` then `groupby().head(n)` |
| Last-touch attribution | for each conversion, `merge_asof` backwards onto the touch log |

## What a good problem here looks like

- A small event log (10–30 rows) built inline in the test, containing exactly the awkward cases:
  a user who skips a funnel step, one who repeats a step, one with events out of order, one with
  a duplicate event at the same timestamp, and one with a single event.
- A question whose *definition* is the hard part: "what's our week-1 retention?" requires
  deciding day-N vs rolling, whether the cohort day counts, and what a user with no activity
  means.
- A stated denominator. Most wrong analytics answers are wrong denominators.
- Follow-ups: make the funnel steps order-agnostic, handle timezones, compute it per cohort,
  make it work when the log arrives in chunks.

## Traps to build into problems and to catch when tutoring

- **Ambiguous definitions accepted silently.** Retention "day 1" — the day after signup, or
  within 24 hours? Ask before computing; interviewers plant this.
- Funnel computed with counts per step instead of per-user ordered progression, so users who did
  step 3 without step 2 are counted as converting.
- Join fan-out inflating user counts — check `len` before and after every merge.
- Double-counted events (retries, client-side double fire) not deduped.
- Sessionization on an unsorted frame, or a gap applied globally instead of per user.
- Wrong denominator: dividing by all users instead of the eligible cohort, or by rows instead of
  users.
- Survivorship: computing day-30 retention for cohorts less than 30 days old.
- Timezone/day-boundary mismatch between the cohort date and the activity date.
- `groupby(dropna=True)` silently dropping null user ids or event types.
- Mixing rates across groups of different sizes and calling it an average.

## Verification standard

Build the input DataFrame inline in the test, hand-compute the expected result for that tiny
log, and assert with `pandas.testing.assert_frame_equal`. Include the awkward users listed above
as test cases. Implementation in `coding/lib/`, run `pytest -k <module>`. State the metric
definition explicitly in the solution — an answer without its definition isn't checkable.

## Sources

The pandas user guide (Group By, Time Series, Merge). Analytics framing from Kohavi ch. 6–7 and
[case-studies](../case-studies/SKILL.md).
