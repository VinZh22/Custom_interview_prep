# Two Sum

- **Topic:** arrays, hash map
- **Difficulty:** easy
- **Source:** classic (example file showing the format)
- **Asked by:** everyone, as a screen
- **Attempts:** —

## Statement

Given an array of integers `nums` and an integer `target`, return the indices of the two
numbers that add to `target`. Exactly one valid answer exists; you may not use the same
element twice. Return them in any order.

## My attempt

<Write your attempt here before opening the solution.>

---

<details>
<summary>Solution</summary>

## Idea

Brute force is O(n²) over pairs. Instead, walk once and ask "have I already seen
`target - x`?" — a hash map turns the inner search into O(1).

## Walkthrough

Keep `seen: value -> index`. For each `(i, x)`: if `target - x` is in `seen`, return
`(seen[target - x], i)`; otherwise record `seen[x] = i`. Checking *before* inserting is
what prevents reusing the same element when `2x == target`.

Implementation: [../lib/two_sum.py](../lib/two_sum.py) ·
tests: [../tests/test_two_sum.py](../tests/test_two_sum.py)

## Complexity

- Time: O(n) — one pass, O(1) expected per lookup.
- Space: O(n) for the map.

## Follow-ups an interviewer would ask

- **Sorted input?** Two pointers from both ends, O(n) time and O(1) extra space.
- **All pairs, not just one?** Duplicates matter — count occurrences, and handle
  `x == target - x` separately.
- **Three sum?** Sort, fix one index, two-pointer the rest: O(n²).
- **Array too large for memory?** External sort then two-pointer, or partition by hash.

</details>

---

## Notes to self

Cue: "find two elements with a given relationship" → store the complement in a hash map.
Same skeleton as pair-with-difference-k and subarray-sum-equals-k (prefix sums).
