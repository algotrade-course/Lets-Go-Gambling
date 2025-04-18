import pandas as pd
from datetime import datetime, timedelta
from src.evaluation_metrics import sharpe_ratio, maximum_drawdown
from src.helper import report, visualization
from src.settings import pre_optimization_params, in_sample_data, in_sample_params

class MarketMaker:
    def __init__(self, order_size, spread, wait_time, sample_data=None,
                 future_code="UNKNOWN", START_DATE="N/A", END_DATE="N/A"):
        self.order_size = order_size
        self.spread = spread
        self.wait_time = wait_time
        self.sample_data = sample_data
        self.future_code = future_code
        self.START_DATE = START_DATE
        self.END_DATE = END_DATE

    def run(self):
        print(f"\n### Running MarketMaking for {self.future_code} from {self.START_DATE} to {self.END_DATE}... ###")

        # Validate dates
        try:
            start_date = datetime.strptime(self.START_DATE, "%Y-%m-%d")
            end_date = datetime.strptime(self.END_DATE, "%Y-%m-%d")
        except ValueError:
            print(" Invalid date format! Use YYYY-MM-DD.")
            return

        if not self.sample_data:
            print(" No historical data found.")
            return

        print(f"### Loaded {len(self.sample_data)} data points for backtesting. ###")

        # Load into DataFrame
        self.df = pd.DataFrame(self.sample_data, columns=["datetime", "price"])
        self.df["datetime"] = pd.to_datetime(self.df["datetime"])

        # Evaluation metrics
        returns = self.df["price"].pct_change().dropna().tolist()
        self.sharpe = sharpe_ratio(returns, risk_free_return=0)
        self.max_drawdown = maximum_drawdown(returns)

        print(f" Sharpe Ratio: {self.sharpe:.2f}")
        print(f" Maximum Drawdown: {self.max_drawdown:.2f}")

        # Simulation state
        self.total_trades = 0
        self.match_trades = 0
        self.pnl = 0
        self.pnl_over_time = []
        self.buy_orders = []
        self.sell_orders = []

        active_orders = []
        matched_orders = []

        for _, row in self.df.iterrows():
            timestamp, price = row["datetime"], float(row["price"])

            # Execute matched orders
            executed = []
            for order in active_orders:
                o_type, o_price, o_size, o_time = order
                if (o_type == "BUY" and price <= o_price) or (o_type == "SELL" and price >= o_price):
                    matched_orders.append((timestamp, o_type, price, o_size, o_time))
                    self.match_trades += 1
                    executed.append(order)
            for order in executed:
                active_orders.remove(order)

            # Cancel stale orders
            active_orders = [
                o for o in active_orders
                if timestamp - o[3] < timedelta(seconds=self.wait_time)
            ]

            # Place new orders if all matched
            if not active_orders:
                for match in matched_orders:
                    _, m_type, m_price, m_size, _ = match
                    pnl = m_size * (price - m_price) if m_type == "BUY" else m_size * (m_price - price)
                    self.pnl += pnl
                matched_orders.clear()

                # Place new buy/sell orders
                buy_price = price * (1 - self.spread)
                sell_price = price * (1 + self.spread)

                active_orders.append(("BUY", buy_price, self.order_size, timestamp))
                active_orders.append(("SELL", sell_price, self.order_size, timestamp))

                self.buy_orders.append((timestamp, buy_price))
                self.sell_orders.append((timestamp, sell_price))
                self.total_trades += 2

            self.pnl_over_time.append(self.pnl)

        return self.get_results()

    def get_results(self):
        return {
            "total_trades": self.total_trades,
            "match_trades": self.match_trades,
            "pnl": self.pnl,
            "pnl_over_time": self.pnl_over_time,
            "sharpe_ratio": self.sharpe,
            "maximum_drawdown": self.max_drawdown,
        }

    def full_run(self):
        self.run()
        visualization(self.df, self.future_code, self.buy_orders, self.sell_orders, self.pnl_over_time)
        report(self.total_trades, self.match_trades, self.pnl)
        return self.get_results()


if __name__ == "__main__":
    MarketMaker(
        **pre_optimization_params,
        sample_data=in_sample_data,
        future_code=in_sample_params["future_code"],
        START_DATE=in_sample_params["START_DATE"],
        END_DATE=in_sample_params["END_DATE"]
    ).full_run()

    input("\nPress Enter to exit...")
