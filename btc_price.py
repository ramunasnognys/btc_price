import requests
import json
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

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

def get_historical_prices(currency='usd', days=7):
    """Fetch historical Bitcoin prices from CoinGecko API
    
    Args:
        currency (str): Currency code (e.g., 'usd', 'nok')
        days (int): Number of days of historical data to fetch
        
    Returns:
        tuple: Lists of dates and prices
    """
    try:
        url = f'https://api.coingecko.com/api/v3/coins/bitcoin/market_chart'
        params = {
            'vs_currency': currency,
            'days': days,
            'interval': 'daily'
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        prices = data['prices']
        
        dates = [datetime.fromtimestamp(price[0]/1000) for price in prices]
        price_values = [price[1] for price in prices]
        
        return dates, price_values
        
    except (requests.RequestException, KeyError, json.JSONDecodeError) as e:
        print(f'Error fetching historical prices: {e}')
        return None, None

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

def plot_price_history(currency='usd', days=7):
    """Plot Bitcoin price history using matplotlib
    
    Args:
        currency (str): Currency code (e.g., 'usd', 'nok')
        days (int): Number of days of historical data to plot
    """
    dates, prices = get_historical_prices(currency, days)
    
    if dates and prices:
        plt.figure(figsize=(10, 6))
        plt.plot(dates, prices, 'b-', linewidth=2)
        
        # Configure the plot
        plt.title(f'Bitcoin Price History ({currency.upper()})')
        plt.xlabel('Date')
        plt.ylabel(f'Price ({currency.upper()})')
        
        # Format x-axis to show dates nicely
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.gcf().autofmt_xdate()  # Rotate and align the tick labels
        
        # Add grid
        plt.grid(True, linestyle='--', alpha=0.7)
        
        # Customize the y-axis format
        plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: format_currency(x, currency)))
        
        plt.tight_layout()
        plt.show()

def main():
    """Main function to demonstrate the Bitcoin price fetcher"""
    currencies = ['usd', 'nok']
    btc_data = get_btc_price(currencies)
    
    if btc_data:
        print('\nBitcoin Price Information:')
        print(f'Last Updated: {btc_data["last_updated"].strftime("%Y-%m-%d %H:%M:%S")}\n')
        
        for currency, data in btc_data['prices'].items():
            print(f'Price ({currency.upper()}): {format_currency(data["price"], currency)}')
            print(f'24h Change: {data["change_24h"]:,.2f}%')
            print()
        
        # Plot price history for USD
        print("Generating price history plot...")
        plot_price_history('usd', days=7)

if __name__ == '__main__':
    main()