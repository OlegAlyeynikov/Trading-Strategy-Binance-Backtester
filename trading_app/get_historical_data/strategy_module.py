import json
import os
from jsonschema import validate, ValidationError

schema_path = os.path.join(os.path.dirname(__file__), 'strategy_schema.json')

if not os.path.exists(schema_path):
    raise FileNotFoundError(f"Schema file not found at path: {schema_path}")

with open(schema_path, 'r') as schema_file:
    try:
        schema = json.load(schema_file)
    except json.JSONDecodeError as e:
        raise ValueError(f"Error reading JSON schema file: {e}")


def validate_strategy(strategy):
    try:
        validate(instance=strategy, schema=schema)
        return True, None
    except ValidationError as e:
        return False, e.message


def load_strategy(filename):
    with open(filename, 'r') as file:
        strategy = json.load(file)

    is_valid, error_message = validate_strategy(strategy)
    if is_valid:
        return strategy
    else:
        raise ValueError(f"Invalid strategy configuration: {error_message}")


def save_strategy(strategy, filename):
    is_valid, error_message = validate_strategy(strategy)
    if is_valid:
        with open(filename, 'w') as file:
            json.dump(strategy, file, indent=4)
    else:
        raise ValueError(f"Invalid strategy configuration: {error_message}")


# Example usage
if __name__ == "__main__":
    strategy = {
        "market": "Crypto",
        "exchange": "Binance",
        "assets": ["BTC", "ETH", "SOL", "DOGE", "XRP", "MATIC"],
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
        "timeframe": "1m",
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

    # Save the strategy to a file
    save_strategy(strategy, '/code/trading_app/get_historical_data/strategy.json')

    # Load the strategy from the file
    loaded_strategy = load_strategy('/code/trading_app/get_historical_data/strategy.json')
    print(loaded_strategy)
