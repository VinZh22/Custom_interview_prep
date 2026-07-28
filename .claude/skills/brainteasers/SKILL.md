---
name: brainteasers
description: Scope and standards for math/brainteasers — puzzles with no fixed syllabus: weighing, hat problems, invariants, parity, strategy games, estimation. Use when tutoring or writing a problem in math/brainteasers/, or when a question is testing lateral reasoning rather than a technique.
---

# Brainteasers

Folder: [math/brainteasers/](../../../math/brainteasers/)

No syllabus, which is the point: the interviewer wants to watch you think when no procedure
applies. Graded on the *approach* — do you find structure, or do you flail.

## Scope

Weighing and measuring (coins, balances, jugs) · hat and prisoner problems with pre-agreed
strategy · light-bulb / switch problems · river crossings and state search · pirate and
divide-the-loot induction · truth-tellers and liars · covering and tiling arguments ·
invariants and monovariants · parity and coloring arguments · pigeonhole in disguise ·
combinatorial games (Nim, subtraction games, first-player-wins arguments) · Fermi estimation ·
information-theoretic lower bounds ("how few weighings can suffice").

## Techniques worth having reflexive

1. **Invariant hunting.** What quantity never changes, or only moves one way? Kills a huge
   fraction of "can you reach state X" puzzles instantly.
2. **Parity / coloring.** Checkerboard-color the board; count squares of each color.
3. **Information bound.** `log` of the number of outcomes over `log` of outcomes per test gives
   the floor on how many tests you need — then construct a scheme meeting it.
4. **Work backwards** from the terminal state (pirates, games, last-move-wins).
5. **Induction on `n`**, having solved `n = 1, 2, 3` explicitly.
6. **Backward induction / strategy stealing** for games; find the losing positions.
7. **Extremal argument** — consider the largest/smallest element and what must be true of it.
8. **Assume a strategy exists and derive its properties** when you can't construct it directly.

## What a good problem here looks like

- Statement fits in three sentences and needs no notation.
- The insight is checkable once found — no "aha" that depends on wordplay or a trick reading of
  the English. Reject riddles; these should be math.
- Has a clean optimality claim ("and prove you can't do better in fewer"), because the lower
  bound is where the real grading happens.
- Follow-ups: generalize to `n`, tighten the resource budget, or make the adversary adaptive.

## Traps to build into problems and to catch when tutoring

- Finding *a* solution and stopping, without proving it's optimal.
- Missing that participants can pre-agree on a strategy (hat problems) or can use the *timing*
  of others' actions as a channel.
- Assuming the adversary is random when they're adversarial, or vice versa — always pin down
  which.
- Forgetting that "you may not communicate" often still permits communication through a public
  observable action.
- For estimation: not stating assumptions, or not sanity-checking the order of magnitude at the
  end.

## Tutoring note

These reward the hint ladder more than anything else in the repo. Rung 4 — "solve it for
`n = 2` first" — resolves most of them without giving anything away. Push for the lower-bound
argument even after the user has a construction.

## Verification standard

For any claimed optimum, verify the bound argument separately from the construction. For
state-search puzzles, BFS the state space in the scratchpad to confirm the minimum number of
moves.

## Sources

*Heard on the Street*, Peter Winkler's *Mathematical Puzzles*, Xinfeng Zhou ch. 2–3.
