import sqlite3
import hashlib

# Simulate fingerprint scanning
def scan_fingerprint():
    # In a real system, this function would interface with a fingerprint scanner
    # Here, we will just return a "scanned" fingerprint id for simplicity.
    fingerprint = raw_input("Please scan your fingerprint: ")  # Simulating fingerprint scan
    return fingerprint

# ATM System Class
class ATMSystem:
    def __init__(self):
        self.conn = sqlite3.connect('atm_system.db')
        self.cursor = self.conn.cursor()
        self._setup_db()

    def _setup_db(self):
        # Create users table to store account info and fingerprint data
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            fingerprint_id TEXT NOT NULL UNIQUE,
            balance REAL NOT NULL
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
        # Simulate fingerprint scan and match with database
        fingerprint_id = scan_fingerprint()
        self.cursor.execute("SELECT * FROM users WHERE fingerprint_id = ?", (fingerprint_id,))
        user = self.cursor.fetchone()
        if user:
            print("User authenticated successfully!")
            return user
        else:
            print("Authentication failed. Fingerprint not recognized.")
            return None

    def check_balance(self, user):
        print("Your current balance is: ${:.2f}".format(user[3]))

    def withdraw(self, user, amount):
        if user[3] < amount:
            print("Insufficient balance!")
            return
        new_balance = user[3] - amount
        self.cursor.execute("UPDATE users SET balance = ? WHERE id = ?", (new_balance, user[0]))
        self.conn.commit()
        print("You have successfully withdrawn ${:.2f}".format(amount))

    def deposit(self, user, amount):
        new_balance = user[3] + amount
        self.cursor.execute("UPDATE users SET balance = ? WHERE id = ?", (new_balance, user[0]))
        self.conn.commit()
        print("You have successfully deposited ${:.2f}".format(amount))

    def close(self):
        self.conn.close()

