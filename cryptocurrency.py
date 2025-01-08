import requests

class Cryptocurrency:
    def __init__(self, name, symbol, price=None, marketCap=None, supply=None):
        self.name = name
        self.symbol = symbol
        self.price = price
        self.marketCap = marketCap
        self.supply = supply

    def getPrice(self):
        if self.price is not None:
            return self.price
        else:
            return self.fetch_real_time_data()['price']

    def updatePrice(self, new_price):
        self.price = new_price
        print(f"Price of {self.name} updated to {self.price}")

    def fetch_real_time_data(self):
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={self.name.lower()}&vs_currencies=gbp"
        response = requests.get(url)
        data = response.json()
        
        # Update the cryptocurrency's real-time price and other data
        if self.name.lower() in data:
            self.updatePrice(data[self.name.lower()]["gbp"])
            # Fetch marketCap and supply if needed
            # Example: 'market_cap' and 'total_supply' could also be fetched similarly
            return {
                'price': self.price,
                'marketCap': data[self.name.lower()].get("market_cap", "N/A"),
                'supply': data[self.name.lower()].get("total_supply", "N/A")
            }
        else:
            print(f"Error fetching data for {self.name}")
            return {}

# Example 
bitcoin = Cryptocurrency("bitcoin", "BTC")
print(bitcoin.getPrice())  # Calls the API if price is not set