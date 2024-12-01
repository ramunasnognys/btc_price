# Bitcoin Price Tracker

A simple Python script that fetches real-time Bitcoin price data using the CoinGecko API. The script provides current price, 24-hour price change, and last updated timestamp.

## Features

- Real-time Bitcoin price in USD
- 24-hour price change percentage
- Last updated timestamp
- Automatic updates every 60 seconds
- Error handling for API requests

## Requirements

- Python 3.6 or higher
- `requests` library

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/ramunasnognys/btc_price.git
   cd btc_price
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the script:
```bash
python btc_price.py
```

The script will start fetching Bitcoin price data and update it every 60 seconds. To stop the script, press `Ctrl+C`.

## Sample Output

```
Starting Bitcoin Price Tracker...

Bitcoin Price Information:
Current Price: $37,245.67
24h Change: -2.14%
Last Updated: 2024-12-01 05:13:45

Waiting 60 seconds for next update...
```

## API Reference

This script uses the [CoinGecko API](https://www.coingecko.com/en/api) to fetch Bitcoin price data. The API is free to use and doesn't require authentication for basic endpoints.

## License

This project is open source and available under the MIT License.