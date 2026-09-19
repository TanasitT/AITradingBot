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

---

## Weekly Reflection — Week of 2026-08-03 (Final, logged 2026-08-08)

### Week Stats
- Trades executed: 0 | Wins: 0 | Losses: 0 | Win rate: N/A
- Net P&L: $0.00 (no trade log entries for any day 08-03 through 08-08)
- Portfolio: $98,970.71 (07-31 close) -> $98,970.71 (08-07 close), 0.00%
- SPY performance this week: $746.79 (07-31) -> $773.16 (08-07), +3.53%
- Alpha vs SPY: ~-3.53% — the worst weekly alpha since tracking began (2026-06-15 baseline), surpassing the prior worst (-2.17%, week of 07-27)
- Cumulative alpha since inception: extended its decline from last week; unlike 07-27's negative alpha (driven by realized AMD losses), this week's alpha loss came entirely from sitting out a strong, uninterrupted SPY rally with zero trades

### Signals That Worked
- **No hard rules broken**: daily loss cap and 3-trades/day limit never triggered because zero trades were placed; the bot did not force a bad entry just to stay active during the rally.
- **Zero realized losses**: for the first time since 07-20, a full week passed with no stop-loss or EOD force-close losses — because no positions were ever opened.

### Signals That Failed
- **Missed a sustained, low-volatility SPY rally**: SPY climbed +3.53% over the week (746.79 -> 773.16) in a steady uptrend with no drawdown days visible in benchmark_tracking.md, yet the bot placed zero trades. This is the clearest case yet of the "under-trading during a calm, rising market" pattern first flagged in the 06-30 and 07-07 reflections — except this time the opportunity cost (-3.53% alpha) is the largest single-week cost the bot has recorded, larger even than the 07-27 AMD stop-loss week (-2.17%).
- **Pre-market research staleness blocked trading again**: the 08-04 market-open routine explicitly skipped trading because research_cache.md/daily_context.md was 4 days stale (per weekly_trade_counter.md's 2026-08-04 EOD entry). This is the same failure mode first identified on 07-23 and flagged as an open action item every week since — it has now caused at least two full missed trading days across two separate weeks (07-23, 08-04) and has not been fixed.
- **No trade_log.md entries at all for 08-03 through 08-08**, including no skip-reason entries — the "log skip decisions daily" action item (open since Week 2, 2026-06-30) remains unresolved after 6+ weeks, making it impossible to tell from the trade log alone whether the other 4 trading days (08-03, 08-05, 08-06, 08-07) had near-miss setups or genuinely no qualifying candidates.

### VIX Conditions
- VIX was not logged for this week in any memory file — the VIX-at-entry/VIX-at-decision gap flagged since Week 1 remains unresolved after 8 weeks of tracking, and now also blocks any explanation of why zero candidates qualified during a week when SPY rose steadily (a backdrop that historically correlates with low, calm VIX).
- SPY's steady +3.53% climb with no logged pullback days is consistent with a low-VIX, low-fear environment — suggesting the VIX<28 gate was not the constraint; the volume/score/staleness gates were.

### Emerging Patterns (8 weeks tracked — moderate-to-high confidence on recurring issues)
- **Pre-market research staleness is now a confirmed 2-week-recurring bug (07-23, 08-04), not a one-off**: both times it blocked the market-open routine on the day it happened. This should be escalated from "investigate" to "fix" — the standing action item from 07-20's reflection has now cost a second missed trading day.
- **The bot's largest weekly alpha losses are now split evenly between two distinct causes**: realized stock-specific losses (07-27 week, AMD, -2.17% alpha) and pure opportunity cost from under-trading a rally (08-03 week, -3.53% alpha). Both are real costs; the under-trading cost is now demonstrably larger, which argues against loosening risk rules further and instead argues for fixing the research-freshness pipeline so more candidate-days are actually evaluated.
- **Skip-reason logging remains the single most-repeated unresolved action item** (raised in Week 2, 3, 4, 5, 6, 7, and now Week 8) — its absence directly limited this week's reflection depth, since it's unknown whether 08-03, 08-05, 08-06, or 08-07 had any near-miss candidates.

### Open Action Items (carry forward to next week)
1. **Escalated, 2nd occurrence**: Fix the pre-market research pipeline so daily_context.md/research_cache.md does not go stale (now confirmed to have blocked trading on both 07-23 and 08-04) — this is no longer a hypothesis, it's a repeat failure with a direct, attributable cost.
2. *(Unresolved, 4th week running)* Root-cause and fix the engine/coordinator.py position-logging bug causing live Alpaca fills to go unrecorded in open_positions.md/trade_log.md at entry time — not observed this week only because no trades occurred, not because it was fixed.
3. *(Unresolved, 7 weeks running — now the most-repeated open item)* Log skip decisions in trade_log.md daily, including reason and top candidate scores/volume — 08-03 through 08-08 has zero entries of any kind.
4. *(Unresolved, 8 weeks running)* Add VIX at entry/decision time to trade log and daily_context.md.
5. *(Unresolved, 7 weeks running)* Add valuation risk modifier: flag reduces research score by 7 points.
6. *(Unresolved from 07-27)* Formally evaluate whether the "no overnight catalyst = force-close" rule is net-negative in expectancy — still open, no new data this week since zero trades occurred.
7. *(Unresolved from 07-27)* Add a same-ticker cooldown after a stop-loss exit — still open, not tested this week.

---

## Weekly Reflection — Week of 2026-08-10 (Final, logged 2026-08-15)

### Week Stats
- Trades executed: 1 | Wins: 1 | Losses: 0 | Win rate: 100.0%
- Net P&L: +$126.44 (NVDA, 44sh combined, entered 08-12 avg $224.10, closed 08-14 avg $226.97, +1.28%)
- Portfolio: $98,970.71 (08-07 close) -> $99,097.14 (08-14 close), +0.13%
- SPY performance this week: $773.16 (08-07) -> $776.30 (08-14), +0.41%
- Alpha vs SPY: ~-0.28% (a genuine realized win still lost to a calm, steadily rising SPY)
- Cumulative alpha since inception: continues to be dragged mainly by under-trading calm rally weeks (08-03, and now 08-10) rather than by realized losses

### Signals That Worked
- **First 100%-win-rate week since tracking began**: the bot's only trade this week (NVDA) closed positive. NVDA's thesis — Jensen Huang's "$500B AI infrastructure financing" framing plus the PLTR-NVDA classified-AI partnership — held up over the 2-day hold (08-12 to 08-14), unlike most prior wins which were single-day EOD force-closes.
- **No hard rules broken**: the 44sh NVDA position stayed within the 5% position cap, daily loss cap never neared -2% at any point in the week, and the 3-trades/day and 3-trades/week limits were respected (only 1 fill this week, NVDA; MSFT never filled).
- **VIX stayed at 2026 lows all week (14.40-15.45)**, confirming VIX was never the binding constraint on any decision this week — consistent with prior weeks' findings that the bottleneck is candidate availability/logging, not risk-off caution.

### Signals That Failed
- **NVDA's exit reason is unknown — a new failure mode**: the position was found already closed at the 08-14 09:33 ET monitor check. Neither the 5% stop-loss ($212.90) nor take-profit tier 1 (+8%, $242.03) had been breached at the exit price ($226.97 avg, roughly +1.28%/+42% of the way to TP1) — meaning no coded rule in engine/monitor.py or engine/coordinator.py should have triggered this sell, yet it filled. This is the first "unrule-triggered exit" recorded in the trade log's history (prior exits were always EOD no-catalyst force-closes or stop-loss/TP hits). It happened to be profitable this time, but an unexplained close mechanism is a correctness risk regardless of outcome — the bot cannot currently distinguish a lucky unexplained exit from a buggy one.
- **MSFT order never filled**: a 10sh limit order at $492.45 (submitted alongside NVDA on 08-12) expired unfilled on 08-13 without ever generating a position. This is not itself a bug (limit orders can legitimately go unfilled), but it means one of the week's two trade-trigger candidates produced zero data — a reminder that "order submitted" and "trade executed" are different events and only the latter should count toward weekly stats (this was handled correctly this week, per weekly_trade_counter.md).
- **Position-logging drift recurred one more time**: the 44sh NVDA position was the combination of two separate 22sh buy orders (20:43 ET and 20:59 ET on 08-12) that were not confirmed as filled/combined until an 11:34 ET intraday check on 08-13 — a full session-plus later. This is the same chronic engine/coordinator.py write-path gap flagged in nearly every reflection since 07-13, still unresolved after 5 weeks.

### VIX Conditions
- VIX ranged 14.40 (08-12 intraday low, the 2026 low to date) to 15.45 (08-11), closing the week at 14.52 (08-14) — the calmest, lowest-fear week recorded since tracking began.
- SPY's RSI spiked to an overbought 85.568 on 08-12 (post-CPI, pre-earnings AI rally) before normalizing to 66.175 by 08-14 — a healthy technical reset that coincided with NVDA's position being held through rather than force-closed, unlike the pattern in every prior "no overnight catalyst" week.

### Emerging Patterns (9 weeks tracked — moderate-to-high confidence on recurring issues)
- **All-time win rate crossed 30% for the first time (4/13, up from 3/12)**, and profit factor nearly tripled (0.066 -> 0.181) on the back of a single $126.44 win — still deeply unprofitable in aggregate (gross loss $1,104.79 vs gross win $199.68), but the trend this week is the best single-trade outcome recorded to date, both in absolute P&L and as the new largest single gain (surpassing META's +$38.26 from 07-20).
- **Unexplained/unrule-triggered exits are now a confirmed new risk category**, distinct from the two previously identified failure modes (EOD no-catalyst force-close, stop-loss trigger). Because this one happened to be profitable, it is easy to under-weight — but the same unexplained-close mechanism could just as easily fire during an unrealized loss and lock it in early, or fire during a winning run and cap upside before take-profit. This needs the same root-cause attention as the position-logging drift bug, since both point to gaps between what engine/coordinator.py and engine/monitor.py are supposed to do and what is actually executing against the live Alpaca account.
- **Opportunity-cost alpha drag continues to dominate realized-loss alpha drag**: two of the last three active weeks (08-03 flat, 08-10 with a real win) both posted negative alpha purely because SPY outran the bot's activity level or trade sizing, not because of stock-specific losses (07-27's AMD week remains the only loss-driven negative-alpha week). This reinforces the standing argument for prioritizing the research-freshness and position-logging fixes over further tightening risk rules.

### Open Action Items (carry forward to next week)
1. **New, high priority**: Investigate what closed the NVDA position on 08-14 before the 09:33 ET monitor check ran — neither monitor.py's stop-loss/TP logic nor coordinator.py's EOD force-close should have fired given the price and timing; determine if this was a manual/external action, a scheduling overlap between two routine instances, or a genuine logic bug that happens to fail safe.
2. *(Unresolved, 5th week running)* Root-cause and fix the engine/coordinator.py position-logging bug causing live Alpaca fills (both entries and, now, exits) to lag or go unrecorded in open_positions.md/trade_log.md at the time they actually happen — this week's NVDA combine took over 15 hours to confirm.
3. *(Unresolved, 8 weeks running)* Add VIX at entry/decision time directly to trade_log.md rows (daily_context.md now tracks it reliably, but trade_log.md entries still don't carry it forward).
4. *(Unresolved, 8 weeks running)* Add valuation risk modifier: flag reduces research score by 7 points.
5. *(Unresolved from 07-27)* Formally evaluate whether the "no overnight catalyst = force-close" rule is net-negative in expectancy — still open; this week's NVDA hold-through-to-a-win is a data point against always force-closing on distant earnings dates.
6. *(Unresolved from 07-27)* Add a same-ticker cooldown after a stop-loss exit — still open, not tested this week (no stop-loss triggered).

---

## Weekly Reflection — Week of 2026-08-17 (Final, logged 2026-08-23)

### Week Stats
- Trades executed: 0 | Wins: 0 | Losses: 0 | Win rate: N/A
- Net P&L: $0.00 (no trade_log.md entries for any day 08-17 through 08-21)
- Portfolio: $99,097.14 (08-14 close) -> $99,096.91 (08-21 close), essentially flat (-0.0002%)
- SPY performance this week: $776.30 (08-14) -> $765.64 (08-21), -1.37%
- Alpha vs SPY: ~+1.37% — best weekly alpha since 07-23's +1.01%, entirely from sitting out a declining SPY rather than from any realized gain
- Cumulative alpha since inception: modestly improved after two straight negative-alpha weeks (08-03 at -3.53%, 08-10 at -0.28%); this week's inaction happened to land on the right side of a down market

### Signals That Worked
- **No hard rules broken**: daily loss cap and 3-trades/day limit never triggered because zero trades were placed; weekly_trade_counter.md confirms trades_this_week stayed 0/3 across every EOD reset this week (08-20, 08-23).
- **Zero-trade week coincided with a declining SPY (-1.37%)**: this is the mirror image of 08-03 (zero trades during a +3.53% SPY rally, worst alpha to date) — the same "no signal" outcome produced a good result this time purely because the market moved against a hypothetical long position instead of with it. Reinforces that the bot's alpha in no-trade weeks is essentially a coin flip tied to SPY's direction, not a skill signal.

### Signals That Failed
- **A full second consecutive week with zero trades and no skip-reason logging**: trade_log.md has no entries — active or skipped — for 08-17 through 08-21. This is the same "log skip decisions daily" gap that has been the single most-repeated open action item since Week 2 (2026-06-30), now unresolved for 12+ weeks running. It remains impossible to tell from the trade log alone whether any candidate came close to qualifying this week or whether research/candidates were simply absent.
- **No new data on the standing open bugs**: the engine/coordinator.py position-logging drift and the 08-14 unrule-triggered-exit mystery were not tested this week (no positions were ever opened), so both remain open with no additional evidence either way.
- **research_cache.md/daily_context.md staleness risk not explicitly ruled out**: given two prior weeks (07-23, 08-04) were confirmed blocked by stale research, and this week again produced zero trades with no skip log, stale research remains a plausible (unconfirmed) explanation alongside "no qualifying candidates."

### VIX Conditions
- VIX levels were not explicitly logged this week in any memory file — the VIX-at-decision gap flagged since Week 1 remains unresolved after 10 weeks of tracking.
- SPY's steady -1.37% decline without a daily_loss_halt or VIX>28 gate ever firing (portfolio never held a position to be affected) suggests a moderate pullback rather than a volatility spike, consistent with prior no-panic pullback weeks (e.g. 07-20).

### Emerging Patterns (10 weeks tracked — moderate-to-high confidence on recurring issues)
- **No-trade weeks are now a near-coin-flip on alpha, split by SPY's direction that week**: 08-03 (SPY +3.53%, alpha -3.53%) and now 08-17 (SPY -1.37%, alpha +1.37%) are both zero-trade weeks with alpha almost exactly mirroring negative SPY movement. This makes "inaction" a poor strategy to rely on for consistent alpha — it only works when the bot happens to sit out down weeks, which it cannot control or predict without actually evaluating candidates.
- **Skip-reason logging is now the most overdue open item in the project's history** (raised Weeks 2 through 9, now also Week 10) — 12+ weeks unresolved. This has graduated from an analysis inconvenience to the single clearest, cheapest fix available (a code/prompt change to engine/coordinator.py or the market-open routine) that would meaningfully improve every future reflection's quality.
- **The bot has now had 4 of the last 5 tracked weeks (08-03, 08-10, 08-17, and effectively 07-31) with 0-1 trades** — trading frequency remains far below the 3/day (15/week) budget, and the cause (candidate scarcity vs. a pipeline/staleness bug vs. an overly strict filter) is still not diagnosable from available logs.

### Open Action Items (carry forward to next week)
1. **Most overdue, 12+ weeks running**: Log skip decisions in trade_log.md daily, including reason and top candidate scores/volume — this week (08-17 to 08-21) again has zero entries of any kind, active or skipped.
2. *(Unresolved, 6th week running)* Root-cause and fix the engine/coordinator.py position-logging bug — not observed this week only because no trades occurred, not because it was fixed.
3. *(Unresolved)* Investigate what closed the NVDA position on 08-14 before the monitor check ran — still no new evidence, no positions opened since.
4. *(Unresolved, 9 weeks running)* Add VIX at entry/decision time directly to trade_log.md and daily_context.md.
5. *(Unresolved, 9 weeks running)* Add valuation risk modifier: flag reduces research score by 7 points.
6. *(Unresolved from 07-27)* Formally evaluate whether the "no overnight catalyst = force-close" rule is net-negative in expectancy — still open, no new data (zero trades this week).
7. *(Unresolved from 07-27)* Add a same-ticker cooldown after a stop-loss exit — still open, not tested this week.
8. **New**: Confirm whether pre-market research (research_cache.md/daily_context.md) actually ran and stayed fresh every weekday this week (08-17 to 08-21) — given the confirmed staleness bugs on 07-23 and 08-04, a silent third occurrence during a zero-trade week cannot currently be ruled out from the available logs.

---

## Weekly Reflection — Week of 2026-08-24 (Final, logged 2026-09-01)

### Week Stats
- Trades executed: 0 | Wins: 0 | Losses: 0 | Win rate: N/A
- Net P&L: $0.00 (no trade_log.md entries for any day 08-24 through 08-28)
- Portfolio: $99,096.91 (08-21 close) -> $99,096.91 (08-28 close), 0.00% (flat, 0 positions held all week)
- SPY performance this week: $765.64 (08-21) -> $769.28 (08-28), +0.48%
- Alpha vs SPY: ~-0.48% — a flat, no-trade week that landed on the wrong side of a mildly rising market
- Cumulative alpha since inception: gave back most of last week's +1.37% inaction gain; the no-trade alpha coin-flip landed tails this time

### Signals That Worked
- **No hard rules broken**: daily loss cap and 3-trades/day limit never triggered (zero trades); weekly_trade_counter.md confirms trades_this_week stayed 0/3 across the 08-26 EOD resets.
- **Zero realized losses**: no stop-loss or EOD force-close losses, because no position was ever opened.
- **VIX was a non-factor** (~14-16 all week) — consistent with every prior reflection: risk-off caution is not what is keeping the bot out of the market.

### Signals That Failed
- **Fifth zero-or-one-trade week out of the last six** (08-03: 0, 08-10: 1, 08-17: 0, 08-24: 0). The bot used 0 of its 15-trade weekly budget again during a calm, slightly-up tape — the same structural under-trading flagged since the 06-30 reflection, now with a -0.48% alpha cost this week.
- **Skip-reason logging still absent** — trade_log.md has no entries, active or skipped, for 08-24 to 08-28. This is the single most-repeated open action item in the project (raised every week since 2026-06-30, now ~14 weeks) and again made it impossible to tell whether any candidate came close to the volume/score gate this week or whether research was simply thin.
- **Then the opposite failure the following Monday+1**: after weeks of nothing, the 2026-09-01 market-open routine fired 3 entries in one morning — NVDA 22sh @ $217.99 (score 82), AMZN 19sh @ $254.24 (score 80), AMD 10sh @ $454.50 (score 80) — exhausting the 3/3 weekly limit before noon, directly into a risk-off session (S&P -0.53%, Iran/Hormuz headline shock, Brent ~$92, yields at highs). Feast-or-famine cadence: the bot goes from zero conviction for a month to three simultaneous high-beta AI/semi entries on a single down day.
- **NVDA protective stop-limit failed to place (403 Forbidden)** on 2026-09-01 — a new failure mode. NVDA 22sh has sat unprotected at the broker across every intraday monitor since (AMZN and AMD both got working stop_limits; only NVDA's failed). No routine has retried the placement.
- **Position-logging drift recurred** — open_positions.md still read "confirmed flat" at the first 2026-09-01 intraday check while 3 positions were live on Alpaca; same chronic engine/coordinator.py write-path gap flagged since 07-13, still unresolved, engine/*.py still show uncommitted edits in git status.
- **EOD 2026-09-01 force-close not executed**: all 3 positions were flagged for force-close (no strong overnight catalyst found, risk-off tape) but the automated EOD run is not permitted to place orders — the closes and /journal entries are pending manual action, and the EOD email was not sent.

### VIX Conditions
- VIX ranged ~14-16 through 08-24/08-28, then ~15.88 on 2026-09-01 (+6.4% on the Iran headline) — still comfortably under the 28 gate. VIX has not been the binding constraint on a single decision in 11 weeks of tracking.
- The 2026-09-01 entries were placed with SPY sitting right at / marginally below its 5-day MA and VIX ticking up — a weaker technical backdrop than the strategy's "SPY above 5-day MA" entry rule nominally wants; worth checking whether the market-open routine evaluated the MA on an intraday quote rather than the prior close.

### Emerging Patterns (11 weeks tracked — moderate-to-high confidence on recurring issues)
- **The bot's trading cadence is bimodal, not steady**: long stretches of zero trades punctuated by same-day bursts that hit the weekly cap at once (07-16: 3, 07-20: 3, now 09-01: 3). This concentrates entry timing risk — every burst so far has gone in near a local high or into a down day, and three of them exhausted the weekly budget in one session, leaving no capacity to act on a better setup later that week.
- **Skip-reason logging (14 weeks unresolved) is now the clearest blocker to improving this reflection** — without it, "under-trading" cannot be attributed to candidate scarcity vs. an over-strict volume gate vs. a research-freshness bug. This should be the next fix.
- **Broker-order placement is now a two-instance problem**: EOD force-close orders can't be placed by the automated run (permission), and now protective stop-limits are failing at entry (403). The bot is increasingly opening positions it cannot protect or close on schedule — a correctness risk that compounds with the position-logging drift.
- **No-trade weeks remain an alpha coin-flip**: 08-17 (+1.37%, SPY down) and 08-24 (-0.48%, SPY up) bracket the pattern — inaction is not a strategy, it only looks like alpha when SPY happens to fall.

### Open Action Items (carry forward to next week)
1. **Immediate**: Place a protective stop for NVDA 22sh (retry the stop-limit that 403'd on 2026-09-01) and decide on the 3 open positions (NVDA/AMZN/AMD) flagged for force-close at EOD 09-01 but not executed — all three are unprotected/overdue per the EOD overnight-thesis rule.
2. **Most overdue, ~14 weeks running**: Log skip decisions in trade_log.md daily, including reason and top candidate scores/volume — 08-24 to 08-28 again has zero entries of any kind.
3. *(Unresolved, 7th week running)* Root-cause and fix the engine/coordinator.py position-logging bug — recurred again 2026-09-01 (open_positions.md read "flat" with 3 live positions).
4. **New**: Investigate why the NVDA stop-limit hit 403 Forbidden at market-open on 2026-09-01 while AMZN/AMD stop-limits placed fine — same account, same routine, same order type.
5. **New**: Review why 3 entries fired simultaneously on 2026-09-01 into a risk-off session with SPY at/below its 5-day MA — check the MA evaluation source (intraday quote vs prior close) and whether staggering entries would reduce burst-timing risk.
6. *(Unresolved, 10 weeks running)* Add VIX at entry/decision time directly to trade_log.md rows.
7. *(Unresolved, 9 weeks running)* Add valuation risk modifier: flag reduces research score by 7 points.
8. *(Unresolved from 07-27)* Formally evaluate whether the "no overnight catalyst = force-close" rule is net-negative in expectancy — about to get fresh data from the 3 open 09-01 positions once they are closed.
9. *(Unresolved from 07-27)* Add a same-ticker cooldown after a stop-loss exit — still open, not tested.

---

## Weekly Reflection — Week of 2026-08-31 (Final, logged 2026-09-06)

### Week Stats
- Trades executed: 3 (all entries, all 2026-09-01) | Closed: 0 | Wins: 0 | Losses: 0 | Win rate: N/A
- Net realized P&L: $0.00 — nothing was closed; all 3 positions (NVDA 22sh @ $217.99, AMZN 19sh @ $254.24, AMD 10sh @ $454.50) remain open
- Unrealized P&L at 2026-09-04 close: NVDA +$272.96 (+5.69%), AMZN +$81.32 (+1.68%), AMD +$232.60 (+5.12%) = +$586.88 combined, all three green
- Portfolio: $99,096.91 (08-28 close) -> $99,683.78 (09-04 close), +0.59% (100% mark-to-market, 0% realized)
- SPY this week: $769.28 (08-28) -> $770.18 (09-04), +0.12%
- Alpha vs SPY: ~+0.47% — earned entirely by holding three rising positions the rules said to close
- Cumulative alpha since inception: nudged positive this week, but on unrealized marks that reverse instantly if the positions gap down before they are closed

### Signals That Worked
- **The 2026-09-01 entry scores held up over 3 sessions**: NVDA (82), AMZN (80), AMD (80) all moved higher into the 09-04 close. Unlike the 07-16/07-20 bursts that were force-closed same-day at small losses, these were never closed — and the AI/semi thesis (NVDA data-center demand, AMD MI450/Helios H2 ramp, AMZN AI-capex) firmed up rather than breaking. First time a same-day multi-entry burst is sitting on a material gain.
- **No hard rules broken on the entry side**: all 3 positions sized within the 5% cap (NVDA ~$4.8k, AMZN ~$4.8k, AMD ~$4.5k on a ~$99k book), 3/3 weekly limit respected, daily loss cap never neared -2% on any day (worst daily print was +0.008%).
- **VIX was a non-factor again** (~15-16 all week, briefly ~15.9 on the 09-01 Iran/Hormuz headline) — 12 weeks running, VIX < 28 has never been the binding constraint on a single decision.
- **AMZN and AMD protective stop-limits placed and held all week** (AMZN stop $241.53/limit $240.32; AMD stop $431.77/limit $429.61) — the stop mechanism works when the order is accepted.

### Signals That Failed
- **The EOD no-overnight-catalyst force-close rule was flagged three times (09-01, 09-02, 09-04) and executed zero times**: every EOD run correctly researched the overnight thesis, correctly concluded all 3 should be closed, and then could not act because the automated run is not permitted to place orders. The positions rode through the entire week unmanaged by rule. This week that *helped* (+$586.88 unrealized), but the bot got the good outcome by failing to follow its own process, not by design — the same gap would have locked in a loss just as easily if the week had gone the other way.
- **NVDA 22sh had no broker-side protective stop for the entire week**: the stop-limit 403'd at placement on 09-01 and no routine ever retried it. NVDA is the largest and highest-beta of the three positions and ran from $217.99 to $230.36 completely unprotected. AMZN and AMD (same account, same routine, same order type, same session) placed fine — so this is an order-specific or symbol-specific rejection, not an account-wide permissions problem.
- **Position-logging drift recurred**: open_positions.md still read "confirmed flat" at the first 09-01 intraday check while 3 positions were live on Alpaca; the file was only reconciled to live state at the 10:32 ET monitor run. Same chronic engine/coordinator.py write-path gap flagged in nearly every reflection since 07-13; engine/*.py still show uncommitted edits in git status.
- **Feast-or-famine cadence, third instance**: after 4 consecutive near-zero-trade weeks (08-03: 0, 08-10: 1, 08-17: 0, 08-24: 0), the bot fired all 3 allowed trades in a single morning (09-01) directly into a risk-off session (SPY -0.34% that day, Iran/Hormuz headline, Brent ~$92). Same pattern as 07-16 (3 in a day) and 07-20 (3 in a day). Every burst so far has exhausted the weekly budget at once and gone in near a local low or into a down day — this time the down-day entry timing actually worked in the bot's favor as the market recovered 09-02 to 09-04.
- **Skip-reason logging still absent** for 09-03/09-04 (no entries evaluated those days because the 3/3 cap was already hit) — ~15 weeks unresolved, though less impactful this week since the cap, not candidate scarcity, was the blocker.

### VIX Conditions
- VIX ~15-16 through the week, one ~15.9 tick on the 09-01 geopolitical headline, back to ~15 by 09-04. Never near the 28 gate.
- The 09-01 entries were placed with SPY sitting right at / marginally below its 5-day MA (09-01 close $760.86 vs 5-day MA $766.83 — SPY *below* MA, which nominally blocks regular-stock entries). SPY did not reclaim its 5-day MA until the 09-03 close ($773.12). Worth re-checking whether the 09-01 market-open routine evaluated the MA on an intraday quote rather than the prior close — if SPY was below its 5-day MA at the open, all 3 regular-stock entries were placed against the strategy's own SPY-health gate.

### Emerging Patterns (12 weeks tracked)
- **The bot is now structurally unable to close positions on schedule**: EOD force-closes have been flagged-but-not-executed on 09-01, 09-02, 09-04 (and were also the pending item from the 08-31 reflection). Combined with the NVDA stop-limit 403, the bot spent the whole week holding three positions it could neither protect nor exit by rule. This is the single most important finding this week — it is a correctness failure that happened to pay off, which is the most dangerous kind because it discourages fixing it.
- **First "rule said sell, holding won" data point for the no-overnight-catalyst debate**: 8 of the bot's first 10 lifetime trades lost to same-day/next-day force-closes for a combined -$372.75. This week, three positions the rule wanted closed on 09-01 are +$586.88 three sessions later. One week is not an expectancy study, but it is the first concrete case *against* mechanical same-day exits on distant-earnings names — consistent with the 08-14 NVDA hold-to-a-win. The pattern forming: force-closing intraday momentum names the same day compresses winners to zero while leaving the small losers; letting a few ride has now helped twice (08-14, this week).
- **Entry timing on bursts is not as bad as first feared**: the 06-22 through 07-20 read was "every burst goes in near a local high." The 09-01 burst went in near a *local low* (SPY had just dropped on the Iran headline) and all 3 positions are up 1.7-5.7%. Small sample, but the "bursts always mistime the top" hypothesis is weaker now.
- **VIX gate remains dead weight** — 12 weeks, zero binding decisions. Not a criticism (it's cheap insurance), just a confirmed non-factor in the current low-vol regime.

### Open Action Items (carry forward to next week)
1. **Immediate / carried from 08-31**: The 3 open positions (NVDA/AMZN/AMD) are still open, still flagged for force-close every EOD since 09-01, and NVDA is still unprotected. A permitted process (user or authorized routine) needs to either (a) place the NVDA stop and formally decide to hold all 3 with a documented thesis, or (b) execute the three force-closes. They cannot keep riding in limbo.
2. **New, high priority**: Fix the automated-run gap where EOD/monitor routines can research and decide an exit but cannot execute it. Either grant the EOD routine scoped sell-to-close permission on the paper account, or route flagged closes to a process that can act, or explicitly change the strategy to "flag only, human executes" and stop calling them force-*closes*.
3. **New**: Root-cause the NVDA stop-limit 403 Forbidden (09-01) — it is order/symbol-specific, not account-wide (AMZN/AMD placed same session). Add an automatic retry on stop-order placement failure so a position is never left unprotected silently.
4. *(Unresolved, 8th week running)* Root-cause and fix the engine/coordinator.py position-logging bug — recurred again 09-01 (open_positions.md read "flat" with 3 live positions).
5. **New**: Verify the 09-01 market-open routine's SPY 5-day MA check — SPY closed *below* its 5-day MA on 09-01, which should have blocked all 3 regular-stock entries. Determine whether it evaluated an intraday quote vs the prior close.
6. *(Unresolved from 07-27, now with supporting data)* Formally evaluate the "no overnight catalyst = force-close" rule's expectancy — this week and 08-14 both favor holding; the 07-16/07-20 weeks favor closing. Needs a real backtest, not another week of anecdote.
7. *(Unresolved, 11 weeks)* Add VIX at entry/decision time directly to trade_log.md rows.
8. *(Unresolved, 10 weeks)* Add valuation risk modifier: flag reduces research score by 7 points — especially relevant with AMD +142% YTD and NVDA/AMZN both extended at entry.
9. *(Unresolved from 07-27)* Add a same-ticker cooldown after a stop-loss exit — still open, not tested.
