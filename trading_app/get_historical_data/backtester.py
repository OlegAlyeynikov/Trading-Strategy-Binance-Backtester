import os
import pandas as pd
import logging
from sqlalchemy import create_engine
from tqdm import tqdm
from dotenv import load_dotenv
from datetime import datetime
import json
import matplotlib.pyplot as plt

load_dotenv()

DB_USER = os.getenv('POSTGRES_USER')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('POSTGRES_DB')

engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def fetch_historical_data(symbol, interval):
    logging.info(f"Fetching historical data for {symbol}...")
    table_name = f'"{symbol}USDT_{interval}"'
    query = f"SELECT * FROM {table_name}"
    data = pd.read_sql(query, engine)
    data['timestamp'] = pd.to_datetime(data['timestamp'])
    data['close'] = data['close'].astype(float)
    return data


def simulate_trading(data, strategy):
    logging.info("Starting trading simulation...")
    initial_balance = strategy['balance']['min']
    balance = initial_balance
    trades = []
    balance_history = []

    position = None
    entry_price = 0

    for i in tqdm(range(len(data))):
        row = data.iloc[i]

        if position is None and i % 100 == 0:
            position = 'buy'
            entry_price = row['close']
            continue

        if position == 'buy' and i % 100 == 50:
            exit_price = row['close']
            profit = exit_price - entry_price
            balance += profit
            trade = {
                'timestamp': row['timestamp'],
                'symbol': strategy['assets'][0],
                'action': 'sell',
                'price': exit_price,
                'balance': balance,
                'profit': profit
            }
            trades.append(trade)
            balance_history.append(balance)

            position = None
            entry_price = 0

    logging.info("Trading simulation completed.")
    return trades, balance_history


def generate_report(trades, filename):
    logging.info(f"Generating report: {filename}")
    df = pd.DataFrame(trades)
    df.to_csv(filename, index=False)
    logging.info("Report generated.")


def plot_balance_history(balance_history, filename):
    plt.figure(figsize=(10, 5))
    plt.plot(balance_history, label='Balance Over Time')
    plt.xlabel('Trade Number')
    plt.ylabel('Balance')
    plt.title('Balance Changes Over Time')
    plt.legend()
    plt.grid(True)
    plot_filename = filename.replace('.csv', '.png')
    plt.savefig(plot_filename)
    plt.show()
    logging.info(f"Balance plot saved as {plot_filename}")


def load_strategy(filename):
    with open(filename, 'r') as file:
        strategy = json.load(file)
    return strategy


if __name__ == "__main__":
    strategy = load_strategy('/code/trading_app/get_historical_data/strategy.json')

    for symbol in strategy['assets']:
        interval = strategy['timeframe']
        data = fetch_historical_data(symbol, interval)
        trades, balance_history = simulate_trading(data, strategy)
        report_filename = f"backtest_report_{symbol}_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
        generate_report(trades, report_filename)
        plot_balance_history(balance_history, report_filename)
