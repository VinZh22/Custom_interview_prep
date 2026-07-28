# How long should this A/B test run?

- **Topic:** experimentation — power and sample size
- **Difficulty:** medium
- **Source:** classic (example file showing the format)
- **Asked by:** product DS / analytics loops
- **Attempts:** —

## Statement

Your checkout conversion rate is 4%. Product wants to detect a relative lift of 5%
(4% → 4.2%) at 80% power and a two-sided 5% significance level. You get 50,000 visitors
per day, split 50/50. How long must the test run, and what would you push back on?

## My attempt

<Write your attempt here before opening the solution.>

---

<details>
<summary>Solution</summary>

## Idea

Per-arm sample size for two proportions:
`n ≈ 2 · (z_{α/2} + z_β)² · p(1-p) / Δ²`, then convert to days. The interesting part of
the answer is the pushback, not the arithmetic.

## Derivation

With `α = 0.05` two-sided and 80% power: `z_{α/2} = 1.96`, `z_β = 0.84`, so
`(1.96 + 0.84)² ≈ 7.85`.

```
p  = 0.04,  p(1-p) = 0.0384
Δ  = 0.002            (absolute, = 5% of 4%)
Δ² = 4e-6

n ≈ 2 × 7.85 × 0.0384 / 4e-6 ≈ 1.51e5 ... per arm
```

`2 · 7.85 · 0.0384 = 0.603`; `0.603 / 4e-6 ≈ 150,700` per arm, so ≈ **301,000 visitors
total**. At 50,000/day that is **about 6 days** — round up to 7 to cover a full weekly
cycle.

## Answer

**≈150k per arm, ~301k total, one full week.**

Note the `1/Δ²` scaling: halving the detectable effect quadruples the runtime. That is the
single most useful fact to say out loud.

## What to push back on

- **Run whole weeks.** Day-of-week composition differs; stopping mid-cycle biases the mix.
- **No peeking.** Repeated significance testing inflates false positives well past 5%;
  if they want early looks, use sequential testing or alpha spending, not eyeballing.
- **Is 5% relative a real MDE or a wish?** Ask what lift would change the decision — the
  MDE should come from the business threshold, not from what's convenient.
- **Unit of randomization** must be the unit of analysis (visitor, not visit) or the
  variance estimate is wrong.
- **Variance reduction:** CUPED on pre-period conversion can cut required duration
  materially when pre-period data is predictive.
- **Multiple metrics** → correct for it, or pre-register one primary metric plus guardrails.

## Follow-ups an interviewer would ask

- One-sided instead of two-sided? (`z_α = 1.645`, ~21% fewer samples.)
- 90% power? (`z_β = 1.28`; factor becomes `(1.96+1.28)² ≈ 10.5`, ~34% more.)
- A revenue-per-user metric instead of a rate? (Heavy tail — use the observed variance,
  consider trimming or a log transform; expect a much larger `n`.)
- Novelty effects and how you'd detect them? (Effect trend over time by cohort.)

</details>

---

## Notes to self

Memorize `(1.96 + 0.84)² ≈ 7.85` and the `16 · σ² / Δ²` rule of thumb for means. Interviewers
care more that you interrogate the MDE than that you nail the arithmetic.
