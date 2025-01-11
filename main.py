from user import UserManager
from cryptocurrency import Cryptocurrency
from portfolio import Portfolio

def main():
    # Initialize the UserManager and Portfolio
    user_manager = UserManager()
    portfolio = None  # No portfolio unless the user logs in
    logged_in = False

    while True:
        print("\nWelcome to the Crypto Portfolio Manager")
        print("1. Register")
        print("2. Login")
        print("3. Add Cryptocurrency")
        print("4. Remove Cryptocurrency")
        print("5. View Portfolio Value")
        print("6. Portfolio Analytics")
        print("7. Exit")

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
                    portfolio = Portfolio()  # Create a new portfolio for the logged-in user

            case "3":  # Add Cryptocurrency
                if not logged_in:
                    print("Please log in to access this feature.")
                    continue
                name = input("Enter the cryptocurrency name (e.g., bitcoin): ")
                symbol = input("Enter the cryptocurrency symbol (e.g., BTC): ")
                quantity = int(input("Enter the quantity: "))
                crypto = Cryptocurrency(name, symbol)
                portfolio.addCrypto(crypto, quantity)
                print(f"Added {quantity} of {name} ({symbol}) to your portfolio.")

            case "4":  # Remove Cryptocurrency
                if not logged_in:
                    print("Please log in to access this feature.")
                    continue
                symbol = input("Enter the cryptocurrency symbol to remove: ")
                quantity = int(input("Enter the quantity to remove: "))
                portfolio.removeCrypto(symbol, quantity)

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

            case "7":  # Exit
                print("Goodbye!")
                break

            case _:  # Default case for invalid input
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()