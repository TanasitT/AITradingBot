# Open Positions

Last updated: 2026-07-16 EOD ET (EOD close routine)

| Ticker | Shares | Entry Price | Entry Date | Cost Basis | Stop-Loss | TP1 (+8%) | TP2 (+15%) | TP3 (+25%) | Order ID |
|---|---|---|---|---|---|---|---|---|---|
| — | — | — | — | — | — | — | — | — | — |

## No open positions.

NOTE (2026-07-16 EOD): Alpaca live account was found holding AMZN, META, and NVDA
at the start of this routine — META and NVDA were never recorded here or in
trade_log.md (likely written outside the normal memory-write path while
engine/coordinator.py etc. were mid-edit; see reasoning.md for detail).
All three were closed EOD per the no-overnight-thesis force-close trigger:
- AMZN: 19sh, exit ~$248.63, close order ba... see trade_log.md
- META: 7sh, exit ~$662.46, close order ba5820ad-a2c6-46a0-b33b-6a72cfa9ba91
- NVDA: 23sh, exit ~$206.36, close order b84d91df-7fd9-4d68-b749-521a52710c65
- AMZN close order b5db3b7c-935e-4535-9a39-3802edc5b718 (its prior GTC stop-limit
  order 6824c992 was cancelled first to free the shares)

NVDA (23 shares) closed EOD via market order at ~$207.88.
Close order ID: 9317f93a-81f0-4727-bdbf-2f04439647be
Reason: Perplexity AI found no strong confirmed overnight catalyst. Strategy force-close trigger applied.

