from user import UserManager
from cryptocurrency import Cryptocurrency
from portfolio import Portfolio
import pandas as pd

def main():
    # Initialize the UserManager
    user_manager = UserManager()
    portfolio = None  # Portfolio is created only after login
    logged_in = False

    while True:
        print("\nWelcome to the Crypto Portfolio Manager")
        print("1. Register")
        print("2. Login")
        print("3. Add Cryptocurrency")
        print("4. Remove Cryptocurrency")
        print("5. View Portfolio Value")
        print("6. Portfolio Analytics")
        print("7. View Cryptocurrency List")
        print("8. Exit")

        choice = input("Enter your choice: ")

        # Use match-case for cleaner control flow
        match choice:
            case "1":  # Register
                email = input("Enter your email: ")
                password = input("Enter your password: ")
                print(user_manager.register_user(email, password))

            case "2":  # Login
                email = input("Enter your email: ")
                password = input("Enter your password: ")
                auth_message = user_manager.authenticate_user(email, password)
                print(auth_message)
                if auth_message == "Login successful.":
                    logged_in = True
                    portfolio = Portfolio(email)  # Create a portfolio for the logged-in user
                    portfolio.load_portfolio()

            case "3":  # Add Cryptocurrency
                if not logged_in:
                    print("Please log in to access this feature.")
                    continue
                name = input("Enter the cryptocurrency name (e.g., bitcoin): ")
                quantity = int(input("Enter the quantity: "))
                portfolio.addCrypto(name, quantity)

            case "4":  # Remove Cryptocurrency
                if not logged_in:
                    print("Please log in to access this feature.")
                    continue
                crypto_name = input("Enter the cryptocurrency name to remove: ")
                quantity = int(input("Enter the quantity to remove: "))
                portfolio.removeCrypto(crypto_name, quantity)

            case "5":  # View Portfolio Value
                if not logged_in:
                    print("Please log in to access this feature.")
                    continue
                print(f"Total Portfolio Value: £{portfolio.calculateTotalValue()}")

            case "6":  # Portfolio Analytics
                if not logged_in:
                    print("Please log in to access this feature.")
                    continue
                portfolio.analytics()

            case "7": # Cryptocurrency List
                coins = ["bitcoin", "ethereum", "tether", "solana", "dogecoin", "cardano"]
                for coin in coins:
                    print(coin)
                    
                coin_input = input("Which coin would you like to view? ")
                if coin_input in coins:
                    crypto = Cryptocurrency(coin_input)
                    print(f"Price: {crypto.fetch_real_time_data()['price']}")
                    print(f"Market Cap: {crypto.fetch_real_time_data()['marketCap']}")
                    print(f"Supply: {crypto.fetch_real_time_data()['supply']}")
                else:
                    print("Coin is not supported by this application.")
                    continue
                    
            
            case "8":  # Exit
                print("Goodbye!")
                break

            case _:  # Default case for invalid input
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
