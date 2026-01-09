import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from simulator.exchange import Exchange
from simulator.agents import MarketMaker, NoiseTrader, InformedTrader
from simulator.metrics import compute_slippage_and_impact
from simulator.utils import ladder_view

# -----------------------------
# Sidebar parameters
# -----------------------------
st.title("Market Microstructure Simulator")

st.sidebar.header("Parameters")
steps = st.sidebar.slider("Steps", 50, 1000, 200)
mm_spread = st.sidebar.slider("Market Maker Spread (ticks)", 1, 10, 2)
noise_intensity = st.sidebar.slider("Noise Intensity", 0.0, 1.0, 0.40)
alpha_prob = st.sidebar.slider("Informed Alpha Probability", 0.0, 1.0, 0.10)

run_button = st.sidebar.button("Run Simulation")

# -----------------------------
# Simulation
# -----------------------------
if run_button:
    ex = Exchange(initial_price=100)

    mm = MarketMaker(spread=mm_spread)
    nt = NoiseTrader(intensity=noise_intensity)
    it = InformedTrader(alpha_prob=alpha_prob)

    mids = []
    spreads = []

    for step in range(steps):
        # enforce integer mid for cleaner display/ladder
        mid = int(round(ex.mid()))
        mids.append(mid)
        spreads.append(ex.spread())

        # agents submit orders based on current mid
        for agent in [mm, nt, it]:
            for side, qty, price in agent.generate(mid):
                ex.submit_order(side, qty, price, step)

    # -----------------------------
    # Order book depth snapshot
    # -----------------------------
    depth = ex.book.aggregate_depth()
    bids, asks = ladder_view(depth)

    # -----------------------------
    # Trade analytics (slippage / impact / blotter)
    # -----------------------------
    blotter = compute_slippage_and_impact(ex.trades, mids)

    # -----------------------------
    # Charts: mid price & spread
    # -----------------------------
    st.subheader("Mid Price Path")
    st.line_chart(mids)

    st.subheader("Spread Path")
    st.line_chart(spreads)

    # -----------------------------
    # Slippage & impact
    # -----------------------------
    if not blotter.empty:
        st.subheader("Slippage Distribution")
        fig_slip, ax_slip = plt.subplots()
        ax_slip.hist(blotter["slippage"], bins=20)
        ax_slip.set_xlabel("Slippage (ticks)")
        ax_slip.set_ylabel("Count")
        st.pyplot(fig_slip)

        st.subheader("Impact vs Step")
        st.line_chart(blotter.set_index("step")["impact"])

        st.subheader("Trade Blotter (Chronological)")
        st.dataframe(
            blotter.sort_values("step")[["step", "side", "qty", "price", "mid_before", "slippage", "impact"]]
        )

        st.subheader("Summary Metrics")
        summary = {
            "Number of trades": int(len(blotter)),
            "Average slippage": float(blotter["slippage"].mean()),
            "Average impact": float(blotter["impact"].mean()),
            "Final spread": spreads[-1],
        }
        st.write(summary)
    else:
        st.info("No trades occurred in this run. Increase noise / alpha to see more activity.")

    # -----------------------------
    # Final depth histogram
    # -----------------------------
    st.subheader("Final Depth Histogram")

    fig_depth, ax_depth = plt.subplots()
    for p, q in bids:
        ax_depth.barh(p, q)
    for p, q in asks:
        ax_depth.barh(p, q)
    ax_depth.set_xlabel("Size")
    ax_depth.set_ylabel("Price (ticks)")
    st.pyplot(fig_depth)

    # -----------------------------
    # Level II Ladder (clean table)
    # -----------------------------
    st.subheader("Level II Ladder")

    ladder_rows = []
    for p, q in bids:
        ladder_rows.append({"Side": "Bid", "Price": p, "Size": q})
    for p, q in asks:
        ladder_rows.append({"Side": "Ask", "Price": p, "Size": q})

    if ladder_rows:
        df_ladder = pd.DataFrame(ladder_rows)
        # show bids first (sorted desc), then asks (sorted asc)
        df_ladder = df_ladder.sort_values(
            by=["Side", "Price"],
            ascending=[False, False]  # Bids desc, Asks asc
        )
        st.table(df_ladder)
    else:
        st.info("Order book is empty at the final snapshot.")

