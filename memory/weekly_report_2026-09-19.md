WEEKLY SUMMARY — Week of 2026-09-14 (also backfills Week of 2026-09-07)
==================================================

PORTFOLIO
  Total equity:     $100,237.10
  Week P&L:         +$426.02 (+0.43%) [09-08 close $99,811.08 -> 09-18 close $100,237.10]
  Cash available:   $84,928.47
  Open positions:   3 (NVDA, AMZN, AMD)
  First week-ending close above the original $100,000 baseline (2026-06-15) since tracking began

BENCHMARK
  Portfolio: +0.43% | SPY: -0.57% ($765.96 -> $761.62) | Alpha: +0.99%

TRADES THIS WEEK: 0/3 (3rd straight week of zero new entries; last entries were 2026-09-01)

THIS WEEK'S TRADE ACTIVITY (no fills — all attempts/flags only)
  - AMD: crossed BOTH take-profit tiers (TP1 +8% $490.65 on 09-08, TP2 +15% $522.46 by mid-week). 6sh partial-sell (60% of position) flagged, never executed — automated runs cannot place orders.
  - NVDA: EOD close attempt (order 282a15c4) accepted as a market sell but market was closed — QUEUED, unfilled, expected to fill at Monday 2026-09-21 09:30 ET open.
  - AMZN: EOD close attempt BLOCKED — 403 "insufficient qty," all 19sh held by its existing stop_limit; the order's cancel request is stuck "pending_cancel."
  - AMD: EOD close attempt BLOCKED for the same reason — cancel of its stop_limit also stuck "pending_cancel."

OPEN POSITIONS (as of 2026-09-18 close)
  AMD   10sh | Entry: $454.31   | Current: $559.82   | +23.22% | Stop: $431.59 (5%) — own stop_limit currently "pending_cancel" (temporarily unprotected)
  AMZN  19sh | Entry: $254.23   | Current: $253.71   | -0.21%  | Stop: $241.52 (5%) — working stop_limit in place (cancel attempt stuck pending)
  NVDA  22sh | Entry: $217.9527 | Current: $222.27    | +1.98%  | Stop: NONE — no broker-side protective stop since placement failed (403) on 2026-09-01, unresolved 18 consecutive days

WEEKLY PERFORMANCE STATS (from performance_metrics.md, computed this run)
  All-time: 13 trades, 4 wins, 30.8% win rate, profit factor 0.181 — unchanged, nothing closed in 3 weeks
  This week (09-14 to 09-18): 0 trades, $0.00 realized P&L, +$1,140.20 unrealized (NVDA +$94.98, AMZN -$9.88, AMD +$1,055.10)
  Backfilled week (09-07, Labor Day-shortened): 0 trades, $0.00 realized, +$713.80 unrealized at 09-08 close; AMD's TP1 was hit and missed that week too

BOT REASONING THIS WEEK (selected highlights — full detail in reasoning.md)
  Every EOD/monitor run this week reached the same conclusion: no hard company-specific
  overnight catalyst for NVDA/AMZN/AMD (moves read as a broad semiconductor-sector
  rebound, not company news), but all three still score >= 70 so the mechanical
  force-close rule was treated as borderline and not forced — until the final 2026-09-19
  eod-tuesday run, which was explicitly instructed to execute the closes and hit the
  stop_limit-cancel blocker described above.

MARKET CONTEXT
  SPY ranged $761.62-$770.18 this week/prior week, staying near its 5-day MA throughout
  (no SH inverse-ETF entries triggered). VIX was not explicitly logged this week in any
  memory file — a standing 13+ week gap.

NEW / ESCALATED RISKS THIS WEEK
  1. NVDA has now gone 18 consecutive days with NO broker-side protective stop.
  2. AMD's own protective stop — previously the one reliable one — is now ALSO stuck in
     "pending_cancel" limbo as a side effect of Friday night's close attempt, exposing
     the position with the largest unrealized gain (+23.22%) right when it has the most
     to lose from a reversal.
  3. A newly discovered failure mode: even when a run IS explicitly permitted to close
     positions, Alpaca's paper account would not finalize the stop_limit cancels needed
     to free the shares while the market was closed — AMZN and AMD are effectively stuck
     until Monday's open regardless of what the bot decides.
  4. Separately, git status shows uncommitted changes in engine/risk_manager.py and
     engine/coordinator.py that appear to remove the volume (>=1.25x) entry gate and the
     technical-soundness check ahead of new buy decisions — flagged in reasoning.md,
     not evaluated or acted on by this run, needs review before Monday's market-open
     routine runs live code.

OUTSTANDING ITEMS NEEDING ATTENTION (Monday 2026-09-21 market open)
  1. Confirm NVDA's queued market-sell filled.
  2. Retry AMZN/AMD stop cancel + close now that the market is open.
  3. Place a working NVDA stop if any of the three positions are kept.
  4. Resolve AMD's TP1+TP2 partial-sell backlog (6sh) if the full close doesn't happen.
  5. Review the uncommitted engine/*.py changes (flagged above) before they run live.

FULL DETAIL: see memory/trade_log.md, memory/performance_metrics.md,
memory/benchmark_tracking.md, and memory/learned_patterns.md (Weekly Reflection —
Week of 2026-09-14) for complete numbers and analysis.
