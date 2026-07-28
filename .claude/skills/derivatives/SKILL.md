---
name: derivatives
description: Scope and standards for quant/derivatives — no-arbitrage, put-call parity, Black-Scholes intuition, the Greeks, hedging, implied vs realized vol. Use when tutoring or writing a problem in quant/derivatives/.
---

# Derivatives

Folder: [quant/derivatives/](../../../quant/derivatives/)

For trading roles the bar is intuition and no-arbitrage reasoning at speed, not stochastic
calculus. For quant-research roles, expect the derivation too.

## Scope

Forwards and futures, cost of carry · no-arbitrage bounds and replication arguments · put–call
parity `C − P = S − Ke^{-rT}` · option payoff diagrams and combinations (spreads, straddles,
strangles, butterflies, risk reversals) · early exercise and American vs European · binomial
pricing and risk-neutral valuation · Black–Scholes: assumptions, the formula's shape, what each
input does · the Greeks — delta, gamma, theta, vega, rho — their signs and their behavior across
strike and time · delta hedging and the gamma/theta relationship · implied vs realized vol, the
vol smile/skew and why it exists · dividends · convexity, and Jensen applied to option value ·
what a P&L attribution of a hedged option position looks like.

## Facts and approximations to have instant

- Put–call parity, and being able to derive it from a payoff table in 20 seconds.
- ATM straddle ≈ `0.8 · S · σ · √T` (from `E|Z| = √(2/π)`); ATM call ≈ `0.4 · S · σ · √T`.
- ATM delta ≈ 0.5; ATM gamma is highest and rises as expiry approaches; ATM vega ≈ `0.4·S·√T`.
- Annualized vol from daily: `× √252`, and `√252 ≈ 15.9` — so 1%/day ≈ 16%/year.
- Long option = long gamma, long vega, short theta. Gamma and theta trade off: gamma scalping
  earns realized vol and pays theta.
- Deep ITM call → behaves like the stock (delta → 1); deep OTM → delta → 0.
- Higher vol raises both calls and puts; longer maturity raises both (ignoring dividends/rates).

## What a good problem here looks like

- Answerable by a replication or no-arbitrage argument, not a formula: "call is trading at X,
  put at Y, stock at Z — is there an arbitrage, and what do you trade?"
- Or a Greeks-intuition question with a direction to justify: "you're long a straddle and the
  stock doesn't move — what happens to your P&L, and which Greek is responsible?"
- Or a mental approximation with clean numbers (S = 100, σ = 20%, T = 1).
- Follow-ups: add dividends, add rates, move to American, ask about the hedge's P&L over a path
  rather than at a point.

## Traps to build into problems and to catch when tutoring

- Applying put–call parity to American options.
- Forgetting discounting, or forgetting dividends, in a parity or forward calculation.
- Sign errors on the Greeks of a short position; confusing "long vol" with "long delta".
- Assuming delta-hedged means risk-free — you're still exposed to gamma and vega.
- Treating implied vol as a forecast of realized vol rather than a price.
- Ignoring that vega falls and gamma rises as expiry approaches — they move oppositely.
- Claiming higher vol always raises option value while holding the *forward* fixed but changing
  the drift.
- Reasoning about probability of exercise as if the risk-neutral measure were the real one.

## Verification standard

Price it two ways: a binomial tree (a few steps, by hand or in the scratchpad) and the
closed form. For any arbitrage claim, write the full trade table with cash flows at `t = 0` and
at expiry in every state — that's the only way to be sure, and it's also the answer the
interviewer wants. Check Greeks numerically by finite-differencing the price.

## Sources

Hull for the reference, Natenberg for trading intuition (the more useful of the two here),
Xinfeng Zhou ch. 6, *Heard on the Street* for the quick ones.
