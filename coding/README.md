# Coding

Write-ups live in the topic folders; runnable implementations live in
[lib/](lib/) with tests in [tests/](tests/). Every coding problem should end with a
green test — reading a solution is not the same as having written one.

## Folders

- [algorithms/](algorithms/) — two pointers, sliding window, binary search, sorting,
  greedy, recursion/backtracking, dynamic programming, graphs.
- [data-structures/](data-structures/) — arrays/strings, hash maps, stacks/queues, heaps,
  linked lists, trees, tries, union-find.
- [data-manipulation/](data-manipulation/) — **pandas, not SQL**: `groupby`/`agg`/`transform`,
  `merge`, reshaping, `MultiIndex`, rolling and window ops, vectorization.
- [system-design/](system-design/) — design write-ups: requirements, estimates, data model,
  API, scaling, trade-offs.

The analyses that data manipulation serves — funnels, retention, attribution — live in
[../data-science/product-analytics/](../data-science/product-analytics/). This folder is the
mechanics; that one is the questions.

## Workflow per problem

1. Copy [../templates/problem.md](../templates/problem.md) into the topic folder.
2. State the brute force and its complexity **out loud** before optimizing.
3. Implement in `lib/<module>.py`, test in `tests/test_<module>.py`.
4. `pytest -k <module>` until green, then re-read for naming and edge cases.

## Checklist before calling a solution done

- [ ] Empty / single-element / all-equal inputs.
- [ ] Integer overflow-ish and off-by-one boundaries; `lo <= hi` vs `lo < hi`.
- [ ] Stated time and space complexity, and whether the bound is tight.
- [ ] Would this still work if the input were streamed / too big for memory?

## Index

- [algorithms/001-example-two-sum.md](algorithms/001-example-two-sum.md)
- [data-manipulation/001-example-repeat-purchase-latency.md](data-manipulation/001-example-repeat-purchase-latency.md)
