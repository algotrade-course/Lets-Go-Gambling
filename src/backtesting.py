from matplotlib import dates
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from data_accessing import get_db_connection

default = {
    "future_code" : "VN30F1M",
    "order_size" : 1,
    "spread" : 0.2/100,
    "wait_time" : 720,
    "START_DATE" : "2022-01-05",
    "END_DATE" : "2022-01-08",
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

    total_trades = 0
    pnl = 0
    active_orders = []  # Track active orders
    buy_orders = []
    sell_orders = []

    for index, row in df.iterrows():
        timestamp = row["datetime"]
        price = float(row["price"])

        # Calculate buy/sell prices
        buy_price = price * (1 - spread)
        sell_price = price * (1 + spread)

        # Check for execution of active orders
        for order in active_orders:
            order_type, order_price, order_size, order_time = order
            if (order_type == "BUY" and price <= order_price) or (order_type == "SELL" and price >= order_price):
                if order_type == "BUY":
                    pnl += (price - order_price) * order_size
                else:
                    pnl += (order_price - price) * order_size
                active_orders.remove(order)

        # Cancel orders if wait time exceeded
        for order in active_orders:
            order_time = order[3]
            if timestamp - order_time >= timedelta(seconds=wait_time):
                active_orders.remove(order)

        # Place new buy/sell orders only if no open positions
        if not active_orders:
            active_orders.append(("BUY", buy_price, order_size, timestamp))
            active_orders.append(("SELL", sell_price, order_size, timestamp))
            buy_orders.append((timestamp, buy_price))
            sell_orders.append((timestamp, sell_price))
            total_trades += 2

    # Visualization
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

    # Format X-axis for better readability
    plt.xticks(rotation=45)  # Rotate for better visibility
    plt.gca().xaxis.set_major_formatter(dates.DateFormatter('%Y-%m-%d %H:%M'))  # Custom format
    plt.gca().xaxis.set_major_locator(dates.AutoDateLocator())  # Auto spacing

    plt.legend()
    plt.grid()
    plt.show()

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