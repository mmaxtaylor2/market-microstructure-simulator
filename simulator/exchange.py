from simulator.order_book import OrderBook

class Exchange:
    def __init__(self, tick_size=1, initial_price=100):
        self.tick = tick_size
        self.last_price = initial_price
        self.book = OrderBook()
        self.trades = []

    def submit_order(self, side, qty, price, step):
        # match buys against best asks
        if side == "buy":
            best_ask = self.book.best_ask()
            if best_ask and price >= best_ask:
                self._execute_trade(best_ask, qty, side, step)
            else:
                self.book.add_order(price, qty, side)

        # match sells against best bids
        else:
            best_bid = self.book.best_bid()
            if best_bid and price <= best_bid:
                self._execute_trade(best_bid, qty, side, step)
            else:
                self.book.add_order(price, qty, side)

    def _execute_trade(self, price, qty, side, step):
        trade = {
            "price": price,
            "qty": qty,
            "side": side,
            "step": step
        }
        self.trades.append(trade)
        self.last_price = price

    def mid(self):
        return self.book.mid(self.last_price)

    def spread(self):
        return self.book.spread()
