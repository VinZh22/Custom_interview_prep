---
name: mental-math
description: Scope and standards for quant/mental-math — timed arithmetic, Fermi estimation, log and root approximations, percentage and compounding shortcuts. Use when tutoring or writing drills for quant/mental-math/, or when running a timed arithmetic session.
---

# Mental math

Folder: [quant/mental-math/](../../../quant/mental-math/)

A screening filter at trading firms, and pure practice — no insight required, so the only thing
that improves it is timed reps. Track time *and* accuracy; 90% correct in 60 seconds beats 100%
in five minutes.

## Scope

Two- and three-digit multiplication and division · squares, cubes, and square roots ·
percentages, percentage changes, and reversing them · fractions ↔ decimals ↔ percentages ·
compounding and the rule of 72 · logs and exponentials by approximation · orders of magnitude
and unit conversion · Fermi estimation · quick expected-value arithmetic (`p × payoff` sums) ·
odds ↔ probability conversion · weighted averages.

## Tables to have memorized cold

- Squares to 40; cubes to 15; powers of 2 to 2²⁰ (`2¹⁰ = 1024`, `2²⁰ ≈ 1.05 M`).
- `1/n` as decimals for `n ≤ 16` (`1/7 = .1429`, `1/9 = .1111`, `1/11 = .0909`, `1/13 = .0769`).
- `ln 2 ≈ .693`, `ln 3 ≈ 1.099`, `ln 10 ≈ 2.303`, `log₁₀2 ≈ .301`, `e ≈ 2.718`.
- `√2 ≈ 1.414`, `√3 ≈ 1.732`, `√5 ≈ 2.236`, `√10 ≈ 3.162`, `√252 ≈ 15.9`, `√π ≈ 1.772`.
- Normal: ±1σ 68%, ±2σ 95%, ±3σ 99.7%; `z₉₅ = 1.96`, `z₉₀ = 1.645`, `z₉₉ = 2.576`.

## Techniques

1. **Difference of squares**: `47 × 53 = 50² − 3² = 2491`. Any pair symmetric about a round
   number.
2. **Round and correct**: `98 × 47 = 100×47 − 2×47`.
3. **Squares near a base**: `(a±b)² = a² ± 2ab + b²` with `a` round.
4. **Split by place value**, and multiply left-to-right — you get the leading digits first,
   which is often all that's needed.
5. **Percentages via fractions**: 12.5% = 1/8, 16.67% = 1/6, 37.5% = 3/8.
6. **Compounding**: `(1+r)ⁿ ≈ 1 + nr` for small `nr`, then add `C(n,2)r²`. Rule of 72 for
   doubling time.
7. **Logs**: `ln x` via `ln 2` and `ln 10` decomposition; `log₁₀` from the digit count.
8. **Square roots** by bracketing then one Newton step: `√n ≈ (g + n/g)/2`.
9. **Estimate first, then refine.** State the order of magnitude before the digits — an answer
   that's 10× off is much worse than one that's 2% off.
10. **Fermi**: decompose into factors you can bound, keep one significant figure, and sanity-check
    the result against something you know.

## What a good drill file looks like

- A **set** of 10–20 items with a time budget per item, not a single question — this folder is
  drills, not problems.
- Answers in the `<details>` block as a plain list, plus the *technique* to use for each so the
  user learns the shortcut rather than grinding.
- Clean but non-trivial numbers: pairs symmetric about a round number, percentages that are nice
  fractions, roots near a known square.
- For estimation items: the expected order of magnitude and the decomposition, since there's no
  exact answer.
- Difficulty scaled by time budget, not by uglier numbers.

## Traps

- Arithmetic slips from skipping the estimate — always know the magnitude before the digits.
- Reversing a percentage change wrongly: down 20% then up 20% is not flat (0.8 × 1.2 = 0.96);
  to undo −20% you need +25%.
- Confusing percentage points with percent.
- Basis points (1 bp = 0.01%).
- Compounding vs simple interest over multiple periods.
- Annualizing vol linearly instead of by `√T`.
- Losing track of a carried digit while talking — practice narrating and computing at once.

## Tutoring note

Run these with a visible timer and no hints. Log time and accuracy in
[progress/log.md](../../../progress/log.md) — trend over sessions is the whole signal here. When
the user misses one, give the *shortcut* rather than the answer, then re-ask a similar item
immediately.

## Verification standard

Compute every answer in the scratchpad (Python) before writing the file. Mental-math sheets with
wrong answers are worse than useless — they train wrong reflexes and destroy trust in the drill.

## Sources

Zetamac (`arithmetic.zetamac.com`) for timed reps, *Secrets of Mental Math* (Benjamin) for the
techniques, Fermi problems from *Guesstimation*.
