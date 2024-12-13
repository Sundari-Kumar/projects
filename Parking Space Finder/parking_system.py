import sqlite3
import datetime

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
                print(f"Space ID: {space[0]}, Vehicle Type: {space[1]}")
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
                print(f"Parking Space {space_id} has been booked successfully!")
            else:
                print(f"Parking Space {space_id} is already booked!")
        else:
            print("Invalid Parking Space ID!")

    def view_parking_status(self):
        """ View the status of all parking spaces """
        self.cursor.execute("SELECT * FROM parking_spaces")
        all_spaces = self.cursor.fetchall()
        print("Parking Spaces Status:")
        for space in all_spaces:
            print(f"Space ID: {space[0]}, Vehicle Type: {space[1]}, Status: {space[2]}")

    def close(self):
        """ Close the database connection """
        self.conn.close()

