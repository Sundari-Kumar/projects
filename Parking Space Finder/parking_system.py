import sqlite3
import time

class ParkingSystem:
    def __init__(self):
        self.conn = sqlite3.connect('parking_system.db')
        self.cursor = self.conn.cursor()
        self._setup_db()

    def _setup_db(self):
        """ Create parking spaces table if not exists """
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS parking_spaces (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_type TEXT NOT NULL,
            status TEXT NOT NULL
        )""")
        
        self.conn.commit()

    def add_parking_space(self, vehicle_type):
        """ Add parking space to the system """
        self.cursor.execute("""
        INSERT INTO parking_spaces (vehicle_type, status)
        VALUES (?, ?)""", (vehicle_type, "available"))
        self.conn.commit()

    def view_available_spaces(self):
        """ View available parking spaces """
        self.cursor.execute("SELECT * FROM parking_spaces WHERE status = 'available'")
        available_spaces = self.cursor.fetchall()
        if available_spaces:
            print("Available Parking Spaces:")
            for space in available_spaces:
                print("Space ID: {0}, Vehicle Type: {1}".format(space[0], space[1]))
        else:
            print("No available parking spaces at the moment.")
    
    def book_parking_space(self, space_id):
        """ Book a parking space if available """
        self.cursor.execute("SELECT * FROM parking_spaces WHERE id = ?", (space_id,))
        space = self.cursor.fetchone()
        if space:
            if space[2] == 'available':
                self.cursor.execute("""
                UPDATE parking_spaces SET status = 'booked' WHERE id = ?""", (space_id,))
                self.conn.commit()
                print("Parking Space {0} has been booked successfully!".format(space_id))
            else:
                print("Parking Space {0} is already booked!".format(space_id))
        else:
            print("Invalid Parking Space ID!")

    def view_parking_status(self):
        """ View the status of all parking spaces """
        self.cursor.execute("SELECT * FROM parking_spaces")
        all_spaces = self.cursor.fetchall()
        print("Parking Spaces Status:")
        for space in all_spaces:
            print("Space ID: {0}, Vehicle Type: {1}, Status: {2}".format(space[0], space[1], space[2]))

    def close(self):
        """ Close the database connection """
        self.conn.close()

def main():
    system = ParkingSystem()

    # Add some parking spaces to the system
    system.add_parking_space("Car")
    system.add_parking_space("Truck")
    system.add_parking_space("Motorcycle")
    
    while True:
        print("\nParking System")
        print("1. View Available Parking Spaces")
        print("2. Book a Parking Space")
        print("3. View All Parking Spaces Status")
        print("4. Exit")
        
        choice = raw_input("Enter your choice: ")

        if choice == '1':
            system.view_available_spaces()
        elif choice == '2':
            try:
                space_id = int(raw_input("Enter Parking Space ID to book: "))
                system.book_parking_space(space_id)
            except ValueError:
                print("Invalid input. Please enter a valid Parking Space ID.")
        elif choice == '3':
            system.view_parking_status()
        elif choice == '4':
            print("Exiting the system.")
            break
        else:
            print("Invalid choice. Please try again.")
        
        time.sleep(2)  # Adding a brief pause before next action.

    system.close()

if __name__ == "__main__":
    main()
