import requests
from dotenv import load_dotenv
import os

def configure():
    load_dotenv()

class Cryptocurrency:
    def __init__(self, name, price=None, marketCap=None, supply=None):
        self.name = name
        self.price = price
        self.marketCap = marketCap
        self.supply = supply

    # Gets price of a given cryptocurrency
    def getPrice(self):
        if self.price is not None:
            return self.price
        else:
            return self.fetch_real_time_data()['price'] # Accesses the dictionary which the API returns

    # Updates the price of the cryptocurrency
    def updatePrice(self, new_price):
        self.price = new_price

    def fetch_real_time_data(self):
        # Accesses the API
        url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=gbp&ids={self.name.lower()}"
        headers = {
            "accept": "application/json",
            "x-cg-demo-api-key": os.getenv('api_key')
        }
        params = {
            "vscurrency": "gbp",
            "ids": self.name.lower()
        }
        
        try:
            response = requests.get(url, headers=headers, params = params)
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()

            # Check if the cryptocurrency name exists in the API response
            if len(data) > 0:
                    coin_data = data[0]  # Get the first (and only) item in the response list
                    self.updatePrice(coin_data["current_price"])  # Update the price attribute
                    return {
                        'price': self.price,
                        'marketCap': coin_data.get("market_cap", "N/A"),
                        'supply': coin_data.get("circulating_supply", "N/A")
                    }
            else:
                print(f"No data found for {self.name}.")
                return None
        # If the API request didn't work
        except requests.exceptions.RequestException as e:
            print(f"API request error: {e}")
            return None

