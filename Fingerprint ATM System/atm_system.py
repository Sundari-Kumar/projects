import sqlite3
import hashlib
import time

# Simulate fingerprint scanning
def scan_fingerprint():
    # In a real system, this would interface with a fingerprint scanner
    fingerprint = raw_input("Please scan your fingerprint: ")
    return fingerprint

# ATM System Class
class ATMSystem:
    def __init__(self):
        self.conn = sqlite3.connect('atm_system.db')
        self.cursor = self.conn.cursor()
        self.user = None  # Logged-in user
        self._setup_db()

    def _setup_db(self):
        # Users Table
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            fingerprint_id TEXT NOT NULL UNIQUE,
            balance REAL NOT NULL
        )""")
        
        # Transactions Table
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            type TEXT NOT NULL,
            amount REAL NOT NULL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )""")
        
        self.conn.commit()

    def add_user(self, name, fingerprint_id, initial_balance):
        try:
            self.cursor.execute("INSERT INTO users (name, fingerprint_id, balance) VALUES (?, ?, ?)",
                                (name, fingerprint_id, initial_balance))
            self.conn.commit()
            print("User added successfully!")
        except sqlite3.IntegrityError:
            print("Error: User with this fingerprint already exists.")

    def authenticate_user(self):
        fingerprint_id = scan_fingerprint()
        self.cursor.execute("SELECT * FROM users WHERE fingerprint_id = ?", (fingerprint_id,))
        self.user = self.cursor.fetchone()
        if self.user:
            print("Authentication successful! Welcome, {}.".format(self.user[1]))
            return True
        else:
            print("Authentication failed. Fingerprint not recognized.")
            return False

    def check_balance(self):
        print("Your current balance is: ${:.2f}".format(self.user[3]))

    def deposit(self, amount):
        new_balance = self.user[3] + amount
        self.cursor.execute("UPDATE users SET balance = ? WHERE id = ?", (new_balance, self.user[0]))
        self.cursor.execute("INSERT INTO transactions (user_id, type, amount, timestamp) VALUES (?, 'Deposit', ?, ?)",
                            (self.user[0], amount, time.ctime()))
        self.conn.commit()
        self.user = (self.user[0], self.user[1], self.user[2], new_balance)  # Update user session
        print("Successfully deposited ${:.2f}".format(amount))

    def withdraw(self, amount):
        if self.user[3] < amount:
            print("Insufficient balance!")
            return
        new_balance = self.user[3] - amount
        self.cursor.execute("UPDATE users SET balance = ? WHERE id = ?", (new_balance, self.user[0]))
        self.cursor.execute("INSERT INTO transactions (user_id, type, amount, timestamp) VALUES (?, 'Withdraw', ?, ?)",
                            (self.user[0], amount, time.ctime()))
        self.conn.commit()
        self.user = (self.user[0], self.user[1], self.user[2], new_balance)  # Update user session
        print("Successfully withdrew ${:.2f}".format(amount))

    def view_transactions(self):
        self.cursor.execute("SELECT * FROM transactions WHERE user_id = ?", (self.user[0],))
        transactions = self.cursor.fetchall()
        if transactions:
            print("\nTransaction History:")
            for txn in transactions:
                print("ID: {}, Type: {}, Amount: ${:.2f}, Date: {}".format(txn[0], txn[2], txn[3], txn[4]))
        else:
            print("No transaction history available.")

    def logout(self):
        print("Logging out...")
        self.user = None

    def close(self):
        self.conn.close()

# Main Function
def main():
    atm = ATMSystem()

    # Add test user (use this once, then comment out)
    #atm.add_user("Test User", "123", 500)

    while True:
        print("\n--- Welcome to the Fingerprint ATM System ---")
        if atm.authenticate_user():
            while True:
                print("\nATM Menu:")
                print("1. Check Balance")
                print("2. Deposit")
                print("3. Withdraw")
                print("4. View Transactions")
                print("5. Logout")
                choice = raw_input("Enter choice: ")

                if choice == "1":
                    atm.check_balance()
                elif choice == "2":
                    amount = float(raw_input("Enter amount to deposit: $"))
                    atm.deposit(amount)
                elif choice == "3":
                    amount = float(raw_input("Enter amount to withdraw: $"))
                    atm.withdraw(amount)
                elif choice == "4":
                    atm.view_transactions()
                elif choice == "5":
                    atm.logout()
                    break
                else:
                    print("Invalid choice. Please try again.")
        else:
            print("Authentication failed. Try again.")

    atm.close()

if __name__ == "__main__":
    main()
