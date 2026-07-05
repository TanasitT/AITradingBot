import logging
import statistics
from utils.alpaca_client import get_bars, get_snapshot
from config import MIN_VOLUME_MULTIPLIER, HIGH_BETA_THRESHOLD

log = logging.getLogger(__name__)


def analyze(symbol):
    try:
        bars = get_bars(symbol, timeframe="1Day", limit=60)
        if not bars:
            return None

        closes = [b["c"] for b in bars]
        volumes = [b["v"] for b in bars]

        current_price = closes[-1]
        avg_volume_30d = statistics.mean(volumes[-30:]) if len(volumes) >= 30 else statistics.mean(volumes)

        snapshot = get_snapshot(symbol)
        todays_volume = snapshot.get("dailyBar", {}).get("v", 0)
        volume_ratio = todays_volume / avg_volume_30d if avg_volume_30d else 0

        ma50 = statistics.mean(closes[-50:]) if len(closes) >= 50 else None
        ma200 = statistics.mean(closes[-200:]) if len(closes) >= 200 else None
        ma5 = statistics.mean(closes[-5:]) if len(closes) >= 5 else None

        above_ma50 = current_price > ma50 if ma50 else None
        above_ma200 = current_price > ma200 if ma200 else None

        gains = [max(closes[i] - closes[i - 1], 0) for i in range(1, len(closes))]
        losses = [max(closes[i - 1] - closes[i], 0) for i in range(1, len(closes))]
        period = 14
        avg_gain = statistics.mean(gains[-period:]) if len(gains) >= period else 0
        avg_loss = statistics.mean(losses[-period:]) if len(losses) >= period else 1
        rs = avg_gain / avg_loss if avg_loss else 100
        rsi = 100 - (100 / (1 + rs))

        daily_returns = [
            (closes[i] - closes[i - 1]) / closes[i - 1]
            for i in range(1, len(closes))
        ]
        if len(daily_returns) >= 20:
            vol = statistics.stdev(daily_returns[-20:])
            spy_vol = 0.01
            beta = vol / spy_vol
        else:
            beta = 1.0

        high_beta = beta > HIGH_BETA_THRESHOLD
        volume_ok = volume_ratio >= MIN_VOLUME_MULTIPLIER
        rsi_ok = 40 <= rsi <= 70

        result = {
            "symbol": symbol,
            "price": current_price,
            "volume_ratio": volume_ratio,
            "rsi": rsi,
            "above_ma50": above_ma50,
            "above_ma200": above_ma200,
            "beta": beta,
            "high_beta": high_beta,
            "volume_ok": volume_ok,
            "rsi_ok": rsi_ok,
            "technically_sound": volume_ok and rsi_ok and (above_ma50 is not False),
        }
        log.info(
            f"[Technical] {symbol}: price={current_price:.2f} vol_ratio={volume_ratio:.1f}x "
            f"RSI={rsi:.0f} beta={beta:.1f} sound={result['technically_sound']}"
        )
        return result

    except Exception as e:
        log.warning(f"[Technical] Failed to analyze {symbol}: {e}")
        return None
