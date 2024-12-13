import sqlite3
import pytest
from event_scheduler import setup_database, add_event, display_events_for_date

# Fixture to create an in-memory SQLite database for testing
@pytest.fixture
def mock_db():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_name TEXT NOT NULL,
            event_date TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            description TEXT
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
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='events'")
    assert cursor.fetchone() is not None  # Events table should exist

# Test adding an event
def test_add_event(monkeypatch, mock_db):
    def mock_get_entry(field):
        # Mock inputs for adding event
        fields = {
            'event_name_entry.get': "Conference",
            'event_date_entry.get': "2024-12-25",
            'start_time_entry.get': "10:00",
            'end_time_entry.get': "12:00",
            'description_entry.get': "Tech Conference"
        }
        return fields[field]

    # Monkeypatch database connection and GUI inputs
    monkeypatch.setattr('sqlite3.connect', lambda _: mock_db)
    monkeypatch.setattr('event_scheduler.event_name_entry', type('MockEntry', (), {'get': lambda: mock_get_entry('event_name_entry.get')}))
    monkeypatch.setattr('event_scheduler.event_date_entry', type('MockEntry', (), {'get': lambda: mock_get_entry('event_date_entry.get')}))
    monkeypatch.setattr('event_scheduler.start_time_entry', type('MockEntry', (), {'get': lambda: mock_get_entry('start_time_entry.get')}))
    monkeypatch.setattr('event_scheduler.end_time_entry', type('MockEntry', (), {'get': lambda: mock_get_entry('end_time_entry.get')}))
    monkeypatch.setattr('event_scheduler.description_entry', type('MockEntry', (), {'get': lambda: mock_get_entry('description_entry.get')}))

    add_event()

    # Validate the event was added to the database
    cursor = mock_db.cursor()
    cursor.execute("SELECT * FROM events WHERE event_name = 'Conference'")
    result = cursor.fetchone()
    assert result is not None
    assert result[1] == "Conference"
    assert result[2] == "2024-12-25"

# Test displaying events for a specific date
def test_display_events_for_date(monkeypatch, mock_db):
    # Prepopulate the mock database with an event
    cursor = mock_db.cursor()
    cursor.execute("INSERT INTO events (event_name, event_date, start_time, end_time, description) VALUES ('Conference', '2024-12-25', '10:00', '12:00', 'Tech Conference')")
    mock_db.commit()

    # Mock database connection
    monkeypatch.setattr('sqlite3.connect', lambda _: mock_db)

    # Capture event display results with monkeypatched messagebox
    display_results = []

    def mock_showinfo(title, message):
        display_results.append(message)

    monkeypatch.setattr('tkMessageBox.showinfo', mock_showinfo)

    display_events_for_date()
    assert "Conference - Tech Conference (10:00 to 12:00)" in display_results[0]
