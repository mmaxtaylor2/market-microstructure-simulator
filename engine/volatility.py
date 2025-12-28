# ------------------------------------------------------------
# volatility.py
# Controls volatility shocks and spread behavior
# ------------------------------------------------------------
import random

class VolatilityModel:
    def __init__(self, order_book, shock_probability=0.25):
        self.order_book = order_book
        self.shock_probability = shock_probability

    def maybe_shock(self):
        if random.random() < self.shock_probability:
            # simulate liquidity dropping
            self.order_book.asks = {k: int(v * 0.5) for k, v in self.order_book.asks.items()}
            self.order_book.bids = {k: int(v * 0.5) for k, v in self.order_book.bids.items()}

            # widen the spread artificially
            if self.order_book.best_ask() is not None:
                new_ask = round(self.order_book.best_ask() + 0.2, 2)
                self.order_book.asks[new_ask] = 50

            if self.order_book.best_bid() is not None:
                new_bid = round(self.order_book.best_bid() - 0.2, 2)
                self.order_book.bids[new_bid] = 50

            return True  # shock occurred
        return False

