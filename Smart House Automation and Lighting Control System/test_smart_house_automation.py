import sqlite3
import pytest
from smart_house_automation import setup_database, control_lights, show_light_status

# Fixture to create an in-memory SQLite database for testing
@pytest.fixture
def mock_db():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE lights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_name TEXT NOT NULL,
            light_status TEXT NOT NULL,
            timer TEXT
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
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='lights'")
    assert cursor.fetchone() is not None  # Lights table should exist

# Test turning lights on
def test_control_lights_on(monkeypatch, mock_db):
    # Mock database connection and function call
    monkeypatch.setattr('sqlite3.connect', lambda _: mock_db)
    control_lights('Living Room', 'On', '30')

    cursor = mock_db.cursor()
    cursor.execute("SELECT * FROM lights WHERE room_name = 'Living Room'")
    result = cursor.fetchone()

    assert result is not None
    assert result[1] == 'Living Room'
    assert result[2] == 'On'
    assert result[3] == '30'

# Test turning lights off
def test_control_lights_off(monkeypatch, mock_db):
    # First, turn the light on
    control_lights('Kitchen', 'On', '15')
    
    # Now turn it off
    control_lights('Kitchen', 'Off', None)

    cursor = mock_db.cursor()
    cursor.execute("SELECT * FROM lights WHERE room_name = 'Kitchen'")
    result = cursor.fetchone()

    assert result is not None
    assert result[2] == 'Off'
    assert result[3] is None

# Test viewing light status
def test_show_light_status(monkeypatch, mock_db):
    # Prepopulate the mock database with some lights
    cursor = mock_db.cursor()
    cursor.execute("INSERT INTO lights (room_name, light_status, timer) VALUES ('Living Room', 'On', '30')")
    cursor.execute("INSERT INTO lights (room_name, light_status, timer) VALUES ('Kitchen', 'Off', None)")
    mock_db.commit()

    # Capture the output of show_light_status
    light_list = []
    def mock_showinfo(title, message):
        light_list.append(message)

    monkeypatch.setattr('tkMessageBox.showinfo', mock_showinfo)

    show_light_status()

    assert "Living Room - Status: On (Timer: 30)" in light_list[0]
    assert "Kitchen - Status: Off (Timer: None)" in light_list[0]
