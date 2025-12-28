## Market Microstructure Simulator

This project is a simplified market microstructure simulator built in Python. It models an electronic limit order book, basic order execution mechanics, and position/PnL tracking. The goal is to demonstrate practical understanding of execution flow, bid/ask dynamics, and price formation in a market environment.

This is not intended to be a production trading engine. It is a foundational educational project that shows competency in market structure, simulation design, and core Python architecture.

---

## Project Features
- Limit order book with bids and asks
- Market and limit order handling
- Matching engine using price/time priority
- Market Maker and Retail order flow bots
- Position tracking, cost basis, and realized/unrealized PnL
- Basic terminal interface for interaction

---

## Purpose of the Project
This project is designed for recruiter and hiring manager review. It demonstrates the ability to:
- Implement order-driven market logic in code
- Structure a simulation around real-world market mechanics
- Understand liquidity, execution flow, and price formation
- Build functioning tools rather than isolated scripts

This project is appropriate for entry-level candidates applying to:
- Trading, execution, or market operations roles
- Quant or trading internships
- Data and risk analytics positions
- Brokerage or trading firm rotational programs

---

## Project Structure
(Formatted to avoid GitHub indentation or spacing issues)
market-microstructure-simulator/
|
├── exchange.py              # Core engine: order book, matching, bots, PnL
|
├── ui/
│   └── terminal_ui.py       # Interactive terminal interface
|
├── data/                    # Optional output folder (trade logs, CSVs)
|
└── __init__.py              # Enables package/module execution

## How to Run the Simulator
From the project root directory:
python3 -m ui.terminal_ui

## Terminal Command Options
(1) View Order Book
(2) Place Order (Market / Limit)
(3) Advance Simulation Step
(4) View PnL & Recent Trades
(5) Toggle Bots On/Off
(6) Quit
