from cryptocurrency import Cryptocurrency
import matplotlib.pyplot as plt

class Portfolio:
    def __init__(self):
        self.holdings = {}  # Dictionary to store {symbol: [crypto, quantity]}
    
    def addCrypto(self, crypto, quantity=1):
        if crypto.symbol in self.holdings:
            # If already present, increase the quantity
            self.holdings[crypto.symbol][1] += quantity
        else:
            # If not present, add the cryptocurrency with the initial quantity
            self.holdings[crypto.symbol] = [crypto, quantity]
    
    def removeCrypto(self, symbol, quantity=1):
        if symbol in self.holdings:
            current_quantity = self.holdings[symbol][1]
            if current_quantity <= quantity:
                # Remove the crypto if the quantity to remove is greater or equal to what is held
                del self.holdings[symbol]
            else:
                # Reduce the quantity
                self.holdings[symbol][1] -= quantity
        else:
            print(f"{symbol} is not in your portfolio")
    
    def calculateTotalValue(self):
        total_value = sum(crypto.getPrice() * quantity for crypto, quantity in self.holdings.values())
        return total_value
    
    def analytics(self):
        if not self.holdings:
            print("Your portfolio is empty. Add some cryptocurrencies first.")
            return

        # Calculate portfolio allocation
        labels = []
        values = []
        for symbol, (crypto, quantity) in self.holdings.items():
            value = crypto.getPrice() * quantity
            labels.append(f"{crypto.name} ({crypto.symbol})")
            values.append(value)

        # Plot the pie chart
        plt.figure(figsize=(8, 8))
        plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.title("Portfolio Allocation")
        plt.show()
        
        
# Example usage
portfolio = Portfolio()

# Adding cryptos
bitcoin = Cryptocurrency("bitcoin", "BTC")
ethereum = Cryptocurrency("ethereum", "ETH")
portfolio.addCrypto(bitcoin, 3)
portfolio.addCrypto(ethereum, 2)


# Viewing the portfolio and total value
for symbol, (crypto, quantity) in portfolio.holdings.items():
    print(f"{quantity} units of {crypto.name} ({crypto.symbol}) at £{crypto.getPrice()} each")
print(f"Portfolio total value: £{portfolio.calculateTotalValue()}")

portfolio.analytics()