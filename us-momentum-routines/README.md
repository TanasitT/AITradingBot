# us-momentum-routines

The research half of the system: a weekly US momentum screen and a weekday pre-open order plan.
These scripts analyse data and write files only. The executor in the parent project
(`engine/momentum.py`) places orders from the plan and manages the stops.

| Script | Output |
|---|---|
| `scripts/us_momentum_screen.py` | `results/latest/` (and a dated copy): five-tier watchlist, summary, changes, CSV, TradingView import list |
| `scripts/preopen_plan.py [--date YYYY-MM-DD]` | `plans/<date>.json` and `.md`: market regime and order tickets for the day |

Rules: [docs/SPEC.md](docs/SPEC.md). Sizing inputs: `config/risk.json`. Extra tickers outside the
S&P 500: `config/extra_tickers.txt`. Results and plans are generated locally and not committed.

Run from this folder:

```
python scripts/us_momentum_screen.py
python scripts/preopen_plan.py
```
