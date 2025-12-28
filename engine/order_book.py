# ------------------------------------------------------------
# order_book.py
# Basic Limit Order Book (LOB) structure for our simulator
# ------------------------------------------------------------

class OrderBook:
    def __init__(self):
        # dictionaries: price -> size
        self.bids = {}  # BUY side liquidity
        self.asks = {}  # SELL side liquidity

    # Add a limit order (order that sits on the book)
    def add_limit_order(self, side, price, size):
        book = self.bids if side.lower() == "buy" else self.asks
        book[price] = book.get(price, 0) + size

    # Get current highest buy price
    def best_bid(self):
        return max(self.bids.keys()) if self.bids else None

    # Get current lowest sell price
    def best_ask(self):
        return min(self.asks.keys()) if self.asks else None

    # Calculate bid-ask spread
    def spread(self):
        if self.best_bid() is None or self.best_ask() is None:
            return None
        return round(self.best_ask() - self.best_bid(), 2)

    # Useful snapshot for logging / debugging
    def snapshot(self):
        return {
            "best_bid": self.best_bid(),
            "best_ask": self.best_ask(),
            "spread": self.spread(),
            "bid_depth": sum(self.bids.values()),
            "ask_depth": sum(self.asks.values())
        }

