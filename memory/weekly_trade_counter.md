# Weekly Trade Counter

Week of: 2026-08-10
trades_this_week: 3
last_eod_reset: 2026-08-12
max_trades_per_week: 3
trades_remaining: 0

## Halt Flags
daily_loss_halt: false
halt_reason:
halt_date:

## EOD Reset — 2026-07-31 (Saturday-cycle EOD, closing 2026-07-31 Friday session)
daily_loss_halt set to false (was already false; daily change 0.00%, well within -2% cap,
0 open positions). trades_this_week reset to 0/3 (was already 0/3 — no new entries placed
today).

## EOD Reset — 2026-07-30 (Friday-cycle EOD, closing 2026-07-30 session)
daily_loss_halt set to false (was already false; daily change ~0.00%, well within -2% cap,
0 open positions). trades_this_week reset to 0/3 (was already 0/3 — no new entries placed
today; SPY remained below its 5-day MA per daily_context.md, blocking regular stock entries,
and SH scored 48/100, below the 60 threshold, so no SH entry either).

## EOD Reset — 2026-07-29 (Thursday-cycle EOD, closing 2026-07-29 session)
daily_loss_halt set to false (was already false; daily change -0.0963%, well within -2% cap,
0 open positions). trades_this_week reset to 0/3 (was already 0/3 — no new entries placed
today; the AMD sell filled today was a queued exit order from the 2026-07-28 EOD routine,
not a new trade).

## EOD Reset — 2026-07-27 (Tuesday-cycle EOD, closing Monday 2026-07-27 session)
daily_loss_halt set to false (was already false; daily change -0.38% — AMD's
stop-loss realized loss — well within -2% cap). trades_this_week reset to 0/3
(was already showing 0/3 in this file's header, though AMD was in fact entered
this week via the 08:37 ET market-open trigger and never got counted here — see
portfolio_state.md/reasoning.md for the flagged write-path drift; noting for
follow-up rather than silently correcting the count).

## EOD Reset — 2026-07-04 (Saturday EOD)
daily_loss_halt reset to false by EOD Saturday routine.
trades_this_week reset to 0 for new week (2026-07-07).

## EOD Reset — 2026-07-07 (Tuesday EOD)
daily_loss_halt confirmed/reset to false. trades_this_week confirmed/reset to 0 (was already 0 — no trades placed this week).

## EOD Reset — 2026-07-08 (Thursday EOD)
daily_loss_halt confirmed/reset to false. trades_this_week confirmed/reset to 0 (was already 0 — no trades placed this week).

## EOD Reset — 2026-07-09 (Friday EOD)
daily_loss_halt confirmed/reset to false. trades_this_week confirmed/reset to 0 (was already 0 — no trades placed this week).

## Trade History This Week
| Date | Ticker | Shares | Entry | Order ID |
|---|---|---|---|---|
| (no trades yet) | — | — | — | — |

## EOD Reset — 2026-07-11 (Saturday EOD)
daily_loss_halt confirmed/reset to false. trades_this_week confirmed/reset to 0 (was already 0 — no trades placed this week).

## EOD Reset — 2026-07-14 (Tuesday EOD)
daily_loss_halt set to false. trades_this_week reset to 0 (was already 0 — no trades placed today).

## EOD Reset — 2026-07-15 (Wednesday EOD, closing 2026-07-14 Tuesday session)
daily_loss_halt set to false (was already false). trades_this_week reset to 0 (was already 0 — no trades placed on 2026-07-14).

## EOD Reset — 2026-07-16 (Thursday EOD, closing 2026-07-15 session)
daily_loss_halt set to false (was already false). trades_this_week reset to 0 (was already 0 — no trades placed on 2026-07-15).

- 2026-07-16: BUY AMZN @ $254.25 (counted)

## EOD Reset — 2026-07-16 (Friday-cycle EOD, closing Thursday 2026-07-16 session)
daily_loss_halt set to false (was already false; daily loss -0.26%, well within -2% cap).
trades_this_week reset to 0/3 (was 1/3 — AMZN entry counted for the week is now cleared
per scheduled EOD reset instructions; note AMZN, META, and NVDA were all force-closed
EOD today with no overnight thesis — see reasoning.md and trade_log.md).

## EOD Reset — 2026-07-17 (Saturday-cycle EOD, closing Friday 2026-07-17 session)
daily_loss_halt set to false (was already false; daily gain +0.04%, well within -2% cap).
trades_this_week reset to 0/3 (AAPL and META were both force-closed EOD today with no
overnight thesis — see reasoning.md and trade_log.md; these were exits of an entry
made earlier in the day, per the market-open routine trigger).

- 2026-07-20: BUY AAPL @ $326.77 (counted)

