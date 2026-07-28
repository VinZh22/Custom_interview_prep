---
name: experimentation
description: Scope and standards for data-science/experimentation — A/B test design, power and sample size, multiple testing, CUPED, network effects, novelty, guardrail metrics, peeking. Use when tutoring or writing a problem in data-science/experimentation/.
---

# Experimentation

Folder: [data-science/experimentation/](../../../data-science/experimentation/)

The most reliably asked DS topic at product companies, and the one where candidates most often
give an answer that's technically fine and practically naive.

## Scope

Hypothesis and metric definition; primary vs secondary vs guardrail · randomization unit and
why it must match the analysis unit · sample size and power; the `1/Δ²` scaling · MDE chosen
from a business threshold, not convenience · duration and weekly cycles · SRM (sample ratio
mismatch) as the first sanity check · peeking, sequential testing, alpha spending · multiple
comparisons (Bonferroni, Benjamini–Hochberg) · variance reduction: CUPED, stratification,
covariate adjustment · heterogeneous treatment effects and segment analysis · interference:
network effects, marketplace two-sidedness, switchback designs, cluster randomization ·
novelty and primacy effects · non-inferiority tests · ratio metrics and the delta method ·
quasi-experiments when randomization is impossible: diff-in-diff, synthetic control,
regression discontinuity, instrumental variables · practical significance vs statistical.

## The framework to run every design question through

1. **Decision.** What action does this test inform, and what result would change it?
2. **Metric.** Primary (one), guardrails (latency, crash rate, revenue), and the tension
   between them.
3. **Unit.** Randomize on user (or cluster), analyze on the same unit. Session-level
   randomization for a persistent UI change is a design bug.
4. **Power.** `n ≈ 2(z_{α/2}+z_β)²σ²/Δ²`; `(1.96+0.84)² ≈ 7.85`. Convert to days, round up to
   whole weeks.
5. **Validity checks.** SRM, pre-period A/A behavior, instrumentation coverage.
6. **Analysis plan, pre-registered.** No peeking, correction for multiplicity, segments
   declared in advance.
7. **Read-out.** Effect size with a CI, practical significance, and what you'd do if it's
   flat.

## What a good problem here looks like

- Concrete numbers the user can work without a calculator (4% baseline, 5% relative lift,
  50k/day), so the arithmetic finishes in two minutes and the discussion gets the rest.
- A design flaw planted in the setup, waiting to be caught (wrong randomization unit, a metric
  that can be gamed, a two-week test on a marketplace with spillover).
- An ambiguous business goal that must be turned into a metric — that translation is the skill.
- Follow-ups: the result is flat (now what), the guardrail regressed, the effect is positive in
  one segment only, the PM wants to stop early.

## Traps to build into problems and to catch when tutoring

- Peeking and stopping at the first significant reading; no correction for repeated looks.
- Randomizing sessions but analyzing users, or vice versa — variance estimate is then wrong.
- Ignoring SRM; a 51/49 split with millions of users is a broken experiment, not noise.
- Testing 20 metrics, reporting the one that hit `p < 0.05`.
- Network/marketplace interference treated as independent units (both sides of a marketplace,
  social graphs, shared inventory, ad auction budgets).
- Novelty effect read as a durable lift; not checking the effect trend over time.
- Ratio metrics analyzed with naive variance (needs the delta method).
- Simpson's paradox when traffic mix shifts between arms mid-test.
- Declaring "no difference" from an underpowered test.
- Post-hoc segmentation presented as a finding.

## Verification standard

Do the sample-size arithmetic twice and sanity-check it against the `1/Δ²` scaling. Where a
claim is about a procedure's error rate (peeking, multiplicity), simulate it — a few hundred
synthetic A/A tests in the scratchpad demonstrates the inflated false-positive rate concretely,
which is also the most convincing thing to say in an interview.

## Sources

*Trustworthy Online Controlled Experiments* (Kohavi, Tang, Xu) — the reference. Theory in
[statistics](../statistics/SKILL.md); metric investigation in
[case-studies](../case-studies/SKILL.md).
