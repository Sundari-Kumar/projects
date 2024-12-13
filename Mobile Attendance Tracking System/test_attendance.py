import sqlite3
import pytest
from attendance import setup_database, mark_attendance, view_attendance, list_all_attendance

# Fixture to create an in-memory SQLite database for testing
@pytest.fixture
def mock_db():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            date TEXT NOT NULL,
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
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='attendance'")
    assert cursor.fetchone() is not None  # Table should exist

# Test marking attendance
def test_mark_attendance(monkeypatch, mock_db):
    def mock_get_entry(field):
        # Mock inputs for marking attendance
        fields = {
            'attendance_name_entry.get': "John Doe",
            'attendance_status_var.get': "Present"
        }
        return fields[field]

    # Monkeypatch database connection and GUI inputs
    monkeypatch.setattr('sqlite3.connect', lambda _: mock_db)
    monkeypatch.setattr('attendance.attendance_name_entry', type('MockEntry', (), {'get': lambda: mock_get_entry('attendance_name_entry.get')}))
    monkeypatch.setattr('attendance.attendance_status_var', type('MockStatus', (), {'get': lambda: mock_get_entry('attendance_status_var.get')}))

    mark_attendance()

    # Validate the attendance was marked in the database
    cursor = mock_db.cursor()
    cursor.execute("SELECT * FROM attendance WHERE name = 'John Doe'")
    result = cursor.fetchone()
    assert result is not None
    assert result[1] == "John Doe"
    assert result[2] is not None  # Ensure the date is stored
    assert result[3] == "Present"

# Test viewing attendance
def test_view_attendance(monkeypatch, mock_db):
    # Prepopulate the mock database
    cursor = mock_db.cursor()
    cursor.execute("INSERT INTO attendance (name, date, status) VALUES (?, ?, ?)", ("John Doe", "2024-12-13 10:00:00", "Present"))
    mock_db.commit()

    def mock_view_entry():
        return "John Doe", "2024-12-13"

    # Mock database connection and view input
    monkeypatch.setattr('sqlite3.connect', lambda _: mock_db)
    monkeypatch.setattr('attendance.view_name_entry', type('MockEntry', (), {'get': lambda: mock_view_entry()[0]}))
    monkeypatch.setattr('attendance.view_date_entry', type('MockEntry', (), {'get': lambda: mock_view_entry()[1]}))

    # Capture view results with monkeypatched messagebox
    view_results = []

    def mock_showinfo(title, message):
        view_results.append(message)

    monkeypatch.setattr('tkMessageBox.showinfo', mock_showinfo)

    view_attendance()
    assert "John Doe" in view_results[0]
    assert "Present" in view_results[0]

# Test listing all attendance records
def test_list_all_attendance(monkeypatch, mock_db):
    # Prepopulate the mock database
    cursor = mock_db.cursor()
    cursor.executemany("INSERT INTO attendance (name, date, status) VALUES (?, ?, ?)", [
        ("Jane Doe", "2024-12-12 09:00:00", "Absent"),
        ("Mark Smith", "2024-12-13 09:00:00", "Present")
    ])
    mock_db.commit()

    # Mock database connection
    monkeypatch.setattr('sqlite3.connect', lambda _: mock_db)

    # Capture attendance list results with monkeypatched messagebox
    attendance_list_results = []

    def mock_showinfo(title, message):
        attendance_list_results.append(message)

    monkeypatch.setattr('tkMessageBox.showinfo', mock_showinfo)

    list_all_attendance()
    assert "Jane Doe" in attendance_list_results[0]
    assert "Mark Smith" in attendance_list_results[0]
