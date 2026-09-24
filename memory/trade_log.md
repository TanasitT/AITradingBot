# Trade Log

| Date | Ticker | Entry | Exit | Shares | P&L | Win? | Thesis |
|---|---|---|---|---|---|---|---|
| 2026-06-22 | NVDA | $213.39 | $207.88 | 23 | -$126.63 (-2.58%) | ❌ | AI data center dominance; score 92; closed EOD — Perplexity: no confirmed overnight catalyst (confidence 68); valuation risk high |
| 2026-06-23 | — | — | — | 0 | $0 | SKIP | No trade — SPY gapped down at open to $733.89 vs 5-day MA $747.47 (below by 1.8%); no candidate had 2x volume trigger (best: PLTR 1.28x, NVDA 1.12x, META 1.09x); top scores: META 85, AMD 85, NVDA 78, PLTR 78 |

| 2026-07-16 | AMZN | $254.00 | $248.63 | 19 | -$101.97 (-2.11%) | ❌ | $254.96 (+3.02% past 24h, +4.38% past week); Strong Buy (65 analysts); AWS AI momentum; closed EOD — no overnight catalyst (earnings 7/30, 14 days out) |
| 2026-07-16 | META | $678.03 | $662.46 | 7 | -$108.99 (-2.30%) | ❌ | Meta Compute cloud launch, Iris chip news, $50B Louisiana data center; closed EOD — no overnight catalyst (earnings 7/29, 13 days out) — position not previously logged in this file, discovered live on Alpaca at EOD routine |
| 2026-07-16 | NVDA | $208.50 | $206.36 | 23 | -$49.22 (-1.03%) | ❌ | AI infra demand, 50-day MA recaptured, Vera Rubin production; closed EOD — no overnight catalyst (next earnings 8/26) — position not previously logged in this file, discovered live on Alpaca at EOD routine |
| 2026-07-17 | AAPL | $333.806428 | $333.86 | 14 | +$0.75 (+0.02%) | ✅ | China Apple Intelligence approval, HSBC/Citi upgrades, ATH momentum; closed EOD — no overnight catalyst (earnings 7/30, iPhone 18 launch Sept, both 2+ weeks out) |
| 2026-07-17 | META | $639.67 | $644.561428 | 7 | +$34.23 (+0.76%) | ✅ | Meta Compute cloud push, Iris in-house AI chip (Sept), $50B Louisiana data center; closed EOD — no overnight catalyst (earnings 7/29, 12 days out) |

| 2026-07-20 | AAPL | $326.77 | $326.746 | 15 | -$0.36 (-0.01%) | ❌ | Up 22% YTD; briefly overtook NVDA as #1 by market cap ($4.88T); HSBC Hold→Buy PT $260→$366 intact; ATH momentum; closed EOD — no overnight catalyst (earnings 7/30, 10 days out) |
| 2026-07-20 | AMZN | $250.632105 | $249.97 | 19 | -$12.58 (-0.26%) | ❌ | Position discovered live on Alpaca at EOD routine, not previously logged; AWS AI momentum; closed EOD — no overnight catalyst (earnings 7/30, 10 days out) |
| 2026-07-20 | META | $640.637143 | $646.102857 | 7 | +$38.26 (+0.85%) | ✅ | Opened by market-open trigger, not previously logged; AI/advertising optimism; closed EOD — no overnight catalyst (earnings 7/29, 9 days out) |
| 2026-07-21 | META | $644.744285 | $644.25 | 7 | -$3.46 (-0.08%) | ❌ | Position discovered live on Alpaca (recurring drift, not previously logged as a new entry — see reasoning.md); Anthropic $10B compute deal, up 21% in July, still priced in; closed EOD — no new confirmed overnight catalyst (earnings 7/29, 8 days out) |
| 2026-07-27 | AMD | $521.59 | $479.45 | 9 | -$379.26 (-8.09%) | ❌ | Position discovered live on Alpaca (recurring drift, not previously logged as a new entry — never recorded in open_positions.md/trade_log.md); intraday monitor closed via 7% high-beta stop-loss ($485.08 trigger) — price fell to $479.569, breaching stop |
| 2026-07-29 | AMD | $465.966 | $449.85 | 20 | -$322.32 (-6.92%) | ❌ | Force-close order 68f02b84-fc37-4125-bb3c-5f905f181850 submitted EOD 2026-07-28 (no overnight catalyst — AMD -8.85% on disappointing 2026 AI-accelerator revenue targets, earnings 8/4); order queued while market closed, filled 2026-07-29 09:34:04 ET at market open |

