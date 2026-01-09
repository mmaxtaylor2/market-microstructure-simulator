import random

class MarketMaker:
    def __init__(self, spread=2, size=5):
        self.spread = spread
        self.size = size

    def generate(self, mid):
        bid = int(mid - self.spread)
        ask = int(mid + self.spread)
        return [
            ("buy", self.size, bid),
            ("sell", self.size, ask)
        ]


class NoiseTrader:
    def __init__(self, intensity=0.3, max_size=5):
        self.intensity = intensity
        self.max_size = max_size

    def generate(self, mid):
        if random.random() < self.intensity:
            side = random.choice(["buy", "sell"])
            return [(side, random.randint(1, self.max_size), mid)]
        return []


class InformedTrader:
    def __init__(self, alpha_prob=0.1, size=3):
        self.alpha_prob = alpha_prob
        self.size = size

    def generate(self, mid):
        if random.random() < self.alpha_prob:
            side = random.choice(["buy", "sell"])
            return [(side, self.size, mid)]
        return []
