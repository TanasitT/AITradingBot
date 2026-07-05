Compile the end-of-day summary and send it to jankla2010@gmail.com via Gmail SMTP.

Steps:
1. Read memory/trade_log.md — extract rows where date = today
2. Read memory/portfolio_state.md — get current equity and daily P&L
3. Read memory/open_positions.md — list all open positions with unrealized gain/loss
4. Read memory/benchmark_tracking.md — find today's row for portfolio vs SPY comparison
5. Read memory/weekly_trade_counter.md — get trades_this_week count
6. Read memory/reasoning.md — extract all entries from today (entries starting with today's date)
7. Compose the email:

Subject: Trading Bot — EOD Summary [DATE] | P&L: [daily_pnl]

Body (plain text):
```
EOD SUMMARY — [DATE]
==================================================

PORTFOLIO
  Total equity:     $[X]
  Daily P&L:        $[X] ([pct]%)
  Cash available:   $[X]
  Open positions:   [N]

BENCHMARK
  Portfolio: [pct]% | SPY: [pct]% | Alpha: [pct]%

TRADES THIS WEEK: [N]/3

TODAY'S TRADES
  [BUY/SELL] [TICKER] [N]sh @ $[price] | [thesis excerpt]
  (or: No trades today)

OPEN POSITIONS
  [TICKER] [N]sh | Entry: $[X] | Current: $[X] | [pct]% | Stop: $[X]
  (or: No open positions)

BOT REASONING TODAY
  [HH:MM] — [journal entry excerpt, max 200 chars each]

MARKET CONTEXT (from daily_context.md)
  [SPY trend, VIX, sector, trade environment]
```

8. Send the email using Gmail SMTP (EMAIL_SENDER, EMAIL_PASSWORD from .env)
9. Call /journal with: "EOD report sent to jankla2010@gmail.com."
10. Commit and push memory/ to GitHub with message: `auto: EOD report sent | [date]`

For the weekly version (called on Fridays): include the full trade_log.md, performance_metrics.md,
benchmark_tracking.md for the full week, and learned_patterns.md.
Subject for weekly: Trading Bot — Weekly Summary | [DATE] | Week P&L: [pct]%
