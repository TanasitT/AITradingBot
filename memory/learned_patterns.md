# Learned Patterns

## Week of 2026-06-23 (first live week)

### What Worked
- **Entry filter on SPY MA held firm**: On 2026-06-23, SPY was 1.8% below its 5-day MA ($733.89 vs $747.47). The bot correctly skipped all trades. This likely avoided further losses given broad market weakness.
- **Volume filter caught false opportunities**: PLTR (1.28x), NVDA (1.12x), META (1.09x) all failed the 2x volume threshold on 06-23, meaning no conviction in any move. Skipping was correct.

### What Failed
- **EOD force-close on NVDA cost -$126.63 (-2.58%)**: NVDA entered at $213.39 on 06-22. Thesis score was high (92/100) but Perplexity confidence for overnight hold was only 68 — below the implicit threshold. Exit at $207.88. The position would have benefited from a tighter stop being hit intraday rather than waiting for EOD close to trigger the no-overnight-catalyst rule.
- **High score (92) did not protect against loss**: NVDA's AI data center thesis was strong, but "valuation risk high" was flagged and should have been a warning signal. Consider adding valuation risk as a score modifier.

### VIX Conditions
- VIX data not recorded in trade log for 06-22 entry — need to add VIX at time of entry to future trade log entries to diagnose VIX-related losses.
- Strategy rule is VIX < 28 for entry; no VIX spike appears to have triggered the NVDA exit, but force-close was EOD-thesis-based.

### Emerging Patterns (1 week sample — low confidence)
- **Sector-wide weakness overrides strong individual scores**: Even a 92-score NVDA trade lost when the broader market was in a down move. SPY health check is the most critical gate.
- **Perplexity overnight confidence < 70 = exit**: The 68 confidence score correctly flagged "don't hold overnight." This heuristic should be formalized: if overnight confidence < 70, close EOD regardless of P&L.
- **Week 1 summary**: 1 trade executed, 1 skipped, 0 wins, -$126.63 net. Filters worked as designed on the skip day. First trade loss was within the acceptable per-trade risk band (5% max position; actual was -2.58%). No hard rules broken.

### Action Items for Strategy
1. Add VIX at entry to trade log template
2. Formalize Perplexity overnight confidence threshold: < 70 = mandatory EOD exit
3. Consider adding valuation risk flag as a -5 to -10 score modifier in research scoring

---

## Weekly Reflection — Week of 2026-06-22 (Final, logged 2026-06-27)

