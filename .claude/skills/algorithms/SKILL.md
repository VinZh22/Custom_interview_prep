---
name: algorithms
description: Scope and standards for coding/algorithms — two pointers, sliding window, binary search, greedy, recursion/backtracking, dynamic programming, graphs. Use when tutoring or writing a problem in coding/algorithms/.
---

# Algorithms

Folder: [coding/algorithms/](../../../coding/algorithms/) · code in
[coding/lib/](../../../coding/lib/) · tests in [coding/tests/](../../../coding/tests/)

Practice by pattern, not at random. The goal is that an unseen problem announces its pattern
within the first minute.

## Scope and the pattern list

| Pattern | Recognition cue |
| --- | --- |
| Two pointers | sorted input, pair/triplet with a target, in-place partition |
| Sliding window | contiguous subarray/substring, "longest/shortest with property" |
| Binary search | sorted, or monotone predicate — including "search the answer space" |
| Prefix sums / difference arrays | range sums, subarray-sum-equals-k |
| Sorting + greedy | intervals, scheduling, "minimum number of X" |
| Heap / top-k | k-th largest, merge k lists, streaming median |
| Recursion & backtracking | enumerate all valid configurations, prune early |
| Dynamic programming | overlapping subproblems + optimal substructure; count/optimize over sequences |
| Graph traversal | BFS for shortest unweighted path, DFS for connectivity/cycles, topo sort for ordering |
| Shortest path | Dijkstra (non-negative), Bellman–Ford (negative edges) |
| Union-find | dynamic connectivity, cycle detection in undirected graphs |
| Bit manipulation | subsets, XOR tricks, parity |

## Method to teach and to enforce

1. **Restate the problem** and confirm constraints: input size, value ranges, duplicates,
   sortedness, in-place requirement.
2. **Brute force out loud, with its complexity**, before optimizing. Interviewers want the
   baseline; skipping it reads as guessing.
3. **Name the target complexity** from the constraints — `n ≤ 10⁵` says O(n log n),
   `n ≤ 20` says exponential/bitmask, `n ≤ 500` allows O(n³).
4. **Pick the pattern, justify it in one sentence.**
5. **Dry-run on a 3-element example before writing code.** Most bugs die here.
6. **Then implement**, then test edge cases, then state final complexity.

For DP specifically: define the state in words, then the recurrence, then the base case, then
the iteration order, then space optimization. In that order — code last.

## What a good problem here looks like

- One pattern as the core, with a twist that blocks the naive application of it.
- Implementable in 20–40 lines; the interview constraint is time, not typing.
- Has a real edge case that a careless solution fails (empty input, all-equal, single element,
  duplicates, negative values).
- Follow-ups: streaming/too-big-for-memory, k-th instead of first, online instead of batch,
  or "what if the array is sorted".

## Traps to build into problems and to catch when tutoring

- Off-by-one in binary search: `lo <= hi` vs `lo < hi`, `mid` rounding, which half to discard,
  and the infinite loop when the window doesn't shrink.
- Sliding window that shrinks in the wrong place, or that assumes all-positive values.
- Mutating a list while iterating it.
- Greedy asserted without an exchange argument — ask "why is local optimal global here".
- DP recurrence that's right with a wrong base case, or wrong iteration order.
- Recursion depth on `n = 10⁵` (Python default limit ~1000).
- Forgetting `visited` in a graph traversal, or marking visited at pop instead of push.
- Shallow copy of nested structures in backtracking; not undoing the state change.

## Verification standard

**Write the implementation in `coding/lib/` and run `pytest -k <module>`.** A solution that
hasn't executed doesn't go in the repo. Include the degenerate cases in the test as
parametrized cases, and for anything subtle, add a brute-force reference and compare on random
inputs.

## Sources

*Elements of Programming Interviews*, *Cracking the Coding Interview*, LeetCode organized by
the pattern table above. Overlaps with [combinatorics](../combinatorics/SKILL.md) for counting
DP and [data-structures](../data-structures/SKILL.md) for the underlying containers.
