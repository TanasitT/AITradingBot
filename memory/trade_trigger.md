# Trade Trigger
status: executing
requested_at: 2026-08-27 08:37 ET
candidates: NVDA:82, AMD:80, AMZN:80, SMCI:78, PLTR:76, MSFT:74, META:72, COIN:72
context: SPY above 5-day MA (~$767 vs ~$765.5), VIX ~15.4 (< 28). Regular stock entries ALLOWED; SH blocked (score 22). Research cache fresh (2026-08-27 pre-market run). NOTE: NVDA/AMD/SMCI all gapped up +5-6% pre-market on NVDA's Q2 beat — entering at the open buys above Wed close with a 5% stop inside likely intraday gap-fill range. research_cache.md flags AMZN as the cleanest entry with the least gap-chase risk (AWS +37%, not dependent on the chip gap trade). Prior trigger (2026-08-26 20:37 ET) was left status:pending and never executed by the Python executor — superseded by this one.
already_held: none
paper_trading: true (live_trading = false in strategy.md)
priority_order_for_executor: AMZN (least gap-chase risk), then PLTR, then MSFT; NVDA/AMD/SMCI eligible by score but flagged for gap-chase risk — executor should verify live volume >= 1.25x 30-day avg and apply standard 5% position size / stops.
