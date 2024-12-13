import sqlite3
import random

# Ticket Booking System Class
class TicketBookingSystem:
    def __init__(self):
        self.conn = sqlite3.connect('ticket_booking.db')
        self.cursor = self.conn.cursor()
        self._setup_db()

    def _setup_db(self):
        # Create a table to store ticket details
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            event_id INTEGER PRIMARY KEY,
            event_name TEXT NOT NULL,
            available_seats INTEGER NOT NULL,
            ticket_price REAL NOT NULL
        )""")
        self.conn.commit()

    def add_event(self, event_name, available_seats, ticket_price):
        # Add a new event to the system
        self.cursor.execute("""
        INSERT INTO events (event_name, available_seats, ticket_price) 
        VALUES (?, ?, ?)""", (event_name, available_seats, ticket_price))
        self.conn.commit()
        print(f"Event '{event_name}' added successfully.")

    def view_events(self):
        # View all available events
        self.cursor.execute("SELECT * FROM events")
        events = self.cursor.fetchall()
        if events:
            print("\nAvailable Events:")
            for event in events:
                print("Event ID: {}, Name: {}, Available Seats: {}, Price: ${}".format(
                    event[0], event[1], event[2], event[3]))
        else:
            print("No events available.")

    def book_ticket(self, event_id, num_tickets):
        # Book tickets for a selected event
        self.cursor.execute("SELECT * FROM events WHERE event_id = ?", (event_id,))
        event = self.cursor.fetchone()

        if event:
            event_name, available_seats, ticket_price = event[1], event[2], event[3]
            total_price = ticket_price * num_tickets

            if num_tickets <= available_seats:
                print(f"\nBooking {num_tickets} tickets for '{event_name}'")
                print(f"Total Price: ${total_price}")
                if self.process_payment(total_price):
                    # Update available seats in the database
                    new_seats = available_seats - num_tickets
                    self.cursor.execute("UPDATE events SET available_seats = ? WHERE event_id = ?",
                                        (new_seats, event_id))
                    self.conn.commit()
                    print(f"\nBooking successful! {num_tickets} tickets booked for '{event_name}'.")
                else:
                    print("\nPayment failed! Try again later.")
            else:
                print("\nNot enough available seats for your request.")
        else:
            print("\nEvent not found.")

    def process_payment(self, amount):
        # Simulate payment gateway
        print(f"\nProcessing payment of ${amount}...")
        payment_successful = random.choice([True, False])  # Simulating payment success/failure
        if payment_successful:
            print("Payment successful!")
            return True
        else:
            print("Payment failed. Please try again.")
            return False

    def close(self):
        self.conn.close()
