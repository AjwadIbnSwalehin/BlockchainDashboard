# import csv
# from portfolio import Portfolio
# from cryptocurrency import Cryptocurrency

# class UserManager:
#     def __init__(self, csv_file="Logins.csv"):
#         self.users = {}  # Format: {email: {'password': password, 'portfolio': Portfolio}}
#         self.csv_file = csv_file
#         self.load_users()

#     def load_users(self):
#         """Load user data and initialize portfolios."""
#         try:
#             with open(self.csv_file, mode='r') as file:
#                 reader = csv.DictReader(file)
#                 for row in reader:
#                     email = row['Emails']
#                     password = row['Passwords']
#                     portfolio = Portfolio()
                    
#                     # Load cryptos into the portfolio
#                     for key, value in row.items():
#                         if key not in ['Emails', 'Passwords'] and value:
#                             portfolio.addCrypto(Cryptocurrency(key, key), int(value))
                    
#                     self.users[email] = {'password': password, 'portfolio': portfolio}
#         except FileNotFoundError:
#             print("CSV file not found. Starting fresh.")

#     def save_users(self):
#         """Save user portfolios back to CSV."""
#         fieldnames = ['Emails', 'Passwords'] + self.get_all_cryptos()
#         with open(self.csv_file, mode='w', newline='') as file:
#             writer = csv.DictWriter(file, fieldnames=fieldnames)
#             writer.writeheader()
#             for email, data in self.users.items():
#                 row = {'Emails': email, 'Passwords': data['password']}
#                 portfolio = data['portfolio']
#                 for symbol, (crypto, quantity) in portfolio.holdings.items():
#                     row[symbol] = quantity
#                 writer.writerow(row)

#     def get_all_cryptos(self):
#         """Gather all unique cryptos across all portfolios."""
#         cryptos = set()
#         for data in self.users.values():
#             cryptos.update(data['portfolio'].holdings.keys())
#         return list(cryptos)

#     def register_user(self, email, password):
#         """Register a new user."""
#         if email in self.users:
#             return "Email already registered."
#         self.users[email] = {'password': password, 'portfolio': Portfolio()}
#         self.save_users()
#         return f"User with email {email} registered successfully."

#     def authenticate_user(self, email, password):
#         """Authenticate a user."""
#         if email in self.users and self.users[email]['password'] == password:
#             return "Login successful."
#         return "Invalid email or password."

#     def update_password(self, email, old_password, new_password):
#         """Update the password for a user."""
#         if email in self.users and self.users[email]['password'] == old_password:
#             self.users[email]['password'] = new_password
#             self.save_users()
#             return "Password updated successfully."
#         return "Old password is incorrect or email not found."

#     def add_crypto_to_user(self, email, crypto, quantity):
#         """Add a cryptocurrency to a user's portfolio."""
#         if email in self.users:
#             self.users[email]['portfolio'].addCrypto(crypto, quantity)
#             self.save_users()
#             return f"Added {quantity} of {crypto.name} to {email}'s portfolio."
#         return f"User {email} not found."

#     def remove_crypto_from_user(self, email, symbol, quantity):
#         """Remove a cryptocurrency from a user's portfolio."""
#         if email in self.users:
#             self.users[email]['portfolio'].removeCrypto(symbol, quantity)
#             self.save_users()
#             return f"Removed {quantity} of {symbol} from {email}'s portfolio."
#         return f"User {email} not found."

import csv

class UserManager:
    def __init__(self, csv_file="Logins.csv"):
        self.users = {}
        self.csv_file = csv_file
        self.load_users()

    def load_users(self):
        try:
            with open(self.csv_file, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Parse the portfolio field
                    portfolio_data = row['Portfolio']
                    portfolio_dict = dict(
                        [item.split(':') for item in portfolio_data.split(',')] if portfolio_data else []
                    )
                    # Convert portfolio quantities to integers
                    portfolio_dict = {k: int(v) for k, v in portfolio_dict.items()}
                    
                    self.users[row['Emails']] = {
                        'password': row['Passwords'],
                        'portfolio': portfolio_dict
                    }
        except FileNotFoundError:
            print("CSV file not found")

    def save_users(self):
        with open(self.csv_file, mode='w', newline='') as file:
            fieldnames = ['Emails', 'Passwords', 'Portfolio']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for email, data in self.users.items():
                portfolio = ','.join([f"{k}:{v}" for k, v in data['portfolio'].items()])  # Convert portfolio dict to a string
                writer.writerow({'Emails': email, 'Passwords': data['password'], 'Portfolio': portfolio})
        print("user saved")

    def register_user(self, email, password):
        if email in self.users:
            return "Email already registered."
        self.users[email] = {'password': password, 'portfolio': {}}
        self.save_users()
        return f"User with email {email} registered successfully."

    def authenticate_user(self, email, password):
        if email in self.users and self.users[email]['password'] == password:
            return "Login successful."
        return "Invalid email or password."

    def update_password(self, email, old_password, new_password):
        if email in self.users and self.users[email]['password'] == old_password:
            self.users[email]['password'] = new_password
            self.save_users()
            return "Password updated successfully."
        return "Old password is incorrect or email not found."