import pytest
from transportation_system import TransportationSystem

@pytest.fixture
def setup_transportation_system():
    # Create a fresh instance of the TransportationSystem and clear database before each test
    system = TransportationSystem()
    system.cursor.execute("DELETE FROM vehicles")  # Clear the vehicles table
    system.conn.commit()
    return system

def test_add_vehicle(setup_transportation_system):
    system = setup_transportation_system
    system.add_vehicle("V123", "Bus", "Downtown", "Available")
    system.cursor.execute("SELECT * FROM vehicles WHERE vehicle_number = 'V123'")
    vehicle = system.cursor.fetchone()
    assert vehicle is not None
    assert vehicle[1] == "V123"
    assert vehicle[2] == "Bus"
    assert vehicle[3] == "Downtown"
    assert vehicle[4] == "Available"

def test_update_vehicle(setup_transportation_system):
    system = setup_transportation_system
    system.add_vehicle("V123", "Bus", "Downtown", "Available")
    system.update_vehicle("V123", location="Uptown", status="In-use")
    system.cursor.execute("SELECT * FROM vehicles WHERE vehicle_number = 'V123'")
    updated_vehicle = system.cursor.fetchone()
    assert updated_vehicle[3] == "Uptown"
    assert updated_vehicle[4] == "In-use"

def test_delete_vehicle(setup_transportation_system):
    system = setup_transportation_system
    system.add_vehicle("V123", "Bus", "Downtown", "Available")
    system.delete_vehicle("V123")
    system.cursor.execute("SELECT * FROM vehicles WHERE vehicle_number = 'V123'")
    vehicle = system.cursor.fetchone()
    assert vehicle is None

def test_search_vehicle(setup_transportation_system):
    system = setup_transportation_system
    system.add_vehicle("V123", "Bus", "Downtown", "Available")
    system.add_vehicle("V124", "Car", "Uptown", "In-use")
    
    # Search for bus
    system.search_vehicle(vehicle_type="Bus")
    system.search_vehicle(location="Uptown")
    system.search_vehicle(vehicle_number="V123")