## EOD Reset — 2026-07-20 (Tuesday EOD)
daily_loss_halt set to false (was already false; daily gain +0.03%, well within -2% cap).
trades_this_week reset to 0/3 (was 1/3 — AAPL entry counted for the week is now cleared
per scheduled EOD reset instructions; AAPL, AMZN, and META were all force-closed EOD
today with no overnight thesis — see reasoning.md and trade_log.md).

## EOD Reset — 2026-07-21 (Wednesday EOD)
daily_loss_halt set to false (was already false; daily change -0.00%, well within -2% cap).
trades_this_week reset to 0/3 (was already 0/3 — META was a carried-over position from a
prior undated entry, not a new trade counted this week; force-closed EOD today with no
overnight thesis — see reasoning.md and trade_log.md).

## EOD Reset — 2026-07-23 (Thursday EOD)
daily_loss_halt set to false (was already false; daily change -0.00%, well within -2% cap,
no positions held). trades_this_week reset to 0/3 (was already 0/3 — no trades placed
2026-07-22 or 2026-07-23; the 08:37 ET market-open routine on 07-23 skipped trading
because research was stale — see reasoning.md).

## EOD Reset — 2026-07-24 (Friday EOD)
daily_loss_halt set to false (was already false; daily change 0.00%, well within -2% cap,
no positions held). trades_this_week reset to 0/3 (was already 0/3 — no trades placed
this week).

## EOD Reset — 2026-07-25 (Saturday-cycle routine, re-confirming 2026-07-24 Friday session)
daily_loss_halt re-confirmed false (was already false). trades_this_week re-confirmed 0/3
(was already 0/3). This run found the Friday EOD routine had already reset these same
fields for the same session (see entry above) — no change was needed, values re-verified
against live Alpaca account (equity $99,672.34, 0 open positions, market closed until
2026-07-27).

## EOD Reset — 2026-07-29 (Wednesday EOD, closing 2026-07-28 Tuesday session)
daily_loss_halt set to false (was already false; daily change -0.32%, well within -2% cap).
trades_this_week reset to 0/3 (was already 0/3 — no new entries placed 2026-07-28; the
20sh AMD position had been opened earlier via a prior market-open trigger). AMD force-closed
this routine via sell-to-close order 68f02b84-fc37-4125-bb3c-5f905f181850 — order queued,
pending fill at next market open since Alpaca clock showed market closed at submission time.

## EOD Reset — 2026-08-04 (Tuesday-cycle EOD, closing 2026-08-03 Monday session)
daily_loss_halt set to false (was already false; daily change 0.00%, well within -2% cap,
0 open positions). trades_this_week reset to 0/3 (was already 0/3 — no new entries placed
this week; market-open routine on 2026-08-04 skipped trading due to 4-day-stale pre-market
research). "Week of" header advanced from stale 2026-07-07 to 2026-08-03 (current week) —
the header had not been advancing on prior EOD resets despite the reset log entries below
it moving forward; corrected here.

## EOD Reset — 2026-08-06 (Friday-cycle EOD, closing 2026-08-06 Friday session)
daily_loss_halt set to false (was already false; daily change 0.00%, well within -2% cap,
0 open positions). trades_this_week reset to 0/3 (was already 0/3 — no new entries placed
this week).

## EOD Reset — 2026-08-08 (Saturday-cycle EOD, closing 2026-08-07 Friday session)
daily_loss_halt set to false (was already false; daily change 0.00%, well within -2% cap,
0 open positions). trades_this_week reset to 0/3 (was already 0/3 — no new entries placed
this week).

## EOD Reset — 2026-08-11 (Tuesday-cycle EOD, closing 2026-08-10 Monday session)
daily_loss_halt set to false (was already false; daily change 0.00%, well within -2% cap,
0 open positions). trades_this_week reset to 0/3 (was already 0/3 — no new entries placed
this week).

## EOD Reset — 2026-08-12 (Wednesday-cycle EOD, closing 2026-08-11 Tuesday session)
daily_loss_halt set to false (was already false; daily change 0.00%, well within -2% cap,
0 open positions). trades_this_week reset to 0/3 (was already 0/3 — the 20:37 ET
market-open trigger flagged NVDA/MSFT/PLTR but no fill was ever confirmed on Alpaca,
so no trade counted this week).

## EOD Reset — 2026-08-13 (Thursday-cycle EOD, closing 2026-08-12 Wednesday session)
daily_loss_halt set to false (was already false; daily change 0.00%, well within -2% cap,
0 open positions). trades_this_week reset to 0/3 (was already 0/3 — the 20:37 ET
market-open trigger flagged NVDA/MSFT but no fill was ever confirmed on Alpaca, so no
trade counted this week).

- 2026-08-12: BUY NVDA @ $224.11 (counted)

- 2026-08-12: BUY MSFT @ $492.45 (counted)

- 2026-08-12: BUY NVDA @ $224.11 (counted)
