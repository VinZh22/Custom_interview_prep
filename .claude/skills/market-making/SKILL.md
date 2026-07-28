---
name: market-making
description: Scope and standards for quant/market-making — quoting games, expected value under adverse selection, bet sizing, Kelly, edge vs variance. Use when tutoring or writing a problem in quant/market-making/, or when running a timed trading-game drill.
---

# Market making

Folder: [quant/market-making/](../../../quant/market-making/)

Trading-floor interviews test calibration and composure under an adversarial counterparty. The
arithmetic is easy; the discipline is not.

## Scope

Quoting a two-sided market on a random quantity · bid/ask spread as compensation for variance and
adverse selection · updating on information (center) vs uncertainty (width) · being picked off,
and what the counterparty's trade tells you · size as information · expected value of a bet ·
Kelly criterion and fractional Kelly · risk of ruin · edge vs variance trade-offs · pricing
simple wagers and lotteries · information value (`Var(E[X|Y])`) · sequential games where the
counterparty chooses when to trade · tail risk and why symmetric-EV bets aren't equivalent.

## The two dials — the whole skill in one line

- **Center = conditional expectation** given everything you know, including what their trade just
  revealed.
- **Width = conditional variance + adverse selection**, widened by their information advantage
  and by the size they can trade.

## Facts and formulas to have instant

- Fair die: `E = 3.5`, `Var = 35/12 ≈ 2.92`. Two dice: `E = 7`, `Var ≈ 5.83`, `σ ≈ 2.4`.
- Kelly on an even-money bet with win probability `p`: `f* = 2p − 1`. General:
  `f* = (bp − q)/b`. Half-Kelly gives 75% of the growth with far less variance — say that.
- `Var(X) = E[Var(X|Y)] + Var(E[X|Y])` — the value of information is the second term.
- Seeing one of two i.i.d. components halves your variance, so you can quote `1/√2 ≈ 71%` as
  wide for the same risk.
- `E[max of two dice] = 161/36 ≈ 4.47`; `E[|Z|] = √(2/π) ≈ 0.80`.

## What a good problem here looks like

- Adversarially framed and interactive: "make me a market, then I'll trade, then I'll tell you
  something." The sequence is the problem.
- Fair value computable in under a minute mentally.
- Has a stage where the counterparty is *informed*, so the correct answer involves widening or
  refusing — a candidate who always quotes tight is the one being tested for.
- Follow-ups: they can trade size, they can choose when to trade over several rounds, they get to
  see part of the state, the payoff becomes non-linear.
- The reference solution states the *reasoning to say out loud*, not just the numbers, because
  that's what's graded.

## Traps to build into problems and to catch when tutoring

- Quoting a wide, safe market (4/10 on two dice) — safe but reads as not knowing the fair value.
- Quoting tight against an informed counterparty and getting picked off.
- Failing to update the center after they trade; their trade is information.
- Not widening when size increases.
- Kelly-sizing a bet whose edge is estimated, not known — over-betting on an estimated edge is
  how accounts blow up. Mention fractional Kelly.
- Confusing `E[X]` staying the same with risk staying the same when information arrives.
- Maximizing EV while ignoring risk of ruin, or refusing a positive-EV bet because it can lose.
- Arithmetic slips under time pressure — being 0.2 off is survivable; going silent is not.

## Tutoring note

**Run these on a clock, out loud.** Play the counterparty: quote back, trade against them
immediately when their quote is off, and ask "why did I do that?" Being lifted on the offer right
after you revealed a fact should visibly change their next quote. Don't let them think in silence.

## Verification standard

Compute the conditional expectations exactly, and simulate the game in the scratchpad when the
sequencing is non-trivial (adaptive counterparty, multi-round). Verify any EV claim against a
Monte Carlo of the stated rules.

## Sources

Xinfeng Zhou ch. 2–5, *Heard on the Street*, Thorp on Kelly. Probability backing in
[probability](../probability/SKILL.md); arithmetic speed in
[mental-math](../mental-math/SKILL.md).
