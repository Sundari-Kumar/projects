import sqlite3
import pytest
from expenses_tracking import setup_database, add_expense, show_expenses, clear_entries

# Fixture to create an in-memory SQLite database for testing
@pytest.fixture
def mock_db():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL
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
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='expenses'")
    assert cursor.fetchone() is not None  # Expenses table should exist

# Test adding an expense
def test_add_expense(monkeypatch, mock_db):
    # Mock database connection and function call
    monkeypatch.setattr('sqlite3.connect', lambda _: mock_db)
    add_expense('Food', 100.50)

    cursor = mock_db.cursor()
    cursor.execute("SELECT * FROM expenses WHERE category = 'Food'")
    result = cursor.fetchone()

    assert result is not None
    assert result[1] == 'Food'
    assert result[2] == 100.50

# Test viewing expenses
def test_show_expenses(monkeypatch, mock_db):
    # Prepopulate the mock database with some expenses
    cursor = mock_db.cursor()
    cursor.execute("INSERT INTO expenses (category, amount, date) VALUES ('Food', 100.50, '2024-12-12')")
    cursor.execute("INSERT INTO expenses (category, amount, date) VALUES ('Transport', 50.25, '2024-12-12')")
    mock_db.commit()

    # Capture the output of show_expenses
    expense_list = []
    def mock_showinfo(title, message):
        expense_list.append(message)

    monkeypatch.setattr('tkMessageBox.showinfo', mock_showinfo)

    show_expenses()

    assert "Food - Food: $100.50 on 2024-12-12" in expense_list[0]
    assert "Transport - Transport: $50.25 on 2024-12-12" in expense_list[0]
    assert "Total Expenses: $150.75" in expense_list[0]
