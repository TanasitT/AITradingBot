# Screening rules and output files

These rules are the single source of truth for both routines; the two scripts implement them and the agents must not deviate. Method: Minervini Trend Template + VCP, following Clement Ang's routine and watchlist write-up (https://tradingresourcehub.substack.com/p/how-to-build-and-maintain-watchlists-clement-ang). Thresholds marked "default" are this guide's choices.

## Universe and data
S&P 500 (Wikipedia list) plus `config/extra_tickers.txt`, with SPY and QQQ as benchmarks. Daily adjusted bars from Yahoo Finance via yfinance, 14 months; tickers with under 260 bars are dropped. Data is unofficial and the universe is large-cap heavy, so small caps are missed.

## Measures
| Measure | Rule |
| --- | --- |
| Performance | 1M, 3M, 6M returns over 21, 63, 126 sessions |
| Trend Template (7 checks) | Price above 150 and 200-day SMA; 150 above 200; 200 rising vs 22 sessions ago; 50 above 150 and 200; price above 50; price at least 130% of 52-week low; price within 25% of 52-week high |
| RS Rating (approximation) | 0.4 x 3M + 0.2 x 6M + 0.2 x 9M + 0.2 x 12M return, percentile-ranked inside the universe, scaled 1-99. Pass = 70+. Not the IBD market-wide rating |
| Contraction (VCP proxy) | High-low range (% of low) of three consecutive 10-session windows shrinks oldest to newest |
| Volume dry-up | Avg volume last 10 sessions / last 50 |
| Fundamentals | Execution and Almost Ready only. Latest-quarter revenue and diluted EPS vs prior quarter (QoQ) and year-ago quarter (YoY). meets_30pct_qoq = both QoQ >= 30%. Yahoo GAAP EPS can mislead |

## Tiers
| Tier | Rule | Cap |
| --- | --- | --- |
| Execution | Trend Template pass and RS 70+, within 3% of 20-session high, 10-session range <= 12%, and (contracting or volume ratio <= 0.92) | Top 5 by RS |
| Almost Ready | Trend Template pass and RS 70+, above 20-day EMA, (contracting or tight or dry), within 12% of 52-week high. Execution overflow lands here | 60 |
| Secondary | Any other Trend Template pass | none |
| Wide List (Long) | 6+ of 7 checks and RS 60+, but not a full pass | none |
| Wide List (Short) | Below 150 and 50-day SMA, RS <= 15 | 20 weakest |

## Regime (default)
Defense: SPY below its 50-day SMA. Selective: SPY above it but under 50% of the universe above its own 50-day SMA. Offense: both fine. Max new orders per day: full, half, none.

## Ticket rules (default)
Pivot = highest high of last 10 sessions. Trigger = pivot x (1 + trigger_buffer_pct). Limit = trigger x (1 + limit_buffer_pct). Stop = the higher of (lowest low of last 10 sessions x 0.999) and (trigger x (1 - max_stop_pct)). Shares = floor(min(risk_per_trade_usd / (trigger - stop), max_position_usd / trigger)). Skip on earnings inside the blackout window or when size < 1 share.

## Files
| Path | Content |
| --- | --- |
| results/latest/ and results/<data_date>/ | tiers.json, summary.json, changes.json, screen_results.csv, watchlist.txt (script); report.md (Routine 1) |
| plans/<date>.md and .json | Routine 2 plan and its data |
| config/ | risk.json, extra_tickers.txt, optional positions.csv (ticker,shares,entry,stop) |
| scripts/ | us_momentum_screen.py, preopen_plan.py |

Rule-based screening only, not investment advice. These scripts never place orders: the executor (`engine/momentum.py` in the parent project) turns plan tickets into paper-account orders and manages the stops.
