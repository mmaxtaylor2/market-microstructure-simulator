def ladder_view(depth):
    bids = sorted(depth["bids"].items(), key=lambda x: -x[0])
    asks = sorted(depth["asks"].items(), key=lambda x: x[0])
    return bids, asks
