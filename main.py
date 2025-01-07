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
                    self.users[row['Emails']] = row['Passwords']
        except FileNotFoundError:
            print("CSV file not found")

    def save_users(self):
        with open(self.csv_file, mode='w', newline='') as file:
            fieldnames = ['Emails', 'Passwords']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for email, password in self.users.items():
                writer.writerow({'Emails': email, 'Passwords': password})

    def register_user(self, email, password):
        if email in self.users:
            return "Email already registered."
        self.users[email] = password
        self.save_users()
        return f"User with email {email} registered successfully."

    def authenticate_user(self, email, password):
        if email in self.users and self.users[email] == password:
            return "Login successful."
        return "Invalid email or password."

    def update_password(self, email, old_password, new_password):
        if email in self.users and self.users[email] == old_password:
            self.users[email] = new_password
            self.save_users()
            return "Password updated successfully."
        return "Old password is incorrect or email not found."
    
# Initialize UserManager
user_manager = UserManager()

# Register a new user
print(user_manager.register_user("john@gmail.com", "ddddd"))

# Authenticate an existing user
print(user_manager.authenticate_user("alex@gmail.com", "aaaaa"))

# Update a user's password
print(user_manager.update_password("alex@gmail.com", "aaaaa", "newpass123"))