import sqlite3
import pytest
from real_estate import setup_database, add_property, search_property, list_all_properties

# Fixture to create an in-memory SQLite database for testing
@pytest.fixture
def mock_db():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE properties (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            address TEXT NOT NULL,
            price INTEGER NOT NULL,
            owner TEXT NOT NULL
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
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='properties'")
    assert cursor.fetchone() is not None  # Table should exist

# Test adding a property
def test_add_property(monkeypatch, mock_db):
    def mock_get_entry(field):
        # Mock inputs for property addition
        fields = {
            'reg_address_entry.get': "123 Main St",
            'reg_price_entry.get': "500000",
            'reg_owner_entry.get': "Alice Smith"
        }
        return fields[field]

    # Monkeypatch database connection and GUI inputs
    monkeypatch.setattr('sqlite3.connect', lambda _: mock_db)
    monkeypatch.setattr('real_estate.reg_address_entry', type('MockEntry', (), {'get': lambda: mock_get_entry('reg_address_entry.get')}))
    monkeypatch.setattr('real_estate.reg_price_entry', type('MockEntry', (), {'get': lambda: mock_get_entry('reg_price_entry.get')}))
    monkeypatch.setattr('real_estate.reg_owner_entry', type('MockEntry', (), {'get': lambda: mock_get_entry('reg_owner_entry.get')}))

    add_property()

    # Validate the property was added to the database
    cursor = mock_db.cursor()
    cursor.execute("SELECT * FROM properties WHERE address = '123 Main St'")
    result = cursor.fetchone()
    assert result is not None
    assert result[1] == "123 Main St"
    assert result[2] == 500000
    assert result[3] == "Alice Smith"

# Test searching for a property
def test_search_property(monkeypatch, mock_db):
    # Prepopulate the mock database
    cursor = mock_db.cursor()
    cursor.execute("INSERT INTO properties (address, price, owner) VALUES (?, ?, ?)", ("456 Elm St", 400000, "Bob Johnson"))
    mock_db.commit()

    def mock_search_entry():
        return "Elm"

    # Mock database connection and search input
    monkeypatch.setattr('sqlite3.connect', lambda _: mock_db)
    monkeypatch.setattr('real_estate.search_address_entry', type('MockEntry', (), {'get': mock_search_entry}))

    # Capture search results with monkeypatched messagebox
    search_results = []

    def mock_showinfo(title, message):
        search_results.append(message)

    monkeypatch.setattr('tkMessageBox.showinfo', mock_showinfo)

    search_property()
    assert "456 Elm St - 400000 - Bob Johnson" in search_results[0]

# Test listing all properties
def test_list_all_properties(monkeypatch, mock_db):
    # Prepopulate the mock database
    cursor = mock_db.cursor()
    cursor.executemany("INSERT INTO properties (address, price, owner) VALUES (?, ?, ?)", [
        ("789 Oak St", 600000, "Charlie Brown"),
        ("101 Pine St", 700000, "David Green")
    ])
    mock_db.commit()

    # Mock database connection
    monkeypatch.setattr('sqlite3.connect', lambda _: mock_db)

    # Capture donor list results with monkeypatched messagebox
    property_list_results = []

    def mock_showinfo(title, message):
        property_list_results.append(message)

    monkeypatch.setattr('tkMessageBox.showinfo', mock_showinfo)

    list_all_properties()
    assert "789 Oak St - 600000 - Charlie Brown" in property_list_results[0]
    assert "101 Pine St - 700000 - David Green" in property_list_results[0]
