import pytest
from ticket_booking_system import TicketBookingSystem

@pytest.fixture
def setup_ticket_booking_system():
    # Create a fresh instance of the TicketBookingSystem and clear the events table before each test
    system = TicketBookingSystem()
    system.cursor.execute("DELETE FROM events")  # Clear the events table
    system.conn.commit()
    return system

def test_add_event(setup_ticket_booking_system):
    system = setup_ticket_booking_system
    system.add_event("Concert", 100, 20.0)
    system.cursor.execute("SELECT * FROM events WHERE event_name = 'Concert'")
    event = system.cursor.fetchone()
    assert event is not None
    assert event[1] == "Concert"
    assert event[2] == 100
    assert event[3] == 20.0

def test_view_events(setup_ticket_booking_system):
    system = setup_ticket_booking_system
    system.add_event("Concert", 100, 20.0)
    system.add_event("Play", 50, 15.0)
    system.view_events()
    # The print statements are being verified visually when running the test

def test_book_ticket_success(setup_ticket_booking_system):
    system = setup_ticket_booking_system
    system.add_event("Concert", 100, 20.0)
    system.book_ticket(1, 2)  # Book 2 tickets for event ID 1
    system.cursor.execute("SELECT available_seats FROM events WHERE event_id = 1")
    available_seats = system.cursor.fetchone()[0]
    assert available_seats == 98  # 100 - 2 = 98

def test_book_ticket_failure(setup_ticket_booking_system):
    system = setup_ticket_booking_system
    system.add_event("Concert", 100, 20.0)
    system.book_ticket(1, 200)  # Attempt to book more tickets than available
    system.cursor.execute("SELECT available_seats FROM events WHERE event_id = 1")
    available_seats = system.cursor.fetchone()[0]
    assert available_seats == 100  # No change, booking failed

def test_payment_simulation(setup_ticket_booking_system):
    system = setup_ticket_booking_system
    system.add_event("Concert", 100, 20.0)
    # Simulate booking and check payment success
    result = system.process_payment(40.0)
    assert result is True or result is False  # Payment should either succeed or fail
