#!/usr/bin/env python3
"""Weekly US momentum screen (Minervini-style Trend Template + RS approximation + contraction).

Writes results/<data_date>/ and results/latest/:
  tiers.json, summary.json, changes.json, screen_results.csv, watchlist.txt
Run from the repo root:  python scripts/us_momentum_screen.py
Data: Yahoo Finance via yfinance (unofficial, daily bars). Analysis only - no trading.
"""
import argparse, io, json, shutil, sys, time, warnings
from datetime import date
from pathlib import Path
import numpy as np, pandas as pd, requests, yfinance as yf
warnings.filterwarnings("ignore")

TT_COLS = ["p_gt_150_200", "s150_gt_200", "s200_up", "s50_gt_150_200",
           "p_gt_50", "gt30_above_low", "within25_high"]
CFG = dict(min_history=260, rs_min=70, rs_wide_min=60, near_high_exec=0.03, tight_10d=0.12,
           vol_dry=0.92, almost_high=0.12, exec_cap=5, almost_cap=60, short_cap=20)


def load_universe(extra_path):
    tickers = set()
    try:
        html = requests.get("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies",
                            headers={"User-Agent": "Mozilla/5.0"}, timeout=30).text
        tickers |= set(pd.read_html(io.StringIO(html))[0]["Symbol"].str.replace(".", "-", regex=False))
    except Exception as e:
        print("WARN: S&P 500 list failed:", e, file=sys.stderr)
    p = Path(extra_path)
    if p.exists():
        for line in p.read_text().splitlines():
            line = line.split("#")[0].replace(",", " ")
            tickers |= {t.strip().upper() for t in line.split() if t.strip()}
    return sorted(tickers | {"SPY", "QQQ"})


def download(tickers, tries=3):
    for i in range(tries):
        try:
            px = yf.download(tickers, period="14mo", interval="1d", auto_adjust=True,
                             progress=False, threads=True, group_by="column")
            if px is not None and not px.empty:
                return px
        except Exception as e:
            print("download retry", i, e, file=sys.stderr)
        time.sleep(30)
    sys.exit("ERROR: price download failed after retries")


def metrics(c, h, l, v):
    """Scalar metrics for one ticker from daily close/high/low/volume Series (>= 260 bars)."""
    sma50, sma150, sma200 = [c.rolling(n).mean() for n in (50, 150, 200)]
    ema20 = c.ewm(span=20, adjust=False).mean()
    ema10 = c.ewm(span=10, adjust=False).mean()
    last = float(c.iloc[-1])
    hi52, lo52 = float(h.iloc[-252:].max()), float(l.iloc[-252:].min())
    ret = lambda n: float(c.iloc[-1] / c.iloc[-1 - n] - 1)
    r1, r3, r6, r9, r12 = [ret(n) for n in (21, 63, 126, 189, 252)]

    def rng(a, b):
        hh, ll = h.iloc[a:b].max(), l.iloc[a:b].min()
        return float((hh - ll) / ll)

    w3, w2, w1 = rng(-30, -20), rng(-20, -10), rng(-10, None)
    m = dict(
        price=last, r1m=r1, r3m=r3, r6m=r6,
        rs_raw=0.4 * r3 + 0.2 * r6 + 0.2 * r9 + 0.2 * r12,
        pct_from_high=last / hi52 - 1,
        above_ema20=bool(last > ema20.iloc[-1]),
        sma50=float(sma50.iloc[-1]), sma200=float(sma200.iloc[-1]), ema10=float(ema10.iloc[-1]),
        rng_w3=w3, rng_w2=w2, rng_w1=w1, contracting=bool(w3 > w2 > w1),
        vol_dryup=float(v.iloc[-10:].mean() / v.iloc[-50:].mean()),
        dist_20d_high=float(last / h.iloc[-20:].max() - 1),
        p_gt_200=bool(last > sma200.iloc[-1]),
        p_gt_150_200=bool(last > sma150.iloc[-1] and last > sma200.iloc[-1]),
        s150_gt_200=bool(sma150.iloc[-1] > sma200.iloc[-1]),
        s200_up=bool(sma200.iloc[-1] > sma200.iloc[-22]),
        s50_gt_150_200=bool(sma50.iloc[-1] > sma150.iloc[-1] and sma50.iloc[-1] > sma200.iloc[-1]),
        p_gt_50=bool(last > sma50.iloc[-1]),
        gt30_above_low=bool(last >= 1.30 * lo52),
        within25_high=bool(last >= 0.75 * hi52),
    )
    m["tt_count"] = int(sum(m[k] for k in TT_COLS))
    return m


