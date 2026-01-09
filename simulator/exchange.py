from simulator.order_book import OrderBook

class Exchange:
    def __init__(self, tick_size=1, initial_price=100):
        self.tick = tick_size
        self.price = initial_price
        self.book = OrderBook()
        self.trades = []

    def submit_order(self, side, qty, price):
        """
        Try to match order; if not filled, add to book.
        """
        if side == "buy":
            best_ask = self.book.best_ask()
            if best_ask and price >= best_ask:
                self._execute_trade(best_ask, qty, side)
            else:
                self.book.add_order(price, qty, "buy")

        elif side == "sell":
            best_bid = self.book.best_bid()
            if best_bid and price <= best_bid:
                self._execute_trade(best_bid, qty, side)
            else:
                self.book.add_order(price, qty, "sell")

    def _execute_trade(self, price, qty, side):
        self.trades.append({"price": price, "qty": qty, "side": side})
        self.price = price  # update last traded

    def get_mid_price(self):
        bid = self.book.best_bid()
        ask = self.book.best_ask()
        if bid and ask:
            return (bid + ask) / 2
        return self.price
