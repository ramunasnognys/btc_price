import requests
import time
from datetime import datetime

def get_bitcoin_price():
    """Fetch current Bitcoin price from CoinGecko API"""
    try:
        # CoinGecko API endpoint for Bitcoin price in USD
        url = 'https://api.coingecko.com/api/v3/simple/price'
        params = {
            'ids': 'bitcoin',
            'vs_currencies': 'usd',
            'include_24hr_change': 'true',
            'include_last_updated_at': 'true'
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        data = response.json()
        price = data['bitcoin']['usd']
        change_24h = data['bitcoin']['usd_24h_change']
        last_updated = datetime.fromtimestamp(data['bitcoin']['last_updated_at'])
        
        return {
            'price': price,
            'change_24h': round(change_24h, 2),
            'last_updated': last_updated
        }
        
    except requests.exceptions.RequestException as e:
        print(f'Error fetching Bitcoin price: {e}')
        return None

def main():
    """Main function to demonstrate the usage"""
    while True:
        btc_data = get_bitcoin_price()
        
        if btc_data:
            print('\nBitcoin Price Information:')
            print(f'Current Price: ${btc_data["price"]:,.2f}')
            print(f'24h Change: {btc_data["change_24h"]}%')
            print(f'Last Updated: {btc_data["last_updated"].strftime("%Y-%m-%d %H:%M:%S")}')
        
        # Wait for 60 seconds before the next update
        print('\nWaiting 60 seconds for next update...')
        time.sleep(60)

if __name__ == '__main__':
    print('Starting Bitcoin Price Tracker...')
    try:
        main()
    except KeyboardInterrupt:
        print('\nBitcoin Price Tracker stopped.')