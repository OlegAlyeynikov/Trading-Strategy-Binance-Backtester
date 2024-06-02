# Trading Strategy Binance Backtester

This project is a trading strategy backtester using historical data from Binance. It includes a Django web application and a PostgreSQL database, both running in Docker containers. The backtester simulates trading strategies on historical data and generates reports and graphs to visualize the performance.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Building the Docker Project](#building-the-docker-project)
3. [Downloading Historical Data from Binance](#downloading-historical-data-from-binance)
4. [Running the Backtester](#running-the-backtester)
5. [Generating Reports and Graphs](#generating-reports-and-graphs)

## Getting Started

### Prerequisites

- Docker
- Docker Compose

Ensure you have Docker and Docker Compose installed on your system.

### Cloning the Repository

Clone the repository to your local machine:

```
git clone https://github.com/yourusername/trading-backtester.git
cd trading-backtester
```

## Building the Docker Project

### Step 1: Build Docker Images

Build the Docker images for the Django application and PostgreSQL database:

> docker-compose build
> docker-compose up -d

### Step 2: Apply Migrations

Apply Django migrations to set up the database schema:

> docker-compose run web python manage.py migrate

> docker-compose run web python manage.py makemigrations /code/trading_app

> docker-compose run web python manage.py migrate /code/trading_app

### Step 3: Create Superuser

(Optional) Create a Django superuser to access the Django admin interface:

> docker-compose run web python manage.py createsuperuser

## Downloading Historical Data from Binance

### Step 1: Create .env File

Edit example.env file or create a new .env file in the project root directory with the following content:

> POSTGRES_DB=trading_db
> 
> POSTGRES_USER=trading_user
> 
> POSTGRES_PASSWORD=trading_password
> 
> DB_HOST=db
> 
> DB_PORT=5432
> 
> DJANGO_SECRET_KEY=generate_your_django_secret_key
> 
> BINANCE_API_KEY=your_binance_api_key
> 
> BINANCE_API_SECRET=your_binance_api_secret

### Step 2: Run the Data Fetching Script

Run the script to download historical data from Binance:

> docker-compose run web python /code/trading_app/get_historical_data/fetch_historical_data.py

This script will download historical data and store it in the PostgreSQL database.

## Running the Backtester
Step 1: Prepare the Strategy File

Use existing or edit a strategy file in /project_root_directory/trading_app/get_historical_data/strategy.json. Here's an example of the content:

```
{
  "market": "Crypto",
  "exchange": "Binance",
  "assets": ["BTCUSDT", "ETHUSDT", "SOLUSDT", "DOGEUSDT", "XRPUSDT", "MATICUSDT"],
  "instrument": "Futures",
  "date_range": {
    "start": "2022-01-01",
    "end": "2024-06-01"
  },
  "balance": {
    "min": 5,
    "max": 1000000
  },
  "investment": {
    "min": 5,
    "max": 100000
  },
  "leverage": {
    "min": 1,
    "max": 100
  },
  "timeframe": "1min",
  "opening_parameters": {
    "long_period": 50,
    "short_period": 20,
    "long_price_diff": 1.0,
    "short_price_diff": 0.5,
    "order_price_increase_limit": 2.0,
    "order_execution_time_limit": 60
  },
  "closing_parameters": {
    "long": {
      "takeprofit": 10.0,
      "stoploss": 5.0,
      "trailingstoploss": 2.0,
      "delay_next_order": 5
    },
    "short": {
      "takeprofit": 10.0,
      "stoploss": 5.0,
      "trailingstoploss": 2.0,
      "hold_next_order": 5
    }
  }
}
```

### Step 2: Run the Backtester Script

Run the backtester script to simulate trading and generate reports:

> docker-compose run web python /code/trading_app/get_historical_data/backtester.py

## Generating Reports and Graphs

The backtester script will generate CSV reports and balance history graphs for each asset in the strategy. The CSV reports and graphs will be saved in the project directory.
Example Output

    backtest_report_BTCUSDT_20240602132745.csv

    backtest_report_BTCUSDT_20240602132745.png

These files contain detailed trade logs and visualizations of the balance changes over time.
