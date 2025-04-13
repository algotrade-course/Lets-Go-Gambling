from matplotlib import dates, pyplot as plt
from data_accessing import get_db_connection

def visualization(df, future_code, buy_orders, sell_orders, pnl_over_time):
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
    plt.title("PnL Over Time for {future_code}")
    plt.gca().xaxis.set_major_formatter(dates.DateFormatter('%Y-%m-%d %H:%M'))
    plt.gca().xaxis.set_major_locator(dates.AutoDateLocator())
    plt.legend()
    plt.grid()
    plt.show(block=False)

def report(total_trades, match_trades, pnl):
    print("\n ### Backtest Complete! ###")
    print(f" Total Orders Placed: {total_trades}")
    print(f" Total Trades: {match_trades}")
    print(f" Net PnL: {100000*pnl:.2f} dong")

def fetch_data(future_code, start_date, end_date):
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
                return cur.fetchall()
    except Exception as e:
        print(f" Error loading historical data: {e}")
        return None