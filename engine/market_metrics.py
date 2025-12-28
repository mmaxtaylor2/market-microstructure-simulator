# ------------------------------------------------------------
# market_metrics.py (CLEAN RESET)
# ------------------------------------------------------------

def calc_mid(lob):
    bid = lob.best_bid()
    ask = lob.best_ask()
    if bid is not None and ask is not None:
        return round((bid + ask) / 2, 4)
    return bid or ask or None

def calc_vwap(trades):
    if not trades:
        return None
    total_value = sum(p * s for p, s in trades)
    total_volume = sum(s for _, s in trades)
    return round(total_value / total_volume, 4) if total_volume > 0 else None

__all__ = ["calc_mid", "calc_vwap"]

