import time
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
                print("ID: {}, Food Name: {}, Quantity: {}".format(food[0], food[1], food[2]))
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
                print("Food item {} has been donated successfully!".format(food[1]))
            else:
                print("Food item {} is already donated.".format(food[1]))
        else:
            print("Invalid Food Item ID!")

    def view_food_status(self):
        """ View the status of all food items """
        self.cursor.execute("SELECT * FROM food_items")
        all_food = self.cursor.fetchall()
        print("Food Items Status:")
        for food in all_food:
            print("ID: {}, Food Name: {}, Quantity: {}, Status: {}".format(food[0], food[1], food[2], food[3]))

    def close(self):
        """ Close the database connection """
        self.conn.close()


def main():
    system = FoodDonationSystem()

    # Add some food items to the system
    system.add_food_item("Rice", 100)
    system.add_food_item("Wheat", 50)
    system.add_food_item("Vegetables", 30)

    while True:
        print("\nWaste Food Management and Donation System")
        print("1. View Available Food Items for Donation")
        print("2. Donate a Food Item")
        print("3. View All Food Items Status")
        print("4. Exit")
        
        choice = raw_input("Enter your choice: ")

        if choice == '1':
            system.view_available_food()
        elif choice == '2':
            try:
                food_id = int(raw_input("Enter Food Item ID to donate: "))
                system.donate_food(food_id)
            except ValueError:
                print("Invalid input. Please enter a valid Food Item ID.")
        elif choice == '3':
            system.view_food_status()
        elif choice == '4':
            print("Exiting the system.")
            break
        else:
            print("Invalid choice. Please try again.")
        
        time.sleep(2)  # Adding a brief pause before next action.

    system.close()


if __name__ == "__main__":
    main()
