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
            print("CSV file not found. Starting fresh.")

    def save_users(self):
        with open(self.csv_file, mode='w', newline='') as file:
            fieldnames = ['Emails', 'Passwords', 'Portfolio']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for email, data in self.users.items():
                portfolio = ','.join([f"{k}:{v}" for k, v in data['portfolio'].items()])  # Convert portfolio dict to a string
                writer.writerow({'Emails': email, 'Passwords': data['password'], 'Portfolio': portfolio})
        print("User Saved.")

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

