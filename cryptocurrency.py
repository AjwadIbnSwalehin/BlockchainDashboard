import requests
from dotenv import load_dotenv
import os
import matplotlib.pyplot as plt
from datetime import datetime

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

    def fetch_trend_data(self):
        vs_currency = "gbp"
        days = "30"
        url = f"https://api.coingecko.com/api/v3/coins/{self.name}/market_chart"
        params = {"vs_currency": vs_currency, "days": days}
        headers = {"accept": "application/json"}
        
        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for {self.name}: {e}")
            return None

    def plot_price_trend(self):
        trend_data = self.fetch_trend_data()  # Call the method to get the data
        if not trend_data:
            print(f"Trend data for {self.name} could not be retrieved.")
            return

        timestamps = [datetime.utcfromtimestamp(price[0] / 1000) for price in trend_data["prices"]]
        prices = [price[1] for price in trend_data["prices"]]

        # Plot the trend line
        plt.figure(figsize=(10, 5))
        plt.plot(timestamps, prices, label=self.name.capitalize(), color="blue")
        plt.title(f"{self.name.capitalize()} Price Trend (Last 30 Days)")
        plt.xlabel("Date")
        plt.ylabel("Price (GBP)")
        plt.legend()
        plt.grid(True)
        plt.show()

        
