import sqlite3
import pytest
from survey_polling import setup_database, add_poll_question, record_response, display_polls

# Fixture to create an in-memory SQLite database for testing
@pytest.fixture
def mock_db():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE polls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            poll_id INTEGER,
            response TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (poll_id) REFERENCES polls (id)
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
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='polls'")
    assert cursor.fetchone() is not None  # Poll table should exist
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='responses'")
    assert cursor.fetchone() is not None  # Responses table should exist

# Test adding a poll question
def test_add_poll_question(monkeypatch, mock_db):
    def mock_get_entry(field):
        # Mock inputs for adding poll question
        fields = {
            'poll_question_entry.get': "What is your favorite color?"
        }
        return fields[field]

    # Monkeypatch database connection and GUI inputs
    monkeypatch.setattr('sqlite3.connect', lambda _: mock_db)
    monkeypatch.setattr('survey_polling.poll_question_entry', type('MockEntry', (), {'get': lambda: mock_get_entry('poll_question_entry.get')}))

    add_poll_question()

    # Validate the poll question was added to the database
    cursor = mock_db.cursor()
    cursor.execute("SELECT * FROM polls WHERE question = 'What is your favorite color?'")
    result = cursor.fetchone()
    assert result is not None
    assert result[1] == "What is your favorite color?"

# Test recording a response
def test_record_response(monkeypatch, mock_db):
    # Prepopulate the mock database with a poll
    cursor = mock_db.cursor()
    cursor.execute("INSERT INTO polls (question) VALUES ('What is your favorite fruit?')")
    poll_id = cursor.lastrowid
    mock_db.commit()

    def mock_get_entry(field):
        # Mock inputs for submitting a response
        fields = {
            'poll_listbox.curselection': [0],  # Mock selection of the first poll
            'response_entry.get': "Apple"  # Mock response input
        }
        return fields[field]

    # Monkeypatch database connection and GUI inputs
    monkeypatch.setattr('sqlite3.connect', lambda _: mock_db)
    monkeypatch.setattr('survey_polling.poll_listbox', type('MockListbox', (), {'get': lambda index: poll_id if index == [0] else None, 'curselection': lambda: [0]}))
    monkeypatch.setattr('survey_polling.response_entry', type('MockEntry', (), {'get': lambda: mock_get_entry('response_entry.get')}))

    record_response()

    # Validate the response was recorded in the database
    cursor.execute("SELECT * FROM responses WHERE poll_id = ? AND response = 'Apple'", (poll_id,))
    result = cursor.fetchone()
    assert result is not None
    assert result[2] == "Apple"

# Test displaying polls
def test_display_polls(monkeypatch, mock_db):
    # Prepopulate the mock database with polls
    cursor = mock_db.cursor()
    cursor.execute("INSERT INTO polls (question) VALUES ('What is your favorite animal?')")
    cursor.execute("INSERT INTO polls (question) VALUES ('What is your favorite food?')")
    mock_db.commit()

    # Mock database connection
    monkeypatch.setattr('sqlite3.connect', lambda _: mock_db)

    # Capture poll display results with monkeypatched messagebox
    display_results = []

    def mock_showinfo(title, message):
        display_results.append(message)

    monkeypatch.setattr('tkMessageBox.showinfo', mock_showinfo)

    display_polls()
    assert "What is your favorite animal?" in display_results[0]
    assert "What is your favorite food?" in display_results[0]
