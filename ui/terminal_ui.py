# ui/terminal_ui.py
from exchange import Exchange
import sys

class TerminalUI:
    def __init__(self):
        self.exchange = Exchange()
        self.running = True
        self.bots_enabled = True

    # ------------------------------------------------------------
    # MAIN LOOP
    # ------------------------------------------------------------
    def run(self):
        while self.running:
            self.show_menu()
            choice = input("Enter choice: ").strip()

            if choice == "1":
                self.show_order_book()
            elif choice == "2":
                self.place_order()
            elif choice == "3":
                self.advance_step()
            elif choice == "4":
                self.view_pnl()
            elif choice == "5":
                self.toggle_bots()
            elif choice == "6":
                self.quit()
            else:
                print("Invalid choice. Try again.\n")

    # ------------------------------------------------------------
    # MENU
    # ------------------------------------------------------------
    def show_menu(self):
        print("""
============================================================
 MARKET MICROSTRUCTURE SIMULATOR — INTERACTIVE TERMINAL
============================================================
(1) View Order Book
(2) Place Order (Market / Limit)
(3) Advance Simulation Step
(4) View PnL & Recent Trades
(5) Toggle Bots (On/Off)
(6) Quit
------------------------------------------------------------
        """)

    # ------------------------------------------------------------
    # ORDER BOOK
    # ------------------------------------------------------------
    def show_order_book(self):
        snapshot = self.exchange.get_snapshot(levels=5)
        print("\n--- ORDER BOOK (Top Levels) ---")
        print("BID                 | ASK")
        print("----------------------------------------")

        for i in range(5):
            bid = snapshot["bids"][i] if i < len(snapshot["bids"]) else ("-", "-")
            ask = snapshot["asks"][i] if i < len(snapshot["asks"]) else ("-", "-")
            print(f"{bid[1]:>4}@{bid[0]:<8}     | {ask[0]:<8}@{ask[1]:>4}")

        print("----------------------------------------\n")

    # ------------------------------------------------------------
    # ORDER ENTRY
    # ------------------------------------------------------------
    def place_order(self):
        print("\n--- PLACE ORDER ---")
        side = input("Side (buy/sell): ").strip().lower()
        kind = input("Type (market/limit): ").strip().lower()
        qty  = int(input("Quantity: ").strip())

        price = None
        if kind == "limit":
            price = float(input("Limit Price: ").strip())

        result = self.exchange.submit_order(side, qty, kind, price)
        print("Order Response:", result, "\n")

    # ------------------------------------------------------------
    # SIM STEP
    # ------------------------------------------------------------
    def advance_step(self):
        result = self.exchange.step(bots=self.bots_enabled)
        print("\n--- MARKET UPDATED ---")
        print(f"Step       : {result['step']}")
        print(f"Mid-Price  : {result['mid']}")
        print(f"Spread     : {result['spread']}")
        print(f"Position   : {result['position']}")
        print(f"Realized   : {result['realized']}")
        print("------------------------------------------------------------\n")

    # ------------------------------------------------------------
    # PNL VIEW
    # ------------------------------------------------------------
    def view_pnl(self):
        report = self.exchange.pnl_report()

        print("\n--- PnL REPORT ---")
        print(f"Position     : {report['position']} shares")
        print(f"Avg Cost     : {report['avg_cost']}")
        print(f"Mid Price    : {report['mid_price']}")
        print(f"Unrealized   : {report['unrealized']}")
        print(f"Realized     : {report['realized']}")
        print("-----------------------------------")
        print(f"TOTAL PnL    : {report['total']}")
        print("-----------------------------------")

        print("\n--- RECENT TRADES ---")
        trades = self.exchange.trade_log[-10:]
        if not trades:
            print("No trades yet.")
        else:
            for trade in trades:
                print(trade)
        print("\n")

    # ------------------------------------------------------------
    # BOT TOGGLE
    # ------------------------------------------------------------
    def toggle_bots(self):
        self.bots_enabled = not self.bots_enabled
        print(f"\nBots Enabled: {self.bots_enabled}\n")

    # ------------------------------------------------------------
    # EXIT
    # ------------------------------------------------------------
    def quit(self):
        print("\nExiting simulator...")
        self.running = False
        sys.exit()

# ------------------------------------------------------------
# LAUNCH
# ------------------------------------------------------------
if __name__ == "__main__":
    TerminalUI().run()

