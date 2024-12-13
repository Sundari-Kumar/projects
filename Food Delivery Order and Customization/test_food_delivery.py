import sqlite3
import pytest
from food_delivery import setup_database, add_order, show_orders, update_order_status

# Fixture to create an in-memory SQLite database for testing
@pytest.fixture
def mock_db():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            food_item TEXT NOT NULL,
            customizations TEXT,
            status TEXT NOT NULL
        )
    """)
    conn.commit()
    yield conn  # Provide the connection to the tests
    conn.close()

# Test for setting up the database
def test_setup_database(monkeypatch, mock_db):
    # Mock the database connection
    monkeypatch.setattr('sqlite3.connect', lambda _: mock_db)
    setup_database()
    cursor = mock_db.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='orders'")
    assert cursor.fetchone() is not None  # Orders table should exist

# Test for adding an order
def test_add_order(monkeypatch, mock_db):
    # Mock the database connection
    monkeypatch.setattr('sqlite3.connect', lambda _: mock_db)
    add_order('John Doe', 'Pizza', 'Extra cheese, No mushrooms')

    cursor = mock_db.cursor()
    cursor.execute("SELECT * FROM orders WHERE customer_name = 'John Doe'")
    result = cursor.fetchone()

    assert result is not None
    assert result[1] == 'John Doe'
    assert result[2] == 'Pizza'
    assert result[3] == 'Extra cheese, No mushrooms'
    assert result[4] == 'Pending'

# Test for showing all orders
def test_show_orders(monkeypatch, mock_db):
    # Prepopulate mock database with orders
    cursor = mock_db.cursor()
    cursor.execute("INSERT INTO orders (customer_name, food_item, customizations, status) VALUES ('Jane Doe', 'Burger', 'No pickles', 'Pending')")
    mock_db.commit()

    # Capture the orders displayed
    orders = []
    def mock_showinfo(title, message):
        orders.append(message)

    monkeypatch.setattr('tkMessageBox.showinfo', mock_showinfo)
    show_orders()

    assert "Jane Doe - Burger: No pickles (Customizations: Pending)" in orders[0]
