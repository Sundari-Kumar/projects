import sqlite3

# Vehicle Class representing the transportation system
class TransportationSystem:
    def __init__(self):
        self.conn = sqlite3.connect('transportation_system.db')
        self.cursor = self.conn.cursor()
        self._setup_db()

    def _setup_db(self):
        # Create a table for storing vehicle details
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS vehicles (
            id INTEGER PRIMARY KEY,
            vehicle_number TEXT NOT NULL UNIQUE,
            vehicle_type TEXT NOT NULL,
            location TEXT NOT NULL,
            status TEXT NOT NULL
        )""")
        self.conn.commit()

    def add_vehicle(self, vehicle_number, vehicle_type, location, status):
        # Adds a new vehicle to the system
        try:
            self.cursor.execute("""
            INSERT INTO vehicles (vehicle_number, vehicle_type, location, status) 
            VALUES (?, ?, ?, ?)""", (vehicle_number, vehicle_type, location, status))
            self.conn.commit()
            print("Vehicle added successfully!")
        except sqlite3.IntegrityError:
            print("Error: Vehicle with this number already exists.")
    
    def update_vehicle(self, vehicle_number, vehicle_type=None, location=None, status=None):
        # Update vehicle details
        query = "UPDATE vehicles SET "
        params = []

        if vehicle_type:
            query += "vehicle_type = ?, "
            params.append(vehicle_type)
        
        if location:
            query += "location = ?, "
            params.append(location)
        
        if status:
            query += "status = ?, "
            params.append(status)
        
        # Remove trailing comma and space
        query = query.rstrip(', ') 
        query += " WHERE vehicle_number = ?"
        params.append(vehicle_number)
        
        self.cursor.execute(query, tuple(params))
        self.conn.commit()
        print("Vehicle updated successfully.")

    def delete_vehicle(self, vehicle_number):
        # Delete a vehicle from the system
        self.cursor.execute("DELETE FROM vehicles WHERE vehicle_number = ?", (vehicle_number,))
        self.conn.commit()
        print("Vehicle deleted successfully.")

    def search_vehicle(self, vehicle_number=None, vehicle_type=None, location=None):
        # Search for vehicles based on the provided criteria
        query = "SELECT * FROM vehicles WHERE"
        conditions = []
        params = []

        if vehicle_number:
            conditions.append("vehicle_number = ?")
            params.append(vehicle_number)
        
        if vehicle_type:
            conditions.append("vehicle_type = ?")
            params.append(vehicle_type)
        
        if location:
            conditions.append("location = ?")
            params.append(location)
        
        if not conditions:
            print("No search criteria provided.")
            return

        query += " AND ".join(conditions)

        self.cursor.execute(query, tuple(params))
        vehicles = self.cursor.fetchall()

        if vehicles:
            print("Found vehicles:")
            for vehicle in vehicles:
                print("Vehicle Number: {}, Type: {}, Location: {}, Status: {}".format(
                    vehicle[1], vehicle[2], vehicle[3], vehicle[4]))
        else:
            print("No vehicles found matching the criteria.")

    def close(self):
        self.conn.close()

