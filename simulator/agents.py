import random

class MarketMaker:
    def __init__(self, spread=2, size=5):
        self.spread = spread
        self.size = size

    def generate_orders(self, mid):
        """
        Posts liquidity on both sides around midprice.
        """
        return [
            ("buy", self.size, mid - self.spread),
            ("sell", self.size, mid + self.spread),
        ]


class NoiseTrader:
    def __init__(self, intensity=0.3):
        self.intensity = intensity

    def generate_orders(self, mid):
        if random.random() < self.intensity:
            side = random.choice(["buy", "sell"])
            return [(side, random.randint(1, 5), mid)]
        return []


class InformedTrader:
    def __init__(self, alpha_prob=0.1, alpha_size=3):
        self.alpha_prob = alpha_prob
        self.alpha_size = alpha_size

    def generate_orders(self, mid):
        if random.random() < self.alpha_prob:
            # informed trader "knows" direction
            side = random.choice(["buy", "sell"])
            return [(side, self.alpha_size, mid)]
        return []
