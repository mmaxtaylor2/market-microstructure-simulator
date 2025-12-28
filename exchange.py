# exchange.py
import random
from collections import defaultdict, deque

class Exchange:
    def __init__(self):
        # order book storage
        self.bids = defaultdict(deque) # buy orders  (high → low)
        self.asks = defaultdict(deque) # sell orders (low → high)

        # trade + price history
        self.trade_log = []
        self.current_step = 0

        # pnl + position tracking
        self.position = 0
        self.avg_cost = 0.0
        self.realized_pnl = 0.0

        # internal counters
        self.order_id = 0
        self.last_shock = False

    # ------------------------------------------------------------
    # ORDER ENTRY
    # ------------------------------------------------------------
    def submit_order(self, side, qty, order_type="market", price=None):
        self.order_id += 1
        oid = self.order_id

        if order_type == "market":
            return self._market_order(side, qty, oid)

        if order_type == "limit" and price is not None:
            if side == "buy":
                self.bids[price].append((qty, oid, "buy"))
            else:
                self.asks[price].append((qty, oid, "sell"))
            return {"id": oid, "status": "resting", "side": side, "qty": qty, "price": price}

        raise ValueError("Invalid order. Must specify type and price for limit.")

    # ------------------------------------------------------------
    # MARKET ORDERS → immediate execution
    # ------------------------------------------------------------
    def _market_order(self, side, qty, oid):
        if side == "buy":
            return self._match("buy", qty, oid, self.asks, ascending=True)
        else:
            return self._match("sell", qty, oid, self.bids, ascending=False)

    # ------------------------------------------------------------
    # MATCHING ENGINE
    # ------------------------------------------------------------
    def _match(self, side, qty, oid, book, ascending):
        remaining = qty
        prices = sorted(book.keys(), reverse=not ascending)

        for price in prices:
            if remaining <= 0:
                break

            queue = book[price]
            updated = deque()

            while queue and remaining > 0:
                book_qty, bid_id, book_side = queue.popleft()
                trade_size = min(remaining, book_qty)
                remaining -= trade_size
                leftover = book_qty - trade_size

                # trade record
                self.trade_log.append((price, trade_size, side))

                # pnl logic
                self._apply_fill(side, price, trade_size)

                if leftover > 0:
                    updated.append((leftover, bid_id, book_side))

            if updated:
                book[price] = updated
            else:
                del book[price]

        return {"id": oid, "filled": qty - remaining, "unfilled": remaining}

    # ------------------------------------------------------------
    # PnL LOGIC
    # ------------------------------------------------------------
    def _apply_fill(self, side, price, qty):
        # BUY → increase position, adjust cost
        if side == "buy":
            if self.position + qty != 0:
                self.avg_cost = ((self.avg_cost * self.position) + (price * qty)) / (self.position + qty)
            self.position += qty

        # SELL → decrease position, lock in pnl
        elif side == "sell":
            if self.position > 0:
                realized = (price - self.avg_cost) * min(self.position, qty)
                self.realized_pnl += realized
            self.position -= qty

    # ------------------------------------------------------------
    # BOOK STATE / METRICS
    # ------------------------------------------------------------
    def get_mid(self):
        if not self.bids or not self.asks:
            return None
        return round((max(self.bids.keys()) + min(self.asks.keys())) / 2, 3)

    def get_spread(self):
        if not self.bids or not self.asks:
            return None
        return round(min(self.asks.keys()) - max(self.bids.keys()), 3)

    def get_snapshot(self, levels=5):
        bids = sorted(self.bids.items(), reverse=True)[:levels]
        asks = sorted(self.asks.items())[:levels]
        return {
            "bids": [(px, sum(q for q,_,_ in ql)) for px, ql in bids],
            "asks": [(px, sum(q for q,_,_ in ql)) for px, ql in asks]
        }

    # ------------------------------------------------------------
    # BOTS (LIGHTWEIGHT)
    # ------------------------------------------------------------
    def _bots(self):
        mid = self.get_mid()
        if not mid:
            mid = 100.0
        
        # market maker
        self.submit_order("buy",  random.randint(5,15), "limit", round(mid-0.05,2))
        self.submit_order("sell", random.randint(5,15), "limit", round(mid+0.05,2))

        # occasional retail
        if random.random() < 0.20:
            side = random.choice(["buy","sell"])
            self.submit_order(side, random.randint(3,20), "market")

    # ------------------------------------------------------------
    # SIM STEP
    # ------------------------------------------------------------
    def step(self, bots=True):
        self.current_step += 1
        self.last_shock = random.random() < 0.10
        move = random.choice([-0.05,0.05]) * (5 if self.last_shock else 1)

        # shift book
        self.bids = defaultdict(deque, {round(p+move,2):q for p,q in self.bids.items()})
        self.asks = defaultdict(deque, {round(p+move,2):q for p,q in self.asks.items()})

        if bots: self._bots()

        return {
            "step": self.current_step,
            "mid": self.get_mid(),
            "spread": self.get_spread(),
            "position": self.position,
            "realized": round(self.realized_pnl,2)
        }

    def pnl_report(self):
        mid = self.get_mid() or 0
        unreal = (mid - self.avg_cost) * self.position if self.position != 0 else 0
        total = self.realized_pnl + unreal
        return {
            "position": self.position,
            "avg_cost": round(self.avg_cost,3),
            "mid_price": mid,
            "unrealized": round(unreal,2),
            "realized": round(self.realized_pnl,2),
            "total": round(total,2)
        }

