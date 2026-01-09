import pandas as pd

def compute_slippage_and_impact(trades, mids):
    rows = []
    for t in trades:
        step = t["step"]
        px_exec = t["price"]
        mid_before = mids[step]
        mid_after = mids[min(step + 1, len(mids) - 1)]

        side = t["side"]
        signed = 1 if side == "buy" else -1

        slippage = signed * (px_exec - mid_before)
        impact = mid_after - mid_before

        rows.append({
            "step": step,
            "side": side,
            "qty": t["qty"],
            "price": px_exec,
            "mid_before": mid_before,
            "slippage": slippage,
            "impact": impact
        })

    return pd.DataFrame(rows) if rows else pd.DataFrame()

