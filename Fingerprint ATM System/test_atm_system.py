import pytest
from atm_system import ATMSystem
import sqlite3

@pytest.fixture
def setup_atm_system():
    # Create a fresh instance of ATM system and mock database for testing
    atm = ATMSystem()
    atm.cursor.execute("DELETE FROM users")  # Clear the database before each test
    atm.conn.commit()
    return atm

def test_add_user(setup_atm_system):
    # Test user addition
    atm = setup_atm_system
    atm.add_user("Alice", "f12345", 1000)
    atm.cursor.execute("SELECT * FROM users WHERE fingerprint_id = 'f12345'")
    user = atm.cursor.fetchone()
    assert user is not None
    assert user[1] == "Alice"
    assert user[2] == "f12345"
    assert user[3] == 1000.0

def test_balance_check(setup_atm_system):
    # Test balance check functionality
    atm = setup_atm_system
    atm.add_user("Alice", "f12345", 1000)
    atm.cursor.execute("SELECT * FROM users WHERE fingerprint_id = 'f12345'")
    user = atm.cursor.fetchone()
    # Simulate balance check
    assert user[3] == 1000.0

def test_withdraw(setup_atm_system):
    # Test withdrawing money
    atm = setup_atm_system
    atm.add_user("Alice", "f12345", 1000)
    atm.cursor.execute("SELECT * FROM users WHERE fingerprint_id = 'f12345'")
    user = atm.cursor.fetchone()

    atm.withdraw(user, 200)
    atm.cursor.execute("SELECT * FROM users WHERE fingerprint_id = 'f12345'")
    updated_user = atm.cursor.fetchone()
    assert updated_user[3] == 800.0

def test_deposit(setup_atm_system):
    # Test depositing money
    atm = setup_atm_system
    atm.add_user("Alice", "f12345", 1000)
    atm.cursor.execute("SELECT * FROM users WHERE fingerprint_id = 'f12345'")
    user = atm.cursor.fetchone()

    atm.deposit(user, 500)
    atm.cursor.execute("SELECT * FROM users WHERE fingerprint_id = 'f12345'")
    updated_user = atm.cursor.fetchone()
    assert updated_user[3] == 1500.0

