# Expected number of distinct coupons collected

- **Topic:** probability — linearity of expectation
- **Difficulty:** easy
- **Source:** classic (example file showing the format)
- **Asked by:** common at trading firms as a warm-up
- **Attempts:** —

## Statement

There are `n` coupon types. You draw `k` coupons independently and uniformly at random
with replacement. What is the expected number of *distinct* types you end up holding?

## My attempt

<Write your attempt here before opening the solution.>

First attempt: I tried decomposing the expected number into $\sum x_i$ where $x_i$ is the indicator that we have seen the $i^{th}$ type during the k draws. We have $x_i = 1 - (\frac{n-1}{n})^k$, so the expected value is $n - n(\frac{n-1}{n})^k$.

Second attempt: Another approach which could work algorithmically was to find a recursion formula, we could then compute it with DP. The formula I found was: $X_{n, k} = 1 + \frac{1}{n-1}X_{n, k-1} + \frac{n-1}{n-1}X_{n-1, k-1}$.

Not sure that both reconcile.

---

<details>
<summary>Solution</summary>

## Idea

Don't count distinct types directly — that couples the draws. Put an indicator on each
*type* and use linearity of expectation.

## Derivation

Let `X_i = 1` if type `i` appears at least once among the `k` draws. The number of
distinct types is `X = Σ X_i`.

A single draw misses type `i` with probability `1 - 1/n`, and draws are independent, so

```
P(X_i = 0) = (1 - 1/n)^k
E[X_i]     = 1 - (1 - 1/n)^k
```

Linearity gives the answer with no independence assumption needed on the `X_i`
(they are in fact dependent — that's the point):

## Answer

**`E[X] = n · (1 - (1 - 1/n)^k)`**

Sanity checks: `k = 0` → 0. `k = 1` → 1. For `k = n` and large `n`,
`(1 - 1/n)^n → e^{-1}`, so `E[X] ≈ n(1 - 1/e) ≈ 0.632 n`.

## Complexity

O(1) closed form.

## Follow-ups an interviewer would ask

- Variance of `X`? (Needs `E[X_i X_j]` — inclusion of two types, so
  `P(both missing) = (1 - 2/n)^k`.)
- Expected `k` to collect *all* `n` types? (Coupon collector: `n H_n ≈ n ln n`, from
  summing geometric waiting times.)
- Non-uniform coupon probabilities `p_i`? (Answer becomes `Σ_i (1 - (1 - p_i)^k)`.)

</details>

---

## Notes to self

Cue: "expected number of X satisfying a property" → indicators + linearity, and choose
the indicator over the *objects* (types), not the *trials* (draws).

Cue (missed 2026-07-28): when deciding what state a recursion needs, check whether the
transition probability is *linear* in the running state. Here `P(k-th draw is new)` is
`(n - X_{k-1})/n`, linear in `X_{k-1}`, so expectation passes through and a mean-only
state suffices — `f(k) = 1 + (1 - 1/n) f(k-1)`, one index, no distribution carried. If
the transition were nonlinear in the state (say `∝ X²`), the mean would not propagate and
you *would* need the full distribution. Second trap in the same attempt: an unconditional
`1 +` in the recursion asserts every draw yields a new type — the `+1` belongs inside the
branch where the new type actually arrives.

Also: `k/n` alone determines the answer only asymptotically (`E[X]/n → 1 - e^{-k/n}`),
not exactly. Good enough for a fast estimate out loud, wrong as a closed form.
