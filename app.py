import streamlit as st
from simulator.exchange import Exchange
from simulator.agents import MarketMaker, NoiseTrader, InformedTrader
from simulator.metrics import compute_metrics
import pandas as pd
import matplotlib.pyplot as plt

st.title("Market Microstructure Simulator")

st.sidebar.header("Simulation Settings")
steps = st.sidebar.slider("Simulation Steps", 10, 500, 100)
mm_spread = st.sidebar.slider("Market Maker Spread", 1, 10, 2)
noise_intensity = st.sidebar.slider("Noise Trader Intensity", 0.0, 1.0, 0.3)
alpha_prob = st.sidebar.slider("Informed Trader Probability", 0.0, 1.0, 0.1)

run_button = st.sidebar.button("Run Simulation")

if run_button:
    ex = Exchange()

    mm = MarketMaker(spread=mm_spread)
    nt = NoiseTrader(intensity=noise_intensity)
    it = InformedTrader(alpha_prob=alpha_prob)

    trades = []
    book_snapshots = []

    for step in range(steps):
        mid = ex.get_mid_price()

        for agent in [mm, nt, it]:
            orders = agent.generate_orders(mid)
            for side, qty, price in orders:
                ex.submit_order(side, qty, price)

        trades.extend(ex.trades)
        book_snapshots.append({
            "spread": ex.book.spread(),
            "mid": ex.get_mid_price()
        })

    st.subheader("Trade Prices Over Time")
    if trades:
        df = pd.DataFrame(trades)
        st.line_chart(df["price"])

    st.subheader("Spread Over Time")
    sp = [b["spread"] for b in book_snapshots]
    st.line_chart(sp)

    st.subheader("Execution Metrics")
    st.write(compute_metrics(trades, book_snapshots))
