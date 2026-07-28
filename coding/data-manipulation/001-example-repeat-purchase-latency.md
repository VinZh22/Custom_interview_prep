# Days to a user's second order

- **Topic:** pandas — groupby, ranking within a group, group-wise diff
- **Difficulty:** medium
- **Source:** classic analytics ask (example file showing the format)
- **Asked by:** product DS / analytics engineering loops
- **Attempts:** —

## Statement

You're given an `orders` DataFrame:

| column | type | notes |
| --- | --- | --- |
| `user_id` | str | |
| `order_id` | int | unique |
| `ts` | datetime64 | order timestamp; **rows are not sorted** |
| `amount` | float | |

Return a DataFrame with one row per user who has placed **at least two** orders, with
columns `user_id` and `days_to_second_order` — the number of days (fractional) between that
user's first and second order — sorted by `user_id`.

Constraints and decisions you must handle:

- Users with a single order are **excluded**, not reported as `NaN`.
- A user with three or more orders contributes only the gap between orders 1 and 2.
- Two orders can share a timestamp; that's a gap of `0.0`.
- Don't mutate the input.
- No `apply` — solve it with vectorized group operations.

Deliverable: working code with tests, plus the complexity in terms of `n` rows and `u` users.

## My attempt

<Write your attempt here before opening the solution.>

---

<details>
<summary>Solution</summary>

## Idea

Rank each user's orders with `groupby().cumcount()`, keep the first two, then take
`groupby().diff()` on the timestamp. The `diff` is `NaT` on every user's first row, so
"drop the NaT rows" *is* the "exclude single-order users" rule — no special case needed.

## Walkthrough

```python
ranked = orders.sort_values(["user_id", "ts"], kind="stable").assign(
    k=lambda df: df.groupby("user_id").cumcount()
)
first_two = ranked.loc[ranked["k"] < 2]
gap = first_two.groupby("user_id")["ts"].diff()
```

Then attach the surviving rows' `user_id` to the non-null gaps and convert to days with
`.dt.total_seconds() / 86400`.

Three things carry the correctness:

1. **`sort_values(..., kind="stable")`** — `cumcount` is positional, so it means nothing
   unless the frame is sorted first. Stable sort makes ties (identical timestamps)
   deterministic.
2. **Filtering to `k < 2` before the diff**, so a user with 10 orders can't contribute the
   2→3 gap.
3. **`.dt.total_seconds() / 86400`** rather than `.dt.days`, which floors and would turn a
   60-hour gap into `2` instead of `2.5`.

Implementation: [../lib/repeat_purchase.py](../lib/repeat_purchase.py) ·
tests: [../tests/test_repeat_purchase.py](../tests/test_repeat_purchase.py)

## Complexity

- Time: O(n log n), dominated by the sort.
- Space: O(n).

## Why the pivot version is worse

An alternative is to `pivot` the two ranked orders into columns `0` and `1` and subtract.
It works on normal input and then raises `TypeError: cannot subtract DatetimeArray from
ndarray` when **no** user has a second order — column `1` never gets created, and a
`reindex` fills it with `NaN` at the wrong dtype. The `diff` version has no such
degenerate case. Worth knowing because the empty frame is exactly what a reviewer tests.

## Follow-ups an interviewer would ask

- Median gap across users, and why the median rather than the mean here.
- The gap between the *last two* orders instead (`k` from the tail: sort descending, or
  `groupby().cumcount(ascending=False)`).
- Every consecutive gap per user, not just the first (drop the `k < 2` filter).
- Orders arrive in daily chunks that don't fit in memory — what do you keep per user?
  (Just the two earliest timestamps: a bounded per-user state.)
- Timestamps are UTC but "days" should be in the user's local timezone — where does that
  change the code, and what breaks around DST?

</details>

---

## Notes to self

Cue: "per-entity ordering within a group" → `sort_values` then `groupby().cumcount()`, and
reach for `diff`/`shift` inside the group rather than `apply`. `NaT` from a group-wise
`diff` marking each group's first row is a free filter — use it instead of a
`size() >= 2` join.

Also: `.dt.days` floors. Use `.dt.total_seconds()` whenever a fractional answer is wanted.
