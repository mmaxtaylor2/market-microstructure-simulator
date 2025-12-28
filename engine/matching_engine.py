# ------------------------------------------------------------
# matching_engine.py
# Executes market orders with price impact (walk the book)
# ------------------------------------------------------------

class MatchingEngine:
    def __init__(self, order_book):
        self.book = order_book
        self.trade_history = []

    def execute_market_order(self, side, size):
        trades = []
        remaining = size

        # market BUY -> remove from best ask upwards
        if side.lower() == "buy":
            while remaining > 0 and self.book.asks:
                best_price = self.book.best_ask()
                available = self.book.asks[best_price]

                trade_size = min(remaining, available)
                trades.append((best_price, trade_size))

                self.book.asks[best_price] -= trade_size
                if self.book.asks[best_price] == 0:
                    del self.book.asks[best_price]

                remaining -= trade_size

        # market SELL -> remove from best bid downwards
        else:
            while remaining > 0 and self.book.bids:
                best_price = self.book.best_bid()
                available = self.book.bids[best_price]

                trade_size = min(remaining, available)
                trades.append((best_price, trade_size))

                self.book.bids[best_price] -= trade_size
                if self.book.bids[best_price] == 0:
                    del self.book.bids[best_price]

                remaining -= trade_size

        # log trades
        for price, qty in trades:
            self.trade_history.append({"side": side, "price": price, "size": qty})

        return trades if trades else None

