# Bitcoin Price Fetcher

A simple Python script that fetches the current Bitcoin price using the CoinGecko API. Supports multiple currencies including USD and NOK (Norwegian Krone).

## Features

- Fetches real-time Bitcoin price in multiple currencies (USD, NOK)
- Shows 24-hour price change percentage for each currency
- Displays last updated timestamp
- Proper currency formatting for each supported currency
- Error handling for API requests

## Requirements

- Python 3.6+
- requests library

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

Simply run the script:
```bash
python btc_price.py
```

The script will display:
- Current Bitcoin price in USD and NOK
- 24-hour price change for each currency
- Last updated time

### Sample Output
```
Bitcoin Price Information:
Last Updated: 2024-12-16 08:45:00

Price (USD): $42,123.45
24h Change: -2.15%

Price (NOK): 445,678.90 kr
24h Change: -2.15%
```

## API Reference

This project uses the [CoinGecko API](https://www.coingecko.com/en/api) to fetch Bitcoin price data.

## License

MIT