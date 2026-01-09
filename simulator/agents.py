import random

class MarketMaker:
    def __init__(self, spread=2, size=5):
        """
        Simple symmetric market maker posting around the mid price.
        spread: number of ticks away from mid for bid/ask
        size:   quantity posted at each level
        """
        self.spread = spread
        self.size = size

    def generate(self, mid):
        # enforce integer ticks for quotes
        mid_int = int(round(mid))
        bid = mid_int - self.spread
        ask = mid_int + self.spread
        return [
            ("buy", self.size, bid),
            ("sell", self.size, ask),
        ]


class NoiseTrader:
    def __init__(self, intensity=0.3, max_size=5):
        """
        Random liquidity taker. With probability = intensity, submits
        a buy or sell marketable order around the mid price.
        """
        self.intensity = intensity
        self.max_size = max_size

    def generate(self, mid):
        if random.random() >= self.intensity:
            return []

        side = random.choice(["buy", "sell"])
        qty = random.randint(1, self.max_size)
        price = int(round(mid))  # trade at mid in ticks
        return [(side, qty, price)]


class InformedTrader:
    def __init__(self, alpha_prob=0.1, size=3):
        """
        Informed-ish trader: occasionally submits a larger order
        at the mid price. Direction is still random in this MVP.
        """
        self.alpha_prob = alpha_prob
        self.size = size

    def generate(self, mid):
        if random.random() >= self.alpha_prob:
            return []

        side = random.choice(["buy", "sell"])
        price = int(round(mid))  # trade at mid in ticks
        return [(side, self.size, price)]
