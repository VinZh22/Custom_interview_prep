---
name: statistics
description: Scope and standards for math/statistics — estimators, bias/variance, MLE, CLT, hypothesis tests, confidence intervals, regression theory. Use when tutoring or writing a problem in math/statistics/, or when a data-science question needs the underlying inference theory.
---

# Statistics

Folder: [math/statistics/](../../../math/statistics/)

Where interviewers check that you understand *why* a procedure works, not just which function
to call. Expect derivations on paper and "what would you say to a PM" translations.

## Scope

Estimators and their properties (bias, variance, consistency, efficiency) · MSE decomposition
· method of moments and MLE, with the Fisher-information/asymptotic-normality story ·
sufficiency at a working level · CLT and delta method · confidence intervals and their correct
interpretation · hypothesis testing, `α`/`β`, power, p-values · t-, chi-square, and F-tests ·
non-parametric alternatives · multiple testing (Bonferroni, FDR) · bootstrap · OLS theory:
assumptions, Gauss–Markov, `Var(β̂) = σ²(XᵀX)⁻¹`, omitted-variable bias, heteroskedasticity ·
Bayesian basics: conjugate priors, shrinkage.

## Techniques worth having reflexive

1. **Bias–variance decomposition** as the first framing for "is this estimator good".
2. **Delta method** for the variance of a transformed estimator — turns `Var(X̄)` into
   `Var(g(X̄)) ≈ g'(μ)² Var(X̄)`.
3. **MLE recipe**: log-likelihood → score → set to zero → second derivative for the
   information → asymptotic CI. Practice on Bernoulli, Poisson, exponential, normal.
4. **Sample-size / power algebra**: `n ≈ 2(z_{α/2}+z_β)²σ²/Δ²`, and the `1/Δ²` scaling.
5. **Simulation and bootstrap** when the analytic sampling distribution is out of reach.
6. **Regression as projection** — connects to [linear-algebra](../linear-algebra/SKILL.md).

## What a good problem here looks like

- Asks for a derivation with a stated conclusion ("show this estimator is biased, then
  de-bias it"), not a plug-in computation.
- Or asks for an interpretation under pressure: "the p-value is 0.049 — what do you conclude,
  and what *can't* you conclude?"
- Includes a numeric part the user can do without a calculator (`z = 1.96`, `1.64`, `2.58`).
- Follow-ups push toward the practical failure mode: what breaks when the assumption fails.

## Traps to build into problems and to catch when tutoring

- Reading a p-value as `P(H₀ | data)`, or a 95% CI as "95% chance the parameter is in here".
- Failing to reject ≠ evidence of no effect; underpowered study reported as a null result.
- Dividing by `n` vs `n-1` and being able to say *why* the correction exists.
- Assuming normality of the data when only the *sampling distribution* needs it — and knowing
  when `n` is too small or the tail too heavy for that.
- Multiple comparisons unaccounted for; peeking at a running experiment.
- Correlation/causation, confounding, selection bias, survivorship bias.
- Regression to the mean read as a treatment effect.

## Verification standard

Derive twice, or derive once and simulate the sampling distribution. For any variance formula,
check the units and the `n → ∞` behavior. For a claimed unbiasedness, take the expectation
explicitly rather than asserting it.

## Sources

Casella & Berger for theory, ISL for the applied framing, Kohavi for testing practice.
Pairs with [experimentation](../experimentation/SKILL.md) on the DS side.
