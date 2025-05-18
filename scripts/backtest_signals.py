# scripts/backtest_signals.py

import pandas as pd
import os

def backtest_signals(df, initial_cash=100000):
    df = df.sort_values("date").reset_index(drop=True)
    cash = initial_cash
    position = 0
    trades = []
    equity_curve = []

    for i in range(len(df)):
        row = df.iloc[i]
        signal = row.get("signal", "")
        price = row["close"]

        if signal == "buy" and cash >= price:
            position = cash / price
            cash = 0
            trades.append({"date": row["date"], "type": "buy", "price": price})
        elif signal == "sell" and position > 0:
            cash = position * price
            trades.append({"date": row["date"], "type": "sell", "price": price})
            position = 0

        equity_curve.append(cash + (position * price))

    df["equity"] = equity_curve
    returns = []
    for i in range(1, len(trades), 2):
        buy = trades[i - 1]["price"]
        sell = trades[i]["price"]
        returns.append((sell - buy) / buy * 100)

    summary = {
        "total_trades": len(returns),
        "win_rate": sum(r > 0 for r in returns) / len(returns) if returns else 0,
        "avg_return": sum(returns) / len(returns) if returns else 0,
        "final_equity": round(equity_curve[-1], 2)
    }

    return df, pd.DataFrame([summary])

if __name__ == "__main__":
    os.makedirs("backtest_results", exist_ok=True)
    symbols = ["ALIF", "EXIMBANK", "SEMLFBSLGF", "MAKSONSPIN"]

    for symbol in symbols:
        signal_file = f"signals/{symbol}_signals.csv"
        if not os.path.exists(signal_file):
            print(f"⚠️ File {signal_file} does not exist. Skipping...")
            continue

        df = pd.read_csv(signal_file, parse_dates=["date"])
        equity_df, summary_df = backtest_signals(df)
        equity_df.to_csv(f"backtest_results/{symbol}_equity.csv", index=False)
        summary_df.to_csv(f"backtest_results/{symbol}_summary.csv", index=False)
        print(f"✅ Backtest done for {symbol}")