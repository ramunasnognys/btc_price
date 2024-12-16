import requests
import json
from datetime import datetime

def get_btc_price():
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
        
        # Make the API request
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Parse the response
        data = response.json()
        
        # Extract the price information
        btc_data = data['bitcoin']
        price = btc_data['usd']
        price_change = btc_data['usd_24h_change']
        last_updated = datetime.fromtimestamp(btc_data['last_updated_at'])
        
        return {
            'price': price,
            'price_change_24h': price_change,
            'last_updated': last_updated
        }
        
    except requests.exceptions.RequestException as e:
        print(f'Error fetching Bitcoin price: {e}')
        return None
    except (KeyError, json.JSONDecodeError) as e:
        print(f'Error parsing response: {e}')
        return None

def main():
    """Main function to demonstrate the Bitcoin price fetcher"""
    btc_data = get_btc_price()
    
    if btc_data:
        print('\nBitcoin Price Information:')
        print(f'Current Price: ${btc_data["price"]:,.2f}')
        print(f'24h Change: {btc_data["price_change_24h"]:,.2f}%')
        print(f'Last Updated: {btc_data["last_updated"].strftime("%Y-%m-%d %H:%M:%S")}\n')

if __name__ == '__main__':
    main()