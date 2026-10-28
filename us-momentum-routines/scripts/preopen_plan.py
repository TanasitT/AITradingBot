#!/usr/bin/env python3
"""Pre-open order PLAN for the Execution list. Analysis only - this script never places orders.

Reads  results/latest/{tiers,summary}.json and config/risk.json (and optional config/positions.csv).
Writes plans/<ET date>.md and plans/<ET date>.json
Run from the repo root:  python scripts/preopen_plan.py [--date YYYY-MM-DD]
"""
import argparse, json, math, sys, warnings
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo
import pandas as pd, yfinance as yf
sys.path.insert(0, str(Path(__file__).parent))
from us_momentum_screen import metrics, TT_COLS, CFG  # noqa: E402
warnings.filterwarnings("ignore")

# NYSE full-day closures 2026 (verify against the official NYSE calendar)
NYSE_HOLIDAYS = {"2026-01-01", "2026-01-19", "2026-02-16", "2026-04-03", "2026-05-25",
                 "2026-06-19", "2026-07-03", "2026-09-07", "2026-11-26", "2026-12-25"}


def earnings_flag(t, today, days):
    try:
        cal = yf.Ticker(t).calendar
        eds = cal.get("Earnings Date") if isinstance(cal, dict) else None
        for d in (eds or []):
            dd = d if isinstance(d, date) else pd.Timestamp(d).date()
            if 0 <= (dd - today).days <= days + 2:
                return f"EARNINGS {dd}"
        return "none found"
    except Exception:
        return "unknown"


