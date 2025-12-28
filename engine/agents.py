# ------------------------------------------------------------
# agents.py
# Hybrid market maker: reacts to shocks & price impact
# ------------------------------------------------------------
import random

class NoiseTrader:
    """Random trader sending unpredictable market orders."""
    def __init__(self, engine):
        self.engine = engine

    def step(self):
        side = random.choice(["buy", "sell"])
        size = random.randint(10, 100)
        self.engine.execute_market_order(side, size)


class MarketMaker:
    """Adaptive market maker that adjusts quotes based on volatility."""
    def __init__(self, order_book, base_spread=0.05):
        self.book = order_book
        self.base_spread = base_spread

    def adaptive_quote(self, mid, stressed=False, aggressive=False):
        # Spread widens when stressed
        spread = self.base_spread * (2.5 if stressed else 1.0)

        # Price shifts upward after aggressive buy pressure
        if aggressive:
            mid = round(mid + 0.10, 2)

        bid = round(mid - spread, 2)
        ask = round(mid + spread, 2)

        # If liquidity vanished, supply wider quotes to recover depth
        if self.book.best_ask() is None:
            ask = round(mid + spread * 2, 2)
        if self.book.best_bid() is None:
            bid = round(mid - spread * 2, 2)

        # Size shrinks under stress
        size = 50 if not stressed else 20

        self.book.add_limit_order("buy", bid, size)
        self.book.add_limit_order("sell", ask, size)

        return bid, ask

