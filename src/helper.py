from matplotlib import dates, pyplot as plt
import pandas as pd
from src.settings import DATA_PATH_ROOT
import os

def visualization(df, future_code, buy_orders, sell_orders, pnl_over_time, asset_over_time):
    # Plot asset overtime
    asset_df = pd.DataFrame(asset_over_time, columns=["timestamp", "asset"])
    plt.figure(figsize=(12, 6))
    plt.plot(asset_df["timestamp"], asset_df["asset"], label="Asset Value", color="blue")
    plt.xlabel("Date")
    plt.ylabel("Asset")
    plt.title(f"Asset Over Time for {future_code}")
    plt.gca().xaxis.set_major_formatter(dates.DateFormatter('%Y-%m-%d %H:%M'))
    plt.gca().xaxis.set_major_locator(dates.AutoDateLocator())
    plt.ylim(bottom=0)
    plt.legend()
    plt.grid()
    plt.savefig(os.path.join(DATA_PATH_ROOT, f"asset_over_time.png"))
    
    # Plot market price with buy/sell orders
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
    plt.savefig(os.path.join(DATA_PATH_ROOT, f"backtest_results.png"))
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
    plt.savefig(os.path.join(DATA_PATH_ROOT, f"pnl_over_time.png"))

def report(total_trades, match_trades, pnl, sharpe, max_drawdown, asset):
    print(f"\n ### Backtest Complete! ###")
    print(f" Total Orders Placed: {total_trades}")
    print(f" Total Trades: {match_trades}")
    print(f" Net PnL: {100000*pnl:.0f} đồng")
    print(f" Sharpe Ratio: {sharpe:.4f}")
    print(f" Maximum Drawdown: {max_drawdown:.8f}")
    print(f" Final Asset Value: {100000*asset:.0f} đồng")
