import streamlit as st
from simulator.exchange import Exchange
from simulator.agents import MarketMaker, NoiseTrader, InformedTrader
from simulator.metrics import compute_metrics

st.title("Market Microstructure Simulator")

vol = st.slider("Volatility", 0.01, 1.0, 0.25)
steps = st.slider("Steps", 10, 500, 100)

if st.button("Run Simulation"):
    ...

