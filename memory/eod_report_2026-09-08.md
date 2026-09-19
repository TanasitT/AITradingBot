EOD SUMMARY — 2026-09-08 session (compiled by eod-wednesday task, run 2026-09-09)
==================================================

DELIVERY NOTE: This report was NOT emailed. Sending mail on the user's behalf
requires explicit per-run permission and this was an unattended automated run.
Delivered as a file instead.

PORTFOLIO
  Total equity:     $99,811.08
  Daily P&L:        +$127.30 (+0.128%)  vs last_equity $99,683.78
  Cash available:   $84,928.47
  Open positions:   3 (NVDA, AMZN, AMD)

BENCHMARK
  Portfolio: +0.13% | SPY: -0.55% ($765.96) | Alpha: +0.68%

TRADES THIS WEEK: 0/3

TODAY'S TRADES
  No trades executed.
  - Market-open trigger (2026-09-08 09:37 ET) wrote trade_trigger.md
    status=pending, candidates [AMD:80, NVDA:76, AMZN:73, META:70]. The Python
    executor (main.py) did not pick it up — still pending. NVDA/AMZN/AMD already
    near the 5% cap; META (70) was the only actionable new name.

OPEN POSITIONS
  NVDA 22sh | Entry $217.95 | Current $225.41 | +3.42% | Stop $207.05/$202.70 (NONE placed broker-side — 403 at 2026-09-01)
  AMZN 19sh | Entry $254.23 | Current $256.59 | +0.93% | Stop $241.53 (working stop_limit)
  AMD  10sh | Entry $454.31 | Current $504.80 | +11.11% | Stop $431.77 (working stop_limit)

PENDING USER ACTION (not executed by this automated run — no trade execution, even on paper)
  1. AMD TP1 (+8%, $490.65) triggered since 2026-09-08 10:34 ET — sell 3sh (33%);
     on fill, resize AMD sell stop_limit from 10sh to 7sh.
  2. Mechanical EOD rule → force-close NVDA / AMZN / AMD (no hard overnight
     catalyst). Borderline: all three still score >= 70. Flagged, not forced.
  3. NVDA 22sh has NO broker-side protective stop — retry placement.
  4. trade_trigger.md still status=pending — executor/main.py not running.

BOT REASONING TODAY
  EOD — SPY 2026-09-08 close $765.96 vs 5-day MA $767.20 → SPY BELOW its 5-day
  MA. No SH held (inverse-ETF branch N/A). Overnight-thesis web research found no
  company-specific catalyst for the three holdings; scores still >= 70 so the
  hold thesis is borderline-intact. daily_loss_halt stays false (+0.128% day).
  weekly_trade_counter.md reset to 0/3.

MARKET CONTEXT (from daily_context.md, 2026-09-08)
  Regime: RATES + GEOPOLITICS. ~60% odds of a 25bp Fed hike at the Sept 15-16
  FOMC; 10Y near 3-year highs (~4.8%). Renewed US-Iran strikes lifting oil;
  US-Canada trade war a second front. VIX ~15.3 (< 28). Mega-cap AI fundamentals
  firm (NVDA near record). SH score 45 — not eligible. September seasonality
  weak. CPI this week is the next high-impact event.
