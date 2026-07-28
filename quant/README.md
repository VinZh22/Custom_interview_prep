# Quant

Trading interviews test speed and calibration under pressure more than depth. The mental
math and games folders matter as much as the theory ones.

## Folders

- [market-making/](market-making/) — quoting games, expected value under adverse selection,
  bet sizing, Kelly, edge/variance trade-offs, "what's your market on X".
- [derivatives/](derivatives/) — no-arbitrage, put–call parity, Black–Scholes intuition,
  the Greeks, hedging, implied vs realized vol.
- [time-series/](time-series/) — stationarity, AR/MA, autocorrelation, mean reversion,
  vol clustering, Sharpe and its estimation error, backtest pitfalls.
- [mental-math/](mental-math/) — timed arithmetic, estimation/Fermi problems, log and
  square-root approximations, percentage compounding.

## Numbers worth knowing cold

- Squares to 40; powers of 2 to 2^20; 1/n as decimals to n = 16.
- `ln 2 ≈ 0.693`, `ln 10 ≈ 2.303`, `e ≈ 2.718`, `√2 ≈ 1.414`, `√3 ≈ 1.732`.
- Normal tails: ±1σ ≈ 68%, ±2σ ≈ 95%, ±3σ ≈ 99.7%; `E|Z| = √(2/π) ≈ 0.798`.
- Annualization: daily vol × √252, and √252 ≈ 15.9.
- ATM straddle ≈ `0.8 × S × σ × √T`.

## Drill format

Keep a stopwatch. Log accuracy *and* time in [../progress/log.md](../progress/log.md) —
for these, getting 90% right in 60s beats 100% in 5 minutes.

## Index

- [market-making/001-example-quote-a-market.md](market-making/001-example-quote-a-market.md)
