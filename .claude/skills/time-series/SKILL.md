---
name: time-series
description: Scope and standards for quant/time-series — stationarity, AR/MA, autocorrelation, mean reversion, vol clustering, Sharpe estimation, backtest pitfalls. Use when tutoring or writing a problem in quant/time-series/.
---

# Time series

Folder: [quant/time-series/](../../../quant/time-series/)

Half theory (what is an AR(1) and what does it do), half professional skepticism (why is this
backtest lying to you). The second half is what separates candidates.

## Scope

Stationarity, weak vs strong; unit roots and differencing · autocovariance, ACF, PACF, and
reading them · white noise, random walk, AR, MA, ARMA, ARIMA · AR(1) properties: mean reversion
speed, half-life `ln2/|ln φ|`, variance `σ²/(1−φ²)` · Ornstein–Uhlenbeck as the continuous analog
· cointegration and pairs trading; spread construction · vol clustering, ARCH/GARCH intuition,
vol-of-vol · realized vs implied vol; vol estimators and their bias · returns: log vs simple,
aggregation, fat tails, why normality fails · Sharpe ratio, its annualization (`× √252`), and its
**standard error** `≈ √((1 + SR²/2)/T)` · drawdown and its relation to Sharpe · autocorrelation
inflating or deflating a Sharpe estimate · backtest methodology: look-ahead, survivorship,
transaction costs, capacity, overfitting/multiple testing on strategies.

## Facts to have instant

- Random walk: variance grows linearly in time, `σ_T = σ√T`; no mean reversion, ACF of levels
  ≈ 1 at all lags.
- AR(1) with coefficient `φ`: ACF at lag `k` is `φ^k`; half-life of a shock is `ln2/|ln φ|`.
- Daily vol → annual: `× √252`, `√252 ≈ 15.9`.
- A Sharpe of 1 measured over 1 year has a standard error of roughly 1 — **one year of data
  cannot distinguish a Sharpe of 1 from 0**. This is the most useful thing in this folder.
- 20 strategies tested at 5% each: expect one "significant" by luck.
- MA(q) has ACF cutting off after lag `q`; AR(p) has PACF cutting off after lag `p`.

## What a good problem here looks like

- A small model with numbers, asking for a derived property: "given AR(1) with φ = 0.9, what's
  the half-life and the unconditional variance?"
- Or a skepticism question: "this backtest shows Sharpe 2.5 over 18 months — what do you ask
  before allocating?" The answer is a checklist, and the checklist is the skill.
- Or a diagnosis: "returns look i.i.d. but squared returns are strongly autocorrelated — what's
  going on and what do you do about it?"
- Follow-ups: add transaction costs, shorten the sample, add autocorrelation, ask for the
  capacity of the strategy.

## Traps to build into problems and to catch when tutoring

- Reporting a Sharpe without its standard error or the sample length.
- Look-ahead bias: using a signal computed with data unavailable at trade time; restated
  fundamentals; using the close to trade at the close.
- Survivorship bias in the universe (delisted names removed).
- Ignoring transaction costs, slippage, borrow costs, and capacity — many "edges" die on costs.
- Overfitting via parameter search, then reporting the in-sample best as expected performance;
  no out-of-sample or walk-forward.
- Standard k-fold cross-validation on time-ordered data (leakage across folds).
- Regressing two non-stationary series and reading the R² as a relationship (spurious
  regression); cointegration required.
- Treating returns as normal when tails are fat; using a vol estimate through a regime change.
- Confusing a random walk with a mean-reverting series on a short sample — they look the same.
- Annualizing a Sharpe from autocorrelated returns with a naive `√252`.

## Verification standard

Simulate the process in the scratchpad (numpy) and check the claimed property empirically —
ACF, half-life, and variance are all quick to confirm, and simulation immediately exposes
estimation-error claims. For any Sharpe or significance claim, compute the standard error, not
just the point estimate.

## Sources

Tsay for the theory; Bailey & López de Prado on backtest overfitting; *Advances in Financial
Machine Learning* (López de Prado) ch. 7 for cross-validation on time series. Statistical
backing in [statistics](../statistics/SKILL.md).
