import requests
import time
from datetime import datetime
from typing import Dict, Optional, Union, Any
from requests.exceptions import RequestException, HTTPError
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class RateLimitException(Exception):
    """Custom exception for rate limiting"""
    pass

def get_bitcoin_price() -> Optional[Dict[str, Union[float, str, datetime]]]:
    """
    Fetch current Bitcoin price from CoinGecko API

    Returns:
        Optional[Dict[str, Union[float, str, datetime]]]: Dictionary containing price data or None if error occurs
        
    Raises:
        RateLimitException: When API rate limit is hit
        RequestException: When API request fails
    """
    try:
        # CoinGecko API endpoint for Bitcoin price in USD
        url = 'https://api.coingecko.com/api/v3/simple/price'
        params: Dict[str, Any] = {
            'ids': 'bitcoin',
            'vs_currencies': 'usd',
            'include_24hr_change': 'true',
            'include_last_updated_at': 'true'
        }
        
        response = requests.get(url, params=params, timeout=10)  # Added timeout
        
        # Check for rate limiting
        if response.status_code == 429:
            raise RateLimitException('Rate limit exceeded. Please wait before making another request.')
        
        response.raise_for_status()
        
        data = response.json()
        
        # Validate response data
        if 'bitcoin' not in data or not all(key in data['bitcoin'] for key in ['usd', 'usd_24h_change', 'last_updated_at']):
            logging.error('Invalid response format from API')
            return None
        
        price = data['bitcoin']['usd']
        change_24h = data['bitcoin']['usd_24h_change']
        last_updated = datetime.fromtimestamp(data['bitcoin']['last_updated_at'])
        
        return {
            'price': price,
            'change_24h': round(change_24h, 2),
            'last_updated': last_updated
        }
        
    except RateLimitException as e:
        logging.warning(f'Rate limit hit: {e}')
        # Wait for 60 seconds when rate limit is hit
        time.sleep(60)
        return None
        
    except HTTPError as e:
        logging.error(f'HTTP error occurred: {e}')
        return None
        
    except RequestException as e:
        logging.error(f'Error fetching Bitcoin price: {e}')
        return None
        
    except (KeyError, ValueError) as e:
        logging.error(f'Error processing response data: {e}')
        return None

def main() -> None:
    """Main function to demonstrate the usage"""
    logging.info('Starting Bitcoin Price Tracker...')
    
    consecutive_errors = 0
    max_consecutive_errors = 3
    
    while True:
        try:
            btc_data = get_bitcoin_price()
            
            if btc_data:
                consecutive_errors = 0  # Reset error counter on successful fetch
                
                print('\nBitcoin Price Information:')
                print(f'Current Price: ${btc_data["price"]:,.2f}')
                print(f'24h Change: {btc_data["change_24h"]}%')
                print(f'Last Updated: {btc_data["last_updated"].strftime("%Y-%m-%d %H:%M:%S")}')
            else:
                consecutive_errors += 1
                if consecutive_errors >= max_consecutive_errors:
                    logging.error(f'Failed to fetch data {max_consecutive_errors} times in a row. Exiting...')
                    break
            
            # Wait for 60 seconds before the next update
            print('\nWaiting 60 seconds for next update...')
            time.sleep(60)
            
        except KeyboardInterrupt:
            logging.info('Bitcoin Price Tracker stopped by user.')
            break
        
        except Exception as e:
            logging.error(f'Unexpected error occurred: {e}')
            consecutive_errors += 1
            if consecutive_errors >= max_consecutive_errors:
                logging.error(f'Too many consecutive errors ({max_consecutive_errors}). Exiting...')
                break
            time.sleep(60)  # Wait before retrying

if __name__ == '__main__':
    main()
