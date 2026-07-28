---
name: data-structures
description: Scope and standards for coding/data-structures — arrays, hash maps, stacks/queues, heaps, linked lists, trees, tries, union-find, and implementing them from scratch. Use when tutoring or writing a problem in coding/data-structures/.
---

# Data structures

Folder: [coding/data-structures/](../../../coding/data-structures/) · code in
[coding/lib/](../../../coding/lib/) · tests in [coding/tests/](../../../coding/tests/)

Two question types: *use* the right structure (most interviews) and *build* one (LRU cache,
trie, min-stack, union-find — very common as a 30-minute problem).

## Scope

Dynamic arrays and amortized resizing · hash maps and sets: hashing, collisions, why O(1) is
expected not worst-case · stacks and queues, monotonic stack/queue · heaps and priority queues,
`heapq` idioms including max-heap via negation · linked lists, dummy heads, cycle detection ·
binary trees, BSTs, traversals (recursive and iterative), balance · tries · union-find with
path compression and union by rank · intervals and sorted containers · when to reach for
`collections.deque`, `defaultdict`, `Counter`, `OrderedDict`, `bisect`.

## Complexity table to have memorized

| Structure | Access | Search | Insert | Delete |
| --- | --- | --- | --- | --- |
| Dynamic array | O(1) | O(n) | O(1) amortized at end | O(n) |
| Hash map | — | O(1) expected | O(1) expected | O(1) expected |
| Balanced BST | O(log n) | O(log n) | O(log n) | O(log n) |
| Heap | O(1) min | O(n) | O(log n) | O(log n) pop-min |
| Trie | — | O(L) | O(L) | O(L) |
| Union-find | — | ~O(1) amortized | ~O(1) | — |

Know which of these Python actually gives you: there is no built-in balanced BST — say
"I'd use `sortedcontainers` or maintain a sorted list with `bisect`" rather than pretending.

## Techniques worth having reflexive

1. **Hash map as memory** — "have I seen the complement / this prefix sum / this frequency".
2. **Monotonic stack** for next-greater-element and histogram-shaped problems.
3. **Two heaps** for a running median; heap of size k for top-k.
4. **Dummy head** to avoid special-casing the first node in linked lists.
5. **Hash map + doubly linked list** for O(1) LRU — the canonical build-a-structure problem.
6. **Union-find** whenever "are these connected" is asked repeatedly.
7. **BST in-order traversal is sorted** — the key to most BST validation/k-th problems.

## What a good problem here looks like

- Either "implement X with these complexity guarantees" — stated as guarantees, since that's
  what forces the design — or a problem where choosing the wrong container costs a factor of n.
- Small enough to implement and test in one sitting.
- Follow-ups: make it thread-safe-ish, make it support one more O(1) operation, bound the
  memory, or handle duplicates.

## Traps to build into problems and to catch when tutoring

- Claiming hash-map O(1) worst case; not mentioning it's expected.
- Mutable default arguments and mutable dict keys.
- Losing the `next` pointer during a linked-list reversal.
- Modifying a dict or set while iterating it.
- Iterative traversal implemented with the wrong push order.
- Recursion on a degenerate (linked-list-shaped) tree hitting the depth limit.
- Forgetting to update the map when evicting from an LRU — the classic memory leak.
- Union-find without path compression, then claiming near-constant time.

## Verification standard

Implement in `coding/lib/`, test in `coding/tests/`, and for any structure you build, test it
against a naive reference implementation on a random operation sequence — that catches
state-corruption bugs that hand-picked cases miss.

## Sources

*Elements of Programming Interviews* ch. 7–15; CPython docs on `collections` and `heapq`.
Pairs with [algorithms](../algorithms/SKILL.md).
