import sqlite3
import datetime

class FoodDonationSystem:
    def __init__(self):
        self.conn = sqlite3.connect('food_donation.db')
        self.cursor = self.conn.cursor()
        self._setup_db()

    def _setup_db(self):
        """ Create food items table if not exists """
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS food_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            food_name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            status TEXT NOT NULL
        )""")
        self.conn.commit()

    def add_food_item(self, food_name, quantity):
        """ Add a new food item available for donation """
        self.cursor.execute("""
        INSERT INTO food_items (food_name, quantity, status)
        VALUES (?, ?, ?)""", (food_name, quantity, "available"))
        self.conn.commit()
        print("Food item added successfully!")

    def view_available_food(self):
        """ View available food items for donation """
        self.cursor.execute("SELECT * FROM food_items WHERE status = 'available'")
        available_food = self.cursor.fetchall()
        if available_food:
            print("Available Food Items for Donation:")
            for food in available_food:
                print(f"ID: {food[0]}, Food Name: {food[1]}, Quantity: {food[2]}")
        else:
            print("No food items available for donation.")

    def donate_food(self, food_id):
        """ Donate food item and mark it as donated """
        self.cursor.execute("SELECT * FROM food_items WHERE id = ?", (food_id,))
        food = self.cursor.fetchone()
        if food:
            if food[3] == 'available':
                self.cursor.execute("""
                UPDATE food_items SET status = 'donated' WHERE id = ?""", (food_id,))
                self.conn.commit()
                print(f"Food item {food[1]} has been donated successfully!")
            else:
                print(f"Food item {food[1]} is already donated.")
        else:
            print("Invalid Food Item ID!")

    def view_food_status(self):
        """ View the status of all food items """
        self.cursor.execute("SELECT * FROM food_items")
        all_food = self.cursor.fetchall()
        print("Food Items Status:")
        for food in all_food:
            print(f"ID: {food[0]}, Food Name: {food[1]}, Quantity: {food[2]}, Status: {food[3]}")

    def close(self):
        """ Close the database connection """
        self.conn.close()