def fundamentals(t):
    try:
        q = yf.Ticker(t).quarterly_income_stmt
        rev = q.loc["Total Revenue"].dropna().sort_index()
        out = {"last_q": str(rev.index[-1].date()), "rev_qoq": float(rev.iloc[-1] / rev.iloc[-2] - 1),
               "rev_yoy": float(rev.iloc[-1] / rev.iloc[-5] - 1) if len(rev) >= 5 else None}
        if "Diluted EPS" in q.index:
            eps = q.loc["Diluted EPS"].dropna().sort_index()
            if len(eps) >= 2 and eps.iloc[-2] > 0:
                out["eps_qoq"] = float(eps.iloc[-1] / eps.iloc[-2] - 1)
            if len(eps) >= 5 and eps.iloc[-5] > 0:
                out["eps_yoy"] = float(eps.iloc[-1] / eps.iloc[-5] - 1)
        out["meets_30pct_qoq"] = bool(out["rev_qoq"] >= 0.30 and out.get("eps_qoq", -1) >= 0.30)
        return out
    except Exception as e:
        return {"error": str(e)[:60]}


def entry(df, t, fund=None):
    r = df.loc[t]
    d = {"ticker": t, "price": round(r.price, 2), "r1m": round(r.r1m * 100, 1), "r3m": round(r.r3m * 100, 1),
         "r6m": round(r.r6m * 100, 1), "rs_rating": int(r.rs_rating),
         "pct_from_high": round(r.pct_from_high * 100, 1), "above_ema20": bool(r.above_ema20),
         "contracting": bool(r.contracting), "vol_dryup": round(r.vol_dryup, 2),
         "dist_20d_high": round(r.dist_20d_high * 100, 1), "rng_10d_pct": round(r.rng_w1 * 100, 1),
         "tt_count": int(r.tt_count)}
    if fund:
        d["fundamentals"] = fund
    return d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--extra", default="config/extra_tickers.txt")
    ap.add_argument("--outdir", default="results")
    a = ap.parse_args()

    tickers = load_universe(a.extra)
    print("universe:", len(tickers))
    px = download(tickers)
    close, high, low, vol = px["Close"], px["High"], px["Low"], px["Volume"]
    close = close.dropna(axis=1, thresh=CFG["min_history"])
    data_date = str(close.index[-1].date())

    rows = []
    for t in close.columns:
        c = close[t].dropna()
        if len(c) < CFG["min_history"]:
            continue
        m = metrics(c, high[t].reindex(c.index), low[t].reindex(c.index), vol[t].reindex(c.index))
        m["ticker"] = t
        rows.append(m)
    df = pd.DataFrame(rows).set_index("ticker")
    bench = df.loc[[i for i in ("SPY", "QQQ") if i in df.index]]
    df = df.drop(index=bench.index)
    df["rs_rating"] = (df["rs_raw"].rank(pct=True) * 98 + 1).round(0)
    df["tt_7"] = df[TT_COLS].all(axis=1)
    df["tt_pass"] = df["tt_7"] & (df["rs_rating"] >= CFG["rs_min"])

    near = df.dist_20d_high >= -CFG["near_high_exec"]
    tight = df.rng_w1 <= CFG["tight_10d"]
    dry = df.vol_dryup <= CFG["vol_dry"]
    ex_all = df[df.tt_pass & near & tight & (df.contracting | dry)].sort_values("rs_rating", ascending=False)
    ex = ex_all.head(CFG["exec_cap"])
    al_all = df[df.tt_pass & df.above_ema20 & (df.contracting | tight | dry) &
                (df.pct_from_high >= -CFG["almost_high"])].drop(index=ex.index).sort_values("rs_rating", ascending=False)
    al = al_all.head(CFG["almost_cap"])
    sec = df[df.tt_pass].drop(index=ex.index.union(al.index)).sort_values("rs_rating", ascending=False)
    wl = df[(df.tt_count >= 6) & (df.rs_rating >= CFG["rs_wide_min"]) & ~df.tt_pass].sort_values("rs_rating", ascending=False)
    sh = df[(~df.p_gt_150_200) & (~df.p_gt_50) & (df.rs_rating <= 15)].sort_values("rs_rating").head(CFG["short_cap"])

    print("fundamentals for", len(ex) + len(al), "names ...")
    fund = {t: fundamentals(t) for t in list(ex.index) + list(al.index)}
    tiers = {
        "execution": [entry(df, t, fund.get(t)) for t in ex.index],
        "almost_ready": [entry(df, t, fund.get(t)) for t in al.index],
        "secondary": [entry(df, t) for t in sec.index],
        "wide_long": [entry(df, t) for t in wl.index],
        "wide_short": [entry(df, t) for t in sh.index],
    }

    spy = bench.loc["SPY"] if "SPY" in bench.index else None
    breadth50, breadth200 = float(df.p_gt_50.mean()), float(df.p_gt_200.mean())
    regime = "Selective"
    if spy is not None:
        regime = "Defense" if not spy.p_gt_50 else ("Offense" if breadth50 >= 0.5 else "Selective")
    summary = dict(data_date=data_date, run_date=str(date.today()), universe_scored=int(len(df)),
                   trend_template_pass=int(df.tt_pass.sum()), breadth_above_50sma=round(breadth50, 3),
                   breadth_above_200sma=round(breadth200, 3), regime=regime,
                   spy=None if spy is None else dict(price=round(spy.price, 2), sma50=round(spy.sma50, 2),
                                                     sma200=round(spy.sma200, 2), r1m=round(spy.r1m * 100, 1),
                                                     r3m=round(spy.r3m * 100, 1)),
                   counts={k: len(v) for k, v in tiers.items()})

    out = Path(a.outdir)
    prev = {}
    pj = out / "latest" / "tiers.json"
    if pj.exists():
        old = json.loads(pj.read_text())
        prev = {e["ticker"]: k for k, v in old.items() for e in v}
    new = {e["ticker"]: k for k, v in tiers.items() for e in v}
    changes = [{"ticker": t, "from": prev.get(t, "-"), "to": k} for t, k in new.items() if prev.get(t, "-") != k]
    changes += [{"ticker": t, "from": k, "to": "-"} for t, k in prev.items() if t not in new]

    dated = out / data_date
    dated.mkdir(parents=True, exist_ok=True)
    (dated / "tiers.json").write_text(json.dumps(tiers, indent=1))
    (dated / "summary.json").write_text(json.dumps(summary, indent=1))
    (dated / "changes.json").write_text(json.dumps(changes, indent=1))
    names = [("1 Execution", "execution"), ("2 Almost Ready", "almost_ready"), ("3 Secondary", "secondary"),
             ("4 Wide List Long", "wide_long"), ("5 Wide List Short", "wide_short")]
    (dated / "watchlist.txt").write_text(
        "\n".join("###" + n + "," + ",".join(e["ticker"] for e in tiers[k]) for n, k in names) + "\n")
    res = df.copy()
    res["tier"] = [new.get(t, "-") for t in res.index]
    res.drop(columns=["rs_raw"]).round(4).to_csv(dated / "screen_results.csv")
    latest = out / "latest"
    if latest.exists():
        shutil.rmtree(latest)
    shutil.copytree(dated, latest)
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
