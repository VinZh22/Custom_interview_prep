---
name: probability
description: Scope and standards for math/probability — conditional probability, Bayes, expectation tricks, distributions, random walks, Markov chains, order statistics. Use when tutoring or writing a problem in math/probability/, or when a problem in another area turns on a probabilistic argument.
---

# Probability

Folder: [math/probability/](../../../math/probability/)

The highest-yield area for quant interviews and the most common source of "clever" problems
elsewhere. Most interview probability is one of a dozen patterns in disguise.

## Scope

Conditional probability and Bayes · independence vs conditional independence · expectation
and variance, including the tower property · indicator variables and linearity · common
distributions (Bernoulli, binomial, geometric, Poisson, uniform, exponential, normal) and
when each arises · memorylessness · sums and transformations of random variables · order
statistics · random walks and gambler's ruin · Markov chains and stationary distributions ·
generating functions for waiting times · basic martingales and optional stopping.

## Techniques, roughly in order of how often they crack a problem

1. **Linearity of expectation with indicators.** Put the indicator on the objects being
   counted, not the trials. Works without independence — that's the whole point.
2. **Condition on the first step.** Turns "expected time until X" into a recursion. The
   default move for random walks, sequential games, and anything with "keep going until".
3. **Symmetry.** Before computing, ask whether an exchange argument gives the answer for free
   (e.g. "probability A beats B" in a symmetric setup is 1/2 by relabeling).
4. **Law of total expectation / variance.** `E[X] = E[E[X|Y]]`,
   `Var(X) = E[Var(X|Y)] + Var(E[X|Y])` — the second is underused and shows up in
   information-value questions.
5. **Complementary counting.** `P(at least one)` via `1 - P(none)`.
6. **Change of variables** with the Jacobian for densities; CDF-first for order statistics.
7. **Optional stopping / martingales** for gambler's-ruin and stopping-time shapes.
8. **Poissonization** and thinning when events arrive in time.

## What a good problem here looks like

- Solvable in under 10 minutes by hand, with a closed form or a clean recursion.
- Hinges on choosing the *right* conditioning or the *right* indicator, not on grinding.
- Numbers stay arithmetic-friendly; the answer is checkable by a sanity case.
- Comes with follow-ups that push to the variance, the non-uniform case, or the limiting
  behavior as *n* → ∞.

## Traps to build into problems and to catch when tutoring

- Confusing `P(A|B)` with `P(B|A)`; base-rate neglect in Bayes problems.
- Assuming independence to multiply, when the events are only conditionally independent.
- The waiting-time paradox / size-biased sampling ("the bus you catch is a longer wait").
- Boy-girl and Monty-Hall-family problems where the *information mechanism* changes the
  answer — always ask *how* the fact was learned.
- Non-transitive or counterintuitive setups (Simpson's paradox, non-transitive dice).
- Treating `E[1/X]` as `1/E[X]`, or `E[XY]` as `E[X]E[Y]` without justification.
- Forgetting that a geometric expectation is `1/p` but the *conditional* one after a failure
  is unchanged (memorylessness).

## Verification standard

Simulate. A short Monte Carlo in the scratchpad settles almost any answer here in seconds and
catches the conditioning errors that reasoning alone won't. For closed forms, also check
`n = 1`, `n = 2`, and the large-*n* limit.

## Sources

Mosteller's *Fifty Challenging Problems*, Blitzstein, Xinfeng Zhou ch. 4–5, *Heard on the
Street*.