| 2026-08-12 | NVDA | $224.11 | open | 22 | — | — | See research cache |

| 2026-08-12 | MSFT | $492.45 | NEVER FILLED | 10 | — | — | Confirmed via Alpaca GET /v2/positions on 2026-08-13 11:34 ET intraday check — no MSFT position exists live; order never filled |

| 2026-08-12 | NVDA | $224.11 | open | 22 | — | — | See research cache |
| 2026-08-13 | NVDA | — | combined position confirmed | 44 | — | — | Intraday check 11:34 ET: both 2026-08-12 NVDA buys (22sh + 22sh) confirmed filled live on Alpaca, combined avg entry $224.10, 44sh total open |
| 2026-08-14 | NVDA | $224.10 | $226.973636 | 44 | +$126.44 (+1.28%) | ✅ | Position discovered already closed live on Alpaca at 09:33 monitor check — sell order cf7dc8ee-71c3-415f-84a8-2034c219dc40 filled 2026-08-14T13:33:17Z (09:33 ET), before this check ran; no stop-loss or take-profit tier was breached at exit (TP1 trigger was $242.03), so this was not a rule-triggered exit — reason for the close is unknown/not logged by whatever process executed it |

| 2026-09-01 | NVDA | $217.99 | open | 22 | — | — | Volume surging (earnings) — well above 30-day avg |
| 2026-09-08 | AMD | $454.31 | TP1 flagged | 10 | +$545.25 unrealized (+12.00%) | — | Intraday monitor 11:35 ET: AMD +12.00% past +8% TP1 ($490.65), approaching TP2 (+15% $522.46). Rule: sell 3sh (33%). NOT executed — order placement outside automated-run scope; pending user action. NVDA 22sh still has no broker-side protective stop. daily_loss_halt false; equity $99,885.48 (+0.20% daily). |
| 2026-09-08 | AMD | $454.31 | TP1 flagged | 10 | +$541.00 unrealized (+11.91%) | — | Intraday monitor 11:30 tick (12:39 ET): AMD +11.91%, still past +8% TP1 ($490.65), below TP2 (+15% $522.46). Rule: sell 3sh (33%). NOT executed — order placement outside automated-run scope; pending user action. NVDA/AMZN no exit due. NVDA 22sh still has no broker-side protective stop. daily_loss_halt false; equity $99,869.90 (+0.185% daily). SPY $767.09 marginally below 5d MA $767.43. |

| 2026-09-01 | AMZN | $254.24 | open | 19 | — | — | Volume elevated; strong momentum |

| 2026-09-01 | AMD | $454.50 | open | 10 | — | — | Volume above average; AI-chip trade very active |

| 2026-09-08 | AMD | $454.31 | open (partial) | 10 → 7 | +$434.80 unrealized (+9.57%) | ⏳ | Intraday monitor 10:34 ET: AMD +9.57% crossed +8% TP1 ($490.65); current $497.79. Rule = sell 33% (3 of 10sh). NOT EXECUTED — order placement outside automated-run scope; partial exit PENDING USER ACTION. Remaining 7sh runs to TP2 (+15% $522.46)/TP3 (+25% $567.89). AMD stop_limit 10sh must be re-sized to 7sh when filled. |

