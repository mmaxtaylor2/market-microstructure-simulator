# simulator package initializer

from collections import deque

class OrderBook:
    def __init__(self):
        # price → deque of orders
        self.bids = {}
        self.asks = {}

    def add_order(self, price, qty, side):
        book = self.bids if side == "buy" else self.asks
        if price not in book:
            book[price] = deque()
        book[price].append({"price": price, "qty": qty})

    def best_bid(self):
        return max(self.bids.keys()) if self.bids else None

    def best_ask(self):
        return min(self.asks.keys()) if self.asks else None

    def mid(self, last_price):
        bid = self.best_bid()
        ask = self.best_ask()
        if bid and ask:
            return (bid + ask) / 2
        return last_price

    def spread(self):
        if not self.bids or not self.asks:
            return None
        return self.best_ask() - self.best_bid()

    def aggregate_depth(self):
        return {
            "bids": {p: sum(o["qty"] for o in orders) for p, orders in self.bids.items()},
            "asks": {p: sum(o["qty"] for o in orders) for p, orders in self.asks.items()}
        }
