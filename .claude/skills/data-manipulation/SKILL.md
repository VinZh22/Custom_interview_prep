---
name: data-manipulation
description: Scope and standards for coding/data-manipulation — pandas mechanics: groupby/agg, merge, reshape, MultiIndex, window and rolling operations, vectorization. This repo uses pandas instead of SQL; never write SQL here. Use when tutoring or writing a problem in coding/data-manipulation/.
---

# Data manipulation (pandas)

Folder: [coding/data-manipulation/](../../../coding/data-manipulation/) · code in
[coding/lib/](../../../coding/lib/) · tests in [coding/tests/](../../../coding/tests/)

**This repo does not use SQL.** Every data-wrangling question is posed and solved in pandas.
Don't write `SELECT` statements, and don't offer "the SQL equivalent" as an explanation — the
user is deliberately building pandas fluency instead.

This skill covers the *mechanics*. The analyses they serve (funnels, retention, attribution)
live in [product-analytics](../product-analytics/SKILL.md).

## Scope

Selection and filtering: `loc`/`iloc`, boolean masks, `query` · `assign` and method chaining ·
`groupby` with `agg`, `transform`, `filter`, `apply`, and knowing which of the four you want ·
`merge` (all four `how` values, validation, suffixes, indicator) vs `join` vs `concat` ·
reshaping: `pivot`, `pivot_table`, `melt`, `stack`/`unstack` · `MultiIndex` construction and
flattening · time series: `to_datetime`, `resample`, `asfreq`, `rolling`, `expanding`,
`shift`/`diff`, `merge_asof` · ranking and window-like operations: `rank`, `cumsum`,
`groupby().cumcount()`, `nlargest` · missing data: `isna`, `fillna`, `dropna`, and `NaN` vs
`None` vs `NaT` · dtypes, `category`, memory footprint · `value_counts`, `crosstab`,
`duplicated`/`drop_duplicates` · vectorization vs `apply` vs `itertuples`.

## The five operations that carry most problems

1. **`groupby(...).transform(...)`** — aggregate broadcast back to row level. This is the
   pandas answer to a SQL window function, and the single most useful thing to be fluent in.
2. **`groupby(...).agg({...})`** with named aggregation for clean multi-metric output.
3. **`merge` with `validate=` and `indicator=`** — proves the join didn't silently fan out.
4. **`sort_values` + `groupby().head(n)`** for top-n-per-group.
5. **`shift`/`diff` within a group** for sessionization, gaps, and consecutive-event logic.

## What a good problem here looks like

- A small synthetic DataFrame constructed inline in the test (5–20 rows), so the expected
  output can be written by hand and asserted exactly.
- A realistic ask: "per user, the time between their first and second purchase",
  "flag rows where the value jumped more than 20% from the previous day per sensor".
- Has a wrong-but-plausible one-liner that a careful solution avoids (usually a fan-out join
  or an `apply` that silently drops groups).
- Follow-ups: do it without `apply`; make it work when a group has one row; make it work when
  timestamps are unsorted or duplicated; scale it to a file that doesn't fit in memory
  (chunking, dtypes, `category`).

## Traps to build into problems and to catch when tutoring

- **Join fan-out.** A many-to-many merge silently multiplies rows. Always check `len` before
  and after, or pass `validate="one_to_many"`.
- `SettingWithCopyWarning` — chained assignment on a slice; use `.loc` or `assign`.
- `apply` on a groupby when `transform` was wanted (wrong shape) or when a vectorized op
  existed (100× slower).
- `groupby` dropping `NaN` keys by default (`dropna=True`), silently losing rows.
- `mean()` skipping `NaN` by default, so denominators differ between columns.
- Unsorted index with `rolling` on time, or `resample` without a DatetimeIndex.
- Timezone-naive vs aware timestamps compared, and UTC-vs-local day boundaries.
- Integer columns promoted to float by a `NaN`; `==` comparisons on floats.
- Assuming `drop_duplicates` keeps the row you want — it keeps the first unless told otherwise.
- Chained boolean masks without parentheses.

## Verification standard

Implement in `coding/lib/`, and in the test build the input DataFrame inline and assert against
a hand-written expected frame with `pandas.testing.assert_frame_equal` (reset the index and be
explicit about dtypes and column order). Also assert the **row count** where a join is
involved. Run `pytest -k <module>`.

## Sources

The pandas user guide (Group By, Merge, Reshaping, Time Series sections) — read those four
rather than tutorials. *Python for Data Analysis* (McKinney) for the systematic pass.
