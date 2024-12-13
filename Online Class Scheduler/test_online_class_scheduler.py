import sqlite3
import pytest
from online_class_scheduler import setup_database, add_class_schedule, display_scheduled_classes, clear_entries

# Fixture to create an in-memory SQLite database for testing
@pytest.fixture
def mock_db():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE classes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_name TEXT NOT NULL,
            instructor TEXT NOT NULL,
            date TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL
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
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='classes'")
    assert cursor.fetchone() is not None  # Classes table should exist

# Test adding a class schedule
def test_add_class_schedule(monkeypatch, mock_db):
    def mock_get_entry(field):
        # Mock inputs for adding class schedule
        fields = {
            'course_name_entry.get': "Math 101",
            'instructor_entry.get': "Dr. Smith",
            'date_entry.get': "2024-12-15",
            'start_time_entry.get': "09:00",
            'end_time_entry.get': "10:30"
        }
        return fields[field]

    # Monkeypatch database connection and GUI inputs
    monkeypatch.setattr('sqlite3.connect', lambda _: mock_db)
    monkeypatch.setattr('online_class_scheduler.course_name_entry', type('MockEntry', (), {'get': lambda: mock_get_entry('course_name_entry.get')}))
    monkeypatch.setattr('online_class_scheduler.instructor_entry', type('MockEntry', (), {'get': lambda: mock_get_entry('instructor_entry.get')}))
    monkeypatch.setattr('online_class_scheduler.date_entry', type('MockEntry', (), {'get': lambda: mock_get_entry('date_entry.get')}))
    monkeypatch.setattr('online_class_scheduler.start_time_entry', type('MockEntry', (), {'get': lambda: mock_get_entry('start_time_entry.get')}))
    monkeypatch.setattr('online_class_scheduler.end_time_entry', type('MockEntry', (), {'get': lambda: mock_get_entry('end_time_entry.get')}))

    add_class_schedule()

    # Validate the class schedule was added to the database
    cursor = mock_db.cursor()
    cursor.execute("SELECT * FROM classes WHERE course_name = 'Math 101' AND instructor = 'Dr. Smith'")
    result = cursor.fetchone()
    assert result is not None
    assert result[1] == "Math 101"
    assert result[2] == "Dr. Smith"

# Test displaying scheduled classes
def test_display_scheduled_classes(monkeypatch, mock_db):
    # Prepopulate the mock database with a class schedule
    cursor = mock_db.cursor()
    cursor.execute("INSERT INTO classes (course_name, instructor, date, start_time, end_time) VALUES ('Physics 101', 'Dr. Green', '2024-12-16', '10:00', '11:30')")
    mock_db.commit()

    # Mock database connection
    monkeypatch.setattr('sqlite3.connect', lambda _: mock_db)

    # Capture class display results with monkeypatched messagebox
    display_results = []

    def mock_showinfo(title, message):
        display_results.append(message)

    monkeypatch.setattr('tkMessageBox.showinfo', mock_showinfo)

    display_scheduled_classes()
    assert "Physics 101 - Dr. Green (2024-12-16) from 10:00 to 11:30" in display_results[0]
