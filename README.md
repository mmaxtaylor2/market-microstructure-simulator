# Market Microstructure Simulator

https://market-microstructure-simulator-unffozunxgihsalzxtmgau.streamlit.app

## Overview

A Python-based analytical project that models electronic limit order book (LOB) microstructure under different order flow assumptions. The project mirrors how execution analysts and microstructure researchers study price formation by linking quoting behavior, liquidity-taking flow, and matching mechanisms into a unified simulation environment.

The objective is to quantify how market makers, noise traders, and informed traders influence mid-price dynamics, spreads, liquidity distribution, and short-horizon execution metrics such as slippage and price impact.

## Problem Context

Microstructure analysis focuses on how markets translate trading intentions into transaction prices. While valuation frameworks explain why assets should trade at certain levels, microstructure determines how they actually do so — order by order and tick by tick. Bid-ask spreads, queue depth, inventory risk, and order flow composition produce measurable execution costs and market quality outcomes.

This project introduces a structured simulation environment for analyzing these dynamics within a simplified electronic limit order book.

## Key Questions

-- How does the mid-price evolve under different order flow environments?  
-- What determines the behavior of the spread over time?  
-- How does depth accumulate across price levels in the LOB?  
-- Under what conditions does execution slippage remain negligible?  
-- How does informed flow influence price impact?  

## Microstructure Framework

The model adopts a discrete-time agent-based setting in which quoting and trading occur at integer tick resolution. At each time step:

1. Market Makers post symmetric bid and ask quotes around the mid at fixed tick offsets.  
2. Noise Traders generate random liquidity-taking flow with tunable intensity.  
3. Informed Traders submit larger trades with configurable probability.  

A simple price-time priority matching engine executes trades when incoming orders cross the book.

## Execution Metrics

The simulator computes two execution metrics commonly used in microstructure and TCA studies:

**Slippage**
\[
\text{slippage}_t = s_t (p^{exec}_t - m^{before}_t)
\]
where \(s_t = +1\) for buys and \(-1\) for sells

**Impact**
\[
\text{impact}_t = m^{after}_t - m^{before}_t
\]

Trade-level results are displayed in a blotter and visualized graphically.

## Scenario Layer

The system exposes configurable inputs for experimentation:

-- Number of time steps  
-- Market maker quoting width (ticks)  
-- Noise trader intensity  
-- Informed trader arrival probability  

These levers allow users to explore different microstructure regimes ranging from low-activity symmetric flow to high-activity directional environments.

## Outputs

The application reports:

-- Mid-price path  
-- Spread path  
-- Slippage distribution  
-- Impact vs. step  
-- Trade blotter  
-- Final depth histogram  
-- Level II book snapshot  

Together, these outputs illustrate how quoting behavior and order flow propagate through the matching engine and into observable execution metrics.

## Interpretation

Under symmetric flow with synchronous execution and no informational edge, slippage clusters around zero and spreads converge toward a minimum tick value. Depth accumulates away from the inside market, consistent with simple quoting incentives. Market maker activity anchors price behavior, while informed flow introduces intermittent directional effects.

## Possible Extensions

The framework may be extended to incorporate:

-- Market maker PnL and adverse selection  
-- Latency and queue priority effects  
-- Fair-value drift and alpha signals  
-- Transaction cost analysis (TCA) tooling  
-- Execution algorithms (TWAP, POV, IS)  
-- Multi-venue routing  
-- Hawkes order flow dynamics  

These extensions are not required for the baseline mechanism to function.

