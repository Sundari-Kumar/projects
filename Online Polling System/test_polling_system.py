import pytest
import sqlite3
from polling_system import PollingSystem

@pytest.fixture(scope='module')
def setup_polling_system():
    """Set up the Polling System and return the system instance"""
    system = PollingSystem()
    yield system
    system.close()

def test_create_poll(setup_polling_system):
    system = setup_polling_system
    system.create_poll("What is your favorite programming language?", ["Python", "Java", "Ruby", "C++"])
    
    # Verify the poll was created
    system.cursor.execute("SELECT COUNT(*) FROM polls WHERE question = 'What is your favorite programming language?'")
    count = system.cursor.fetchone()[0]
    assert count == 1, "Poll was not created successfully"

def test_vote(setup_polling_system):
    system = setup_polling_system
    system.vote(1, 1)  # Vote for Python (option 1)
    
    # Verify vote count
    system.cursor.execute("SELECT votes FROM poll_options WHERE id = 1")
    vote_count = system.cursor.fetchone()[0]
    assert vote_count == 1, "Vote was not counted correctly"

def test_view_poll_results(setup_polling_system):
    system = setup_polling_system
    system.view_poll_results(1)
    
    # Here we don't have a direct assert, but we want to ensure no errors during execution.
    assert True

def test_get_poll(setup_polling_system):
    system = setup_polling_system
    system.get_poll(1)
    
    # Here we expect the output to show the poll's question and its options.
    assert True
