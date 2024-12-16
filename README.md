# Bitcoin Price Fetcher

A simple Python script that fetches the current Bitcoin price using the CoinGecko API.

## Features

- Fetches real-time Bitcoin price in USD
- Shows 24-hour price change percentage
- Displays last updated timestamp
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

The script will display the current Bitcoin price, 24-hour price change, and last updated time.

## API Reference

This project uses the [CoinGecko API](https://www.coingecko.com/en/api) to fetch Bitcoin price data.

## License

MIT