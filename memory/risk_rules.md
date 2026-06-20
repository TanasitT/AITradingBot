# Risk Rules (editable numerical parameters)
# NOTE: Hard rules (5% max position, -2% daily halt, 3 trades/week, no options)
# live in strategy.md and cannot be overridden here. This file tunes everything else.

- Stop-loss default: 5% below entry
- Stop-loss high-beta (beta > 1.5): 7% below entry
- Max concurrent open positions: 5
- Min research score to enter trade: 70
- Min volume multiplier vs 30d avg: 2x
- SPY must be above N-day MA: 5
- Max VIX to place new trades: 28
- Take-profit tier 1: +8% (sell 33%)
- Take-profit tier 2: +15% (sell 33%)
- Take-profit tier 3: +25% (sell 34%)
- Trailing stop after tier 1: 3% from intraday high
