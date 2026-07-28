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
