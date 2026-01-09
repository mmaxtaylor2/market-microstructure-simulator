# empty initializer for simulator package

from collections import deque

class OrderBook:
    def __init__(self):
        self.bids = {}  # {price: deque([orders])}
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

    def spread(self):
        if not self.bids or not self.asks:
            return None
        return self.best_ask() - self.best_bid()

    def depth(self):
        return {
            "bids": {p: sum(o["qty"] for o in orders) for p, orders in self.bids.items()},
            "asks": {p: sum(o["qty"] for o in orders) for p, orders in self.asks.items()},
        }