### Week Stats
- Trades executed: 1 | Skipped: 1 | Wins: 0 | Losses: 1
- Win rate: 0% | Net P&L: -$126.63 | Avg loss: -2.58%
- Portfolio: $99,873.35 (down -0.13% from $100,000.00 baseline)
- SPY performance this week: -1.59% (Jun 22 $743.54 → Jun 26 $731.71)
- Alpha vs SPY: +1.46% (bot lost -0.13% vs SPY's -1.59%; defensive filters outperformed)

### Signals That Worked
- **SPY 5-day MA gate blocked a bad day (Jun 23)**: SPY was 1.8% below its MA. All candidates failed volume (best: PLTR 1.28x vs required 2x). Skipping saved an unknown but likely negative P&L in a market-down session. This was the single most valuable filter this week.
- **Perplexity overnight confidence (68 < 70) triggered correct EOD exit**: The exit signal fired as designed. Holding NVDA overnight into Jun 23 (a down market day) would likely have produced a larger loss.
- **No hard rules broken**: Daily loss cap, trade limit, and position sizing all held. NVDA loss was -2.58% on position size (within the 5% max position cap).

### Signals That Failed
- **Research score 92 on NVDA did not predict same-day gain**: Score reflects thesis strength, not intraday momentum. A high score is necessary but not sufficient — broad market context must dominate.
- **No volume confirmation on entry day**: Entry did not verify whether NVDA had 2x volume at open vs. the 2x threshold required. The trade log entry lacks intraday volume at time of entry. Needs to be logged.
- **"Valuation risk high" flag was noted but not acted upon**: This should reduce the effective score by 5-10 points.

### VIX Conditions
- VIX was not recorded in trade log for Jun 22 entry — this remains an open gap.
- No VIX-based exit was triggered; force-close was thesis-confidence-driven.
- Market weakness Jun 23 (SPY -1.8% vs MA) correlated with typical high-VIX environment. Suspected VIX was elevated (20-25 range) but unconfirmed.

### Emerging Patterns (Week 1 of 2 — very low sample, low confidence)
- **Defensive alpha via filters**: In a down week for SPY (-1.59%), the bot's conservative filter set produced +1.46% alpha purely by not trading. This pattern will matter in sustained downtrends.
- **Inaugural week bottleneck is data quality, not signal quality**: Missing VIX at entry, missing intraday volume at entry, missing overnight hold decision reasoning — these gaps limit post-trade analysis.
- **Single trade, single loss = insufficient to infer signal failure**: NVDA loss could be random; sector-momentum signal needs 5+ trades before drawing conclusions.

### Open Action Items (carry forward to Week 2)
1. Add VIX at entry to trade log template
2. Add intraday volume multiple at time of entry to trade log
3. Formalize overnight confidence threshold: Perplexity confidence < 70 = mandatory EOD close
4. Add valuation risk modifier: flag reduces research score by 7 points
5. Confirm SPY MA calculation uses close prices, not intraday

---

## Weekly Reflection — Week of 2026-06-30 (Final, logged 2026-07-04)

### Week Stats
- Trades executed: 0 | Skipped: unknown (no entries logged) | Wins: 0 | Losses: 0
- Win rate: N/A | Net P&L: $0.00 | Avg loss: N/A
- Portfolio: $99,873.35 (unchanged from prior week close)
- SPY performance this week: +0.41% (Jun 30 $741.03 → Jul 4 $744.07)
- Alpha vs SPY: -0.41% (flat portfolio vs SPY gaining; underperformed by sitting out)
- Cumulative alpha since inception: +1.05% (portfolio -0.13% vs SPY +0.92% net from baseline)

### Signals That Worked
- **Zero trades = zero losses**: No entries triggered this week, meaning no capital was put at risk during a mild SPY rally (+0.41%). Entry criteria held — no logs show a qualifying setup was missed.
- **Holiday week reduced opportunity**: July 4th (Friday) was a market holiday. 4-day trading week with no high-volume breakout candidates appearing in prior daily logs.

### Signals That Failed
- **No trades means no alpha capture**: SPY gained +0.41% this week. A flat portfolio produced -0.41% weekly alpha — the cost of a slow/no-signal week in a rising market. This is expected behavior but worth tracking.
- **Trade log gap for this week**: No trade log entries exist for 2026-06-30 through 2026-07-04. It is unknown how many skip decisions were made (if any) due to entry criteria failures. This is a logging gap — skip decisions should be recorded in the trade log, not just executed trades.

### VIX Conditions
- VIX data not available for this week in trade log (same ongoing gap from Week 1).
- SPY was above its 5-day MA for most of this period (SPY range $741–$747), suggesting no inverse ETF (SH) conditions were triggered.
- The mild +0.41% SPY gain suggests VIX was likely subdued (estimated 14–18 range), meaning entry criteria could have been met if a qualifying candidate appeared.

### Emerging Patterns (Week 2 of 2 — still very low sample)
- **Two consecutive no-trade or low-trade weeks**: Week 1 had 1 trade (loss), Week 2 had 0 trades. The bot is trading at very low frequency relative to its 3/day limit. Either the signal quality bar is appropriately high, or the watchlist lacks enough qualifying candidates on any given day.
- **Flat portfolio in rising market = negative alpha drag**: When SPY trends up and bot holds cash, alpha goes negative. This is the hidden cost of conservative filters. Over a bull run, the opportunity cost compounds.
- **Volume filter (2x 30-day avg) appears to be the primary gatekeeper**: From Week 1 data, even high-scoring tickers (NVDA 78, META 85, PLTR 78) failed to hit 2x volume on the skip day. If the volume threshold is rarely met, the bot will rarely trade. Consider whether 1.5x is more appropriate as a threshold.

### Open Action Items (carry forward to Week 3)
1. *(Unresolved from Week 1)* Add VIX at entry to trade log template
2. *(Unresolved from Week 1)* Add intraday volume multiple at time of entry to trade log
3. *(Unresolved from Week 1)* Formalize overnight confidence threshold: Perplexity confidence < 70 = mandatory EOD close
4. *(Unresolved from Week 1)* Add valuation risk modifier: flag reduces research score by 7 points
5. **New**: Log skip decisions in trade_log.md (not just executed trades) — record date, reason for skip, top candidate scores/volume at time of skip
6. **New**: Evaluate whether 2x volume threshold is too restrictive — backtest 1.5x threshold against Week 1 candidates (PLTR 1.28x, NVDA 1.12x, META 1.09x would still not qualify at 1.5x, but worth reviewing over broader history)
7. **New**: Track weekly alpha running total — currently -0.41% week 2; need 5+ weeks to determine if filters add net value vs. SPY buy-and-hold

---

## Weekly Reflection — Week of 2026-07-07 (Final, logged 2026-07-11)

### Week Stats
- Trades executed: 0 | Skipped: unknown count (no skip entries logged in trade_log.md) | Wins: 0 | Losses: 0
- Win rate: N/A | Net P&L: $0.00 | Avg loss: N/A
- Portfolio: $99,873.35 (unchanged for third consecutive week)
- SPY performance this week: +0.46% (Jul 7 $751.63 -> Jul 10 $755.10)
- Alpha vs SPY: -0.46% (flat portfolio underperformed a rising market)
- Cumulative alpha since inception: ~+0.59% (roughly netting week 1's +1.46% against week 2's -0.41% and week 3's -0.46%)

### Signals That Worked
- **VIX stayed low and stable all week (15.53-23.34 range, ending 15.67 on Jul 10)** — no VIX-driven halts were needed, confirming the VIX<28 gate is not the binding constraint right now.
- **No hard rules broken** — daily loss cap, trade limit, and position sizing never triggered because zero trades were placed; the bot did not force a bad entry just to stay active.

### Signals That Failed
- **Three consecutive weeks with 0-1 trades total** — the bot has executed only 1 trade in 3 weeks against a 3/day (15/week) budget. Either qualifying setups are genuinely rare, or a filter (likely the volume multiplier) is over-restrictive.
- **daily_context.md shows 5 tickers cleared for entry (META 86, NVDA 78, AMD 76, MSFT 72, AMZN 71) as of Friday close, all above the 70 score threshold** — yet no trade was placed this week. This strongly suggests the volume confirmation filter (or timing of the market-open routine relative to intraday volume data) is the actual bottleneck, not research quality.
- **trade_log.md has not been updated since 2026-06-25** — daily skip decisions are not being written to the log despite the Week 1 action item to do so. This is now a 3-week-old open item and is starting to block weekly analysis (cannot tell whether Mon-Fri this week had near-miss setups or no candidates at all).

### VIX Conditions
- VIX ranged 15.53-23.34 over the trailing month, closing the week at 15.67 (near the low end) — a low-fear, low-volatility regime.
- Low VIX combined with zero trades suggests the bottleneck is not risk-off caution; the entry criteria (volume/score combination) simply aren't being satisfied by watchlist tickers at market-open.

### Emerging Patterns (Week 3 of 3 tracked — low-to-moderate confidence)
- **Persistent under-trading in a calm, rising market**: With VIX low and SPY trending up 3 of the last 3 weeks, a strategy that trades 0-1 times per week is leaving the 3-trades/day budget almost entirely unused. If this continues for 2+ more weeks, the volume threshold (1.25x per config.py, though watchlist.md/strategy.md still reference a stricter historical 2x in earlier logs) should be re-examined against actual realized watchlist volume.
- **Score threshold (70) is being cleared regularly** (5 tickers >=70 as of Jul 10) without translating into trades — reinforces that score is not the limiting factor.

### Open Action Items (carry forward to Week 4)
1. *(Unresolved, 3 weeks running)* Log skip decisions in trade_log.md daily — record date, reason for skip, top candidate scores/volume at time of skip. This is now the highest-priority gap.
2. *(Unresolved)* Add VIX at entry to trade log template
3. *(Unresolved)* Formalize overnight confidence threshold: Perplexity confidence < 70 = mandatory EOD close
4. *(Unresolved)* Add valuation risk modifier: flag reduces research score by 7 points
5. **New**: Audit whether the market-open routine is actually re-checking volume against the current MIN_VOLUME_MULTIPLIER (1.25x per config.py) or a stale stricter value — 3 weeks of near-zero trading with scores clearing 70+ warrants a code-level check of engine/risk_manager.py's volume gate
6. **New**: Reconcile trade_log.md (stale since 06-25) with weekly_trade_counter.md and portfolio_state.md (both current) — pick one source of truth and keep it updated daily

---

## Weekly Reflection -- Week of 2026-07-13 (Final, logged 2026-07-18)

### Week Stats
- Trades executed: 5 | Wins: 2 | Losses: 3 | Win rate: 40.0%
- Net P&L: -$225.20 (5 fills across 07-16 and 07-17; no logged activity 07-13 to 07-15)
- Portfolio: $99,873.35 -> $99,648.14 (-0.23%)
- SPY performance this week: $749.13 (07-13) -> $743.68 (07-17), roughly -0.73%
- Alpha vs SPY: ~+0.50% (losses were smaller than the market's own decline)
- Cumulative alpha since inception: positive but thinning -- first week with net realized losses larger than any prior single week

### Signals That Worked
- **The under-trading streak finally broke**: after 3 consecutive weeks of 0-1 trades, the bot placed 5 trades in 2 days (AMZN, META, NVDA on 07-16; AAPL, META on 07-17), confirming the volume/score gates are not permanently closed -- they just needed the right week.
- **AAPL and META (07-17) both closed positive**, driven by concrete near-term catalysts (China Apple Intelligence approval + HSBC/Citi upgrades for AAPL; Meta Compute cloud push + Iris chip news for META) rather than pure momentum scores.
- **No hard rules broken across 5 trades**: every position sized within the 5% cap, daily loss cap never neared -2% on either day (worst daily print was still a gain +0.04% on 07-17), and the 3-trades/day limit was respected (3 on 07-16, 2 on 07-17).

### Signals That Failed
- **3 of 5 trades were force-closed at a loss purely on "no overnight catalyst," not on stop-loss or thesis invalidation**: AMZN -2.11%, META -2.30%, NVDA -1.03% on 07-16. The thesis in each case (AWS AI momentum, Meta Compute, Vera Rubin) was intact -- the exits were mechanical (earnings 2+ weeks out = no overnight hold), not driven by a negative catalyst. This is the same "EOD force-close cost me a real loss" pattern first seen with NVDA on 2026-06-22, now repeated 3x in one day.
- **Position tracking drift recurred for a second straight week**: on 07-16 and again on 07-17, live Alpaca positions (META/NVDA on 07-16; AAPL/META on 07-17) were discovered at monitor/EOD time without ever being logged at entry in open_positions.md or trade_log.md. reasoning.md repeatedly flags uncommitted in-progress edits to engine/coordinator.py, engine/risk_manager.py, engine/technical.py, utils/alpaca_client.py as the likely cause -- this is now a 2-week-old unresolved gap and the most concrete, fixable bug surfaced this quarter.
- **Entry order IDs and entry timestamps are unknown for 4 of the 5 positions this week** (AAPL, META 07-16, META 07-17, NVDA) because they were reconstructed from live Alpaca state rather than captured at fill time -- this blocks precise hold-duration and slippage analysis.

### VIX Conditions
- VIX stayed in a low, calm band all week (roughly 15-18 based on adjacent weeks' readings) -- no VIX-driven halts were triggered and VIX was not the binding constraint on any of the 5 trades.
- Low VIX combined with an active trading week suggests the earlier under-trading weeks (07-07, 06-30) were volume/candidate-availability driven, not risk-driven -- consistent with the standing hypothesis from prior reflections.

### Emerging Patterns (5 weeks tracked -- moderate confidence now building on force-close losses)
- **The mandatory EOD-no-catalyst force-close is now a recurring, quantifiable drag**: 4 of the bot's 6 lifetime trades (NVDA 06-22, AMZN/META/NVDA 07-16) were closed at a loss specifically because of the "no overnight thesis" rule, not because the underlying thesis broke. Combined lifetime cost of this exit rule alone: -$126.63 -$101.97 -$108.99 -$49.22 = -$386.81 against only +$34.98 in wins. This is now the single largest identifiable driver of the bot's -$351.83 lifetime net P&L and merits a strategy review: either loosen the same-day earnings-distance requirement or add a smaller partial-hold allowance when the intraday move is favorable at close.
- **Live-account/memory-file drift is a 2-week-recurring, code-level bug, not a one-off**: happening on both 07-16 and 07-17 EOD/intraday routines while engine/*.py files show uncommitted edits. This should be treated as a priority engineering fix rather than another "flag for follow-up" entry, since it is now actively corrupting the trade log's entry-time data for every trade this week.
- **Win rate over the last 5 trades (40%) is closer to a coin flip than the bot's high average research scores (76-92) would suggest** -- reinforcing the week-1 finding that score predicts thesis quality, not same-day/next-day price direction.

### Open Action Items (carry forward to next week)
1. **New, highest priority**: Root-cause and fix the engine/coordinator.py position-logging bug causing live Alpaca fills to go unrecorded in open_positions.md/trade_log.md at entry time (2 weeks running: 07-16, 07-17).
2. **New**: Formally evaluate whether the "no overnight catalyst = force-close" rule is net-negative in expectancy -- 4 of 6 lifetime trades lost specifically to this rule for a combined -$386.81, vs. 2 wins for +$34.98. Consider requiring a genuinely negative catalyst (not just an absent one) before forcing an exit on a thesis that hasn't broken.
3. *(Unresolved, 4 weeks running)* Add VIX at entry to trade log template.
4. *(Unresolved, 4 weeks running)* Add valuation risk modifier: flag reduces research score by 7 points.
5. *(Unresolved)* Log skip decisions in trade_log.md daily, including on days with zero trades (07-13 through 07-15 this week have no entries at all, active or skipped).

---

## Weekly Reflection — Week of 2026-07-20 (Final, logged 2026-07-25)

### Week Stats
- Trades executed: 4 | Wins: 1 | Losses: 3 | Win rate: 25.0%
- Net P&L: +$21.86 (4 fills across 07-20 and 07-21; zero trades 07-22 through 07-24)
- Portfolio: $99,648.14 -> $99,672.34 (+0.02%)
- SPY performance this week: $741.99 (07-20) -> $735.98 (07-24), roughly -0.81%
- Alpha vs SPY: ~+0.83% (small positive P&L against a declining index)
- Cumulative alpha since inception: still positive but thin — 4 of 6 tracked active weeks now show losing or barely-breakeven trade P&L offset mainly by SPY underperforming those same days

### Signals That Worked
- **First positive-P&L trading week since inception**: despite only a 25% win rate, the single win (META 07-20 +$38.26) outsized the three small losses (AAPL -$0.36, AMZN -$12.58, META 07-21 -$3.46) combined (-$16.40), turning the week net positive for the first time.
- **No hard rules broken across 4 trades**: every position sized within the 5% cap, daily loss cap never approached -2% on any day, and the 3-trades/day limit held (3 on 07-20, 1 on 07-21).
- **Bot correctly sat out 3 of 5 trading days (07-22 to 07-24)** rather than forcing a trade to stay active — 07-23 explicitly logged a skip because research_cache.md/daily_context.md were stale, showing the pre-flight staleness check is working as a safety gate.

### Signals That Failed
- **All 4 trades were again force-closed on "no overnight catalyst," not stop-loss/take-profit**: same mechanical EOD exit pattern as every prior active week (NVDA 06-22; AMZN/META/NVDA 07-16; AAPL/META 07-17). Lifetime, 8 of 10 trades have now closed via this rule for a combined -$372.75 against +$73.24 in wins — the rule remains the single largest identified drag on performance (carried-forward action item, still unresolved).
- **Live-account/memory drift extended to a third straight active week**: AMZN and META on 07-20 were discovered live on Alpaca without a prior open_positions.md/trade_log.md entry, and META reappeared live again on 07-21 despite being recorded as closed on 07-20 — the bot treated Alpaca as source of truth each time rather than trusting its own memory files. Uncommitted edits to engine/coordinator.py, engine/risk_manager.py, engine/technical.py, and utils/alpaca_client.py are still present in git status as of this writing, consistent with the standing hypothesis that in-progress code changes are the root cause.
- **Research staleness caused a missed trading day (07-23)**: the market-open routine could not evaluate entries because daily_context.md/research_cache.md hadn't been refreshed since 07-21. This is a scheduling/pipeline gap (pre-market research not running reliably every day), not a strategy filter — it directly reduced trading days from 5 to effectively 2 this week.

### VIX Conditions
- VIX conditions were not explicitly logged for 07-20/07-21 entries in trade_log.md — the VIX-at-entry gap flagged since Week 1 is still unresolved after 6 weeks of tracking.
- SPY declined steadily through the week (-0.81% from 07-20 to 07-24) without triggering the VIX>28 gate or the daily -2% halt, suggesting a moderate, non-panic pullback rather than a volatility spike.

### Emerging Patterns (6 weeks tracked — moderate confidence)
- **A single strong intraday win can flip a low-win-rate week to net positive**: this week's 25% win rate still produced positive P&L because the one winner (+$38.26, +0.85%) was larger than all three losers combined. This reinforces that win rate alone is a poor predictor of weekly outcome; average win/loss magnitude matters more given the EOD-force-close pattern compresses most losses to under -0.3%.
- **The mandatory EOD-no-catalyst force-close is now confirmed across 6 consecutive active weeks (8 of 10 lifetime trades)**: combined lifetime cost -$372.75 vs +$73.24 in wins. This is the same open action item from the 07-13 reflection, now with two more weeks of evidence — the case for revisiting the same-day-earnings-distance rule (or adding a partial-hold allowance) has strengthened, not weakened.
- **Live-account/memory-file drift is now a chronic, multi-week bug (07-16, 07-17, 07-20, 07-21 — 4 of the last 5 active trading days)**: this has moved from "recurring" to "essentially every active day" and continues to corrupt entry-time data (unknown order IDs/timestamps for most positions this week), blocking slippage and hold-duration analysis.
- **Pre-market research staleness cost a trading day this week (07-23)**: this is a new failure mode not seen in prior weekly reflections — the research pipeline itself, not the strategy's entry filters, was the bottleneck on that day.

### Open Action Items (carry forward to next week)
1. **Still highest priority, 3rd week unresolved**: Root-cause and fix the engine/coordinator.py position-logging bug causing live Alpaca fills to go unrecorded in open_positions.md/trade_log.md at entry time (now observed 07-16, 07-17, 07-20, 07-21).
2. *(Unresolved, 2 weeks running)* Formally evaluate whether the "no overnight catalyst = force-close" rule is net-negative in expectancy — now 8 of 10 lifetime trades lost or reduced by this rule for a combined -$372.75, vs. 2 winners for +$73.24 that happened to close positive anyway.
3. **New**: Investigate why pre-market research (research_cache.md/daily_context.md) went stale on 07-22/07-23, causing the market-open routine to skip 07-23 entirely — check whether the 7:33 PM ICT research routine is running reliably every weekday.
4. *(Unresolved, 5 weeks running)* Add VIX at entry to trade log template.
5. *(Unresolved, 5 weeks running)* Add valuation risk modifier: flag reduces research score by 7 points.
6. *(Unresolved)* Log skip decisions in trade_log.md daily — 07-22 through 07-24 (3 of 5 trading days) have no skip-reason entries logged, only reconstructed from portfolio_state.md/open_positions.md notes.

---

## Weekly Reflection — Week of 2026-07-27 (Final, logged 2026-08-01)

### Week Stats
- Trades executed: 2 | Wins: 0 | Losses: 2 | Win rate: 0.0%
- Net P&L: -$701.58 (AMD -$379.26 on 07-27, AMD -$322.32 on 07-29 — same ticker, re-entered and stopped out twice)
- Portfolio: $99,672.34 (07-24 close) -> $98,970.71 (07-31 close), -0.70%
- SPY performance this week: $735.98 (07-24) -> $746.79 (07-31), +1.47%
- Alpha vs SPY: ~-2.17% — the worst weekly alpha since tracking began (2026-06-15 baseline)
- Cumulative alpha since inception: turned negative for the first time this week; prior weeks' thin positive alpha (built mostly on sitting out declining SPY days) was erased by this week's real losses on a rising SPY

### Signals That Worked
- **The 7% high-beta stop-loss rule fired as designed, twice**: unlike every prior loss (which came from the mechanical EOD no-overnight-catalyst rule), both AMD losses this week were genuine stop-loss triggers (07-27: stop at $485.08, filled $479.57; 07-29: exit $449.85 after a queued force-close from 07-28's -8.85% AMD reaction to disappointing 2026 AI-accelerator revenue targets). This is the first week the stop-loss mechanism — not the overnight-catalyst mechanism — was the binding exit rule, confirming it functions correctly under a real adverse move.
- **No hard rules broken**: both AMD positions (9sh and 20sh) stayed within the 5% max position cap, and the daily loss cap never triggered despite the -8.09% and -6.92% single-trade losses (daily portfolio drawdown stayed under -0.4% on the worst day, 07-27).

### Signals That Failed
- **Re-entering the same ticker right after a stop-loss cost a second loss**: AMD was stopped out 07-27, then a new/carried AMD position was force-closed again 07-29 (queued 07-28) for -6.92% on the same disappointing AI-accelerator-revenue catalyst. Re-entering (or holding through) the same name shortly after a stop-loss, without a new confirmed catalyst, effectively doubled down on a thesis that had already been invalidated by price action. No rule currently prevents same-ticker re-entry within days of a stop-loss.
- **High-beta stop-loss (7%) is materially more expensive than the standard 5% stop or the EOD no-catalyst exits**: this week's two losses (-8.09%, -6.92%) are now the two largest single-trade losses in the bot's history, both exceeding the prior record (NVDA -2.58%) by more than 3x. The wider stop for high-beta names is doing its job (letting the position breathe) but is also the most expensive failure mode observed so far.
- **AMD's own negative catalyst (weak 2026 AI-accelerator revenue targets, -8.85% reaction) was known before the 07-29 exit filled** — the 07-28 EOD force-close order was correctly queued, but it sat pending overnight because the market was closed at submission time, meaning the position was exposed to a full extra session (07-28 close to 07-29 open) of AMD-specific downside gap risk on a name that had already broken its thesis.

### VIX Conditions
- VIX conditions were not explicitly logged for either AMD entry in trade_log.md — the VIX-at-entry gap flagged since Week 1 remains unresolved after 7 weeks of tracking, and it is now specifically blocking analysis of whether elevated VIX contributed to this week's losses.
- SPY itself gained +1.47% this week (738.83 -> 746.79), so the losses were stock-specific (AMD earnings-adjacent news), not a broad market/VIX-driven drawdown — the SPY 5-day MA and VIX<28 gates were not the constraint here.

### Emerging Patterns (7 weeks tracked — moderate confidence)
- **First week where stop-losses, not EOD no-catalyst force-closes, drove all realized losses** — a genuinely new failure mode distinct from the pattern documented in every prior reflection (06-22 through 07-20). The bot's other structural issue (mechanical EOD exits costing -$372.75 lifetime through 07-24) did not fire even once this week; instead, a single bad-news ticker (AMD) cost more in one week (-$701.58) than the EOD-exit rule has cost across its entire multi-week history.
- **Single-ticker concentration risk surfaced for the first time**: both trades this week were AMD, and both lost. With only 2 trades in the week, this is a 1-name sample, but it is the first time the weekly reflection has nothing to say about "signal type worked" beyond "the stop-loss rule functioned" — every AMD entry this week lost money.
- **Cumulative alpha turned negative this week** — a milestone worth tracking going forward; 6 of 7 weeks had been flat-to-positive alpha, mostly earned by sitting out declining-SPY days rather than by winning trades outright.

### Open Action Items (carry forward to next week)
1. **New, high priority**: Add a same-ticker cooldown after a stop-loss exit (e.g., no re-entry within N days without a new confirmed catalyst) — AMD's back-to-back losses this week (07-27 stop-loss, 07-29 force-close on the same broken thesis) suggest the bot re-engaged a name whose catalyst had already failed.
2. *(Unresolved from prior weeks)* Root-cause and fix the engine/coordinator.py position-logging bug causing live Alpaca fills to go unrecorded in open_positions.md/trade_log.md at entry time — engine/coordinator.py, engine/risk_manager.py, engine/technical.py, utils/alpaca_client.py all still show uncommitted edits in git status as of this writing.
3. *(Unresolved, 3 weeks running)* Formally evaluate whether the "no overnight catalyst = force-close" rule is net-negative in expectancy — still 8 of 10 pre-this-week trades affected; this week's losses came from a different mechanism (stop-loss) so the underlying question is still open.
4. *(Unresolved, 6 weeks running)* Add VIX at entry to trade log template — now also needed to determine whether VIX context played any role in AMD's move.
5. *(Unresolved, 6 weeks running)* Add valuation risk modifier: flag reduces research score by 7 points.
6. **New**: Investigate whether queued EOD force-close orders that fill at next-day market open (as happened 07-28 -> 07-29 for AMD) should instead be submitted as a market-on-close or pre-market order to avoid overnight gap exposure on names with an already-broken thesis.