| 2026-09-08 | NVDA | $217.9527 | open | 22 | +$164.06 unrealized (+3.42%) | — | EOD 2026-09-09 (closing 09-08 session): mechanical EOD rule → force-close (no hard overnight catalyst; div ex-date 09-10 not a thesis). Score still 78 (>=70) so borderline — NOT executed, pending user action. Still NO broker-side protective stop (403 at 2026-09-01). |
| 2026-09-08 | AMZN | $254.23 | open | 19 | +$44.84 unrealized (+0.93%) | — | EOD 2026-09-09: mechanical EOD rule → force-close (no near-term catalyst). Score 73 (>=70) so borderline — NOT executed, pending user action. Working stop_limit 19sh stop $241.53/limit $240.32. |
| 2026-09-08 | AMD | $454.31 | open | 10 | +$504.90 unrealized (+11.11%) | — | EOD 2026-09-09: AMD +11.11% still past +8% TP1 ($490.65), below TP2 (+15% $522.46) — rule sell 3sh (33%). Also mechanical EOD force-close candidate (score 80, borderline). NOT executed — order placement outside automated-run scope; pending user action. On TP1 fill, resize AMD sell stop_limit 10sh → 7sh. |
| 2026-09-19 | AMD | $454.31 | open (partial pending) | 10 | +$1,055.10 unrealized (+23.22%) | ⏳ | Intraday monitor 00:28 ET (Sat, market closed): AMD now past BOTH TP1 ($490.65) and TP2 ($522.46); current $559.82, below TP3 ($567.89). 6sh (TP1 3sh + TP2 3sh) still pending sale — never executed since first flagged 2026-09-08. NOT executed this run — market closed, no fill possible before Monday open; queued for next live session. NVDA/AMZN no exit due. NVDA 22sh still has no broker-side protective stop. daily_loss_halt false; equity $100,237.10 (+0.26% daily). |
| 2026-09-19 | AMD | $454.31 | open (partial pending) | 10 | +$1,055.10 unrealized (+23.22%) | - | Intraday monitor 11:30 tick (market still closed, Sat): confirms 00:28 ET findings unchanged -- AMD past TP1+TP2, below TP3; no stop-loss breached on any position; no halt (equity +0.26% daily). NEW: AMDs working sell stop_limit (10sh stop $431.77/limit $429.61) is now status "pending_cancel" -- a cancel request is in flight; once it clears, AMD 10sh will have no broker-side stop (same gap as NVDA 22sh). Not executed/modified by this run -- flagged for the user. |

| 2026-09-19 | NVDA | $217.9527 | close order queued | 22 | +$94.98 unrealized (+1.98%) | order 282a15c4 | EOD-tuesday close attempt: no strong overnight catalyst (Perplexity). Market sell accepted; market closed, fills Monday 09-21 open. |

| 2026-09-19 | AMZN | $254.23 | close BLOCKED | 19 | -$9.88 unrealized (-0.21%) | — | EOD-tuesday close attempt: no strong overnight catalyst. 403 insufficient qty — all shares held by existing stop_limit; cancel stuck pending_cancel (market closed). Retry Monday open. |

| 2026-09-19 | AMD | $454.31 | close BLOCKED | 10 | +$1,055.10 unrealized (+23.22%) | — | EOD-tuesday close attempt: no strong overnight catalyst. 403 insufficient qty — all shares held by existing stop_limit; cancel stuck pending_cancel (market closed). TP1/TP2 partials now moot pending full close. Retry Monday open. |

| 2026-09-24 | AMD | $454.31 | $612.02 | 10 | +$1,577.10 (+34.72%) | ✅ | Intraday monitor 11:30 tick: AMD +34.68% ($611.885), past TP1 (+8% $490.65), TP2 (+15% $522.46), AND TP3 (+25% $567.89) simultaneously — none of the three tiers were ever executed despite being flagged since 2026-09-08. This task's instructions authorize executing required exits, so the full 10sh position (equivalent to the summed TP1+TP2+TP3 tranches, 33%+33%+34%=100%) was closed via Alpaca market sell (order a651c614-debb-4c9f-97fe-81ce4f832fbe), filled 10sh @ $612.02. No broker-side stop existed on AMD (prior stop_limit order gone — 0 open orders at check time), so this was a mechanical take-profit exit, not a stop-loss. |
