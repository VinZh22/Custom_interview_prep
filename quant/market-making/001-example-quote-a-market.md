# Make me a market on the sum of two dice, then I'll trade

- **Topic:** market making — quoting, edge, adverse selection
- **Difficulty:** medium
- **Source:** classic (example file showing the format)
- **Asked by:** Jane Street, Optiver, SIG-style first rounds
- **Attempts:** —

## Statement

I roll two fair dice. Make me a market on the sum. I will then either buy at your offer or
sell at your bid, and we settle at the true value. Then: I tell you the first die shows a
6 — requote. Then: I let you *choose* whether to see one die before quoting; what's that
information worth?

## My attempt

<Write your attempt here before opening the solution.>

---

<details>
<summary>Solution</summary>

## Idea

Quote around the fair value, with a spread wide enough to cover the variance you're
exposed to and the fact that the counterparty may know more than you. Then update the
*center* on information and the *width* on uncertainty.

## Walkthrough

**Fair value.** `E[sum] = 7`. `Var = 2 · 35/12 ≈ 5.83`, so `σ ≈ 2.4`.

**Initial quote.** Something like **6.5 / 7.5** — centered on 7, a spread of 1. Say the
reasoning out loud: symmetric because the counterparty has no information here, and a
one-wide market keeps expected loss to trading noise while showing you know the fair value.
Quoting 4/10 is "safe" and reads as not knowing the answer; quoting 6.9/7.1 with an
informed counterparty is how you get picked off.

**After "the first die is a 6".** Conditional fair value is `6 + 3.5 = 9.5`, and the
remaining uncertainty is a single die, `σ ≈ 1.71`. Requote around **9 / 10**. Two moves
matter: the center jumps by 2.5, and the width can *tighten* slightly because variance
fell — but only if you believe the information is true and complete.

**The value of seeing one die.** Seeing a die doesn't change your unconditional expectation
(it's still 7 by the tower property) — it changes your conditional variance, and that is
what you're being paid for as a market maker. `Var(E[sum | die 1]) = 35/12 ≈ 2.92`, exactly
half the total variance. So the information removes half your variance: you can quote
roughly `1/√2 ≈ 71%` as wide for the same risk. Worth taking, always — free variance
reduction with no cost.

## Answer

**6.5 / 7.5 → 9 / 10 after the 6; the peek halves your variance, so quote ~30% tighter.**

## What they're actually grading

- Do you center correctly and update fast, without arithmetic errors under pressure.
- Do you widen when the counterparty might be informed and tighten when they can't be.
- Do you say your reasoning while computing, or go silent.
- When they trade against you, do you notice *why* — being lifted on the offer right after
  they learned something is information, and your next quote should reflect it.

## Follow-ups an interviewer would ask

- I can now roll again and take the max of the two rolls — requote. (`E[max]` of two dice
  is `161/36 ≈ 4.47`; for the sum-of-two-dice version, recompute from scratch.)
- Same game, but I can trade up to 10 units at your quote. (Size is adverse selection:
  widen, and think about how much of your quote you're willing to show.)
- What if I get to choose *when* to trade over the next five rolls? (You're now short an
  option; the spread must cover its value.)
- Kelly-size a bet where you have a 55% edge. (`f* = 2p - 1 = 10%` of bankroll on an
  even-money bet.)

</details>

---

## Notes to self

Two dials, always: **center = conditional expectation**, **width = conditional variance +
adverse selection**. Practice requoting out loud on a timer; the failure mode is going
quiet, not being 0.2 off.
