import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from simulator.exchange import Exchange
from simulator.agents import MarketMaker, NoiseTrader, InformedTrader
from simulator.metrics import compute_slippage_and_impact
from simulator.utils import ladder_view

st.title("Market Microstructure Simulator")

st.sidebar.header("Parameters")
steps = st.sidebar.slider("Steps", 50, 1000, 200)
mm_spread = st.sidebar.slider("Market Maker Spread", 1, 10, 2)
noise_intensity = st.sidebar.slider("Noise Intensity", 0.0, 1.0, 0.3)
alpha_prob = st.sidebar.slider("Informed Alpha Probability", 0.0, 1.0, 0.1)

if st.sidebar.button("Run Simulation"):
    ex = Exchange(initial_price=100)

    mm = MarketMaker(spread=mm_spread)
    nt = NoiseTrader(intensity=noise_intensity)
    it = InformedTrader(alpha_prob=alpha_prob)

    mids = []
    spreads = []

    for step in range(steps):
        mid = ex.mid()
        mids.append(mid)
        spreads.append(ex.spread())

        for agent in [mm, nt, it]:
            for side, qty, price in agent.generate(mid):
                ex.submit_order(side, qty, price, step)

    # process depth snapshot
    depth = ex.book.aggregate_depth()
    bids, asks = ladder_view(depth)

    # trade analytics
    blotter = compute_slippage_and_impact(ex.trades, mids)

    st.subheader("Mid Price Path")
    st.line_chart(mids)

    st.subheader("Spread Path")
    st.line_chart(spreads)

    if not blotter.empty:
        st.subheader("Slippage Distribution")
        st.bar_chart(blotter["slippage"])

        st.subheader("Impact vs Step")
        st.line_chart(blotter.set_index("step")["impact"])

        st.subheader("Trade Blotter")
        st.dataframe(blotter.sort_values("step"))

    st.subheader("Final Depth Histogram")
    fig, ax = plt.subplots()
    for p, q in bids:
        ax.barh([p], [q], color="blue")
    for p, q in asks:
        ax.barh([p], [q], color="red")
    ax.set_xlabel("Size")
    ax.set_ylabel("Price")
    st.pyplot(fig)

    st.subheader("Level II Ladder")
    st.write({"bids": bids, "asks": asks})
