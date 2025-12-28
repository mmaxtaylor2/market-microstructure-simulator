print(">>> MARKET MICROSTRUCTURE SIMULATOR LAUNCHING <<<")

from exchange import Exchange
import csv, os, matplotlib.pyplot as plt

# Make sure data folder exists
if not os.path.exists("data"):
    os.makedirs("data")

# Initialize CSV logs
with open("data/book_snapshots.csv", "w", newline="") as f:
    csv.writer(f).writerow(["step","mid","spread","bid_depth","ask_depth","shock","vwap"])

with open("data/trades.csv", "w", newline="") as f:
    csv.writer(f).writerow(["step","price","size","vwap"])


def run_simulation(steps=20):
    ex = Exchange(vol=0.25)
    mid_series, spread_series, shock_series = [], [], []

    for step in range(1, steps+1):

        result = ex.step(step)

        # log book state
        with open("data/book_snapshots.csv", "a", newline="") as f:
            csv.writer(f).writerow([
                result["step"], result["mid"], result["spread"],
                result["bid_depth"], result["ask_depth"],
                result["shock"], result["vwap"]
            ])

        # log trade executions
        if result["trades"]:
            for price, size in result["trades"]:
                with open("data/trades.csv", "a", newline="") as f:
                    csv.writer(f).writerow([result["step"], price, size, result["vwap"]])

        print(f"Step {step} | mid={result['mid']} | spread={result['spread']} | shock={result['shock']}")

        mid_series.append(result["mid"])
        spread_series.append(result["spread"])
        shock_series.append(result["shock"])

    # --------- Graphs ----------
    plt.figure(figsize=(12,5))
    plt.plot(mid_series)
    plt.scatter(
        [i for i,x in enumerate(shock_series) if x],
        [mid_series[i] for i,x in enumerate(shock_series) if x],
        marker="X", s=100
    )
    plt.title("Mid Price Over Time (Shocks Marked)")
    plt.xlabel("Step")
    plt.show()

    plt.figure(figsize=(12,5))
    plt.plot(spread_series, color="red")
    plt.title("Spread Over Time")
    plt.xlabel("Step")
    plt.show()

    print("\n>>> SIMULATION COMPLETE — DATA LOGGED TO /data <<<")


if __name__ == "__main__":
    run_simulation(steps=20)
    print(">>> END <<<")

