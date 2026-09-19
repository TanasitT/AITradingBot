# Trade Trigger
status: executing
requested_at: 2026-09-08 09:37 ET
action: buy
candidates: [AMD:80, NVDA:76, AMZN:73, META:70]
context: SPY above 5-day MA (7,718.60 vs ~7,695), VIX ~14.5, weekly count 0/3, daily_loss_halt false. Regular stock entries UNBLOCKED. SH not eligible (score 40).
already_held: NVDA 22sh, AMZN 19sh, AMD 10sh (each ~5% — expect executor to reject adds on the position-size cap; META is the only un-held Tier-1 name)
paper_trading: true (live_trading = false in strategy.md)

Executor instructions: verify positions + buying power via Alpaca, enforce 5% position-size cap (3% for SH), stocks only, confirm >=1.25x 30-day-average volume on the 2026-09-08 session before any entry, place limit order + protective stop if all criteria pass, then update open_positions.md / trade_log.md / weekly_trade_counter.md and set status: done.

Outstanding (not this trigger): NVDA 22sh still has NO broker-side protective stop (403 Forbidden at 2026-09-01 placement) — retry a protective stop for the existing NVDA position.

## Prior trigger (SUPERSEDED / cancelled 2026-09-07)
The 2026-09-07 12:24 ET trigger fired on a closed market (Labor Day) and placed nothing. Superseded by this run.
