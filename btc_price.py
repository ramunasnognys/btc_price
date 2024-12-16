import requests
import json
from datetime import datetime

def get_btc_price(currencies=['usd', 'nok']):
    """Fetch current Bitcoin price from CoinGecko API for specified currencies
    
    Args:
        currencies (list): List of currency codes (e.g., ['usd', 'nok'])
        
    Returns:
        dict: Dictionary containing price information for each currency
    """
    try:
        # Convert currencies list to comma-separated string
        vs_currencies = ','.join(currencies)
        
        # CoinGecko API endpoint for Bitcoin price
        url = 'https://api.coingecko.com/api/v3/simple/price'
        params = {
            'ids': 'bitcoin',
            'vs_currencies': vs_currencies,
            'include_24hr_change': 'true',
            'include_last_updated_at': 'true'
        }
        
        # Make the API request
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        # Parse the response
        data = response.json()
        btc_data = data['bitcoin']
        
        # Create result dictionary
        result = {
            'last_updated': datetime.fromtimestamp(btc_data['last_updated_at']),
            'prices': {}
        }
        
        # Add price information for each currency
        for currency in currencies:
            result['prices'][currency] = {
                'price': btc_data[currency],
                'change_24h': btc_data.get(f'{currency}_24h_change', 0)
            }
        
        return result
        
    except requests.exceptions.RequestException as e:
        print(f'Error fetching Bitcoin price: {e}')
        return None
    except (KeyError, json.JSONDecodeError) as e:
        print(f'Error parsing response: {e}')
        return None

def format_currency(amount, currency):
    """Format currency amount with appropriate symbol
    
    Args:
        amount (float): The amount to format
        currency (str): Currency code (e.g., 'usd', 'nok')
    
    Returns:
        str: Formatted currency string
    """
    currency = currency.lower()
    if currency == 'usd':
        return f'${amount:,.2f}'
    elif currency == 'nok':
        return f'{amount:,.2f} kr'
    else:
        return f'{amount:,.2f} {currency.upper()}'

def main():
    """Main function to demonstrate the Bitcoin price fetcher"""
    btc_data = get_btc_price(['usd', 'nok'])
    
    if btc_data:
        print('\nBitcoin Price Information:')
        print(f'Last Updated: {btc_data["last_updated"].strftime("%Y-%m-%d %H:%M:%S")}\n')
        
        for currency, data in btc_data['prices'].items():
            print(f'Price ({currency.upper()}): {format_currency(data["price"], currency)}')
            print(f'24h Change: {data["change_24h"]:,.2f}%')
            print()

if __name__ == '__main__':
    main()