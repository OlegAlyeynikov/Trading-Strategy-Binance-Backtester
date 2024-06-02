import os
import pandas as pd
import logging
from binance.client import Client
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('BINANCE_API_KEY')
API_SECRET = os.getenv('BINANCE_API_SECRET')

DB_USER = os.getenv('POSTGRES_USER')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('POSTGRES_DB')

client = Client(API_KEY, API_SECRET)

engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def fetch_and_store_historical_data(symbol, interval, start_str, end_str=None):
    logging.info(f"Fetching historical data for {symbol}...")

    klines = client.get_historical_klines(symbol, interval, start_str, end_str)
    logging.info(f"Fetched {len(klines)} records for {symbol}.")

    columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time',
               'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume',
               'taker_buy_quote_asset_volume', 'ignore']
    data = pd.DataFrame(klines, columns=columns)

    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
    data['close_time'] = pd.to_datetime(data['close_time'], unit='ms')

    logging.info(f"Inserting data into PostgreSQL for {symbol}...")

    data.to_sql(f'{symbol}_{interval}', engine, if_exists='replace', index=False)

    logging.info(f"Data insertion completed for {symbol}.")


if __name__ == "__main__":
    symbols = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'DOGEUSDT', 'XRPUSDT', 'MATICUSDT']
    interval = Client.KLINE_INTERVAL_1MINUTE
    start_str = '1 Jan 2022'
    end_str = '1 Jun 2024'

    for symbol in symbols:
        fetch_and_store_historical_data(symbol, interval, start_str, end_str)
