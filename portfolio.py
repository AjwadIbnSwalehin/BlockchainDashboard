from cryptocurrency import Cryptocurrency
import matplotlib.pyplot as plt
from user import UserManager

class Portfolio:
    def __init__(self, user_email):
        self.user_email = user_email
        self.user_manager = UserManager() 
        self.holdings = self.load_portfolio()
        self.coins = ["bitcoin", "ethereum", "tether", "solana", "dogecoin", "cardano"]
        
    def load_portfolio(self):
        # Load portfolio from UserManager for the current user
        portfolio_data = self.user_manager.users[self.user_email].get('portfolio', {})
        
        # Debugging: Check if the portfolio data is empty
        if not portfolio_data:
            print(f"No portfolio data found for {self.user_email}")
            return {}

        print(f"Portfolio data for {self.user_email}: {portfolio_data}")  # Debug line
        return portfolio_data
    
    def addCrypto(self, crypto, quantity=1):
        # Checks if crypto is in the tradeable ones
        if crypto in self.coins:
            if crypto in self.holdings:
                # If already present, increase the quantity
                self.holdings[crypto] += quantity
            else:
                # If not present, add the cryptocurrency with the initial quantity
                self.holdings[crypto] = quantity
                
            self.user_manager.users[self.user_email]['portfolio'] = self.holdings
            self.user_manager.save_users()  # Save changes to CSV
        
        else:
            print("You can only trade: ")
            for coin in self.coins:
                print(coin)
    
    def removeCrypto(self, crypto, quantity=1):
        # Checks if crypto is stored in portfolio
        if crypto in self.holdings:
            current_quantity = self.holdings[crypto]
            if current_quantity <= quantity:
                # Remove the crypto if the quantity to remove is greater or equal to what is held
                del self.holdings[crypto]
            else:
                # Reduce the quantity
                self.holdings[crypto] -= quantity
            self.user_manager.users[self.user_email]['portfolio'] = self.holdings
            self.user_manager.save_users()  # Save changes to CSV
        else:
            print(f"{crypto} is not in your portfolio")
    
    def calculateTotalValue(self):
        total_value = 0  # Initialize total value
        print(f"self.holdings.items: {self.holdings.items()}")

        for crypto_name, quantity in self.holdings.items():
            # Create a Cryptocurrency object for each symbol
            crypto = Cryptocurrency(crypto_name)
            
            # Get the price of the cryptocurrency
            price = crypto.getPrice()
            
            # Calculate the value for the current cryptocurrency and add to total_value
            total_value += price * quantity
            
        return total_value
    
    def analytics(self):
        if not self.holdings:
            print("Your portfolio is empty. Add some cryptocurrencies first.")
            return

        # Calculate portfolio allocation
        labels = []
        values = []
        for crypto_name, quantity in self.holdings.items():
            crypto = Cryptocurrency(crypto_name)  # Create the cryptocurrency object for each symbol
            values.append(crypto.getPrice() * quantity)
            labels.append(f"{crypto_name} ({crypto.name})")

        # Plot the pie chart
        plt.figure(figsize=(8, 8))
        plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.title("Portfolio Allocation")
        plt.show()
        

