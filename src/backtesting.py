from matplotlib import dates
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from data_accessing import get_db_connection
from evaluation_metrics import sharpe_ratio, maximum_drawdown

default = {
    "future_code" : "VN30F1M",
    "order_size" : 1,
    "spread" : 0.2/100,
    "wait_time" : 1800,
    "START_DATE" : "2024-12-02",
    "END_DATE" : "2024-12-03",
}

def backtest(future_code, order_size, spread, wait_time, START_DATE, END_DATE):
    print(f"### Running Backtest for {future_code} from {START_DATE} to {END_DATE}... ###")

    try:
        start_date = datetime.strptime(START_DATE, "%Y-%m-%d")
        end_date = datetime.strptime(END_DATE, "%Y-%m-%d")
    except ValueError:
        print(" Invalid date format! Use YYYY-MM-DD.")
        return

    # Load historical data
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT DISTINCT m.datetime, m.price 
                    FROM "quote"."matched" AS m
                    JOIN (
                        SELECT DISTINCT tickersymbol
                        FROM "quote"."futurecontractcode"
                        WHERE futurecode = %s
                        AND datetime BETWEEN %s AND %s
                    ) AS f
                    ON m.tickersymbol = f.tickersymbol
                    WHERE m.datetime BETWEEN %s AND %s
                    ORDER BY m.datetime ASC;
                    """, 
                    (future_code, start_date, end_date, start_date, end_date)
                )
                result = cur.fetchall()
    except Exception as e:
        print(f" Error loading historical data: {e}")
        return

    if not result:
        print(" No historical data found.")
        return

    print(f"### Loaded {len(result)} data points for backtesting. ###")
    # Convert result to DataFrame
    df = pd.DataFrame(result, columns=["datetime", "price"])
    df["datetime"] = pd.to_datetime(df["datetime"])

    # sharp ratio
    period_returns = df["price"].pct_change().dropna().tolist()
    risk_free_return = 0
    sharpe = sharpe_ratio(period_returns, risk_free_return)
    print(f" Sharpe Ratio: {sharpe:.2f}")

    # Maximum Drawdown
    max_drawdown = maximum_drawdown(period_returns)
    print(f" Maximum Drawdown: {max_drawdown:.2f}")

    total_trades = 0
    pnl = 0
    active_orders = []
    match_order = []
    buy_orders = []
    sell_orders = []
    pnl_over_time = []

    for index, row in df.iterrows():

        timestamp = row["datetime"]
        price = float(row["price"])

        # Calculate buy/sell prices
        buy_price = price * (1 - spread)
        sell_price = price * (1 + spread)

        # Check for execution of active orders, wait for matched
        executed_orders = []
        for order in active_orders[:]:
            order_type, order_price, order_size, order_time = order
            if (order_type == "BUY" and price <= order_price) or (order_type == "SELL" and price >= order_price):
                if order_type == "BUY" and price <= order_price:
                    match_order.append((timestamp, "BUY", price, order_size, order_time))
                elif order_type == "SELL" and price >= order_price:
                    match_order.append((timestamp, "SELL", price, order_size, order_time))
                executed_orders.append(order)
        
        for order in executed_orders:
            active_orders.remove(order)

        # Cancel orders if wait time exceeded
        for order in active_orders[:]:
            order_time = order[3]
            if timestamp - order_time >= timedelta(seconds=wait_time):
                active_orders.remove(order)

        # Place new buy/sell orders only if no open waiting positions, close all open positions
        if not active_orders:
            for order in match_order:
                match_time, match_type, match_price, match_size, match_order_time = order
                if match_type == "BUY":
                    pnl += match_size * (price - match_price)
                else:
                    pnl += match_size * (match_price - price)
            match_order.clear()

            active_orders.append(("BUY", buy_price, order_size, timestamp))
            active_orders.append(("SELL", sell_price, order_size, timestamp))
            buy_orders.append((timestamp, buy_price))
            sell_orders.append((timestamp, sell_price))
            total_trades += 2

        pnl_over_time.append(pnl)

    # Visualization
    # plot price and orders
    plt.figure(figsize=(12, 6))
    plt.plot(df["datetime"], df["price"], label="Market Price", color="blue")

    if buy_orders:
        buy_times, buy_prices = zip(*buy_orders)
        plt.scatter(buy_times, buy_prices, color="green", marker="^", label="Buy Orders")
    if sell_orders:
        sell_times, sell_prices = zip(*sell_orders)
        plt.scatter(sell_times, sell_prices, color="red", marker="v", label="Sell Orders")

    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.title(f"Backtest Results for {future_code}")
    plt.gca().xaxis.set_major_formatter(dates.DateFormatter('%Y-%m-%d %H:%M')) 
    plt.gca().xaxis.set_major_locator(dates.AutoDateLocator())

    plt.legend()
    plt.grid()
    plt.show(block=False)
    plt.pause(0.1)

    # plot pnl over time
    plt.figure(figsize=(12, 6))
    plt.plot(df["datetime"], pnl_over_time, label="PnL", color="green")
    plt.xlabel("Date")
    plt.ylabel("PnL")
    plt.title(f"PnL Over Time for {future_code}")
    plt.gca().xaxis.set_major_formatter(dates.DateFormatter('%Y-%m-%d %H:%M'))
    plt.gca().xaxis.set_major_locator(dates.AutoDateLocator())
    plt.legend()
    plt.grid()
    plt.show(block=False)

    # Final report
    print(f"\n ### Backtest Complete! ###")
    print(f" Total Trades: {total_trades}")
    print(f" Net PnL: ${pnl:.2f}")

def data_search(future_code,start_date,end_date):
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT tickersymbol 
                FROM "quote"."futurecontractcode" 
                WHERE futurecode = %s 
                AND datetime BETWEEN %s AND %s
                """, 
                (future_code, start_date, end_date)
            )
            result = cur.fetchall()
            print(result)

if __name__ == "__main__":
    backtest(**default)
    #data_search("VN30F1M","2022-01-01","2022-02-27")
    input("\nPress Enter to exit...")