Run the trading bot order placement agent. Follow these steps in strict order — do not skip any step.

STEP 1 — Read strategy.md
Read memory/strategy.md. Note the live_trading flag (true = live account, false = paper account).
If the file cannot be read, abort immediately and report the error.

STEP 2 — Check daily trade limit
Read memory/weekly_trade_counter.md.
If trades_this_week >= 3: log "Daily trade limit reached (3/3). No new entries.", call /journal with this message, stop.

STEP 3 — Check daily halt flag
Read memory/weekly_trade_counter.md.
If daily_loss_halt = true: log "Daily loss halt is active. No trades today.", call /journal, stop.

STEP 4 — Load research candidates
Read memory/research_cache.md. Extract all tickers with Score >= 70/100, sorted highest first.
Exclude SPY and QQQ — these are market benchmarks, not alpha candidates.
If no candidates meet the threshold: log "No candidates above threshold today.", call /journal, stop.

STEP 5 — Check existing positions (memory)
Read memory/open_positions.md. Note which tickers are already held.

STEP 6 — Confirm market context
Read memory/daily_context.md.

If SPY is ABOVE 5-day MA and VIX < 28:
  - Proceed with regular stock candidates (score >= 70). Skip SH.

If SPY is BELOW 5-day MA and VIX < 28:
  - Block all regular stock entries.
  - Check if SH is in research_cache.md with score >= 60.
  - If yes: include SH as sole candidate.
  - If no: log "SPY below MA, SH not scored or below threshold. No trades today.", call /journal, stop.

If VIX >= 28: log reason, call /journal, stop regardless of SPY direction.

STEP 7 — Write trade trigger for Python execution
You cannot call the Alpaca API directly. Instead, write memory/trade_trigger.md with the
following content (replace placeholders with actual values):

```
# Trade Trigger
status: pending
requested_at: [current date and time ET]
candidates: [TICKER1:SCORE1, TICKER2:SCORE2, ...]
context: SPY [above/below] 5-day MA, VIX [X]
already_held: [list from open_positions.md, or "none"]
```

The running main.py process on the local machine will detect this file within 30 seconds,
execute all Alpaca API calls (position check, account balance, technical validation,
order placement, stop-loss setup), update open_positions.md, trade_log.md, and
weekly_trade_counter.md, then set status: done in trade_trigger.md.

STEP 8 — Journal and wait
Call /journal with: "Trade trigger written. Candidates: [list]. Waiting for Python executor."
Do NOT update open_positions.md, trade_log.md, or weekly_trade_counter.md yourself —
the Python executor will do that after confirming fills via the Alpaca API.

After placing one trade: re-check weekly_trade_counter.md. If trades_this_week >= 3, stop evaluating further candidates for today.

SPECIAL EXIT RULE FOR SH:
During intraday monitor, if SH is held and SPY has reclaimed its 5-day moving average
(current SPY price > 5-day MA), write memory/trade_trigger.md with:
```
# Trade Trigger
status: pending
action: close_sh
reason: SPY reclaimed 5-day MA — inverse ETF thesis resolved.
requested_at: [current date and time ET]
```
