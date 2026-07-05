Append today's portfolio vs SPY snapshot to memory/benchmark_tracking.md.

Steps:
1. Call Alpaca API: GET /v2/account — extract equity (current portfolio value)
2. Get SPY closing price for today via Alpaca market data API: GET /v2/stocks/SPY/bars/latest
   - If market is still open, use the latest bar close as an intraday estimate
3. Read memory/benchmark_tracking.md — find the most recent portfolio value row to calculate % change
4. Calculate:
   - portfolio_chg_pct = (today_equity - prev_equity) / prev_equity
   - spy_chg_pct = (today_spy - prev_spy) / prev_spy (use yesterday's close from bars)
   - alpha = portfolio_chg_pct - spy_chg_pct
5. Append one row to memory/benchmark_tracking.md in this exact format:
   `| [DATE] | $[equity] | [portfolio_chg]% | $[spy_close] | [spy_chg]% | [alpha]% |`
   NEVER overwrite existing rows — always append only.
6. Call /journal with: "Benchmark logged. Portfolio: $[X] ([pct]%) | SPY: $[X] ([pct]%) | Alpha: [pct]%"
7. Commit and push memory/benchmark_tracking.md to GitHub with message: `auto: benchmark | [date] | alpha [pct]%`

The alpha column shows whether the bot is beating the market. A positive alpha means the bot
outperformed SPY that day. Track this weekly to determine if the strategy adds value over
simply holding an index fund.
