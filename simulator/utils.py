def ladder_view(depth):
    """
    Convert raw depth dict into sorted bid/ask ladders with integer prices.

    Returns:
        bids: list of (price, size) sorted descending by price
        asks: list of (price, size) sorted ascending by price
    """
    raw_bids = depth.get("bids", {})
    raw_asks = depth.get("asks", {})

    bids = [(int(p), q) for p, q in raw_bids.items()]
    asks = [(int(p), q) for p, q in raw_asks.items()]

    bids_sorted = sorted(bids, key=lambda x: -x[0])
    asks_sorted = sorted(asks, key=lambda x: x[0])

    return bids_sorted, asks_sorted