def write(outdir, day, md, js):
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / f"{day}.md").write_text(md)
    (outdir / f"{day}.json").write_text(json.dumps(js, indent=1))
    print(md)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tiers", default="results/latest/tiers.json")
    ap.add_argument("--summary", default="results/latest/summary.json")
    ap.add_argument("--risk", default="config/risk.json")
    ap.add_argument("--positions", default="config/positions.csv")
    ap.add_argument("--outdir", default="plans")
    ap.add_argument("--date", default=None, help="override US/Eastern date (testing)")
    a = ap.parse_args()

    today = date.fromisoformat(a.date) if a.date else datetime.now(ZoneInfo("America/New_York")).date()
    day = str(today)
    out = Path(a.outdir)
    if today.weekday() >= 5 or day in NYSE_HOLIDAYS:
        write(out, day, f"# Pre-open plan {day}\n\n**No session today (weekend or NYSE holiday). No orders to prepare.**\n",
              {"date": day, "status": "market_closed", "tickets": []})
        return

    risk = json.loads(Path(a.risk).read_text())
    tiers = json.loads(Path(a.tiers).read_text())
    summ = json.loads(Path(a.summary).read_text())
    cands = {e["ticker"]: e for k in ("execution", "almost_ready") for e in tiers[k]}
    pp = Path(a.positions)
    pos_df = pd.read_csv(pp) if pp.exists() else None
    names = sorted(set(cands) | {"SPY"} | (set(pos_df["ticker"]) if pos_df is not None else set()))
    px = yf.download(names, period="14mo", interval="1d", auto_adjust=True, progress=False,
                     threads=True, group_by="column")
    close, high, low, vol = px["Close"], px["High"], px["Low"], px["Volume"]
    last_bar = str(close.index[-1].date())

    def series(t):
        c = close[t].dropna()
        return c, high[t].reindex(c.index), low[t].reindex(c.index), vol[t].reindex(c.index)

    spy = metrics(*series("SPY"))
    if not spy["p_gt_50"]:
        regime, max_orders = "Defense", 0
    elif summ["breadth_above_50sma"] < 0.5:
        regime, max_orders = "Selective", max(1, risk["max_new_orders"] // 2)
    else:
        regime, max_orders = "Offense", risk["max_new_orders"]

    rows, skipped = [], []
    for t, e in cands.items():
        try:
            c, h, l, v = series(t)
            m = metrics(c, h, l, v)
        except Exception as ex:
            skipped.append((t, f"data error: {str(ex)[:40]}"))
            continue
        tt7 = all(m[k] for k in TT_COLS)
        ready = (tt7 and e["rs_rating"] >= CFG["rs_min"] and m["dist_20d_high"] >= -CFG["near_high_exec"]
                 and m["rng_w1"] <= CFG["tight_10d"] and (m["contracting"] or m["vol_dryup"] <= CFG["vol_dry"]))
        pivot = float(h.iloc[-10:].max())
        trigger = pivot * (1 + risk["trigger_buffer_pct"])
        limit = trigger * (1 + risk["limit_buffer_pct"])
        stop = max(float(l.iloc[-10:].min()) * 0.999, trigger * (1 - risk["max_stop_pct"]))
        rps = trigger - stop
        shares = math.floor(min(risk["risk_per_trade_usd"] / rps, risk["max_position_usd"] / trigger)) if rps > 0 else 0
        row = dict(ticker=t, from_tier="execution" if t in {x["ticker"] for x in tiers["execution"]} else "almost_ready",
                   rs=e["rs_rating"], close=round(m["price"], 2), pivot=round(pivot, 2), trigger=round(trigger, 2),
                   limit=round(limit, 2), stop=round(stop, 2), risk_per_share=round(rps, 2), shares=shares,
                   risk_usd=round(shares * rps, 2), position_usd=round(shares * trigger, 2),
                   stop_pct=round(rps / trigger * 100, 1), ready=bool(ready), tt7=bool(tt7),
                   dist_to_pivot_pct=round((pivot / m["price"] - 1) * 100, 1))
        row["earnings"] = earnings_flag(t, today, risk["earnings_blackout_days"]) if ready else "-"
        rows.append(row)

    tickets, watch = [], []
    for r in sorted(rows, key=lambda x: -x["rs"]):
        if not r["ready"]:
            if r["from_tier"] == "execution":
                skipped.append((r["ticker"], "no longer meets Execution rules on fresh data"))
            else:
                watch.append(r)
            continue
        if r["earnings"].startswith("EARNINGS"):
            skipped.append((r["ticker"], r["earnings"] + " inside blackout window")); continue
        if r["shares"] < 1:
            skipped.append((r["ticker"], "position size < 1 share under your risk rules")); continue
        if len(tickets) >= max_orders:
            skipped.append((r["ticker"], f"over the {max_orders}-order cap for regime {regime}")); continue
        tickets.append(r)
    watch = sorted(watch, key=lambda x: abs(x["dist_to_pivot_pct"]))[:8]

    pos_lines = []
    if pos_df is not None:
        for _, p in pos_df.iterrows():
            try:
                c, h, l, v = series(p["ticker"]); m = metrics(c, h, l, v)
                flags = []
                if m["price"] < p["stop"]: flags.append("CLOSED BELOW STOP")
                if m["price"] < m["ema10"]: flags.append("below 10-day EMA (trail watch)")
                pos_lines.append(f"| {p['ticker']} | {m['price']:.2f} | {p['stop']} | {', '.join(flags) or 'ok'} |")
            except Exception:
                pos_lines.append(f"| {p['ticker']} | n/a | {p['stop']} | data error |")

    L = [f"# Pre-open plan {day} (US/Eastern)", "",
         f"Data through the {last_bar} close. Rule-based output from your own criteria, not investment advice. "
         "This plan places no orders; you place them yourself.", "",
         f"**Regime: {regime}** (SPY {'above' if spy['p_gt_50'] else 'below'} its 50-day SMA; "
         f"{summ['breadth_above_50sma']*100:.0f}% of the universe above its 50-day SMA as of the {summ['data_date']} screen). "
         f"Maximum new orders today: {max_orders}.", ""]
    if tickets:
        L += ["## Order tickets to place manually", "",
              "| Ticker | RS | Buy-stop trigger | Limit | Stop-loss | Stop % | Shares | $ risk | $ position | Earnings |",
              "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
        for r in tickets:
            L.append(f"| {r['ticker']} | {r['rs']} | {r['trigger']} | {r['limit']} | {r['stop']} | {r['stop_pct']} | "
                     f"{r['shares']} | {r['risk_usd']} | {r['position_usd']} | {r['earnings']} |")
        L += ["", "Per ticket: Buy Stop-Limit (trigger, limit), day order. After a fill, enter the stop-loss. "
              f"Skip it if the stock opens more than {risk['skip_if_open_above_trigger_pct']*100:.0f}% above the trigger, "
              "or if the breakout is not on volume of about 1.4x average pace.", ""]
    else:
        L += ["## Order tickets", "", "**No setup, no trade: nothing qualifies today.**", ""]
    if skipped:
        L += ["## Skipped", "", "| Ticker | Reason |", "| --- | --- |"] + [f"| {t} | {w} |" for t, w in skipped] + [""]
    if watch:
        L += ["## Almost Ready, closest to a pivot", "", "| Ticker | RS | Close | Pivot | Distance to pivot % |", "| --- | --- | --- | --- | --- |"]
        L += [f"| {r['ticker']} | {r['rs']} | {r['close']} | {r['pivot']} | {r['dist_to_pivot_pct']} |" for r in watch] + [""]
    if pos_lines:
        L += ["## Open positions check", "", "| Ticker | Close | Stop | Flag |", "| --- | --- | --- | --- |"] + pos_lines + [""]
    write(out, day, "\n".join(L) + "\n",
          {"date": day, "status": "ok", "regime": regime, "max_orders": max_orders, "data_through": last_bar,
           "tickets": tickets, "skipped": skipped, "watch": watch})


if __name__ == "__main__":
    main()
