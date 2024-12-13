import pytest
from security_system import SecuritySystem
import random

# Mock the random.choice function for predictable test results
@pytest.fixture
def mock_random_choice():
    # This mock will always return True (Intruder Detected)
    def mock_choice(options):
        return True
    original_random_choice = random.choice
    random.choice = mock_choice
    yield
    random.choice = original_random_choice  # Restore the original random.choice

def test_intruder_detection(mock_random_choice):
    system = SecuritySystem()
    system.detect_intruder()

    # Check if an intruder was detected and the alarm was triggered
    assert system.intruder_detected is True

    # Check if an event was logged
    system.cursor.execute("SELECT * FROM intruder_log")
    logs = system.cursor.fetchall()
    assert len(logs) == 1
    assert logs[0][2] == "Intruder Detected"  # Check that the status is correct

    system.close()

def test_no_intruder_detection(mock_random_choice):
    # Modify the mock to simulate no intruder detected
    def mock_choice(options):
        return False
    original_random_choice = random.choice
    random.choice = mock_choice
    system = SecuritySystem()
    system.detect_intruder()

    # Check if no intruder was detected
    assert system.intruder_detected is False

    # Check if an event was logged
    system.cursor.execute("SELECT * FROM intruder_log")
    logs = system.cursor.fetchall()
    assert len(logs) == 1
    assert logs[0][2] == "No Intruder"  # Check that the status is correct

    system.close()

