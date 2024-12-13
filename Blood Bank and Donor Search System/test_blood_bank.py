import sqlite3
import pytest
from blood_bank import setup_database, register_donor, search_donor, list_all_donors

# Fixture to create an in-memory SQLite database for testing
@pytest.fixture
def mock_db():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE donors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            blood_type TEXT NOT NULL,
            contact TEXT NOT NULL
        )
    """)
    conn.commit()
    yield conn  # Provide the connection to the tests
    conn.close()

# Test setup_database function
def test_setup_database(monkeypatch, mock_db):
    # Mock the database connection
    monkeypatch.setattr('sqlite3.connect', lambda _: mock_db)
    setup_database()
    cursor = mock_db.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='donors'")
    assert cursor.fetchone() is not None  # Table should exist

# Test registering a donor
def test_register_donor(monkeypatch, mock_db):
    def mock_get_entry(field):
        # Mock inputs for registration
        fields = {
            'reg_name_entry.get': "John Doe",
            'reg_blood_type_entry.get': "A+",
            'reg_contact_entry.get': "1234567890"
        }
        return fields[field]

    # Mock database connection and GUI inputs
    monkeypatch.setattr('sqlite3.connect', lambda _: mock_db)
    monkeypatch.setattr('blood_bank.reg_name_entry', type('MockEntry', (), {'get': lambda: mock_get_entry('reg_name_entry.get')}))
    monkeypatch.setattr('blood_bank.reg_blood_type_entry', type('MockEntry', (), {'get': lambda: mock_get_entry('reg_blood_type_entry.get')}))
    monkeypatch.setattr('blood_bank.reg_contact_entry', type('MockEntry', (), {'get': lambda: mock_get_entry('reg_contact_entry.get')}))

    register_donor()

    # Validate the donor was added to the database
    cursor = mock_db.cursor()
    cursor.execute("SELECT * FROM donors WHERE name = 'John Doe'")
    result = cursor.fetchone()
    assert result is not None
    assert result[1] == "John Doe"
    assert result[2] == "A+"
    assert result[3] == "1234567890"

# Test searching for a donor
def test_search_donor(monkeypatch, mock_db):
    # Prepopulate the mock database
    cursor = mock_db.cursor()
    cursor.execute("INSERT INTO donors (name, blood_type, contact) VALUES (?, ?, ?)", ("Jane Smith", "B+", "9876543210"))
    mock_db.commit()

    def mock_search_entry():
        return "B+"

    # Mock database connection and search input
    monkeypatch.setattr('sqlite3.connect', lambda _: mock_db)
    monkeypatch.setattr('blood_bank.search_blood_type_entry', type('MockEntry', (), {'get': mock_search_entry}))

    # Capture search results with monkeypatched messagebox
    search_results = []

    def mock_showinfo(title, message):
        search_results.append(message)

    monkeypatch.setattr('tkMessageBox.showinfo', mock_showinfo)

    search_donor()
    assert "Jane Smith - 9876543210" in search_results[0]

# Test listing all donors
def test_list_all_donors(monkeypatch, mock_db):
    # Prepopulate the mock database
    cursor = mock_db.cursor()
    cursor.executemany("INSERT INTO donors (name, blood_type, contact) VALUES (?, ?, ?)", [
        ("Alice", "O+", "5555555555"),
        ("Bob", "A-", "6666666666")
    ])
    mock_db.commit()

    # Mock database connection
    monkeypatch.setattr('sqlite3.connect', lambda _: mock_db)

    # Capture donor list results with monkeypatched messagebox
    donor_list_results = []

    def mock_showinfo(title, message):
        donor_list_results.append(message)

    monkeypatch.setattr('tkMessageBox.showinfo', mock_showinfo)

    list_all_donors()
    assert "Alice (O+) - 5555555555" in donor_list_results[0]
    assert "Bob (A-) - 6666666666" in donor_list_results[0]
